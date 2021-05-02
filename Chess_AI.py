import math
import copy
import chess
import random

PAWN_VALUE = 10
KNIGHT_VALUE = 30
BISHOP_VALUE = 40
ROOK_VALUE = 60
QUEEN_VALUE = 100
KING_VALUE = 800


class ChessNode:  # Value variable is for potential minimax or heuristic based search
    def __init__(self, chess_board, parent_node, visited_branch_set, value):
        self.chessBoard = chess_board
        self.parentNode = parent_node
        self.childNodes = []
        self.heuristic = value
        self.visitedBranchSet = visited_branch_set

    def set_children(self, child_nodes):
        self.childNodes = [self.childNodes + [x] for x in child_nodes if child_nodes]


# Creates a stage 1 new node
def nbr(board, move, parent, visited_branch):
    new_chessboard = copy.deepcopy(board)
    new_chessboard.push(move)
    new_chess_node = ChessNode(new_chessboard, parent, visited_branch, 0)
    return new_chess_node


def possible_moves(chess_node):
    return [nbr(chess_node, moves, chess_node, chess_node.visitedBranchSet.add(chess_node))
            for moves in list(chess_node.chessBoard.generate_legal_moves())]


def determine_value(captured_piece, player):
    if player == 1:
        if str(captured_piece) == 'p':
            return PAWN_VALUE
        if str(captured_piece) == 'n':
            return KNIGHT_VALUE
        if str(captured_piece) == 'b':
            return BISHOP_VALUE
        if str(captured_piece) == 'r':
            return ROOK_VALUE
        if str(captured_piece) == 'q':
            return QUEEN_VALUE
        if str(captured_piece) == 'k':
            return KING_VALUE
    else:
        if str(captured_piece) == 'P':
            return PAWN_VALUE
        if str(captured_piece) == 'N':
            return KNIGHT_VALUE
        if str(captured_piece) == 'B':
            return BISHOP_VALUE
        if str(captured_piece) == 'R':
            return ROOK_VALUE
        if str(captured_piece) == 'Q':
            return QUEEN_VALUE
        if str(captured_piece) == 'K':
            return KING_VALUE


def heuristic(state, player):
    for squareIndex in state.chessBoard.piece_map():
        state.heuristic = + determine_value(state.chessBoard.piece_at(squareIndex), player)


def max_value(state, max_depth, depth, alpha, beta):
    if state.is_game_over():
        return -900
    elif max_depth == depth:
        return heuristic(state, 1)
    else:
        state.heuristic = -math.inf
        for move in possible_moves(state):
            move.heuristic = heuristic(move, 1) - heuristic(move, -1)
            state.heuristic = max(state.heuristic, min_value(move, max_depth, depth + 1, alpha, beta))
            if state.heuristic >= beta:
                return state.heuristic
            alpha = max(alpha, state.heuristic)
    return state.heuristic


# min's move
def min_value(state, max_depth, depth, alpha, beta):
    if state.is_game_over():
        return 900
    elif max_depth == depth:
        return heuristic(state, -1)
    else:
        state.heuristic = math.inf
        for move in possible_moves(state):
            move.heuristic = heuristic(move, 1) - heuristic(move, -1)
            state.heuristic = min(state.heuristic, max_value(move, max_depth, depth + 1, alpha, beta))
            if state.heuristic <= alpha:
                return state.heuristic
            beta = min(beta, state.heuristic)
    return state.heuristic


#  main starting point for the heuristic_minimax algorithm
def heuristic_minimax(chess_state, max_depth, depth):
    return max_value(chess_state, max_depth, depth, -math.inf, math.inf)


def player_move(chessboard):
    print(chessboard)
    x = 1
    legal_moves = [str(y) for y in list(chessboard.legal_moves)]
    while x not in legal_moves:
        print('Enter move: ')
        x = input()
    for i in range(len(list(chessboard.legal_moves))):
        if str(list(chessboard.legal_moves)[i]) == x:
            chessboard.push(list(chessboard.legal_moves)[i])
            break
    print(chessboard)


def start_game(chessboard, minmax_depth, starting_depth, starting_player):
    if starting_player == 1:
        while not chessboard.chessBoard.is_game_over():
            chessboard.chessBoard.push(heuristic_minimax(chessboard, minmax_depth, starting_depth))
            player_move(chessboard.chessBoard)
    elif starting_player == -1:
        while not chessboard.chessBoard.is_game_over():
            player_move(chessboard.chessBoard)
            chessboard.chessBoard.push(heuristic_minimax(chessboard, minmax_depth, starting_depth))


def main(args):
    # At depth 10 player results are found
    chessboard = chess.Board()

    # while not chessboard.is_game_over():
    #     moves = list(chessboard.generate_legal_moves())
    #     move = moves[random.randint(0, len(moves) - 1)]
    #     chessboard.push(move)
    #     print('\n')
    #    print(chessboard)

    chessboard = chess.Board()
    state_state = ChessNode(chessboard, None, {}, 0)

    minmax_depth = 3
    starting_player = -1
    starting_depth = 0

    start_game(state_state, minmax_depth, starting_depth, starting_player)

    return 0


if __name__ == '__main__':
    import sys

    sys.setrecursionlimit(2000)
    sys.exit(main(sys.argv))
