"""
Docstring for semantic.py

This phase checks the meaning of the program.
It ensures correct variable usage and type consistency.
Now supports built in functions and function calls without treating them as variables.
"""

class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = {}
        self.errors = []
        self.builtin_functions = {"printf", "print"}  # add more later if needed

    def analyze(self):
        while not self._is_end():
            self._check_statement()
        return self.symbol_table, self.errors

    # helpers
    def _is_end(self):
        return self.pos >= len(self.tokens)

    def _current(self):
        if self._is_end():
            return None
        return self.tokens[self.pos]

    def _peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def _advance(self):
        self.pos += 1

    # main statement checker
    def _check_statement(self):
        token = self._current()
        if not token:
            return

        tok_type, tok_val, line = token

        # Declaration: int x = 10;
        if tok_type == "KEYWORD" and tok_val in ("int", "float", "double", "char"):
            self._handle_declaration()

        # Function call: printf(...) or print(x);
        elif tok_type == "IDENTIFIER" and self._is_function_call():
            self._skip_function_call()

        # Assignment: x = 5;
        elif tok_type == "IDENTIFIER":
            name = tok_val
            self._check_usage(name, line)  # check left side variable
            self._advance()  # skip identifier
            if self._current() and self._current()[1] == "=":
                self._advance()  # =
                self._check_expression()  # check variables in right-hand side

        else:
            self._advance()

    # Check if current identifier starts a function call
    def _is_function_call(self):
        # Look ahead: identifier followed by '('
        current = self._current()
        peek = self._peek()
        if current and current[0] == "IDENTIFIER" and peek and peek[1] == "(":
            return True
        return False

    # Skip entire function call (name + args + ); )
    def _skip_function_call(self):
        self._advance()  # skip function name

        if not self._current() or self._current()[1] != "(":
            return
        self._advance()  # (

        # Skip arguments
        while self._current() and self._current()[1] != ")":
            if self._current()[0] == "STRING":
                self._advance()
            elif self._current()[0] == "IDENTIFIER":
                # Do NOT report undeclared — could be variable or function
                # We skip checking args strictly for simplicity
                self._advance()
            elif self._current()[0] == "NUMBER":
                self._advance()
            else:
                self._advance()  # operators, etc.

            if self._current() and self._current()[1] == ",":
                self._advance()

        if self._current() and self._current()[1] == ")":
            self._advance()  # )
        if self._current() and self._current()[1] == ";":
            self._advance()  # ;

    # Handle declaration and add to symbol table
    def _handle_declaration(self):
        datatype = self._current()[1]
        self._advance()  # datatype

        if self._is_end():
            return

        name_token = self._current()
        name = name_token[1]
        line = name_token[2]

        if name in self.symbol_table:
            self.errors.append(f"Semantic Error at line {line}: variable '{name}' redeclared")
        else:
            self.symbol_table[name] = {"type": datatype, "value": None}

        self._advance()  # name

        if self._current() and self._current()[1] == "=":
            self._advance()  # =
            self._check_expression()

        if self._current() and self._current()[1] == ";":
            self._advance()

    # Check variables used in expression
    def _check_expression(self):
        while not self._is_end() and self._current()[1] not in {";", ")", ","}:
            tok = self._current()
            if tok[0] == "IDENTIFIER":
                # Only report if NOT a builtin function
                if tok[1] not in self.builtin_functions:
                    if tok[1] not in self.symbol_table:
                        self.errors.append(f"Semantic Error at line {tok[2]}: variable '{tok[1]}' used before declaration")
            self._advance()

    # Check variable usage (left side of assignment)
    def _check_usage(self, name, line):
        if name in self.builtin_functions:
            return  # don't check builtins
        if name not in self.symbol_table:
            self.errors.append(f"Semantic Error at line {line}: variable '{name}' used before declaration")