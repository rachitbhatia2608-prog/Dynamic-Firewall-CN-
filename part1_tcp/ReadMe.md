# Part 1: TCP Client-Server Communication

## 1. Overview

This part demonstrates connection-oriented communication using TCP
sockets in Python. A client connects to a server, sends a message,
and receives an acknowledgement from the server.

The server uses Python threading to handle multiple client connections.

## 2. Project Structure

- `server.py` - TCP server that accepts connections, receives messages,
  and sends acknowledgements.
- `client.py` - TCP client that connects to the server, sends a message,
  and receives the response.
- `README.md` - Documentation and execution instructions.

## 3. Requirements

- Ubuntu/Linux or another supported operating system
- Python 3
- No third-party Python packages required

## 4. Concepts Demonstrated

- TCP sockets and connection-oriented communication
- Client-server architecture
- Socket creation, binding, listening, and accepting connections
- Sending and receiving data over a TCP connection
- Concurrent client handling using Python threads
- Acknowledgement messages

## 5. Configuration

- Host: `127.0.0.1`
- Port: `5000`
- Protocol: TCP

The loopback address is suitable when the client and server run on
the same machine. Communication between different machines requires
appropriate network addresses and firewall configuration.

## 6. How to Run

Open two Ubuntu terminals.

### Terminal 1: Start the server

    cd /home/rachit/CN-Dynamic-Firewall/part1_tcp
    python3 server.py

Keep the server running.

### Terminal 2: Run the client

    cd /home/rachit/CN-Dynamic-Firewall/part1_tcp
    python3 client.py

Expected response:

    Received response: ACK: Received 'Hello, Server! This is Client.'

## 7. Verification

The basic client-server test was run successfully in Ubuntu. The client
connected to the server, sent a message, received the expected
acknowledgement, and closed its socket.

## 8. Limitations

This part demonstrates basic TCP communication. It does not implement
dynamic firewall rules, intrusion detection, or security-event logging.
These features must be implemented and tested separately as part of
the larger project.
