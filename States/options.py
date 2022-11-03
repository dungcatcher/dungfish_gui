import pygame
import json

from .state import State
from app import App
from pygame_widgets.dropdown import Dropdown

with open('States/options.json') as f:
    options = json.load(f)


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

        self.player_colour_dropdown = None
        self.widgets = None
        self.gen_widgets()

    def change_player_colour(self):
        print(self.player_colour_dropdown.getSelected())
        options['player_colour'] = self.player_colour_dropdown.getSelected()

    def gen_widgets(self):
        self.player_colour_dropdown = Dropdown(
            App.window, self.rect.centerx + 0.05 * self.rect.width, self.rect.top + 0.3 * self.rect.height,
                        self.rect.width * 0.4, self.rect.height * 0.07, choices=['WHITE', 'BLACK'], direction='down',
            name=options['player_colour'], values=['WHITE', 'BLACK'], onClick=self.change_player_colour
        )
        self.widgets = [self.player_colour_dropdown]

    def resize(self):
        self.image = pygame.transform.smoothscale(
            self.orig_options_image, (
                (self.orig_options_image.get_width() / App.HIGH_RES[0]) * App.window.get_width(),
                (self.orig_options_image.get_height() / App.HIGH_RES[1]) * App.window.get_height()
            )
        )
        self.rect = self.image.get_rect(center=(App.window.get_width() / 2, App.window.get_height() / 2))
        self.gen_widgets()

    def close(self):
        with open('States/options.json', 'w') as f:
            json.dump(options, f)

    def update(self):
        self.draw()

    def draw(self):
        App.window.fill((9, 14, 23))
        App.window.blit(self.image, self.rect)
        for widget in self.widgets:
            widget.draw()
