"""
Raw ASM Function
"""

import os
import uuid
import subprocess

__all__ = ["CFunctionCompiler"]

class CFunctionCompiler:
    EXEC = 'gcc'
    ARGS = ['-nostdlib', '-g0', '-O0', '-c']

    def __init__(self, name: str, c: str, opts: dict):
        if not name.isidentifier():
            raise TypeError("`name` must be an identifyer.")
        self.c = c
        self.code = (
            opts.get('--returns', 'void')
            + ' '
            + name
            + opts.get('--args', '()')
            + '{'
            + c
            + '}'
        )
        self.filename = '/tmp/' + str(uuid.uuid4())
        with open(self.filename + '.c', 'w') as file:
            file.write(self.code)
            file.close()
        process = subprocess.run(
            [CFunctionCompiler.EXEC] + CFunctionCompiler.ARGS
            + [self.filename + '.c', '-o', self.filename]
        )
        os.remove(self.filename + '.c')
        process.check_returncode()

    def destroy(self):
        os.remove(self.filename)
