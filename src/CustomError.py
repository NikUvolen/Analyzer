class InvalidInstructionsError(Exception):
    def __init__(self, instruction):
        self.instruction = instruction
    
    def __str__(self):
        return f'Invalid instruction {self.instruction}'
