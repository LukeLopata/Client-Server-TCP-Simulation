# README for Client-Server Notification System

## Overview
This project implements a basic client-server notification system in Python using `socket`, `threading`, and `queue` modules. The server can handle multiple client connections, allowing them to subscribe to or publish notifications on specific topics (e.g., "NEWS" and "WEATHER"). Clients can connect to the server, subscribe to topics, publish messages, and disconnect.

## Features
- **Client-side functionalities**:
  - Connect to the server.
  - Subscribe to topics (NEWS, WEATHER).
  - Publish notifications to subscribed topics.
  - Disconnect from the server.
- **Server-side functionalities**:
  - Accepts and manages multiple client connections.
  - Maintains a list of connected clients and their subscription statuses.
  - Sends notifications to subscribed clients.
  - Handles client disconnection.

## Project Structure
The project is composed of two main files:
1. **Server Script (`server.py`)**: Handles client connections, processes client requests, and sends notifications.
2. **Client Script (`client.py`)**: Connects to the server, interacts with the user, and manages subscriptions and publishing.

## Detailed Explanation

### Server (`server.py`)
- **Classes and Variables**:
  - `Client`: Represents a connected client and stores its details like name, socket, address, and subscription status.
  - `clients`: A list to store connected clients.
  - `newsQ`, `weatherQ`: Queues to store notifications for "NEWS" and "WEATHER".
  - `notifications`: A dictionary mapping topics to their respective queues.

- **Functions**:
  - `handleClient(client_socket, client_address)`: Processes messages from the connected client, handles subscriptions, publications, and disconnections.
  - `weatherNotifier()` and `newsNotifier()`: Continuously monitor their respective queues and send notifications to subscribed clients.

- **Workflow**:
  - The server waits for client connections and spawns a new thread for each client.
  - Processes subscription requests and sends acknowledgment or error messages.
  - Publishes notifications to clients that are subscribed to the respective topics.

### Client (`client.py`)
- **Variables**:
  - `SUB_ACK`, `SUB_FAILED`, `CONN_ACK`, `DISC_ACK`, `PUB_EROR`: Threading events to synchronize communication with the server.
  - `messages_out`, `messages_in`: Queues to manage outgoing and incoming messages.

- **Functions**:
  - `recevie_messages(client_socket)`: Listens for incoming messages from the server.
  - `send_messages()`: Sends queued messages to the server.
  - `subscribe(topic)`: Sends a subscription request and handles acknowledgment or retries.
  - `publish(subject, message)`: Queues a message to be published to a topic.
  - `disconnect()`: Sends a disconnection request and waits for acknowledgment.
  - `connect(client_name)`: Initiates a connection and waits for acknowledgment.

- **Workflow**:
  - The client connects to the server, provides a name, and can interact with the server by subscribing, publishing, or disconnecting.

## How to Run

### Prerequisites
- Python 3.x
- Ensure `socket`, `threading`, and `queue` modules are installed (part of Python standard library).

### Steps to Run the Server
1. Run the server script:
   ```bash
   python server.py
   ```

2. The server will start and wait for client connections.

### Steps to Run the Client
1. Run the client script:
   ```bash
   python client.py
   ```

2. Follow the prompts to:
   - Enter the client's name and port number.
   - Choose to subscribe to topics, publish messages, or disconnect.

## Sample Workflow

1. **Client connects to the server**.
   - The server responds with `CONN_ACK`.

2. **Client subscribes to "NEWS"**.
   - The server checks the subscription and responds with `SUB_ACK` if successful.

3. **Client publishes a message to "NEWS"**.
   - The message is sent to all clients subscribed to "NEWS".

4. **Client disconnects**.
   - The server acknowledges with `DISC_ACK`, and the client ends the connection.

## Error Handling
- The server handles various errors, such as invalid subscriptions and unknown message tags.
- The client uses events and timeouts to handle unresponsive or delayed server responses.
