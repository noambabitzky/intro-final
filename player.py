from enum import Enum

class Player:
    """
    Represents a player in the game.
    """

    def __init__(self, color, name):
        """
        Initializes a Player object with the specified color and name.
        Args:
            color (Color): The color of the player's game pieces.
            name (str): The name of the player.
        """
        self.__color = color
        self.__name = name
        self.__losses = 0
        self.__wins = 0

    def add_losses(self):
        """
        Increments the number of losses for the player.
        """
        self.__losses += 1

    def add_wins(self):
        """
        Increments the number of wins for the player.
        """
        self.__wins += 1

    def get_color(self):
        """
        Returns the color of the player's game pieces.
        Returns:
            Color: The color of the player.
        """
        return self.__color

    def get_name(self):
        """
        Returns the name of the player.
        Returns:
            str: The name of the player.
        """
        return self.__name

    def get_losses(self):
        """
        Returns the number of losses for the player.
        Returns:
            int: The number of losses.
        """
        return self.__losses

    def get_wins(self):
        """
        Returns the number of wins for the player.
        Returns:
            int: The number of wins.
        """
        return self.__wins


class Color(Enum):
    """
    Enum representing colors for game pieces.
    """
    OUT_OF_BOARD = "out_of_board"
    BLANK = "lightgrey"
    AZURE = "cyan"
    BLUE = "steelblue"
    YELLOW = "gold"
    ORANGE = "salmon"
    GREEN = "lightgreen"
    PURPLE = "orchid"
