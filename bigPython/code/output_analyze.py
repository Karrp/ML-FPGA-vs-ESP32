from analyze import qstr_val, mem_val

# strings for frame (fr)
# d^-^b ["---> start"/"<--- stop"], <name>, <function>, ["before"/"after"]
fr_sign = "d^-^b" # start of the frame
fr_start = "---> start"
fr_stop = "<--- stop"
fr_qstr = "qstr_info"
fr_mem = "mem_info"
fr_before = "before"
fr_after = "after"

# chose file with console dump to open
path_in = "bigPython/results/test_results.txt"
# path_in = "bigPython/results/g_var_6_results.txt"
file = open(path_in, 'r').read()
file = file.split(fr_sign + " ")

results = []
for element in file:
    if element.find(fr_start) != -1:
        head = (element.splitlines()[0]).split(", ")[1:]
        name, fun, when = head # maybe to dictionary? or class?

        data = element[element.find("\n")+1:]

        if fun == fr_qstr:
            data = qstr_val(data)
        elif fun == fr_mem:
            data = mem_val(data)
            # pass

        results.append([head, data])

        # analyze rest of data or pass just in string
    elif element.find(fr_stop) != -1:
        # check if frame stop is ending last data frame (head parameters are aqual)
        start_head = results[-1][0]
        head = (element.splitlines()[0]).split(", ")[1:]
        if head[0] == start_head[0] and head[1] == start_head[1]:
            pass
            # print(head[0], head[1], "fine")
        else:
            print(head[0], head[1], "problem!!!")
        # pass
        
del file
