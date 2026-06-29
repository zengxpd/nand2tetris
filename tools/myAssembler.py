'''
This is my assembler for nand2tetris project, which can translate .asm file into .hack file. It can handle A_COMMAND, C_COMMAND and L_COMMAND, and also support symbol table for variables and labels. 
It will check the syntax of the input file and report errors if any invalid symbols or mnemonics are found.
By the way, it is my first time to write an assembler, so there may be some bugs or inefficiencies in the code. 
I like it.
'''





import sys
import re


class Code:
    def __init__(self):
        pass

    dest_table = {
        'null': '000',
        'M':    '001',
        'D':    '010',
        'MD':   '011',
        'A':    '100',
        'AM':   '101',
        'AD':   '110',
        'AMD':  '111'
    }

    comp_table = {
        '0':   '101010',
        '1':   '111111',
        '-1':  '111010',
        'D':   '001100',
        'A':   '110000',
        '!D':  '001101',
        '!A':  '110001',
        '-D':  '001111',
        '-A':  '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101',
        'M':   '110000',
        '!M':  '110001',
        '-M':  '110011',
        'M+1': '110111',
        'M-1': '110010',
        'D+M': '000010',
        'D-M': '010011',
        'M-D': '000111',
        'D&M': '000000',
        'D|M': '010101'
    }

    jump_table = {
        'null': '000',
        'JGT':  '001',
        'JEQ':  '010',
        'JGE':  '011',
        'JLT':  '100',
        'JNE':  '101',
        'JLE':  '110',
        'JMP':  '111'
    }

    def d2b(self, Dec, len):
        num = int(Dec)
        return format(num, f'0{len}b')

    def dest(self, mnemonic):
        return self.dest_table.get(mnemonic, '000')

    def comp(self, mnemonic):
        return self.comp_table.get(mnemonic, '000000')

    def jump(self, mnemonic):
        return self.jump_table.get(mnemonic, '000')
    


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []
        self._commands = []
        self.code = Code()
        with open(file_path, 'r') as file:
            self.lines = file.readlines()
    

    symbols = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
              'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
              'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
              'SCREEN': 16384, 'KBD': 24576}
    symbols_counter = 16

    def lab2addr(self, label):
        if label in self.symbols:
            return self.symbols[label]
        else:
            self.symbols[label] = self.symbols_counter
            self.symbols_counter += 1
            return self.symbols[label]
        
    def lab_or_num(self,str):
        if re.match(r'^\d+$', str):
            return 'num'
        elif re.match(r'^[A-Za-z_.$:][A-Za-z0-9_.$:]*$', str):
            return 'lab'
        else:
            return 'invalid'
        
    def process(self):
        cmdlindex = 0
        for index, line in enumerate(self.lines, start=1):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            if line.startswith('@'):    #A_COMMAND
                flag = self.lab_or_num(line[1:])
                if flag == 'num':
                    commond_value = int(line[1:])
                    if commond_value < 0 or commond_value > 32767:
                        print(f"Error: Numeric value '{commond_value}' out of range at line {index}")
                        sys.exit(1)
                elif flag == 'lab':
                    pass
                else:
                    print(f"Error: Invalid symbol '{line[1:]}' at line {index}")
                    sys.exit(1)
                cmdlindex += 1
                
            elif line.startswith('(') and line.endswith(')'):   #L_COMMAND
                label = line[1:-1]
                if self.lab_or_num(label) != 'lab':
                    print(f"Error: Invalid label '{label}' at line {index}")
                    sys.exit(1)
                self.symbols[label] = cmdlindex

            else:   #C_COMMAND
                dest, comp, jump = 'null', line, 'null'
                if '=' in line:
                    parts = line.split('=')
                    dest = parts[0].strip()
                    comp = parts[1].strip()
                if ';' in comp:
                    parts = comp.split(';')
                    comp = parts[0].strip()
                    jump = parts[1].strip()
                if dest not in self.code.dest_table:
                    print(f"Error: Invalid dest mnemonic '{dest}' at line {index}")
                    sys.exit(1)
                if comp not in self.code.comp_table:
                    print(f"Error: Invalid comp mnemonic '{comp}' at line {index}")
                    sys.exit(1)
                if jump not in self.code.jump_table:
                    print(f"Error: Invalid jump mnemonic '{jump}' at line {index}")
                    sys.exit(1)
                cmdlindex += 1


        for index, line in enumerate(self.lines, start=1):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            if line.startswith('@'):    #A_COMMAND
                flag = self.lab_or_num(line[1:])
                if flag == 'num':
                    commond_value = int(line[1:])
                    if commond_value < 0 or commond_value > 32767:
                        print(f"Error: Numeric value '{commond_value}' out of range at line {index}")
                        sys.exit(1)
                elif flag == 'lab':
                    commond_value = self.lab2addr(line[1:])
                else:
                    print(f"Error: Invalid symbol '{line[1:]}' at line {index}")
                    sys.exit(1)
                self._commands.append(('A_COMMAND', self.code.d2b(commond_value, 16)))
                
            elif line.startswith('(') and line.endswith(')'):   #L_COMMAND
                label = line[1:-1]
                if self.lab_or_num(label) != 'lab':
                    print(f"Error: Invalid label '{label}' at line {index}")
                    sys.exit(1)
                self.symbols[label] = len(self._commands)

            else:   #C_COMMAND
                dest, comp, jump = 'null', line, 'null'
                if '=' in line:
                    parts = line.split('=')
                    dest = parts[0].strip()
                    comp = parts[1].strip()
                if ';' in comp:
                    parts = comp.split(';')
                    comp = parts[0].strip()
                    jump = parts[1].strip()
                if dest not in self.code.dest_table:
                    print(f"Error: Invalid dest mnemonic '{dest}' at line {index}")
                    sys.exit(1)
                if comp not in self.code.comp_table:
                    print(f"Error: Invalid comp mnemonic '{comp}' at line {index}")
                    sys.exit(1)
                if jump not in self.code.jump_table:
                    print(f"Error: Invalid jump mnemonic '{jump}' at line {index}")
                    sys.exit(1)
                a= '1' if 'M' in comp else '0'
                self._commands.append(('C_COMMAND', '111' + a + self.code.comp(comp) + self.code.dest(dest) + self.code.jump(jump)))

    def create_hack_file(self):
        output_file = self.file_path.replace('.asm', '.hack')
        with open(output_file, 'w') as file:
            for command in self._commands:
                file.write(command[1] + '\n')



def main():
    if len(sys.argv) != 2:
        print("Usage: python myAssembler.py <input_file.asm>")
        sys.exit(1)

    input_file = sys.argv[1]

    if re.match(r'.*\.asm$', input_file) is None:
        print("Error: Input file must have a .asm extension")
        sys.exit(1)

    parser = Parser(input_file)
    parser.process()
    parser.create_hack_file()

    print(f"Assembly completed successfully. Output file: {input_file.replace('.asm', '.hack')}")

if __name__ == "__main__":
    main()