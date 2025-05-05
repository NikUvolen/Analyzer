class InvalidInstructionsError(Exception):
    def __init__(self, instruction: str):
        self.instruction = instruction
    
    def __str__(self):
        return f'Invalid instruction "{self.instruction}"'
    
class InvalidRegister(Exception):
    def __init__(self, register: str, instruction: str, imm: str = None):
        self.register = register
        self.instruction = instruction
        self.imm = imm

    
    def __str__(self):
        if self.imm is None:
            return f'Invalid register "{self.register}" in "{self.instruction}"'
        else:
            return f'Invalid register or immediate in "{self.instruction}"'

class InstructionsEmpty(Exception):
    def __str__(self):
        return 'Instructions is empty'
