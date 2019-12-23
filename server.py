import os
import subprocess
from xmlrpc.server import SimpleXMLRPCServer

def run_command(c):
    print("running command: " + c)
    subprocess.Popen(c, shell=True, stdout=subprocess.PIPE)
    #os.system(c)
    return ""

server = SimpleXMLRPCServer(("localhost", 4000), logRequests=False)
print("Listening on port 4000...")
server.register_function(run_command, "run_command")
server.serve_forever()
