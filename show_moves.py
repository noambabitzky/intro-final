import sys
import helper
import pygame
import game
import player
import re


class ShowMoves:
    def __init__(self, time, date, line):
        self.__time = time
        self.__date = date
        self.__line = line

    def get_line(self):
        return self.__line


def create(move):
    """
    Description: Creates the game state based on the provided move.
    Parameters:
    move: An instance of the ShowMoves class representing the move to be recreated.
    Process:
    Reads game data from a log file.
    Initializes the game board, players, and game variables.
    Draws the initial game state including player positions and arrows indicating move directions.
    Enters the main game loop.
    """
    import board
    try:
        # Read game data from a log file
        with open('numbers.log', 'r') as file:
            lines = [line.split(' - ')[1].strip() for line in file]
        # Extract player information and initialize the game
        human_players = lines[move.get_line() + 1].split(', Auto players: ')[0].split("Players: ")[1].strip()
        auto_players = lines[move.get_line() + 1].split(', Auto players: ')[1].strip()
        num_of_players = int(human_players) + int(auto_players)
        board_instance = board.Board()
        new_game = game.Game(num_of_players, board_instance)
        names = lines[move.get_line() + 2].split("names: ")[1].strip()
        names_list = names.split(", ")

        # Ensure enough players are available, adding computer players if necessary
        if num_of_players > len(names_list):
            for i in range(1, num_of_players - len(names_list) + 1):
                names_list.append(f"computerPlayer{i}")

        # Initialize game variables
        to_continue = True
        state_of_game = ""
        i = 3
        steps_in_game = []
        num_of_line = move.get_line()

        # Extract game steps from the log file
        while to_continue:
            if num_of_line + i < len(lines):
                line = lines[num_of_line + i]
                match = re.search(r'Location\(row=(\d+), column=(\d+)\) to Location\(row=(\d+), column=(\d+)\)', line)
                if match:
                    # Extract the locations and add them as a tuple to the moves list
                    move = (
                        (int(match.group(1)), int(match.group(2))),
                        (int(match.group(3)), int(match.group(4)))
                    )
                    steps_in_game.append(move)
                if line.startswith("Game"):
                    to_continue = False
                    state_of_game = line.split()[-1]
                i += 1
            else:
                to_continue = False

        # Initialize Pygame window and draw initial game state
        arrow_width = 20
        arrow_height = 40
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 600
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game of Chinese Checkers")
        screen.fill(WHITE)
        pygame.display.flip()
        new_game.add_player(names_list)
        new_game.set_source_aim_of_players()
        new_game.add_players_to_board()

        create_board(new_game, screen)

        # Draw the arrow triangle pointing left
        pygame.draw.polygon(screen, BLACK, [(0, WINDOW_HEIGHT - 30), (arrow_width, WINDOW_HEIGHT - 30 - arrow_height // 2),
                                            (arrow_width, WINDOW_HEIGHT - 30 + arrow_height // 2)])

        # Draw the short line that intersects the triangle
        pygame.draw.line(screen, BLACK, (arrow_width, WINDOW_HEIGHT - 30), (arrow_width + 30, WINDOW_HEIGHT - 30), 10)

        # Draw the arrow triangle pointing right
        pygame.draw.polygon(screen, BLACK, [(WINDOW_WIDTH, WINDOW_HEIGHT - 30),
                                            (WINDOW_WIDTH - arrow_width, WINDOW_HEIGHT - 30 - arrow_height // 2),
                                            (WINDOW_WIDTH - arrow_width, WINDOW_HEIGHT - 30 + arrow_height // 2)])

        # Draw the short line that intersects the triangle
        pygame.draw.line(screen, BLACK, (WINDOW_WIDTH - arrow_width, WINDOW_HEIGHT - 30),
                         (WINDOW_WIDTH - arrow_width - 30, WINDOW_HEIGHT - 30), 10)

        # Update the display
        pygame.display.flip()
        pygame.display.update()
        main(new_game, screen, state_of_game, steps_in_game, num_of_line)
    except IndexError:
        return



def main(new_game, screen, state, moves, num_line):
    """
    Description: Implements the main game loop and user interaction.
    Parameters:
    new_game: An instance of the Game class representing the current game state.
    screen: The Pygame screen object.
    state: The state of the game ("show" or "stopped.").
    moves: A list of moves to be displayed.
    num_line: The line number in the log file where the game state begins.
    Process:
    Initializes Pygame and sets up game colors and dimensions.
    Handles player turns, move selection, and game continuation.
    Draws the game board, player positions, arrows, and buttons for interaction.
    Manages events such as mouse clicks and key presses.
    Updates the display and continues the game loop until the game ends or the user quits.
    """
    pygame.init()
    color_light = (202, 203, 213)
    color_dark = (2, 6, 145)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    current_player_index = -1
    current_player = new_game.get_players()[0]
    to_write_current_player_index = 0

    # Arrow dimensions
    arrow_width = 20
    arrow_height = 40
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    index_to_move = -1

    font2 = pygame.font.Font(None, 30)
    while True:

        pygame.display.flip()
        location_of_player = new_game.coordinates_of_player(current_player.get_color())
        screen.fill(WHITE)
        helper.button("Quit", 10, 0, 88, 30, BLACK, color_light, screen, quit)
        helper.button("Continue the game", 130, 0, 200, 30, BLACK, color_light, screen)
        if to_write_current_player_index <= len(moves) - 1:
            to_write_current_player = new_game.get_players()[
                to_write_current_player_index % len(new_game.get_players())]
            instructions_text = font2.render(f"It's {to_write_current_player.get_name()}'s turn", True,
                                             pygame.Color(to_write_current_player.get_color().value))
            screen.blit(instructions_text, (550, 50))
        else:
            instructions_text = font2.render(f"There are no more steps", True,
                                             BLACK)
            screen.blit(instructions_text, (550, 50))
        pygame.draw.polygon(screen, BLACK,
                            [(0, WINDOW_HEIGHT - 30), (arrow_width, WINDOW_HEIGHT - 30 - arrow_height // 2),
                             (arrow_width, WINDOW_HEIGHT - 30 + arrow_height // 2)])

        # Draw the short line that intersects the triangle
        pygame.draw.line(screen, BLACK, (arrow_width, WINDOW_HEIGHT - 30), (arrow_width + 30, WINDOW_HEIGHT - 30), 10)

        # Draw the arrow triangle pointing right
        pygame.draw.polygon(screen, BLACK, [(WINDOW_WIDTH, WINDOW_HEIGHT - 30),
                                            (WINDOW_WIDTH - arrow_width, WINDOW_HEIGHT - 30 - arrow_height // 2),
                                            (WINDOW_WIDTH - arrow_width, WINDOW_HEIGHT - 30 + arrow_height // 2)])

        # Draw the short line that intersects the triangle
        pygame.draw.line(screen, BLACK, (WINDOW_WIDTH - arrow_width, WINDOW_HEIGHT - 30),
                         (WINDOW_WIDTH - arrow_width - 30, WINDOW_HEIGHT - 30), 10)
        create_board(new_game, screen)
        pygame.display.update()

        finished = False
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if ((
                            0 <= mouse_x <= arrow_width and WINDOW_HEIGHT - 30 - arrow_height // 2 <= mouse_y <= WINDOW_HEIGHT - 30 + arrow_height // 2 and index_to_move != -1)
                            or (
                                    0 <= mouse_x <= arrow_width + 30 and WINDOW_HEIGHT - 30 - 5 <= mouse_y <= WINDOW_HEIGHT - 30 + 5 and index_to_move != -1)):
                        original_location = moves[index_to_move][0]
                        target_location = moves[index_to_move][1]
                        try:
                            new_game.get_board()[original_location[0]][original_location[1]] = current_player.get_color()
                            new_game.get_board()[target_location[0]][target_location[1]] = player.Color.BLANK
                            new_game.remove_from_color_locations(current_player.get_color(), target_location)
                            new_game.add_to_color_locations(current_player.get_color(), original_location)
                            finished = True
                            to_write_current_player_index -= 1
                            index_to_move -= 1
                            current_player_index = (current_player_index - 1) % len(new_game.get_players())
                            current_player = new_game.get_players()[current_player_index]
                        except ValueError:
                            return

                    elif (
                            WINDOW_WIDTH - arrow_width <= mouse_x <= WINDOW_WIDTH and WINDOW_HEIGHT - 30 - arrow_height // 2 <= mouse_y <= WINDOW_HEIGHT - 30 + arrow_height // 2 and index_to_move + 1 < len(
                            moves)) \
                            or (
                            WINDOW_WIDTH - arrow_width - 30 <= mouse_x <= WINDOW_WIDTH - arrow_width and WINDOW_HEIGHT - 30 - 5 <= mouse_y <= WINDOW_HEIGHT - 30 + 5 and index_to_move + 1 < len(
                        moves)):
                        index_to_move = index_to_move + 1
                        current_player_index = (current_player_index + 1) % len(new_game.get_players())
                        current_player = new_game.get_players()[current_player_index]
                        original_location = moves[index_to_move][0]
                        target_location = moves[index_to_move][1]
                        try:
                            new_game.get_board()[original_location[0]][original_location[1]] = player.Color.BLANK
                            new_game.get_board()[target_location[0]][target_location[1]] = current_player.get_color()
                            new_game.remove_from_color_locations(current_player.get_color(), original_location)
                            new_game.add_to_color_locations(current_player.get_color(), target_location)
                            finished = True
                            to_write_current_player_index += 1
                        except ValueError:
                            return
                    elif 130 <= mouse_x <= 330 and 0<= mouse_y <=30:
                        continue_game(new_game.get_players(), state, num_line, screen)
                        finished = True
                helper.button("Quit", 10, 0, 88, 30, BLACK, color_light, screen, quit)
                helper.button("Continue the game", 130, 0, 200, 30, BLACK, color_light, screen)
                pygame.display.update()


def create_board(new_game, screen):
    """
    Description: Draws the game board and player positions on the screen.
    Parameters:
    new_game: An instance of the Game class representing the current game state.
    screen: The Pygame screen object.
    Process:
    Calculates the position and size of each cell on the board.
    Draws rectangles for each cell based on the player positions on the board.
    """
    pions_rect = []
    CELL_SIZE = 32
    board_width = 25 * CELL_SIZE  # Width of the board in pixels
    board_height = 17 * CELL_SIZE  # Height of the board in pixels

    # Calculate initial screen position to center the board
    board_x = (screen.get_width() - board_width) // 2
    board_y = (screen.get_height() - board_height) // 2

    for i in range(0, 17):
        for j in range(0, 25):
            if new_game.get_board()[i][j] != player.Color.OUT_OF_BOARD:
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                rect.x += board_x
                rect.y += board_y
                try:
                    pions_rect.append(pygame.draw.rect(screen, new_game.get_board()[i][j].value, rect,
                                                       border_radius=30))
                except AttributeError:
                    pions_rect.append(pygame.draw.rect(screen, new_game.get_board()[i][j], rect,
                                                       border_radius=30))

def continue_game(players, state, num_line, screen):
    """
    Description: Handles game continuation after it has been stopped.
    Parameters:
    players: A list of player objects.
    state: The state of the game ("stopped." if the game was stopped).
    num_line: The line number in the log file where the game state begins.
    screen: The Pygame screen object.
    Process:
    Calls the here() function from the main module to continue the game based on the saved state in the log file.
    Shows a message if the game has already been ended.
    """
    import screen1
    names = []
    num_of_players = len(players)
    for player_play in players:
        names.append(player_play.get_name())
    if state == "stopped.":
        screen1.here(num_of_players, names, num_line)
    else:
        helper.show_message(screen, "The game has been ended.")
        return

