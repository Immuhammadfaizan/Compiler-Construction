class CodeOptimizer:
    def __init__(self, intermediate_code):
        self.code = intermediate_code
        self.optimized = []

    def optimize(self):
        self._remove_duplicate_lines()
        self._constant_folding()
        self._remove_unused_temps()
        return self.optimized

    # remove repeated instructions
    def _remove_duplicate_lines(self):
        seen = set()
        for line in self.code:
            if line not in seen:
                seen.add(line)
                self.optimized.append(line)

    # simplify constant expressions
    def _constant_folding(self):
        new_code = []

        for line in self.optimized:
            parts = line.split()

            if len(parts) == 5 and parts[1] == "=":
                left = parts[0]
                op1 = parts[2]
                operator = parts[3]
                op2 = parts[4]

                if self._is_number(op1) and self._is_number(op2):
                    result = self._evaluate(op1, operator, op2)
                    new_code.append(f"{left} = {result}")
                else:
                    new_code.append(line)
            else:
                new_code.append(line)

        self.optimized = new_code

    # remove unused temporary variables
    def _remove_unused_temps(self):
        used = set()

        for line in self.optimized:
            for part in line.split():
                if part.startswith("t"):
                    used.add(part)

        final_code = []
        for line in self.optimized:
            if "=" in line:
                left = line.split("=")[0].strip()
                if left.startswith("t") and left not in used:
                    continue
            final_code.append(line)

        self.optimized = final_code

    # helpers
    def _is_number(self, value):
        return value.replace('.', '', 1).isdigit()

    def _evaluate(self, a, op, b):
        a = float(a)
        b = float(b)

        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            return a / b

        return 0