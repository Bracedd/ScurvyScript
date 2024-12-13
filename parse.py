class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        if self.tokens:  # Check if tokens is not empty
            self.token = self.tokens[self.idx]
        else:
            self.token = None # Handle empty input

    def factor(self):
        if self.token is None: # Handle cases where token is none
            return None
        if self.token.type == "INT" or self.token.type == 'FLT':
            return self.token
        elif self.token.value == '(':
            self.move()
            expression = self.expression()
            if self.token and self.token.value == ')': #check for closing parenthesis
                self.move()
            return expression
        
        elif self.token.type.startswith('VAR'):
            return self.token   
    
        return None # Added to handle unexpected tokens in factor

    def term(self):
      if self.token is None:
          return None
      left_node = self.factor()
      if left_node is None:
          return None
      self.move()
      while self.token and (self.token.value == "*" or self.token.value == '/'): #check if token exists
          operation = self.token
          self.move()
          right_node = self.factor()
          if right_node is None:
              return None
          self.move()
          left_node = [left_node, operation, right_node]

      return left_node
    
    def expression(self):
        if self.token is None:
            return None
        left_node = self.term()
        if left_node is None:
            return None
        while self.token and (self.token.value == "+" or self.token.value == '-'): #check if token exists
            operation = self.token
            self.move()
            right_node = self.term()
            if right_node is None:
                return None
            left_node = [left_node, operation, right_node]

        return left_node
    
    def variable(self):
        if self.token and self.token.type.startswith('VAR'): #check if token exists
            return self.token
        return None

    def statement(self):
        if self.token is None:
            return None
        if self.token.type == 'DECL':
            self.move()
            left_node = self.variable()
            if left_node is None:
                return None # Handle if variable is invalid
            self.move()
            if self.token and self.token.value == '=': # Correct comparison here
                operation = self.token
                self.move()
                right_node = self.expression()
                return [left_node, operation, right_node]

        elif self.token.type == 'INT' or self.token.type == 'FLT' or self.token.type == 'OP':
            return self.expression()
        return None # added to handle cases where statement could not be parsed

    def parse(self):
        if self.tokens:
            return self.statement()
        return None


    def move(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
        else:
            self.token = None # Set token to None when end is reached