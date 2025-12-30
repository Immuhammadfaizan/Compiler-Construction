""" 
Docstring for intermediate.py

This phase converts source level constructs into intermediate code.
The output is Three Address Code (TAC).
"""

class IntermediateCodeGenerator:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def generate(self):
        while not self._is_end():
            self._statement()
        return self.code

    # basic helpers
    def _is_end(self):
        return self.pos >= len(self.tokens)

    def _current(self):
        if self._is_end():
            return None
        return self.tokens[self.pos]

    def _advance(self):
        if not self._is_end():
            self.pos += 1

    def _peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def _new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def _new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    # statement handling
    def _statement(self):
        token = self._current()
        if not token:
            return

        tok_type, tok_val, _ = token

        if tok_type == "KEYWORD" and tok_val in ("int", "float", "double", "char"):
            self._declaration()

        elif tok_type == "IDENTIFIER":
            self._assignment()

        elif tok_type == "BUILTIN_FUNC" and tok_val == "printf":
            self._print_stmt()

        elif tok_type == "KEYWORD" and tok_val == "if":
            self._if_stmt()

        elif tok_type == "KEYWORD" and tok_val == "while":
            self._while_stmt()

        else:
            self._advance()  # skip unknown

    # declaration: int x = 10;
    def _declaration(self):
        self._advance()  # skip datatype
        var_name = self._current()[1]
        self._advance()  # identifier

        if self._current() and self._current()[1] == "=":
            self._advance()  # =
            value = self._expression()
            self.code.append(f"{var_name} = {value}")

        if self._current() and self._current()[1] == ";":
            self._advance()  # ;

    # assignment: x = y + 5;
    def _assignment(self):
        var_name = self._current()[1]
        self._advance()  # identifier
        self._advance()  # =

        value = self._expression()
        self.code.append(f"{var_name} = {value}")

        if self._current() and self._current()[1] == ";":
            self._advance()  # ;

    # expressions: + - * /
    def _expression(self):
        left = self._term()

        while not self._is_end() and self._current()[1] in ("+", "-"):
            op = self._current()[1]
            self._advance()
            right = self._term()
            temp = self._new_temp()
            self.code.append(f"{temp} = {left} {op} {right}")
            left = temp

        return left

    def _term(self):
        left = self._factor()

        while not self._is_end() and self._current()[1] in ("*", "/"):
            op = self._current()[1]
            self._advance()
            right = self._factor()
            temp = self._new_temp()
            self.code.append(f"{temp} = {left} {op} {right}")
            left = temp

        return left

    def _factor(self):
        tok = self._current()
        if not tok:
            return "0"  # safety

        value = tok[1]
        self._advance()
        return value

    # printf("Hello", x + y, 42);
    def _print_stmt(self):
        self._advance()  # printf
        self._advance()  # (

        args = []

        # parse arguments
        while not self._is_end() and self._current()[1] != ")":
            tok = self._current()

            if tok[0] == "STRING":
                # Keep quotes exactly as in source
                args.append(tok[1])  # e.g. "Hello\nWorld"
                self._advance()

            else:
                # expression argument
                expr_result = self._expression()
                args.append(expr_result)

            # comma?
            if self._current() and self._current()[1] == ",":
                self._advance()

        self._advance()  # )
        self._advance()  # ;

        # Emit single PRINT with all arguments
        if args:
            print_line = "PRINT " + " ".join(args)
            self.code.append(print_line)

    # if statement
    def _if_stmt(self):
        self._advance()  # if
        self._advance()  # (

        condition = self._expression()
        end_label = self._new_label()

        self.code.append(f"IF_FALSE {condition} GOTO {end_label}")

        self._advance()  # )
        self._advance()  # {

        while not self._is_end() and self._current()[1] != "}":
            self._statement()

        self._advance()  # }
        self.code.append(f"LABEL {end_label}")

    # while loop
    def _while_stmt(self):
        start_label = self._new_label()
        end_label = self._new_label()

        self.code.append(f"LABEL {start_label}")

        self._advance()  # while
        self._advance()  # (

        condition = self._expression()
        self.code.append(f"IF_FALSE {condition} GOTO {end_label}")

        self._advance()  # )
        self._advance()  # {

        while not self._is_end() and self._current()[1] != "}":
            self._statement()

        self._advance()  # }
        self.code.append(f"GOTO {start_label}")
        self.code.append(f"LABEL {end_label}")