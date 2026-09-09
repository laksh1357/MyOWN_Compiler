"""
TAC Optimizer for MiniLang.
Performs Constant Folding and Dead Code Elimination on TAC instructions.
"""

from tac import TACInstruction


class TACOptimizer:
    def __init__(self, instructions: list[TACInstruction]):
        self.instructions = instructions

    def optimize(self) -> list[TACInstruction]:
        optimized = self._constant_folding(self.instructions)
        optimized = self._dead_code_elimination(optimized)
        return optimized

    def _constant_folding(self, insts: list[TACInstruction]) -> list[TACInstruction]:
        res: list[TACInstruction] = []
        for inst in insts:
            if inst.op in ("+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="):
                arg1_is_num = isinstance(inst.arg1, (int, float))
                arg2_is_num = isinstance(inst.arg2, (int, float))

                if arg1_is_num and arg2_is_num:
                    val1 = inst.arg1
                    val2 = inst.arg2
                    folded_val = None
                    try:
                        if inst.op == "+":
                            folded_val = val1 + val2
                        elif inst.op == "-":
                            folded_val = val1 - val2
                        elif inst.op == "*":
                            folded_val = val1 * val2
                        elif inst.op == "/":
                            if val2 != 0:
                                folded_val = int(val1 // val2) if isinstance(val1, int) and isinstance(val2, int) else val1 / val2
                        elif inst.op == "==":
                            folded_val = 1 if val1 == val2 else 0
                        elif inst.op == "!=":
                            folded_val = 1 if val1 != val2 else 0
                        elif inst.op == "<":
                            folded_val = 1 if val1 < val2 else 0
                        elif inst.op == ">":
                            folded_val = 1 if val1 > val2 else 0
                        elif inst.op == "<=":
                            folded_val = 1 if val1 <= val2 else 0
                        elif inst.op == ">=":
                            folded_val = 1 if val1 >= val2 else 0
                    except ZeroDivisionError:
                        pass

                    if folded_val is not None:
                        # Replace binary op with constant assignment
                        res.append(TACInstruction("ASSIGN", folded_val, None, inst.result))
                        continue

            elif inst.op == "NEG" and isinstance(inst.arg1, (int, float)):
                res.append(TACInstruction("ASSIGN", -inst.arg1, None, inst.result))
                continue

            res.append(inst)
        return res

    def _dead_code_elimination(self, insts: list[TACInstruction]) -> list[TACInstruction]:
        res: list[TACInstruction] = []
        unreachable = False

        for inst in insts:
            if inst.op == "LABEL":
                unreachable = False
                res.append(inst)
            elif unreachable:
                continue
            else:
                res.append(inst)
                if inst.op == "JUMP":
                    unreachable = True

        return res
