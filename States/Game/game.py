import pygame

from States.state import State
from app import App
from .graphic import GraphicalPiece, PromotionPiece
from .board import Board
from .movegen import get_move_string


class Game(State):
    def __init__(self):
        super().__init__()
        self.board_segment_rect = pygame.Rect(0, 0, 0.7 * App.window.get_width(), App.window.get_height())

        self.orig_image = pygame.image.load('./Assets/board.png').convert_alpha()
        self.board_image = pygame.transform.smoothscale(
            self.orig_image, (
                (self.orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width(),
                (self.orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width()
            )
        )
        self.board = Board()
        self.board_rect = self.board_image.get_rect(center=self.board_segment_rect.center)
        self.pieces = []

        for y in range(8):
            for x in range(8):
                if self.board.position[y][x]:
                    self.pieces.append(GraphicalPiece((x, y), self.board_rect, self.board.position[y][x]))

        self.in_promotion = False
        self.promotion_move = None
        self.promotion_list = ['q', 'n', 'r', 'b']
        self.selected_promotion = None
        # Promotion images
        self.w_promotion_pieces = []
        self.b_promotion_pieces = []
        for i, piece_letter in enumerate(self.promotion_list):
            for colour in ['w', 'b']:
                promotion_piece = PromotionPiece(colour + piece_letter, self, i)
                if colour == 'w':
                    self.w_promotion_pieces.append(promotion_piece)
                else:
                    self.b_promotion_pieces.append(promotion_piece)

    def resize(self):
        self.board_image = pygame.transform.smoothscale(
            self.orig_image, (
                (self.orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width(),
                (self.orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width()
            )
        )
        self.board_segment_rect = pygame.Rect(0, 0, 0.7 * App.window.get_width(), App.window.get_height())
        self.board_rect = self.board_image.get_rect(center=self.board_segment_rect.center)

        for piece in self.pieces:
            piece.resize(self.board_rect)

    def update(self):
        if not self.in_promotion:
            for piece in self.pieces:
                piece.update(self)
        else:
            if self.board.turn == 'w':
                for promotion_piece in self.w_promotion_pieces:
                    promotion_piece.update(self)
            else:
                for promotion_piece in self.b_promotion_pieces:
                    promotion_piece.update(self)

            if self.selected_promotion:
                for piece in self.pieces:
                    if piece.pos == self.promotion_move.start:
                        self.promotion_move.promotion_type = self.selected_promotion
                        piece.make_move(self.promotion_move, self)
                        self.in_promotion = False
                        self.selected_promotion = None
                        self.promotion_move = None
                        break
        self.draw()

    def draw(self):
        App.window.fill((30, 30, 30))
        pygame.draw.rect(App.window, (20, 20, 20), self.board_segment_rect)

        App.window.blit(self.board_image, self.board_rect)
        for piece in self.pieces:
            piece.draw(self.board_rect)

        if self.in_promotion:
            transparent_surf = pygame.Surface(self.board_rect.size, pygame.SRCALPHA, 32)
            transparent_surf.fill((0, 0, 0, 64))
            App.window.blit(transparent_surf, self.board_rect)

            if self.board.turn == 'w':
                for promotion_piece in self.w_promotion_pieces:
                    promotion_piece.draw()
            else:
                for promotion_piece in self.b_promotion_pieces:
                    promotion_piece.draw()



