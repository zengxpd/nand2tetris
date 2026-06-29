import sys
import re
from pathlib import Path
from enum import Enum


class CommandType(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


class VMTranslator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = Path(input_file).with_suffix('.asm')
        self.parser = Parser(input_file)
        self.code_writer = CodeWriter(self.output_file)

    def translate(self):
        for line in self.parser.lines:
            command_type = self.parser.command_type(line)
            if command_type == CommandType.C_ARITHMETIC:
                self.code_writer.write_arithmetic(self.parser.arg1(line))
            elif command_type in [CommandType.C_PUSH, CommandType.C_POP]:
                segment = self.parser.arg1(line)
                index = self.parser.arg2(line)
                self.code_writer.write_push_pop(command_type, segment, index)



class Parser:
    def __init__(self, input_file):
        self.input_file = input_file
        # 读取文件、去除注释并过滤空行
        self.lines = []
        with open(self.input_file, 'r') as f:
            for raw in f:
                line = re.sub(r'//.*', '', raw).strip()
                if line:
                    self.lines.append(line)

    def command_type(self, command):
        if command.startswith('push'):
            return CommandType.C_PUSH
        elif command.startswith('pop'):
            return CommandType.C_POP
        elif command.startswith('label'):
            return CommandType.C_LABEL
        elif command.startswith('goto'):
            return CommandType.C_GOTO
        elif command.startswith('if-goto'):
            return CommandType.C_IF
        elif command.startswith('function'):
            return CommandType.C_FUNCTION
        elif command.startswith('return'):
            return CommandType.C_RETURN
        elif command.startswith('call'):
            return CommandType.C_CALL
        else:
            return CommandType.C_ARITHMETIC

    def arg1(self, command):
        command_type = self.command_type(command)
        if command_type == CommandType.C_ARITHMETIC:
            return command.split()[0]
        elif command_type in [CommandType.C_PUSH, CommandType.C_POP, CommandType.C_LABEL,
                              CommandType.C_GOTO, CommandType.C_IF, CommandType.C_FUNCTION,
                              CommandType.C_CALL]:
            return command.split()[1]

    def arg2(self, command):
        command_type = self.command_type(command)
        if command_type in [CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION,
                             CommandType.C_CALL]:
            return int(command.split()[2])



class CodeWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.file_name = Path(output_file).stem
        self.label_counter = 0
        self.file = open(self.output_file, 'w')

    push_commands = '@SP\nA=M\nM=D\n@SP\nM=M+1\n'
    pop_commands = '@SP\nAM=M-1\nD=M\n' 

    def write_arithmetic(self, command):
        self.file.write(f'\n//{command}\n')
        if command == 'add':
            self.file.write('@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n')
        elif command == 'sub':
            self.file.write('@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n')
        elif command == 'neg':
            self.file.write('@SP\nA=M-1\nM=-M\n')
        elif command == 'eq':
            self.file.write(f'''@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @{self.file_name}.eq.{self.label_counter}
                            D;JEQ
                            D=0
                            @{self.file_name}.eq.{self.label_counter}.end
                            0;JMP
                            ({self.file_name}.eq.{self.label_counter})
                            D=-1
                            ({self.file_name}.eq.{self.label_counter}.end)
                            @SP
                            A=M-1
                            M=D''')
            self.label_counter += 1
        elif command == 'gt':
            self.file.write(f'''@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @{self.file_name}.gt.{self.label_counter}
                            D;JGT
                            D=0
                            @{self.file_name}.gt.{self.label_counter}.end
                            0;JMP
                            ({self.file_name}.gt.{self.label_counter})
                            D=-1
                            ({self.file_name}.gt.{self.label_counter}.end)
                            @SP
                            A=M-1
                            M=D''')
            self.label_counter += 1
        elif command == 'lt':
            self.file.write(f'''@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @{self.file_name}.lt.{self.label_counter}
                            D;JLT
                            D=0
                            @{self.file_name}.lt.{self.label_counter}.end
                            0;JMP
                            ({self.file_name}.lt.{self.label_counter})
                            D=-1
                            ({self.file_name}.lt.{self.label_counter}.end)
                            @SP
                            A=M-1
                            M=D''')
            self.label_counter += 1
        elif command == 'and':
            self.file.write('@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n')
        elif command == 'or':
            self.file.write('@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n')
        elif command == 'not':
            self.file.write('@SP\nA=M-1\nM=!M\n')
        else:
            raise ValueError(f"Invalid arithmetic command: {command}")


    def write_push_pop(self, command_type, segment, index):
        self.file.write(f'\n//{'push' if command_type == CommandType.C_PUSH else 'pop'} {segment} {index}\n')
        if command_type == CommandType.C_PUSH:
            if segment == 'constant':
                self.file.write(f'@{index}\nD=A\n{self.push_commands}')
            elif segment == 'local':
                self.file.write(f'@LCL\nD=M\n@{index}\nA=D+A\nD=M\n{self.push_commands}')
            elif segment == 'argument':
                self.file.write(f'@ARG\nD=M\n@{index}\nA=D+A\nD=M\n{self.push_commands}')
            elif segment == 'static':
                self.file.write(f'@{self.file_name}.{index}\nD=M\n{self.push_commands}')
            elif segment == 'this':
                self.file.write(f'@THIS\nD=M\n@{index}\nA=D+A\nD=M\n{self.push_commands}')
            elif segment == 'that':
                self.file.write(f'@THAT\nD=M\n@{index}\nA=D+A\nD=M\n{self.push_commands}')
            elif segment == 'pointer':
                if index == 0:
                    self.file.write(f'@THIS\nD=M\n{self.push_commands}')
                elif index == 1:
                    self.file.write(f'@THAT\nD=M\n{self.push_commands}')
            elif segment == 'temp':
                self.file.write(f'@{5 + index}\nD=M\n{self.push_commands}')
            else:
                raise ValueError(f"Invalid segment: {segment}")
            
        elif command_type == CommandType.C_POP:
            if segment == 'local':
                self.file.write(f'@{index}\nD=A\n@LCL\nD=D+M\n@R13\nM=D\n{self.pop_commands}@R13\nA=M\nM=D\n')
            elif segment == 'argument':
                self.file.write(f'@{index}\nD=A\n@ARG\nD=D+M\n@R13\nM=D\n{self.pop_commands}@R13\nA=M\nM=D\n')
            elif segment == 'static':
                self.file.write(f'@SP\nAM=M-1\nD=M\n@{self.file_name}.{index}\nM=D\n')
            elif segment == 'this':
                self.file.write(f'@{index}\nD=A\n@THIS\nD=D+M\n@R13\nM=D\n{self.pop_commands}@R13\nA=M\nM=D\n')
            elif segment == 'that':
                self.file.write(f'@{index}\nD=A\n@THAT\nD=D+M\n@R13\nM=D\n{self.pop_commands}@R13\nA=M\nM=D\n')
            elif segment == 'pointer':
                if index == 0:
                    self.file.write(f'{self.pop_commands}@THIS\nM=D\n')
                elif index == 1:
                    self.file.write(f'{self.pop_commands}@THAT\nM=D\n')
            elif segment == 'temp':
                self.file.write(f'{self.pop_commands}@{index + 5}\nM=D\n')
            else:
                raise ValueError(f"Invalid segment: {segment}")
        

    def close(self):
        self.file.write(f'\n\n\n({self.file_name}.end)\n@{self.file_name}.end\n0;JMP\n')
        self.file.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python myVMTranslator.py <inputfile.vm>")
        sys.exit(1)

    input_file = sys.argv[1]
    translator = VMTranslator(input_file)
    translator.translate()
    translator.code_writer.close()
    print(f"Translation complete. Output written to {translator.output_file}")