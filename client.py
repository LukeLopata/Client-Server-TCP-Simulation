import socket
import queue
import threading




CLIENTPORTNUMBER = 5678
SERVERPORTNUMBER = 1234

publisher = True



messages_out = queue.Queue()
messages_in = queue.Queue()


def recevie_messages(client_socket):
    
    print("hello")
    
def send_messages(client_socket):
    while True:
        try:
            message = messages_out.get() # blocks until there is a message in the Que
            client.send(message.encode())
        except:
            print("Error in sending messages")
            break
        
def wait_for_ack():
    while True:
        TODO need to manage ACK coming in here vs coming into the recieve message function
        
    
        
        
    
        
    
        




if __name__ == "__main__":
    client_name = "Client Number 1"
    
    print("Starting Client")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reusing the port
    client.connect(("localhost", SERVERPORTNUMBER))
    print("Client connected")
    
    recevie_thread = threading.Thread(target = recevie_messages, args=([client]))
    recevie_thread.daemon()
    recevie_thread.start()
    
    send_thread = threading.Thread(target = send_messages, args=([client]))
    send_thread.daemon()
    send_thread.start()
    
    # send connection message
    messages_out.put(f"{client_name}, CONN\n")
    
    action = input("What do you want to do, sub, pub, disc")
    
    if action.lower() == "sub":
        topic = input("What topic do you want to subscribe to?")
        messages_out.put(f"{client_name}, SUB, {topic}\n")
    elif action.lower() == "pub":
        topic = input("What topic do you want to publish to?")
        message = input("What messaeg would you like to send?")
        messages_out.put(f"{client_name}, PUB, {topic}, {message}\n")
    elif action.lower() == "disc":
        messages_out.put("DISC\n")
        
        
        
        


    if publisher:
        message = "PUB, WEATHER"
        client.send(message.encode())
        
    else: # subscriber
        print("i am subscribber")
        


    # Receive a message from the server
    message = client.recv(1024)
    print("Message from server:", message.decode())

    # Close the connection
    client.close()





