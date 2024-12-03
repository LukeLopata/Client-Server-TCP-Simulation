# Client-Server TCP Notification System: README

This README explains how to use a client-server TCP notification system that allows clients to subscribe to topics, publish messages, and receive notifications. The system supports reconnections and stores pending messages for offline clients.



## Features

1. **Subscriptions:** Clients can subscribe to topics like "NEWS" and "WEATHER" to receive notifications.
2. **Publishing:** Clients can publish messages to specific topics.
3. **Offline Message Queueing:** Notifications sent while a client is offline are queued for delivery upon reconnection.
4. **Concurrency:** The server handles multiple clients simultaneously using threads.
5. **Acknowledgments:** Robust feedback mechanism for actions like connection, subscription, and disconnection.



## How It Works

### Server
- **Start:** The server runs on `localhost` at port `1234`.
- **Topics:** Default topics are "NEWS" and "WEATHER."
- **Threading:** The server spawns a thread for each connected client and a thread for notifying subscribed clients about new messages for each topic.
- **Notification Handling:** Messages are queued and sent to clients subscribed to the corresponding topic.
- **Reconnection:** Reconnected clients receive queued messages from topics they missed while offline.

### Client
- **Start:** The client connects to the server on `localhost:1234`.
- **Threading:** Separate threads handle sending and receiving messages.
- **Interaction:** A text-based interface allows the user to perform actions (e.g., subscribe, publish, disconnect).
- **Acknowledgment Handling:** Acknowledgment messages confirm the success or failure of actions.



## How to Use

### Starting the Server
1. Run the server script:
   
   python server.py
   
2. The server listens for client connections and outputs logs for activity.

### Connecting a Client
1. Run the client script:
   
   python client.py
   
2. Follow the prompts to:
   - Enter a unique client name.
   - Provide a client port number (not used in the current implementation but required for future updates).

### Available Client Actions
1. **Subscribe to a Topic:**
   - Input `sub`.
   - Enter the topic (e.g., `NEWS` or `WEATHER`).
2. **Publish a Message:**
   - Input `pub`.
   - Enter the topic and the message.
   - Only subscribed clients can publish messages to a topic.
3. **Disconnect:**
   - Input `disc`.
   - Disconnects the client from the server.

### Reconnection
1. After disconnection, restart the client script.
2. Select the reconnection option to resume from where you left off, including receiving queued notifications.



## Error Handling
1. **Connection Errors:** Retries on connection failures with a timeout mechanism.
2. **Subscription Errors:** Notifies users if a subscription fails or if they attempt to publish without a subscription.
3. **Disconnection Errors:** Retries disconnection requests until acknowledged.



## Customization
- **Topics:** Modify the `list_of_subjects` in `server.py` to add or remove topics.
- **Port Numbers:** Change the `PORTNUMBER` in `server.py` and `SERVERPORTNUMBER` in `client.py` as needed.


