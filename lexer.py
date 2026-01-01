import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.errors = []

        # all c keywords 
        self.keywords = {
            # data types
            "char", "int", "float", "double", "void",
            "short", "long", "signed", "unsigned",

            # control flow
            "if", "else", "switch", "case", "default",
            "for", "while", "do", "break", "continue", "goto",

            # storage classes
            "auto", "register", "static", "extern",

            # type qualifiers & others
            "const", "volatile", "sizeof", "typedef",
            "struct", "union", "enum", "return"
        }

        # standard library functions
        self.builtin_functions = {
            # stdio.h
            "printf", "scanf", "fopen", "fclose",
            "fgetc", "fputc",

            # stdlib.h
            "malloc", "calloc", "realloc", "free",
            "exit", "abs", "labs",
            "atoi", "atof", "atol",

            # math.h
            "sqrt", "pow", "sin", "cos", "tan",
            "ceil", "floor", "log", "log10",

            # string.h
            "strlen", "strcpy", "strncpy",
            "strcat", "strncat",
            "strcmp", "strncmp",
            "strchr", "strstr",

            # ctype.h
            "isalpha", "isdigit", "isspace",
            "toupper", "tolower",

            # time.h
            "time", "clock", "localtime", "gmtime",

            # assert.h
            "assert"
        }

        # regex rules for tokens specification
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

        for line_no, line in enumerate(self.source_code.splitlines(), start=1):
            for match in re.finditer(combined_regex, line):
                kind = match.lastgroup
                value = match.group()

                if kind == "WHITESPACE":
                    continue

                # check identifiers more deeply
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

    # write lexer errors to file
    def _write_lexer_errors(self):
        if not self.errors:
            return

        with open("reported-lexer-error.txt", "w") as file:
            for err in self.errors:
                file.write(err + "\n")
