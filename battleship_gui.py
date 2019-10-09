import tkinter as tk
from random import randint


class Player:
    def __init__(self, name, root):
        self.score = 0
        self.name = name
        self.root = root
        #create player's board
        self.players_board = []
        for x in range(5):
            self.players_board.append(["O"] * 5)
        self.create_ships()
        #create toplevel window for player's boards, use withdraw to hide the window when program starts
        self.win = tk.Toplevel(root)
        self.win.withdraw()
        self.win.title("Battleship")
        self.opponent_board = tk.Frame(self.win)
        self.board = tk.Frame(self.win)
        self.create_opponent_board()
        self.create_player_board()

    def create_ships(self):
        board = self.players_board
        # randomly place 1X1 ship to player's board, try again if space is occupied
        for x in range(3):
            done = False
            while not done:
                ship_row = randint(0, len(board) - 1)
                ship_col = randint(0, len(board) - 1)
                if board[ship_row][ship_col] == "O":
                    board[ship_row][ship_col] = "X"
                    done = True

    #opens the players window from being withdrawn
    def open_window(self):
        self.win.deiconify()

    #display the opponent's and player's board in the toplevel window
    def create_opponent_board(self):
        #create opponent's board for guessing
        self.opponent_board.grid(row=0, column=0, sticky=tk.W, padx=15)
        tk.Label(self.opponent_board, text="Opponent's board").grid(row=0, column=0, columnspan=5, sticky=tk.W, pady=2)
        #each button has its own x and y to be passed to a function
        for x in range(5):
            for y in range(5):
                btn = tk.Button(self.opponent_board, text="O", command=
                lambda player=self, window=self.win, frame=self.opponent_board, row=x, col=y:
                    make_guess(player, window, frame, row, col))
                btn.grid(row=x+1, column=y, sticky=tk.W, padx=2, pady=2)
    def create_player_board(self):
        #Create players board
        self.board.grid(row=0, column=1, sticky=tk.W, padx=15)
        tk.Label(self.board, text=self.name + " board").grid(row=0, column=0, sticky=tk.W, pady=2)
        # show players board as a grid of labels
        i = 1
        for row in self.players_board:
            lbl = tk.Label(self.board, text="  ".join((row)))
            lbl.grid(row=i, column=0, sticky=tk.W, padx=2, pady=5)
            i += 1

game_over = False
player_going = None
player_not_going = None

def make_guess(player, window, f, x=0, y=0):
    print("{}, {}".format(x + 1, y + 1))
    global player_going
    global player_not_going
    # make this player the player_going
    if player_going != player:
        player_going, player_not_going = player_not_going, player_going

    # set the global guess variables to the x and y and the frame to f
    guess_row = x
    guess_col = y
    # hide the player's window after they make a guess and open opponents window
    window.withdraw()
    take_turn(f, guess_row, guess_col)
    global game_over
    if not game_over:
        player_not_going.open_window()

def take_turn(frame, guess_row, guess_col):
    global game_over
    global player_going
    global player_not_going

    #already guessed
    if (player_not_going.players_board[guess_row][guess_col] == "M") or (
            player_not_going.players_board[guess_row][guess_col] == "H"):
        print("You guessed that one already!")
    #correct guess
    elif player_not_going.players_board[guess_row][guess_col] == "X":
        print("HIT!")
        # changes the opponents board and update
        player_not_going.players_board[guess_row][guess_col] = "H"
        player_not_going.create_player_board()
        # change the players board
        button = frame.grid_slaves(guess_row + 1)[4-guess_col]
        button["text"] = "H"
        button["bg"] = "green"
        #check for winner, compare hits on this_player.opponent_board with opponent.board
        if sum(x.count("X") for x in player_not_going.players_board) == 0:
            print(player_going.name + " wins!")
            player_going.score += 1
            game_over = True
            player_going.win.withdraw()
            player_going.create_opponent_board()
            player_not_going.create_opponent_board()
            player_going.root.update()
    #incorrect guess
    elif player_not_going.players_board[guess_row][guess_col] == "O":
        print("MISS!")
        #change opponents board and update
        player_not_going.players_board[guess_row][guess_col] = "M"
        player_not_going.create_player_board()
        # change the players board
        button = frame.grid_slaves(guess_row+1)[4-guess_col]
        button["text"] = "M"
        button["bg"] = "red"

def main():
    root = tk.Tk()
    root.title("Battleship")

    global player_going
    global player_not_going
    player1 = Player("Player 1", root)
    player2 = Player("Player 2", root)
    # let player1 go first
    player_going = player1
    player_not_going = player2

    open_p1 = tk.Button(root, text="Open Player 1's Window", command=player1.open_window).pack()
    open_p2 = tk.Button(root, text="Open Player 2's Window", command=player2.open_window).pack()
    play = tk.Button(root, text="Play", command=player1.open_window).pack()
    p1 = tk.Label(root, text="Player 1 Score: "+str(player1.score)).pack()
    p2 = tk.Label(root, text="Player 2 Score: " + str(player2.score)).pack()

    root.mainloop()

main()