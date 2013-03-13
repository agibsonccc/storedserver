import BaseHTTPServer
import simplejson as json
import time
import sys
import os
import logging
import threading
from basestorage import BaseStorage
import socket
import multiprocessing
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
import getpass
"""
Multi threaded http server with a stoppable flag
"""
class MultiThreadedHTTPServer(ThreadingMixIn,HTTPServer,object):

    def __init__(self,*args,**kwargs):
       self.data = BaseStorage()
       self.please_die = threading.Event()
       super(MultiThreadedHTTPServer,self).__init__(*args,**kwargs)

    def stop_server(self):
      print 'stopping'
      self.stop = True
      self.shutdown()

    def serve_forever (self):
        """
        Handle one request at a time until stopped.
        """
        print 'started server'
        self.stop = False
        
        while not self.stop:
           self.handle_request()
        print 'stopping 2'
"""
Request handler that stores values backed by BaseStorage
This in turn is an abstraction of a dictionary that allows appending of values
depending on a setting.
"""            
class StorageJSONHandler(BaseHTTPServer.BaseHTTPRequestHandler,object):
       

       def do_QUIT (self):
            """
            Send 200 OK response, and set server.stop to True.
            """
            self.send_response(200)
            self.end_headers()
            self.server.stop = True
            self.server.please_die.set()


       def do_GET(self):
           """Respond to a GET request."""
           
           self.send_response(200)
           content_type = ''
           if self.path == '/data.csv':
              content_type = 'text/csv'


           elif self.path == '/data.html':
               content_type = 'text/html'

           else:
                content_type = 'text/html'
           self.send_header("Content-Type", content_type )
           self.end_headers()
           output=''
           print 'content ' + content_type
           
           if content_type == 'text/html':
              output= output + ("<!doctype html><html><head><title>Title goes here.</title></head>")
              output= output + ("<body>")
              output = output + '<table>'
              for k,v in self.server.data.entries():
                     output = output +  "<tr><td>%s</td>" % (k)
                     if isinstance(v,basestring):
                         print 'basestring'
                         output = output  + '<td>' + str(v) + '</td>'

                     else:
                          for item in v:
                             output = output  + '<td>' + str(item) + '</td>'  

              output = output + '</tr>'
              output = output + "</table></body></html>"
            
           elif content_type == 'text/csv':
                 for k,v in self.server.data.entries():
                     output= output + k + ', ' 
                     if isinstance(v,basestring):
                             output = output + str(v) + ','
                     else:
                          for item in v:
                              output = output + str(item) + ','
                     output = output[0:-1]
                     output= output + (unicode('\n'))
           
           self.wfile.write(unicode(output))

       def do_POST(self):
           self.send_header("Content-Type","application/json")
           print 'data so far ' + ','.join(self.server.data.keys())
          
           self.wfile.write('{"status":"saved"}')
           varLen = int(self.headers['Content-Length'])
           postVars = unicode(self.rfile.read(varLen))

           data = json.loads( postVars )
           print 'adding data ' + postVars
           for k in data:
               self.server.data.add(k,data[k])

           self.send_response(200) 
           self.end_headers()
           self.wfile.write('{"status":"Sent"}')
  

