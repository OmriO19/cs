import sys
import random
import math
from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo

ASTEROIDS_NUM = 5
START_SPEED = 0
START_HEADING = 0
START_SIZE = 3
AST_HIT_MSG = ("Hit!", "You've been hit by an asteroid.")
MAX_TORPEDO_NUM = 10
START_SCORE = 0
END_GAME_NO_ASTEROIDS = ("Congrats!~", "You destroyed all the asteroids, "
                                       "what a champ!")
END_GAME_EXIT = ("Exit", "Goodbye")
END_GAME_NO_LIFE = ("No dinner for you", "You lost, better luck next time!")
MAX_SPECIAL_TORPEDO = 5
LARGE = 3
MEDIUM = 2
SMALL = 1
MIN_AST_SPD = 1
MAX_AST_SPD = 4
SCORE_FOR_SPECIAL = 200
SCORE_FOR_LARGE = 20
SCORE_FOR_MEDIUM = 50
SCORE_FOR_SMALL = 100
RIGHT_TURN = -7
LEFT_TURN = 7
DEG_IN_PIE = 180
MAX_TOR_LIFETIME = 200
MAX_SPECIAL_TOR_LIFETIME = 150


class GameRunner:
    """
    This class is in charge of running the game, it encapsulates the ship,
    torpedo and asteroid classes.
    """
    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__torpedo_lst = []
        self.__special_torpedo_lst = []
        self.__score = START_SCORE
        # create two lists of random numbers for the start locations of the
        # ship and the asteroids
        ran_lst_x = random.sample(
            range(self.__screen_min_x, self.__screen_max_x),
            (asteroids_amount + 1))
        ran_lst_y = random.sample(
            range(self.__screen_min_y, self.__screen_max_y),
            (asteroids_amount + 1))
        # create a ship object with the start values
        self.__ship = Ship(ran_lst_x[0], START_SPEED, ran_lst_y[0],
                           START_SPEED, START_HEADING)
        # create asteroids with the start values and add them to a list
        self.__asteroid_lst = []
        for i in range(1, asteroids_amount + 1):
            location_x = ran_lst_x[i]
            location_y = ran_lst_y[i]
            ast_speed = random.randint(MIN_AST_SPD, MAX_AST_SPD)
            self.__asteroid_lst.append(
                Asteroid(location_x, ast_speed, location_y, ast_speed,
                         START_SIZE))
        for asteroid in self.__asteroid_lst:
            self.__screen.register_asteroid(asteroid, asteroid.get_size())

    def run(self):
        """
        Starts the screen and runs the loop
        :return:
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """
        Activates the game loop and sets the timer
        :return:
        """
        # You don't need to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        The main function of the game. In this function whether the game should
        be finished, move the objects (depending on the user's actions), create
        the special and regular torpedoes (if the user presses the right key)
        and check for collisions of the ship and the torpedos with the
        asteroids that are currently in the screen
        :return: None
        """
        if self.is_game_done():
            self.__screen.end_game()
            sys.exit()
        self.ship_movement()
        self.teleport()
        for asteroid in self.__asteroid_lst:
            self.__screen.draw_asteroid(asteroid, asteroid.get_x(),
                                        asteroid.get_y())
            self.asteroid_movement(asteroid)
        # in the next lines it creates and move the torpedoes
        self.create_torpedo()
        for tor in self.__torpedo_lst:
            self.torpedo_movement(tor)
        self.create_special_torpedo()
        for s_tor in self.__special_torpedo_lst:
            self.torpedo_movement(s_tor)
        # in the lines it checks if there's a collision of an asteroid with
        # some object
        for asteroid in self.__asteroid_lst:
            if self.ship_collision(asteroid):
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroid_lst.remove(asteroid)
            for torpedo in self.__torpedo_lst:
                if self.torpedo_collision(asteroid,torpedo):
                    self.__screen.unregister_asteroid(asteroid)
                    self.__asteroid_lst.remove(asteroid)
            for special_tor in self.__special_torpedo_lst:
                if self.torpedo_collision(asteroid, special_tor):
                    self.__screen.unregister_asteroid(asteroid)
                    self.__asteroid_lst.remove(asteroid)

    def asteroid_movement(self, asteroid):
        """
        This method "moves" the asteroids by adjusting their location according
        to the given formula.
        :param asteroid:
        :return:
        """
        new_x = self.movement(asteroid.get_speed_x(), asteroid.get_x(),
                              self.__screen_min_x, self.__screen_max_x)
        new_y = self.movement(asteroid.get_speed_y(), asteroid.get_y(),
                              self.__screen_min_y, self.__screen_max_y)
        asteroid.set_x(new_x)
        asteroid.set_y(new_y)

    def ship_movement(self):
        """
        This method "moves" the ship by adjusting its location according
        to the given formula. The movement depends on the user's key choice.
        :return:
        """
        x = self.__ship.get_x()
        y = self.__ship.get_y()
        x_speed = self.__ship.get_speed_x()
        y_speed = self.__ship.get_speed_y()
        heading = self.__ship.get_heading()
        self.__screen.draw_ship(x, y, heading)
        new_x = self.movement(x_speed, x, self.__screen_min_x,
                              self.__screen_max_x)
        new_y = self.movement(y_speed, y, self.__screen_min_y,
                              self.__screen_max_y)
        self.__ship.set_x(new_x)
        self.__ship.set_y(new_y)
        if self.__screen.is_up_pressed():
            new_speed_x = self.acceleration_x(x_speed, heading)
            new_speed_y = self.acceleration_y(y_speed, heading)
            self.__ship.set_speed_x(new_speed_x)
            self.__ship.set_speed_y(new_speed_y)
        if self.__screen.is_right_pressed():
            self.__ship.set_heading(RIGHT_TURN)
        if self.__screen.is_left_pressed():
            self.__ship.set_heading(LEFT_TURN)

    def ship_collision(self, asteroid):
        """
        This method checks whether the asteroid has collided with the ship,
        and adjusts the ship's life accordingly, in addition to a message
        appearing on the screen and the asteroid being removed.
        :param asteroid:
        :return: bool
        """
        if asteroid.has_intersection(self.__ship):
            self.__ship.set_lives(-1)
            self.__screen.remove_life()
            title, message = AST_HIT_MSG
            self.__screen.show_message(title, message)
            return True
        return False

    def torpedo_collision(self, asteroid, torpedo):
        """
        This method checks whether the asteroid has collided with any one of
        the torpedos that have been launched and are still in the game. If the
        asteroid has collided with any of them, it adjusts the score
        accordingly and removes them both from the game.
        :param asteroid:
        :param torpedo:
        :return: bool
        """
        if asteroid.has_intersection(torpedo):
            if torpedo.is_special():
                self.__score += SCORE_FOR_SPECIAL
                self.__screen.set_score(self.__score)
                self.__screen.unregister_torpedo(torpedo)
                self.__special_torpedo_lst.remove(torpedo)
            else:
                if asteroid.get_size() == LARGE:
                    self.__score += SCORE_FOR_LARGE
                    self.__screen.set_score(self.__score)
                    self.split_asteroid(torpedo, asteroid)
                elif asteroid.get_size() == MEDIUM:
                    self.__score += SCORE_FOR_MEDIUM
                    self.__screen.set_score(self.__score)
                    self.split_asteroid(torpedo, asteroid)
                else:
                    self.__score += SCORE_FOR_SMALL
                    self.__screen.set_score(self.__score)
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedo_lst.remove(torpedo)
            return True
        return False

    def create_special_torpedo(self):
        """
        This method creates a special torpedo if the space key is pressed.
        :return:
        """
        if self.__screen.is_special_pressed():
            if len(self.__special_torpedo_lst) < MAX_SPECIAL_TORPEDO:
                special_torpedo = Torpedo(self.__ship.get_x(), 0,
                                          self.__ship.get_y(), 0,
                                          self.__ship.get_heading())
                special_torpedo.set_special()
                self.__special_torpedo_lst.append(special_torpedo)
                self.__screen.register_torpedo(special_torpedo)

    def teleport(self):
        """
        This method teleports the ship into a random location on the screen,
        only if it isn't occupied by an asteroid.
        :return:
        """
        if self.__screen.is_teleport_pressed():
            new_loc_x = random.randint(self.__screen_min_x,
                                       self.__screen_max_x)
            new_loc_y = random.randint(self.__screen_min_y,
                                       self.__screen_max_y)
            for ast in self.__asteroid_lst:
                if (ast.get_x(), ast.get_y()) == (new_loc_x, new_loc_y):
                    self.teleport()
            self.__ship.set_x(new_loc_x)
            self.__ship.set_y(new_loc_y)

    def is_game_done(self):
        """
        This method ends the game if any one of the conditions to end the game
        is met. It prints the appropriate message to the screen and exits the
        game.
        :return:
        """
        if self.__ship.get_lives() == 0:
            title, message = END_GAME_NO_LIFE
            self.__screen.show_message(title, message)
            return True
        if not len(self.__asteroid_lst):
            title, message = END_GAME_NO_ASTEROIDS
            self.__screen.show_message(title, message)
            return True
        if self.__screen.should_end():
            title, message = END_GAME_EXIT
            self.__screen.show_message(title, message)
            return True
        return False

    def split_asteroid(self, torpedo, asteroid):
        """
        This method splits the asteroid into two smaller asteroids that move in
        new, different direction at a new speed, determined by a given formula.
        :param torpedo:
        :param asteroid:
        :return:
        """
        astro_x = asteroid.get_x()
        astro_y = asteroid.get_y()
        tor_spd_x = torpedo.get_speed_x()
        tor_spd_y = torpedo.get_speed_y()
        old_size = asteroid.get_size()
        ast_spd_x = asteroid.get_speed_x()
        ast_spd_y = asteroid.get_speed_y()
        spd_x_1 = self.split_speed(tor_spd_x, ast_spd_x, ast_spd_y)
        spd_y_1 = self.split_speed(tor_spd_y, ast_spd_y, ast_spd_x)
        spd_x_2 = self.split_speed(tor_spd_x, (-1) * ast_spd_x, ast_spd_y)
        spd_y_2 = self.split_speed(tor_spd_y, (-1) * ast_spd_y, ast_spd_x)
        if old_size == LARGE:
            new_size = MEDIUM
        else:
            new_size = SMALL
        new_ast1 = Asteroid(astro_x, spd_x_1, astro_y, spd_y_1, new_size)
        new_ast2 = Asteroid(astro_x, spd_x_2, astro_y, spd_y_2, new_size)
        self.__asteroid_lst.append(new_ast1)
        self.__asteroid_lst.append(new_ast2)
        self.__screen.register_asteroid(new_ast1, new_size)
        self.__screen.register_asteroid(new_ast2, new_size)
        self.__screen.draw_asteroid(new_ast1, astro_x, astro_y)
        self.__screen.draw_asteroid(new_ast2, astro_x, astro_y)

    def split_speed(self, torpedo_speed, cur_axis_speed, alt_axis_speed):
        """
        This method is used to determine the speed of the asteroid that's
        created after the split
        :param torpedo_speed:
        :param cur_axis_speed:
        :param alt_axis_speed:
        :return: The new speed of the asteroid post-split
        """
        new_spd = (torpedo_speed + cur_axis_speed) \
                  / math.sqrt((cur_axis_speed ** 2) + (alt_axis_speed ** 2))
        return new_spd

    def create_torpedo(self):
        """
        This method creates a new torpedo object if the screen key is pressed.
        :return: the Torpedo
        """
        if self.__screen.is_space_pressed():
            if len(self.__torpedo_lst) < MAX_TORPEDO_NUM:
                # tor = self.create_torpedo()

                loc_x = self.__ship.get_x()
                loc_y = self.__ship.get_y()
                heading = self.__ship.get_heading()
                new_speed_x = (self.__ship.get_speed_x() +
                               (2 * (math.cos(self.radian(heading)))))
                new_speed_y = (self.__ship.get_speed_y() +
                               (2 * (math.sin(self.radian(heading)))))
                tor = Torpedo(loc_x, new_speed_x, loc_y, new_speed_y, heading)
                self.__torpedo_lst.append(tor)
                self.__screen.register_torpedo(tor)

    def torpedo_movement(self, torpedo):
        """
        This method "moves" the Torpedo by changing it's coordinates
        according to the given formula. it also checks for the torpedo's
        lifetime, and in case it has met it, the torpedo is removed.
        :param torpedo:
        :return:
        """
        new_x = self.movement(torpedo.get_speed_x(), torpedo.get_x(),
                              self.__screen_min_x, self.__screen_max_x)
        new_y = self.movement(torpedo.get_speed_y(), torpedo.get_y(),
                              self.__screen_min_y, self.__screen_max_y)
        torpedo.set_x(new_x)
        torpedo.set_y(new_y)
        self.__screen.draw_torpedo(torpedo, torpedo.get_x(), torpedo.get_y(),
                                   torpedo.get_heading())
        if torpedo.get_lifetime() >= MAX_TOR_LIFETIME:
            self.__screen.unregister_torpedo(torpedo)
            self.__torpedo_lst.remove(torpedo)
        elif torpedo.get_lifetime() >= MAX_SPECIAL_TOR_LIFETIME and\
                torpedo.is_special():
                self.__screen.unregister_torpedo(torpedo)
                self.__special_torpedo_lst.remove(torpedo)
        else:
            torpedo.set_lifetime()

    def movement(self, speed, old_coord, min_coord, max_coord):
        """
        This method is used to determine movement of objects in the game by
        reflecting the movement formula.
        :param speed:
        :param old_coord:
        :param min_coord:
        :param max_coord:
        :return: new coordinate
        """
        delta_axis = max_coord - min_coord
        new_coord = ((speed + old_coord - min_coord) % delta_axis) + min_coord
        return new_coord

    def acceleration_x(self, speed, heading):
        """
        This method determines the x- axis acceleration of the ship object in
        the game space and returns it's new speed
        :param speed:
        :param heading:
        :return:
        """
        new_speed = speed + (math.cos(self.radian(heading)))
        return new_speed

    def acceleration_y(self, speed, heading):
        """
        This method determines the y- axis acceleration of the ship object in
        the game space and returns it's new speed
        :param speed:
        :param heading:
        :return:
        """
        new_speed = speed + math.sin(self.radian(heading))
        return new_speed

    def radian(self, heading):
        """
        This method converts degrees into radians
        :param heading:
        :return: num of radians
        """
        return (heading * math.pi) / DEG_IN_PIE


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(ASTEROIDS_NUM)
