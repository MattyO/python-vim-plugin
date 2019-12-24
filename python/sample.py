import vim
import xmlrpc.client
import os.path
import re
import linecache

class Test:
    pass

def file_test_method_and_class(file_path, line_num):
    test_class = None
    test_method = None
    search_function = re.compile("def (test_\S*)\(.*\):")
    search_class = re.compile("class ([A-Z].*)\(.*TestCase.*\):")
    while line_num > 0 and (test_class is None or test_method is None):

        line = linecache.getline(file_path, line_num).strip()
        if line.startswith("def test_"):
            test_method = search_function.search(line).group(1)
        if line.startswith("class"):
            test_class = search_class.search(line).group(1)

        line_num  -=1
    return (test_class, test_method)

def test_command(num_string):
    if num_string == 'all':
        return "python -m unittest discover"

    test_command_string = "python -m unittest discover"
    full_file_path = vim.eval("expand('%:p')")
    file_parts = full_file_path.split("/")
    file_name = file_parts.pop()
    local_parts = []
    row, col = vim.current.window.cursor
    #current_line = vim.current.buffer[row-1]

    while len(file_parts)> 0:
        if(os.path.exists("/".join(file_parts + ['.git']))):
            break
        local_parts.append(file_parts.pop())

    print("/".join(local_parts))
    print(file_name)

    file_name_without_extension = re.sub('\.py$', '', file_name)
    if file_name.startswith("test"):
        test_class, test_method = file_test_method_and_class("/".join(local_parts + [file_name]), row)
        test_command_string = "python -m unittest " +  ".".join(local_parts + [file_name_without_extension] +[test_class, test_method])
    elif file_name.endswith(".py"):
        test_command_string = "python -m unittest " +  ".".join(['tests'] + local_parts + ["test_" + file_name_without_extension])

    print(test_command_string)

    return test_command_string

def  run_command(c):
    with xmlrpc.client.ServerProxy("http://localhost:4000/", allow_none=True) as proxy:
        print(c)
        proxy.run_command(c)
