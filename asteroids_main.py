from screen import Screen
import random
import math
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys

DEFAULT_ASTEROIDS_NUM = 5
DEFAULT_ASTEROID_SIZE = 3
MAX_TORPEDOES = 10
MAX_SP_TORPEDOES = 5
SPLIT_TIME = 30
BOOM_FACTOR = 1
SPEED_ACCELERATE = 2
WIN_TITLE = "WE HAVE A WINNER"
WIN_MESSAGE = "you did it man... or woman... women can be spaceship " \
              "drivers too i guess...\nyour score is: "
LOSE_TITLE = "LOOOOOOOOSER"
LOSE_MESSAGE = "oh snap you lost, those asteroids sure showed you\nyour " \
               "score is: "
WIMP_COUGH_TITLE = "ESCAPED CERTAIN DOOM"
WIMP_COUGH_MESSAGE = "don't worry about it, you did your best\nyour score " \
                     "is: "
HIT_TITLE = "!&*DANGER HIT DANGER*&!"
HIT_MESSAGE = "you seem to have made a booboo"
BIG = 3
BIG_SCORE = 20
MEDIUM = 2
MEDIUM_SCORE = 50
SMALL = 1
SMALL_SCORE = 100
RANDOM_MIN = -500
RANDOM_MAX = 501
ASTEROID_MIN_SPEED = 1
ASTEROID_MAX_SPEED = 4
RIGHT = -7
LEFT = 7
DELTA_X = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X
DELTA_Y = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroid_list = list()
        self.__torpedo_list = list()
        self.__ship = Ship()
        self.__initialize_ship()
        self.__score = 0
        self.__special_list = list()
        for asteroid_num in range(asteroids_amount):
            self.__initialize_asteroid()
        for asteroid in self.__asteroid_list:
            self.__screen.register_asteroid(asteroid, asteroid.get_size())
            self.__screen.draw_asteroid(asteroid, asteroid.get_x_location(),
                                        asteroid.get_y_location())

    def __initialize_ship(self):
        """
        creates the ship on the screen.
        """
        good, ship_start_x, ship_start_y = \
            self.__get_random_location_not_asteroid()
        self.__ship = Ship(ship_start_x, ship_start_y)
        self.__screen.draw_ship(ship_start_x, ship_start_y, 0)

    def __initialize_asteroid(self):
        """
        creates the asteroids on the screen.
        makes sure that an asteroid can't be created on a ship.
        """
        # Initial random coordinates
        asteroid_start_x, asteroid_start_y = \
            self.__get_random_location_not_ship()
        asteroid_speed_x = random.randint(ASTEROID_MIN_SPEED,
                                          ASTEROID_MAX_SPEED)
        asteroid_speed_y = random.randint(ASTEROID_MIN_SPEED,
                                          ASTEROID_MAX_SPEED)
        new_asteroid = Asteroid(asteroid_start_x, asteroid_speed_x,
                                asteroid_start_y, asteroid_speed_y,
                                DEFAULT_ASTEROID_SIZE)
        self.__asteroid_list.append(new_asteroid)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 3)

    def _game_loop(self):
        """
        loops over every aspect of the game,
        redraws every object (ship, asteroids, torpedoes) as the game goes,
        checks every input and acts accordingly.
        because we work in the passive way of programming here, this function
        is run at small intervals and each time 'tastes' the program, then
        it acts according to what it needed to do, this is why all the methods
        are run one after the after regardless of input (it checks input
        inside them instead).
        """
        # Add ship to the screen
        self.__screen.draw_ship(self.__ship.get_x_location(),
                                self.__ship.get_y_location(),
                                self.__ship.get_direction())
        # Add the asteroids to the screen
        for asteroid in self.__asteroid_list:
            self.__screen.draw_asteroid(asteroid, asteroid.get_x_location(),
                                        asteroid.get_y_location())
        # Adds the torpedoes to the screen
        for torpedo in self.__torpedo_list:
            self.__screen.draw_torpedo(torpedo, torpedo.get_x_location(),
                                       torpedo.get_y_location(),
                                       torpedo.get_direction())
        # All the methods for every input possible in the game
        self.__ship_spin()
        self.__ship_speedup()
        self.__check_hit()
        self.__fire()
        self.__move_objects()
        self.__torpedo_death()
        self.__teleport()
        self.__super_shot()
        self.__end_game()

    def __count_normal_torpedoes(self):
        """
        counts the number of non special torpedoes.
        :return: the number of normal torpedoes.
        """
        counter = 0
        for torpedo in self.__torpedo_list:
            if not torpedo.get_special():
                counter += 1
        return counter

    def __super_shot(self):
        """
        creates a super shot that splits into two torpedoes every few seconds.
        :return:
        """
        special_list = list()
        for torpedo in self.__torpedo_list:
            if torpedo.get_special():
                special_list.append(torpedo)
        for torpedo in special_list:
            if torpedo.get_life() % SPLIT_TIME == 0 and torpedo.get_life() != 0:
                self.__split(torpedo)

    def __split(self, torpedo):
        """
        this method receives a torpedo and splits it to two new ones.
        :param torpedo: (torpedo) the torpedo we split.
        """
        torpedo1 = Torpedo(torpedo.get_x_location(), torpedo.get_x_speed(),
                           torpedo.get_y_location(), torpedo.get_y_speed(),
                           torpedo.get_direction(), True)
        torpedo2 = Torpedo(torpedo.get_x_location(), torpedo.get_x_speed(),
                           torpedo.get_y_location(), torpedo.get_y_speed(),
                           torpedo.get_direction(), True)
        torpedo1.set_x_speed(torpedo1.get_x_speed() + BOOM_FACTOR)
        torpedo2.set_y_speed(torpedo2.get_y_speed() + BOOM_FACTOR)
        torpedo1.set_life(torpedo.get_life())
        torpedo2.set_life(torpedo.get_life())
        self.__torpedo_list.append(torpedo1)
        self.__torpedo_list.append(torpedo2)
        self.__screen.register_torpedo(torpedo1)
        self.__screen.register_torpedo(torpedo2)

    def __teleport(self):
        """
        teleports the ship if the right key is pressed
        """
        if self.__screen.is_teleport_pressed():
            good, new_x, new_y = self.__get_random_location_not_asteroid()
            while good is False:
                good, new_x, new_y = self.__get_random_location_not_asteroid()
            self.__ship.set_x_location(new_x)
            self.__ship.set_y_location(new_y)

    def __get_random_location_not_ship(self):
        """
        gets a random x and y location for an asteroid.
        makes sure it isn't the location of the ship.
        :return: the new x, y coordinates.
        """
        new_x = random.randint(RANDOM_MIN, RANDOM_MAX)
        new_y = random.randint(RANDOM_MIN, RANDOM_MAX)
        while self.__ship.get_x_location() == new_x and \
                self.__ship.get_y_location() == new_y:
            new_x = random.randint(RANDOM_MIN, RANDOM_MAX)
            new_y = random.randint(RANDOM_MIN, RANDOM_MAX)
        return new_x, new_y

    def __get_random_location_not_asteroid(self):
        """
        gets a random x and y location for the ship.
        makes sure it isn't close to any asteroid.
        :return: True if the location is good and False otherwise, regardless
        it also returns the x and y location.
        """
        new_x, new_y = self.__get_random_location_not_ship()
        temp_ship = Ship(new_x, new_y)
        for asteroid in self.__asteroid_list:
            if asteroid.has_intersection(temp_ship):
                return False, new_x, new_y
        return True, new_x, new_y

    def __end_game(self):
        """
        the method that checks to see if the game should end and sends
        appropriate message for each possible end.
        """
        end = False
        if not self.__asteroid_list:
            self.__screen.show_message(WIN_TITLE, WIN_MESSAGE +
                                       (str(self.__score)))
            end = True
        if self.__ship.get_lives() == 0:
            self.__screen.show_message(LOSE_TITLE, LOSE_MESSAGE +
                                       (str(self.__score)))
            end = True
        if self.__screen.should_end():
            self.__screen.show_message(WIMP_COUGH_TITLE, WIMP_COUGH_MESSAGE +
                                       (str(self.__score)))
            end = True
        if end:
            self.__screen.end_game()
            sys.exit()

    def __torpedo_death(self):
        """
        activates method in torpedo that 'hurts' the torpedo and if it is dead
        it mourns its loss and moves on by deleting it from the screen.
        """
        for torpedo in self.__torpedo_list:
            if not torpedo.hurt_torpedo():
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedo_list.remove(torpedo)
                if torpedo in self.__special_list:
                    self.__special_list.remove(torpedo)

    def __move_objects(self):
        """
        moves the objects on the screen.
        """
        # Ship
        move_in_y(self.__ship)
        move_in_x(self.__ship)

        # Asteroids
        for asteroid in self.__asteroid_list:
            move_in_x(asteroid)
            move_in_y(asteroid)

        # Torpedoes
        for torpedo in self.__torpedo_list:
            move_in_x(torpedo)
            move_in_y(torpedo)

    def __fire(self):
        """
        a method that adds the torpedo to the screen.
        """
        torpedo_x_speed = x_speed_calc(self.__ship.get_x_speed(),
                                       self.__ship.get_direction())
        torpedo_y_speed = y_speed_calc(self.__ship.get_y_speed(),
                                       self.__ship.get_direction())
        if self.__screen.is_space_pressed() and \
                self.__count_normal_torpedoes() < MAX_TORPEDOES:
            torpedo = Torpedo(self.__ship.get_x_location(), torpedo_x_speed,
                              self.__ship.get_y_location(), torpedo_y_speed,
                              self.__ship.get_direction())
            self.__torpedo_list.append(torpedo)
            self.__screen.register_torpedo(torpedo)
            self.__screen.draw_torpedo(torpedo, torpedo.get_x_location(),
                                       torpedo.get_y_location(),
                                       torpedo.get_direction())
        if self.__screen.is_special_pressed() and \
                len(self.__special_list) < MAX_SP_TORPEDOES:
            torpedo = Torpedo(self.__ship.get_x_location(), torpedo_x_speed,
                              self.__ship.get_y_location(), torpedo_y_speed,
                              self.__ship.get_direction(), True)
            self.__torpedo_list.append(torpedo)
            self.__screen.register_torpedo(torpedo)
            self.__screen.draw_torpedo(torpedo, torpedo.get_x_location(),
                                       torpedo.get_y_location(),
                                       torpedo.get_direction())
            self.__special_list.append(torpedo)

    def __check_hit(self):
        """
        this method checks if the ship hit an asteroid.
        """
        for asteroid in self.__asteroid_list:
            if asteroid.has_intersection(self.__ship):
                self.__ship.ship_hit()
                self.__screen.show_message(HIT_TITLE, HIT_MESSAGE)
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroid_list.remove(asteroid)
            for torpedo in self.__torpedo_list:
                if asteroid.has_intersection(torpedo):
                    self.__create_smaller_asteroids(asteroid, torpedo)
                    if asteroid.get_size() == BIG:
                        self.__score += BIG_SCORE
                    elif asteroid.get_size() == MEDIUM:
                        self.__score += MEDIUM_SCORE
                    elif asteroid.get_size() == SMALL:
                        self.__score += SMALL_SCORE
                    self.__screen.set_score(self.__score)
                    break

    def __create_smaller_asteroids(self, asteroid, torpedo):
        """
        splits the asteroid that was hit with a torpedo to 2 if its size is 2
        or 3, and sends each one in a new direction, and if it is one then
        just remove it.
        :param asteroid: (asteroid) the asteroid that we split or remove
        """
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroid_list.remove(asteroid)
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedo_list.remove(torpedo)
        if torpedo in self.__special_list:
            self.__special_list.remove(torpedo)
        if asteroid.get_size() > 1:
            negetive_x_speed = -1 * asteroid.get_x_speed()
            negetive_y_speed = -1 * asteroid.get_y_speed()
            # First asteroid (positive speed)
            new_x_speed_1 = torpedo.get_x_speed() + asteroid.get_x_speed() / \
                            (((asteroid.get_x_speed()) ** 2) +
                             ((asteroid.get_y_speed()) ** 2) ** 0.5)
            new_y_speed_1 = torpedo.get_y_speed() + asteroid.get_y_speed() / \
                            (((asteroid.get_x_speed()) ** 2) +
                             ((asteroid.get_y_speed()) ** 2) ** 0.5)
            # Second asteroid (negetive speed)
            new_x_speed_2 = torpedo.get_x_speed() + negetive_x_speed / \
                            ((negetive_x_speed ** 2) + (
                                        negetive_y_speed ** 2) ** 0.5)
            new_y_speed_2 = torpedo.get_y_speed() + negetive_y_speed / \
                            ((negetive_x_speed ** 2) + (
                                        negetive_y_speed ** 2) ** 0.5)
            asteroid1 = Asteroid(asteroid.get_x_location(), new_x_speed_1,
                                 asteroid.get_y_location(), new_y_speed_1,
                                 asteroid.get_size() - 1)
            asteroid2 = Asteroid(asteroid.get_x_location(), new_x_speed_2,
                                 asteroid.get_y_location(), new_y_speed_2,
                                 asteroid.get_size() - 1)
            self.__screen.register_asteroid(asteroid1, asteroid1.get_size())
            self.__screen.register_asteroid(asteroid2, asteroid2.get_size())
            self.__asteroid_list.append(asteroid1)
            self.__asteroid_list.append(asteroid2)

    def __ship_spin(self):
        """
        spins the ship right if right is pressed and left if left is pressed.
        """
        if self.__screen.is_left_pressed():
            spin_left(self.__ship)
        if self.__screen.is_right_pressed():
            spin_right(self.__ship)

    def __ship_speedup(self):
        """
        speeds up the ship in both axises.
        """
        if self.__screen.is_up_pressed():
            # Set X axis speed
            new_speed_x = self.__ship.get_x_speed() + \
                          math.cos(math.radians(self.__ship.get_direction()))
            self.__ship.set_x_speed(new_speed_x)
            # Set Y axis speed
            new_speed_y = self.__ship.get_y_speed() + \
                          math.sin(math.radians(self.__ship.get_direction()))
            self.__ship.set_y_speed(new_speed_y)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


def x_speed_calc(x_speed, direction):
    return x_speed + SPEED_ACCELERATE * math.cos(math.radians(direction))


def y_speed_calc(y_speed, direction):
    return y_speed + SPEED_ACCELERATE * math.sin(math.radians(direction))


def move_in_x(object):
    """
    moves given object in the X axis using the formula.
    :param object: an object that wants to move (can be ship/asteroid/torpedo)
    """
    object.set_x_location((object.get_x_speed() + object.get_x_location() -
                           Screen.SCREEN_MIN_X) % DELTA_X +
                          Screen.SCREEN_MIN_X)


def move_in_y(object):
    """
    moves given object in the Y axis using the formula.
    :param object: an object that wants to move (can be ship/asteroid/torpedo)
    """
    object.set_y_location((object.get_y_speed() + object.get_y_location() -
                           Screen.SCREEN_MIN_Y) % DELTA_Y +
                          Screen.SCREEN_MIN_Y)


def spin_right(object, times=1):
    """
    spins the object 7 degrees to the right.
    :param object: an object that wants to spin (can be ship/torpedo)
    """
    for time in range(times):
        object.set_direction(object.get_direction() + RIGHT)


def spin_left(object, times=1):
    """
    spins the object 7 degrees to the left.
    :param object: an object that wants to spin (can be ship/torpedo)
    """
    for time in range(times):
        object.set_direction(object.get_direction() + LEFT)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
