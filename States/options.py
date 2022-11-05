import pygame
import pygame.freetype
import json

from .state import State
from app import App
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.textbox import TextBox

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
        self.clock_textbox = None
        self.widgets = None
        self.widget_font = pygame.freetype.SysFont('arial', int(self.rect.height * 0.07 * 0.4))
        self.gen_widgets()

    def input_clock_time(self):
        text = self.clock_textbox.getText()
        split_text = text.split('+')
        if len(split_text) == 2:
            try:
                int(split_text[0])
                int(split_text[1])
            except ValueError:
                print('Put in a real number')

            options['clock_time'] = text
        else:
            print('starting time + increment')

    def gen_widgets(self):
        self.player_colour_dropdown = Dropdown(
            App.window, self.rect.centerx + 0.1 * self.rect.width, self.rect.top + 0.3 * self.rect.height,
            self.rect.width * 0.3, self.rect.height * 0.07, choices=['WHITE', 'BLACK'], direction='down',
            name=options['player_colour'], values=['WHITE', 'BLACK'], inactiveColour=(50, 50, 50),
            pressedColour=(60, 60, 60), hoverColour=(70, 70, 70), textColour=(200, 200, 200)
        )
        self.clock_textbox = TextBox(
            App.window, self.rect.centerx + 0.1 * self.rect.width, self.rect.top + 0.45 * self.rect.height,
            self.rect.width * 0.3, self.rect.height * 0.07, onSubmit=self.input_clock_time,
            placeholderText="e.g. 5+3", colour=(50, 50, 50), borderThickness=2, borderColour=(70, 70, 70),
            fontSize=int(self.rect.height * 0.07 * 0.8), textColour=(200, 200, 200)
        )

        self.widget_font.size = int(self.rect.height * 0.07 * 0.4)
        self.widgets = {
            'PLAYER COLOUR': self.player_colour_dropdown,
            'TIME PER SIDE': self.clock_textbox
        }

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
        if self.player_colour_dropdown.getSelected():
            options['player_colour'] = self.player_colour_dropdown.getSelected()

        self.draw()

    def draw(self):
        App.window.fill((9, 14, 23))
        App.window.blit(self.image, self.rect)
        for i, (widget_name, widget) in enumerate(reversed(self.widgets.items())):  # Reversed for drawing order
            i = len(self.widgets.keys()) - i - 1  # Reversed index since the dict is reversed

            rect = pygame.Rect(0, 0, self.rect.width * 0.9, self.rect.height * 0.1)
            rect.midtop = self.rect.centerx, self.rect.top + self.rect.height * (0.3 - 0.015) + i * self.rect.height * 0.15
            pygame.draw.rect(App.window, (20, 20, 20), rect, border_radius=5)

            text_surf, text_rect = self.widget_font.render(widget_name, (255, 255, 255))
            text_rect.center = rect.left + rect.width * 0.25, rect.centery
            App.window.blit(text_surf, text_rect)

            pygame.draw.line(App.window, (50, 50, 50), (rect.centerx, rect.top + 0.1 * rect.height),
                             (rect.centerx, rect.bottom - 0.1 * rect.height), width=2)

            widget.draw()
