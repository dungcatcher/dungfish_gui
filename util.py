import pygame
import pygame.freetype

from app import App


class Button:
    def __init__(self, pos, text, target_state):
        self.pos = pos
        self.text = text
        self.target_state = target_state

        self.orig_image = pygame.image.load('./Assets/button.png').convert_alpha()
        self.image = pygame.transform.smoothscale(
            self.orig_image, (
                (self.orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width(),
                (self.orig_image.get_height() / App.HIGH_RES[1]) * App.window.get_height()
            )
        )
        self.rect = self.image.get_rect(
            center=(self.pos[0] * App.window.get_width(), self.pos[1] * App.window.get_height()))
        self.font = pygame.freetype.SysFont('arial', self.rect.height * 0.5)

        self.hovered = False

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

    def resize(self):
        self.image = pygame.transform.smoothscale(
            self.orig_image, (((self.orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width()),
            (self.orig_image.get_height() / App.HIGH_RES[1]) * App.window.get_height())
        )
        self.rect = self.image.get_rect(
            center=(self.pos[0] * App.window.get_width(), self.pos[1] * App.window.get_height()))
        self.font.size = self.rect.height * 0.7

    def draw(self):
        App.window.blit(self.image, self.rect)

        text_colour = (255, 255, 255) if self.hovered else (200, 200, 200)
        text_surf, text_rect = self.font.render(self.text, text_colour)
        text_rect.center = self.rect.center
        App.window.blit(text_surf, text_rect)


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet_img = pygame.image.load(filename).convert_alpha()
        self.piece_size = 60

    def get_image_at(self, rect):
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.spritesheet_img, (0, 0), rect)
        return image
