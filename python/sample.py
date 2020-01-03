import vim
import xmlrpc.client
import os.path
import re
import linecache
import json
import sys

###COVERAGE###
def get_current_sign_ids():
    missing_lines = []
    abs_current_file = "/".join(project_directory_parts())
    sign_text = vim.command("sign place file=" + abs_current_file)
    
    results = re.finditer("^\s*line=(\w*)\s*id=(\w*)\s*name=(\w*)\s*$", sign_text,)
    return [ m.group(1) for m in results]

def create_sign():
#❌
#∅
#⊝
#❎
    vim.command('sign define CoverageCross text=❌ texthl=Coverage')

def signs_defined_text():
    return vim.command("sign list")

def is_sign_defined():
    sign_definition = "sign CoverageCross  text=❌ texthl=Coverage"
    return sign_definition in signs_defined_text()

def is_file_in_project_directory(file_path):
    abs_dir_list, local_dir_list, file_name = project_directory_parts()
    full_file_path = "/".join(abs_dir_list + file_path.split("/"))
    return (os.path.exists(full_file_path), full_file_path)

def get_sign_lines():
    missing_lines = []
    abs_dir_list, local_dir_list, file_name = project_directory_parts()
    coverage_location = "/".join(abs_dir_list + ['coverage.json'])
    if not os.path.exists(coverage_location):
        return ""

    report_key = "/".join(local_dir_list+[file_name])
    with open(coverage_location) as f:
        report = json.loads(f.read())
        missing_lines = report['files'].get(report_key, {'missing_lines': []})['missing_lines']

    return missing_lines


def create_signs_in_file(line_nums):
    abs_current_file = current_full_file_path()
    for i, line_num in enumerate(line_nums):
        c = "sign place {} line={} name=CoverageCross file={}".format( 
                8000 + i,
                line_num,
                abs_current_file)

        vim.command(c)

def file_test_method_and_class(file_path, line_num):
    test_class = None
    test_method = None
    search_function = re.compile("def (test_\S*)\(.*\):")
    search_class = re.compile("class ([A-Z].*)\(.*TestCase.*\):")

    linecache.checkcache(file_path)
    first_line = linecache.getline(file_path, line_num).strip()
    if first_line.startswith("class"):
        return (search_class.search(first_line ).group(1), None)

    while line_num > 0 and (test_class is None or test_method is None):

        line = linecache.getline(file_path, line_num).strip()
        if line.startswith("def test_"):
            test_method = search_function.search(line).group(1)
        if line.startswith("class"):
            test_class = search_class.search(line).group(1)

        line_num  -=1
    return (test_class, test_method)

def current_full_file_path():
    return vim.eval("expand('%:p')")

def project_directory_parts():
    full_file_path = current_full_file_path() 
    file_parts = full_file_path.split("/")
    file_name = file_parts.pop()
    local_parts = []
    row, col = vim.current.window.cursor

    while len(file_parts)> 0:
        if(os.path.exists("/".join(file_parts + ['.git']))):
            break
        local_parts.insert(0, file_parts.pop())
    return (file_parts, local_parts, file_name)

def test_command(num_string):
    abs_dir_list, local_dir_list, file_name = project_directory_parts()
    python_exe = "/".join(abs_dir_list + ['env', 'bin', 'python'])
    is_dockerfile_in_directory, dockerfile_path = is_file_in_project_directory("Dockerfile")
    de = 'docker exec -ti'

    if is_dockerfile_in_directory:
        python_exe = de + " {} /venv/bin/python".format(abs_dir_list[-1])

    if num_string == 'all':
        return python_exe + " -m unittest discover"

    test_command_string = python_exe + " -m unittest discover"

    row, col = vim.current.window.cursor
    #current_line = vim.current.buffer[row-1]

    file_name_without_extension = re.sub('\.py$', '', file_name)
    if file_name.startswith("test"):
        test_class, test_method = file_test_method_and_class("/".join(local_dir_list+ [file_name]), row)
        test_parts = local_dir_list + [file_name_without_extension] +[test_class, test_method]
        test_parts = filter(lambda p: p is not None, test_parts )

        test_command_string = python_exe + " -m unittest " +  ".".join(test_parts)

    elif file_name.endswith(".py"):
        test_command_string = python_exe +" -m unittest " +  ".".join(['tests'] + local_dir_list  + ["test_" + file_name_without_extension])

    return test_command_string

def  run_command(c, directory=None ):
    abs_parts, local_parts, file_name=project_directory_parts() 
    with xmlrpc.client.ServerProxy("http://localhost:4000/", allow_none=True) as proxy:
        proxy.run_command(c, "/".join(abs_parts) )
