import os
import subprocess
from xmlrpc.server import SimpleXMLRPCServer
import pty
import re

def run_command(c, directory=None):
    print("running command: " + c)
    print("in directory: " + directory)
    p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=directory)
    d = ""
    data = ""
    print("reading output")

    while(p.returncode is None):
        print(p.returncode)
        d = p.stdout.read(512).decode('utf-8')
        print('after first read')
        data += d
        if len(d) == 0:
            continue
        longest_line = max( len(l) for l in data.split("\n") if re.match("[-]+", l))
        d = re.sub("OK", "\033[42m\033[30m{}\033[00m".format("OK".ljust(longest_line)), d)
        d = re.sub("FAILED(.*)\n", r"\033[41m\033[37m{}\1\n\033[00m".format("FAILED".ljust(longest_line)), d)
        print(d)
        if d == '':
            print('done reading')
            break;
    return ""

server = SimpleXMLRPCServer(("localhost", 4000), logRequests=False)
print("Listening on port 4000...")
server.register_function(run_command, "run_command")
server.serve_forever()
