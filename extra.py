import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.errors = []

        self.keywords = {
            "char", "int", "float", "double", "void",
            "short", "long", "signed", "unsigned",
            "if", "else", "switch", "case", "default",
            "for", "while", "do", "break", "continue", "goto",
            "auto", "register", "static", "extern",
            "const", "volatile", "sizeof", "typedef",
            "struct", "union", "enum", "return"
        }

        self.builtin_functions = {
            "printf", "scanf", "fopen", "fclose",
            "fgetc", "fputc",
            "malloc", "calloc", "realloc", "free",
            "exit", "abs", "labs",
            "atoi", "atof", "atol",
            "sqrt", "pow", "sin", "cos", "tan",
            "ceil", "floor", "log", "log10",
            "strlen", "strcpy", "strncpy",
            "strcat", "strncat",
            "strcmp", "strncmp",
            "strchr", "strstr",
            "isalpha", "isdigit", "isspace",
            "toupper", "tolower",
            "time", "clock", "localtime", "gmtime",
            "assert"
        }

        self.token_specification = [
            ("NUMBER",      r'\b\d+(\.\d+)?\b'),
            ("IDENTIFIER",  r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ("STRING",      r'"[^"]*"'),
            ("CHAR",        r"'.'"),
            ("OPERATOR",    r'==|!=|<=|>=|\+\+|--|[+\-*/%=<>]'),
            ("SEPARATOR",   r'[;(),{}\[\]]'),
            ("WHITESPACE",  r'\s+'),
            ("MISMATCH",    r'.')
        ]

    def tokenize(self):
        combined_regex = "|".join(
            f"(?P<{name}>{pattern})"
            for name, pattern in self.token_specification
        )
        regex = re.compile(combined_regex)

        for line_no, line in enumerate(self.source_code.splitlines(), start=1):
            pos = 0
            while pos < len(line):
                match = regex.match(line, pos)
                if not match:
                    error = f"Lexical Error at line {line_no}: Invalid character '{line[pos]}'"
                    self.errors.append(error)
                    pos += 1
                    continue

                kind = match.lastgroup
                value = match.group()
                pos = match.end()

                if kind == "WHITESPACE":
                    continue

                if kind == "IDENTIFIER":
                    if value in self.keywords:
                        self.tokens.append(("KEYWORD", value, line_no))
                    elif value in self.builtin_functions:
                        self.tokens.append(("BUILTIN_FUNC", value, line_no))
                    else:
                        self.tokens.append(("IDENTIFIER", value, line_no))

                elif kind == "MISMATCH":
                    error = f"Lexical Error at line {line_no}: Invalid character '{value}'"
                    self.errors.append(error)

                else:
                    self.tokens.append((kind, value, line_no))

        self._write_lexer_errors()
        return self.tokens, self.errors

    def _write_lexer_errors(self):
        if not self.errors:
            return

        with open("reported-lexer-error.txt", "w") as file:
            for err in self.errors:
                file.write(err + "\n")

def main():
    filename = input("Enter the source file path (e.g., input/test.c): ").strip()
    
    try:
        with open(filename, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    lexer = Lexer(source_code)
    tokens, errors = lexer.tokenize()

    print("\nTokens generated:\n")
    for token in tokens:
        kind, value, line = token
        print(f"{kind:<15} | {value:<20} | Line: {line}")

    if errors:
        print("\nLexical errors found. See 'reported-lexer-error.txt' for details.")
    else:
        print("\nNo lexical errors found.")

if __name__ == "__main__":
    main()