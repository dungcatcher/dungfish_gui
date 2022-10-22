import copy

from .constants import SQUARE_LETTER_TABLE


class Move:
    def __init__(self, start, end, flags=None, promotion_type=None):
        if flags is None:
            flags = []
        self.start = start
        self.end = end
        self.flags = flags
        self.promotion_type = promotion_type


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
            double_push = abs(vector[1]) == 2  # true or false
            test_square = (pos[0] + vector[0], pos[1] + vector[1])
            if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
                if not board.position[test_square[1]][test_square[0]]:
                    if not double_push:
                        if test_square[1] == 0 and board.turn == 'w' or test_square[1] == 7 and board.turn == 'b':
                            moves.append(Move(pos, test_square, flags=['promotion']))
                        else:
                            moves.append(Move(pos, test_square))
                    else:
                        moves.append(Move(pos, test_square, flags=['double push']))
                else:
                    break

    for capture_vector in capture_vectors:
        test_square = (pos[0] + capture_vector[0], pos[1] + capture_vector[1])
        if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
            if board.position[test_square[1]][test_square[0]]:
                if board.position[test_square[1]][test_square[0]][0] != piece_colour:
                    if test_square[1] == 0 and board.turn == 'w' or test_square[1] == 7 and board.turn == 'b':
                        moves.append(Move(pos, test_square, flags=['capture', 'promotion']))
                    else:
                        moves.append(Move(pos, test_square, flags=['capture']))
            else:
                if test_square == board.ep_square:
                    moves.append(Move(pos, test_square, flags=['enpassant']))

    return moves


def gen_absolute(pos, board, vectors):
    moves = []

    piece_colour, piece_id = board.position[pos[1]][pos[0]]

    for vector in vectors:
        test_square = (pos[0] + vector[0], pos[1] + vector[1])
        if 0 <= test_square[0] <= 7 and 0 <= test_square[1] <= 7:
            if board.position[test_square[1]][test_square[0]]:
                if board.position[test_square[1]][test_square[0]][0] != piece_colour:
                    moves.append(Move(pos, test_square, flags=['capture']))
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
                        moves.append(Move(pos, test_square, flags=['capture']))
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


def check_castling_possibility(board, king_pos, side):
    if board.castling[board.turn][side]:
        if not in_check(board):  # King is in check
            print(board.position[0 if board.turn == 'b' else 7][0 if side == 'queenside' else 7][1])
            vectors = [(-1, 0), (-2, 0)] if side == 'queenside' else [(1, 0), (2, 0)]

            for vector in vectors:
                test_square = (king_pos[0] + vector[0], king_pos[1] + vector[1])
                if not board.position[test_square[1]][test_square[0]]:  # Not occupied
                    new_board = copy.deepcopy(board)
                    fake_move = Move(king_pos, test_square)
                    new_board.make_move(fake_move)
                    print(new_board.print())

                    if in_check(new_board):
                        return False
                    if board.position[0 if board.turn == 'b' else 7][0 if side == 'queenside' else 7][1] != 'r':  # No rook
                        return False
                else:
                    return False
        else:
            return False
    else:
        return False

    return True


def gen_king_moves(pos, board, castling=True):
    moves = []

    vectors = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
    moves += gen_absolute(pos, board, vectors)

    # Castling
    if castling:
        queenside_possible = check_castling_possibility(board, pos, 'queenside')
        if queenside_possible:
            moves.append(Move(pos, (pos[0] - 2, pos[1]), flags=['queenside castle']))

        kingside_possible = check_castling_possibility(board, pos, 'kingside')
        if kingside_possible:
            moves.append(Move(pos, (pos[0] + 2, pos[1]), flags=['kingside castle']))

    return moves


def check_attacking_pieces(moves, board, target_pieces):
    for move in moves:
        target_piece = board.position[move.end[1]][move.end[0]]
        if target_piece:
            if target_piece[1] in target_pieces:
                return True

    return False


def in_check(board):
    king_pos = board.wk_pos if board.turn == 'w' else board.bk_pos

    rook_moves = gen_rook_moves(king_pos, board)
    bishop_moves = gen_bishop_moves(king_pos, board)
    knight_moves = gen_knight_moves(king_pos, board)
    pawn_captures = gen_pawn_moves(king_pos, board, only_capture=True)
    king_moves = gen_king_moves(king_pos, board, castling=False)

    if check_attacking_pieces(rook_moves, board, ['r', 'q']):
        return True
    if check_attacking_pieces(bishop_moves, board, ['b', 'q']):
        return True
    if check_attacking_pieces(knight_moves, board, ['n']):
        return True
    if check_attacking_pieces(pawn_captures, board, ['p']):
        return True
    if check_attacking_pieces(king_moves, board, ['k']):
        return True

    return False


def filter_illegal_moves(moves, board):
    legal_moves = []
    #  Generates queen, knight and pawn moves from king position
    for move in moves:
        new_board = copy.deepcopy(board)
        new_board.make_move(move)

        if not in_check(new_board):
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
