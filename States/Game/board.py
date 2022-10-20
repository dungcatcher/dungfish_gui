class Board:
    def __init__(self):
        self.position = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, "wq", None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
