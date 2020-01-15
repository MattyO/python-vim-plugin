import os
import json
import time

import subprocess
import re
import time
import sys


COMMAND_DIRECTORY = os.path.join(os.path.dirname(__file__), 'commands')

if not os.path.exists(COMMAND_DIRECTORY):
    os.mkdir(COMMAND_DIRECTORY)

def is_buffered_line(start_str, buffered):
    return start_str.startswith(buffered) or re.match(start_str, buffered)

def run_command(c, directory=None):
    print("running command: " + c)
    print("in directory: " + directory)
    #"stdbuf -o0 " +
    p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=directory, bufsize=0, )
    d = ""
    data = ""
    current_line = ''
    lines = []
    longest_line = 0
    buffering_line = True
    buffered = ""


    while(p.poll() is None):
        character = p.stdout.read(1).decode("utf-8")
        data += character
        current_line += character
        if buffering_line:
            buffered += character

        if character == "\n":
            lines.append(current_line)
            if re.match("[-]+", current_line):
                longest_line = max([len(current_line), longest_line])
            current_line = ""
            buffering_line = False

        if not (is_buffered_line("OK", buffered) or is_buffered_line("FAILED", buffered)):
            buffering_line = False

        if not buffering_line and len(buffered) >= 1:
            buffered = re.sub("OK", "\033[42m\033[30m{}\033[00m".format("OK".ljust(longest_line)), buffered )
            buffered  = re.sub("FAILED(.*)\n", r"\033[41m\033[37m{}\1\033[00m\n".format("FAILED".ljust(longest_line)), buffered )
            sys.stdout.write(buffered)
            buffered = ""
        elif not buffering_line:
            sys.stdout.write(character)
        sys.stdout.flush()

        if character == "\n":
            buffering_line = True

        #longest_line = max([len(l) for l in data.encode("utf-8").split("\n") if re.match("[-]+", l)] + [0])
    the_rest = p.stdout.read().decode("utf-8")
    the_rest = re.sub("OK", "\033[42m\033[30m{}\033[00m".format("OK".ljust(longest_line)), the_rest )
    the_rest  = re.sub("FAILED(.*)\n", r"\033[41m\033[37m{}\1\033[00m\n".format("FAILED".ljust(longest_line)), the_rest )
    sys.stdout.write(the_rest)
    sys.stdout.flush()

    return ""

def run_commands_if_present():
    things = os.listdir(COMMAND_DIRECTORY)
    if len(things) > 0:
        for thing in things:
            command_file_path = COMMAND_DIRECTORY + '/' + thing
            with open(command_file_path) as f:
                command_info = json.loads(f.read())
                os.remove(command_file_path)
                run_command(command_info['command'], command_info['directory'])


def run_watcher_forever():
    print("watching directory...")
    while True:
        time.sleep(.5)
        run_commands_if_present()
