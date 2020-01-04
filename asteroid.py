DEFAULT_SIZE = 3


class Asteroid:
    """
    the class that represents the asteroids in the game asteroids,
    they each have speed and location on x and on the y axis and a size.
    """
    def __init__(self, x_location=0, x_speed=0, y_location=0, y_speed=0,
                 asteroid_size=DEFAULT_SIZE):
        self.__x_location = x_location
        self.__x_speed = x_speed
        self.__y_location = y_location
        self.__y_speed = y_speed
        self.__asteroid_size = asteroid_size
        self.__radius = asteroid_size * 10 - 5

    def has_intersection(self, obj):
        distance = ((obj.get_x_location() - self.__x_location) ** 2 +
                    (obj.get_y_location() - self.__y_location) ** 2) ** 0.5
        if distance <= self.__radius + obj.get_radius():
            return True
        return False

    # Getters
    def get_size(self):
        return self.__asteroid_size

    def get_x_location(self):
        return self.__x_location

    def get_y_location(self):
        return self.__y_location

    def get_x_speed(self):
        return self.__x_speed

    def get_y_speed(self):
        return self.__y_speed

    def get_radius(self):
        return self.__radius

    # Setters
    def set_size(self, new_size):
        self.__asteroid_size = new_size

    def set_x_location(self, new_x):
        self.__x_location = new_x

    def set_y_location(self, new_y):
        self.__y_location = new_y