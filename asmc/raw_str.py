"""
Raw String Builder
"""

__all__ = ["RawStrBuilder"]

class RawStrBuilder:
    MAX_WIDTH = 65

    def __init__(self, bs: bytes):
        self.input = bs

    def represent(self, b: int, n: int):
        if (b >= 32 and b <= 126) and (b != ord(';')):
            if b == ord('\'') or b == ord('\"'):
                return f"\\{chr(b)}"
            return chr(b)
        if (b == ord('\n')):
            return '\\n'
        if (b == ord('\t')):
            return '\\t'
        if (b == ord('\x1b')):
            return '\\e'
        if (b == 0):
            return '\\0'
        out = hex(b)[2:]
        if (len(out) == 1):
            out = '0' + out
        if (n >= 48 and n <= 57) or (n >= 65 and n <= 70) \
            or (n >= 97 and n <= 102):
            out+='""'
        return f"\\x{out}"

    def build(self) -> list[str]:
        out = []
        data = ""
        for i in range(len(self.input)):
            byte = self.input[i]
            next_byte = 0
            if (len(self.input) > i + 1):
                next_byte = self.input[i + 1]
            data += self.represent(byte, next_byte)
            if (len(data) > RawStrBuilder.MAX_WIDTH):
                if (data.endswith('""')):
                    data = data[:-2]
                out.append(data)
                data = ""
        if (len(data) > 0):
            out.append(data)
        return out;
