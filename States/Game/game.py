import pygame
import pygame.freetype
from pygame_widgets.button import Button
import threading

from States.state import State
from States.options import options
from app import App
from .graphic import GraphicalPiece, PromotionPiece
from .board import Board
from .engine import read_engine_output, Engine, send_to_engine
from .constants import square_to_pos, turn_to_word
from .clock import Clock


class Game(State):
    def __init__(self):
        super().__init__()
        self.board_segment_rect = pygame.Rect(0, 0, 0.7 * App.window.get_width(), App.window.get_height())
        self.move_segment_rect = pygame.Rect(0.7 * App.window.get_width(), 0, 0.3 * App.window.get_width(), App.window.get_height())
        self.player_colour = 'w' if options['player_colour'] == 'WHITE' else 'b'

        self.orig_image = pygame.image.load('./Assets/board.png').convert_alpha()
        board_size = min(0.75 * self.board_segment_rect.height, 0.75 * self.board_segment_rect.width)
        self.board_image = pygame.transform.smoothscale(
            self.orig_image, (board_size, board_size)
        )
        self.board_rect = self.board_image.get_rect(center=self.board_segment_rect.center)
        self.buttons = self.gen_buttons()

        self.orig_end_screen_image = pygame.image.load('./Assets/end_screen.png').convert_alpha()
        self.end_screen_image = pygame.transform.smoothscale(
            self.orig_end_screen_image, (0.6 * self.board_rect.width, 0.8 * self.board_rect.height)
        )
        self.end_screen_rect = self.end_screen_image.get_rect(center=self.board_rect.center)
        self.end_screen_font = pygame.freetype.SysFont('arial', self.board_rect.height * 0.05)

        self.board = Board()
        self.pieces = []

        # Load all graphical pieces
        for y in range(8):
            for x in range(8):
                if self.board.position[y][x]:
                    self.pieces.append(GraphicalPiece((x, y), self, self.board.position[y][x]))

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

        self.clocks = [Clock(self, 'w'), Clock(self, 'b')]

        engine_thread = threading.Thread(name='read_engine_output', target=read_engine_output, daemon=True)
        engine_thread.start()

        if self.board.turn != self.player_colour:
            self.send_position_to_engine()

    def send_position_to_engine(self):
        if self.board.turn != self.player_colour and self.board.state == 'playing':
            for clock in self.clocks:
                if clock.colour != self.player_colour:
                    send_to_engine(f'{clock.colour}time {clock.time_remaining * 1000}')
                    send_to_engine(f'{clock.colour}inc {clock.increment * 1000}')

            send_to_engine(f'position fen {self.board.fen}')
            send_to_engine(f'go movetime 1000')

    def gen_buttons(self):
        buttons = [
            Button(
                App.window, self.move_segment_rect.centerx - int(0.3 * self.move_segment_rect.width),
                int(0.9 * self.move_segment_rect.height), int(0.6 * self.move_segment_rect.width),
                int(0.06 * self.move_segment_rect.height), onClick=lambda: self.reset(), text='RESTART'
            )
        ]
        return buttons

    def reset(self):
        self.board = Board()
        self.pieces = []
        Engine.best_move = None

        # Load all graphical pieces
        for y in range(8):
            for x in range(8):
                if self.board.position[y][x]:
                    self.pieces.append(GraphicalPiece((x, y), self, self.board.position[y][x]))

        for clock in self.clocks:
            clock.reset()

    def resize(self):
        self.board_segment_rect = pygame.Rect(0, 0, 0.7 * App.window.get_width(), App.window.get_height())
        self.move_segment_rect = pygame.Rect(0.7 * App.window.get_width(), 0, 0.3 * App.window.get_width(),
                                             App.window.get_height())

        board_size = min(0.75 * self.board_segment_rect.height, 0.75 * self.board_segment_rect.width)
        self.board_image = pygame.transform.smoothscale(
            self.orig_image, (board_size, board_size)
        )
        self.board_rect = self.board_image.get_rect(center=self.board_segment_rect.center)
        self.end_screen_image = pygame.transform.smoothscale(
            self.orig_end_screen_image, (0.6 * self.board_rect.width, 0.8 * self.board_rect.height)
        )
        self.end_screen_rect = self.end_screen_image.get_rect(center=self.board_rect.center)

        for piece in self.pieces:
            piece.resize(self)
        for promotion_piece in self.promotion_pieces:
            promotion_piece.resize(self)

        for clock in self.clocks:
            clock.resize(self)

        self.buttons = self.gen_buttons()

    def update(self):
        if turn_to_word[self.board.turn] != options['player_colour']:
            if Engine.best_move:
                start_pos = square_to_pos(Engine.best_move[0:2])
                end_pos = square_to_pos(Engine.best_move[2:])

                for piece in self.pieces:
                    if piece.piece_string[0] != self.player_colour:
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

        for clock in self.clocks:
            clock.update(self)

        self.draw()

    def draw(self):
        App.window.fill((30, 30, 30))
        pygame.draw.rect(App.window, (20, 20, 20), self.board_segment_rect)

        App.window.blit(self.board_image, self.board_rect)
        for piece in sorted(self.pieces, key=lambda a: a.selected):  # Selected pieces always above
            piece.draw(self)

        for button in self.buttons:
            button.draw()

        if self.in_promotion:
            transparent_surf = pygame.Surface(self.board_rect.size, pygame.SRCALPHA, 32)
            transparent_surf.fill((0, 0, 0, 64))
            App.window.blit(transparent_surf, self.board_rect)

            for promotion_piece in self.promotion_pieces:
                if promotion_piece.piece_string[0] == self.board.turn:
                    promotion_piece.draw()

        if self.board.state != 'playing':
            transparent_surf = pygame.Surface(self.board_rect.size, pygame.SRCALPHA, 32)
            transparent_surf.fill((0, 0, 0, 64))
            App.window.blit(transparent_surf, self.board_rect)

            App.window.blit(self.end_screen_image, self.end_screen_rect)
            if self.board.state == 'checkmate' or self.board.state == 'timeout':
                if self.board.turn == self.player_colour:
                    result = 'lost'
                else:
                    result = 'won'
            else:
                result = 'drew'

            text_surf, text_rect = self.end_screen_font.render(f'You {result} by {self.board.state}!', (255, 255, 255))
            text_rect.center = self.end_screen_rect.centerx, self.end_screen_rect.top + 0.15 * self.end_screen_rect.height
            App.window.blit(text_surf, text_rect)

        for clock in self.clocks:
            clock.draw(self)
