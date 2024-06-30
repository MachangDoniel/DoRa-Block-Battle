import random
import copy
import numpy as np


def create_DoRa_game(rows, cols):
    row = [False for _ in range(cols)]
    board = [row.copy() for _ in range(rows)]
    return DoRaGame(board.copy())


class DoRaGame(object):

    # Required
    def __init__(self, board):
        self._board = board
        self.num_rows = len(board)
        self.num_cols = len(board[0])

    def get_board(self):
        return self._board

    def print_board(self):
        for row in self._board:
            print(row)
        print()

    def reset(self):
        row = [False for _ in range(self.num_cols)]
        board = [row.copy() for _ in range(self.num_rows)]
        self._board = board.copy()

    def is_legal_move(self, row, col, vertical):
        if vertical:
            DoRa = ((row, col), (row+1, col))
        else:
            DoRa = ((row, col), (row, col+1))

        if not self.move_on_board(DoRa):
            return False

        if not self.move_on_free_space(DoRa):
            return False

        return True

    def move_on_board(self, DoRa):
        for square in DoRa:
            row = square[0]
            col = square[1]
            if row < 0 or row >= self.num_rows:
                return False
            if col < 0 or col >= self.num_cols:
                return False

        return True

    def move_on_free_space(self, DoRa):
        for square in DoRa:
            row = square[0]
            col = square[1]

            if self._board[row][col] == True:
                return False

        return True

    def legal_moves(self, vertical):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.is_legal_move(row, col, vertical):
                    yield (row, col)

    def perform_move(self, row, col, vertical):
        if vertical:
            DoRa = ((row, col), (row+1, col))
        else:
            DoRa = ((row, col), (row, col+1))

        for square in DoRa:
            row = square[0]
            col = square[1]
            self._board[row][col] = True

    def game_over(self, vertical):
        moves = list(self.legal_moves(vertical))
        if len(moves) == 0:
            return True

        return False

    def copy(self):
        return DoRaGame(copy.deepcopy(self._board))

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            new_game = self.copy()
            new_game.perform_move(move[0], move[1], vertical)
            yield (move, new_game)

    def get_random_move(self, vertical):
        return random.choice(list(self.legal_moves(vertical)))

    def evaluate_board(self, state, vertical):
        max_moves = list(state.legal_moves(vertical))
        min_moves = list(state.legal_moves(not vertical))

        return len(max_moves) - len(min_moves)
