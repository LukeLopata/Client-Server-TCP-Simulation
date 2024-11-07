import socket
import threading
import time



class Client:
    def __init__(self, socket, address):
        self.name = ""
        self.socket = socket
        self.address = address
        self.wantsweather = False
        self.wantsnews = False
        
PORTNUMBER = 1234
clients = []



def connectClient(socket, address):
    newclient = Client(socket, address)
    clients.append(newclient)
    
    return newclient


def handleClient(client):
    try:
        while True:
            print("waiting for client message")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("stopping server from client thread")
        server.close()
        exit()

        
    






print("Starting Server")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', PORTNUMBER))
server.listen()


try:
    running = True
    while (running):
        print("Waiting for connection")
        clientSocket, clientAddress = server.accept()
        print("Connection accepted")
        client = connectClient(clientSocket, clientAddress)
        
        thread = threading.Thread(target=handleClient, args=([client]))
        thread.start()
except KeyboardInterrupt:
    print()
    print("Closing server")
    server.close()
    exit()
    
    
    

    





