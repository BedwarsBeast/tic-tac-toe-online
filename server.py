import socket
import threading

HOST = "0.0.0.0"  # سرور روی همه اینترفیس‌ها گوش می‌دهد
PORT = 5555       # پورت سرور

board = [" " for _ in range(9)]
players = {}
turn = "X"
lock = threading.Lock()

def check_winner():
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "Draw"
    return None

def broadcast(msg):
    for conn in players.values():
        try:
            conn.sendall(msg.encode())
        except:
            pass

def handle_client(conn, symbol):
    global turn
    conn.sendall(f"Welcome! You are {symbol}\n".encode())
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            with lock:
                if symbol == turn and data.isdigit() and 0 <= int(data) < 9:
                    idx = int(data)
                    if board[idx] == " ":
                        board[idx] = symbol
                        turn = "O" if turn == "X" else "X"
                        winner = check_winner()
                        broadcast(f"BOARD {''.join(board)} TURN {turn}\n")
                        if winner:
                            broadcast(f"RESULT {winner}\n")
                            break
                else:
                    conn.sendall("Invalid move\n".encode())
        except:
            break
    conn.close()

def main():
    global players
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(2)
    print(f"Server started on {HOST}:{PORT}")

    symbols = ["X","O"]
    i = 0
    while i < 2:
        conn, addr = s.accept()
        players[symbols[i]] = conn
        print("Player", symbols[i], "connected:", addr)
        threading.Thread(target=handle_client, args=(conn, symbols[i])).start()
        i += 1

if __name__ == "__main__":
    main()
