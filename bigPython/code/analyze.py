
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
    if mem_map: # mem_info(True) not mem_info()
        start = mem_map[0].split(" ")[-1].replace(":", "")
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

    return values, start, structure # , address # addres can be calculated from index

