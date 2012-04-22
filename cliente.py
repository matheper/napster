# -*- coding:utf-8 -*-
import socket
import threading
import SocketServer
import os

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)

        """Trata mensagem recebida conforme tipo, é o lado servidor."""

        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    files = os.listdir(os.path.expanduser('~/Arquivos/CienciaDaComputacao/6.Semestre/Sistemas_Distribuidos/napster'))
    message={}
    message['type']= 'connectToServer'
    message['ip']=ip
    message['port']= port
    message['files']= files

    data = str(message)

    client(ip, 8004, data)

    server.serve_forever()
#    server.shutdown()
