import socket
import queue
import threading
import time


SERVERPORTNUMBER = 1234

SUB_ACK = threading.Event()
PUB_EROR = threading.Event()
CONN_ACK = threading.Event()
DISC_ACK = threading.Event()
SUB_FAILED = threading.Event()
END_SENDER = threading.Event()

def recevie_messages(client_socket):
    try:
        while True:
            time.sleep(0.1)
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
                END_SENDER.set()
                messages_out.put("") # put an empty/dummy message in the out Que to make ure the thread closes
                break   # break to the finally of the try block to handle ending this thread
            elif message == "ERROR: Not Subscribed" :
                PUB_EROR.set()
                print("tried to publish info to a topic we are not subscribed to")
            # else:   # put messages that are not ACK in a queue to be stored/processed if we want more than just printing them
            #     messages_in.put(message)
    except Exception as e:
        print(f"ERROR {e} in recevie_messages")
    finally:
        print("Ending receive_message thread")
        
            
                
def send_messages(current_client):
    print("in send message")
    END_SENDER.clear()
    while True:
        try:
            message = messages_out.get() # waits for message in Que. Only blocks for 1 second
            if END_SENDER.is_set():
                break  
            current_client.send(message.encode())
            
        except Exception as e:
            print(f"ERROR {e} in send_messages")
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

def connect(client_name, first_connection = False):
    
    try:
        print("Starting Client")    
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reusing the port
        client.connect(("localhost", SERVERPORTNUMBER))

        # start sending and reciveing threads
        recevie_thread = threading.Thread(target = recevie_messages, args=([client]))
        recevie_thread.daemon = True
        recevie_thread.start()
        
        send_thread = threading.Thread(target = send_messages, args=([client]))
        send_thread.daemon = True
        send_thread.start()
        
        CONN_ACK.clear()
        if first_connection:
            connection_message = f"{client_name}, CONN\n"
        else:
            connection_message = f"RECONNECT, {client_name}\n"

        messages_out.put(connection_message)
        while not CONN_ACK.wait(timeout = 3):
            print("Connection not ACK'ed, trying again")
            messages_out.put(connection_message)
        firstconnection = False
            
        print("Client connected")
        return True
    except Exception as e:
        print(f"Failed to connect with Error {e}")
        return False

if __name__ == "__main__":
    messages_out = queue.Queue()
    messages_in = queue.Queue()
    
    # get user info
    # lient_name = input("What is the name of this client?\n")
    client_name = "Client Number 1"
    
    # CLIENTPORTNUMBER = int(input("What is the client port number\n"))
    CLIENTPORTNUMBER = 5678


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    

    connect(client_name, first_connection=True)
    connected = True
    while True:
        if (connected):
            action = input("What do you want to do. Options: sub, pub, disc\n")
            if action.lower() == "sub":
                topic = input("What topic do you want to subscribe to?\n")
                subscribe(topic.upper())        
            elif action.lower() == "pub":
                subject = input("What topic do you want to publish to?\n")
                message = input("What message would you like to send?\n")
                publish(subject, message)
            elif action.lower() == "disc":
                connected = False
                disconnect()
                client.close()      
        else: # not connected
            action = input("Would you like to reconnect? [Y/N]\n")
            if action.lower() == "yes" or action.lower() == "y":
                connected = connect(client_name, first_connection=False)
            else:
                print("Ending CLient")
                break
                
            
