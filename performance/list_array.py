import array
import gc
import random
import time

try:
    del(len)
    print("len deleted")
except:
    print("len not exists")

def l_a_test(elements = 100, pos = 100, pos_times=100, pythonic = False):
    gc.collect() 

    # cashing functions
    us = time.ticks_us
    diff = time.ticks_diff
    rrange = random.randrange
    mem = gc.mem_alloc
    # predefining variables
    t0 = us()
    t1 = us()
    m0 = mem()
    m1 = mem()
    buf = 0

    # positions
    l_pos = [0]*pos
    for i in range(len(l_pos)):
        l_pos[i] = rrange(elements)
    
    a_pos = array.array('i', l_pos)


    ### LIST ###
    print("\n\n--- LIST ---")
    # list
    gc.collect()
    m0 = mem()
    t0 = us()
    l = [0]*elements # list
    t1 = us()
    gc.collect()
    m1 = mem()
    print("\nl = [0]*{}\t\t\t\t {}b\t {}us".format(elements, (m1-m0), diff(t1, t0)))

    # changing value of every element
    t0 = us()
    for i in range(len(l)):
        l[i] = i
    t1 = us()
    print("\tchange every element:\t{}us".format(diff(t1, t0)))

    # random access to list
    buf = 0
    t0 = us()
    for _ in range(pos_times):
        for i in l_pos:
            buf += l[i]
    t1 = us()
    print("\trandom acces time:\t{}us\tper access".format(diff(t1, t0)/(pos*pos_times)))

    # create and fill list by appending
    gc.collect()
    m0 = mem()
    t0 = us()
    la = []
    for i in range(elements):
        la.append(i)
    t1 = us()
    gc.collect()
    m1 = mem()
    print("\nla = [0]*{}\t\t\t\t {}b\t {}us".format(elements, (m1-m0), diff(t1, t0)))


    ### ARRAY ###
    print("\n\n--- ARRAY ---")
    # array
    gc.collect()
    m0 = mem()
    t0 = us()
    a = array.array('i',[0]*elements) # creates list inside -> [0]*elements
    t1 = us()
    gc.collect()
    m1 = mem()
    print("\narray('i',[0]*{})\t\t\t {}b\t {}us".format(elements, (m1-m0), diff(t1, t0)))

    # changing value of every element of array
    t0 = us()
    for i in range(len(l)):
        a[i] = i
    t1 = us()
    print("\tchange every element:\t{}us".format(diff(t1, t0)))

    # random access to array
    buf = 0
    t0 = us()
    for _ in range(pos_times):
        for i in a_pos:
            buf += a[i]
    t1 = us()
    print("\trandom acces time:\t{}us\tper access\n".format(diff(t1, t0)/(pos*pos_times)))

    # create and fill array by appending
    gc.collect()
    m0 = mem()
    t0 = us()
    aa = array.array('i')
    for i in range(elements):
        aa.append(i)
    t1 = us()
    gc.collect()
    m1 = mem()
    print("\naa = [0]*{}\t\t\t\t {}b\t {}us".format(elements, (m1-m0), diff(t1, t0)))

    # creating array from existing list
    a_list = [0]*elements # list
    gc.collect()
    m0 = mem()
    t0 = us()
    al = array.array('i', a_list)
    t1 = us()
    gc.collect()
    m1 = mem()
    print("\narray('i',list)\t\t\t\t {}b\t {}us".format( (m1-m0), diff(t1, t0)))


    # clean and slow pythonic array
    del(a)
    gc.collect()

    if pythonic:
        gc.collect()
        m0 = mem()
        t0 = us()
        b = array.array('i', (0 for _ in range(elements))) # slower but pythonic ? array
        t1 = us()
        gc.collect()
        m1 = mem()
        print("\narray('i',(0 for _ in range({})))\t {}b\t {}us".format(elements, (m1-m0), diff(t1, t0)))


l_a_test(1_000, 100, 1_000, True)

# exec(open("performance/list_array.py").read())
