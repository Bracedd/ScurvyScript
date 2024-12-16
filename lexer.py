from tokens import Token, Integer, Float, String, Operation, Declaration, Variable, Boolean, Comparison, Reserved, Print

class Lexer:
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    operations = "+-/*=()"
    reserved_keywords = {"print": Print, "if": Reserved, "but_if": Reserved, "by_chance": Reserved, "bet": Reserved, "yeet": Declaration}
    comparisons = [">", "<", ">=", "<=", "?="]

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx] if self.text else None

    def tokenize(self):
        while self.char:
            if self.char in self.digits:
                self.tokens.append(self.extract_number())
            elif self.char in self.letters:
                self.tokens.append(self.extract_word())
            elif self.char in self.operations:
                self.tokens.append(Operation(self.char))
                self.advance()
            elif self.char in [' ', '\t', '\n']:
                self.advance()  # Skip whitespace
            elif self.char == '"':
                self.tokens.append(self.extract_string())
            else:
                raise ValueError(f"Unexpected character: {self.char}")
        return self.tokens

    def extract_number(self):
        num = ""
        is_float = False
        while self.char and (self.char in self.digits or (self.char == "." and not is_float)):
            if self.char == ".":
                is_float = True
            num += self.char
            self.advance()
        return Float(num) if is_float else Integer(num)

    def extract_word(self):
        word = ""
        while self.char and self.char in self.letters:
            word += self.char
            self.advance()
        if word in self.reserved_keywords:
            return self.reserved_keywords[word](word)
        return Variable(word)

    def extract_string(self):
        string = ""
        self.advance()  # Skip opening quote
        while self.char and self.char != '"':
            string += self.char
            self.advance()
        self.advance()  # Skip closing quote
        return String(string)

    def advance(self):
        self.idx += 1
        self.char = self.text[self.idx] if self.idx < len(self.text) else None
