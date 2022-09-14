import os
import json
import time

import subprocess
import re
import time
import sys
import re
import select

pass_text = '''

        ██████╗  █████╗ ███████╗███████╗
        ██╔══██╗██╔══██╗██╔════╝██╔════╝
        ██████╔╝███████║███████╗███████╗
        ██╔═══╝ ██╔══██║╚════██║╚════██║
        ██║     ██║  ██║███████║███████║
        ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
'''
fail_text = '''

        ███████╗ █████╗ ██╗██╗
        ██╔════╝██╔══██╗██║██║
        █████╗  ███████║██║██║
        ██╔══╝  ██╔══██║██║██║
        ██║     ██║  ██║██║███████╗
        ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝
'''

COMMAND_DIRECTORY = os.path.join(os.path.dirname(__file__), 'commands')

if not os.path.exists(COMMAND_DIRECTORY):
    os.mkdir(COMMAND_DIRECTORY)

def is_buffered_line(start_str, buffered):
    return start_str.startswith(buffered) or re.match(start_str, buffered)


def is_stuff_to_read(p):
    return bool(select.select([p.stdout, ], [], [], 0.0)[0])


def write_buffer(buffered):
    term_width = os.get_terminal_size().columns
    buffered = re.sub("OK", "\033[42m\033[30m{}\033[00m".format("OK".ljust(term_width)), buffered )
    buffered  = re.sub("FAILED(.*)\n", r"\033[41m\033[37m{}\1\033[00m\n".format("FAILED".ljust(term_width)), buffered )

    re_text = r'(?P<total_count>[\d]+) example[s]*, (?P<failure_count>[\d]+) failure[s]*'
    result = re.search(re_text, buffered)

    if result and int(result.group("failure_count")) > 0:
        total_match = result.group(0)
        buffered = re.sub(total_match, "\033[41m\033[37m{}\1\033[00m".format(total_match.ljust(term_width)), buffered)
    elif result and int(result.group("failure_count")) == 0:
        total_match = result.group(0)
        buffered = re.sub(total_match, "\033[42m\033[30m{}\033[00m".format(total_match.ljust(term_width)), buffered)

    sys.stdout.write(buffered)


def run_command(c, directory, conn):
    term_width = os.get_terminal_size().columns

    print("running command: " + c)
    print("in directory: " + directory)
    #"stdbuf -o0 " +
    temp_c = f"bash -l '{c}'"
    temp_c = ['bash', '-lc', c]
    p = subprocess.Popen(temp_c, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, cwd=directory, bufsize=0, )
    d = ""
    current_line = ''
    buffered = ""


    while(p.poll() is None):
        #stuff=sys.stdin.read()
        # stuff !='':
        #if stuff is not None and stuff != '':
        #sys.stdout.write(f"reading stdin: {stuff}")
        if(conn.poll()):
            write_buffer(buffered)
            buffered = ''
            stuff = conn.recv()
            p.stdin.write(stuff.encode('utf-8'))

        if(not is_stuff_to_read(p)):
            continue

        character = p.stdout.read(1).decode("utf-8")
        buffered += character

        if character == "\n":
            write_buffer(buffered)
            buffered = ""

        #if not (is_buffered_line("OK", buffered) or is_buffered_line("FAILED", buffered)):
        #    buffering_line = False

    sys.stdout.flush()
    the_rest = p.stdout.read().decode("utf-8")
    the_rest = re.sub("OK", "\033[42m\033[30m{}\033[00m".format("OK".ljust(term_width)), the_rest )
    the_rest  = re.sub("FAILED(.*)\n", r"\033[41m\033[37m{}\1\033[00m\n".format("FAILED".ljust(term_width)), the_rest )

    re_text = '(?P<total_count>[\d]+) example[s]*, (?P<failure_count>[\d]+) failure[s]*'
    result = re.search(re_text, the_rest)

    #stuff=conn.recv()
    #if stuff is not None and stuff != '':
    #sys.stdout.write(f"reading stdin: {stuff}")
    #sys.stdout.flush()


    if result and int(result.group("failure_count")) > 0:
        total_match = result.group(0)
        the_rest = re.sub(total_match, "\033[41m\033[37m{}\1\033[00m".format(total_match.ljust(term_width)), the_rest)
    sys.stdout.write(the_rest)
    sys.stdout.flush()

    if bool(p.returncode):
        sys.stdout.write("\033[41m\033[37m{}\1\033[00m".format(fail_text))
    else:
        sys.stdout.write("\033[42m\033[30m{}\033[00m".format(pass_text))
    sys.stdout.flush()

    return ""

def run_commands_if_present(conn):
    things = os.listdir(COMMAND_DIRECTORY)
    if len(things) > 0:
        for thing in things:
            command_file_path = COMMAND_DIRECTORY + '/' + thing
            with open(command_file_path) as f:
                command_info = json.loads(f.read())
                os.remove(command_file_path)
                run_command(command_info['command'], command_info['directory'], conn)


def run_watcher_forever(conn):
    print("watching directory...")
    while True:
        time.sleep(.5)
        run_commands_if_present(conn)
