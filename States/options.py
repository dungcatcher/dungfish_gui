import pygame

from .state import State
from app import App
from .button import OptionsButton


class Options(State):
    def __init__(self):
        super().__init__()
        self.orig_options_image = pygame.image.load('./Assets/options_screen.png').convert_alpha()
        self.image = pygame.transform.smoothscale(
            self.orig_options_image, (
                (self.orig_options_image.get_width() / App.HIGH_RES[0]) * App.window.get_width(),
                (self.orig_options_image.get_height() / App.HIGH_RES[1]) * App.window.get_height()
            )
        )
        self.rect = self.image.get_rect(center=(App.window.get_width() / 2, App.window.get_height() / 2))

        self.buttons = [
            OptionsButton((self.rect.centerx, self.rect.top + self.rect.height * 0.33), 'PLAYER COLOUR', (255, 255, 255),
                          (self.rect.width * 0.8, self.rect.height * 0.1))
        ]

    def resize(self):
        self.image = pygame.transform.smoothscale(
            self.orig_options_image, (
                (self.orig_options_image.get_width() / App.HIGH_RES[0]) * App.window.get_width(),
                (self.orig_options_image.get_height() / App.HIGH_RES[1]) * App.window.get_height()
            )
        )
        self.rect = self.image.get_rect(center=(App.window.get_width() / 2, App.window.get_height() / 2))

    def update(self):
        self.draw()
        for button in self.buttons:
            button.update()

    def draw(self):
        App.window.fill((9, 14, 23))
        App.window.blit(self.image, self.rect)
        for button in self.buttons:
            button.draw()
