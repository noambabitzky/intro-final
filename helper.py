import pygame
import sys
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
def text_objects(text, font):
    """
    This function renders text with a specified font and returns the text surface and its rectangle.
    """
    textsurface = font.render(text, True, "white")
    return textsurface, textsurface.get_rect()

def button(msg, x, y, w, h, ic, ac, screen, action=None):
    """
    This function creates a button with text on it and handles button click events.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("Ariel", 25)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

class InputBox:
    """
    Represents an input box for entering text.
    """
    def __init__(self, x, y, w, h, text=''):
        self.__rect = pygame.Rect(x, y, w, h)
        self.__color = pygame.Color('lightskyblue3')
        self.__text = text
        self.__txt_surface = pygame.font.Font(None, 32).render(text, True, self.__color)
        self.__active = False
        self.__player_name_list = []

    def set_surface(self, txt):
        """
        Sets the rendered text surface.
        """
        self.__txt_surface = txt

    def get_text(self):
        """
        Gets the text entered in the input box.
        """
        return self.__text

    def set_text(self, text):
        """
        Sets the text of the input box.
        """
        self.__text = text

    def get_color(self):
        """
        Gets the color of the input box.
        """
        return self.__color

    def handle_event(self, event):
        """
         Handles input events for the input box (mouse and keyboard events).
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect, activate it.
            if self.__rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.__active = not self.__active
            else:
                self.__active = False
            # Change the current color of the input box.
            self.__color = pygame.Color('dodgerblue2') if self.__active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                elif len(self.__text) < 11:
                    self.__text += event.unicode
                # Re-render the text.
                self.__txt_surface = pygame.font.Font(None, 32).render(self.__text[:11], True, self.__color)

    def update(self):
        """Updates the input box, resizing it if the text is too long."""
        # Resize the box if the text is too long.
        width = max(200, self.__txt_surface.get_width() + 10)
        self.__rect.w = width

    def draw(self, screen):
        """
        Draws the input box and its text on the screen.
        """
        # Blit the text.
        screen.blit(self.__txt_surface, (self.__rect.x + 5, self.__rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.__color, self.__rect, 2)

def show_message(screen, message):
    """
    Displays a message on the screen and waits for a key press or mouse click event to continue.
    """
    font = pygame.font.SysFont('Arial', 18)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    text2 = font.render("Press everything to continue", True, BLACK)
    text_rect2 = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
    screen.fill(WHITE)
    screen.blit(text, text_rect)
    screen.blit(text2, text_rect2)
    pygame.display.flip()

    # Wait for a key press or quit event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
