"""
Docstring for executor.py

This file simulates execution of generated target code. 
It behaves like a simple virtual machine.

This will be considered as phase 7 of the compiler.
"""

import codecs

class Executor:
    def __init__(self, target_code):
        self.code = [line.strip() for line in target_code]  # strip lines
        self.pc = 0
        self.registers = {"R1": 0, "R2": 0, "R3": 0}
        self.memory = {}
        self.labels = {}
        self.output = []

        self._scan_labels()

    # store label positions
    def _scan_labels(self):
        for index, line in enumerate(self.code):
            if not line:
                continue
            parts = line.split()
            if len(parts) == 1 and parts[0].endswith(":"):
                label = parts[0][:-1]
                self.labels[label] = index

    # start execution
    def run(self):
        while self.pc < len(self.code):
            raw_line = self.code[self.pc]
            self.pc += 1

            if not raw_line or raw_line.endswith(":"):
                continue

            parts = raw_line.split()
            if not parts:
                continue
            op = parts[0].upper()  # case insensitive

            if op == "LOAD":
                self._load(parts)

            elif op == "STORE":
                self._store(parts)

            elif op == "ADD":
                self._add(parts)

            elif op == "SUB":
                self._sub(parts)

            elif op == "MUL":
                self._mul(parts)

            elif op == "DIV":
                self._div(parts)

            elif op == "JUMP":
                self._jump(parts)

            elif op == "JZ":
                self._jump_zero(parts)

            elif op == "JNZ":
                self._jump_nonzero(parts)

            elif op == "PRINT":
                self._execute_print(parts[1:])

            elif op == "HALT":
                break  # stop execution

            else:
                raise RuntimeError(f"Unknown operation: {op}")

        print()  # final newline if needed
        return self.output

    # load value into register
    def _load(self, parts):
        if len(parts) != 3:
            raise RuntimeError("Invalid LOAD instruction")
        reg = parts[1].rstrip(",")
        value = parts[2]
        try:
            self.registers[reg] = int(value)
        except ValueError:
            self.registers[reg] = self.memory.get(value, 0)

    # store register value into memory
    def _store(self, parts):
        if len(parts) != 3:
            raise RuntimeError("Invalid STORE instruction")
        var = parts[1].rstrip(",")
        reg = parts[2]
        self.memory[var] = self.registers[reg]

    # add operation
    def _add(self, parts):
        if len(parts) != 4:
            raise RuntimeError("Invalid ADD instruction")
        src_reg1 = parts[1].rstrip(",")
        src_reg2 = parts[2].rstrip(",")
        dest = parts[3]
        result = self.registers.get(src_reg1, 0) + self.registers.get(src_reg2, 0)
        self.memory[dest] = result
        self.registers["R3"] = result

    # subtract operation
    def _sub(self, parts):
        if len(parts) != 4:
            raise RuntimeError("Invalid SUB instruction")
        src_reg1 = parts[1].rstrip(",")
        src_reg2 = parts[2].rstrip(",")
        dest = parts[3]
        result = self.registers.get(src_reg1, 0) - self.registers.get(src_reg2, 0)
        self.memory[dest] = result
        self.registers["R3"] = result

    # multiply operation
    def _mul(self, parts):
        if len(parts) != 4:
            raise RuntimeError("Invalid MUL instruction")
        src_reg1 = parts[1].rstrip(",")
        src_reg2 = parts[2].rstrip(",")
        dest = parts[3]
        result = self.registers.get(src_reg1, 0) * self.registers.get(src_reg2, 0)
        self.memory[dest] = result
        self.registers["R3"] = result

    # divide operation
    def _div(self, parts):
        if len(parts) != 4:
            raise RuntimeError("Invalid DIV instruction")
        src_reg1 = parts[1].rstrip(",")
        src_reg2 = parts[2].rstrip(",")
        dest = parts[3]
        val2 = self.registers.get(src_reg2, 0)
        if val2 == 0:
            result = 0  # or raise?
        else:
            result = self.registers.get(src_reg1, 0) // val2
        self.memory[dest] = result
        self.registers["R3"] = result

    # jump to label
    def _jump(self, parts):
        if len(parts) != 2:
            raise RuntimeError("Invalid JUMP instruction")
        label = parts[1]
        if label not in self.labels:
            raise RuntimeError(f"Undefined label: {label}")
        self.pc = self.labels[label]

    # jump if register zero
    def _jump_zero(self, parts):
        if len(parts) != 3:
            raise RuntimeError("Invalid JZ instruction")
        reg = parts[1].rstrip(",")
        label = parts[2]
        if label not in self.labels:
            raise RuntimeError(f"Undefined label: {label}")
        if self.registers.get(reg, 0) == 0:
            self.pc = self.labels[label]

    # jump if register non-zero
    def _jump_nonzero(self, parts):
        if len(parts) != 3:
            raise RuntimeError("Invalid JNZ instruction")
        reg = parts[1].rstrip(",")
        label = parts[2]
        if label not in self.labels:
            raise RuntimeError(f"Undefined label: {label}")
        if self.registers.get(reg, 0) != 0:
            self.pc = self.labels[label]

    # print value
    def _execute_print(self, raw_parts):
        buffer = []
        i = 0
        while i < len(raw_parts):
            token = raw_parts[i]
            if token.startswith('"'):
                # collect full string literal
                text = token
                i += 1
                while i < len(raw_parts) and not text.endswith('"'):
                    text += " " + raw_parts[i]
                    i += 1
                text = text.strip('"')
                # unescape using codecs for C-like escapes
                try:
                    text = codecs.decode(text, 'unicode-escape')
                except ValueError:
                    # fallback to manual if needed, but should work
                    pass
                buffer.append(text)
            else:
                # variable or literal
                token = token.rstrip(",")
                if token in self.memory:
                    buffer.append(str(self.memory[token]))
                elif token in self.registers:
                    buffer.append(str(self.registers[token]))
                elif token.lstrip('-').isdigit():
                    buffer.append(token)
                else:
                    raise RuntimeError(f"runtime error undefined variable {token}")
                i += 1

        line = " ".join(buffer)
        print(line, end=" ")
        self.output.append(line)