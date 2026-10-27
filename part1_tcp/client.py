import socket


def connect_to_server(host="127.0.0.1", port=5000):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Attempting to connect to {host}:{port}...")
        client_socket.connect((host, port))
        print("Successfully connected to the server.")

        message = "Hello, Server! This is Client."
        print(f"Sending message: '{message}'")
        client_socket.sendall(message.encode("utf-8"))

        response = client_socket.recv(1024)

        if response:
            print(f"Received response: {response.decode('utf-8')}")

        print("Communication complete.")

    except OSError as exc:
        print(f"Socket error: {exc}")
        print("Ensure the server is running and accessible.")

    finally:
        client_socket.close()
        print("Client socket closed.")


if __name__ == "__main__":
    connect_to_server()
