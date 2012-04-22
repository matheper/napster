# -*- coding:utf-8 -*-
import socket
import threading
import SocketServer
import os
import time

clientsList = {}

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def processMessage(self, message):
        """Process the message according to the type."""
        data = eval(message)
        messageType = data['type']
        if messageType == 0:#connect
            clientsList[(data['ip'],data['port'])]=(data['files'])
            print clientsList
            print "Added client %s port %s"%(data['ip'],data['port'])
        elif messageType == 1:#disconnect
            clientsList.pop((data['ip'],data['port']))
            print "Removed client %s port %s"%(data['ip'],data['port'])
        elif messageType == 2:#search
            filename = data['filename']
            response = []
            for client in clientsList:
                print "filename: %s"%(filename)
                print "listFiles: %s"%(clientsList[client])
                if filename in clientsList[client]:
                    response.append(client)
                    print 'Igual'
            response = str(response)
            self.request.sendall(response)


    def handle(self):
        message = self.request.recv(1024)
        self.processMessage(message)
        data = eval(message)

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
    
    while True:
        time.sleep(2)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client = ()
            for i in clientsList:
                client = i
                sock.connect(client)
                message = {}
                message['type'] = 4 #teste conexao
                data = str(message)
                sock.sendall(data)
                print client
        except:
            clientsList.pop(i)
            print 'Cliente %s desconectado por estar off line.'%(i[0])
        finally:
            sock.close()
