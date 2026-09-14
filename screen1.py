import pygame
import player
import sys
import random
import logging
import colorsys
from webcolors import name_to_rgb
from typing import NamedTuple
import helper
import re
import os
import time
def here(num, names, state):
    """ run screen1 """
    import game
    import board

    class Location(NamedTuple):
        row: int
        column: int

    def handle_player_turn(player_play, location_of_player):
        """
        Handles the player's turn,
        including event handling for mouse clicks,
        updating the game board based on player actions, and logging game moves.
        """

        font = pygame.font.Font(None, 20)
        font2 = pygame.font.Font(None, 30)
        # Variable to store the previous player's click
        last_selected_token = None
        finished = False
        while not finished:
            helper.button("Menu", 340, 0, 90, 30, BLACK, color_light, screen)
            helper.button("Quit", 10, 0, 88, 30, color_dark, color_light, screen)
            helper.button("Start a new game", 120, 0, 200, 30, BLACK, color_light, screen)
            pygame.display.flip()
            if isinstance(player_play,game.DummyAutoPlayer):
                pygame.time.delay(1000)
                action = {}
                for location in location_of_player:
                    valid_actions = new_game.valid_moves(location)
                    if len(valid_actions) != 0 :
                        action[location] = valid_actions
                original_location = random.choice(list(action.keys()))
                is_bigger= True
                while is_bigger:
                    target_location = new_game.get_better_move(player_play.get_color(),(action[original_location]), original_location, True)
                    if target_location == original_location:
                        if len(action) > 1:
                            action.pop(original_location)
                            original_location = random.choice(list(action.keys()))
                        else:
                            target_location = new_game.get_better_move(player_play.get_color(),
                                                                       (action[original_location]), original_location,
                                                                       False)
                            is_bigger = False
                    else:
                        is_bigger = False
                new_game.get_board()[original_location.row][original_location.column] = player.Color.BLANK
                new_game.get_board()[target_location.row][target_location.column] = player_play.get_color()
                new_game.remove_from_color_locations(player_play.get_color(), original_location)
                new_game.add_to_color_locations(player_play.get_color(), target_location)
                logging.info(f"{player_play.get_name()}: move {original_location} to {target_location}")
                return
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        logging.info(f"Game end!, game stopped.")
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        row, column = get_clicked_cell(mouse_pos[0], mouse_pos[1], 32, 50, 28)
                        location = Location(row, column)
                        if 340 <= mouse_pos[0] <= 430 and 0 <= mouse_pos[1] <= 30:
                            logging.info(f"Game end!, game stopped.")
                            pygame.quit()
                            os.system('python main.py')
                            sys.exit()

                        if 120 <= mouse_pos[0] <= 320 and 0 <= mouse_pos[1] <= 30:
                            logging.info(f"Game end!, game stopped.")
                            screen.fill(WHITE)
                            new_game.set_source_aim_of_players()
                            new_game.add_players_to_board()
                            create_board()
                            auto_player = 0
                            list_names = []
                            for player_play in new_game.get_players():
                                if isinstance(player_play, game.DummyAutoPlayer):
                                    auto_player += 1
                                else:
                                    list_names.append(player_play.get_name())
                            logging.info(f"Match start!")
                            logging.info(f"Players: {len(new_game.get_players())- auto_player}, Auto players: {auto_player}")
                            logging.info(f"names: {', '.join(list_names)}")
                            pygame.display.update()
                            new_game.set_start_again(True)
                            return
                        # Check if the click is in the source selection phase
                        if last_selected_token is None:

                            if location.row == -1 and -2<location.column <1:
                                logging.info(f"Game end!, game stopped.")
                                pygame.quit()
                                sys.exit()
                            if location in location_of_player:
                                screen.fill(WHITE)
                                create_board()
                                instructions_text = font2.render(f"it`s {player_play.get_name()} turn", True,
                                                                 pygame.Color(player_play.get_color().value))
                                screen.blit(instructions_text, (600, 50))
                                pygame.display.update()
                                color_here = new_game.get_board()[location.row][location.column]
                                bright_color = increase_brightness(
                                    color_here.value, 4)
                                new_game.get_board()[location.row][location.column] = bright_color
                                create_board()

                                valid_text = font.render("Valid starting location. Choose a target location.",
                                                                 True,
                                                                 BLACK)
                                screen.blit(valid_text, (590, 70))
                                pygame.display.update()
                                last_selected_token = location
                                new_game.get_board()[location.row][location.column] = color_here
                            else:
                                screen.fill(WHITE)
                                create_board()
                                instructions_text = font2.render(f"it`s {player_play.get_name()} turn", True,
                                                                 pygame.Color(player_play.get_color().value))
                                screen.blit(instructions_text, (600, 50))
                                pygame.display.update()
                                valid_text = font.render("Invalid starting location. Choose a valid location.", True,
                                                                 BLACK)
                                screen.blit(valid_text, (590, 70))
                                pygame.display.update()

                        # Check if the click is in the target selection phase
                        else:

                            target_location = location
                            if target_location in new_game.valid_moves(last_selected_token):
                                new_game.get_board()[last_selected_token.row][
                                    last_selected_token.column] = player.Color.BLANK
                                new_game.get_board()[target_location.row][
                                    target_location.column] = player_play.get_color()
                                new_game.remove_from_color_locations(player_play.get_color(), last_selected_token)
                                new_game.add_to_color_locations(player_play.get_color(), target_location)
                                logging.info(f"{player_play.get_name()}: move {last_selected_token} to {target_location}")
                                return
                            else:
                                screen.fill(WHITE)
                                create_board()
                                instructions_text = font2.render(f"it`s {player_play.get_name()} turn", True,
                                                                 pygame.Color(player_play.get_color().value))
                                screen.blit(instructions_text, (600, 50))
                                pygame.display.update()
                                valid_text = font.render("Invalid action. Choose a valid start location.", True,
                                                         BLACK)
                                screen.blit(valid_text, (590, 70))
                                pygame.display.update()
                            last_selected_token = None

    def get_clicked_cell(mouse_x, mouse_y, CELL_SIZE, board_x, board_y):
        # Calculate the row and column in the board's 2D array
        row = (mouse_y - board_y) // CELL_SIZE
        column = (mouse_x - board_x) // CELL_SIZE
        return row, column

    def increase_brightness(color, factor):
        """
        Increases the brightness of a color by a specified factor.
        """
        # Convert RGB color to HSV
        if color == "gold":
            return "khaki"
        elif color == "cyan":
            return "paleturquoise"
        elif color == "salmon":
            return "lightsalmon"
        rgb_tuple = name_to_rgb(color)
        hsv_color = colorsys.rgb_to_hsv(rgb_tuple[0] / 255, rgb_tuple[1] / 255, rgb_tuple[2] / 255)

        # Increase the brightness (value) by the specified factor
        new_value = min(1, hsv_color[2] * factor)

        # Convert back to RGB
        new_rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], new_value)

        # Scale back to RGB values (0-255)
        return tuple(int(val * 255) for val in new_rgb_color)

    def create_board():
        """
        Creates and updates the game board interface.
        """
        pions_rect = []
        CELL_SIZE = 32
        # Board width in pixels
        board_width = 25 * CELL_SIZE
        # Board height in pixels
        board_height = 17 * CELL_SIZE

        # Calculate initial position on the screen so that the board is centered
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

    def main_loop(index=0):
        """
        Manages the main game loop, including player turns,
        event handling, updating the game board,
        checking for game end conditions, and handling game restart.
        """
        if state == "show":
            list_human_names = []
            auto_players = 0
            for player_play in new_game.get_players():
                if isinstance(player_play, game.DummyAutoPlayer):
                    auto_players += 1
                else:
                    list_human_names.append(player_play.get_name())

            logging.info(f"Match start!")
            if auto_players == 5:
                logging.info(f"Players: {len(list_human_names)}, Auto players: {6-len(list_human_names)}")
            else:
                logging.info(f"Players: {len(list_human_names)}, Auto players: {auto_players}")
            logging.info(f"names: {', '.join(list_human_names)}")
        current_player_index = index

        while True:
            helper.button("Menu", 340, 0, 90, 30, BLACK, color_light, screen)
            helper.button("Start a new game", 120, 0, 200, 30, BLACK, color_light, screen)
            helper.button("Quit", 10, 0, 88, 30, color_dark, color_light, screen, quit)

            current_player = new_game.get_players()[current_player_index]
            location_of_player = new_game.coordinates_of_player(current_player.get_color())
            font2 = pygame.font.Font(None, 30)
            font3 = pygame.font.Font(None, 20)
            instructions_text = font2.render(f"it`s {current_player.get_name()} turn", True, pygame.Color(current_player.get_color().value))
            screen.blit(instructions_text, (600, 50))
            pygame.display.flip()
            handle_player_turn(current_player, location_of_player)


            try:
                sound_file = "LightSwitch.mp3"
                sound = pygame.mixer.Sound(sound_file)
                sound.play()
                time.sleep(sound.get_length()-2.5)
            except FileNotFoundError:
                pass
            screen.fill(WHITE)
            create_board()
            pygame.display.flip()

            if new_game.game_ended(color=current_player.get_color()):
                win = font2.render(f"{current_player.get_name()} won!", True,
                                                 pygame.Color(current_player.get_color().value))
                screen.blit(win, (600, 50))
                again = font3.render("If you want to play again, press enter. If not, press 'Esc'" ,True, BLACK)
                screen.blit(again, (540, 70))
                new_game.update_wins_and_losses(current_player)
                logging.info(f"Game end!, {current_player.get_name()} won.")
                pygame.display.flip()
                press = False
                while not press:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:

                                screen.fill(WHITE)
                                new_game.set_source_aim_of_players()
                                new_game.add_players_to_board()
                                create_board()
                                current_player_index = -1
                                logging.info(f"Match start!")
                                logging.info(f"Players: {len(names)}, Auto players: {len(new_game.get_players()) - len(names)}")
                                logging.info(f"names: {', '.join(names)}")
                                press = True
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
            # If game start again.
            if new_game.get_start_again():
                current_player_index = 0
                new_game.set_start_again(False)
            else:
                # After the current player's turn ends, move on to the next player
                current_player_index = (current_player_index + 1) % len(new_game.get_players())

    pygame.mixer.init()
    logging.basicConfig(filename='numbers.log', level=logging.INFO,
                        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    color_light = (202, 203, 213)
    color_dark = (2, 6, 145)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 600

    if state == "show":

        board = board.Board()
        if num == 5:
            new_game = game.Game(num + 1, board)
        else:
            new_game = game.Game(num, board)
        if num == 5:
            if num + 1 > len(names):
                for i in range(1, num - len(names) + 2):
                    # To fix the problem whit 6
                    names.append(f"computerPlayer{i}")
        elif num > 0:
            if num > len(names):
                for i in range(1, num - len(names) + 1):
                    # To fix the problem whit 6
                    names.append(f"computerPlayer{i}")
        pygame.init()
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game of Chinese Checkers")
        screen.fill(WHITE)
        pygame.display.flip()

        new_game.add_player(names)
        new_game.set_source_aim_of_players()
        new_game.add_players_to_board()
        create_board()
        main_loop()

    if state != "show":
        # A function that resumes the game from where we left off and initializes the board accordingly.
        pygame.init()
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game of Chinese Checkers")
        screen.fill(WHITE)
        board = board.Board()
        new_game = game.Game(num, board)
        new_game.add_player(names)
        new_game.set_source_aim_of_players()
        new_game.add_players_to_board()
        create_board()

        line_number = state
        pattern = r'Location\(row=(\d+), column=(\d+)\)'
        with open("numbers.log", 'r') as file:
            lines = file.readlines()
        lines_action=[]
        first_time = False

        for line in lines[line_number:]:
            if "Match start!" in line and first_time:
                break
            else:
                lines.remove(line)
                if line.split(' - ')[1].strip().split(" ")[1] == "move":
                    # Finding all matches to the regular expression in the line.
                    matches = re.findall(pattern, line)
                    lines_action.append(matches)
                first_time = True
        with open("numbers.log", 'w') as file:
            file.writelines(lines)
        logging.info(f"Match start!")
        list_human_names = []
        auto_players = 0
        for player_play in new_game.get_players():
            if isinstance(player_play, game.DummyAutoPlayer):
                auto_players += 1
            else:
                list_human_names.append(player_play.get_name())
        logging.info(f"Players: {len(list_human_names)}, Auto players: {auto_players}")
        logging.info(f"names: {', '.join(list_human_names)}")
        current_player_index = 0
        for move in lines_action:
            current_player = new_game.get_players()[current_player_index]
            row, column = move[0]
            original_location = Location(int(row), int(column))
            row, column = move[1]
            target_location = Location(int(row), int(column))
            new_game.get_board()[original_location[0]][original_location[1]] = player.Color.BLANK
            new_game.get_board()[target_location[0]][target_location[1]] = current_player.get_color()
            new_game.remove_from_color_locations(current_player.get_color(), original_location)
            new_game.add_to_color_locations(current_player.get_color(), target_location)
            logging.info(f"{current_player.get_name()}: move {original_location} to {target_location}")
            current_player_index = (current_player_index + 1) % len(new_game.get_players())
        create_board()
        pygame.display.update()
        pygame.display.flip()
        main_loop(current_player_index)








