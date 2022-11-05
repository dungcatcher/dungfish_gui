import pygame
import pygame.freetype
import math
from time import gmtime

from States.options import options
from app import App


def parse_starting_time():
    starting_time_string = options['clock_time']
    split_starting_time_string = starting_time_string.split('+')

    starting_time = int(split_starting_time_string[0])
    increment = int(split_starting_time_string[1])
    starting_time *= 60  # Convert to seconds

    return starting_time, increment


class Clock:
    def __init__(self, game, colour):
        self.colour = colour
        self.starting_time, self.increment = parse_starting_time()
        self.container_rect = pygame.Rect(0, 0, game.board_rect.width,
                                          (game.board_segment_rect.height - game.board_rect.height) / 2)
        if colour == game.player_colour:
            self.container_rect.topleft = game.board_rect.bottomleft
        else:
            self.container_rect.bottomleft = game.board_rect.topleft
        self.name_font = pygame.freetype.SysFont('arial', int(self.container_rect.height * 0.4))
        self.time_font = pygame.freetype.SysFont('courier', int(self.container_rect.height * 0.4))
        self.paused = True
        self.timeout = False

        self.time_remaining = 10

    def press(self):
        self.paused = True
        self.time_remaining += self.increment

    def depress(self):
        self.paused = False

    def reset(self):
        self.time_remaining = self.starting_time
        self.paused = True
        self.timeout = False

    def resize(self, game):
        self.container_rect = pygame.Rect(0, 0, game.board_rect.width,
                                          (game.board_segment_rect.height - game.board_rect.height) / 2)
        if self.colour == game.player_colour:
            self.container_rect.topleft = game.board_rect.bottomleft
        else:
            self.container_rect.bottomleft = game.board_rect.topleft
        self.name_font.size = int(self.container_rect.height * 0.4)
        self.time_font.size = int(self.container_rect.height * 0.4)

    def update(self, game):
        if not self.paused:
            self.time_remaining -= App.dt
            if self.time_remaining <= 0:
                self.timeout = True
                game.board.state = 'timeout'
        self.get_time_string()

    def get_time_string(self):
        time_string = ""

        if self.timeout:
            return '00:00.00'

        time_struct = gmtime(self.time_remaining)
        if time_struct.tm_hour > 0:
            time_string += f'{time_struct.tm_hour}:'

        if len(str(time_struct.tm_min)) != 2:
            time_string += '0'
        time_string += f'{time_struct.tm_min}:'

        if len(str(time_struct.tm_sec)) != 2:
            time_string += '0'
        time_string += f'{time_struct.tm_sec}'

        if time_struct.tm_sec < 10 and time_struct.tm_min == 0:
            # keep trailing zeroes
            ms_diff = str('{:.2f}'.format(round(self.time_remaining - math.floor(self.time_remaining), 2)))
            decimals = ms_diff.split('.')[-1]

            time_string += f'.{decimals}'

        return time_string

    def draw(self, game):
        name_text = 'Human' if self.colour == game.player_colour else 'Dungfish'
        name_surf, name_rect = self.name_font.render(name_text, (255, 255, 255))
        name_rect.midleft = self.container_rect.midleft
        App.window.blit(name_surf, name_rect)

        time_string = self.get_time_string()
        time_surf, time_rect = self.time_font.render(time_string, (255, 255, 255))
        time_rect.midright = self.container_rect.midright
        App.window.blit(time_surf, time_rect)


