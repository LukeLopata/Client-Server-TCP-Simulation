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


def handleClient(client_socket, client_address):
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"[MESSAGE from {client_address}]: {message}")
            
    except Exception as e:
        print(f"ERROR {e}")
    finally:
        server.close()
        print(f"[INFO] Connection clsoed {client_address}")
        exit()

        


print("Starting Server")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reusing the port
server.bind(('localhost', PORTNUMBER))
server.listen()


try:
    running = True
    while (running):
        print("Waiting for connection")
        client_socket, client_address = server.accept()
        print("Connection accepted")
        client = connectClient(client_socket, client_address)
        
        thread = threading.Thread(target=handleClient, args=(client_socket, client_address))
        thread.daemon()
        thread.start()
except KeyboardInterrupt:
    print()
    print("Closing server")
    server.close()
    exit()
    
    
    

    





