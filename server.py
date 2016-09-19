#  coding: utf-8 
import SocketServer

import os.path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    global head1
    global headtype
    global headlength
    global response
    global end1
    global end2
    
    head1 = "HTTP/1.1 "
    headtype = "Content-type: "
    headlength = "Content-Length: "
    response = {200: "200 OK ",
                302: "302 FOUND ",
                404: "404 NOT FOUND "}
    end1 = "\r\n"
    end2 = "\r\n\r\n"
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        request = self.data.split()
        requested_url = request[1]
        url = requested_url
        
        #print (url)
                
        if os.path.exists("www" + url) or os.path.isdir("www" + url):

            if url.endswith(".css"):
                f = open("www" + url, "rb")
                data = os.fstat(f.fileno())
                self.request.sendall(head1 + response[200] + end1)
                self.request.sendall(headtype + "text/css" + end1)
                self.request.sendall(headlength + str(data.st_size) + end2)
                self.request.sendall(f.read())
                f.close()

            elif url.endswith(".html"):
                f = open("www" + url, "rb")
                data = os.fstat(f.fileno())
                self.request.sendall(head1 + response[200] + end1)
                self.request.sendall(headtype + "text/html" + end1)
                self.request.sendall(headlength + str(data.st_size) + end2)
                self.request.sendall(f.read())
                f.close()
            
            elif url.endswith("/"):
                f = open("www" + url + "index.html", "rb")
                data = os.fstat(f.fileno())
                self.request.sendall(head1 + response[200] + end1)
                self.request.sendall(headtype + "text/html" + end1)
                self.request.sendall(headlength + str(data.st_size) + end2)
                self.request.sendall(f.read())

            elif not url.endswith("/"):
                self.request.sendall(head1 + response[302] + end1)
                self.request.sendall("Location: " + url + "/" + end2)

        else:
            self.request.sendall(head1 + response[404] + end1)
            self.request.sendall(headtype + "text/html" + end1)
            self.request.sendall("Error 404 Page Not Found")
            
        self.request.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
