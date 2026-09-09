"""
Interpreter / Execution Engine for MiniLang.
Executes Three-Address Code (TAC) instructions on a virtual machine model.
Catches runtime errors such as division by zero.
"""

from tac import TACInstruction


class RuntimeError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Runtime Error: {message}")


class Interpreter:
    def __init__(self, instructions: list[TACInstruction]):
        self.instructions = instructions
        self.env: dict[str, int | float] = {}
        self.labels: dict[str, int] = {}
        self.output_buffer: list[str] = []

        # Index labels for fast GOTO
        for idx, inst in enumerate(self.instructions):
            if inst.op == "LABEL" and inst.result:
                self.labels[inst.result] = idx

    def _eval_val(self, val: str | int | float | None) -> int | float:
        if val is None:
            raise RuntimeError("Attempted to evaluate None value.")
        if isinstance(val, (int, float)):
            return val
        if isinstance(val, str):
            if val in self.env:
                return self.env[val]
            raise RuntimeError(f"Variable or temporary '{val}' accessed before assignment.")
        raise RuntimeError(f"Unknown value type '{type(val)}'")

    def execute(self) -> list[str]:
        pc = 0
        n = len(self.instructions)

        while pc < n:
            inst = self.instructions[pc]
            op = inst.op

            if op == "ASSIGN":
                val = self._eval_val(inst.arg1)
                self.env[inst.result] = val
                pc += 1

            elif op in ("+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="):
                v1 = self._eval_val(inst.arg1)
                v2 = self._eval_val(inst.arg2)
                res = None

                if op == "+":
                    res = v1 + v2
                elif op == "-":
                    res = v1 - v2
                elif op == "*":
                    res = v1 * v2
                elif op == "/":
                    if v2 == 0:
                        raise RuntimeError("Division by zero.")
                    res = int(v1 // v2) if isinstance(v1, int) and isinstance(v2, int) else v1 / v2
                elif op == "==":
                    res = 1 if v1 == v2 else 0
                elif op == "!=":
                    res = 1 if v1 != v2 else 0
                elif op == "<":
                    res = 1 if v1 < v2 else 0
                elif op == ">":
                    res = 1 if v1 > v2 else 0
                elif op == "<=":
                    res = 1 if v1 <= v2 else 0
                elif op == ">=":
                    res = 1 if v1 >= v2 else 0

                self.env[inst.result] = res
                pc += 1

            elif op == "NEG":
                val = self._eval_val(inst.arg1)
                self.env[inst.result] = -val
                pc += 1

            elif op == "PRINT":
                val = self._eval_val(inst.arg1)
                output_str = str(val)
                self.output_buffer.append(output_str)
                print(output_str)
                pc += 1

            elif op == "JUMP":
                target_lbl = inst.result
                if target_lbl in self.labels:
                    pc = self.labels[target_lbl]
                else:
                    raise RuntimeError(f"Jump label '{target_lbl}' not found.")

            elif op == "JUMP_IF_FALSE":
                cond_val = self._eval_val(inst.arg1)
                if cond_val == 0 or cond_val is False:
                    target_lbl = inst.result
                    if target_lbl in self.labels:
                        pc = self.labels[target_lbl]
                    else:
                        raise RuntimeError(f"Jump label '{target_lbl}' not found.")
                else:
                    pc += 1

            elif op == "LABEL":
                pc += 1

            else:
                raise RuntimeError(f"Unknown TAC operation '{op}'")

        return self.output_buffer
