import socket
import threading

waiting_players = []
games = []

class Game:
    def __init__(self, player1, player2):
        self.board = [' ']*9
        self.players = [player1, player2]
        self.turn = 0  # 0 -> X, 1 -> O
        self.symbols = ['X','O']
        self.send_board()

    def send_board(self):
        for i, p in enumerate(self.players):
            msg = f"\nBOARD {self.board} TURN {self.symbols[self.turn]}"
            p.sendall(msg.encode())

    def make_move(self, player, pos):
        if player != self.players[self.turn]:
            player.sendall("Not your turn!\n".encode())
            return
        if self.board[pos] != ' ':
            player.sendall("Invalid move!\n".encode())
            return
        self.board[pos] = self.symbols[self.turn]
        self.turn = 1 - self.turn
        self.send_board()

def handle_player(conn, addr):
    global waiting_players
    conn.sendall("Welcome! Waiting for opponent...\n".encode())
    
    if waiting_players:
        opponent = waiting_players.pop(0)
        game = Game(opponent, conn)
        games.append(game)
    else:
        waiting_players.append(conn)
        return  # منتظر بازیکن بعدی بمان

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data: break
            if data.isdigit() and 0 <= int(data) < 9:
                game.make_move(conn, int(data))
        except:
            break
    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen()
    print("Server started on 0.0.0.0:5555")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_player, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
