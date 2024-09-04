# Variable name length
# https://forum.micropython.org/viewtopic.php?p=60153


# test variables:
# global / local
# variables / constants / _constants
# different variable names length


from measure import execute, execute_print

def test():

    exec(open("del_len.py").read()) # possibly check if running on restarted device

    path = "" # "performance/var_const/" # directory
    var_names = True
    heap_map = True

    # global / local variables
    glob = dict(name = "g", pre = "", post = "")
    loc = dict(name = "l", pre = "def test():\n\t", post = "" )#, post = "\ntest()")

    # variables / constants / constants with '_'
    var   = dict(name = "_var_"  , base = "a", expr = " = 1")
    const = dict(name = "_const_", base = "A", expr = " = const(1)")
    under = dict(name = "_under_", base = "_", expr = " = const(1)")

    # generating different variable names length mask
    # s = "xx23456789abcdef0123456789abcdef0"
    s = "xx234"
    length = len(s)

    name = [""]*length
    command = [""]*length


    # scope = [glob, loc]
    scope = [loc]
    # v_type = [var, const, under]
    v_type = [var]

    results = []

    # generate variables of each type and test them
    for sc in scope: # global / local
        for vt in v_type: # variable, constant, underscore

            name[0] = sc["name"] + vt["name"] + "empty"
            command[0] = sc["pre"] + "pass"

            for i in range(1, length):  # variable name length
                name[i] = sc["name"] + vt["name"] + str(i+1)
                command[i] = sc["pre"] + vt["base"] + sc["name"] + s[2:i+1] + vt["expr"] + sc["post"]

            print("\nname:\n", name)
            print("command:\n", command)

            # perform test and save results
            results.append( execute("", list(name), var_names, heap_map, list(command)) )
    
    # print results
    for el in results:
        execute_print(*el)


test()


# exec(open("performance/test_variables.py").read())