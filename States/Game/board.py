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

    def make_move(self, move, real=False):  # real means it is played on the real board
        piece = self.position[move.start[1]][move.start[0]]

        if real:
            if move.flags == 'double push':
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

        if move.flags == 'enpassant':
            if self.turn == 'w':
                self.position[move.end[1] + 1][move.end[0]] = None
            else:
                self.position[move.end[1] - 1][move.end[0]] = None

        self.turn = 'b' if self.turn == 'w' else 'w'

        for y in range(8):
            for x in range(8):
                if self.position[y][x] == 'wk':
                    self.wk_pos = (x, y)
                if self.position[y][x] == 'bk':
                    self.bk_pos = (x, y)
