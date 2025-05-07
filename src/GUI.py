import sys
import slint
from src.Converter import RiscvAsm
from src.CustomError import InstructionsEmpty

sys.path.insert(0, 'slint-gui')
gui_style = (
    'cosmic',
    'cosmic-dark',
    'cosmic-light',
    'cupertino',
    'cupertino-dark',
    'cupertino-light',
    'fluent',
    'fluent-dark',
    'fluent-light',
    'material',
    'material-dark',
    'material-light'
)
selected_style = gui_style[-2]

class App(slint.load_file('slint-gui/app-window.slint', style=selected_style).MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.riscv_asm: RiscvAsm = RiscvAsm()
        self.opcode_str: str = ''
        self.opcode_list: list = []
        self.myColorScheme.is_dark = False if 'light' in selected_style else True

    def _convert_code_to_hex(self) -> bool:
        try:
            self.opcode_list = self.riscv_asm.convert_to_hex(self.opcode_str)
            self.PercentageAdapter.error_text = ''
        except InstructionsEmpty as exc:
            self.PercentageAdapter.error_text = f'ERROR: {str(exc)}'
    
    def _write_result(self):
        result = slint.ListModel([
            slint.ListModel(
                [{"text":str(instruction)}, {"text":str(result)}]
            ) for instruction, result in self.opcode_list
        ]) 
        self.PercentageAdapter.resultRows = result

    @slint.callback(global_name="PercentageAdapter")
    def analyze_asm_code(self):
        self.opcode_str = self.PercentageAdapter.codeArea.replace('\r', '')
        self._convert_code_to_hex()
        self._write_result()
