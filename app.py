from flask import Flask, render_template, request, jsonify, send_from_directory
from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data
import os

app = Flask(__name__)

base = Data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    code = request.json['code']
    
    tokenizer = Lexer(code)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter(tree, base)
    result = interpreter.interpret()
    
    return jsonify({'result': str(result) if result is not None else ''})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0', port=int(os.environ.get('PORT', 8080)))
