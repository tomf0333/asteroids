import math

DEFAULT_RADIUS = 4
DEFAULT_LIFE = 200
DEFAULT_SP_LIFE = 150
HALF_TURN = 45


class Torpedo:
    """
    the class representing the torpedoes in the game asteroids,
    they each have speed and location on x and on the y axis and direction.
    """
    def __init__(self, x_location=0, x_speed=0, y_location=0, y_speed=0,
                 direction=0, special=False):
        self.__x_location = x_location
        self.__x_speed = x_speed
        self.__y_location = y_location
        self.__y_speed = y_speed
        self.__direction = direction
        self.__radius = DEFAULT_RADIUS
        self.__special = special
        if special:
            self.__torpedo_life = DEFAULT_SP_LIFE
        else:
            self.__torpedo_life = DEFAULT_LIFE

    def hurt_torpedo(self):
        """
        decrease torpedo life by one.
        :return: if it is dead (0 life) return False else return True.
        """
        if self.__torpedo_life <= 0:
            return False
        self.__torpedo_life -= 1
        return True

    # Getters
    def get_x_location(self):
        return self.__x_location

    def get_y_location(self):
        return self.__y_location

    def get_x_speed(self):
        return self.__x_speed

    def get_y_speed(self):
        return self.__y_speed

    def get_direction(self):
        return self.__direction

    def get_radius(self):
        return self.__radius

    def get_life(self):
        return self.__torpedo_life

    def get_special(self):
        return self.__special

    # Setters
    def set_x_location(self, new_x):
        self.__x_location = new_x

    def set_y_location(self, new_y):
        self.__y_location = new_y

    def set_x_speed(self, new_speed):
        self.__x_speed = new_speed

    def set_y_speed(self, new_speed):
        self.__y_speed = new_speed

    def set_direction(self, new_direction):
        self.__direction = new_direction

    def set_life(self, new_life):
        self.__torpedo_life = new_life