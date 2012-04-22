# -*- coding:utf-8 -*-
import socket
import threading
import SocketServer
import os

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

#    def sendFile():
#        music=open(fileName,'rb')
#
#        print "enviado %s"%(fileName)
#        for i in music.readlines():
#            self.tcp.send(i)
#
#        music.close()
#
#    def recvFile():
#        fileName = connection.recv(1024)
#        print "Recebendo %s"%(fileName)
#        music = open(fileName+"receved.mp3",'wb')
#        while 1:
#            data=connection.recv(1024)
#            if not data:
#                break
#            music.write(data)
#        music.close()

    def processMessage(self, message):
        """Process the message according to the type."""
        data = eval(message)
        messageType = data['type']
        if messageType == 3:#file transfer
            filename = data['filename']
            print 'Enviando arquivo %s.'%(filename)
            File = open(directory+'/'+filename,'rb')
            for i in File.readlines():
                self.request.sendall(i)
            File.close()
            print 'Enviado com sucesso.'
#            self.request.sendall('teste')

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
        print "Recebendo %s"%(filename)
        data = str(message)
        sock.send(data)
        File = open(directory+'/'+filename,'wb')
        while 1:
            data=sock.recv(1024)
            if not data:
                break
            File.write(data)
        File.close()
        return "Arquivo Recebido com sucesso."
    finally:
        print "aqui"
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

    directory = raw_input("Digite o diretório para compartilhar arquivos: ")

    outputMessage = "Digite:\n1:Conectar ao Servidor\n"
    outputMessage += "2:Consultar\n3:Teste\n"
    outputMessage += "50:Desconectar do Servidor\n0:Sair\n"
    userOpt = int(raw_input(outputMessage))

    while userOpt:
        if userOpt == 1:
            files = os.listdir(os.path.expanduser(directory))
            message={}
            message['type']= 0 #connect server
            message['ip']=ip
            message['port']= port
            message['files']= files

            data = str(message)

            sendMessage(ip, 8004, data)

        elif userOpt == 50:
            message = {}
            message['type']= 1 #disconnect server
            message['ip']= ip
            message['port']= port

            data = str(message)
            sendMessage(ip, 8004, data)

        if userOpt == 2:
            filename = raw_input("Digite o nome do arquivo: ");
            message={}
            message['type']=2 #file search
            message['ip']=ip
            message['port']=port
            message['filename']=filename

            data = str(message)
            response = eval(sendMessage(ip,8004,data))
            if not response:
                print "Arquivo não encontrado."
            else:
                index = 1;
                for opt in response:
                    print "id: %s, local: %s"%(index,opt)
                    index += 1
                index = int(raw_input("Digite o id do arquivo escolhido:"))

                serv = response[index-1]

                message = {}
                message['type']=3 #file transfer
                message['filename']=filename
                
                response = recvFile(serv[0],serv[1],message)

                print response

        userOpt = int(raw_input(outputMessage))

    server.shutdown()
