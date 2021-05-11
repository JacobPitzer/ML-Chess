import math
import copy
import chess
import random

import pandas as pd

PAWN_VALUE = 100
PAWN_POS = [0, 0, 0, 0, 0, 0, 0, 0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5, 5, 10, 25, 25, 10, 5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, -5, -10, 0, 0, -10, -5, 5,
            5, 10, 10, -20, -20, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]
pawn_pos = [0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]
KNIGHT_VALUE = 300
KNIGHT_POS = [-50, -40, -30, -30, -30, -30, -40, -50,
              -40, -20, 0, 0, 0, 0, -20, -40,
              -30, 0, 10, 15, 15, 10, 0, -30,
              -30, 5, 15, 20, 20, 15, 5, -30,
              -30, 0, 15, 20, 20, 15, 0, -30,
              -30, 5, 10, 15, 15, 10, 5, -30,
              -40, -20, 0, 5, 5, 0, -20, -40,
              -50, -40, -30, -30, -30, -30, -40, -50]
BISHOP_VALUE = 400
BISHOP_POS = [-20, -10, -10, -10, -10, -10, -10, -20,
              -10, 0, 0, 0, 0, 0, 0, -10,
              -10, 0, 5, 10, 10, 5, 0, -10,
              -10, 5, 5, 10, 10, 5, 5, -10,
              -10, 0, 10, 10, 10, 10, 0, -10,
              -10, 10, 10, 10, 10, 10, 10, -10,
              -10, 5, 0, 0, 0, 0, 5, -10,
              -20, -10, -10, -10, -10, -10, -10, -20]
bishop_pos = [-20, -10, -10, -10, -10, -10, -10, -20,
              -10, 5, 0, 0, 0, 0, 5, -10,
              -10, 10, 10, 10, 10, 10, 10, -10,
              -10, 0, 10, 10, 10, 10, 0, -10,
              -10, 5, 5, 10, 10, 5, 5, -10,
              -10, 0, 5, 10, 10, 5, 0, -10,
              -10, 0, 0, 0, 0, 0, 0, -10,
              -20, -10, -10, -10, -10, -10, -10, -20]
ROOK_VALUE = 600
ROOK_POS = [0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, 10, 10, 10, 10, 5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            0, 0, 0, 5, 5, 0, 0, 0]
rook_pos = [0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            0, 0, 0, 5, 5, 0, 0, 0]
QUEEN_VALUE = 1000
QUEEN_POS = [-20, -10, -10, -5, -5, -10, -10, -20,
             -10, 0, 0, 0, 0, 0, 0, -10,
             -10, 0, 5, 5, 5, 5, 0, -10,
             -5, 0, 5, 5, 5, 5, 0, -5,
             0, 0, 5, 5, 5, 5, 0, -5,
             -10, 5, 5, 5, 5, 5, 0, -10,
             -10, 0, 5, 0, 0, 0, 0, -10,
             -20, -10, -10, -5, -5, -10, -10, -20]
queen_pos = [-20, -10, -10, -5, -5, -10, -10, -20
             - 10, 0, 5, 0, 0, 0, 0, -10,
             -10, 5, 5, 5, 5, 5, 0, -10,
             0, 0, 5, 5, 5, 5, 0, -5,
             -5, 0, 5, 5, 5, 5, 0, -5,
             -10, 0, 5, 5, 5, 5, 0, -10,
             -10, 0, 0, 0, 0, 0, 0, -10,
             -20, -10, -10, -5, -5, -10, -10, -20, ]
KING_VALUE = 8000
KING_POS = [-30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            20, 20, 0, 0, 0, 0, 20, 20,
            20, 30, 10, 0, 0, 10, 30, 20]
king_pos = [20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30, ]

DATAFRAME_WIDTH = ((64 * 3) + 1)
BOARD_TILE_WIDTH = 8


def generate_state_frame(state, moveList):
    df = pd.read_csv('data.csv')
    frameColumnNames = list(df.columns.values)

    dataFrameArray = [[0 for i in range(DATAFRAME_WIDTH)] for j in range(len(moveList))]
    # 2D arrays have to be declared strangely or values become linked together

    for squareIndex in range(BOARD_TILE_WIDTH * BOARD_TILE_WIDTH):
        for row in range(len(moveList)):
            dataFrameArray[row][squareIndex] = str(state.chessBoard.piece_at(squareIndex))
    # For each square on the board from 0 to 63, copy the piece to the current index of the array

    for moveIndex in range(len(moveList)):
        toSquareColumn = ("to_" + chess.SQUARE_NAMES[moveList[moveIndex].to_square])
        fromSquareColumn = ("from_" + chess.SQUARE_NAMES[moveList[moveIndex].from_square])

        toColumnIndex = frameColumnNames.index(toSquareColumn)
        fromColumnIndex = frameColumnNames.index(fromSquareColumn)

        dataFrameArray[moveIndex][toColumnIndex] = 1
        dataFrameArray[moveIndex][fromColumnIndex] = 1

        # For each move available in the current state, record where that move is from and going to on the board

    print("Check frame states")


class ChessNode:  # Value variable is for potential minimax or heuristic based search
    def __init__(self, chess_board, parent_node, move, visited_branch_set):
        self.chessBoard = chess_board
        self.parentNode = parent_node
        self.move_made = move
        self.childNodes = []
        self.heuristic = 0
        self.visitedBranchSet = visited_branch_set


# Creates a new node of the state of the board
def nbr(board, move, parent, visited_branch, ai_move):
    new_chessboard = copy.deepcopy(board)
    visited_branch.add(parent)
    new_chessboard.push(move)
    if parent.move_made is not None:
        move = parent.move_made
    new_chess_node = ChessNode(new_chessboard, parent, move, visited_branch)
    return new_chess_node


# Generates a list of possible moves on the board
def possible_moves(chess_node, ai_move):
    neighbors = []
    for moves in list(chess_node.chessBoard.legal_moves):
        neighbors.append(nbr(chess_node.chessBoard, moves, chess_node,
                             chess_node.visitedBranchSet, ai_move))
    return neighbors


# Determining the value of a piece and its location on the board
def determine_value(index_piece, squareIndex, ai_move):
    if ai_move == -1:
        if str(index_piece) == 'p':
            return PAWN_VALUE + pawn_pos[squareIndex]
        if str(index_piece) == 'n':
            return KNIGHT_VALUE + KNIGHT_POS[squareIndex]
        if str(index_piece) == 'b':
            return BISHOP_VALUE + bishop_pos[squareIndex]
        if str(index_piece) == 'r':
            return ROOK_VALUE + rook_pos[squareIndex]
        if str(index_piece) == 'q':
            return QUEEN_VALUE + queen_pos[squareIndex]
        if str(index_piece) == 'k':
            return KING_VALUE + king_pos[squareIndex]
        return 0
    else:
        if str(index_piece) == 'P':
            return PAWN_VALUE + pawn_pos[squareIndex]
        if str(index_piece) == 'N':
            return KNIGHT_VALUE + KNIGHT_POS[squareIndex]
        if str(index_piece) == 'B':
            return BISHOP_VALUE + BISHOP_POS[squareIndex]
        if str(index_piece) == 'R':
            return ROOK_VALUE + ROOK_POS[squareIndex]
        if str(index_piece) == 'Q':
            return QUEEN_VALUE + QUEEN_POS[squareIndex]
        if str(index_piece) == 'K':
            return KING_VALUE + KING_POS[squareIndex]
        return 0


# Heuristic calculations
def heuristic(state, ai_move):
    for squareIndex in state.chessBoard.piece_map():
        state.heuristic = state.heuristic + determine_value(state.chessBoard.piece_at(squareIndex), squareIndex,
                                                            ai_move)
        state.heuristic = state.heuristic - determine_value(state.chessBoard.piece_at(squareIndex), squareIndex,
                                                            -ai_move)
    return state


def best_max_state(state, move, ai_move):
    heuristic(move, ai_move)
    if state.heuristic > move.heuristic:
        return state
    return move


def max_value(state, max_depth, depth, alpha, beta, ai_move):
    if state.chessBoard.is_game_over():
        state.heuristic = -9000
        return state
    elif max_depth == depth:
        return heuristic(state, ai_move)
    else:
        state.heuristic = -math.inf
        for move in possible_moves(state, ai_move):
            state = best_max_state(state, min_value(move, max_depth, depth + 1, alpha, beta, ai_move), ai_move)
            if state.heuristic >= beta:
                return state
            alpha = max(alpha, state.heuristic)
    return state


def best_min_move(state, move, ai_move):
    heuristic(move, -ai_move)
    if state.heuristic < move.heuristic:
        return state
    return move


# min's move
def min_value(state, max_depth, depth, alpha, beta, ai_move):
    if state.chessBoard.is_game_over():
        state.heuristic = 9000
        return state
    elif max_depth == depth:
        return heuristic(state, -ai_move)
    else:
        state.heuristic = math.inf
        for move in possible_moves(state, ai_move):
            state = best_min_move(state, max_value(move, max_depth, depth + 1, alpha, beta, ai_move), ai_move)
            if state.heuristic <= alpha:
                return state
            beta = min(beta, state.heuristic)
    return state


#  main starting point for the heuristic_minimax algorithm
def heuristic_minimax(chess_state, max_depth, depth, ai_move):
    return max_value(chess_state, max_depth, depth, -math.inf, math.inf, ai_move)


def player_move(chessboard):
    print(chessboard)
    x = None
    legal_moves = [str(y) for y in list(chessboard.legal_moves)]
    while x not in legal_moves:
        print('Enter move: ')
        x = input()
    for i in range(len(list(chessboard.legal_moves))):
        if str(list(chessboard.legal_moves)[i]) == x:
            chessboard.push(list(chessboard.legal_moves)[i])
            break
    print(chessboard)
    print('\n')


def start_game(chessboard, minimax_depth, starting_depth, starting_player):
    if starting_player == 1:
        while not chessboard.chessBoard.is_game_over():
            state_picked = heuristic_minimax(chessboard, minimax_depth, starting_depth, 1)
            chessboard.chessBoard.push(state_picked.move_made)
            player_move(chessboard.chessBoard)
    elif starting_player == -1:
        while not chessboard.chessBoard.is_game_over():
            player_move(chessboard.chessBoard)
            state_picked = heuristic_minimax(chessboard, minimax_depth, starting_depth, -1)
            chessboard.chessBoard.push(state_picked.move_made)
    print('Game Over!')


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

    moveList = list(start_state.chessBoard.generate_legal_moves())

    generate_state_frame(start_state, moveList)

    minimax_depth = 3
    starting_depth = 1
    starting_player = 1

    start_game(start_state, minimax_depth, starting_depth, starting_player)

    return 0


if __name__ == '__main__':
    import sys

    sys.setrecursionlimit(2000)
    sys.exit(main(sys.argv))
