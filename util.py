import pygame
import pygame.freetype

from app import App


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet_img = pygame.image.load(filename).convert_alpha()
        self.piece_size = 106.5

    def get_image_at(self, rect):
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.spritesheet_img, (0, 0), rect)
        return image
