
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.eq.0
                            D;JEQ
                            D=0
                            @StackTest.eq.0.end
                            0;JMP
                            (StackTest.eq.0)
                            D=-1
                            (StackTest.eq.0.end)
                            @SP
                            A=M-1
                            M=D
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.eq.1
                            D;JEQ
                            D=0
                            @StackTest.eq.1.end
                            0;JMP
                            (StackTest.eq.1)
                            D=-1
                            (StackTest.eq.1.end)
                            @SP
                            A=M-1
                            M=D
//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.eq.2
                            D;JEQ
                            D=0
                            @StackTest.eq.2.end
                            0;JMP
                            (StackTest.eq.2)
                            D=-1
                            (StackTest.eq.2.end)
                            @SP
                            A=M-1
                            M=D
//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.lt.3
                            D;JLT
                            D=0
                            @StackTest.lt.3.end
                            0;JMP
                            (StackTest.lt.3)
                            D=-1
                            (StackTest.lt.3.end)
                            @SP
                            A=M-1
                            M=D
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.lt.4
                            D;JLT
                            D=0
                            @StackTest.lt.4.end
                            0;JMP
                            (StackTest.lt.4)
                            D=-1
                            (StackTest.lt.4.end)
                            @SP
                            A=M-1
                            M=D
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.lt.5
                            D;JLT
                            D=0
                            @StackTest.lt.5.end
                            0;JMP
                            (StackTest.lt.5)
                            D=-1
                            (StackTest.lt.5.end)
                            @SP
                            A=M-1
                            M=D
//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.gt.6
                            D;JGT
                            D=0
                            @StackTest.gt.6.end
                            0;JMP
                            (StackTest.gt.6)
                            D=-1
                            (StackTest.gt.6.end)
                            @SP
                            A=M-1
                            M=D
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.gt.7
                            D;JGT
                            D=0
                            @StackTest.gt.7.end
                            0;JMP
                            (StackTest.gt.7)
                            D=-1
                            (StackTest.gt.7.end)
                            @SP
                            A=M-1
                            M=D
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
                            AM=M-1
                            D=M
                            A=A-1
                            D=M-D
                            @StackTest.gt.8
                            D;JGT
                            D=0
                            @StackTest.gt.8.end
                            0;JMP
                            (StackTest.gt.8)
                            D=-1
                            (StackTest.gt.8.end)
                            @SP
                            A=M-1
                            M=D
//push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

//push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

//neg
@SP
A=M-1
M=-M

//and
@SP
AM=M-1
D=M
A=A-1
M=D&M

//push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

//or
@SP
AM=M-1
D=M
A=A-1
M=D|M

//not
@SP
A=M-1
M=!M



(StackTest.end)
@StackTest.end
0;JMP
