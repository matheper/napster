# -*- coding:utf-8 -*-
import socket
import threading
import SocketServer
import os

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def processMessage(self, message):
        """Process the message according to the type."""
        data = eval(message)
        messageType = data['type']
        if messageType == 3:#file transfer
            filename = data['filename']
            print 'Sending file %s.'%(filename)
            File = open(directory+'/'+filename,'rb')
            for i in File.readlines():
                self.request.sendall(i)
            File.close()
            print 'Sent successfully.'
            print outputMessage

    def handle(self):
        message = self.request.recv(1024)
        self.processMessage(message)
        cur_thread = threading.current_thread()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def recvFile(ip,port,message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,port))
    filename = message['filename']
    try:
        print "Receiving %s"%(filename)
        data = str(message)
        sock.send(data)
        File = open(directory+'/'+filename,'wb')
        while 1:
            data=sock.recv(1024)
            if not data:
                break
            File.write(data)
        File.close()
        return "Received Successfully."
    finally:
        sock.close()

def sendMessage(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        return response
    finally:
        sock.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    directory = raw_input("Enter the directory to share files: ")

    files = os.listdir(os.path.expanduser(directory))
    message={}
    message['type']= 0 #connect server
    message['ip']=ip
    message['port']= port
    message['files']= files
    data = str(message)
    sendMessage(ip, 8004, data)

    outputMessage = "Enter:\n1:Search\n0:Exit\n"
    userOpt = raw_input(outputMessage)

    while userOpt != '0':
        filename = raw_input("Enter the file name: ");
        message={}
        message['type']=2 #file search
        message['ip']=ip
        message['port']=port
        message['filename']=filename

        data = str(message)
        response = eval(sendMessage(ip,8004,data))
        if response:
            index = 1;
            for opt in response:
                print "id: %s, local: %s"%(index,opt)
                index += 1
            print "0: Cancel"
            index = int(raw_input("Enter the id you choose: "))
            if index != '0':
                serv = response[index-1]
                message = {}
                message['type']=3 #file transfer
                message['filename']=filename
                response = recvFile(serv[0],serv[1],message)
                print response
        else:
            print "File not found."
        
        userOpt = raw_input(outputMessage)

    message = {}
    message['type']= 1 #disconnect server
    message['ip']= ip
    message['port']= port
    data = str(message)
    sendMessage(ip, 8004, data)

    server.shutdown()
