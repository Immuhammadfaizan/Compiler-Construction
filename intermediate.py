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


    # helpers
    def _is_end(self):
        return self.pos >= len(self.tokens)

    def _current(self):
        if self._is_end():
            return None
        return self.tokens[self.pos]

    def _advance(self):
        if not self._is_end():
            self.pos += 1

    def _new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def _new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"


    # statement dispatcher
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
            self._advance()


    # int x = 10;
    def _declaration(self):
        self._advance()  # datatype
        var_name = self._current()[1]
        self._advance()  # identifier

        if self._current() and self._current()[1] == "=":
            self._advance()
            value = self._expression()
            self.code.append(f"{var_name} = {value}")

        if self._current() and self._current()[1] == ";":
            self._advance()


    # x = y + 5;
    def _assignment(self):
        var_name = self._current()[1]
        self._advance()  # identifier
        self._advance()  # =

        value = self._expression()
        self.code.append(f"{var_name} = {value}")

        if self._current() and self._current()[1] == ";":
            self._advance()


    # expression handling
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
            return "0"

        value = tok[1]
        self._advance()
        return value


    # printf("text", expr, var)
    def _print_stmt(self):
        self._advance()  # printf
        self._advance()  # (

        args = []

        while not self._is_end() and self._current()[1] != ")":
            tok = self._current()

            if tok[0] == "STRING":
                args.append(tok[1])
                self._advance()
            else:
                expr = self._expression()
                args.append(expr)

            if self._current() and self._current()[1] == ",":
                self._advance()

        self._advance()  # )
        self._advance()  # ;

        if args:
            self.code.append("PRINT " + " ".join(args))


    # if else handling
    def _if_stmt(self):
        self._advance()  # if
        self._advance()  # (

        left = self._expression()
        op = self._current()[1]
        self._advance()
        right = self._expression()

        else_label = self._new_label()
        end_label = self._new_label()

        self.code.append(f"IF_FALSE {left} {op} {right} GOTO {else_label}")

        self._advance()  # )
        self._advance()  # {

        while not self._is_end() and self._current()[1] != "}":
            self._statement()

        self._advance()  # }

        self.code.append(f"GOTO {end_label}")
        self.code.append(f"LABEL {else_label}")

        if not self._is_end() and self._current()[1] == "else":
            self._advance()
            self._advance()

            while not self._is_end() and self._current()[1] != "}":
                self._statement()

            self._advance()

        self.code.append(f"LABEL {end_label}")


    # while loop
    def _while_stmt(self):
        start_label = self._new_label()
        end_label = self._new_label()

        self.code.append(f"LABEL {start_label}")

        self._advance()  # while
        self._advance()  # (

        left = self._expression()
        op = self._current()[1]
        self._advance()
        right = self._expression()

        self.code.append(f"IF_FALSE {left} {op} {right} GOTO {end_label}")

        self._advance()  # )
        self._advance()  # {

        while not self._is_end() and self._current()[1] != "}":
            self._statement()

        self._advance()

        self.code.append(f"GOTO {start_label}")
        self.code.append(f"LABEL {end_label}")
