import screen1
import pygame
import sys
import helper
from typing import NamedTuple

GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Location(NamedTuple):
    row: int
    column: int


def valid_name(names, name):
    """
    This function checks if a player name is valid based on certain criteria:
    The name should not already exist in the names list.
    """
    for i in names:
        if name == i:
            return False
    for char in name:
        # Check if the character is not a letter or is not an English letter
        if not char.isalpha() or (not char.islower() and not char.isupper()):
            return False
    return True


# Define Functions
def enter_name(num_of_players):
    """
    This function creates a Pygame interface for entering player names.
    It includes input boxes for entering names, buttons for adding names and starting the game, and messages for feedback.
    :param num_of_players: The number of players expected to enter names.:
    :return: A list of valid player names entered by the users.
    """
    names = []
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Text Input Box")
    clock = pygame.time.Clock()

    more_players_button = pygame.Rect(210, 400, 150, 40)
    start_game_button = pygame.Rect(450, 400, 150, 40)
    input_box1 = helper.InputBox(300, 268, 140, 32)
    input_boxes = [input_box1]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if more_players_button.collidepoint(mouse_pos):
                    if len(input_box1.get_text()) > 0:
                        if valid_name(names, input_box1.get_text()):
                            helper.show_message(screen, "Player name successfully added!")
                            names.append(input_box1.get_text())
                        else:
                            helper.show_message(screen, "Adding the name failed, Enter a name with letters in English only and different names.")
                        if num_of_players == 5:
                            if len(names) == num_of_players + 1:
                                done = True
                                return names
                        else:
                            if len(names) == num_of_players:
                                done = True
                                return names
                        color = input_box1.get_color()
                        # resetting the text in the input box
                        input_box1.set_text('')
                        # delete text from the rendered
                        input_box1.set_surface(pygame.font.Font(None, 32).render('', True,
                                                                                   color))
                elif start_game_button.collidepoint(mouse_pos):
                    if len(input_box1.get_text()) > 0:
                        helper.show_message(screen, "Player name successfully added!!")
                        names.append(input_box1.get_text())
                    if len(names) > 0:
                        return names
                    else:
                        helper.show_message(screen, "You need to add at least one human player.")

        for box in input_boxes:
            box.update()

        screen.fill((255, 255, 255))  # White background

        for box in input_boxes:
            box.draw(screen)

        font = pygame.font.SysFont("Ariel", 30)
        font2 = pygame.font.SysFont("Ariel", 20)
        text = font.render("Enter your name, ", True, BLACK)
        text_rect = text.get_rect(center=(screen_width // 2 , screen_height // 2 - 120))
        screen.blit(text, text_rect)
        text = font2.render("Enter the names of the human players who want to play, ", True, BLACK)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 90))
        screen.blit(text, text_rect)
        text = font2.render("when you are done to add click 'start game', ", True, BLACK)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 70))
        screen.blit(text, text_rect)
        # Draw more players button
        pygame.draw.rect(screen, GRAY, more_players_button)
        more_players_text = pygame.font.SysFont("Arial", 18).render("add name", True, BLACK)
        screen.blit(more_players_text, (more_players_button.x + 45, more_players_button.y + 10))
        # Draw start game button
        pygame.draw.rect(screen, GRAY, start_game_button)
        start_game_text = pygame.font.SysFont("Arial", 18).render("Start Game", True, BLACK)
        screen.blit(start_game_text, (start_game_button.x + 40, start_game_button.y + 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def main2(num_of_players):
    """
    This function is the main entry point for getting player names and starting the game.
    It calls the enter_name function to get player names and then proceeds with the game if valid names are entered.
    Parameters:
    num_of_players: The number of players expected to enter names.
    Returns:
    If valid names are entered, it calls the here function from the main module with the necessary parameters to start the game.
    """
    names = enter_name(num_of_players)
    if names is None:
        return
    else:
        screen1.here(num_of_players, names, "show")


