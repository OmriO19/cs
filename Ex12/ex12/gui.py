from tkinter import *
import subprocess, os
from .ai import *
import time

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PC_IMG = os.path.join(SCRIPT_DIRECTORY, "pc.png")
HUMAN_VS_PC_IMG = os.path.join(SCRIPT_DIRECTORY, "combined2.png")
PC_VS_HUMAN_IMG = os.path.join(SCRIPT_DIRECTORY, "combined1.png")
STREAK1_IMG = os.path.join(SCRIPT_DIRECTORY, "streak_1.png")
STREAK2_IMG = os.path.join(SCRIPT_DIRECTORY, "streak_2.png")
COUPLE_IMG = os.path.join(SCRIPT_DIRECTORY, "couple.png")
COL_IMG = os.path.join(SCRIPT_DIRECTORY, "col.png")
SONG = os.path.join(SCRIPT_DIRECTORY, "music.wav")
BLANK_IMG = os.path.join(SCRIPT_DIRECTORY, "blank.png")
PLAYER1_IMG = os.path.join(SCRIPT_DIRECTORY, "p1.png")
PLAYER2_IMG = os.path.join(SCRIPT_DIRECTORY, "p2.png")
ROW = 0
COL = 1
AXES = [[(0,-1), (0,1)], [(-1,0), (1,0)], [(-1,-1), (1,1)], [(1,-1), (-1,1)]]
COLOUR = "medium sea green"


class GuiGame:
    """this class runs the graphics of the game four in a row"""
    def __init__(self, game, parent):
        """
        This is the constructor of the class. it takes game and parent as
        parameters.
        :param game: four in a row game object
        :param parent: master window
        """
        self.game = game
        self.parent = parent
        self.parent.geometry("700x600")
        self.parent.resizable(0, 0)
        self.parent.title("Four In A Row")
        self.parent.protocol("WM_DELETE_WINDOW", self.close_windows)
        self.current_player = "1"
        self.player1 = None
        self.player2 = None
        self.cell_labels = {}
        self.col_buttons = []
        self.mainframe = Frame(self.parent, height=600, width=700, bg=COLOUR)
        self.top_frame = Frame(self.parent, height=200, width=700, bg=COLOUR)
        self.cells_frame= Frame(self.parent, height=500, width=560, bg=COLOUR)
        self.player_label = Label(self.top_frame,
                                  text="Current player: {}".
                                  format(self.current_player),
                                  font=("Impact", 20), bg=COLOUR)
        self.new_game = False
        self.opening_window()

    def close_windows(self):
        """
        This function creates and operates the window that pops up when a user
        asks to leave the game using the X on the top right
        :return:
        """
        c_window = Toplevel()
        c_window.geometry("%dx%d%+d%+d" % (200, 80, 500, 500))
        c_window.title("Exit")
        exit_l = Label(c_window, text="Are you sure you want to exit?",
                       font=("Impact", 10))
        exit_y = Button(c_window, padx=30, pady=10, text="Yes",
                        command=self.parent.destroy, font=("Impact", 10))
        exit_n = Button(c_window, padx=30, pady=10, text="No",
                        command=c_window.destroy, font=("Impact", 10))
        exit_l.pack()
        exit_y.pack(side=LEFT)
        exit_n.pack(side=RIGHT)

    def winning_windows(self):
        """
        This function creates and operates the window that pops up when the
        game is over.
        :return:
        """
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', SONG))
        elif os.name == 'nt':  # For Windows environment
            os.startfile(SONG)
        elif os.name == 'posix':  # For Linux, Mac, etc. environment
            subprocess.call(('xdg-open', SONG))
        self.parent.attributes("-topmost", True)
        w_window = Toplevel()
        w_window.attributes("-topmost", True)
        w_window.geometry("%dx%d%+d%+d" % (200, 80, 500, 500))
        w_window.title(" ")
        winner = self.game.get_winner()
        if winner == 1 or winner == 2:
            win_l = Label(w_window,
                          text="CONGRATS! Player %s  Won!" %str(winner),
                          font=("Impact", 11))
        else:
            win_l = Label(w_window, text="It's a tie!", font=("Impact", 11))
        msg = Label(w_window, text="Do you want to play another game?",
                    font=("Impact", 10))
        n_game = Button(w_window, text="Yes", padx=30, pady=10,
                        command=self.start_new_game, font=("Impact", 10))
        y_exit = Button(w_window, text="No", padx=30, pady=10,
                        command=self.parent.destroy, font=("Impact", 10))
        win_l.pack()
        msg.pack()
        n_game.pack(side=LEFT)
        y_exit.pack(side=RIGHT)

    def start_new_game(self):
        """
        This function is called when a new game is desired by the user,
        destroying the old window and changing the flag to True.
        :return:
        """
        self.parent.destroy()
        self.new_game = True

    def is_new_game(self):
        """
        :return: Boolean. True if there's a request for new game, False if not
        """
        return self.new_game

    def opening_window(self):
        """
        This function creates and operates the window that pops up when the
        game is entered.
        :return:
        """
        self.mainframe.pack()
        o_name_label = Label(self.mainframe, text="Four In A Row",
                             bg=COLOUR,fg="black", font=("Impact", 45))
        o_name_label.place(x=190, y= 120)
        chose_player = Label(self.mainframe,
                             text="Choose player type to start playing:",
                             fg="black", bg=COLOUR, font=("Impact", 25))
        chose_player.place(x=117, y=260)
        pc_img = PhotoImage(file=PC_IMG)
        human_vs_pc_img = PhotoImage(file=HUMAN_VS_PC_IMG)
        pc_vs_human_img = PhotoImage(file=PC_VS_HUMAN_IMG)
        couple_img = PhotoImage(file=COUPLE_IMG)
        pc_button = Button(self.mainframe, image=pc_img, width="80",
                           height="80", bg=COLOUR)
        pc_button.image = pc_img
        pc_button.bind("<Button-1>", lambda event:
        self.set_and_destroy(self.mainframe, "pc", "pc"))
        pc_vs_human_button = Button(self.mainframe, image=pc_vs_human_img,
                                    width=80,height=80, bg=COLOUR)
        pc_vs_human_button.image = pc_vs_human_img
        pc_vs_human_button.bind("<Button-1>", lambda event:
        self.set_and_destroy(self.mainframe, "pc", "human"))
        human_vs_pc_button = Button(self.mainframe, image=human_vs_pc_img,
                                    width=80, height=80, bg=COLOUR)
        human_vs_pc_button.image = human_vs_pc_img
        human_vs_pc_button.bind("<Button-1>", lambda event:
        self.set_and_destroy(self.mainframe, "human", "pc"))
        couple_button = Button(self.mainframe, image=couple_img,
                               width=80, height=80, bg=COLOUR)
        couple_button.image=couple_img
        couple_button.bind("<Button-1>", lambda event:
        self.set_and_destroy(self.mainframe, "human", "human"))
        pc_label = Label(self.mainframe, text="AI vs AI", bg=COLOUR, font=("Helvetica", 12, "bold"))
        pc_vs_h_label = Label(self.mainframe, text="AI vs Player", bg=COLOUR, font=("Helvetica", 12, "bold"))
        h_vs_pc_label = Label(self.mainframe, text="Player vs AI", bg=COLOUR, font=("Helvetica", 12, "bold"))
        h_vs_h_label = Label(self.mainframe, text="Player vs Player", bg=COLOUR, font=("Helvetica", 12, "bold"))
        pc_button.place(x=115, y=330)
        pc_label.place(x=127, y=420)
        pc_vs_human_button.place(x=250, y=330)
        pc_vs_h_label.place(x=247, y=420)
        human_vs_pc_button.place(x=380, y=330)
        h_vs_pc_label.place(x=377, y=420)
        couple_button.place(x=510, y=330)
        h_vs_h_label.place(x=495, y=420)

    def set_and_destroy(self, frame, side_1, side_2):
        """
        this function sets the chosen players in the upcoming game and destroys
        the frame in the opening window
        :param frame:
        :param side_1: A string representing the first chosen side
        :param side_2: A string representing the second chosen side
        :return:
        """
        frame.destroy()
        if side_1 == "pc":
            self.player1 = AI(self.game, "1")
        else:
            self.player1 = side_1
        if side_2 == "pc":
            self.player2 = AI(self.game, "2")
        else:
            self.player2 = side_2
        self.game_window()

    def set_current_player(self):
        """
        This function changed the current player according to the whose turn it
        and changes the label in the game window accordingly.
        :return:
        """
        self.current_player = str(self.game.get_current_player())
        self.player_label.configure(text="Current player: {}"
                                    .format(self.current_player))
        player, is_ai = self.get_player_type()
        for button in self.col_buttons:
            if is_ai:
                    button.configure(state=DISABLED)
            else:
                    button.configure(state=NORMAL)

    def get_player_type(self):
        """
        :return: A player: AI object if it's AI, string if not
        :return: A boolean value true if it's AI, false if not
        """
        if self.current_player == "1":
            player = self.player1
            p_type = type(self.player1)
            if p_type != str and p_type is not None:
                is_ai = True
            else:
                is_ai = False
        else:
            player = self.player2
            p_type = type(self.player2)
            if p_type != str and p_type is not None:
                is_ai = True
            else:
                is_ai = False
        return player, is_ai

    def make_ai_move(self):
        """
        This function is responsible for the moves of the players of the type
        AI, as long as the game isn't over.
        :return:
        """
        player, is_ai = self.get_player_type()
        if self.game.get_winner() is None:
                if is_ai:
                    col = player.find_legal_move()
                    time.sleep(1)
                    self.move(col)
                self.parent.after(500, self.make_ai_move)
        else:
            self.winning_windows()

    def move(self, col):
        """
        This function makes the move, changes the player accordingly and if the
        game is won, calls for a change in the winning sequence.
        :param col: A int representing column index
        :return:
        """
        try:
            self.game.make_move(col)
            self.set_current_player()
            last_cord = self.set_cells(col)
            if last_cord:
                self.mark_the_winning_seq(*last_cord)
        except Exception:
            pass

    def game_window(self):
        """
        this function sets the buttons and the labels of the game window,
        the function call to the functions that preform the move
        :return:
        """
        self.top_frame.pack()
        self.player_label.pack(side=TOP)
        col_img = PhotoImage(file=COL_IMG)
        self.cells_frame.pack(side=BOTTOM)
        blank_img = PhotoImage(file=BLANK_IMG)
        for i in range(1,7):
            for j in range(1,8):
                self.cell_labels[(i-1,j-1)] = Label(
                    self.cells_frame, image=blank_img, bg=COLOUR,
                    width=75, height=75)
                self.cell_labels[(i-1,j-1)].image = blank_img
                self.cell_labels[(i-1,j-1)].place(x=j*80, y=i*78, anchor=SE)
        for i in range(7):
            self.col_buttons.append(
                Button(self.top_frame, image=col_img, width=75, height=75,
                       bg=COLOUR, command=self.set_human_move(i)))
            self.col_buttons[i].image = col_img
            self.col_buttons[i].pack(side=LEFT)
        self.make_ai_move()

    def set_human_move(self, col):
        """
        This function is responsible  for the human moves in the game, as
        dictated by the button presses.
        :param col: A int representing column index
        :return:
        """
        def h_move():
            self.move(col)
        return h_move

    def mark_the_winning_seq(self, row, col):
        """
        This function marks the winning streak
        :param row: A int representing row index
        :param col: A int representing column index
        :return:
        """
        cor_set = self.get_the_winning_seq((row, col))
        cor_set.update([(row,col)])
        st1_img = PhotoImage(file=STREAK1_IMG)
        st2_img = PhotoImage(file=STREAK2_IMG)
        for cor in cor_set:
            if self.game.get_winner() == 1:
                self.cell_labels[cor].configure(image=st1_img)
                self.cell_labels[cor].image = st1_img
            elif self.game.get_winner()==2:
                self.cell_labels[cor].configure(image=st2_img)
                self.cell_labels[cor].image = st2_img

    def get_the_winning_seq(self, cor):
        """
        This function looks for the winning streak from the last coordinate
        played by checking the axes relative to it.
        :param cor: A tuple representing a row and a column indexes
        :return:
        """
        winning_player = self.game.get_player_at(*cor)
        axes_dict = {}
        win_cords = set()
        for axis in AXES:
            axes_dict[axis[0]] = []
            for dir in axis:
                next_cor = (cor[ROW]+dir[ROW], cor[COL]+dir[COL])
                if not self.is_in_board(next_cor):
                    continue
                else:
                    while self.game.get_player_at(*next_cor) == winning_player:
                        axes_dict[axis[0]].append(next_cor)
                        next_cor = (next_cor[ROW] + dir[ROW],
                                    next_cor[COL] + dir[COL])
                        if not self.is_in_board(next_cor):
                            break
        for axis, found_cor in axes_dict.items():
            if len(found_cor) >= 3:
                win_cords.update(found_cor)
        return win_cords

    def is_in_board(self, cor):
        """
        This functions returns a boolean value that represents whether the
        coordinate is in the board.
        :param cor: A tuple representing a row and a column indexes
        :return: Boolean
        """
        if cor[ROW] < 0 or cor[ROW] > 5 or cor[COL] > 6 or cor[COL] < 0:
            return False
        return True

    def set_cells(self, col):
        """
        this function changes the image of the cell of current move
        :param col: A int representing column index
        :return: A int representing row index
        :return: A int representing column index
        :return: None if the game isn't over
        """
        player1_img = PhotoImage(file=PLAYER1_IMG)
        player2_img = PhotoImage(file=PLAYER2_IMG)
        for i in range(6):
            player_type = self.game.get_player_at(i,col)
            if player_type == 2:
                self.cell_labels[(i, col)].configure(image=player2_img)
                self.cell_labels[(i, col)].image = player2_img
                if self.game.get_winner() is not None:
                    return i, col
            elif player_type == 1:
                self.cell_labels[(i, col)].configure(image=player1_img)
                self.cell_labels[(i, col)].image = player1_img
                if self.game.get_winner() is not None:
                    return i, col
