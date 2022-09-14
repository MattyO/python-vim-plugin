import signal
import sys
import multiprocessing
import time
import select

import directory_runner
import server

processes = []
should_be_running = True

def handle_signal(signum, frame):
    global should_be_running
    should_be_running = False

signal.signal(signal.SIGINT, handle_signal)

parent_conn, child_conn = multiprocessing.Pipe()

processes.append(multiprocessing.Process(target=directory_runner.run_watcher_forever, args=(child_conn,)))
processes.append(multiprocessing.Process(target=server.run_server_forever))

print('starting everything')
for process in processes:
    process.start()

def is_stuff_to_read():
    return bool(select.select([sys.stdin, ], [], [], 0.0)[0])

while should_be_running:
    time.sleep(1)
    if(is_stuff_to_read()):
        while(is_stuff_to_read()):
            parent_conn.send(sys.stdin.readline())
            print("stuff to read")
    #i = sys.stdin.read()
    #if i != '':
    #    print("Found stuff")
    #    print(i)
    #    parent_conn.send(i)


#print("exiting...")
#for i in range(1,10):
#    time.sleep(.5)
#    print(select.select([sys.stdin, ], [], [], 0.0)[0])
#print('done reading lines')

for process in processes:
    process.terminate()
