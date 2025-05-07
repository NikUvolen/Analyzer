# python GUI analyzer to translate risc-V code to machine code

A risc-V architecture assembly code analyzer written in python and using slint for GUI (https://slint.dev/) to translate to hex code.

## Run Locally

Clone the project or download zip

```
  git clone https://github.com/NikUvolen/Analyzer
```

Go to the project directory

```
  cd my-project
```

Auto-start analyzer (only Windows)
```
run GUI-Analyzer.bat
```
Linux\MacOS
```
python -m venv env
. ./env/Script/activate
pip install -r requirements.txt
python main.py
```