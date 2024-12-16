from flask import Flask, request, jsonify, render_template
from lexer import Lexer
from parse import Parser, ParseError
from interpreter import Interpreter, InterpreterError

app = Flask(__name__)

def run_scurvyscript(code):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        result = interpreter.interpret()
        
        return [str(item) for item in result if item is not None]
    except (ParseError, InterpreterError) as e:
        return [f"ScurvyScript Error: {str(e)}"]
    except Exception as e:
        return [f"Unexpected Error: {str(e)}"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json['code']
    results = run_scurvyscript(code)
    return jsonify({'result': results})

if __name__ == '__main__':
    app.run(debug=True)

