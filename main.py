from src.Converter import RiscvAsm


def riscv_assembler(instruction):
    """Convert RISC-V assembly instruction to machine code (hex)"""
    parts = [p.strip() for p in instruction.replace(',', ' ').split()]
    if not parts:
        return "Invalid instruction"
    
    mnemonic = parts[0].lower()
    
    # R-type instructions
    if mnemonic in ['add', 'sub', 'sll', 'slt', 'sltu', 'xor', 'srl', 'sra', 'or', 'and']:
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
    
    # I-type instructions (immediate)
    elif mnemonic in ['addi', 'slti', 'sltiu', 'xori', 'ori', 'andi']:
        if len(parts) != 4:
            return "Invalid I-type instruction format"
        
        rd = parse_register(parts[1])
        rs1 = parse_register(parts[2])
        imm = parse_immediate(parts[3])
        
        if rd is None or rs1 is None or imm is None:
            return "Invalid register or immediate"
        
        funct3_map = {
            'addi': 0x0, 'slti': 0x2, 'sltiu': 0x3,
            'xori': 0x4, 'ori': 0x6, 'andi': 0x7
        }
        
        funct3 = funct3_map[mnemonic]
        opcode = 0x13
        
        # Sign extend 12-bit immediate
        imm = imm & 0xFFF
        
        machine_code = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return f"{machine_code:08x}"
    
    # Load instructions (I-type)
    elif mnemonic in ['lb', 'lh', 'lw', 'ld', 'lbu', 'lhu', 'lwu']:
        if len(parts) != 3:
            return "Invalid load instruction format"
        
        # Parse format like "ld x3, 8(x4)"
        rd = parse_register(parts[1])
        imm_str, rs1_str = parts[2].split('(')
        rs1 = parse_register(rs1_str[:-1])
        imm = parse_immediate(imm_str)
        
        if rd is None or rs1 is None or imm is None:
            return "Invalid register or immediate"
        
        funct3_map = {
            'lb': 0x0, 'lh': 0x1, 'lw': 0x2, 'ld': 0x3,
            'lbu': 0x4, 'lhu': 0x5, 'lwu': 0x6
        }
        
        funct3 = funct3_map[mnemonic]
        opcode = 0x03
        
        # Sign extend 12-bit immediate
        imm = imm & 0xFFF
        
        machine_code = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
        return f"{machine_code:08x}"
    
    # S-type instructions (store)
    elif mnemonic in ['sb', 'sh', 'sw', 'sd']:
        if len(parts) != 3:
            return "Invalid store instruction format"
        
        # Parse format like "sw x3, 8(x4)"
        rs2 = parse_register(parts[1])
        imm_str, rs1_str = parts[2].split('(')
        rs1 = parse_register(rs1_str[:-1])
        imm = parse_immediate(imm_str)
        
        if rs2 is None or rs1 is None or imm is None:
            return "Invalid register or immediate"
        
        funct3_map = {'sb': 0x0, 'sh': 0x1, 'sw': 0x2, 'sd': 0x3}
        funct3 = funct3_map[mnemonic]
        opcode = 0x23
        
        # Split immediate into imm[11:5] and imm[4:0]
        imm_11_5 = (imm >> 5) & 0x7F
        imm_4_0 = imm & 0x1F
        
        machine_code = (imm_11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
        return f"{machine_code:08x}"
    
    # U-type instructions (lui, auipc)
    elif mnemonic in ['lui', 'auipc']:
        if len(parts) != 3:
            return "Invalid U-type instruction format"
        
        rd = parse_register(parts[1])
        imm = parse_immediate(parts[2])
        
        if rd is None or imm is None:
            return "Invalid register or immediate"
        
        opcode_map = {'lui': 0x37, 'auipc': 0x17}
        opcode = opcode_map[mnemonic]
        
        # Take upper 20 bits
        imm = (imm >> 12) & 0xFFFFF
        
        machine_code = (imm << 12) | (rd << 7) | opcode
        return f"{machine_code:08x}"
    
    # J-type instructions (jal)
    elif mnemonic == 'jal':
        if len(parts) != 3:
            return "Invalid J-type instruction format"
        
        rd = parse_register(parts[1])
        imm = parse_immediate(parts[2])
        
        if rd is None or imm is None:
            return "Invalid register or immediate"
        
        opcode = 0x6F
        
        # Split immediate into J-type format
        imm_20 = (imm >> 20) & 0x1
        imm_10_1 = (imm >> 1) & 0x3FF
        imm_11 = (imm >> 11) & 0x1
        imm_19_12 = (imm >> 12) & 0xFF
        
        machine_code = (imm_20 << 31) | (imm_19_12 << 12) | (imm_11 << 20) | (imm_10_1 << 21) | (rd << 7) | opcode
        return f"{machine_code:08x}"
    
    else:
        return f"Unsupported instruction: {mnemonic}"

def parse_register(reg):
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

def parse_immediate(imm_str):
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

# Example usage
if __name__ == "__main__":
    test_instructions = [
        "add x11, x11, x12",
        "sub x11, x11, x12",
        "sw x10, 8(x11)",
        "addi x2, x2, -4",
        "lui x5, 0x12345",
        "auipc x6, 0x1000",
        "jal x1, 1024",
        "lb x3, 4(x4)"
    ]

    test = '''add x11, x11, x12\n
        sub x11, x11, x12\n
        sw x10, 8(x11)'''
    
    RiscvAsm(test)
    
        # for instr in test_instructions:
    #     machine_code = riscv_assembler(instr)
    #     print(f"{instr:30} => {machine_code}")