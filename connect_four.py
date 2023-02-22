import tkinter as tk

class ConnectFour:
    class Column:
        """
        This class represents a column of the Connect4 game. It stores a series of characters representing game pieces.
        capacity: the max number of tokens the column can store.
        """
        def __init__(self, capacity):
            self.stack = []
            self.capacity = capacity
            self.height = 0

        def full(self):
            return self.height == self.capacity

        def drop(self, token):
            """
            Adds the token to the column. Returns height of token drop  (or -1 if failed.)
            """
            if self.full():
                return -1

            self.stack.append(token)
            self.height += 1
            return self.height - 1

        def match(self, token, height):
            """
            Returns True if token matches the tokens at the specified height, else False.
            """
            if height >= self.height:
                return False

            return self.stack[height] == token

    def __init__(self, columns, height):
        """
        Connect Four game instance.
        """
        self.columns = [self.Column(height) for _ in range(columns)]
        self.dimensions = [columns, height]

    def occupied(self, column, height):
        if column < 0 or height < 0:
            return False
        
        if column > self.dimensions[0] - 1:
            return False

        return height < self.columns[column].height

    def legal(self, column):
        return not self.columns[column].full()

    def drop(self, column, token):
        """
        Returns the height at which the token was dropped.
        """
        if not self.legal(column):
            return -1

        return self.columns[column].drop(token)

    def check_array(self, array, index):
        token = array[index]
        total = 1

        # left
        for i in range(index - 1, 0, -1):
            if array[i] == token:
                total += 1
            else:
                break

        # right
        for i in range(index + 1, len(array)):
            if array[i] == token:
                total += 1
            else:
                break

        return total >= 4

    def full(self):
        for column in self.columns:
            if not column.full():
                return False
        return True

    def check_win(self, column, row):
        # Check various possible wins
        # horizonta;, vertical and both diagonals

        token = self.columns[column].stack[row]

        l = [True, 0]
        r = [True, 0]
        u = [True, 0]
        d = [True, 0]
        dl = [True, 0]
        dr = [True, 0]
        ul = [True, 0]
        ur = [True, 0]
        
        for i in range(1,4):
            # Horizontal
            # Left
            if l[0] and self.occupied(column - i, row) and self.columns[column - i].match(token, row):
                l[1] += 1
            else:
                l[0] = False

            # Right
            if r[0] and self.occupied(column + i, row) and self.columns[column + i].match(token, row):
                r[1] += 1
            else:
                r[0] = False

        return (l[1] + r[1]) >= 3

class Interface:
    TILE_SIZE = 100 # pixels
    MARGIN = 5

    def __init__(self, columns, rows, player1, player2):
        self.game = None
        self.tiles = []
        self.window = tk.Tk()
        self.turn = 0
        self.players = [player1, player2]
        self.score = [0, 0]
        self.dimensions = [columns, rows]
        self.round = 0
    
    def new_game(self):
        self.tiles = []
        self.round += 1

        for child in self.window.winfo_children():
            child.destroy()

        self.game = ConnectFour(self.dimensions[0], self.dimensions[1])
        self.draw_board()
        self.turn = self.round % 2

    def draw_board(self):
        tk.Label(text = "{}: {}".format(self.players[0], self.score[0]), fg = "white", bg = "red").grid(row = 0, column = 2)
        tk.Label(text = "{} :{}".format(self.players[1], self.score[1]), fg = "black", bg = "yellow").grid(row = 0, column = 4)

        for row in range(self.game.dimensions[1]):
            self.tiles.append([])

            for column in range(self.game.dimensions[0]):
                chip = tk.Canvas(self.window, width = self.TILE_SIZE, height = self.TILE_SIZE, bg = "blue")
                chip.bind("<Button>", lambda x, j = column: self.request_drop(j))
                circle = chip.create_oval(self.MARGIN, self.MARGIN, self.TILE_SIZE - self.MARGIN, self.TILE_SIZE - self.MARGIN, fill = "white", outline = "blue")
                chip.grid(row = self.dimensions[1] - row, column = column)
                self.tiles[row].append([chip, circle])

    def request_drop(self, column):
        again = False
        token = self.turn % 2
        location = self.game.drop(column, token)

        if location >= 0:
            color = "red" if token == 0 else "yellow"
            self.tiles[location][column][0].itemconfig(self.tiles[location][column][1], fill = color)

            if self.game.check_win(column, location):
                print("player {} won!".format(token))
                self.score[token] += 1
                self.new_game()
            else:
                self.turn += 1
        else:
            print("Error -> couldn't drop at coordinates ({},{})".format(column, location))

        # can we continue
        if self.game.full():
            # tie
            self.new_game()

    def run(self):
        self.new_game()
        tk.mainloop()

if __name__ == '__main__':
    game = Interface(7, 6, "Veronika", "Lane")
    game.run()


