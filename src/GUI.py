import sys
from re import sub
import slint
from src.Converter import RiscvAsm

import builtins

sys.path.insert(0, 'slint-gui')

class App(slint.loader.app_window.MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.riscv_asm: RiscvAsm = RiscvAsm()
        self.opcode_str: str = ''
        self.opcode_list: list = []

    def _convert_code_to_hex(self):
        self.opcode_list = self.riscv_asm.convert_to_hex(self.opcode_str)
    
    def _write_result(self):
        result_str = ''
        for instruction, result in self.opcode_list:
            result_str += f'{instruction:30} => {result}\n'
        self.PercentageAdapter.hexResultArea = result_str
    
    @slint.callback(global_name="PercentageAdapter")
    def analyze_asm_code(self):
        self.opcode_str = self.PercentageAdapter.codeArea.replace('\r', '')
        self._convert_code_to_hex()
        self._write_result()
