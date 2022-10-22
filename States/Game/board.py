class Board:
    def __init__(self):
        self.position = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        self.turn = 'w'
        self.wk_pos = (4, 7)
        self.bk_pos = (4, 0)
        self.ep_square = None  # en passant target square
        self.castling = {
            'w': {'queenside': True, 'kingside': True},
            'b': {'queenside': True, 'kingside': True}
        }

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

        if real:
            self.turn = 'b' if self.turn == 'w' else 'w'
