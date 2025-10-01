class CLICommand:
    def __init__(self, usage, description, callback):
        self.usage = usage
        self.description = description
        self.callback = callback
    
    def info(self):
        return f"{self.name}: {self.description}"