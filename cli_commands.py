class CLICommand:
    def __init__(self, name, description, callback):
        self.name = name
        self.description = description
        self.callback = callback
    
    def info(self):
        return f"{self.name}: {self.description}"