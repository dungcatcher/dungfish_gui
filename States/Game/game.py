import pygame

from States.state import State
from app import App
from .graphic import GraphicalPiece, GraphicalPieceGroup
from .board import Board
from .movegen import gen_moves


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
        self.pieces = GraphicalPieceGroup()

        moves = gen_moves((0, 1), self.board, 'b')
        for move in moves:
            print(move.start, move.end)

        for y in range(8):
            for x in range(8):
                if self.board.position[y][x]:
                    self.pieces.add(GraphicalPiece((x, y), self.board_rect, self.board.position[y][x]))

    def resize(self):
        self.board_image = pygame.transform.smoothscale(
            self.orig_image, (
                (self.orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width(),
                (self.orig_image.get_width() / App.HIGH_RES[0]) * App.window.get_width()
            )
        )
        self.board_segment_rect = pygame.Rect(0, 0, 0.7 * App.window.get_width(), App.window.get_height())
        self.board_rect = self.board_image.get_rect(center=self.board_segment_rect.center)

        self.pieces.resize(self.board_rect)

    def update(self):
        self.draw()

    def draw(self):
        App.window.fill((30, 30, 30))
        pygame.draw.rect(App.window, (20, 20, 20), self.board_segment_rect)

        App.window.blit(self.board_image, self.board_rect)
        self.pieces.draw(App.window)
