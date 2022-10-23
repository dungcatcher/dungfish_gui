import pygame
import threading

from util import Spritesheet
from .movegen import gen_moves
from app import App

piece_spritesheet = Spritesheet('./Assets/chess_pieces.png')

piece_letter_to_x_value = {
    'k': 0, 'q': 1, 'b': 2, 'n': 3, 'r': 4, 'p': 5
}
piece_colour_to_y_value = {
    'w': 0, 'b': 1
}

move_sound = pygame.mixer.Sound('./Assets/move.ogg')
capture_sound = pygame.mixer.Sound('./Assets/capture.ogg')


class GraphicalPiece:
    def __init__(self, pos, board_rect, piece_string):
        self.pos = pos
        self.piece_string = piece_string

        self.orig_image = None
        self.image = None
        self.rect = None
        self.prev_rect = None
        self.ghost_img = None
        self.load_image_from_piece_string(board_rect, piece_string)

        self.orig_move_circle = pygame.image.load('./Assets/move_circle.png').convert_alpha()
        self.move_circle = pygame.transform.smoothscale(self.orig_move_circle,
                                                        (board_rect.width / 8, board_rect.height / 8))
        self.orig_capture_marker = pygame.image.load('./Assets/capture_marker.png').convert_alpha()
        self.capture_marker = pygame.transform.smoothscale(self.orig_capture_marker,
                                                           (board_rect.width / 8, board_rect.height / 8))
        self.dragging = False
        self.selected = False
        self.hidden = False

        self.moves = []

    def load_image_from_piece_string(self, board_rect, piece_string):
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
        if 'capture' in move.flags:
            for piece in game.pieces:
                if piece.pos == move.end:
                    game.pieces.remove(piece)
        if 'enpassant' in move.flags:
            for piece in game.pieces:
                if game.board.turn == 'w':
                    if piece.pos == (move.end[0], move.end[1] + 1):
                        game.pieces.remove(piece)
                else:
                    if piece.pos == (move.end[0], move.end[1] - 1):
                        game.pieces.remove(piece)
        if 'queenside castle' in move.flags:
            for piece in game.pieces:
                if piece.pos == (move.end[0] - 2, move.end[1]):
                    piece.pos = (move.end[0] + 1, move.end[1])
                    piece.resize(game.board_rect)
        if 'kingside castle' in move.flags:
            for piece in game.pieces:
                if piece.pos == (move.end[0] + 1, move.end[1]):
                    piece.pos = (move.end[0] - 1, move.end[1])
                    piece.resize(game.board_rect)

        if 'promotion' not in move.flags:
            self.pos = move.end
            self.resize(game.board_rect)
            self.selected = False
            self.moves = []
            game.board.make_move(move, real=True)
        else:
            if move.promotion_type:
                self.pos = move.end
                self.load_image_from_piece_string(game.board_rect, self.piece_string[0] + move.promotion_type)
                self.selected = False
                self.moves = []
                game.board.make_move(move, real=True)
            else:
                self.hidden = True
                game.in_promotion = True
                game.promotion_move = move

        if 'capture' not in move.flags:
            move_sound.play()
        else:
            if not ('promotion' in move.flags and move.promotion_type):
                capture_sound.play()
            if 'enpassant' in move.flags:
                capture_sound.play()

    def update(self, game):
        square_hovering = (int((pygame.mouse.get_pos()[0] - game.board_rect.left) // (game.board_rect.width / 8)),
                           int((pygame.mouse.get_pos()[1] - game.board_rect.top) // (game.board_rect.height / 8)))

        if App.left_click:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if game.board.turn == self.piece_string[0]:
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
        if not self.hidden:
            if self.selected:
                App.window.blit(self.ghost_img, self.prev_rect)
                for move in self.moves:
                    if 'capture' in move.flags or 'enpassant' in move.flags:
                        image = self.capture_marker
                    else:
                        image = self.move_circle

                    marker_rect = image.get_rect(
                        center=(board_rect.left + move.end[0] * board_rect.width / 8 + board_rect.width / 16,
                                board_rect.top + move.end[1] * board_rect.height / 8 + board_rect.height / 16))
                    App.window.blit(image, marker_rect)

            App.window.blit(self.image, self.rect)


class PromotionPiece:
    def __init__(self, piece_string, game, index):
        self.index = index
        self.piece_string = piece_string
        spritesheet_rect = pygame.Rect(
            piece_letter_to_x_value[piece_string[1]] * piece_spritesheet.piece_size,
            piece_colour_to_y_value[piece_string[0]] * piece_spritesheet.piece_size,
            piece_spritesheet.piece_size, piece_spritesheet.piece_size
        )
        self.orig_image = piece_spritesheet.get_image_at(spritesheet_rect)
        self.image = pygame.transform.smoothscale(self.orig_image, (game.board_rect.width / 8, game.board_rect.height / 8))
        self.rect = self.image.get_rect()
        self.hovered = False

    def resize(self, game):
        self.image = pygame.transform.smoothscale(self.orig_image, (game.board_rect.width / 8, game.board_rect.height / 8))
        self.rect = self.image.get_rect()

    def update(self, game):
        offset = -self.index if self.piece_string[0] == 'b' else self.index

        self.rect.topleft = (game.board_rect.left + (game.board_rect.width / 8) * (game.promotion_move.end[0]),
                             game.board_rect.top + (game.board_rect.height / 8) * (game.promotion_move.end[1] + offset))

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
            if App.left_click:
                game.selected_promotion = self.piece_string[1]
        else:
            self.hovered = False

    def draw(self):
        bg_colour = (255, 255, 255) if not self.hovered else (200, 200, 200)

        pygame.draw.rect(App.window, bg_colour, self.rect)
        App.window.blit(self.image, self.rect)
