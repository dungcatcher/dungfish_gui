from .constants import SQUARE_LETTER_TABLE
from.engine import send_to_engine


class Board:
    def __init__(self):
        self.fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.position = self.load_fen(self.fen)

        self.turn = 'w'
        self.wk_pos = (4, 7)
        self.bk_pos = (4, 0)
        self.ep_square = None  # en passant target square
        self.castling = {
            'w': {'queenside': True, 'kingside': True},
            'b': {'queenside': True, 'kingside': True}
        }
        self.halfmoves = 0
        self.fullmoves = 1

    def print(self):
        string = ""
        for y in range(8):
            for x in range(8):
                piece = self.position[y][x]
                if piece:
                    if piece[0] == 'b':
                        string += piece[1]
                    else:
                        string += piece[1].upper()
                else:
                    string += '.'
            string += '\n'

        return string

    def load_fen(self, fen: str):
        position = [[None for _ in range(8)] for _ in range(8)]
        split_fen = fen.split()

        position_fen = split_fen[0]

        row = 0
        col = 0
        for char in position_fen:
            if char.isalpha():
                if char.isupper():
                    position[row][col] = f'w{char.lower()}'
                else:
                    position[row][col] = f'b{char}'
            if char.isnumeric():
                col += int(char)

            if char == '/':
                row += 1
                col = 0
            else:
                col += 1

        return position

    def get_fen(self):
        fen = ""

        # Piece locations
        empty = 0
        for y in range(8):
            for x in range(8):
                target_piece = self.position[y][x]
                if target_piece:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0

                    if target_piece[0] == 'b':
                        fen += target_piece[1]
                    else:
                        fen += target_piece[1].upper()
                else:
                    empty += 1

            if empty > 0:
                fen += str(empty)
                empty = 0
            if y != 7:
                fen += '/'

        # Turn
        fen += f' {self.turn}'

        castling_string = " "
        # Castling
        if self.castling['w']['kingside']:
            castling_string += 'K'
        if self.castling['w']['queenside']:
            castling_string += 'Q'
        if self.castling['b']['kingside']:
            castling_string += 'k'
        if self.castling['b']['queenside']:
            castling_string += 'q'

        if castling_string == " ":
            castling_string += '-'
        fen += castling_string

        # En passant
        if self.ep_square:
            square = SQUARE_LETTER_TABLE[self.ep_square[1]][self.ep_square[0]]
            fen += f' {square}'
        else:
            fen += ' -'

        # Moves
        fen += f' {self.halfmoves}'
        fen += f' {self.fullmoves}'

        return fen

    def make_move(self, move, real=False):  # real means it is played on the real board
        piece = self.position[move.start[1]][move.start[0]]

        if 'double push' in move.flags:
            if self.turn == 'w':
                self.ep_square = (move.start[0], move.end[1] + 1)
            else:
                self.ep_square = (move.start[0], move.end[1] - 1)
        else:
            self.ep_square = None

        # Update castling availability
        move_piece = self.position[move.start[1]][move.start[0]]
        if move_piece[1] == 'k':
            self.castling[move_piece[0]]['queenside'] = False
            self.castling[move_piece[0]]['kingside'] = False
        elif move_piece[1] == 'r':
            if move_piece[0] == 'w':
                if move.start == (0, 7):
                    self.castling['w']['queenside'] = False
                elif move.start == (7, 7):
                    self.castling['w']['kingside'] = False
            else:
                if move.start == (0, 0):
                    self.castling['b']['queenside'] = False
                elif move.start == (7, 0):
                    self.castling['b']['kingside'] = False

        self.position[move.end[1]][move.end[0]] = piece
        self.position[move.start[1]][move.start[0]] = None

        if 'enpassant' in move.flags:
            if self.turn == 'w':
                self.position[move.end[1] + 1][move.end[0]] = None
            else:
                self.position[move.end[1] - 1][move.end[0]] = None
        if 'queenside castle' in move.flags:
            self.position[move.end[1]][move.end[0] + 1] = self.position[move.end[1]][move.end[0] - 2]
            self.position[move.end[1]][move.end[0] - 2] = None
        if 'kingside castle' in move.flags:
            self.position[move.end[1]][move.end[0] - 1] = self.position[move.end[1]][move.end[0] + 1]
            self.position[move.end[1]][move.end[0] + 1] = None

        if 'promotion' in move.flags:
            if move.promotion_type:
                self.position[move.end[1]][move.end[0]] = (self.turn + move.promotion_type)

        for y in range(8):
            for x in range(8):
                if self.position[y][x] == 'wk':
                    self.wk_pos = (x, y)
                if self.position[y][x] == 'bk':
                    self.bk_pos = (x, y)

        self.halfmoves += 1
        if self.turn == 'b':
            self.fullmoves += 1

        if real:
            self.turn = 'b' if self.turn == 'w' else 'w'
            self.fen = self.get_fen()
            if self.turn == 'b':
                send_to_engine(f'position fen {self.fen}')
                send_to_engine(f'go movetime 1000')
