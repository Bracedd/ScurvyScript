from tokens import Integer, Float, String, Operation, Boolean, Comparison, Variable, Declaration, Print

class InterpreterError(Exception):
    pass

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.variables = {}

    def interpret(self):
        results = []
        for statement in self.tree:
            result = self.execute(statement)
            if result is not None:
                results.append(result)
        return results

    def execute(self, node):
        if isinstance(node, tuple):
            node_type = node[0]
            if node_type == 'declaration':
                return self.handle_declaration(node)
            elif node_type == 'print':
                return self.handle_print(node)
            elif node_type == 'if':
                return self.handle_if(node)
            elif node_type == 'while':
                return self.handle_while(node)
            elif node_type == 'binary_op':
                return self.handle_binary_op(node)
            elif node_type == 'unary_op':
                return self.handle_unary_op(node)
            elif node_type == 'literal':
                return self.handle_literal(node)
            elif node_type == 'variable':
                return self.handle_variable(node)
        raise InterpreterError(f"Unknown node type: {node}")

    def handle_declaration(self, node):
        _, var, value = node
        self.variables[var.value] = self.execute(value)

    def handle_print(self, node):
        _, expr = node
        value = self.execute(expr)
        print(value)
        return value

    def handle_if(self, node):
        _, conditions = node
        for condition, action in conditions:
            if self.execute(condition):
                return self.execute(action)
        return None

    def handle_while(self, node):
        _, condition, body = node
        results = []
        while self.execute(condition):
            results.append(self.execute(body))
        return results

    def handle_binary_op(self, node):
        _, op, left, right = node
        left_val = self.execute(left)
        right_val = self.execute(right)
        if op.value == '+':
            return left_val + right_val
        if op.value == '-':
            return left_val - right_val
        if op.value == '*':
            return left_val * right_val
        if op.value == '/':
            if right_val == 0:
                raise InterpreterError("Division by zero")
            return left_val / right_val
        raise InterpreterError(f"Unknown operator: {op.value}")

    def handle_unary_op(self, node):
        _, op, expr = node
        value = self.execute(expr)
        if op.value == '-':
            return -value
        if op.value == 'nay':
            return not value
        raise InterpreterError(f"Unknown unary operator: {op.value}")

    def handle_literal(self, node):
        _, token = node
        if isinstance(token, Integer):
            return int(token.value)
        if isinstance(token, Float):
            return float(token.value)
        if isinstance(token, String):
            return token.value
        if isinstance(token, Boolean):
            return 1 if token.value == 'aye' else 0

    def handle_variable(self, node):
        _, var = node
        if var.value not in self.variables:
            raise InterpreterError(f"Undefined variable: {var.value}")
        return self.variables[var.value]
