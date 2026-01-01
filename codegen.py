"""
Docstring for codegen.py

This phase converts optimized intermediate code into target code.
The output is assembly like instructions for the virtual machine.
"""

class CodeGenerator:
    def __init__(self, optimized_code):
        self.code = optimized_code
        self.target = []

    def generate(self):
        for line in self.code:
            if line.strip():  # skip empty lines
                self._translate(line.strip())
        return self.target

    def _translate(self, line):
        parts = line.split()
        instr = parts[0]

        # keep label exactly for executor
        if instr == "LABEL":
            label = parts[1]
            self.target.append(f"LABEL {label}")
            return

        # keep goto exactly for executor
        if instr == "GOTO":
            label = parts[1]
            self.target.append(f"GOTO {label}")
            return

        # keep IF_FALSE intact for executor
        if instr == "IF_FALSE":
            left = parts[1]
            op = parts[2]
            right = parts[3]
            label = parts[5]
            self.target.append(f"IF_FALSE {left} {op} {right} GOTO {label}")
            return

        # print instruction
        if instr == "PRINT":
            self.target.append(line)
            return

        # assignment or arithmetic
        if len(parts) >= 3 and parts[1] == "=":
            dest = parts[0]

            # simple assignment
            if len(parts) == 3:
                value = parts[2]
                self.target.append(f"LOAD R1, {value}")
                self.target.append(f"STORE {dest}, R1")
                return

            # arithmetic assignment
            if len(parts) == 5:
                op1 = parts[2]
                operator = parts[3]
                op2 = parts[4]

                self.target.append(f"LOAD R1, {op1}")
                self.target.append(f"LOAD R2, {op2}")

                if operator == "+":
                    self.target.append(f"ADD R1, R2, {dest}")
                elif operator == "-":
                    self.target.append(f"SUB R1, R2, {dest}")
                elif operator == "*":
                    self.target.append(f"MUL R1, R2, {dest}")
                elif operator == "/":
                    self.target.append(f"DIV R1, R2, {dest}")
                else:
                    raise ValueError(f"unsupported operator {operator}")

                return

        raise ValueError(f"unknown intermediate instruction: {line}")