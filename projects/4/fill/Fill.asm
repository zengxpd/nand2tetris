// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(END)
@SCREEN
D=A
@j
M=D
@i
M=0
@8192
D=A
@s
M=D
@KBD
D=M
@Y
D;JEQ
@fill
M=0
@FOR
0;JMP 
(Y)
@fill
M=-1

(FOR)
    @i
    D=M
    @s
    D=D-M
    @END
    D;JEQ
    
    @fill
    D=M
    @j
    A=M
    M=D
    @i
    M=M+1
    @j
    M=M+1
    @FOR
    0;JMP
    @END
    0;JMP