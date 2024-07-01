import random
import copy
import numpy as np
import time

def create_DoRa_game(rows, cols):
    print('DoRa.py -> create_DoRa_game')
    row = [False for _ in range(cols)]
    board = [row.copy() for _ in range(rows)]
    return DoRaGame(board.copy())

class DoRaGame(object):

    # Required
    def __init__(self, board):
        print('DoRa.py -> DoRaGame __init__')
        self._board = board
        self.num_rows = len(board)
        self.num_cols = len(board[0])

    def get_board(self):
        print('DoRa.py -> get_board')
        return self._board

    def print_board(self):
        print('DoRa.py -> print_board')
        for row in self._board:
            print(row)
        print()

    def reset(self):
        print('DoRa.py -> reset')
        row = [False for _ in range(self.num_cols)]
        board = [row.copy() for _ in range(self.num_rows)]
        self._board = board.copy()

    def is_legal_move(self, row, col, vertical):
        # print('DoRa.py -> is_legal_move')
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
        # print('DoRa.py -> move_on_board')
        for square in DoRa:
            row = square[0]
            col = square[1]
            if row < 0 or row >= self.num_rows:
                return False
            if col < 0 or col >= self.num_cols:
                return False

        return True

    def move_on_free_space(self, DoRa):
        # print('DoRa.py -> move_on_free_space')
        for square in DoRa:
            row = square[0]
            col = square[1]

            if self._board[row][col] == True:
                return False

        return True

    def legal_moves(self, vertical):
        # print('DoRa.py -> legal_moves')
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.is_legal_move(row, col, vertical):
                    yield (row, col)

    def perform_move(self, row, col, vertical):
        # print('DoRa.py -> perform_move')
        if vertical:
            DoRa = ((row, col), (row+1, col))
        else:
            DoRa = ((row, col), (row, col+1))

        for square in DoRa:
            row = square[0]
            col = square[1]
            self._board[row][col] = True

    def game_over(self, vertical):
        print('DoRa.py -> game_over')
        moves = list(self.legal_moves(vertical))
        if len(moves) == 0:
            return True

        return False

    def copy(self):
        print('DoRa.py -> copy')
        return DoRaGame(copy.deepcopy(self._board))

    def successors(self, vertical):
        print('DoRa.py -> successors')
        for move in self.legal_moves(vertical):
            new_game = self.copy()
            new_game.perform_move(move[0], move[1], vertical)
            yield (move, new_game)

    def get_random_move(self, vertical):
        print('DoRa.py -> get_random_move')
        return random.choice(list(self.legal_moves(vertical)))
    
    # Alpha-Beta Pruning

    def get_alpha_beta_move(self, vertical, limit):
        print("DoRa.py -> get_alpha_beta_move -----------------------------------------------------------------------------------")
        self.first_move = vertical
        self.max_limit = limit
        self.leaf_counter = 0
        self.alpha_beta_move = ()

        v = self.alpha_beta_search(self.copy(), vertical)
        return (self.alpha_beta_move, int(v), self.leaf_counter)

    def alpha_beta_search(self, state, vertical):
        print('DoRa.py -> alpha_beta_search')
        v = self.max_value(state, vertical,  -np.inf, np.inf, 1)
        return v

    def max_value(self, state, vertical, alpha, beta, depth):
        print('DoRa.py -> max_values')
        if depth > self.max_limit or state.game_over(vertical):
            self.leaf_counter += 1
            return state.evaluate_board(state, vertical)

        v = -np.inf
        self.alpha_beta_move = next(state.legal_moves(vertical))
        for new_move, new_state in state.successors(vertical):
            new_vertical = not vertical
            new_v = np.max([v, self.min_value(new_state, new_vertical, alpha, beta, depth+1)])

            if new_v > v:
                self.alpha_beta_move = new_move

            v = new_v

            if v >= beta:
                return v
            alpha = np.max([alpha, v])

        return v

    def min_value(self, state, vertical, alpha, beta, depth):
        print('DoRa.py -> min_value')
        if depth > self.max_limit or state.game_over(vertical):
            self.leaf_counter += 1
            return state.evaluate_board(state, not vertical)

        v = np.inf
        for _, new_state in state.successors(vertical):
            new_vertical = not vertical
            v = np.min([v, self.max_value(new_state, new_vertical, alpha, beta, depth+1)])

            if v <= alpha:
                return v
            beta = np.min([beta, v])

        return v
    

    # Genetic Algorithm

    def get_genetic_algorithm_move(self, vertical, population_size, generations):
        print("DoRa.py -> get_genetic_algorithm_move -----------------------------------------------------------------------------------")
        population = self.initialize_population(population_size, vertical)
        
        for generation in range(generations):
            fitness_scores = [self.evaluate_individual(individual, vertical) for individual in population]
            selected_parents = self.select_parents(population, fitness_scores)
            offspring = self.crossover(selected_parents)
            mutated_offspring = [self.mutate(individual, vertical) for individual in offspring]
            population = mutated_offspring
            
        best_individual = max(population, key=lambda x: self.evaluate_individual(x, vertical))
        return best_individual[0], self.evaluate_individual(best_individual, vertical)

    def initialize_population(self, population_size, vertical):
        print('DoRa.py -> initialize_population')
        initial_population = []
        for _ in range(population_size):
            individual = [self.get_random_move(vertical) for _ in range(10)]
            initial_population.append(individual)
        return initial_population

    def evaluate_individual(self, individual, vertical):
        print('DoRa.py -> evaluate_individual')
        game_copy = self.copy()
        for move in individual:
            game_copy.perform_move(move[0], move[1], vertical)
        max_moves = list(game_copy.legal_moves(vertical))
        min_moves = list(game_copy.legal_moves(not vertical))
        return len(max_moves) - len(min_moves)

    def select_parents(self, population, fitness_scores):
        print('DoRa.py -> select_parents')
        selected_parents = []
        for _ in range(len(population)):
            candidates = random.sample(list(enumerate(population)), 2)
            candidate1, candidate2 = candidates[0], candidates[1]
            parent = candidate1 if fitness_scores[candidate1[0]] > fitness_scores[candidate2[0]] else candidate2
            selected_parents.append(parent)
        return selected_parents

    def crossover(self, selected_parents):
        print('DoRa.py -> crossover')
        offspring = []
        for parent1, parent2 in zip(selected_parents[::2], selected_parents[1::2]):
            crossover_point = random.randint(1, min(len(parent1[1]), len(parent2[1])) - 1)
            child1 = parent1[1][:crossover_point] + parent2[1][crossover_point:]
            child2 = parent2[1][:crossover_point] + parent1[1][crossover_point:]
            offspring.extend([child1, child2])
        return offspring

    def mutate(self, individual, vertical):
        print('DoRa.py -> mutate')
        mutation_point = random.randint(0, len(individual) - 1)
        individual[mutation_point] = self.get_random_move(vertical)
        return individual

    def evaluate_board(self, state, vertical):
        print('DoRa.py -> evaluate_board')
        max_moves = list(state.legal_moves(vertical))
        min_moves = list(state.legal_moves(not vertical))
        return len(max_moves) - len(min_moves)

    # Fuzzy Logic

    def get_fuzzy_logic_move(self, vertical):
        print("DoRa.py -> get_fuzzy_logic_move -----------------------------------------------------------------------------------")
        legal_moves = list(self.legal_moves(vertical))
        move_scores = []

        for move in legal_moves:
            simulated_game = self.copy()
            simulated_game.perform_move(move[0], move[1], vertical)
            move_scores.append(self.fuzzy_evaluate_board(simulated_game, vertical))

        best_move = legal_moves[np.argmax(move_scores)]
        return best_move

    def fuzzy_evaluate_board(self, game, vertical):
        print('DoRa.py -> fuzzy_evaluate_board')
        max_moves = len(list(game.legal_moves(vertical)))
        min_moves = len(list(game.legal_moves(not vertical)))

        # Fuzzy logic to evaluate the board
        score = 0

        if max_moves > min_moves:
            score += 0.7 * (max_moves - min_moves)
        else:
            score += 0.3 * (min_moves - max_moves)

        return score
