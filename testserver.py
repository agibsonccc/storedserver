import unittest
from storedserver.storagejsonhandler import MultiThreadedHTTPServer,StorageJSONHandler
import threading
import urllib2
import simplejson as json
from storedserver.basestorage import BaseStorage
from multiprocessing import Process
import time
import sys
import os
import httplib
from StringIO import StringIO
from httplib import HTTPResponse

class FakeSocket(StringIO):
    def makefile(self, *args, **kw):
        return self
"""
NOTE DOES NOT STOP, need to send kill signal.
Unsure of what to do with stopping the background server
"""
class TestReplaceCase(unittest.TestCase):
      
       @classmethod
       def start_server (cls,handler):
           """Start an HTTP server thread and return its port number."""
           handler.protocol_version = "HTTP/1.0"
           port = cls.httpd.server_port
           t = threading.Thread(target=cls.httpd.serve_forever)
           t.start()
           # wait for server to start up
           while True:
              try:
                   conn = httplib.HTTPConnection("localhost:%d" % cls.port)
                   print 'attempting on  ' + str(cls.port)
                   conn.request("GET", "/data.csv")
                   conn.getresponse()
                   break
              except:
                   print 'waiting...'
                   print "Unexpected error:", sys.exc_info()[0]
                   time.sleep(0.5)
       @classmethod
       def httpparse(cls,fp):
          socket = FakeSocket(fp.read())
          response = HTTPResponse(socket)
          response.begin()

          return response
       

       @classmethod
       def setUpClass(cls):
            """Call before every test case."""
            
            print "setting up httpd"
            cls.handler = StorageJSONHandler
            cls.host = '0.0.0.0'
            cls.port = 8081
            cls.httpd = MultiThreadedHTTPServer((cls.host, cls.port), cls.handler)
            
            print 'created server...'
            cls.start_server(cls.handler)
            cls.headers = {'Content-Type':'application/json'}
            cls.base_url = 'http://localhost:' + str(cls.port)
       
       @classmethod
       def stop_server (cls):
         """Stop an HTTP server thread."""
         conn = httplib.HTTPConnection("localhost:%d" % cls.port)
         conn.request("QUIT", "/")
         print 'about quit' 
         conn.getresponse()
         print 'called quit' 
          
       @classmethod
       def tearDownClass(cls):
          """Call after every test case."""
          cls.stop_server()
          print 'stopped server'



          
       def test_html(self):
           print 'test html'
           #add to storage
           self.send_post()
           opener = urllib2.build_opener(urllib2.HTTPHandler)
           request = urllib2.Request(TestReplaceCase.base_url + '/data.html')
           url = opener.open(request)
           self.assertEquals('<!doctype html><html><head><title>Title goes here.</title></head><body><table><tr><td>data</td><td>val</td></tr></table></body></html>',url.read())
           
           
       def send_post(self):
           data = {'data':'val'}
           send = json.dumps( data )
           opener = urllib2.build_opener(urllib2.HTTPHandler)
           request = urllib2.Request(TestReplaceCase.base_url,data=send)
           request.add_header('Content-Type', 'application/json')
           request.get_method = lambda: 'POST'
           

           url = opener.open(request)
           
           resp =  TestReplaceCase.strip_http_headers(url.read())
           respdata = json.loads( resp )
           self.assertEquals('Sent',respdata['status'])

           


       def test_csv_values(self):
           print 'test csv'
           #add to the storage
           self.send_post()
           opener = urllib2.build_opener(urllib2.HTTPHandler)
           request = urllib2.Request(TestReplaceCase.base_url + '/data.csv')
           url = opener.open(request)
           self.assertEquals('data, val\n',url.read())



       

if __name__ == '__main__':
     unittest.main()
