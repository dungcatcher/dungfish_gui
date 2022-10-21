import copy

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


def gen_pawn_moves(pos, board, only_capture=False):
    moves = []

    piece_colour, piece_id = board.position[pos[1]][pos[0]]

    direction = 1 if piece_colour == 'b' else -1
    # 2 from start
    if pos[1] == 1 and piece_colour == 'b' or pos[1] == 6 and piece_colour == 'w':
        vectors = [(0, direction), (0, 2 * direction)]
    else:
        vectors = [(0, direction)]
    capture_vectors = [(-1, direction), (1, direction)]

    if not only_capture:
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


def check_attacking_pieces(moves, board, target_pieces):
    for move in moves:
        target_piece = board.position[move.end[1]][move.end[0]]
        if target_piece:
            if target_piece[1] in target_pieces:
                return True

    return False


def filter_illegal_moves(moves, board):
    legal_moves = []
    #  Generates queen, knight and pawn moves from king position
    for move in moves:
        new_board = copy.deepcopy(board)
        new_board.make_move(move)

        king_pos = new_board.wk_pos if board.turn == 'w' else new_board.bk_pos
        print(king_pos)

        queen_moves = gen_queen_moves(king_pos, new_board)
        knight_moves = gen_knight_moves(king_pos, new_board)
        pawn_captures = gen_pawn_moves(king_pos, new_board, only_capture=True)

        if check_attacking_pieces(queen_moves, new_board, ['b', 'r', 'q']):
            continue
        if check_attacking_pieces(knight_moves, new_board, ['n']):
            continue
        if check_attacking_pieces(pawn_captures, new_board, ['p']):
            continue

        legal_moves.append(move)

    return legal_moves


def gen_moves(pos, board, turn):
    moves = []

    if board.position[pos[1]][pos[0]]:
        target_colour, target_id = board.position[pos[1]][pos[0]]
        if target_colour == turn:
            if target_id == 'p':
                moves = gen_pawn_moves(pos, board)
            elif target_id == 'n':
                moves = gen_knight_moves(pos, board)
            elif target_id == 'b':
                moves = gen_bishop_moves(pos, board)
            elif target_id == 'r':
                moves = gen_rook_moves(pos, board)
            elif target_id == 'q':
                moves = gen_queen_moves(pos, board)
            elif target_id == 'k':
                moves = gen_king_moves(pos, board)

    moves = filter_illegal_moves(moves, board)

    return moves
