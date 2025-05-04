from src.Converter import RiscvAsm

if __name__ == "__main__":
    instructions = '''add x11, x11, x12\n
        sub x11, x11, x12\n
        sw x10, 8(x11)\n
        addi x2, x2, -4 -5\n
        lui x5, 0x12345\n
        auipc x6, 0x1000\n
        jal x1, 1024\n
        lb x3, 4(x4)'''
    
    riscv_asm = RiscvAsm()
    result = riscv_asm.convert_to_hex(instructions)
    riscv_asm.print_results(result)
