class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx] if self.tokens else None

    def factor(self):
        if self.token is None:
            return None

        if self.token.type in ("INT", "FLT"):
            value = self.token
            self.move()
            return value

        elif self.token.value == '(':
            self.move()
            expression = self.boolean_expression()
            if self.token and self.token.value == ')':
                self.move()
            return expression
        
        elif self.token.value == 'nay':
            operator = self.token
            self.move()
            return [operator, self.boolean_expression()]

        elif self.token.type.startswith('VAR'):
            value = self.token
            self.move()
            return value

        elif self.token.value in ('+', '-'):
            operator = self.token
            self.move()
            operand = self.boolean_expression()
            return [operator, operand]

        return None

    def term(self):
        if self.token is None:
            return None

        left_node = self.factor()
        if left_node is None:
            return None

        while self.token and self.token.value in ("*", "/"):
            operator = self.token
            self.move()
            right_node = self.factor()
            if right_node is None:
                return None
            left_node = [left_node, operator, right_node]

        return left_node
    
    def if_statement(self):
        self.move()
        condition = self.boolean_expression()

        if self.token.value == 'bet':
            self.move()
            action = self.statement()

            return condition, action
        
        elif self.tokens[self.idx-1].value == 'bet':
            action = self.statement()
            return condition, action


    def if_statements(self):
        conditions = []
        actions = []

        if_statement = self.if_statement()
        conditions.append(if_statement[0])
        actions.append(if_statement[1])

        while self.token and self.token.value == 'but_if':  # Check if self.token is not None
            if_statement = self.if_statement()
            conditions.append(if_statement[0])
            actions.append(if_statement[1])

        if self.token and self.token.value == 'by_chance':  # Check if self.token is not None
            self.move()
            self.move()
            else_action = self.statement()

            return [conditions, actions, else_action]

        return [conditions, actions]


    def comp_expression(self):
        left_node = self.expression()
        while self.token and self.token.type == 'COMP':  # Check if self.token is not None
            operator = self.token
            self.move()
            right_node = self.expression()
            left_node = [left_node, operator, right_node]

        return left_node



    def boolean_expression(self):
        left_node = self.comp_expression()
        while self.token and self.token.type == "BOOL":
            operator = self.token
            self.move()
            right_node = self.comp_expression()
            left_node = [left_node, operator, right_node]

        return left_node

    def expression(self):
        left_node = self.term()

        while self.token and self.token.value in ("+", "-"):
            operator = self.token
            self.move()
            right_node = self.term()
            if right_node is None:
                return None
            left_node = [left_node, operator, right_node]

        return left_node

    def variable(self):
        if self.token and self.token.type.startswith('VAR'):
            variable = self.token
            self.move()
            return variable
        return None

    def statement(self):
        if self.token is None:
            return None

        if self.token.type == 'DECL':
            self.move()
            left_node = self.variable()
            if left_node is None:
                return None
            if self.token and self.token.value == '=':
                operation = self.token
                self.move()
                right_node = self.boolean_expression()
                return [left_node, operation, right_node]

        elif self.token.type in ("INT", "FLT", "OP") or self.token.value == 'nay':
            return self.boolean_expression()
        
        elif self.token.value == 'if':
            return [self.token, self.if_statements()]

        return None

    def parse(self):
        if not self.tokens:
            return None
        return self.statement()

    def move(self):
        self.idx += 1
        self.token = self.tokens[self.idx] if self.idx < len(self.tokens) else None
