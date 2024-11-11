import socket
import threading
import time



class Client:
    def __init__(self, socket, address):
        self.name = ""
        self.socket = socket
        self.address = address
        self.sub_weather = False
        self.sub_news = False
        
PORTNUMBER = 1234
clients = []



def connectClient(socket, address):
    newclient = Client(socket, address)
    clients.append(newclient)
    
    return newclient


def handleClient(client_socket, client_address):
    
    client = Client(client_socket, client_address)
    # handle connection message seperatly
    message = client.socket.recv(1024).decode()
    message = message.split(",")
    if message[1] != "CONN":
        print(f"First message is not a conn: {message}")
    client.name = message[0]
    

    try:
        # handle all messages 
        while True:
            message = client.socket.recv(1024).decode()
            if not message:
                break
            
            print(f"[MESSAGE from {client.address}]: {message}")
            message = message.split(",")
            message = [elem.strip() for elem in message] # strip all extra white space from the message
            
            if(message[0] == "DISC"):
                print("TODO disconnect")
            elif (message[0] != client.name):
                print("ERROR, name in message doesnt match name on file")
                print(f"On file: {client.name} Recieved: {message[0]}")
                
            elif (message[1] == "SUB"):
                client.socket.send("SUB_ACK".encode())
                if message[2].lower() == "news" :
                    client.sub_news = True
                    print(f"{client.name} succsefully subscribed to NEWS")
                elif message[2].lower()== "weather" :
                    client.sub_news = True
                    print(f"{client.name} succsefully subscribed to WEATHER")
                else:
                    print(f"{client.name} was not able to subscribe to {message[2]}")
            elif(message[1] == "PUB"):
                print("TODO handle publishing")
            else:
                print(f"ERROR: message tag {message[1]} unknown")
                
            
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
        thread.daemon = True
        thread.start()
except KeyboardInterrupt:
    print()
    print("Closing server")
    server.close()
    exit()
    
    
    

    





