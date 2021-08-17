from .game import *
import random
NO_MOVES = "No possible AI moves."
FIRST_ROW = 0


class AI:
    """This class represents the artificial intelligence part of the game"""
    def __init__(self, game, player):
        """
        This is the constructor of the class. is has the attributes:
        game (a game object) and player.
        :param game: four in a row game object
        :param player: A string representing the player number
        """
        self.game = game
        self.player = player

    def find_legal_move(self, timeout=None):
        """
        This function returns a move that can be made by the AI according to
        the rules of the game.
        :param timeout: None
        :return: A int representing a column index
        """
        if self.game.get_winner():
            raise Exception(NO_MOVES)
        lst = []
        for col in range(7):
            if not self.game.get_player_at(FIRST_ROW, col):
                lst.append(col)
        if len(lst) > 0:
            index = random.randint(0, len(lst)-1)
            return lst[index]
        else:
            raise Exception(NO_MOVES)

    def get_last_found_move(self):
        pass

