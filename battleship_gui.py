import tkinter as tk

class Player:
    def __init__(self, name, root):
        self.name = name
        #create player's board
        self.players_board = []
        for x in range(5):
            self.players_board.append(["O"] * 5)
        #create toplevel window for player's boards, use withdraw to hide the window when program starts
        self.win = tk.Toplevel(root)
        self.win.withdraw()
        self.win.title("Battleship")
        self.opponent_board = tk.Frame(self.win)
        self.board = tk.Frame(self.win)
        self.create_board()

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
                lambda window=self.win, row=x, col=y: make_guess(window, row, col))
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
guess_row = 0
guess_col = 0

def make_guess(window, x=0, y=0):
    global guess_row
    global guess_col
    print("{}, {}".format(x + 1, y + 1))
    # set the global guess variables to the x and y
    guess_row = x+1
    guess_col = y+1
    # hide the player's window after they make a guess
    window.withdraw()

def take_turn(this_player, opponent):
    global game_over
    this_player.print_board()
    #loop to check for valid input
    done = False
    while not done:
        try:
            guess_row = int(input("Guess row:")) -1
            guess_col = int(input("Guess col:")) -1
            if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
                raise
            done = True
        except:
            print("INVALID INPUT! Please enter values between 1 and 5")

    #already guessed
    if (this_player.opponent_board[guess_row][guess_col] == "M") or (
            this_player.opponent_board[guess_row][guess_col] == "H"):
        print("You guessed that one already!")
    #correct guess
    elif opponent.board[guess_row][guess_col] == "X":
        print("HIT!")
        this_player.opponent_board[guess_row][guess_col] = "H"
        opponent.board[guess_row][guess_col] = "H"
        #check for winner, compare hits on this_player.opponent_board with opponent.board
        if sum(x.count("X") for x in opponent.board) == 0:
            print(this_player.get_name() + " wins!")
            game_over = True
    #incorrect guess
    elif opponent.board[guess_row][guess_col] == "O":
        print("MISS!")
        this_player.opponent_board[guess_row][guess_col] = "M"
        opponent.board[guess_row][guess_col] = "M"

def main():
    root = tk.Tk()
    root.title("Battleship")
    p1 = Player("Player 1", root)
    p2 = Player("Player 2", root)
    open_p1 = tk.Button(root, text="Open Player 1's Window", command=lambda player=p1: p1.open_window()).pack()
    open_p2 = tk.Button(root, text="Open Player 2's Window", command=lambda player=p1: p2.open_window()).pack()
    root.mainloop()

main()