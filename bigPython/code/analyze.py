
def qstr_val(s:str) -> tuple[list[int], set[str]]:
    # s = b.decode() # to string
    variables_names = set(s.splitlines()[1:]) # save variables names
    s = s.splitlines()[0] # cut first line when qstr_info(True)
    # s = s.split(':')[1] # not needed

    values = s.split(', ')
    values[:] = [int(element.split('=')[1]) for element in values] # extract values and convert to int
    # example
        # qstr pool: n_pool=4, n_qstr=200, n_str_data_bytes=1712, n_total_bytes=3936
    
    return values, variables_names
