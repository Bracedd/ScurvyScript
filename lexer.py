from tokens import Token, Integer, Float, Operation, Declaration, Variable, Boolean, Comparison, Reserved, Print, String

class Lexer:
    digits = '0123456789'
    letters = 'abcdefghijklmnopqrstuvwxyz'
    operations = '+-/*()='
    stopwords = [" "]
    declarations = ['yeet']
    boolean = ["with", "or", "nay"]  
    comparisons = ['>', '<', '>=', '<=', '?=']
    specialCharacters = "<>=?"
    reserved = ['if', 'but_if', 'by_chance', 'bet', 'print']

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None

    def tokenize(self):
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()
            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()
            elif self.char in Lexer.stopwords:
                self.move()
                continue
            elif self.char in Lexer.letters:
                word = self.extract_word()
                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    if word == 'print':
                        self.token = Print(word)
                    else:
                        self.token = Reserved(word)
                else:
                    self.token = Variable(word)
            elif self.char in Lexer.specialCharacters:
                comparisonOperator = ''
                while self.char in Lexer.specialCharacters and self.idx < len(self.text):
                    comparisonOperator += self.char
                    self.move()
                self.token = Comparison(comparisonOperator)
            elif self.char == '"':
                self.token = self.extract_string()
            else:
                self.move()
                continue

            self.tokens.append(self.token)

        return self.tokens

    def extract_number(self):
        number = ''
        isFloat = False
        while (self.char in Lexer.digits or (self.char =='.')) and (self.idx < len(self.text)):
            if self.char == '.':
                isFloat = True
            number += self.char
            self.move()

        return Integer(number) if not isFloat else Float(number)
    
    def extract_word(self):
        word = ''
        while self.char in Lexer.letters and self.idx < len(self.text):
            word += self.char
            self.move()

        return word

    def extract_string(self):
        string = ''
        self.move()  # Skip the opening quote
        while self.char != '"' and self.idx < len(self.text):
            string += self.char
            self.move()
        self.move()  # Skip the closing quote
        return String(string)

    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
