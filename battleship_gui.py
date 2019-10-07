import tkinter as tk
from random import randint


class Player:
    def __init__(self, name, root):
        self.name = name
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
        self.create_board()

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
    def create_board(self):
        #create opponent's board for guessing
        self.opponent_board.grid(row=0, column=0, sticky=tk.W, padx=15)
        tk.Label(self.opponent_board, text="Opponent's board").grid(row=0, column=0, columnspan=5, sticky=tk.W, pady=2)
        #each button has its own x and y to be passed to a function
        for x in range(5):
            for y in range(5):
                btn = tk.Button(self.opponent_board, text="O", command=
                lambda window=self.win, frame=self.opponent_board, row=x, col=y: make_guess(window, frame, row, col))
                btn.grid(row=x+1, column=y, sticky=tk.W, padx=2, pady=2)

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

def make_guess(window, f, x=0, y=0):
    print("{}, {}".format(x + 1, y + 1))
    # set the global guess variables to the x and y and the frame to f
    guess_row = x
    guess_col = y
    frame = f
    # hide the player's window after they make a guess
    window.withdraw()
    take_turn(f, guess_row, guess_col)

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
        # changes the opponents board
        player_not_going.players_board[guess_row][guess_col] = "H"
        # change the players board
        button = frame.grid_slaves(guess_row + 1)[4-guess_col]
        button["text"] = "H"
        #check for winner, compare hits on this_player.opponent_board with opponent.board
        if sum(x.count("X") for x in player_not_going.players_board) == 0:
            print(player_going.name + " wins!")
            game_over = True
    #incorrect guess
    elif player_not_going.players_board[guess_row][guess_col] == "O":
        print("MISS!")
        player_not_going.players_board[guess_row][guess_col] = "M"
        # change the players board
        button = frame.grid_slaves(guess_row+1)[4-guess_col]
        button["text"] = "M"

    #switch the players at end of turn
    player_going, player_not_going = player_not_going, player_going

def main():
    root = tk.Tk()
    root.title("Battleship")
    player1 = Player("Player 1", root)
    player2 = Player("Player 2", root)
    global player_going
    global player_not_going
    #let player1 go first
    player_going = player1
    player_not_going = player2
    open_p1 = tk.Button(root, text="Open Player 1's Window", command=player1.open_window).pack()
    open_p2 = tk.Button(root, text="Open Player 2's Window", command=player2.open_window).pack()

    root.mainloop()

main()