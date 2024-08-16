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


exec(open("del_len.py").read())


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

def qstr_read(full:bool=False) -> bytearray:
    ba = bytearray()    # to store REPL output/input # clear bytearray
    dupterm(DUP(ba))    # start reading from REPL

    if full:
        qstr_info(True)
    else:
        qstr_info()     # printing function that want to be stored

    dupterm(None)       # stop reading from REPL
    return ba           # overwriting ba


def qstr_val(b:bytearray) -> tuple[list[int], set[str]]:
    s = b.decode() # to string
    v = set(s.splitlines()[1:]) # save variables names
    s = s.splitlines()[0] # cut first line when qstr_info(True)
    # s = s.split(':')[1] # not needed

    l = s.split(', ')
    l[:] = [int(e.split('=')[1]) for e in l] # extract values and convert to int
    
    return l, v


def execute(path:str, name:list[str], var_names:bool=False, command:list[str]=None):
    # preparation
    # exec(open("del_len.py").read()) # possibly check if running on restarted device
    collect()
    print("")
    
    ext = ".py" # file extension

    length = len(name)

    time_start = [0]*length     # time start
    time_end = [0]*length     # time end
    mem_start = [0]*length     # memory start
    mem_end = [0]*length     # memory end
    qstr_start = [bytearray()]*length   # qstr_info at start
    qstr_end = [bytearray()]*length   # qstr_info at end
    qstr_var_names_start = [set()]*length        # qstr_info variables at start
    qstr_var_names_end = [set()]*length        # qstr_info variables at end

    collect()

    # test all files by executing / importing them (time, memory, qstr_info)
    for i, el in enumerate(name):
        
        if not command: # == None
                # file location and name
            s = path + el + ext # for exec
            s_read = open(s).read()
        else:
            s_read = command[i]
        
        # si = path.replace("/", ".") + el # for import

        print(el,"before:")
        qstr_start[i] = qstr_read(var_names)

        collect()
        mem_start[i] = mem_alloc()
        time_start[i] = ticks_us()

            # execute file
        exec(s_read)
            # import file
            # # import is creating path strings in qstr "path.module" and "path/module.py"
        # __import__(si, globals(), locals(), [], 0)

        time_end[i] = ticks_us()
        # collect()
        mem_end[i] = mem_alloc()

        print(el,"after:")
        qstr_end[i] = qstr_read(var_names)

    # split qstr to values and variables
    for i, el in enumerate(qstr_start):
        qstr_start[i], qstr_var_names_start[i] = qstr_val(el)
    for i, el in enumerate(qstr_end):
        qstr_end[i], qstr_var_names_end[i] = qstr_val(el)

    return name, time_start, time_end, mem_start, mem_end, qstr_start, qstr_end, qstr_var_names_start, qstr_var_names_end, var_names


def slj(variable, space:int=8, sign:str=" ") -> str: # string left just
    s = str(variable)
    return  s + sign*(space - len(s))

def srj(variable, space:int=8, sign:str=" ") -> str: # string right just
    s = str(variable)
    return sign*(space - len(s)) + s


def execute_print(name:list[str], time_start:list[int], time_end:list[int], mem_start:list[int], mem_end:list[int], qstr_start:list[int], qstr_end:list[int], qstr_var_names_start:set[str], qstr_var_names_end:set[str], var_names:bool=False):

    # prepare before values for differences calculartion
    t_empty = ticks_diff( time_end[0], time_start[0] )
    m_empty = mem_end[0] - mem_start[0]

    # print calculations
    print("")
    print( "Element:        Time_us:  T_diff:     Mem:  M_diff:    Pool:    QSTR:   Str_B: Total_B:") # Descriptions
        #   empty:            20425,       0,     592,       0,       0,       0,       0,       0

    for i, el in enumerate(name):
        t = ticks_diff( time_end[i], time_start[i] )
        m = mem_end[i] - mem_start[i]
        q = [qstr_end[i][j] - qstr_start[i][j] for j in range(len(qstr_end[i]))]

        print("{}{},{},{},{},{},{},{},{}".format(slj(el+":",15), srj(t), srj(t - t_empty), srj(m), srj(m - m_empty), srj(q[0]), srj(q[1]), srj(q[2]), srj(q[3]) ) )

    # print variables names added
    if var_names:
        print("")
        print("Element:        Variables:")
        for i, el in enumerate(name):
            print("{}{}".format(slj(el+":",15), qstr_var_names_end[i] - qstr_var_names_start[i]))
        

# exec(open("measure.py").read())
