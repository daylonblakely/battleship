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
                lambda frame=self.opponent_board, row=x, col=y: do_something(frame, row, col))
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


def do_something(frame, x=0, y=0):
    print("{}, {}".format(x + 1, y + 1))

def main():
    root = tk.Tk()
    root.title("Battleship")
    p1 = Player("Player 1", root)
    p2 = Player("Player 2", root)
    open_p1 = tk.Button(root, text="Open Player 1's Window", command=lambda player=p1: p1.open_window()).pack()
    open_p2 = tk.Button(root, text="Open Player 2's Window", command=lambda player=p1: p2.open_window()).pack()
    root.mainloop()

main()