import sys
from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data

base = Data()

def run_scurvyscript(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(ast)
    result = interpreter.interpret()
    
    # Format the result
    if isinstance(result, list):
        return '\n'.join(str(item) for item in result if item is not None)
    elif result is not None:
        return str(result)
    return ''

# Read the input from stdin (which will be passed by subprocess)
text = sys.stdin.read()

print(f"Input received: {text}")  # Debugging: Print the received input

output = run_scurvyscript(text)
print(output)

