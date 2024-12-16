class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return str(self.value)
    
class Doubloon(Token):
    def __init__(self, value):
        super().__init__("DOUBLOON", value)

class Piece8(Token):
    def __init__(self, value):
        super().__init__("PIECE8", value)

class Operation(Token):
    def __init__(self, value):
        super().__init__("OP", value)

class Declaration(Token):
    def __init__(self, value):
        super().__init__("DECL", value)

class Booty(Token):
    def __init__(self, value):
        super().__init__("BOOTY(?)", value) # Variable name, BOOTY, data type
        # hoist ye_flag = 5 # BOOTY(?)

class Boolean(Token):
    def __init__(self, value):
        super().__init__("BOOL", value)
    
class Comparison(Token):
    def __init__(self, value):
        super().__init__("COMP", value)

class Reserved(Token):
    def __init__(self, value):
        super().__init__("RSV", value)

