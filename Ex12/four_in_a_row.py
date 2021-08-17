from ex12.game import *
from ex12.ai import *
from ex12.gui import *
from tkinter import *


class FourInaROW:
    def __init__(self):
        """
        This is the constructor of the game, it create the game object and
        the gui.
        """
        game = Game()
        self.root = Tk()
        self.root.config(background="medium sea green")
        self.gui = GuiGame(game, self.root)
        self.root.mainloop()

    def get_new_game(self):
        """
        :return: True if there's a request for another game
        """
        if self.gui.is_new_game():
            return True


def main():
    """create a game, as long as there's a demand for one"""
    four_in_a_row = FourInaROW()
    while four_in_a_row.get_new_game():
        four_in_a_row = FourInaROW()


if __name__ == "__main__":
    main()

