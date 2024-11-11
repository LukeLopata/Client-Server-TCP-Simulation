import socket
import queue
import threading




CLIENTPORTNUMBER = 5678
SERVERPORTNUMBER = 1234

SUB_ACK = threading.Event()
PUB_EROR = threading.Event()
CONN_ACK = threading.Event()
DISC_ACK = threading.Event()



def recevie_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message == "CONN_ACK":
                CONN_ACK.set()
            elif message == "SUB_ACK":
                SUB_ACK.set()
            elif message == "DISC_ACK":
                DISC_ACK.set()
            elif message == "ERROR: Not Subscribed":
                PUB_EROR.set()
                print("tried to publish info to a topic we are not subscribed to")
            else:
                print("MESSAGE recived: ", message)
                messages_in.put(message)
    except Exception as e:
        print(f"ERROR {e} in recevie_messages")
    finally:
        client.close()
        exit()
            
                
def send_messages(client_socket):
    while True:
        try:
            message = messages_out.get() # blocks until there is a message in the Que
            client.send(message.encode())
        except:
            print("Error in sending messages")
            break

        
def subscribe(topic):
    SUB_ACK.clear()
    messages_out.put(f"{client_name}, SUB, {topic}\n")
    while not SUB_ACK.wait(timeout = 3): # wait for acknoledgment message. 
        # if we timeout, send the message again
        print("subscribe message ACK timeout, sending sub message again")
        messages_out.put(f"{client_name}, SUB, {topic}\n")
    print(f"SUB to {subject} ACK'ed")

        
    
def publish(subject, message):
    messages_out.put(f"{client_name}, PUB, {subject}, {message}\n")
    

    





if __name__ == "__main__":
    messages_out = queue.Queue()
    messages_in = queue.Queue()
    # acknowledgments = queue.Queue()
    
    # get user info
    # client_name = input("What is the name of this client?")
    client_name = "Client Number 1"
    
    #publisher = input("Are you a publisher [Y/N]") 
    publisher = "y"
    publisher = (publisher.lower() == "y" or publisher.lower() == "yes")
    
    # connect and send connection message
    print("Starting Client")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reusing the port
    client.connect(("localhost", SERVERPORTNUMBER))
    print("Client connected")
    messages_out.put(f"{client_name}, CONN\n")
        
    # start sending and reciveing threads
    recevie_thread = threading.Thread(target = recevie_messages, args=([client]))
    recevie_thread.daemon = True
    recevie_thread.start()
    
    send_thread = threading.Thread(target = send_messages, args=([client]))
    send_thread.daemon = True
    send_thread.start()
    
    running = True
    while running:
        
        action = input("What do you want to do. Options: sub, pub, disc")
        
        if action.lower() == "sub":
            topic = input("What topic do you want to subscribe to?")
            subscribe(topic.upper())        
        elif action.lower() == "pub":
            subject = input("What topic do you want to publish to?")
            message = input("What messaeg would you like to send?")
            publish(subject, message)
        elif action.lower() == "disc":
            messages_out.put("DISC\n")
    
    
    

    # Close the connection
    client.close()