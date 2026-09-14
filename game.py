import random

from pygame import color

import board
import player
from typing import NamedTuple


class DummyAutoPlayer(player.Player):
    pass


class Location(NamedTuple):
    row: int
    column: int


class Game:
    """
    Class for managing the Chinese Checkers game.
    """

    def __init__(self, num_of_players, board: board.Board,) -> None:
        """
        Initializes the game with the specified number of players and the game board.

        Args:
        - num_of_players: Number of players in the game.
        - board: The game board object.
        """
        self.__players : list[player.Player] = []
        self.__board = board
        self.__color_locations = dict()
        self.__aim_of_players: dict[player.Color, list[Location]] = dict()
        self.__num_of_players = num_of_players
        self.__start_again = False
        self.__game_over = False

    def set_game_over(self, game_over: bool) -> None:
        self.__game_over = game_over

    def get_game_over(self) -> bool:
        return self.__game_over

    def get_aim(self, player_color):
        return self.__aim_of_players[player_color]

    def get_start_again(self) -> bool:
        """
        Gets the start_again attribute.

        Returns:
        - bool: True if the game should start again, False otherwise.
        """
        return self.__start_again

    def set_start_again(self, start_again: bool) -> None:
        """
        Sets the start_again attribute.

        Args:
        - start_again: Boolean value indicating whether the game should start again.
        """
        self.__start_again = start_again

    def valid_moves(self, location):
        """
        Finds valid moves for a given location on the board.

        Args:
        - location: The location for which valid moves are to be found.

        Returns:
        - list: List of valid move locations.
        """
        list1 = []
        one_steps = self.find_one_step(location)
        for step in one_steps:
            list1.append(step)
        dilugs_list = []
        self.explore_dilugs(location, dilugs_list=dilugs_list)
        for dilug in dilugs_list:
            list1.append(dilug)
        return list1

    def explore_dilugs(self, location, visited=None, dilugs_list=None):
        """
        Explores all possible diagonal jumps (dilugs) from a given location recursively.

        Args:
        - location: The starting location to explore dilugs from.
        - visited: Set of visited locations to prevent revisiting the same location.
        - dilugs_list: List to store the found dilugs.

        Returns:
        - None
        """
        if visited is None:
            visited = set()
        if dilugs_list is None:
            dilugs_list = []

        visited.add(location)
        dilugs = self.find_dilug(location)
        for dilug in dilugs:
            if dilug not in visited:
                dilugs_list.append(dilug)
                self.explore_dilugs(dilug, visited, dilugs_list)

    def find_one_step(self, location):
        """
        Finds valid one-step moves from a given location on the board.

        Args:
        - location: The location for which one-step moves are to be found.

        Returns:
        - list: List of valid one-step move locations.
        """
        optional_locations: list[Location] = [
            Location(row=location.row, column=location.column + 2),
            Location(row=location.row, column=location.column - 2),
            Location(row=location.row + 1, column=location.column + 1),
            Location(row=location.row + 1, column=location.column - 1),
            Location(row=location.row - 1, column=location.column + 1),
            Location(row=location.row - 1, column=location.column - 1),
        ]

        return [
            optional_location
            for optional_location in optional_locations
            if (
                    self.is_valid_location(optional_location)
                    and self.__board.get_board()[optional_location.row][optional_location.column] == player.Color.BLANK
            )
        ]

    def find_dilug(self,location):
        """
        Finds valid diagonal jump (dilug) moves from a given location on the board.

        Args:
        - location: The location for which dilug moves are to be found.

        Returns:
        - list: List of valid dilug move locations.
        """
        optional_locations: list[Location] = [
            Location(row=location.row, column=location.column + 4),
            Location(row=location.row, column=location.column - 4),
            Location(row=location.row + 2, column=location.column + 2),
            Location(row=location.row + 2, column=location.column - 2),
            Location(row=location.row - 2, column=location.column + 2),
            Location(row=location.row - 2, column=location.column - 2),
        ]

        valid_location = []
        for optional_location in optional_locations:
            if self.is_valid_location(optional_location):
                middle_cell_location = Location(row=int((location.row + optional_location.row) / 2), column=int((location.column + optional_location.column) / 2))
                target_cell_color = self.__board.get_board()[optional_location.row][optional_location.column]
                middle_cell_color = self.__board.get_board()[middle_cell_location.row][middle_cell_location.column]
                if (
                        self.is_valid_location(optional_location)
                        and target_cell_color == player.Color.BLANK
                        and middle_cell_color != player.Color.BLANK
                        and middle_cell_color != self.__board.get_board()[location.row][location.column]):

                    valid_location.append(optional_location)
        return valid_location

    def is_valid_location(self, location) -> bool:
        """
        Checks if a given location is valid on the game board.

        Args:
        - location: The location to check for validity.

        Returns:
        - bool: True if the location is valid, False otherwise.
        """
        return (
                0 <= location.row < 17
                and 0 <= location.column < 25
                and self.__board.get_board()[location.row][location.column] != player.Color.OUT_OF_BOARD)

    def game_ended(self, color: player.Color) -> bool:
        """
        Checks if the game has ended for a specific player color.

        Args:
        - color: The player color to check for game end.

        Returns:
        - bool: True if the game has ended for the player color, False otherwise.
        """
        return sorted(self.__color_locations[color]) == sorted(self.__aim_of_players[color])

    def update_wins_and_losses(self, winner: player.Player) -> None:
        """
        Updates the wins and losses for players after a game ends.

        Args:
        - winner: The winning player.

        Returns:
        - None
        """
        for player_play in self.__players:
            if player_play == winner:
                player_play.add_wins()
            else:
                player_play.add_losses()

    def add_player(self, list_names):
        """
        Adds players to the game based on provided names.

        Args:
        - list_names: List of player names.

        Returns:
        - None
        """
        for i in range(1, self.__num_of_players + 1):
            valid = False
            while not valid:
                random_color = random.choice(list(player.Color))
                valid = True
                for j in self.__players:
                    if j.get_color() == random_color:
                        valid = False
                if random_color == player.Color.BLANK or random_color == player.Color.OUT_OF_BOARD :
                    valid = False
            player_color = player.Color(random_color)
            player_new = player.Player(player_color, list_names[i-1])
            for j in range(1, 7):
                name= f"computerPlayer{j}"
                if list_names[i-1] == name:
                    player_new = DummyAutoPlayer(player_color, list_names[i-1])
            self.__players.append(player_new)

    def set_source_aim_of_players(self):
        """
        Sets the source and aim locations for each player based on the number of players.

        Returns:
        - None
        """
        if len(self.__players) == 2:
            self.__color_locations[self.__players[0].get_color()] = [Location(0, 12), Location(1, 11), Location(1, 13), Location(2, 10) ,Location(2, 12), Location(2, 14), Location(3, 9), Location(3, 11), Location(3, 13),Location(3, 15)]
            self.__aim_of_players[self.__players[0].get_color()] = [Location(16, 12), Location(15, 11), Location(15, 13), Location(14, 10),Location(14, 12), Location(14, 14), Location(13, 9), Location(13, 11),Location(13, 13), Location(13, 15)]
            self.__color_locations[self.__players[1].get_color()] = [Location(16, 12), Location(15, 11), Location(15, 13), Location(14, 10), Location(14, 12), Location(14, 14), Location(13, 9), Location(13, 11), Location(13, 13), Location(13, 15)]
            self.__aim_of_players[self.__players[1].get_color()] = [Location(0, 12), Location(1, 11), Location(1, 13), Location(2, 10) ,Location(2, 12), Location(2, 14), Location(3, 9), Location(3, 11), Location(3, 13),Location(3, 15)]
        elif len(self.__players) == 3:
            self.__color_locations[self.__players[0].get_color()] = [Location(0, 12), Location(1, 11), Location(1, 13), Location(2, 10) ,Location(2, 12), Location(2, 14), Location(3, 9), Location(3, 11), Location(3, 13),Location(3, 15)]
            self.__aim_of_players[self.__players[0].get_color()] = [Location(16, 12), Location(15, 11), Location(15, 13), Location(14, 10),Location(14, 12), Location(14, 14), Location(13, 9), Location(13, 11),Location(13, 13), Location(13, 15)]
            self.__color_locations[self.__players[1].get_color()] = [Location(12, 18), Location(12, 20), Location(12, 22), Location(12, 24), Location(11, 19), Location(11, 21), Location(11, 23), Location(10, 20), Location(10, 22), Location(9, 21)]
            self.__aim_of_players[self.__players[1].get_color()] = [Location(4, 0), Location(4, 2), Location(4, 4), Location(4, 6), Location(5, 1), Location(5, 3), Location(5, 5), Location(6, 2), Location(6, 4), Location(7, 3)]
            self.__color_locations[self.__players[2].get_color()] = [Location(12, 0), Location(12, 2), Location(12, 4), Location(12, 6), Location(11, 1), Location(11, 3), Location(11, 5), Location(10, 2), Location(10, 4), Location(9, 3)]
            self.__aim_of_players[self.__players[2].get_color()] = [Location(4, 18), Location(4, 20), Location(4, 22), Location(4, 24), Location(5, 19), Location(5, 21), Location(5, 23), Location(6, 20), Location(6, 22), Location(7, 21)]
        elif len(self.__players) == 4:
            self.__color_locations[self.__players[0].get_color()] = [Location(4, 18), Location(4, 20), Location(4, 22), Location(4, 24), Location(5, 19), Location(5, 21), Location(5, 23), Location(6, 20), Location(6, 22), Location(7, 21)]
            self.__color_locations[self.__players[1].get_color()] = [Location(12, 18), Location(12, 20), Location(12, 22), Location(12, 24), Location(11, 19), Location(11, 21), Location(11, 23), Location(10, 20), Location(10, 22), Location(9, 21)]
            self.__color_locations[self.__players[2].get_color()] = [Location(12, 0), Location(12, 2), Location(12, 4), Location(12, 6), Location(11, 1), Location(11, 3), Location(11, 5), Location(10, 2), Location(10, 4), Location(9, 3)]
            self.__color_locations[self.__players[3].get_color()] = [Location(4, 0), Location(4, 2), Location(4, 4), Location(4, 6), Location(5, 1), Location(5, 3), Location(5, 5), Location(6, 2), Location(6, 4), Location(7, 3)]
            self.__aim_of_players[self.__players[0].get_color()] =[Location(12, 0), Location(12, 2), Location(12, 4), Location(12, 6), Location(11, 1), Location(11, 3), Location(11, 5), Location(10, 2), Location(10, 4), Location(9, 3)]
            self.__aim_of_players[self.__players[1].get_color()] = [Location(4, 0), Location(4, 2), Location(4, 4), Location(4, 6), Location(5, 1), Location(5, 3), Location(5, 5), Location(6, 2), Location(6, 4), Location(7, 3)]
            self.__aim_of_players[self.__players[2].get_color()] =  [Location(4, 18), Location(4, 20), Location(4, 22), Location(4, 24), Location(5, 19), Location(5, 21), Location(5, 23), Location(6, 20), Location(6, 22), Location(7, 21)]
            self.__aim_of_players[self.__players[3].get_color()] = [Location(12, 18), Location(12, 20), Location(12, 22), Location(12, 24), Location(11, 19), Location(11, 21), Location(11, 23), Location(10, 20), Location(10, 22), Location(9, 21)]
        elif len(self.__players) == 6: #0 to 3, 1 to 4, 2 to 5, 3 to 0
            self.__color_locations[self.__players[0].get_color()] = [Location(0, 12), Location(1, 11), Location(1, 13), Location(2, 10) ,Location(2, 12), Location(2, 14), Location(3, 9), Location(3, 11), Location(3, 13),Location(3, 15)]
            self.__color_locations[self.__players[1].get_color()] = [Location(4, 18), Location(4, 20), Location(4, 22), Location(4, 24), Location(5, 19), Location(5, 21), Location(5, 23), Location(6, 20), Location(6, 22), Location(7, 21)]
            self.__color_locations[self.__players[2].get_color()] = [Location(12, 18), Location(12, 20), Location(12, 22), Location(12, 24), Location(11, 19), Location(11, 21), Location(11, 23), Location(10, 20), Location(10, 22), Location(9, 21)]
            self.__color_locations[self.__players[3].get_color()] = [Location(16, 12), Location(15, 11), Location(15, 13), Location(14, 10),Location(14, 12), Location(14, 14), Location(13, 9), Location(13, 11),Location(13, 13), Location(13, 15)]
            self.__color_locations[self.__players[4].get_color()] = [Location(12, 0), Location(12, 2), Location(12, 4), Location(12, 6), Location(11, 1), Location(11, 3), Location(11, 5), Location(10, 2), Location(10, 4), Location(9, 3)]
            self.__color_locations[self.__players[5].get_color()] = [Location(4, 0), Location(4, 2), Location(4, 4), Location(4, 6), Location(5, 1), Location(5, 3), Location(5, 5), Location(6, 2), Location(6, 4), Location(7, 3)]
            self.__aim_of_players[self.__players[0].get_color()] = [Location(16, 12), Location(15, 11), Location(15, 13), Location(14, 10),Location(14, 12), Location(14, 14), Location(13, 9), Location(13, 11),Location(13, 13), Location(13, 15)]
            self.__aim_of_players[self.__players[1].get_color()] =  [Location(12, 0), Location(12, 2), Location(12, 4), Location(12, 6), Location(11, 1), Location(11, 3), Location(11, 5), Location(10, 2), Location(10, 4), Location(9, 3)]
            self.__aim_of_players[self.__players[2].get_color()] = [Location(4, 0), Location(4, 2), Location(4, 4), Location(4, 6), Location(5, 1), Location(5, 3), Location(5, 5), Location(6, 2), Location(6, 4), Location(7, 3)]
            self.__aim_of_players[self.__players[3].get_color()] = [Location(0, 12), Location(1, 11), Location(1, 13), Location(2, 10) ,Location(2, 12), Location(2, 14), Location(3, 9), Location(3, 11), Location(3, 13),Location(3, 15)]
            self.__aim_of_players[self.__players[4].get_color()] =[Location(4, 18), Location(4, 20), Location(4, 22), Location(4, 24), Location(5, 19), Location(5, 21), Location(5, 23), Location(6, 20), Location(6, 22), Location(7, 21)]
            self.__aim_of_players[self.__players[5].get_color()] = [Location(12, 18), Location(12, 20), Location(12, 22), Location(12, 24), Location(11, 19), Location(11, 21), Location(11, 23), Location(10, 20), Location(10, 22), Location(9, 21)]


    def add_players_to_board(self):
        """
        Adds players to the game board based on their source locations.

        Returns:
        - None
        """
        self.__board.set_board()
        for color in self.__color_locations:
            source_scure = self.__color_locations[color]
            for i in source_scure:
                self.__board.get_board()[i.row][i.column] = color

    def remove_from_color_locations(self, player_color, coordinate):
        """
        Removes a coordinate from the color locations dictionary for a specific player color.

        Args:
        - player_color: The color of the player.
        - coordinate: The coordinate to remove.

        Returns:
        - None
        """
        self.__color_locations[player_color].remove(coordinate)

    def add_to_color_locations(self, player_color, coordinate):
        """
        Adds a coordinate to the color locations dictionary for a specific player color.

        Args:
        - player_color: The color of the player.
        - coordinate: The coordinate to add.

        Returns:
        - None
        """
        self.__color_locations[player_color].append(coordinate)

    def get_board(self):
        """
        Returns the game board.

        Returns:
        - list[list[Color]]: The game board.
        """
        return self.__board.get_board()

    def coordinates_of_player(self, player_color):
        """
        Returns the coordinates of a player on the game board.

        Args:
        - player_color: The color of the player.

        Returns:
        - list[Location]: The coordinates of the player.
        """
        return self.__color_locations[player_color]

    def get_players(self):
        """
        Returns the list of players in the game.

        Returns:
        - list[Player]: The list of players.
        """
        return self.__players

    def get_better_move(self, player_color, actions, original_location, first_time):
        best_move = None
        best_distance = float('inf')  # Initialize with a large value
        first_time= True
        distances_to_aims_original=[]
        for action in actions:
            distances_to_aims = []  # Initialize an empty list to store distances to each aim
            for aim in self.__aim_of_players[player_color]:
                if action == aim:
                    return action
                if first_time:
                    distance_to_aim_original = abs(original_location.row - aim.row) + abs(original_location.column - aim.column)
                    distances_to_aims_original.append(distance_to_aim_original)

                distance_to_aim = abs(action.row - aim.row) + abs(action.column - aim.column)
                distances_to_aims.append(distance_to_aim)
            if first_time:
                total_distance_original = sum(distances_to_aims_original)
                first_time = False

            # Sum the distances to all aims
            total_distance = sum(distances_to_aims)

            # Update the best move if the current action brings the player closer to the aim
            if total_distance < best_distance:
                best_distance = total_distance
                best_move = action
        if total_distance > total_distance_original and first_time:
                return original_location
        return best_move



