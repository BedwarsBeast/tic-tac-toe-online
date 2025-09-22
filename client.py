import socket
import threading

SERVER = "localhost"
PORT = 5555

board = [' ']*9

def print_board():
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def listen(sock):
    global board
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data: break
            if data.startswith("BOARD"):
                parts = data.split()
                board = list(parts[1:10])
                print_board()
            else:
                print(data)
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, PORT))
    threading.Thread(target=listen, args=(sock,), daemon=True).start()

    while True:
        move = input("Enter cell (0-8): ")
        sock.sendall(move.encode())

if __name__ == "__main__":
    main()

