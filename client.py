import socket
import threading

SERVER = "your-server-ip-or-domain"  # مثل tic-tac-toe-online.onrender.com
PORT = 5555

def listen(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(data)
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, PORT))
    threading.Thread(target=listen, args=(sock,), daemon=True).start()

    while True:
        msg = input("Enter cell (0-8): ")
        sock.sendall(msg.encode())

if __name__ == "__main__":
    main()
