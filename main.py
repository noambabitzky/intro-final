import pygame
import sys
import helper
import previous_games
import screen_choose_name

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
color_light = (202, 203, 213)
color_dark = (2, 6, 145)

# Set up fonts
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 26)
small_font = pygame.font.SysFont("Arial", 20)


def quit_game():
    """
    This function quits the Pygame application and exits the program.
    """
    pygame.quit()
    sys.exit()


def blit_text(surface, pos, font, color=pygame.Color('black')):
    """
    This function blits text onto a surface at the specified position using the given font and color.
    Parameters:
    surface: The Pygame surface to blit the text onto.
    pos: The position (x, y) where the text should be blitted.
    font: The Pygame font object to use for rendering the text.
    color: The color of the text (defaults to black).
    """
    text = instructions = ("\n\nPress 'ESC' to return to the main menu.\n\n\n"
                           "The Chinese Checkers Board and Pieces:\n "
                           "Chinese Checkers uses a special board that looks like a six pointed start. \n"
                           "There are lots of places in the star where marbles fit. Each player has 10 colored marbles that \n"
                           "start out inside the point of the star.\n\n"
                           " Object of the Game\n"
                           " The object of the Chinese checkers is to get all of your marbles to the\n"
                           " opposite point of the star. The first player to do this wins.\n\n"
                           " Taking a Turn : \n"
                           "When a player takes a turn, they may move one marble.\n"
                           " The marble can be moved to an adjacent open space or may jump over other marbles that are right\n"
                           " next to the marble. You can only jump over 1 marble at a time (for example you can't jump over 2\n"
                           " marbles that are next to each other), but you can do multiple jumps on the same turn;\n"
                           " as long as the hops are all lined up. See the blue path of hops in the picture below for\n"
                           " an example."
                           )
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def show_instructions():
    """
    This function displays instructions about the game using the blit_text function.
    It includes information about the Chinese Checkers game rules and how to play.
    It waits for the user to press the ESC key to return to the main menu.
    """
    helper.button("Quit", 10, 0, 88, 30, color_dark, color_light, screen, quit)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill(WHITE)
        # Draw instructions
        blit_text(screen, (20, 20), small_font)
        helper.button("Quit", 10, 0, 88, 30, color_dark, color_light, screen, quit)
        pygame.display.update()


def main_menu():
    """
    This function displays the main menu of the game.
    It includes buttons for accessing instructions, starting the game, and watching previous games.
    It calls the respective functions based on the user's selection.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        helper.button("Quit", 10, 0, 88, 30, color_dark, color_light,screen, quit)
        pygame.display.flip()

        # Clear the screen
        screen.fill(WHITE)

        # Draw the buttons
        helper.button("Instructions", 300, 200, 200, 50, BLACK, color_light,  screen, show_instructions)
        helper.button("Start Game", 300, 300, 200, 50, BLACK, color_light,screen, select_players)
        helper.button("Watch previous games", 300, 400, 200, 50, BLACK, color_light,screen, previous_games.main)


def select_players():
    """
    This function allows the user to select the number of players for the game.
    It displays buttons for selecting 2, 3, 4, or 6 players and calls screen_choose_name.main2 with the selected number of players.
    """
    screen.fill(WHITE)
    helper.button("Quit", 10, 0, 88, 30, color_dark, color_light,screen, quit)
    pygame.display.flip()
    # Draw the player selection buttons
    num_players_buttons = []
    text = font.render("choose number of players", True, BLACK)
    screen.blit(text, (250, 100))
    for i, num_players in enumerate([2, 3, 4, 6]):

        button_rect = pygame.Rect(300, 200 + i * 50, 200, 45)
        pygame.draw.rect(screen, BLACK, button_rect)
        text = font.render(f"{num_players} Players", True, WHITE)
        screen.blit(text, (340, 215 + i * 50))
        num_players_buttons.append(button_rect)

    pygame.display.update()
    while True:
        helper.button("Quit", 10, 0, 88, 30, color_dark, color_light,screen, quit)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button_rect in enumerate(num_players_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        screen_choose_name.main2(i + 2)
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return


def select_computer_or_user(num_of_players):
    """
    This function is intended to allow the user to select whether players are computer-controlled or human-controlled.
    It is currently incomplete and doesn't have any functionality defined.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill(WHITE)
        helper.button("Quit", 10, 0, 88, 30, color_dark, color_light,screen, quit)
        # Draw the player selection buttons
        num_players_buttons = []


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Hey, this is a Chinese Checkers game.\n"
                  "Run the program without any arguments.\n"
                  "The screen will open, use the screen to play.\n"
                  "There are three options:\n"
                  "* Instructions\n"
                  "* Start Game\n"
                  "* Watch Previous Games\n"
                  "enjoy!!")
    else:
        main_menu()