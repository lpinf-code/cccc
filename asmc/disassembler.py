"""
Disassembler (using objdump)
"""

import re
import sys
import subprocess
import random

from .raw_str import RawStrBuilder

__all__ = ["Disassembler", "Symbol"]

def random_string(t):
    a = ''
    for _ in range(t):
        a += random.choice("abcdef012345678")
    return a

class Symbol:
    ATTRIBUTE = "__attribute__((section(\"%s\")))\n" 
    DEFINITION = "%s %s[%s] = ("
    TABSIZE = 4

    def __init__(self, section: str, name: str, rname: str, hex_bytes: str):
        self.section = section
        self.name = name
        self.real_name = rname
        bc = []
        for i in range(0, len(hex_bytes), 2):
            bc.append(int(hex_bytes[i:i+2], 16))
        self.bytecode = bytes(bc)
        self.string = None

    def build_str(self, ctype: str) -> str:
        out = ""
        if self.name != self.real_name:
            out += '// ' + self.real_name + ' (original identifyer)\n'
        out += Symbol.ATTRIBUTE % (self.section + '#')
        out += Symbol.DEFINITION % (ctype, self.name, len(self.bytecode))
        strings = RawStrBuilder(self.bytecode).build()
        for string in strings:
            out += '\n' + (" " * Symbol.TABSIZE) + f"\"{string}\""
        out += '\n);'
        self.string = out
        return out


class Disassembler:
    EXEC = 'objdump'
    ARGV = [
        '--no-addresses',
        '--disassembler-color=off',
        '-z'
    ]

    def __init__(self, path: str | None, all: bool):
        self.all = all
        self.path = path
        self.obj_disasm = []
        self.symbols = []

    def get_dump(self):
        args = []
        args.append(Disassembler.EXEC)
        args += Disassembler.ARGV
        args.append(['-d', '-D'][self.all])
        if (self.path is not None):
            args.append(self.path)
        process = subprocess.run(
            args,
            stdin=sys.stdin,
            capture_output=True
        )
        if process.returncode != 0:
            raise Exception("Program exited with non-zero status")
        if process.stdout is None:
            raise Exception("No parsable output")
        disasm = process.stdout.decode().splitlines(keepends=False)
        sm = re.compile("^[a-zA-Z ]+\\.(.+):$")
        hm = re.compile("^\t([0-9a-f ]+).+$")
        cur = []
        for line in disasm:
            if line.startswith("Disassembly"):
                if (len(cur) > 0):
                    self.obj_disasm.append("".join(cur))
                self.obj_disasm.append("." + sm.sub("\\1", line))
                cur = []
            elif line.startswith("<"):
                if (len(cur) > 0):
                    self.obj_disasm.append("".join(cur))
                self.obj_disasm.append('!' + line[1:-2])
                cur = []
            elif line.startswith("\t"):
                cur.append(hm.sub("\\1", line).replace(" ", ""))
        self.obj_disasm.append("".join(cur))

    def read_dump(self):
        id = 0
        section = ".text"
        realname = "unknown"
        name = "unknown_" + random_string(5) + hex(id)[2:]
        for e in self.obj_disasm:
            if e.startswith('.'):
                section = e
            elif e.startswith('!.'):
                realname = e[2:]
                if not realname.replace('.', '_') \
                    .replace('-', '_').isidentifier():
                    id += 1
                    name = "unknown_" + random_string(5) + hex(id)[2:]
                else:
                    name = "section_" \
                        + realname.replace('.', '_').replace('-', '_')
                realname = '.' + realname
            elif e.startswith('!'):
                realname = e[1:]
                if not realname.isidentifier():
                    id += 1
                    name = "unknown_" + random_string(5) + hex(id)[2:]
                else:
                    name = realname
            else:
                self.symbols.append(Symbol(section, name, realname, e))

