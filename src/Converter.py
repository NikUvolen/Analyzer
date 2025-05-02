from pprint import pprint
from .CustomError import InvalidInstructionsError


class RiscvAsm:
    """Convert RISC-V assembly instruction to machine code (hex)"""
    def __init__(self, code: str):
        self.opcodes = {
            'R-type': ['add', 'sub', 'sll', 'slt', 'sltu', 'xor', 'srl', 'sra', 'or', 'and'],
            'I-type': ['addi', 'slti', 'sltiu', 'xori', 'ori', 'andi'],
            'I-type load': ['lb', 'lh', 'lw', 'ld', 'lbu', 'lhu', 'lwu'],
            'S-type': ['sb', 'sh', 'sw', 'sd'],
            'U-type': ['lui', 'auipc'],
            'J-type': ['jal']
        }
        self.opcodes_funcs = {
            'R-type': self._r_type,
            'I-type': '',
            'I-type load': '',
            'S-type': '',
            'U-type': '',
            'J-type': ''
        }
        self.parts = []
        for p in code.split('\n'):
            if p:
                self.parts.append(p.strip().replace(',', ' '))

        if not self.parts:
            raise InvalidInstructionsError
        
        self.result_hex = []

    def _r_type(self, opcode_line: str):
        parts = opcode_line.split(' ')
        if len(parts) != 4:
            return "Invalid R-type instruction format"
        
        rd = parse_register(parts[1])
        rs1 = parse_register(parts[2])
        rs2 = parse_register(parts[3])
        
        if rd is None or rs1 is None or rs2 is None:
            return "Invalid register"
        
        funct7_map = {
            'add': 0x00, 'sub': 0x20, 'sll': 0x00, 'slt': 0x00,
            'sltu': 0x00, 'xor': 0x00, 'srl': 0x00, 'sra': 0x20,
            'or': 0x00, 'and': 0x00
        }
        
        funct3_map = {
            'add': 0x0, 'sub': 0x0, 'sll': 0x1, 'slt': 0x2,
            'sltu': 0x3, 'xor': 0x4, 'srl': 0x5, 'sra': 0x5,
            'or': 0x6, 'and': 0x7
        }
        
        funct7 = funct7_map[mnemonic]
        funct3 = funct3_map[mnemonic]
        opcode = 0x33
        
        machine_code = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return f"{machine_code:08x}"

    def print_parts(self):
        pprint(self.parts)

    def convert_to_hex(self):
        pass


        
    
