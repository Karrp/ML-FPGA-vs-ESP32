import frame_naming as fr

def qstr_val(s:str) -> tuple[list[int], set[str]]:
    # s = b.decode() # to string
    variables_names = set((s.replace(")\n", "")).split("Q(")[1:]) # save variables names
    s = s.splitlines()[0] # cut first line when qstr_info(True)
    # s = s.split(':')[1] # not needed

    values = s.split(', ')
    values[:] = [int(element.split('=')[1]) for element in values] # extract values and convert to int
    # example
        # qstr pool: n_pool=4, n_qstr=200, n_str_data_bytes=1712, n_total_bytes=3936
    
    return values, variables_names

def mem_val(s:str):
    mem_map = s.splitlines()[3:] # save memory map
    s = s.splitlines()[:3] # cut first line when qstr_info(True)

    # stack: 976 out of 15360
    buf = s[0].split(" ")
    values = [int(buf[1]) ,int(buf[4])]
    # GC: total: 64000, used: 7344, free: 56656, max new split: 8257536
    buf = s[1].replace(",", "")
    buf = buf.split(": ")[2:]
    buf[:] = [int(e.split(' ')[0]) for e in buf]
    values = values + buf
    #  No. of 1-blocks: 62, 2-blocks: 11, max blk sz: 150, max free sz: 3061
    buf = s[2].replace(",", "")
    buf = buf.split(": ")[1:]
    buf[:] = [int(e.split(' ')[0]) for e in buf]
    values = values + buf

    # GC memory layout; from 3c170f00:
    # 00000000: h=hLhhhAMMBDDhTh=Mhh=================hh=======h=======h=hAh=Shhh
    # 00000400: hTBBB=SShShhhShhShDShh=BBhSBBBShB=SB=hh==ShSh===============DBBh
    # 00000800: SBh==Sh=======h==========h===========h====hShSSh=h=hh===h===ShSh
    # 00000c00: Sh==h==hSShShShShhh======h==========SLhSh=hhSh=h==h==========h==
    # 00001000: ==hSh====hLLh=hhLhSh=Sh====SDhhh====hLhh=hhhhB..h.......h..h=...
    # 00001400: ................................................................
    # 00001800: h==============.................................................
    # 00001c00: ..........h=======h==================h==========================
    # 00002000: ================================================================
    # 00002400: ===========================================================.....
    #     (3 lines all free)
    # 00003400: ...................................................h............

    structure = []
    start_from = ""
    if mem_map: # mem_info(True) not mem_info()
        start_from = mem_map[0].split(" ")[-1].replace(":", "")
        # address = []
        
        empty_line = "." * 64
        for line in mem_map[1:]:
            if line[0] != " ":
                buf = line.split(": ")
                # address.append(buf[0]) # int(buf[0], 16)) # from HEX to DEC
                structure.append(buf[1])
            else:
                free_lines = int(((line.lstrip()).split(" ")[0])[1:])
                for _ in range(free_lines):
                    # address.append()
                    structure.append(empty_line)

    return values, start_from, structure # , address # addres can be calculated from index


def t_m_val(s:str) -> list[int]:
    # Element:        Time_us:     Mem:
    # name:               773,     128
    # l = s.split()
    return [int(e) for e in s.split()] # extract values and convert to int


def head_diff(h_after, h_before, fun_type):
    # check if in right places
    head = []
    if h_before[0] == h_after[0]:
        head.append(h_before[0])
    else:
        print("not the same item compared!!!")

    if h_before[1] == h_after[1] == fun_type:
        head.append(h_before[1])
    else:
        print("not the same test type compared!!!")

    if (h_before[2] == fr.fr_before) and (h_after[2] == fr.fr_after):
        head.append(fr.fr_effect)
    else:
        print("wrong order!!!")
    
    return head


def val_diff(val_after, val_before):
    # int values difference
    values = []
    if len(val_after) == len(val_before):
        for i in range(len(val_before)):
            values.append(val_after[i] - val_before[i])
    else:
        print("different number of variables")

    return values


def qstr_diff(after, before):
    head = head_diff(after[0], before[0], fr.fr_qstr)

    values = val_diff(after[1][0], before[1][0])
    
    # sets difference
    variables_names = after[1][1] - before[1][1]

    data = [values, variables_names]

    # return difference
    effect = [head, data]
    return effect


def mem_line_diff(after:str, before:str) -> tuple[str, str]:
    diff = ""
    overwritten = ""
    changed = False
    for i in range (len(after)):
        if after[i] == before[i]: # the same
            diff += '_'
            overwritten += '_'
        else:
            diff += after[i] # save difference

            if before[i] != '.': # if wasn't empty
                changed = True
                overwritten += before[i]
            else:
                overwritten += '-'
    
    if not changed:
        overwritten = ""

    
    return diff, overwritten

def line_number_to_string(line_number:int) -> str:
    return (line_number*1024).to_bytes(4, byteorder='big').hex()

def mem_diff(after, before, show_diff=False):
    head = head_diff(after[0], before[0], fr.fr_mem)

    values = val_diff(after[1][0], before[1][0])

    # check memory layout from
    if before[1][1] != after[1][1]:
        memoy_layout_from = "Error"
        print("differen memory start address!")
    else:
        memoy_layout_from = before[1][1]

    map_before = before[1][2]
    map_after = after[1][2]

    # always whole memory is mapped so lines number is equal
    additional_lines = [] # if one map has more lines
    if len(map_after) > len(map_before):
        additional_lines = after[1][1] [ len(map_before) : ]
    elif len(map_after) < len(map_before):
        additional_lines = map_before [ len(map_after) : ]

    # find different memory lines
    mem_map = []
    line_number = []
    mem_map_before = []
    for i in range(min(len(map_after), len(map_before))):
        if map_after[i] != map_before[i]:
            mem_map.append(map_after[i])
            line_number.append(i)
            mem_map_before.append(map_before[i])


    if additional_lines: # always whole memory is mapped so lines number is equal
        mem_map += additional_lines

    # --- printing difference ---
    if show_diff:
        print()
        for i, element in enumerate(mem_map_before):
            line = (line_number_to_string(line_number[i]))
            # print(element)
            # print(mem_map[i])
            difference, overwritten = mem_line_diff(mem_map[i], element)
            print("{}:".format(line), difference)
            if overwritten:
                print("---||---:", overwritten)


        if additional_lines: # always whole memory is mapped so lines number is equal
            print("additional lines:")
            for i, element in enumerate(additional_lines):
                line = (line_number_to_string(i + min(len(map_after), len(map_before))))
                print("{}:".format(line), element)
    # --- printing difference end ---

    data = [values, memoy_layout_from, line_number, mem_map, mem_map_before]

    # return difference
    effect = [head, data]
    return effect
