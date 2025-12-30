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

        op = parts[0]

        # Label definition
        if op == "LABEL":
            label = parts[1]
            self.target.append(f"{label}:")
            return

        # Unconditional jump
        if op == "GOTO":
            label = parts[1]
            self.target.append(f"JMP {label}")
            return

        # Conditional jump: IF_FALSE x GOTO L1
        if op == "IF_FALSE":
            condition = parts[1]        # e.g., t1 or x
            _ = parts[2]                # GOTO
            label = parts[3]            # L1
            self.target.append(f"LOAD R1, {condition}")
            self.target.append(f"JZ R1, {label}")
            return

        # Print statement: PRINT "Hello" t1 42
        if op == "PRINT":
            # Reconstruct the full PRINT instruction exactly as needed
            # Keeps string quotes and spaces intact
            full_print = " ".join(parts)
            self.target.append(full_print)
            return

        # Assignment: x = 10    or    t1 = x + y
        if len(parts) >= 3 and parts[1] == "=":
            left = parts[0]             # destination (variable or temp)

            # Simple assignment: x = 10
            if len(parts) == 3:
                value = parts[2]
                self.target.append(f"LOAD R1, {value}")
                self.target.append(f"STORE {left}, R1")
                return

            # Arithmetic: t1 = x + y
            if len(parts) == 5:
                op1 = parts[2]
                operator = parts[3]
                op2 = parts[4]

                self.target.append(f"LOAD R1, {op1}")
                self.target.append(f"LOAD R2, {op2}")

                if operator == "+":
                    self.target.append(f"ADD R1, R2, {left}")
                elif operator == "-":
                    self.target.append(f"SUB R1, R2, {left}")
                elif operator == "*":
                    self.target.append(f"MUL R1, R2, {left}")
                elif operator == "/":
                    self.target.append(f"DIV R1, R2, {left}")
                else:
                    raise ValueError(f"Unsupported operator: {operator}")

                return

        raise ValueError(f"Unknown or malformed intermediate instruction: {line}")