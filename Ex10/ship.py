RADIUS = 1
START_LIVES = 3


class Ship:
    """
    This class defines the Ship object in the game. it contains several
    methods regarding that object
    """
    def __init__(self, location_x, speed_x, location_y, speed_y, heading):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__heading = heading
        self.__radius = RADIUS
        self.__lives = START_LIVES

    def get_x(self):
        """
        :return: The x-axis location of the ship
        """
        return self.__location_x

    def set_x(self, x):
        """
        This method changes the x-axis coordinate of the ship
        :param x:
        :return:
        """
        self.__location_x = x

    def get_speed_x(self):
        """
        :return: The x-axis speed of the ship
        """
        return self.__speed_x

    def set_speed_x(self, speed):
        """
        This method changes the x-axis speed of the ship to a given speed
        :param speed:
        :return:
        """
        self.__speed_x = speed

    def get_y(self):
        """
        :return: The y-axis location of the ship
        """
        return self.__location_y

    def set_y(self, y):
        """
        This method changes the y-axis coordinate of the ship
        :param y: new coordinate
        :return:
        """
        self.__location_y = y

    def get_speed_y(self):
        """
        :return: The y-axis speed of the ship
        """
        return self.__speed_y

    def set_speed_y(self, speed):
        """
        This method changes the y-axis speed of the ship
        :param speed:
        :return:
        """
        self.__speed_y = speed

    def get_heading(self):
        """
        :return: Heading of ship
        """
        return self.__heading

    def set_heading(self, deg):
        """
        Changes the heading of the ship by a given number of degrees
        :param deg:
        :return:
        """
        self.__heading += deg

    def get_radius(self):
        """
        :return: Radius of ship
        """
        return self.__radius

    def get_lives(self):
        """
        :return: number of lives of the ship
        """
        return self.__lives

    def set_lives(self, change):
        """
        Changes the number of lives of the ship
        :param change:
        :return:
        """
        self.__lives += change



