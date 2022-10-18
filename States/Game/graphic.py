import pygame
from util import Spritesheet

piece_spritesheet = Spritesheet('./Assets/chess_pieces.png')

piece_letter_to_x_value = {
    'q': 0, 'k': 1, 'r': 2, 'n': 3, 'b': 4, 'p': 5
}
piece_colour_to_y_value = {
    'b': 0, 'w': 1
}


class GraphicalPieceGroup(pygame.sprite.Group):
    def resize(self, board_rect):
        print(board_rect)
        for spr in self.sprites():
            spr.image = pygame.transform.smoothscale(spr.orig_image, (board_rect.width / 8, board_rect.height / 8))
            spr.rect = spr.image.get_rect(
                center=(spr.board_rect.left + spr.pos[0] * board_rect.width / 8 + board_rect.width / 16,
                        spr.board_rect.top + spr.pos[1] * board_rect.height / 8 + board_rect.height / 16))


class GraphicalPiece(pygame.sprite.Sprite):
    def __init__(self, pos, board_rect, piece_id):
        super().__init__()
        self.pos = pos
        self.board_rect = board_rect
        self.piece_id = piece_id

        spritesheet_rect = pygame.Rect(
            piece_letter_to_x_value[piece_id[1]] * piece_spritesheet.piece_size,
            piece_colour_to_y_value[piece_id[0]] * piece_spritesheet.piece_size,
            piece_spritesheet.piece_size, piece_spritesheet.piece_size
        )
        self.orig_image = piece_spritesheet.get_image_at(spritesheet_rect)
        self.image = pygame.transform.smoothscale(self.orig_image, (board_rect.width / 8, board_rect.height / 8))
        self.rect = self.image.get_rect(center=(self.board_rect.left + self.pos[0] * board_rect.width / 8 + board_rect.width / 16,
                                                self.board_rect.top + self.pos[1] * board_rect.height / 8 + board_rect.height / 16))

