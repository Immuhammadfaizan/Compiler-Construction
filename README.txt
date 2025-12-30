Mini C Compiler Project
Compiler Construction Academic Project

Author
Muhammad Faizan

Programming Language Used
Python

Input Language
Subset of C Language

Purpose of This Project

This project demonstrates the complete working of a compiler for a small subset of the C programming language. The compiler is designed to show how source code written in C is processed through different compiler phases and finally executed using a simulated runtime environment.

The goal of this project is educational. It helps understand how real compilers such as GCC internally work, starting from reading source code up to executing the final program.

This compiler supports variable declarations, arithmetic expressions, conditional statements, loops, and basic input output using printf.

-----------------------------------------------------------------------------------------------------------------------------------------

Project Structure

The project is divided into multiple Python files. Each file represents one phase of the compiler.

lexer.py
parser.py
semantic.py
intermediate.py
optimizer.py
codegen.py
executor.py
compiler.py
test.c  # this would work as input file from the directory input/test.c file to convert into tokens, symbols/symbols table, compile, and execute it for the final output.

Each phase works independently but is connected to the next phase in sequence.

-----------------------------------------------------------------------------------------------------------------------------------------

How to Run the Project

Write your C program inside the test.c file

Open terminal or command prompt in the project folder

Run the compiler using

python compiler.py

The compiler will automatically
Load the source code
Run all compiler phases
Generate intermediate code
Generate target code
Execute the program
Display final output

You do not need to run executor.py separately.
compiler.py handles everything.

-----------------------------------------------------------------------------------------------------------------------------------------

Phase 1 Lexical Analysis

File
lexer.py

What this phase does

Lexical analysis reads the source code character by character and converts it into tokens. Tokens are the smallest meaningful units of a program.

Examples of tokens
Keywords like int float if while return
Identifiers like variable names
Numbers
Operators like + - * / =
Separators like ; ( ) { }
Built in functions like printf

If the lexer encounters invalid characters, it reports them as lexical errors and stores them in a separate error file.

Output of this phase
A list of tokens with type value and line number

-----------------------------------------------------------------------------------------------------------------------------------------

Phase 2 Syntax Analysis

File
parser.py

What this phase does

Syntax analysis checks whether the token sequence follows correct grammatical rules of the C language.

This phase verifies
Variable declarations
Assignments
If statements
While loops
Function calls such as printf
Expression structure

If syntax is incorrect, meaningful syntax error messages are generated with line numbers.

Output of this phase
Either syntax errors or confirmation that syntax is valid

-----------------------------------------------------------------------------------------------------------------------------------------

Phase 3 Semantic Analysis

File
semantic.py

What this phase does

Semantic analysis checks the meaning of the program. Even if syntax is correct, the program may still be logically incorrect.

This phase checks
Variable redeclaration
Use of undeclared variables
Type compatibility in assignments
Type mismatch in expressions

A symbol table is created in this phase to store variable names, data types, and declaration lines.

Output of this phase
Symbol table
Semantic errors if any

-----------------------------------------------------------------------------------------------------------------------------------------

Phase 4 Intermediate Code Generation

File
intermediate.py

What this phase does

This phase converts high level C constructs into intermediate code known as Three Address Code.

Intermediate code is simple and close to machine instructions but still independent of hardware.

Examples
x = 10
t1 = x + y
PRINT "sum" t1

Temporary variables like t1 t2 are generated automatically.

Output of this phase
List of intermediate instructions

-----------------------------------------------------------------------------------------------------------------------------------------

Phase 5 Code Optimization

File
optimizer.py

What this phase does

The optimizer improves intermediate code without changing program behavior.

This phase performs
Removal of redundant instructions
Reuse of computed values
Basic constant handling

This phase shows how compilers improve efficiency before final code generation.

Output of this phase
Optimized intermediate code

-----------------------------------------------------------------------------------------------------------------------------------------

Phase 6 Target Code Generation

File
codegen.py

What this phase does

This phase converts optimized intermediate code into low level target instructions.

The generated target code resembles assembly like instructions such as
LOAD
STORE
ADD
MUL
PRINT

This code is not real machine code but is designed for execution by the custom executor.

Output of this phase
Target code instructions

-----------------------------------------------------------------------------------------------------------------------------------------

Phase 7 Execution Phase

File
executor.py

What this phase does

The executor simulates a runtime environment similar to a real CPU.

It
Maintains memory for variables
Executes arithmetic operations
Evaluates expressions
Handles print statements correctly
Supports strings numeric values and expressions

The executor correctly distinguishes between
String literals
Variables
Temporary values
Expressions

This phase produces the actual output of the C program.

Output of this phase
Final execution result printed on screen

-----------------------------------------------------------------------------------------------------------------------------------------

Compiler Controller

File
compiler.py

What this file does

compiler.py is the main driver file of the project.

It controls the entire compilation process by
Calling the lexer
Passing tokens to the parser
Running semantic analysis
Generating intermediate code
Optimizing code
Generating target code
Executing the program

You only need to run this file.

-----------------------------------------------------------------------------------------------------------------------------------------

Input Program

File
test.c

This file contains the C program to be compiled and executed.

Example supported code

int x = 10;
int y = 5;

printf("sum");
printf(x + y);

Output
sum
15

The compiler also supports
If conditions
While loops
Multiple print statements
Arithmetic expressions

-----------------------------------------------------------------------------------------------------------------------------------------

Limitations

This compiler supports a subset of C language only.
It does not support pointers arrays or user defined functions.
scanf is not implemented.

These limitations are intentional to keep the project focused on learning compiler phases.

-----------------------------------------------------------------------------------------------------------------------------------------

Conclusion

This project demonstrates a complete compiler pipeline from source code to execution. Each phase is implemented clearly and separately to show its role in compilation. The project is suitable for academic presentation and helps in understanding how real world compilers work internally.

-----------------------------------------------------------------------------------------------------------------------------------------