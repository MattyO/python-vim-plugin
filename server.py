import os
import subprocess
from xmlrpc.server import SimpleXMLRPCServer
import pty
import re
import time
import sys
import uuid
import json


def run_command(c, directory=None):
    COMMAND_DIRECTORY = 'commands'

    if not os.path.exists(COMMAND_DIRECTORY):
        os.mkdir(COMMAND_DIRECTORY)


    new_command_file_name = str(uuid.uuid4())
    with open(COMMAND_DIRECTORY + '/' + new_command_file_name, 'w') as f:
        f.write(json.dumps({'command': c,'directory': directory}))

    #print("running command: " + c)
    #print("in directory: " + directory)
    ##"stdbuf -o0 " +
    #p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=directory, bufsize=0, )
    #d = ""
    #data = ""
    #current_line = ''
    #lines = []
    #longest_line = 0
    #buffering_line = True
    #buffered = ""


    #while(p.poll() is None):
    #    character = p.stdout.read(1).decode("utf-8")
    #    data += character
    #    current_line += character
    #    if buffering_line:
    #        buffered += character

    #    if character == "\n":
    #        lines.append(current_line)
    #        if re.match("[-]+", current_line):
    #            longest_line = max([len(current_line), longest_line])
    #        current_line = ""
    #        buffering_line = False

    #    if not (is_buffered_line("OK", buffered) or is_buffered_line("FAILED", buffered)):
    #        buffering_line = False

    #    if not buffering_line and len(buffered) >= 1:
    #        buffered = re.sub("OK", "\033[42m\033[30m{}\033[00m".format("OK".ljust(longest_line)), buffered )
    #        buffered  = re.sub("FAILED(.*)\n", r"\033[41m\033[37m{}\1\033[00m\n".format("FAILED".ljust(longest_line)), buffered )
    #        sys.stdout.write(buffered)
    #        buffered = ""
    #    elif not buffering_line:
    #        sys.stdout.write(character)
    #    sys.stdout.flush()

    #    if character == "\n":
    #        buffering_line = True

    #    #longest_line = max([len(l) for l in data.encode("utf-8").split("\n") if re.match("[-]+", l)] + [0])
    #the_rest = p.stdout.read().decode("utf-8")
    #the_rest = re.sub("OK", "\033[42m\033[30m{}\033[00m".format("OK".ljust(longest_line)), the_rest )
    #the_rest  = re.sub("FAILED(.*)\n", r"\033[41m\033[37m{}\1\033[00m\n".format("FAILED".ljust(longest_line)), the_rest )
    #sys.stdout.write(the_rest)
    #sys.stdout.flush()

    return ""

def run_server_forever():
    server = SimpleXMLRPCServer(("localhost", 4000), logRequests=False)
    print("Listening on port 4000...")
    server.register_function(run_command, "run_command")
    server.serve_forever()
