DEFAULT_RADIUS = 1
DEFAULT_LIVES = 3


class Ship:
    """
    the class representing spaceships for the game asteroids,
    they each have speed and location on x and on the y axis and a direction.
    """
    def __init__(self, x_location=0, y_location=0, x_speed=0, y_speed=0,
                 direction=0):
        self.__x_location = x_location
        self.__x_speed = x_speed
        self.__y_location = y_location
        self.__y_speed = y_speed
        self.__direction = direction
        self.__radius = DEFAULT_RADIUS
        self.__lives = DEFAULT_LIVES

    def ship_hit(self):
        self.__lives -= 1

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

    def get_lives(self):
        return self.__lives

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