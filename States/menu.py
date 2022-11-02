import pygame

from .state import State
from app import App
from .button import MenuButton
import pygame_widgets
from pygame_widgets.button import ButtonArray


class Menu(State):
    def __init__(self):
        super().__init__()
        self.button_orig_image = pygame.image.load('./Assets/button.png').convert_alpha()
        self.button_image = pygame.transform.smoothscale(
            self.button_orig_image, (
                (self.button_orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width(),
                (self.button_orig_image.get_height() / App.HIGH_RES[1]) * App.window.get_height()
            )
        )
        self.button_array = ButtonArray(
            App.window, App.window.get_width() / 2 - self.button_image.get_width() / 2, App.window.get_height() * 0.3,
            self.button_image.get_width(), 3 * self.button_image.get_height(), (1, 2),
            texts=('PLAY', 'OPTIONS'), images=(self.button_image, self.button_image),
            onClicks=(lambda: self.change_state('game'), lambda: self.change_state('options')),
            fontSizes=(int(0.7 * self.button_image.get_height()), int(0.7 * self.button_image.get_height())),
            textColours=((255, 255, 255), (255, 255, 255)), inactiveColours=((9, 14, 23), (9, 14, 23)),
            colour=(9, 14, 23), hoverColours=((9, 14, 23), (9, 14, 23)), pressedColours=((9, 14, 23), (9, 14, 23))
        )

    def resize(self):
        self.button_array = ButtonArray(
            App.window, App.window.get_width() / 2 - self.button_image.get_width() / 2, App.window.get_height() * 0.3,
            self.button_image.get_width(), 3 * self.button_image.get_height(), (1, 2),
            texts=('PLAY', 'OPTIONS'), images=(self.button_image, self.button_image),
            onClicks=(lambda: self.change_state('game'), lambda: self.change_state('options')),
            fontSizes=(int(0.7 * self.button_image.get_height()), int(0.7 * self.button_image.get_height())),
            textColours=((255, 255, 255), (255, 255, 255)), inactiveColours=((9, 14, 23), (9, 14, 23)),
            colour=(9, 14, 23), hoverColours=((9, 14, 23), (9, 14, 23)), pressedColours=((9, 14, 23), (9, 14, 23))
        )

    def update(self):
        self.draw()
        pygame_widgets.update(pygame.event.get())

    def draw(self):
        App.window.fill((9, 14, 23))
