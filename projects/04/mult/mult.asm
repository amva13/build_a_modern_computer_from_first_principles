// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2
M=0 // product starts as 0
@count // variable to store ct; init to 0
M=0

@0
D=M // read R0
@END
D;JEQ // if R0 is zero, answer is 0. so go to terminating condition

@1
D=M // read R1
@END
D;JEQ // if R1 is zero, answer is 0.

(ADDLOOP)
@1
D=M // grab number in R1
@R2 // store running sum
M=D+M;
@count
M=M+1
D=M
@0 // check if we're done
D=D-M
@END
D;JEQ // go to terminating condition if we're done
@ADDLOOP
0;JMP // otherwise, go to the add loop

(END)
@END
0;JMP // forever loop; terminating condition
