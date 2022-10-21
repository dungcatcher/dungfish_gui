import pygame
from util import Spritesheet

from .movegen import gen_moves
from app import App

piece_spritesheet = Spritesheet('./Assets/chess_pieces.png')

piece_letter_to_x_value = {
    'q': 0, 'k': 1, 'r': 2, 'n': 3, 'b': 4, 'p': 5
}
piece_colour_to_y_value = {
    'b': 0, 'w': 1
}


class GraphicalPiece(pygame.sprite.Sprite):
    def __init__(self, pos, board_rect, piece_string):
        super().__init__()
        self.pos = pos
        self.piece_string = piece_string

        spritesheet_rect = pygame.Rect(
            piece_letter_to_x_value[piece_string[1]] * piece_spritesheet.piece_size,
            piece_colour_to_y_value[piece_string[0]] * piece_spritesheet.piece_size,
            piece_spritesheet.piece_size, piece_spritesheet.piece_size
        )
        self.orig_image = piece_spritesheet.get_image_at(spritesheet_rect)
        self.image = pygame.transform.smoothscale(self.orig_image, (board_rect.width / 8, board_rect.height / 8))
        self.rect = self.image.get_rect(
            center=(board_rect.left + self.pos[0] * board_rect.width / 8 + board_rect.width / 16,
                    board_rect.top + self.pos[1] * board_rect.height / 8 + board_rect.height / 16))
        self.prev_rect = self.rect.copy()  # Rect before dragging
        self.ghost_img = self.image.copy()
        self.ghost_img.set_alpha(64)

        self.orig_move_circle = pygame.image.load('./Assets/move_circle.png').convert_alpha()
        self.move_circle = pygame.transform.smoothscale(self.orig_move_circle,
                                                        (board_rect.width / 8, board_rect.height / 8))
        self.orig_capture_marker = pygame.image.load('./Assets/capture_marker.png').convert_alpha()
        self.capture_marker = pygame.transform.smoothscale(self.orig_capture_marker,
                                                           (board_rect.width / 8, board_rect.height / 8))
        self.dragging = False
        self.selected = False

        self.moves = []

    def resize(self, board_rect):
        self.image = pygame.transform.smoothscale(self.orig_image, (board_rect.width / 8, board_rect.height / 8))
        self.rect = self.image.get_rect(
            center=(board_rect.left + self.pos[0] * board_rect.width / 8 + board_rect.width / 16,
                    board_rect.top + self.pos[1] * board_rect.height / 8 + board_rect.height / 16))
        self.prev_rect = self.rect.copy()
        self.ghost_img = self.image.copy()
        self.ghost_img.set_alpha(64)
        self.move_circle = pygame.transform.smoothscale(self.orig_move_circle,
                                                        (board_rect.width / 8, board_rect.height / 8))
        self.capture_marker = pygame.transform.smoothscale(self.orig_capture_marker,
                                                           (board_rect.width / 8, board_rect.height / 8))

    def gen_moves(self, board):
        self.moves = gen_moves(self.pos, board, self.piece_string[0])

    def get_move(self, square):
        for move in self.moves:
            if square == move.end:
                return move

        return False

    def make_move(self, move, game):
        if move.flags == 'capture':
            for piece in game.pieces:
                if piece.pos == move.end:
                    game.pieces.remove(piece)
        self.pos = move.end
        self.resize(game.board_rect)
        self.selected = False
        self.moves = []

        game.board.make_move(move, real=True)

    def update(self, game):
        square_hovering = (int((pygame.mouse.get_pos()[0] - game.board_rect.left) // (game.board_rect.width / 8)),
                           int((pygame.mouse.get_pos()[1] - game.board_rect.top) // (game.board_rect.height / 8)))

        if App.left_click:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if game.board.turn == self.piece_string[0]:
                    if not self.moves:
                        self.gen_moves(game.board)
                    self.selected = True
                    self.dragging = True
            else:
                if self.selected:
                    move = self.get_move(square_hovering)
                    if move:  # Is a move
                        self.make_move(move, game)
                    self.selected = False

        if pygame.mouse.get_pressed()[0]:
            if self.selected:
                self.rect.center = pygame.mouse.get_pos()
        else:
            if self.dragging:
                move = self.get_move(square_hovering)
                if move:  # Is a move
                    self.make_move(move, game)
                else:
                    self.rect = self.prev_rect.copy()

                self.dragging = False

    def draw(self, board_rect):
        if self.selected:
            App.window.blit(self.ghost_img, self.prev_rect)
            for move in self.moves:
                if move.flags != 'capture':
                    image = self.move_circle
                else:
                    image = self.capture_marker

                marker_rect = image.get_rect(
                    center=(board_rect.left + move.end[0] * board_rect.width / 8 + board_rect.width / 16,
                            board_rect.top + move.end[1] * board_rect.height / 8 + board_rect.height / 16))
                App.window.blit(image, marker_rect)

        App.window.blit(self.image, self.rect)
