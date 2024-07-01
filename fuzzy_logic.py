
import numpy as np

def fuzzify(value, min_value, max_value):
    """Converts a crisp value to a fuzzy value between 0 and 1."""
    return (value - min_value) / (max_value - min_value)

def defuzzify(fuzzy_value, min_value, max_value):
    """Converts a fuzzy value between 0 and 1 back to a crisp value."""
    return fuzzy_value * (max_value - min_value) + min_value

def evaluate_move(board, move, vertical):
    """Evaluates a move using fuzzy logic. The specifics depend on your game."""
    row, col = move
    # Define fuzzy rules and apply them to evaluate the move.
    # Example rule: Prefer central moves
    center_row = len(board) / 2
    center_col = len(board[0]) / 2
    distance_to_center = abs(center_row - row) + abs(center_col - col)
    
    # Fuzzify the distance
    fuzzy_distance = fuzzify(distance_to_center, 0, center_row + center_col)
    
    # Other rules can be added here

    # Combine fuzzy values (e.g., using weighted average)
    move_score = 1 - fuzzy_distance  # Higher score for moves closer to the center

    # Return the defuzzified score
    return defuzzify(move_score, 0, 1)

def get_fuzzy_logic_move(game, vertical):
    """Select the best move based on fuzzy logic."""
    best_move = None
    best_score = -np.inf
    
    for row in range(len(game.board)):
        for col in range(len(game.board[0])):
            if game.is_legal_move(row, col, vertical):
                move = (row, col)
                score = evaluate_move(game.board, move, vertical)
                if score > best_score:
                    best_score = score
                    best_move = move

    return best_move
