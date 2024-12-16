from tokens import Declaration, Print, Reserved, Operation, Variable, Integer, Float, String, Boolean, Comparison

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while self.current < len(self.tokens):
            statements.append(self.statement())
        return statements

    def statement(self):
        token = self.peek()
        if isinstance(token, Declaration):
            return self.declaration()
        elif isinstance(token, Print):
            return self.print_statement()
        elif isinstance(token, Reserved) and token.value == "if":
            return self.if_statement()
        else:
            raise ParseError(f"Unexpected token: {token}")

    def declaration(self):
        self.consume(Declaration)
        variable = self.consume(Variable)
        self.consume(Operation, "=")
        value = self.expression()
        return ("declaration", variable, value)

    def print_statement(self):
        self.consume(Print)
        self.consume(Operation, "(")
        value = self.expression()
        self.consume(Operation, ")")
        return ("print", value)

    def if_statement(self):
        self.consume(Reserved, "if")
        condition = self.expression()
        self.consume(Reserved, "bet")
        action = self.statement()
        return ("if", condition, action)

    def expression(self):
        return self.comparison()

    def comparison(self):
        left = self.primary()
        while self.match(Comparison):
            operator = self.advance()
            right = self.primary()
            left = ("binary_op", operator, left, right)
        return left

    def primary(self):
        token = self.peek()
        if isinstance(token, (Integer, Float, String, Variable)):
            return ("literal", self.advance())
        raise ParseError(f"Unexpected token: {token}")

    def match(self, type, value=None):
        token = self.peek()
        return isinstance(token, type) and (value is None or token.value == value)

    def consume(self, type, value=None):
        if self.match(type, value):
            return self.advance()
        raise ParseError(f"Expected {type.__name__} with value {value}, got {self.peek()}")

    def advance(self):
        token = self.peek()
        self.current += 1
        return token

    def peek(self):
        return self.tokens[self.current] if self.current < len(self.tokens) else None
