import pygame
import sys
import helper
import re
import show_moves

pygame.init()
FONT = pygame.font.Font(None, 32)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Moves_game():
    """
    This class manages game moves.
    """
    def __init__(self):
        self.__move = None
    def set_move(self, move):
        """
        Sets the current move.
        """
        self.__move = move

    def get_move(self):
        """
        Retrieves the current move.
        """
        return self.__move

move = Moves_game()

def check_time_format(text):
    """
    Checks if the text follows the time format (HH:MM:SS).
    """
    if len(text) == 8 and text.count(':') == 2:
        parts = text.split(':')
        if parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
                return True
    return False


def check_date_format(text):
    """Checks if the text follows the date format (YYYY-MM-DD)."""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, text):
        year, month, day = map(int, text.split('-'))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return True
    return False

def main():
    """
    Main function to run the Pygame interface.
    Reads log file data and displays matches.
    Manages input boxes for entering date and time.
    Handles button events for showing games and quitting.
    """
    try:
        with open('numbers.log', 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        lines = []

    numbers_match = 0
    matches = [(index, line.split(' - ')[0].strip()) for index, line in enumerate(lines) if "Match start" in line]
    for i in range(len(matches)):
        numbers_match += 33

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    intermediate = pygame.surface.Surface((800, max(numbers_match, 600)))
    intermediate.fill(WHITE)  # Fill the screen with white color
    y = 45
    f = pygame.font.SysFont('malgungothicsemilight', 15)
    i = 1
    for match in matches:
        text_surface = f.render(f"Match {i}, started at {match[1]}", True, BLACK)  # Text color in black
        intermediate.blit(text_surface, (10, y))
        y += 31
        i += 1

    scroll_y = 0
    font1 = pygame.font.SysFont("arial", 20)
    font2 = pygame.font.SysFont("Agency FB", 20)
    input_box1 = helper.InputBox(500, 100, 50, 30)
    input_box2 = helper.InputBox(500, 200, 50, 30)
    input_boxes = [input_box1, input_box2]

    color_light = (202, 203, 213)
    color_dark = (2, 6, 145)
    helper.button("Show game", 550, 300, 110, 30, BLACK, color_light, screen)
    helper.button("Quit", 10, 0, 88, 30, color_dark, color_light, screen, quit)
    pygame.display.update()
    run_it = True
    while run_it:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if numbers_match > 600:
                    if event.button == 4:
                        scroll_y = min(scroll_y + 15, 0)
                    if event.button == 5:
                        scroll_y = max(scroll_y - 15, -(numbers_match - 600))
                if (550 <= mouse_x <= 660) and (300 <= mouse_y <= 330):
                    show_messages([input_box1, input_box2], matches)
                    helper.button("Show game", 550, 300, 110, 30, BLACK, color_light, screen,
                                  lambda: show_messages([input_box1, input_box2], matches))

            elif event.type == pygame.KEYDOWN:
                if numbers_match > 600:
                    if event.key == pygame.K_DOWN:
                        scroll_y = max(scroll_y - 15, -(numbers_match - 600))
                    if event.key == pygame.K_UP:
                        scroll_y = min(scroll_y + 15, 0)
                if event.key == pygame.K_ESCAPE:
                    run_it = False
                    return
            for box in input_boxes:
                box.handle_event(event)

            helper.button("Quit", 10, 0, 88, 30, color_dark, color_light, screen, quit)

        for box in input_boxes:
            box.update()

        pygame.display.update()
        screen.fill((30, 30, 30))

        screen.blit(intermediate, (0, scroll_y))
        for box in input_boxes:
            box.draw(screen)
        text = font1.render("Press 'ESC' to return to the main menu", True, BLACK)
        text_rect = text.get_rect(center=(660, 20))
        screen.blit(text, text_rect)
        text = font2.render("Enter the date (for example: 2024-03-17):", True, BLACK)
        text_rect = text.get_rect(center=(600, 85))
        screen.blit(text, text_rect)
        text = font2.render("Enter the time (for example: 10:39:17):", True, BLACK)
        text_rect = text.get_rect(center=(600, 185))
        screen.blit(text, text_rect)

        helper.button("Show game", 550, 300, 110, 30, BLACK, color_light, screen,
                          lambda: show_messages([input_box1, input_box2], matches))
        helper.button("Quit", 10, 0, 88, 30, color_dark, color_light, screen, quit)
        pygame.display.flip()
        pygame.display.update()

def to_show():
    """
    Calls the create function from the show_moves module to display the game.
    """
    show_moves.create(move.get_move())

def show_messages(input_boxes, matches):
    """
    Validates the entered date and time formats.
    Calls the to_show function to display the game if formats are valid.
    Displays an error message if formats are invalid.
    """
    if check_date_format(input_boxes[0].get_text()) and check_time_format(input_boxes[1].get_text()):
        for match in matches:
            if match[1] == f"{input_boxes[0].get_text()} {input_boxes[1].get_text()}":
                show_m = show_moves.ShowMoves(input_boxes[1].get_text(), input_boxes[0].get_text(), match[0])
                move.set_move(show_m)
                to_show()
                main()


    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont('Arial', 18)
    text = font.render("Date and time does not exist or is in an incorrect format, or error in this file game", True, BLACK)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    text2 = font.render("Enter 'Esc' to continue ", True, BLACK)
    text_rect2 = text.get_rect(center=(screen.get_width() // 2 + 170, screen.get_height() // 2 + 30))

    screen.fill(WHITE)
    screen.blit(text, text_rect)
    screen.blit(text2, text_rect2)
    pygame.display.flip()
    for box in input_boxes:
        color = box.get_color()
        # resetting the text in the input box
        box.set_text('')
        # delete text from the rendered
        box.set_surface(pygame.font.Font(None, 32).render('', True,
                                                                 color))
        pygame.display.flip()
        pygame.display.update()
    # Wait for a key press or quit event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

