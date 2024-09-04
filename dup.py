import io
import os
import webrepl
from micropython import qstr_info

class DUP(io.IOBase):

    def __init__(self, s):
        self.s = s

    def write(self, data):
        self.s += data.decode()
        return len(data)

    def readinto(self, data):
        return 0

# s = bytearray()
s = "dupa"
os.dupterm(DUP(s))
# help(webrepl)
qstr_info() # printing function that want to be stored

os.dupterm(None)