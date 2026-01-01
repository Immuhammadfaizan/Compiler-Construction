class Executor:
    def __init__(self, target_code):
        self.code = target_code
        self.ip = 0
        self.memory = {}
        self.labels = {}
        self.output = []
        self._map_labels()

    # map labels to instruction indexes
    def _map_labels(self):
        for i, line in enumerate(self.code):
            if line.startswith("LABEL"):
                label = line.split()[1]
                self.labels[label] = i

    # main execution loop
    def run(self):
        while self.ip < len(self.code):
            line = self.code[self.ip].strip()

            if line.startswith("LOAD"):
                self._load(line)
                self.ip += 1

            elif line.startswith("STORE"):
                self._store(line)
                self.ip += 1

            elif line.startswith("PRINT"):
                self._print(line)
                self.ip += 1

            elif line.startswith("IF_FALSE"):
                self._if_false(line)

            elif line.startswith("GOTO"):
                self._goto(line)

            elif line.startswith("LABEL"):
                self.ip += 1

            else:
                self.ip += 1

        print("\nOutput:", self.output)

    # LOAD R1, 10
    def _load(self, line):
        _, reg, value = line.replace(",", "").split()
        if value.isdigit():
            self.memory[reg] = int(value)
        else:
            self.memory[reg] = self.memory.get(value, 0)

    # STORE x, R1
    def _store(self, line):
        _, var, reg = line.replace(",", "").split()
        self.memory[var] = self.memory.get(reg, 0)

    # PRINT "text", x + y
    def _print(self, line):
        content = line[len("PRINT"):].strip()
        args = [arg.strip() for arg in content.split(",")]

        out = []

        for arg in args:
            # string literal
            if arg.startswith('"') and arg.endswith('"'):
                out.append(arg[1:-1])
                continue

            # number
            if arg.isdigit():
                out.append(str(int(arg)))
                continue

            # variable
            if arg in self.memory:
                out.append(str(self.memory[arg]))
                continue

            # expression
            value = self._eval_expr(arg)
            out.append(str(value))

        result = " ".join(out)
        print(result)
        self.output.append(result)

    # IF_FALSE x > y GOTO L1
    def _if_false(self, line):
        parts = line.split()
        left = parts[1]
        op = parts[2]
        right = parts[3]
        label = parts[5]

        a = self.memory.get(left, 0)
        b = self.memory.get(right, 0)

        if not self._eval_condition(a, op, b):
            self.ip = self.labels[label]
        else:
            self.ip += 1

    # GOTO L1
    def _goto(self, line):
        label = line.split()[1]
        self.ip = self.labels[label]

    # evaluate condition
    def _eval_condition(self, a, op, b):
        if op == ">": return a > b
        if op == "<": return a < b
        if op == ">=": return a >= b
        if op == "<=": return a <= b
        if op == "==": return a == b
        if op == "!=": return a != b
        return False

    # evaluate expression like x + y
    def _eval_expr(self, expr):
        expr = expr.strip()

        if expr.isdigit():
            return int(expr)

        if expr in self.memory:
            return self.memory[expr]

        parts = expr.split()
        if len(parts) != 3:
            raise RuntimeError(f"invalid expression {expr}")

        left, op, right = parts

        a = self.memory[left] if left in self.memory else int(left)
        b = self.memory[right] if right in self.memory else int(right)

        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/": return a // b

        raise RuntimeError(f"unsupported operator {op}")
