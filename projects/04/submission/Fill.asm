// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(START)
@SCREEN // obtaining the screen register start location
D=A
@R0
M=D // put screen start location in R0

// check the keyboard
(keyboardcheck)
@KBD
D=M // obtain input from keyboard
@black
D;JGT // if anything is pressed, input is non 0, go to change screen to black
@white
D;JEQ // otherwise, input is 0 and go to change screen to white

@keyboardcheck
0;JMP // continuous loop on reading keyboard input

// if button pressed, change to black
(black)
@R1
M=-1 // because -1 is 1111... which would turn the whole word black
@changescreen
0;JMP // goto change screen

// otherwise, change to white
(white)
@R1
M=0 // 0000... is whole word white
@changescreen
0;JMP // goto change screen

// loop to change screen
(changescreen)
@1
D=M // read whether input is white or black

@0
A=M // get the address we want to start filling in, make a pointer to it
M=D // fill the word (note: M now points to register referenced by A)

@0
D=M+1 // get next register (containing 16 pixels)
M=D // save the next register to continue coloring
@KBD
D=A-D // terminating condition: after screen registers, is the keyboard register

@changescreen
D;JGT // if D non-zero, we have screen registers left so keep coloring

// otherwise, we can read from keyboard again and reset register pointer
@START
0;JMP
