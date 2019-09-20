"""Battleship game by Daylon Blakely
9/18/19"""

from random import randint
import copy

class Player:
    def __init__(self, name):
        self.name = name
        self.board = []
        #create 5x5 board
        for x in range(5):
            self.board.append(["O"] * 5)
        #create an identical board to represent opponent
        self.opponent_board = copy.deepcopy(self.board)

    def get_name(self):
        return self.name

    #custom print to organize player's boards
    def print_board(self):
        print(self.get_name() + " board:" + " "*10 + "Opponent's board:")
        i = 0
        for row in self.board:
            print(" ".join(row) + " "*20 + " ".join(self.opponent_board[i]))
            i += 1

def create_ships(Player):
    board = Player.board

    #randomly place 1X1 ship to player's board, try again if space is occupied
    ship_row = randint(0, len(board) - 1)
    ship_col = randint(0, len(board) - 1)
    if board[ship_row][ship_col] == "O":
        board[ship_row][ship_col] = "X"
    else:
        create_ships(Player)

game_over = False

def take_turn(this_player, opponent):
    global game_over
    this_player.print_board()
    guess_row = int(input("Guess row:")) -1
    guess_col = int(input("Guess col:")) -1

    #check for invalid guess
    if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
        print("Not even in the ocean, please enter values between 1 and 5")
        take_turn(this_player, opponent)
    #already guessed
    elif (this_player.opponent_board[guess_row][guess_col] == "M") or (
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
    p1 = Player("Player 1")
    p2 = Player("Player 2")
    create_ships(p1)
    create_ships(p1)
    create_ships(p1)
    create_ships(p2)
    create_ships(p2)
    create_ships(p2)
    p1.print_board()
    p2.print_board()

    #player one goes first
    player_going = p1
    player_not_going = p2
    while not game_over:
        take_turn(player_going, player_not_going)
        #switch players
        temp = player_going
        player_going = player_not_going
        player_not_going = temp
main()
