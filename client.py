import socket




CLIENTPORTNUMBER = 5678
SERVERPORTNUMBER = 1234




print("Starting Client")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(('localhost', CLIENTPORTNUMBER))


client.connect(("localhost", SERVERPORTNUMBER))
print("client connected")



# Receive a message from the server
message = client.recv(1024)
print("Message from server:", message.decode())

# Close the connection
client.close()





