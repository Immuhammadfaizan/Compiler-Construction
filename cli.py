import os
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from intermediate import IntermediateCodeGenerator
from optimizer import CodeOptimizer
from codegen import CodeGenerator
from executor import Executor


def load_source(file_path):
    if not os.path.exists(file_path):
        print("source file not found")
        return None

    with open(file_path, "r") as f:
        return f.read()


def run_lexer(source):
    lexer = Lexer(source)
    tokens, errors = lexer.tokenize()

    print("\n==> LEXICAL ANALYSIS <==")
    for token in tokens:
        print(token)

    if errors:
        print("\nlexical errors found")
        for err in errors:
            print(err)
        return None

    print("no lexical errors found")
    return tokens


def run_parser(tokens):
    parser = Parser(tokens)
    errors = parser.parse()

    print("\n==> SYNTAX ANALYSIS <==")
    if errors:
        for err in errors:
            print(err)
        return False

    print("no syntax errors found")
    return True


def run_semantic(tokens):
    semantic = SemanticAnalyzer(tokens)
    symbol_table, errors = semantic.analyze()

    print("\n==> SEMANTIC ANALYSIS <==")
    print("symbol table:")
    for name, info in symbol_table.items():
        print(name, "->", info)

    if errors:
        print("\nsemantic errors found")
        for err in errors:
            print(err)
        return False

    print("no semantic errors found")
    return True


def run_intermediate(tokens):
    icg = IntermediateCodeGenerator(tokens)
    code = icg.generate()

    print("\n==> INTERMEDIATE CODE <==")
    for line in code:
        print(line)

    return code


def run_optimizer(code):
    optimizer = CodeOptimizer(code)
    optimized_code = optimizer.optimize()

    print("\n==> OPTIMIZED INTERMEDIATE CODE <==")
    for line in optimized_code:
        print(line)

    return optimized_code


def run_codegen(code):
    generator = CodeGenerator(code)
    target_code = generator.generate()

    print("\n==> TARGET CODE GENERATION <==")
    for line in target_code:
        print(line)

    return target_code


def run_executor(target_code):
    print("\n==> EXECUTION OF THE TARGET CODE <==")
    executor = Executor(target_code)
    executor.run()


def menu():
    print("\n========== COMPILER CLI ==========")
    print("1. Lexical analysis")
    print("2. Syntax analysis")
    print("3. Semantic analysis")
    print("4. Intermediate code generation")
    print("5. Code optimization")
    print("6. Target code generation")
    print("7. Execute program")
    print("8. Run full compilation")
    print("0. Exit")


def main():
    file_name = input("enter source file name (example: test.c): ").strip()
    source = load_source(file_name)

    if source is None:
        return

    tokens = None
    intermediate = None
    optimized = None
    target = None

    while True:
        menu()
        choice = input("select option: ").strip()

        if choice == "1":
            tokens = run_lexer(source)

        elif choice == "2":
            if not tokens:
                tokens = run_lexer(source)
            run_parser(tokens)

        elif choice == "3":
            if not tokens:
                tokens = run_lexer(source)
            run_semantic(tokens)

        elif choice == "4":
            if not tokens:
                tokens = run_lexer(source)
            intermediate = run_intermediate(tokens)

        elif choice == "5":
            if not intermediate:
                intermediate = run_intermediate(tokens)
            optimized = run_optimizer(intermediate)

        elif choice == "6":
            if not optimized:
                optimized = run_optimizer(intermediate)
            target = run_codegen(optimized)

        elif choice == "7":
            if not target:
                target = run_codegen(optimized)
            run_executor(target)

        elif choice == "8":
            tokens = run_lexer(source)
            if not tokens:
                continue
            if not run_parser(tokens):
                continue
            if not run_semantic(tokens):
                continue

            intermediate = run_intermediate(tokens)
            optimized = run_optimizer(intermediate)
            target = run_codegen(optimized)
            run_executor(target)

        elif choice == "0":
            print("exiting compiler")
            break

        else:
            print("invalid option")


if __name__ == "__main__":
    main()
