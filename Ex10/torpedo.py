RADIUS = 4
LIFETIME = 0


class Torpedo:
    """
    This class defines the Torpedo objects in the game. it contains several
    methods regarding those objects
    """
    def __init__(self, location_x, speed_x, location_y, speed_y, heading):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__heading = heading
        self.__radius = RADIUS
        self.__lifetime = LIFETIME
        self.__is_special = False

    def get_x(self):
        """
        :return:  The x-axis location of the Torpedo
        """
        return self.__location_x

    def set_x(self, x):
        """
        This method changes the x-axis coordinate of the Torpedo
        :param x: new coordinate
        :return:
        """
        self.__location_x = x

    def get_speed_x(self):
        """
        :return: The x-axis speed of the Torpedo
        """
        return self.__speed_x

    def set_speed_x(self, speed):
        """
        This method changes the x-axis speed of the Torpedo to a given speed
        :param speed:
        :return:
        """
        self.__speed_x = speed

    def get_y(self):
        """
        :return: The y-axis location of the Torpedo
        """
        return self.__location_y

    def set_y(self, y):
        """
        This method changes the y-axis coordinate of the Torpedo
        :param y: new coordinate
        :return:
        """
        self.__location_y = y

    def get_speed_y(self):
        """
        :return: The y-axis speed of the Torpedo
        """
        return self.__speed_y

    def set_speed_y(self, speed):
        """
        This method changes the y-axis speed of the Torpedo
        :param speed:
        :return:
        """
        self.__speed_y = speed

    def get_heading(self):
        """
        :return: Heading of Torpedo
        """
        return self.__heading

    def set_heading(self, deg):
        """
        Changes the heading of the Torpedo by a given number of degrees
        :param deg:
        :return:
        """
        self.__heading += deg

    def get_radius(self):
        """
        :return: Radius of Torpedo
        """
        return self.__radius

    def get_lifetime(self):
        """
        :return: number of lifecycles of Torpedo
        """
        return self.__lifetime

    def set_lifetime(self):
        """
        Increases the number of lifecycles of a Torpedo by 1.
        :return:
        """
        self.__lifetime += 1

    def is_special(self):
        """
        :return: bool
        """
        return self.__is_special

    def set_special(self):
        """
        :return: Converts a created Torpedo into a special one
        """
        self.__is_special = True
