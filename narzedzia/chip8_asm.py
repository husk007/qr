#!/usr/bin/env python3
"""Minimalny asembler CHIP-8. Uzycie: python3 asm.py program.asm -> wypisuje ROM w hex."""
import re
import sys


def reg(s):
    assert re.fullmatch(r"V[0-9A-F]", s, re.I), s
    return int(s[1], 16)


def num(s, labels):
    s = s.strip()
    if s in labels:
        return labels[s]
    return int(s, 0)


def assemble(src):
    lines = []
    for raw in src.splitlines():
        line = raw.split(";")[0].strip()
        if line:
            lines.append(line)
    labels, addr, items = {}, 0x200, []
    for line in lines:
        while ":" in line.split()[0]:
            lab, line = line.split(":", 1)
            labels[lab.strip()] = addr
            line = line.strip()
            if not line:
                break
        if not line:
            continue
        op, *rest = line.split(None, 1)
        args = [a.strip() for a in rest[0].split(",")] if rest else []
        size = len(args) if op.upper() == "DB" else 2
        items.append((addr, op.upper(), args))
        addr += size
    out = bytearray()
    for addr, op, a in items:
        if op == "DB":
            out += bytes(num(x, labels) for x in a)
            continue
        A = a + [""] * 3
        if op == "CLS": w = 0x00E0
        elif op == "RET": w = 0x00EE
        elif op == "JP": w = 0x1000 | num(A[0], labels)
        elif op == "CALL": w = 0x2000 | num(A[0], labels)
        elif op == "SE" and A[1].upper().startswith("V"): w = 0x5000 | reg(A[0]) << 8 | reg(A[1]) << 4
        elif op == "SE": w = 0x3000 | reg(A[0]) << 8 | num(A[1], labels) & 255
        elif op == "SNE" and A[1].upper().startswith("V"): w = 0x9000 | reg(A[0]) << 8 | reg(A[1]) << 4
        elif op == "SNE": w = 0x4000 | reg(A[0]) << 8 | num(A[1], labels) & 255
        elif op == "LD":
            d, s = A[0].upper(), A[1].upper()
            if d == "I": w = 0xA000 | num(A[1], labels)
            elif d == "DT": w = 0xF015 | reg(s) << 8
            elif d == "ST": w = 0xF018 | reg(s) << 8
            elif d == "F": w = 0xF029 | reg(s) << 8
            elif d == "B": w = 0xF033 | reg(s) << 8
            elif d == "[I]": w = 0xF055 | reg(s) << 8
            elif s == "[I]": w = 0xF065 | reg(d) << 8
            elif s == "DT": w = 0xF007 | reg(d) << 8
            elif s == "K": w = 0xF00A | reg(d) << 8
            elif s.startswith("V"): w = 0x8000 | reg(d) << 8 | reg(s) << 4
            else: w = 0x6000 | reg(d) << 8 | num(A[1], labels) & 255
        elif op == "ADD" and A[0].upper() == "I": w = 0xF01E | reg(A[1]) << 8
        elif op == "ADD" and A[1].upper().startswith("V"): w = 0x8004 | reg(A[0]) << 8 | reg(A[1]) << 4
        elif op == "ADD": w = 0x7000 | reg(A[0]) << 8 | num(A[1], labels) & 255
        elif op in ("OR", "AND", "XOR", "SUB", "SHR", "SUBN", "SHL"):
            n = {"OR": 1, "AND": 2, "XOR": 3, "SUB": 5, "SHR": 6, "SUBN": 7, "SHL": 14}[op]
            w = 0x8000 | reg(A[0]) << 8 | reg(A[1] or A[0]) << 4 | n
        elif op == "RND": w = 0xC000 | reg(A[0]) << 8 | num(A[1], labels) & 255
        elif op == "DRW": w = 0xD000 | reg(A[0]) << 8 | reg(A[1]) << 4 | num(A[2], labels)
        elif op == "SKP": w = 0xE09E | reg(A[0]) << 8
        elif op == "SKNP": w = 0xE0A1 | reg(A[0]) << 8
        else: raise SystemExit(f"Nieznana instrukcja: {op} {a}")
        out += w.to_bytes(2, "big")
    return bytes(out)


if __name__ == "__main__":
    rom = assemble(open(sys.argv[1]).read())
    if len(sys.argv) > 2:
        open(sys.argv[2], "wb").write(rom)
    print(len(rom), "B:", rom.hex())
