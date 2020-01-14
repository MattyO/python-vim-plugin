import signal
import sys
import multiprocessing
import time

import directory_runner
import server

processes = []
should_be_running = True

def handle_signal(signum, frame):
    global should_be_running
    should_be_running = False

signal.signal(signal.SIGINT, handle_signal)

processes.append(multiprocessing.Process(target=directory_runner.run_watcher_forever))
processes.append(multiprocessing.Process(target=server.run_server_forever))
for process in processes:
    process.start()

while should_be_running:
    time.sleep(1)

for process in processes:
    process.terminate()
