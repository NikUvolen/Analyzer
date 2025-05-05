from pprint import pprint
from .CustomError import InstructionsEmpty, InvalidInstructionsError, InvalidRegister


class RiscvAsm:
    """Convert RISC-V assembly instruction to machine code (hex)"""
    def __init__(self):
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
            'I-type': self._i_type,
            'I-type load': self._i_type_instuctions,
            'S-type': self._s_type,
            'U-type': self._u_type,
            'J-type': self._j_type
        }
        self.parts = []

    def _get_parts(self, opcode_line: str, type: str, count_parts: int = 4) -> list:
        parts = opcode_line.split()
        if len(parts) != count_parts:
            raise InvalidInstructionsError(opcode_line)
        return parts

    def _r_type(self, opcode_line: str) -> str:
        parts = self._get_parts(opcode_line, 'R-type')
        
        rd = self._parse_register(parts[1])
        rs1 = self._parse_register(parts[2])
        rs2 = self._parse_register(parts[3])
        
        if rd is None or rs1 is None or rs2 is None:
            raise InvalidRegister(parts[0], opcode_line)
        
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
        
        funct7 = funct7_map[parts[0]]
        funct3 = funct3_map[parts[0]]
        opcode = 0x33
        
        machine_code = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return f"{machine_code:08x}"

    def _i_type(self, opcode_line: str) -> str:
        parts = self._get_parts(opcode_line, 'I-type')
        
        rd = self._parse_register(parts[1])
        rs1 = self._parse_register(parts[2])
        imm = self._parse_immediate(parts[3])
        
        if rd is None or rs1 is None or imm is None:
            raise InvalidRegister(parts[0], opcode_line)
        
        funct3_map = {
            'addi': 0x0, 'slti': 0x2, 'sltiu': 0x3,
            'xori': 0x4, 'ori': 0x6, 'andi': 0x7
        }
        
        funct3 = funct3_map[parts[0]]
        opcode = 0x13
        
        # Sign extend 12-bit immediate
        imm = imm & 0xFFF
        
        machine_code = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return f"{machine_code:08x}"

    def _i_type_instuctions(self, opcode_line: str) -> str:
        parts = self._get_parts(opcode_line, 'I-type instructions', count_parts = 3)
        
        # Parse format like "ld x3, 8(x4)"
        rd = self._parse_register(parts[1])
        imm_str, rs1_str = parts[2].split('(')
        rs1 = self._parse_register(rs1_str[:-1])
        imm = self._parse_immediate(imm_str)
        
        if rd is None or rs1 is None or imm is None:
            raise InvalidRegister(parts[0], opcode_line, imm = imm_str)
        
        funct3_map = {
            'lb': 0x0, 'lh': 0x1, 'lw': 0x2, 'ld': 0x3,
            'lbu': 0x4, 'lhu': 0x5, 'lwu': 0x6
        }
        
        funct3 = funct3_map[parts[0]]
        opcode = 0x03
        
        # Sign extend 12-bit immediate
        imm = imm & 0xFFF
        
        machine_code = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return f"{machine_code:08x}"

    def _s_type(self, opcode_line: str) -> str:
        parts = self._get_parts(opcode_line, 'S-type', count_parts = 3)
        
        # Parse format like "sw x3, 8(x4)"
        rs2 = self._parse_register(parts[1])
        imm_str, rs1_str = parts[2].split('(')
        rs1 = self._parse_register(rs1_str[:-1])
        imm = self._parse_immediate(imm_str)

        if rs2 is None or rs1 is None or imm is None:
            raise InvalidRegister(parts[0], opcode_line, imm = imm_str)
        
        funct3_map = {'sb': 0x0, 'sh': 0x1, 'sw': 0x2, 'sd': 0x3}
        funct3 = funct3_map[parts[0]]
        opcode = 0x23
        
        # Split immediate into imm[11:5] and imm[4:0]
        imm_11_5 = (imm >> 5) & 0x7F
        imm_4_0 = imm & 0x1F
        
        machine_code = (imm_11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
        return f"{machine_code:08x}"

    def _u_type(self, opcode_line: str) -> str:
        parts = self._get_parts(opcode_line, 'U-type', count_parts = 3)
        
        rd = self._parse_register(parts[1])
        imm = self._parse_immediate(parts[2])
        
        if rd is None or imm is None:
            raise InvalidRegister(parts[0], opcode_line, imm = imm)
        
        opcode_map = {'lui': 0x37, 'auipc': 0x17}
        opcode = opcode_map[parts[0]]
        
        # Take upper 20 bits
        imm = (imm >> 12) & 0xFFFFF
        
        machine_code = (imm << 12) | (rd << 7) | opcode
        return f"{machine_code:08x}"
    

    def _j_type(self, opcode_line: str) -> str:
        parts = self._get_parts(opcode_line, 'J-type', count_parts = 3)
        
        rd = self._parse_register(parts[1])
        imm = self._parse_immediate(parts[2])
        
        if rd is None or imm is None:
            raise InvalidRegister(parts[0], opcode_line, imm = imm)
        
        opcode = 0x6F
        
        # Split immediate into J-type format
        imm_20 = (imm >> 20) & 0x1
        imm_10_1 = (imm >> 1) & 0x3FF
        imm_11 = (imm >> 11) & 0x1
        imm_19_12 = (imm >> 12) & 0xFF
        
        machine_code = (imm_20 << 31) | (imm_19_12 << 12) | (imm_11 << 20) | (imm_10_1 << 21) | (rd << 7) | opcode
        return f"{machine_code:08x}"

    def _parse_register(self, reg: str) -> int:
        """Parse register name (e.g., 'x1', 'x2') to register number"""
        if not reg.startswith('x'):
            return None
        try:
            num = int(reg[1:])
            if 0 <= num <= 31:
                return num
            return None
        except ValueError:
            return None

    def _parse_immediate(self, imm_str: str) -> int:
        """Parse immediate value (supports decimal, hex with 0x, binary with 0b)"""
        try:
            if imm_str.startswith('0x'):
                return int(imm_str[2:], 16)
            elif imm_str.startswith('0b'):
                return int(imm_str[2:], 2)
            else:
                return int(imm_str)
        except ValueError:
            return None

    def print_results(self, result_output: list) -> None:
        for result in result_output:
            print(f'{result[0]:25} => {result[1]}')

    def convert_to_hex_generator(self, code: str) -> (str, list):
        """
        Low level converter risc-V code to hex view via generator

        :param code: String risc-V code
        :return: tumple like a (instruction, hex_value or err)
        """

        self.parts.clear()
        for p in code.split('\n'):
            if p:
                self.parts.append(p.strip().replace(',', ' '))
        if not self.parts:
            raise InstructionsEmpty

        for part in self.parts:
            try:
                instructions = [p.strip() for p in part.split()]
                found = False
                for type, opcodes in self.opcodes.items():
                    if instructions[0] in opcodes:
                        yield part, self.opcodes_funcs[type](part)
                        found = True
                
                if not found:
                    yield part, f"Unsupported instruction: {instructions[0]}"
            except InvalidInstructionsError as exc:
                yield part, exc
            except InvalidRegister as exc:
                yield part, exc

    def convert_to_hex(self, code: str) -> list:
        """
            Use the self generator to convert risc-V code to hex view

            :param code: String risc-V code
            :return: List with parameters like a (instruction, hex_value or err)
        """

        gen = self.convert_to_hex_generator(code) 
        result = []
        
        for instruction, hex_value in gen:
            result.append([instruction, hex_value])

        return result



                
                


                



        
    
