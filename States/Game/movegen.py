from copy import copy

from .constants import SQUARE_LETTER_TABLE


class Move:
    def __init__(self, start, end, flags=None):
        self.start = start
        self.end = end
        self.flags = flags


def get_move_string(move):
    start_string = SQUARE_LETTER_TABLE[move.start[1]][move.start[0]]
    end_string = SQUARE_LETTER_TABLE[move.end[1]][move.end[0]]
    return start_string + end_string


def gen_pawn_moves(pos, board):
    moves = []

    piece_colour, piece_id = board.position[pos[1]][pos[0]]

    direction = 1 if piece_colour == 'b' else -1
    # 2 from start
    if pos[1] == 1 and piece_colour == 'b' or pos[1] == 6 and piece_colour == 'w':
        vectors = [(0, direction), (0, 2 * direction)]
    else:
        vectors = [(0, direction)]
    capture_vectors = [(-1, direction), (1, direction)]

    for vector in vectors:
        test_square = (pos[0] + vector[0], pos[1] + vector[1])
        if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
            if not board.position[test_square[1]][test_square[0]]:
                moves.append(Move(pos, test_square))
            else:
                break

    for capture_vector in capture_vectors:
        test_square = (pos[0] + capture_vector[0], pos[1] + capture_vector[1])
        if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
            if board.position[test_square[1]][test_square[0]]:
                if board.position[test_square[1]][test_square[0]][0] != piece_colour:
                    moves.append(Move(pos, test_square, flags='capture'))

    return moves


def gen_absolute(pos, board, vectors):
    moves = []

    piece_colour, piece_id = board.position[pos[1]][pos[0]]

    for vector in vectors:
        test_square = (pos[0] + vector[0], pos[1] + vector[1])
        if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
            if board.position[test_square[1]][test_square[0]]:
                if board.position[test_square[1]][test_square[0]][0] != piece_colour:
                    moves.append(Move(pos, test_square, flags='capture'))
            else:
                moves.append(Move(pos, test_square))

    return moves


def gen_sliding(pos, board, vectors):
    moves = []

    piece_colour, piece_id = board.position[pos[1]][pos[0]]

    for vector in vectors:
        new_pos = (pos[0], pos[1])

        blockage_found = False
        while not blockage_found:
            test_square = (new_pos[0] + vector[0], new_pos[1] + vector[1])
            if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
                if board.position[test_square[1]][test_square[0]]:
                    if board.position[test_square[1]][test_square[0]][0] != piece_colour:
                        moves.append(Move(pos, test_square, flags='capture'))
                    blockage_found = True
                else:
                    moves.append(Move(pos, test_square))
            else:
                blockage_found = True

            new_pos = test_square

    return moves


def gen_knight_moves(pos, board):
    vectors = [(-1, 2), (-1, -2), (1, 2), (1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
    return gen_absolute(pos, board, vectors)


def gen_bishop_moves(pos, board):
    vectors = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return gen_sliding(pos, board, vectors)


def gen_rook_moves(pos, board):
    vectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return gen_sliding(pos, board, vectors)


def gen_queen_moves(pos, board):
    return gen_rook_moves(pos, board) + gen_bishop_moves(pos, board)


def gen_king_moves(pos, board):
    vectors = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
    return gen_absolute(pos, board, vectors)


def filter_illegal_moves(moves, board):
    for move in moves:
        new_board = copy(board)
        new_board.make_move(move)


def gen_moves(pos, board, turn):
    if board.position[pos[1]][pos[0]]:
        target_colour, target_id = board.position[pos[1]][pos[0]]
        if target_colour == turn:
            if target_id == 'p':
                return gen_pawn_moves(pos, board)
            elif target_id == 'n':
                return gen_knight_moves(pos, board)
            elif target_id == 'b':
                return gen_bishop_moves(pos, board)
            elif target_id == 'r':
                return gen_rook_moves(pos, board)
            elif target_id == 'q':
                return gen_queen_moves(pos, board)
            elif target_id == 'k':
                return gen_king_moves(pos, board)

    return []
