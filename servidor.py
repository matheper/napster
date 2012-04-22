# -*- coding:utf-8 -*-
import socket
import threading
import SocketServer
import os

clientsList = {}

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        data = eval(data)
        """Trata mensagem recebida conforme tipo, é o lado servidor."""

        cur_thread = threading.current_thread()
#        response = "{}: {}".format(cur_thread.name, data)
#        self.request.sendall(response)
        
#        message = data.split('\n')
#        port = int(message[0])
#        clientsList[port] = message[1].split(' ')
#        print clientsList
        print data

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 8004

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    server.serve_forever()
