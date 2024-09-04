from measure import execute, execute_print

result = execute("", ["test"], True, True, ["a = 10"])

execute_print(*result)