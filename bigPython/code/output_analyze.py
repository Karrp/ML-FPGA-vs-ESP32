from analyze import qstr_val, mem_val, t_m_val, qstr_diff, mem_diff
import frame_naming as fr
import csv

# strings for frame (fr)
# d^-^b ["---> start"/"<--- stop"], <name>, <function>, ["before"/"after"]
# fr.fr_sign = "d^-^b" # start of the frame
# fr.fr_start = "---> start"
# fr.fr_stop = "<--- stop"
# fr.fr_qstr = "qstr_info"
# fr.fr_mem = "mem_info"
# fr.fr_t_m = "time_memory"
# fr.fr_before = "before"
# fr.fr_after = "after"
# fr.fr_effect = "effect"

# chose file with console dump to open
# path_in = "bigPython/results/test_results.txt"
path_in = "bigPython/results/g_var_33_results.txt"
file = open(path_in, 'r').read()

# where to save analyzed results
path_out = "bigPython/results/analysed_results.csv"

# split file by characteristic signs
    # d^-^b ["---> start"/"<--- stop"], <name>, <function>, ["before"/"after"]
    # example:
    # d^-^b ---> start, l_under_empty, mem_info, before
    # mem_info(True)
    # d^-^b <--- stop, l_under_empty, mem_info, before
    # calculations
    # d^-^b ---> start, l_under_empty, mem_info, after
    # mem info(True)
    # d^-^b <--- stop, l_under_empty, mem_info, after

file = file.split(fr.fr_sign + " ")

results = []
for element in file: # change REPL dump to measurements results data
    if element.find(fr.fr_start) != -1:
        head = (element.splitlines()[0]).split(", ")[1:]
        name, fun, moment = head # maybe to dictionary? or class?

        data = element[element.find("\n")+1:]

        if fun == fr.fr_qstr:
            data = qstr_val(data)
        elif fun == fr.fr_mem:
            data = mem_val(data)
        elif fun == fr.fr_t_m:
            data = t_m_val(data)
            # pass

        results.append([head, data])

        # analyze rest of data or pass just in string
    elif element.find(fr.fr_stop) != -1:
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

# analyze data to compress files size? - maybe later?

# divide by measurement type (qstr_info(), mem_info())
# make pairs before/after measurement

calculated = []

for i in range(0, len(results), 5):
    qstr_start = results[i]
    mem_start = results[i+1]
    mem_stop = results[i+2]
    qstr_stop = results[i+3]
    time_mem = results[i+4]

    qstr_effect = qstr_diff(qstr_stop, qstr_start)
    mem_effect = mem_diff(mem_stop, mem_start)

    calculated.append({"time_mem": time_mem, "qstr": qstr_effect, "memory": mem_effect})


### STRUCTURE OF ACTUAL STORED ###
# TODO convert lists to dictionaries or even classes

# head = [name_of_measurement, type_of_measurement, moment]

# time_mem: [
    # head
    # [ time<us>, memory<> ] # [int]*2
# ]

# qstr_info: [
    # head
    # [
        # [ n_pool, n_qstr, n_str_data_bytes, n_total_bytes ] # [int]*4
        # set(variable_names)
    # ]
# ]
# mem_info: [
    #  head
    # [
        # [ # [int]*10
            # stack<>, out_of<>,
            # GC: total<>, used<>, free<>, max_new_split<>,
            # No_of: 1-blocks, 2-blocks, max_block_size, max_free_size # one block is <> size
        # ]
        # memoy_layout_from: str # "3c170f00" for current compilation # can be changed to int
        # [changed_lines_numbers: int]
        # [changed_lines_after]
        # [changed_lines_before]
    # ]
# ]


# save results to output file
# optionally print results

# interesting parameters:
# name_of_measurement, time, memory, all_from_qstr, stack?, GC_used, memory_map

output = []
for measurement in calculated:
    measurement_name = measurement["time_mem"][0][0]

    simple_data = { # just integer values
        "time":             measurement["time_mem"][1][0],
        "memory":           measurement["time_mem"][1][1],
        "qstr_n_pool":              measurement["qstr"][1][0][0],
        "qstr_n_qstr":              measurement["qstr"][1][0][1],
        "qstr_n_str_data_bytes":    measurement["qstr"][1][0][2],
        "qstr_n_total_bytes":       measurement["qstr"][1][0][3], # should be the same as obove
        "stack":            measurement["memory"][1][0][0],
        "GC_used":          measurement["memory"][1][0][3]
    }

    complex_data = { # More advanced info to display
        "qstr_variables":       measurement["qstr"][1][1],
        "memory_map_lines":     measurement["memory"][1][2],
        "memory_map_after":     measurement["memory"][1][3],
        "memory_map_before":    measurement["memory"][1][4]
    }

    output.append({"name":measurement_name,
                   "simple_data": simple_data,
                   "complex_data": complex_data})

# print simple data in table and save as csv file
# for measurement in output:
#     print("\n" + measurement["name"] + ": ")
#     for x in measurement["simple_data"]:
#         print(x + ": ", measurement["simple_data"][x])

# save diffrences between empty(first) measurement as simple_data_delta
empty = output[0]["simple_data"]
for measurement in output:
    # print("\n" + measurement["name"] + ": ")
    simple_data_delta = {}
    for x in measurement["simple_data"]:
        simple_data_delta[x] = measurement["simple_data"][x] - empty[x]
        # print(x + ": ", simple_data_delta[x])
    measurement["simple_data_delta"] = simple_data_delta

# TODO save output as csv file
fields = ["name", "time","", "memory","", "n_pool","", "n_qstr","", "n_str_data_B","", "n_total_B","", "stack","", "GC_used",""]
second_row = ["", "us","diff", "b/B","diff", "no","diff", "no","diff", "bytes","diff", "bytes","diff", "b/B","diff", "b/B","diff"]
with open(path_out, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # parameter
    writer.writerow(fields)
    # diff or normal
    writer.writerow(second_row)
    # data
    for measurement in output:
        buffer = []
        buffer.append(measurement["name"])
        for el in measurement["simple_data"]:
            buffer.append(measurement["simple_data"][el])
            buffer.append(measurement["simple_data_delta"][el])
        writer.writerow(buffer)


# TODO print memory map difference
# maybe later compress whole changes into one line ? str.strip("_")

# TODO print memeory map legend

# what with variable names?


