"""
Docstring for compiler.py

This is the main compiler module that orchastrate all phases of the compiler.
This will help us to integrate lexer, parser, sementic analyzer, intermediate code generator, optimizer, and 
code generator.
"""

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from intermediate import IntermediateCodeGenerator
from optimizer import CodeOptimizer
from codegen import CodeGenerator
from executor import Executor


def read_source_file(path):
    with open(path, "r") as file:
        return file.read()


def main():
    print("\nBELOW ARE THE COMPILATION PHASES 1 to 6, AND THE FINAL EXECUTION ON THE FINAL GENERATED TARGET CODE.\n")

    # test.c - our input file for compilation, located in 'input' folder
    source_code = read_source_file("input/test.c")
    print("Source code loaded successfully.\n")

    # the phase 1 - lexer analysis
    lexer = Lexer(source_code)
    tokens, lex_errors = lexer.tokenize()

    print("==> LEXICAL ANAYSIS <==")
    for tok in tokens:
        print(tok)

    if lex_errors:
        print("\nlexical errors:")
        for err in lex_errors:
            print(err)
        return
    else:
        print("\nno lexical errors found\n")

    # the phase 2 - syntax analysis
    parser = Parser(tokens)
    syn_errors = parser.parse()

    print("==> SYNTAX ANALYSIS <==")
    if syn_errors:
        for err in syn_errors:
            print(err)
        return
    else:
        print("no syntax errors found\n")

    # the phase 3 - semantic analysis
    semantic = SemanticAnalyzer(tokens)
    symbol_table, sem_errors = semantic.analyze()

    print("==> SEMANTIC ANALYSIS <==")
    print("symbol table:")
    for name, info in symbol_table.items():
        print(f"{name} -> {info}")

    if sem_errors:
        print("\nsemantic errors:")
        for err in sem_errors:
            print(err)
        return
    else:
        print("\nno semantic errors found\n")

    # the phase 4 - intermediate code generation
    icg = IntermediateCodeGenerator(tokens)
    intermediate_code = icg.generate()

    print("==> INTERMEDIATE CODE GENERATION <==")
    for line in intermediate_code:
        print(line)
    print()

    # the phase 5 - code optimization
    optimizer = CodeOptimizer(intermediate_code)
    optimized_code = optimizer.optimize()

    print("OPTIMIZED INTERMEDIATE CODE:")
    for line in optimized_code:
        print(line)
    print()

    # the phase 6 - final code generation
    generator = CodeGenerator(optimized_code)
    target_code = generator.generate()

    print("==> TARGET CODE GENERATION <==") # this one is the final code generation
    for line in target_code:
        print(line)

    # finally, execute the target code by using simple executor 
    executor = Executor(target_code)
    print("\n==> EXECUTION OF THE TARGET CODE <==")
    executor.run()
    
    print("\n\nCompilation completed successfully!\n")

if __name__ == "__main__":
    main()