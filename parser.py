class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    # skip tokens until a safe point
    def recover(self, sync_tokens):
        while self.current() and self.current()[1] not in sync_tokens:
            self.advance()
        if self.current():
            self.advance()

    def parse(self):
        while self.current():
            tok = self.current()

            if tok[1] in ["int", "float", "double", "char"]:
                self.parse_declaration()
            elif tok[1] == "if":
                self.parse_if()
            elif tok[1] == "while":
                self.parse_while()
            elif tok[1] == "printf":
                self.parse_function_call()
            elif tok[0] == "IDENTIFIER":
                self.parse_assignment()
            else:
                self.advance()

        return self.errors

    def parse_declaration(self):
        self.advance()

        if not self.current() or self.current()[0] != "IDENTIFIER":
            self.errors.append("syntax error expected identifier")
            self.recover([";"])
            return

        self.advance()

        if self.current() and self.current()[1] == "=":
            self.advance()
            self.parse_expression()

        if not self.current() or self.current()[1] != ";":
            self.errors.append("syntax error missing semicolon")
            self.recover([";"])
        else:
            self.advance()

    def parse_assignment(self):
        self.advance()

        if not self.current() or self.current()[1] != "=":
            self.errors.append("syntax error expected '='")
            self.recover([";"])
            return

        self.advance()
        self.parse_expression()

        if not self.current() or self.current()[1] != ";":
            self.errors.append("syntax error missing semicolon")
            self.recover([";"])
        else:
            self.advance()

    # function call like printf("text", x + y);
    def parse_function_call(self):
        self.advance()

        if not self.current() or self.current()[1] != "(":
            self.errors.append("syntax error expected '('")
            self.recover([";"])
            return
        self.advance()

        # at least one argument
        self.parse_argument()

        # handle multiple arguments
        while self.current() and self.current()[1] == ",":
            self.advance()
            self.parse_argument()

        if not self.current() or self.current()[1] != ")":
            self.errors.append("syntax error expected ')'")
            self.recover([";"])
            return
        self.advance()

        if not self.current() or self.current()[1] != ";":
            self.errors.append("syntax error missing semicolon")
            self.recover([";"])
            return
        self.advance()


    # parse single argument
    def parse_argument(self):
        # string literal
        if self.current() and self.current()[0] == "STRING":
            self.advance()
            return

        # expression
        self.parse_expression()

    # if statement
    def parse_if(self):
        self.advance()

        if not self.current() or self.current()[1] != "(":
            self.errors.append("syntax error expected '(' after if")
            self.recover(["{"])
            return
        self.advance()

        self.parse_condition()

        if not self.current() or self.current()[1] != ")":
            self.errors.append("syntax error expected ')'")
            self.recover(["{"])
            return
        self.advance()

        if not self.current() or self.current()[1] != "{":
            self.errors.append("syntax error expected '{'")
            self.recover(["}"])
            return
        self.advance()

        self.parse_block()

    # while statement
    def parse_while(self):
        self.advance()

        if not self.current() or self.current()[1] != "(":
            self.errors.append("syntax error expected '(' after while")
            self.recover(["{"])
            return
        self.advance()

        self.parse_condition()

        if not self.current() or self.current()[1] != ")":
            self.errors.append("syntax error expected ')'")
            self.recover(["{"])
            return
        self.advance()

        if not self.current() or self.current()[1] != "{":
            self.errors.append("syntax error expected '{'")
            self.recover(["}"])
            return
        self.advance()

        self.parse_block()

    # parse block of statements until '}'
    def parse_block(self):
        while self.current() and self.current()[1] != "}":
            if self.current()[1] == "printf":
                self.parse_function_call()
            elif self.current()[0] == "IDENTIFIER":
                self.parse_assignment()
            else:
                self.advance()

        if self.current() and self.current()[1] == "}":
            self.advance()
        else:
            self.errors.append("syntax error missing '}'")

    # parse condition inside if or while
    def parse_condition(self):
        self.parse_expression()

        if self.current() and self.current()[1] in [">", "<", ">=", "<=", "==", "!="]:
            self.advance()
            self.parse_expression()
        else:
            self.errors.append("syntax error invalid condition")

    # simple parse expression
    # parse arithmetic expression with casting and parentheses
    def parse_expression(self):
        self.parse_term()

        while self.current() and self.current()[1] in ["+", "-", "*", "/"]:
            self.advance()
            self.parse_term()


    # parse single term
    def parse_term(self):
        # handle type cast like (int)y
        if self.current() and self.current()[1] == "(":
            self.advance()

            # type cast
            if self.current() and self.current()[1] in ["int", "float", "double", "char"]:
                self.advance()
                if self.current() and self.current()[1] == ")":
                    self.advance()
                    self.parse_term()
                    return

            # normal parentheses expression
            self.parse_expression()
            if self.current() and self.current()[1] == ")":
                self.advance()
            else:
                self.errors.append("syntax error expected ')'")
            return

        # identifier or number
        if self.current() and self.current()[0] in ["IDENTIFIER", "NUMBER"]:
            self.advance()
            return

        self.errors.append("syntax error invalid expression")