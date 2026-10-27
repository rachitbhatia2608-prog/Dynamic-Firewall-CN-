import socket
import threading


def handle_client(conn, addr):
    print(f"[HANDLER] Handling connection from {addr}")

    try:
        with conn:
            while True:
                data = conn.recv(1024)

                if not data:
                    print(f"[HANDLER] Client {addr} disconnected.")
                    break

                message = data.decode("utf-8").strip()
                print(f"[RECEIVED] From {addr}: {message}")

                response = f"ACK: Received '{message}'"
                conn.sendall(response.encode("utf-8"))
                print(f"[SENT] Response to {addr}: {response}")

    except OSError as exc:
        print(f"[HANDLER] Socket error with {addr}: {exc}")


def start_server(host="127.0.0.1", port=5000):
    print(f"--- Server starting on {host}:{port} ---")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"Server listening on {host}:{port}")

        try:
            while True:
                conn, addr = server.accept()
                print(f"[SERVER] Connection accepted from {addr}")

                thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()

        except KeyboardInterrupt:
            print("\n[SERVER] Server shutting down.")


if __name__ == "__main__":
    start_server()
