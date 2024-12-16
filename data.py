class Data:
    def __init__(self):
        self.variables = {}

    def write(self, name, value):
        self.variables[name.value] = value

    def read(self, name):
        return self.variables.get(name)

    def read_all(self):
        return self.variables

