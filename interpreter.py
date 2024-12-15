from tokens import Integer, Float, Reserved, Print, String, Variable, Declaration

class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base

    def read_INT(self, value):
        return int(value)
    
    def read_FLT(self, value):
        return float(value)
    
    def read_STR(self, value):
        return str(value)
    
    def read_VAR(self, id):
        variable = self.data.read(id)
        return variable.value

    def compute_bin(self, left, op, right):
        if isinstance(left, Variable):
            left = self.read_VAR(left.value)
        if isinstance(right, Variable):
            right = self.read_VAR(right.value)

        if op.value == "+":
            output = left + right
        elif op.value == "-":
            output = left - right
        elif op.value == "*":
            output = left * right
        elif op.value == "/":
            output = left / right
        elif op.value == ">":
            output = 1 if left > right else 0
        elif op.value == ">=":
            output = 1 if left >= right else 0
        elif op.value == "<":
            output = 1 if left < right else 0
        elif op.value == "<=":
            output = 1 if left <= right else 0
        elif op.value == "?=":
            output = 1 if left == right else 0
        elif op.value == "and":
            output = 1 if left and right else 0
        elif op.value == "or":
            output = 1 if left or right else 0

        return Integer(output) if isinstance(left, int) and isinstance(right, int) else Float(output)
        
    def compute_unary(self, operator, operand):
        if isinstance(operand, Variable):
            operand = self.read_VAR(operand.value)

        if operator.value == "+":
            output = +operand
        elif operator.value == "-":
            output = -operand
        elif operator.value == "not":
            output = 1 if not operand else 0
        
        return Integer(output) if isinstance(operand, int) else Float(output)

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        if isinstance(tree, list):
            if isinstance(tree[0], Print):
                value = self.interpret(tree[1])
                if isinstance(value, (Integer, Float, String)):
                    print(value.value)
                else:
                    print(value)
                return value
            elif isinstance(tree[0], Declaration):
                # Handle variable declaration
                var_name = tree[1].value
                var_value = self.interpret(tree[3])
                self.data.write(Variable(var_name), var_value)
                return self.data.read_all()
            elif isinstance(tree[0], Reserved):
                if tree[0].value == "if":
                    for idx, condition in enumerate(tree[1][0]):
                        evaluation = self.interpret(condition)
                        if evaluation == 1:
                            return self.interpret(tree[1][1][idx])
                    
                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])
                    
                    else:
                        return
                elif tree[0].value == "while":
                    condition = self.interpret(tree[1][0])
                    
                    while condition == 1:
                        # Doing the action
                        self.interpret(tree[1][1])

                        # Checking the condition
                        condition = self.interpret(tree[1][0])
                    
                    return

        # Unary operation            
        if isinstance(tree, list) and len(tree) == 2:
            expression = tree[1]
            if isinstance(expression, list):
                expression = self.interpret(expression)
            return self.compute_unary(tree[0], expression)
        
        # No operation
        elif not isinstance(tree, list):
            if isinstance(tree, Variable):
                return self.read_VAR(tree.value)
            return tree
        
        else:
            # Binary operation
            left_node = self.interpret(tree[0])
            right_node = self.interpret(tree[2])
            return self.compute_bin(left_node, tree[1], right_node)

