class Board:
    def __init__(self):
        self.position = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, "wq", None, None, None],
            [None, None, None, None, None, None, None, "bq"],
            [None, None, None, None, None, None, None, None],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        self.turn = 'w'
        self.wk_pos = (4, 7)
        self.bk_pos = (4, 0)

    def make_move(self, move):
        piece = self.position[move.start[1]][move.start[0]]

        self.position[move.end[1]][move.end[0]] = piece
        self.position[move.start[1]][move.start[0]] = None

        self.turn = 'b' if self.turn == 'w' else 'w'

        for y in range(8):
            for x in range(8):
                if self.position[y][x] == 'wk':
                    self.wk_pos = (x, y)
                if self.position[y][x] == 'bk':
                    self.bk_pos = (x, y)
