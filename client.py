import socket
import queue
import threading




CLIENTPORTNUMBER = 5678
SERVERPORTNUMBER = 1234

SUB_ACK = threading.Event()
PUB_EROR = threading.Event()
CONN_ACK = threading.Event()
DISC_ACK = threading.Event()
SUB_FAILED = threading.Event()



def recevie_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            print(f"[{message}]")
            if message == "CONN_ACK":
                CONN_ACK.set()
            elif message == "SUB_ACK":
                SUB_ACK.set()
            elif message == "ERROR: Subscription Failed - Subject Not Found":
                SUB_FAILED.set()
            elif message == "DISC_ACK":
                DISC_ACK.set()
            elif message == "ERROR: Not Subscribed" :
                PUB_EROR.set()
                print("tried to publish info to a topic we are not subscribed to")
            else:
                messages_in.put(message)
    except Exception as e:
        print(f"ERROR {e} in recevie_messages")
    finally:
        client.close()
        exit()
            
                
def send_messages():
    while True:
        try:
            message = messages_out.get() # blocks until there is a message in the Que
            client.send(message.encode())
        except:
            print("Error in sending messages")
            break

        
def subscribe(topic):
    SUB_ACK.clear()
    SUB_FAILED.clear()
    messages_out.put(f"{client_name}, SUB, {topic}\n")
    while not SUB_ACK.wait(timeout = 3) and not SUB_FAILED.wait(timeout = 3): # wait for acknoledgment message. 
        # if we timeout, send the message again
        print("subscribe request timeout, sending sub message again")
        messages_out.put(f"{client_name}, SUB, {topic}\n")
    if SUB_ACK.is_set():
        print(f"SUB to {topic} ACK'ed")
    else: 
        print(f"SUB to {topic} failed")

        
    
def publish(subject, message):
    messages_out.put(f"{client_name}, PUB, {subject}, {message}\n")
    
def disconnect():
    messages_out.put("DISC\n")
    while not DISC_ACK.wait(timeout = 3):
        print("DISC timeout, resending")
        messages_out.put("DISC\n")
    print("Succsefully disconnected")
    
def connect(client_name):
    #
    CONN_ACK.clear()
    messages_out.put(f"{client_name}, CONN\n")
    while not CONN_ACK.wait(timeout = 3):
        print("Connection not ACK'ed, trying again")
        messages_out.put(f"{client_name}, CONN\n")
        
    print("Client connected")

        

    



if __name__ == "__main__":
    messages_out = queue.Queue()
    messages_in = queue.Queue()
    # acknowledgments = queue.Queue()
    
    # get user info
    client_name = input("What is the name of this client?\n")
    # client_name = "Client Number 1"
    
    CLIENTPORTNUMBER = int(input("What is the client port number\n"))
    # CLIENTPORTNUMBER = 5678

    
    # setup socket
    print("Starting Client")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reusing the port
    
    client.connect(("localhost", SERVERPORTNUMBER))

    
    # start sending and reciveing threads
    recevie_thread = threading.Thread(target = recevie_messages, args=([client]))
    recevie_thread.daemon = True
    recevie_thread.start()
    
    send_thread = threading.Thread(target = send_messages, args=([]))
    send_thread.daemon = True
    send_thread.start()
    
    
    connect(client_name)
    running = True
    while running:
        
        action = input("What do you want to do. Options: sub, pub, disc\n")
        
        if action.lower() == "sub":
            topic = input("What topic do you want to subscribe to?\n")
            subscribe(topic.upper())        
        elif action.lower() == "pub":
            subject = input("What topic do you want to publish to?\n")
            message = input("What message would you like to send?\n")
            publish(subject, message)
        elif action.lower() == "disc":
            disconnect()      
        # elif action.lower() == "reconn":
        #     connect( client_name)

    
    
    

    # Close the connection
    client.close(SERVERPORTNUMBER, client_name)