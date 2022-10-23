import pygame
import threading

from States.state import State
from app import App
from .graphic import GraphicalPiece, PromotionPiece
from .board import Board
from .engine import read_engine_output, Engine
from. constants import square_to_pos


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

        # Load all graphical pieces
        for y in range(8):
            for x in range(8):
                if self.board.position[y][x]:
                    self.pieces.append(GraphicalPiece((x, y), self.board_rect, self.board.position[y][x]))

        self.in_promotion = False
        self.promotion_move = None
        self.promotion_list = ['q', 'n', 'r', 'b']
        self.selected_promotion = None
        # Promotion images
        self.promotion_pieces = []
        for i, piece_letter in enumerate(self.promotion_list):
            for colour in ['w', 'b']:
                promotion_piece = PromotionPiece(colour + piece_letter, self, i)
                self.promotion_pieces.append(promotion_piece)

        self.player_colour = 'w'

        engine_thread = threading.Thread(name='read_engine_output', target=read_engine_output, daemon=True)
        engine_thread.start()
        # read_engine_output()

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
        for promotion_piece in self.promotion_pieces:
            promotion_piece.resize(self)

    def update(self):
        if self.board.turn == 'b':
            if Engine.best_move:
                start_pos = square_to_pos(Engine.best_move[0:2])
                end_pos = square_to_pos(Engine.best_move[2:])
                print(start_pos)

                for piece in self.pieces:
                    if piece.piece_string[0] == 'b':
                        if piece.pos == start_pos:
                            piece.gen_moves(self.board)
                            for move in piece.moves:
                                if move.end == end_pos:
                                    target_move = move
                                    piece.make_move(target_move, self)

        if not self.in_promotion:
            for piece in self.pieces:
                piece.update(self)
        else:
            for promotion_piece in self.promotion_pieces:
                if promotion_piece.piece_string[0] == self.board.turn:
                    promotion_piece.update(self)

            if self.selected_promotion:
                for piece in self.pieces:
                    if piece.pos == self.promotion_move.start:
                        self.promotion_move.promotion_type = self.selected_promotion
                        piece.make_move(self.promotion_move, self)
                        piece.hidden = False
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

            for promotion_piece in self.promotion_pieces:
                if promotion_piece.piece_string[0] == self.board.turn:
                    promotion_piece.draw()
