# for measuring parameters of uC
# time, memmory
    
from os import statvfs, dupterm
from gc import collect, mem_alloc, mem_free
from time import ticks_us, ticks_diff
from micropython import mem_info, qstr_info, stack_use, opt_level
from dup import DUP


def help():
    print("avilable_space()\t- shows free file space")
    print("avilable_ram(<>)\t- shows available ram <short=False>")


# just 9 minutes with microsecond resolution
# 6 days with millisecond resolution

# any function timig by "@timed_function" decorator
def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t0 = ticks_us()
        result = f(*args, **kwargs)
        t1 = ticks_us()
        delta = ticks_diff(t1, t0)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func


def avilable_space():
    stat = statvfs('//')
    return ('{0} MB'.format((stat[0]*stat[3])/1048576))


def avilable_ram(short = True):
    collect() # collect garbage
    free = mem_free()
    allocated = mem_alloc()
    total = free + allocated
    percentage = '{0:.2f}%'.format(free/total*100)

    if short:
        return percentage
    else:
        return ('Total:{0} Free:{1} ({2})'.format(total, free, percentage))



# ---------------------------- Is it needed? V ----------------------------

# time_mem_result = [None]*3 # Time, RAM, File_space
# global time_mem_result
time_mem_result = {"func":"", "time":"", "ram":"", "space":""}

# any function timig and memory by "@time_mem" decorator
def time_mem(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        # global time_mem_result

        collect() # collect garbage

        # check uC parameters before function
        ram = mem_alloc()
        stat = statvfs('//')
        file_space = (stat[0]*stat[3])#/1048576   # avilable space in MB
        t = ticks_us()

        # run function
        result = f(*args, **kwargs)

        # check uC parameters after function and calculate difference
        t_delta = ticks_diff(ticks_us(), t)
        ram_delta = mem_alloc() - ram
        stat = statvfs('//')
        file_space_delta = (stat[0]*stat[3]) - file_space #/1048576   # avilable space in MB

        # time_mem_result[0] = t_delta
        # time_mem_result[1] = ram_delta
        # time_mem_result[2] = file_space_delta

        time_mem_result["func"] = myname
        time_mem_result["time"] = t_delta
        time_mem_result["ram"] = ram_delta
        time_mem_result["space"] = file_space_delta

        # print(time_mem_result)

        # write results
        # print('\nFunction {}'.format(myname))
        # print('Time = {:6.3f}ms'.format(t_delta/1000))
        # print('Ram = {}b'.format(ram_delta))
        # print('File space = {}MB'.format(file_space_delta/1048576))
        # print('T:{}us R:{} F:{}MB\n'.format(t_delta, ram_delta, file_space_delta/1048576))
        return result
    return new_func

# any function timig and memory by "@t_m" decorator
def t_m(n, f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    # def new_func(*args, **kwargs):

    collect() # collect garbage

    # check uC parameters before function
    ram = mem_alloc()
    # stat = os.statvfs('//')
    # file_space = (stat[0]*stat[3])#/1048576   # avilable space in MB
    t0 = ticks_us()

    # run function
    for _ in range(n):
        f(*args, **kwargs)

    # check uC parameters after function and calculate difference
    t1 = ticks_us()
    t_delta = ticks_diff(t1, t0)
    ram_delta = mem_alloc() - ram
    # stat = os.statvfs('//')
    # file_space_delta = (stat[0]*stat[3]) - file_space #/1048576   # avilable space in MB

    # time_mem_result["func"] = myname
    # time_mem_result["time"] = t_delta
    # time_mem_result["ram"] = ram_delta
    # time_mem_result["space"] = file_space_delta

    # print(time_mem_result)

    # write results
    print('\nFunction {}'.format(myname))
    print('Time = {:6.3f}ms'.format(t_delta/1000/n))
    print('Ram = {}b'.format(ram_delta/n))
    print('T:{}us R:{}b\n'.format(t_delta/n, ram_delta/n))
    

def print_result(result):
    print('')
    print('F name:\t{}'.format(result["func"]))
    print('Time =\t{:.3f} ms'.format(result["time"]/1000))
    print('RAM =\t{} b'.format(result["ram"]))
    print('Space =\t{} MB'.format(result["space"]/1048576))

# ---------------------------- Is it needed? ^ ----------------------------



# additional functions
# https://docs.micropython.org/en/latest/library/micropython.html#functions
# import micropython
# micropython.mem_info() or (True)  # heap info and map
    # Each letter represents a single block of memory, and each block is 16 bytes.
    # So each line of the heap dump represents 0x400 bytes or 1k of memory.
# micropython.qstr_info() or (True) # variables defined
# micropython.stack_use()           # stack used - integer


# exec(open("measure.py").read())
