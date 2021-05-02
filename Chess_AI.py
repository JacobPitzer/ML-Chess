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
    def __init__(self, chess_board, parent_node, move, visited_branch_set):
        self.chessBoard = chess_board
        self.parentNode = parent_node
        self.move_made = move
        self.childNodes = []
        self.heuristic = 0
        self.visitedBranchSet = visited_branch_set

    def set_children(self, child_nodes):
        for x in child_nodes:
            if child_nodes:
                self.childNodes.append(x)


# Creates a stage 1 new node
def nbr(board, move, parent, visited_branch, ai_move):
    new_chessboard = copy.deepcopy(board)
    visited_branch.add(parent)
    new_chessboard.push(move)
    new_chess_node = ChessNode(new_chessboard, parent, move, visited_branch)
    heuristic(new_chess_node, ai_move)
    return new_chess_node


def possible_moves(chess_node, ai_move):
    neighbors = []
    for moves in list(chess_node.chessBoard.legal_moves):
        neighbors.append(nbr(chess_node.chessBoard, moves, chess_node,
                             chess_node.visitedBranchSet, ai_move))
    chess_node.set_children(neighbors)
    return neighbors


def determine_value(captured_piece, ai_move):
    if ai_move == 1:
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
        return 0
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
        return 0


def heuristic(state, ai_move):
    for squareIndex in state.chessBoard.piece_map():
        state.heuristic = state.heuristic + determine_value(state.chessBoard.piece_at(squareIndex), ai_move)
        state.heuristic = state.heuristic - determine_value(state.chessBoard.piece_at(squareIndex), -ai_move)
    return state


def max_value(state, max_depth, depth, alpha, beta, ai_move):
    if state.chessBoard.is_game_over():
        return -900
    elif max_depth == depth:
        return heuristic(state, ai_move)
    else:
        state.heuristic = -math.inf
        for move in possible_moves(state, ai_move):
            state.heuristic = max(state.heuristic, min_value(move, max_depth, depth + 1, alpha, beta, ai_move).heuristic)
            if state.heuristic >= beta:
                return state
            alpha = max(alpha, state.heuristic)
    return state


# min's move
def min_value(state, max_depth, depth, alpha, beta, ai_move):
    if state.chessBoard.is_game_over():
        return 900
    elif max_depth == depth:
        return heuristic(state, -ai_move)
    else:
        state.heuristic = math.inf
        for move in possible_moves(state, ai_move):
            state.heuristic = min(state.heuristic, max_value(move, max_depth, depth + 1, alpha, beta, ai_move).heuristic)
            if state.heuristic <= alpha:
                return state
            beta = min(beta, state.heuristic)
    return state


#  main starting point for the heuristic_minimax algorithm
def heuristic_minimax(chess_state, max_depth, depth, ai_move):
    best_value = -math.inf
    best_move = None
    for child in max_value(chess_state, max_depth, depth, -math.inf, math.inf, ai_move).childNodes:
        if child.heuristic > best_value:
            best_move = child
            best_value = child.heuristic
    return best_move


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
            chessboard.chessBoard.push(heuristic_minimax(chessboard, minmax_depth, starting_depth, 1))
            player_move(chessboard.chessBoard)
    elif starting_player == -1:
        while not chessboard.chessBoard.is_game_over():
            player_move(chessboard.chessBoard)
            this_sent_back = heuristic_minimax(chessboard, minmax_depth, starting_depth, -1).move_made
            chessboard.chessBoard.push(this_sent_back)


def main(args):
    # chessboard = chess.Board()
    # while not chessboard.is_game_over():
    #     moves = list(chessboard.generate_legal_moves())
    #     move = moves[random.randint(0, len(moves) - 1)]
    #     chessboard.push(move)
    #     print('\n')
    #    print(chessboard)

    chessboard = chess.Board()
    start_state = ChessNode(chessboard, None, None, set())

    minmax_depth = 3
    starting_player = -1
    starting_depth = 0

    start_game(start_state, minmax_depth, starting_depth, starting_player)

    return 0


if __name__ == '__main__':
    import sys

    sys.setrecursionlimit(2000)
    sys.exit(main(sys.argv))
