import socket
import threading
import time
import queue


class Client:
    def __init__(self, socket, address):
        self.name = ""
        self.socket = socket
        self.address = address
        
        self.sub_weather = False   #TODO chnage this to a dictionary for extendability 
        self.sub_news = False
        self.offline = False    #for phase 2
        self.notifications = queue.Queue() # for reconnection 
        
PORTNUMBER = 1234
clients = []
clientlock = threading.Lock()
news = queue.Queue()
weather = queue.Queue()

all_news = []
all_weather = []




def handleClient(client_socket, client_address):
    
    client = Client(client_socket, client_address)
    
    with clientlock:
        clients.append(client)
    # handle connection message seperatly
    
    message = client.socket.recv(1024).decode()
    print(message)
    message = message.split(",")
    if message[1] and message[1].strip() != "CONN":
        print(f"ERROR: First message recieved is not a CONN: {message}")
    print(message)
    client.socket.send("CONN_ACK".encode())
    
    client.name = message[0]

    
    # phase 2, dump all of the notification que here

    try:
        while True:
            message = client.socket.recv(1024).decode()
            if not message:
                break
            
            print(f"[MESSAGE from {client.address}]: {message}")
            message = message.split(",")
            message = [elem.strip() for elem in message] # strip all extra white space from the message
            
            if(message[0] == "DISC"):
                client.socket.send("DISC_ACK".encode())
                break

                
            elif (message[0] != client.name):
                print("ERROR, name in message doesnt match name on file")
                print(f"On file: {client.name} Recieved: {message[0]}")
                
            elif (message[1] == "SUB"):
                if message[2].lower() == "news" :
                    client.sub_news = True
                    print(f"{client.name} succsefully subscribed to NEWS")
                    client.socket.send("SUB_ACK".encode())
                elif message[2].lower()== "weather" :
                    client.sub_weather = True
                    print(f"{client.name} succsefully subscribed to WEATHER")
                    client.socket.send("SUB_ACK".encode())
                else:
                    #print(f"{client.name} was not able to subscribe to {message[2]}")
                    client.socket.send("ERROR: Subscription Failed - Subject Not Found".encode())

            elif(message[1] == "PUB"):
                if message[2] == "news":
                    if client.sub_news:
                        news.put(message[3])   
                    else:
                        client.socket.send("ERROR: Not Subscribed".encode())
                elif message[2] == "weather":
                    if client.sub_weather:
                        weather.put(message[3])
                    else:
                        client.socket.send("ERROR: Not Subscribed".encode())
                else:
                    client.socket.send("ERROR: Subject Not Found".encode())
                    

            else:
                print(f"ERROR: message tag {message[1]} unknown")
                
            
    except Exception as e:
        print(f"ERROR {e}")
    finally:
        server.close()
        print(f"[INFO] Connection clsoed {client_address}")
        exit()

     
def weatherNotifier():
    while True:
        notification = weather.get() # this will block until there is something to grab
        with clientlock:
            for client in clients:
                if client.sub_weather:
                    if (client.offline):
                        print("PHASE 2 cleint is offline")
                    else:
                        print("sending message ")
                        client.socket.send(f"NOTICICATION, WEATHER, {notification}".encode())
        all_weather.append(notification)
            
                     
def newsNotifier():
    while True:
        notification = news.get() # this will block until there is something to grab
        with clientlock:
            for client in clients:
                if client.sub_news:
                    if (client.offline):
                        print("PHASE 2 cleint is offline")
                    else:
                        print("sending message ")
                        client.socket.send(f"NOTICICATION, NEWS, {notification}".encode())
        all_news.append(notification)
    
    
    
    
    
    


print("Starting Server")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reusing the port
server.bind(('localhost', PORTNUMBER))
server.listen()

#make notification thread   
news_notification_thread = threading.Thread(target=newsNotifier, args=())
news_notification_thread.daemon = True
news_notification_thread.start()

weather_notification_thread = threading.Thread(target=weatherNotifier, args=())
weather_notification_thread.daemon = True
weather_notification_thread.start()

try:
    running = True
    while (running):
        print("Waiting for connection")
        client_socket, client_address = server.accept()
        print("Connection accepted")
        
        thread = threading.Thread(target=handleClient, args=(client_socket, client_address))
        thread.daemon = True
        thread.start()
except KeyboardInterrupt:
    print()
    print("Closing server")
    server.close()
    exit()
    
    
    

    





