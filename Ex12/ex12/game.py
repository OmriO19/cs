ROW = 0
COL = 1
FIRST_ROW = 0
FIRST_COL = 0
FIRST_PLAYER = 1
SECOND_PLAYER = 2
EMPTY = None
DOWN = "down"
UP = "up"
RIGHT = "right"
LEFT = "left"
UP_LEFT = "up left"
UP_RIGHT = "up right"
DOWN_RIGHT = "down right"
DOWN_LEFT = "down left"
ILLEGAL_MOVE = "Illegal move."
ILLEGAL_LOCATION = "Illegal location."


class Game:
    """This class is responsible for the game logic and rules"""

    def __init__(self):
        """
        This is the constructor of the class, it has the attributes:
        current_player, board (a board object) and a winner.
        """
        self.current_player = FIRST_PLAYER
        self.board = Board()
        self.winner = None

    def make_move(self, column):
        """
        This function makes the move in the game - as long as the game isn't
        over, it places the disk in the right cell in the column chosen by
        the player. It raises an exception if the move is illegal or made
        after the game is won.
        :param column: A int representing column index
        :return:
        """
        if self.winner is not None:
            raise Exception(ILLEGAL_MOVE)
        else:
            try:
                player = self.current_player
                cell = self.board.set_cell(int(column), player)
                if cell:
                    self.set_winner(cell, player)
                    self.change_player()
                else:
                    raise Exception(ILLEGAL_MOVE)
            except KeyError:
                raise Exception(ILLEGAL_MOVE)

    def get_winner(self):
        """
        :return: The winner of the game
        """
        return self.winner

    def get_player_at(self, row, col):
        """
        This function returns the player at a given location
        :param row: A int representing row index
        :param col: A int representing column index
        :return:
        """
        if (row,col) in self.board.get_cells():
                return self.board.get_cells()[(row,col)].get_data()
        raise Exception(ILLEGAL_LOCATION)

    def get_current_player(self):
        """
        :return: the player that has the current turn
        """
        return self.current_player

    def change_player(self):
        """
        This function changes the switches of the players
        :return:
        """
        if self.current_player == FIRST_PLAYER:
            self.current_player = SECOND_PLAYER
        else:
            self.current_player = FIRST_PLAYER

    def set_winner(self, cell, player):
        """
        This function uses it's supplementary function in order to determine
        the winner of the game.
        :param cell: A cell object
        :param player: A int representing a player
        :return:
        """
        if cell.get_row() == FIRST_ROW:
            if self.board.is_full():
                self.winner = 0
        for dir, neighbor in cell.get_neighbors().items():
            if self.set_winner_helper(neighbor, dir, player, 0):
                self.winner = player
            if neighbor.get_data() == player:
                op_dir = self.opp_dir(dir)
                if self.set_winner_helper(neighbor, op_dir, player, -1):
                    self.winner = player

    def set_winner_helper(self, cell, dir, player, i):
        """
        This function runs recursively on the neighbors of the cell in a
        in which the cell has neighbors of the same "sort" and also on the
        opposite direction and checks for streaks of 4.
        :param cell: A cell object
        :param dir: A string representing direction
        :param player: A int representing a player
        :param i: A int representing counter
        :return:
        """
        if cell.get_data() != player:
            return False
        else:
            i += 1
        if i == 3:
            return True
        if dir not in cell.get_neighbors():
            return False
        return self.set_winner_helper(cell.get_neighbors()[dir],
                                      dir, player, i)

    def opp_dir(self, dir):
        """
        :param dir: A string representing direction
        :return: The opposite direction to the one that given.
        """
        if dir==RIGHT:
            return LEFT
        elif dir==LEFT:
            return RIGHT
        elif dir==UP:
            return DOWN
        elif dir==DOWN:
            return UP
        elif dir==UP_LEFT:
            return DOWN_RIGHT
        elif dir==UP_RIGHT:
            return DOWN_LEFT
        elif dir==DOWN_RIGHT:
            return UP_LEFT
        else:
            return UP_RIGHT

class Cell:
    """This class represents the cells in the game, each coordinate in the game
    is a cell."""

    def __init__(self, row_idx, col_idx):
        """
        A constructor for a cell object, it has the attributes:
        row_idx, col_idx, data and neighbors.
        :param row_idx: A int representing row index
        :param col_idx: A int representing col index
        """
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.data = EMPTY
        self.neighbors = {}

    def get_data(self):
        """
        :return: the cell's data
        """
        return self.data

    def get_row(self):
        """
        :return: the cells row coordinate
        """
        return self.row_idx

    def update_data(self, val):
        """
        This function updates the cells data
        :param val: A int representing player
        """
        self.data = val

    def set_neighbors(self, cor, cell):
        """
        This function updates the cell's neighbors dict according to the cells
        around it
        :param cor: A tuple of row index and a column index
        :param cell: A cell object
        :return:
        """
        if cor[ROW] == self.row_idx:
            if cor[COL] == self.col_idx + 1:
                self.neighbors[RIGHT] = cell
            elif cor[COL] == self.col_idx - 1:
                self.neighbors[LEFT] = cell
        elif cor[ROW] == self.row_idx - 1:
            if cor[COL] == self.col_idx + 1:
                self.neighbors[UP_RIGHT] = cell
            elif cor[COL] == self.col_idx - 1:
                self.neighbors[UP_LEFT] = cell
            elif cor[COL] == self.col_idx:
                self.neighbors[UP] = cell
        elif cor[ROW] == self.row_idx + 1:
            if cor[COL] == self.col_idx + 1:
                self.neighbors[DOWN_RIGHT] = cell
            elif cor[COL] == self.col_idx - 1:
                self.neighbors[DOWN_LEFT] = cell
            elif cor[COL] == self.col_idx:
                self.neighbors[DOWN] = cell

    def get_neighbors(self):
        """
        :return: The cell's neighbors
        """
        return self.neighbors


class Board:
    """This class represents the game board"""

    def __init__(self):
        """
         A constructor for a board object. it has the attribute cell_dict,
         which is a dictionary of all cells in the board, and in each of
         them, their neighbors
        """
        self.cell_dict = {(row, col): Cell(row, col) for row in range(6)
                          for col in range(7)}
        for cor, cell in self.cell_dict.items():
            neighbors = self.neighbors(*cor)
            for coordinate in neighbors:
                cell.set_neighbors(coordinate, self.cell_dict[coordinate])

    def neighbors(self, x, y):
        """
        This function returns the neighbors of each cell, while staying in the
        borders of the board
        :param x: A int representing row index
        :param y: A int representing column index
        :return:
        """
        return [(row, col) for row in range(x - 1, x + 2)
                for col in range(y - 1, y + 2)
                if ((x != row or y != col) and  # check not itself
                    (0 <= row <= 5) and  # check borders x
                    (0 <= col <= 6))]  # check borders y

    def set_cell(self, col, player):
        """
        This function finds the first free cell in the given column and
        updates it's content to the player given to it
        :param col: A int representing column index
        :param player: A int representing player
        :return:
        """
        cur_cell = self.cell_dict[(FIRST_ROW, col)]
        if not cur_cell.get_data():
            while DOWN in cur_cell.get_neighbors():
                if not cur_cell.get_neighbors()[DOWN].get_data():
                    cur_cell = cur_cell.get_neighbors()[DOWN]
                else:
                    break
            cur_cell.update_data(player)
            return cur_cell

    def get_cells(self):
        """
        :return: the cell dictionary of the board
        """
        return self.cell_dict

    def is_full(self):
        """
        This function checks if the board is full, using it's supplementary
        function
        :return:
        """
        first_cell = self.cell_dict[(FIRST_ROW, FIRST_COL)]
        if self.is_full_helper(first_cell):
            return True
        return False

    def is_full_helper(self, cell):
        """
        This function runs recursively on the top row from left ti right,
        checking whether the cells are empty.
        :param cell: A cell object
        :return:
        """
        if not cell.get_data():
            return False
        if RIGHT not in cell.get_neighbors():
            return True
        return self.is_full_helper(cell.get_neighbors()[RIGHT])
