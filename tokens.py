class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"

class Integer(Token):
    def __init__(self, value):
        super().__init__("INT", value)

class Float(Token):
    def __init__(self, value):
        super().__init__("FLT", value)

class String(Token):
    def __init__(self, value):
        super().__init__("STR", value)

class Operation(Token):
    def __init__(self, value):
        super().__init__("OP", value)

class Declaration(Token):
    def __init__(self, value):
        super().__init__("DECL", value)

class Variable(Token):
    def __init__(self, value):
        super().__init__("VAR", value)

class Boolean(Token):
    def __init__(self, value):
        super().__init__("BOOL", value)

class Comparison(Token):
    def __init__(self, value):
        super().__init__("COMP", value)

class Reserved(Token):
    def __init__(self, value):
        super().__init__("RSV", value)

class Print(Token):
    def __init__(self, value):
        super().__init__("PRINT", value)

class While(Token):
    def __init__(self, value):
        super().__init__("WHILE", value)

