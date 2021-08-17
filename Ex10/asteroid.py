import math


class Asteroid:
    """
    This class defines the Asteroid objects in the game. it contains several
    methods regarding those objects
    """

    def __init__(self, location_x, speed_x, location_y, speed_y, size):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__size = size
        self.__radius = (self.__size * 10) - 5

    def get_x(self):
        """
        :return: The x-axis location of the Asteroid
        """
        return self.__location_x

    def get_y(self):
        """
        :return: The y-axis location of the Asteroid
        """
        return self.__location_y

    def get_size(self):
        """
        :return: The size of the Asteroid
        """
        return self.__size

    def set_size(self):
        """
        Changes the size of the Asteroid
        :return:
        """
        return self.__size

    def get_speed_x(self):
        """
        :return: The x-axis speed of the Asteroid
        """
        return self.__speed_x

    def get_speed_y(self):
        """
        :return: The y-axis speed of the Asteroid
        """
        return self.__speed_y

    def set_x(self, x):
        """
        Changes the x-axis coordinates of the Asteroid
        :param x:
        :return:
        """
        self.__location_x = x

    def set_y(self, y):
        """
        Changes the y-axis coordinates of the Asteroid
        :param y:
        :return:
        """
        self.__location_y = y

    def get_radius(self):
        """
        :return: Radius of Asteroid
        """
        return self.__radius

    def has_intersection(self, obj):
        """
        This method determines whether the asteroid has collided with another
        object in the game space.
        :param obj:
        :return: bool
        """
        obj.x = obj.get_x()
        obj.y = obj.get_y()
        distance = math.sqrt(((obj.x - self.__location_x) ** 2) +
                             ((obj.y - self.__location_y) ** 2))
        if distance <= (self.__radius + obj.get_radius()):
            return True
        else:
            return False




