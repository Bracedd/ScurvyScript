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

        elif self.token.type.startswith('VAR'):
            value = self.token
            self.move()
            return value

        elif self.token.value in ('+', '-'):
            operator = self.token
            self.move()
            operand = self.factor()
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


    def boolean_expression(self):
        left_node = self.expression()

        while self.token and self.token.type == "BOOL":
            operator = self.token
            self.move()
            right_node = self.expression()
            if right_node is None:
                return None
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

        elif self.token.type in ("INT", "FLT", "OP"):
            return self.boolean_expression()

        return None

    def parse(self):
        if not self.tokens:
            return None
        return self.statement()

    def move(self):
        self.idx += 1
        self.token = self.tokens[self.idx] if self.idx < len(self.tokens) else None
