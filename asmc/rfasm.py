"""
Raw ASM Function
"""

import os
import uuid
import subprocess

__all__ = ["ASMFunctionCompiler"]

class ASMFunctionCompiler:
    EXEC = 'gcc'
    ARGS = ['-nostdlib', '-g0', '-O0', '-c']

    def __init__(self, name: str, asm: str):
        if not name.isidentifier():
            raise TypeError("`name` must be an identifyer.")
        self.asm = asm.replace('"', '\\"').replace("\n","\"\n\"")
        self.code = "void %s(){__asm__(\"%s\");}" % (name, self.asm)
        self.filename = '/tmp/' + str(uuid.uuid4())
        with open(self.filename + '.c', 'w') as file:
            file.write(self.code)
            file.close()
        process = subprocess.run(
            [ASMFunctionCompiler.EXEC] + ASMFunctionCompiler.ARGS
            + [self.filename + '.c', '-o', self.filename]
        )
        os.remove(self.filename + '.c')
        process.check_returncode()

    def destroy(self):
        os.remove(self.filename)
