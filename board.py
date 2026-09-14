import numpy
import player

from typing import NamedTuple

class Location(NamedTuple):
    row: int
    column: int

class Board:
    """
    Manages the game board for Chinese Checkers.
    """
    def __init__(self, rows: int = 17, columns: int = 25,) -> None:
        self.__rows: int = rows
        self.__columns: int = columns
        self.__board: list[list[player.Color]] = []

    def is_valid_location(self, location: Location) -> bool:
        """
        Checks if a location is valid on the board.
        """
        return (
            0 <= location.row < self.__rows
            and 0 <= location.column < self.__columns
            and self.__board[location.row][location.column] != player.Color.OUT_OF_BOARD
        )

    def set_board(self):
        """
        Initializes the board with player colors and empty spaces.
        """
        board = numpy.full((17, 25), player.Color.OUT_OF_BOARD)
        matrix_rows = [1, 2, 3, 4, 13, 12, 11, 10, 9]
        for i in range(len(matrix_rows)):
            column = 12
            first_time = True
            while matrix_rows[i] > 0:
                if (i % 2 == 0) and first_time: #before it need to be for 2 sides
                    first_time = False
                    # print(i,j)
                    board[i][column] = board[16 - i][column] = player.Color.BLANK

                    matrix_rows[i] -= 1
                else:
                    column -= 1 #odd column
                    board[i][column] = board[i][24 - column] = board[16 - i][column] = board[16 - i][24 - column] = player.Color.BLANK
                    matrix_rows[i] -= 2 #we put to for each side
                column -= 1
        self.__board = board

    def get_board(self):
        """
        Retrieves the current state of the board.
        """
        return self.__board








