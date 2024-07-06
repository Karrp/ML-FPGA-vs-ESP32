import time

# int /  int -> float
# int // int -> int
# float // float -> float(int)
# float / float -> float

def calculations(a, b, loops:int):
    r = range(loops)
    us = time.ticks_us
    diff = time.ticks_diff
    a_type = str(type(a)).split('\'')[1]

    # addition
    t0 = us()
    for _ in r:
        c = a + b

    # subtraction
    t1 = us()
    for _ in r:
        c = a - b

    t2 = us()
    for _ in r:
        c = b - a

    # multiply
    t3 = us()
    for _ in r:
        c = a * b

    t3x = us()

    # divide
    if  a_type == 'int':
        t4 = us()
        for _ in r:
            c = a // b

        t5 = us()
        for _ in r:
            c = b // a
    else:
        t4 = us()
        for _ in r:
            c = a / b

        t5 = us()
        for _ in r:
            c = b / a

    t6 = us()

    print()
    print("\t type:\t", a_type)
    print("a + b = {}\t {}us".format((a + b), diff(t1, t0)))
    print("a - b = {}\t {}us".format((a - b), diff(t2, t1)))
    print("b - a = {}\t {}us".format((b - a), diff(t3, t2)))
    print("a * b = {}\t {}us".format((a * b), diff(t3x, t3)))
    if  a_type == 'int':
        print("a / b = {}\t {}us".format((a // b), diff(t5, t4)))
        print("b / a = {}\t {}us".format((b // a), diff(t6, t5)))
    else:
        print("a / b = {}\t {}us".format((a / b), diff(t5, t4)))
        print("b / a = {}\t {}us".format((b / a), diff(t6, t5)))
    print("")


def inputs():

    # ints
    calculations(4, 2, 10000)

    # floats
    calculations(4.0, 2.0, 10000)

inputs()

# exec(open("performance/int_float.py").read())
