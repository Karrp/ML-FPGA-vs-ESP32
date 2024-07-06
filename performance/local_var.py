# check impact of the buffer recycling

import measure
import time
import gc
import random
from micropython import const

LOOPS = const(1_000)
# LOOPS = 10000

t = [0]*2
r = [0]*2
td = 0
# rand = random.getrandbits
# rand(2)

# Global variables
gc.collect() # collect garbage
r[0] = gc.mem_alloc()
t[0] = time.ticks_us()

x = 1
y = 2
for _ in range(LOOPS):
    # x += rand(2)
    b = x
    x = y
    y = b

td = time.ticks_us()
t[0] = time.ticks_diff(td, t[0])
r[0] = gc.mem_alloc() - r[0]

# del x
# del y
# del b


# Local variables
gc.collect() # collect garbage
# r[1] = gc.mem_alloc()

def var_loc():
    x = 1
    y = 2
    for _ in range(LOOPS):
        # x += rand(2)
        b = x
        x = y
        y = b
    # return x

r[1] = gc.mem_alloc()
t[1] = time.ticks_us()

# print(var_loc())
var_loc()

td = time.ticks_us()
t[1] = time.ticks_diff(td, t[1])
r[1] = gc.mem_alloc() - r[1]



def p_res():
    for i, _ in enumerate(t):
        print("\nIter:\t", i)
        print("Time:\t", t[i])
        print("Ram:\t", r[i])

p_res()


# exec(open("performance/local_var.py").read())
