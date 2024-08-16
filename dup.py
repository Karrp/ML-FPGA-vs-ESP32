import io
import os
import webrepl
from micropython import qstr_info

# duplicate REPL in/out

class DUP(io.IOBase):

    def __init__(self, s:bytearray):
        self.s = s

    def write(self, data):
        self.s += data
        return len(data)

    def readinto(self, data):
        return 0

# # example use:
# s = bytearray() # to store REPL output/input
# os.dupterm(DUP(s)) # start reading from REPL
# # help(webrepl)
# qstr_info() # printing function that want to be stored

# os.dupterm(None) # stop reading from REPL
