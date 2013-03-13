import argparse
import time
from storagejsonhandler import StorageJSONHandler,MultiThreadedHTTPServer
parser = argparse.ArgumentParser(description='Start the server.')
parser.add_argument('--port', type=int,default=8081,nargs='+',
                   help='port to bind to')
parser.add_argument('--host', type=str,default='0.0.0.0',nargs='+',
                   help='host to bind to')
"""
Was going to add support for appending values, turns out it's strange to initialize the replace parameter in there, would have to do it in the server.
I'll add it later.
parser.add_argument('replace', type=bool,default=True,
                   help='whether to replace values or not')
"""
args = parser.parse_args()
PORT_NUMBER = args.port
HOST_NAME = args.host

server_class = MultiThreadedHTTPServer
handler = StorageJSONHandler
httpd = server_class((HOST_NAME, PORT_NUMBER), handler)
print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)