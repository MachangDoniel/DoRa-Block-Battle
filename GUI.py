import tkinter as tk
import random
import DoRa
import time


# variable

# alpha_beta_pruning
limit = 1
# genetic_algorithm
population_size = 100
generations = 100
delay = 100

class Square(tk.Canvas):
    COLOR_EMPTY = "gray"
    COLOR_FILLED_R = "red"
    COLOR_FILLED_B = "blue"

    def __init__(self, master, size=50):
        print('gui.py -> Square __init__')
        tk.Canvas.__init__(self, master, height=size, width=size,
                           background=Square.COLOR_EMPTY, highlightthickness=2,
                           highlightbackground="yellow")
        self.state = False
        self.vertical_color = True

    def set_state(self, state, vertical_color):
        # print('gui.py -> Square set_state')
        self.state = state
        self.vertical_color = vertical_color
        if self.state:
            color = Square.COLOR_FILLED_B if self.vertical_color else Square.COLOR_FILLED_R
        else:
            color = Square.COLOR_EMPTY
        self.configure(background=color)


class Board(tk.Frame):

    def __init__(self, master, game, rows, cols):
        print('gui.py -> Board __init__')
        tk.Frame.__init__(self, master)

        self.two_player = False
        self.mode = "AI"
        self.toss = False
        self.game = game
        self.vertical = True
        self.rows = rows
        self.cols = cols
        self.moved = False

        self.squares = []
        for row in range(rows):
            row_squares = []
            for col in range(cols):
                square = Square(self)
                square.grid(row=row, column=col, padx=1, pady=1)
                square.bind("<Button-1>", lambda event, row=row, col=col: self.perform_move_AI(row, col))
                row_squares.append(square)
            self.squares.append(row_squares)




    def perform_move(self, row, col):
        print('gui.py -> perform_move', self.mode)
        if self.game.is_legal_move(row, col, self.vertical) and self.toss:
            self.game.perform_move(row, col, self.vertical)
            self.squares[row][col].set_state(True, self.vertical)
            if self.vertical:
                self.squares[row+1][col].set_state(True, self.vertical)
            else:
                self.squares[row][col+1].set_state(True, self.vertical)
            self.vertical = not self.vertical
            self.update_squares()
            self.master.update_status()
            self.moved = True
        else:
            self.moved = False
    
    def perform_ai_move(self):
        print('gui.py -> perform_ai_move')
        if self.moved and not self.game.game_over(self.vertical):
            (row, col), best_value, total_leaves = \
                self.game.get_alpha_beta_move(self.vertical, 1)
            self.perform_move(row, col)

    def perform_ai2_move(self):
        print('gui.py -> perform_ai2_move')
        if self.moved and not self.game.game_over(self.vertical):
            row = col = fitness_value = -1
            while not self.game.is_legal_move(row, col, self.vertical):
                (row, col), fitness_value = \
                    self.game.get_genetic_algorithm_move(self.vertical, population_size = 10, generations = 10)
            self.perform_move(row, col)

    def perform_ai3_move(self):
        print('gui.py -> perform_ai3_move')
        if self.moved and not self.game.game_over(self.vertical):
            row = col = best_value = -1
            while not self.game.is_legal_move(row, col, self.vertical):
                (row, col), best_value = \
                    self.game.get_fuzzy_logic_move(self.vertical)
            self.perform_move(row, col)

    def perform_ai4_move(self):
        print('gui.py -> perform_ai4_move')
        if self.moved and not self.game.game_over(self.vertical):
            row = col = best_value = -1
            while not self.game.is_legal_move(row, col, self.vertical):
                (row, col), best_value = \
                    self.game.get_A_star_move(self.vertical)
            self.perform_move(row, col)
    
    def perform_move_AI(self, row, col):
        print('gui.py -> perform_move_AI', self.mode, self.two_player)
        self.perform_move(row, col)
        
        if self.mode == "AI":
            if self.moved:
                if not self.game.game_over(self.vertical):
                    self.after(delay, self.perform_ai_move)

        elif self.mode == "AI-2":
            if self.moved:
                if not self.game.game_over(self.vertical):
                    self.after(delay, self.perform_ai2_move)

        elif self.mode == "AI-3":
            if self.moved:
                if not self.game.game_over(self.vertical):
                    self.after(delay, self.perform_ai3_move)

        elif self.mode == "AI-4":
            if self.moved:
                if not self.game.game_over(self.vertical):
                    self.after(delay, self.perform_ai4_move)

        else:
            self.perform_move(row, col)


    def update_squares(self):
        print('gui.py -> update_squares', self.mode)
        game_board = self.game.get_board()
        for row in range(self.rows):
            for col in range(self.cols):
                square = self.squares[row][col]
                if game_board[row][col]:
                    square.set_state(True, square.vertical_color)
                else:
                    square.set_state(False, True)  # Reset to default empty state


class DoRaGUI(tk.Tk):

    def __init__(self):
        print('gui.py -> DoRaGUI __init__')
        tk.Tk.__init__(self)
        self.title("DoRa Game")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (MainPage, TossPage, BoardPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        print('gui.py -> show_frame')
        frame = self.frames[page_name]
        frame.tkraise()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        print('gui.py -> MainPage __init__')
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, bg="#4caf50", fg="white", text="DoRa Game", font=("Arial", 24))
        label.pack(pady=20)

        btn_start = tk.Button(self, bg="#4caf50", fg="white", text="Start", font=("Arial", 16),
                              command=self.start_game)
        btn_start.pack(pady=20)

    def start_game(self):
        print('GUI.py -> start_game')
        self.controller.show_frame("TossPage")


class TossPage(tk.Frame):

    def __init__(self, parent, controller):
        print('gui.py -> TossPage __init__')
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mode = "AI"

        self.label = tk.Label(self, fg="blue", text="", font=("Arial", 24))
        self.label.pack(pady=20)

        self.btn_toss = tk.Button(self, bg="#4caf50", fg="white", text="Toss", font=("Arial", 16),
                                  command=self.toss)
        self.btn_toss.pack(pady=50)

        self.btn_next = tk.Button(self, bg="#4caf50", fg="white", text="Next", font=("Arial", 16),
                                  command=self.go_to_board)
        self.btn_next.pack(pady=50)
        self.btn_next.pack_forget()  # Hide the Next button initially

    def toss(self):
        print('gui.py -> toss')
        toss_list = ['V', 'H']
        result = random.choice(toss_list)

        if result == 'V':
            self.controller.vertical = True
            result_text = "Vertical"
        else:
            self.controller.vertical = False
            result_text = "Horizontal"

        self.label.config(text="Toss Result: " + result_text)
        self.btn_next.pack(pady=10)  # Show the Next button after the toss

    def go_to_board(self):
        print('gui.py -> go_to_board')
        self.controller.show_frame("BoardPage")
        self.controller.frames["BoardPage"].set_up(self.mode, self.controller.vertical)


class BoardPage(tk.Frame):

    def __init__(self, parent, controller):
        print('gui.py -> BoardPage __init__')
        tk.Frame.__init__(self , parent)
        self.controller = controller
        self.board = None

    def set_up(self, mode, vertical):
        print('gui.py -> set_up - Mode:', mode)
        if self.board is not None:
            self.board.destroy()

        board_row = 6
        board_col = 6

        game = DoRa.create_DoRa_game(board_row, board_col)
        self.board = Board(self, game, board_col, board_col)
        self.board.two_player = (mode == "Two Player")
        self.board.mode = mode
        self.board.vertical = vertical
        self.board.toss = True
        self.board.pack(side=tk.LEFT, padx=1, pady=1)

        menu = tk.Frame(self)

        self.status_label = tk.Label(menu, fg="red", font=("Arial", 16))
        self.status_label.pack(padx=1, pady=(1, 10))
        self.update_status()

        tk.Label(menu, fg="blue", text="Press 'r' to perform a random move.").pack(padx=1, pady=1, anchor=tk.W)
        tk.Label(menu, fg="blue", text="Press 'a' to perform a best move of alpha_beta pruning.").pack(padx=1, pady=1, anchor=tk.W)
        tk.Label(menu, fg="blue", text="Press 'g' to perform a best move of genetic_algorithm.").pack(padx=1, pady=1, anchor=tk.W)
        tk.Label(menu, fg="blue", text="Press 'f' to perform a best move of fuzzy_logic.").pack(padx=1, pady=1, anchor=tk.W)
        tk.Label(menu, fg="blue", text="Press 's' to perform a best move of A_star.").pack(padx=1, pady=1, anchor=tk.W)
        

        tk.Button(menu, bg="#4caf50", fg="white", text="Two Player", command=self.two_player_move).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#4caf50", fg="white", text="Play with AI",command=self.auto_move).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#4caf50", fg="white", text="Play with AI-2", command=self.auto_move2).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#4caf50", fg="white", text="Play with AI-3", command=self.auto_move3).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#4caf50", fg="white", text="Play with AI-4", command=self.auto_move4).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#ff5050", fg="white", text="Reset Game", command=self.reset_click).pack(fill=tk.X, padx=1, pady=1)

        menu.pack(side=tk.RIGHT)

        self.focus_set()

        self.bind("r", lambda event: self.perform_random_move())
        self.bind("a", lambda event: self.perform_alpha_beta_move())
        self.bind("g", lambda event: self.perform_genetic_algorithm_move())
        self.bind("f", lambda event: self.perform_fuzzy_logic_move())
        self.bind("s", lambda event: self.perform_A_star_move())



    def reset_game(self):
        print('gui.py -> reset_game')
        # Reset game logic here if needed
        pass

    def update_status(self):
        print('gui.py -> update_status', self.board.mode)
        if self.board.game.game_over(self.board.vertical):
            winner = "Horizontal" if self.board.vertical else "Vertical"
            self.status_label.config(text=self.board.mode + "\n" + "Winner: " + winner)
        else:
            turn = "Vertical" if self.board.vertical else "Horizontal"
            self.status_label.config(text=f"{self.board.mode}\nTurn: {turn}")

    def reset_click(self):
        print("gui.py -> reset_click", self.board.mode)
        self.board.game.reset()
        self.board.update_squares()
        self.update_status()

    def auto_move(self):
        print("gui.py -> auto_move", self)
        self.reset_click()
        self.board.two_player = False
        self.board.mode = "AI"
        self.update_status()

    def auto_move2(self):
        print("gui.py -> auto_move2", self.board.mode)
        self.reset_click()
        self.board.two_player = False
        self.board.mode = "AI-2"
        self.update_status()

    def auto_move3(self):
        print("gui.py -> auto_move3", self.board.mode)
        self.reset_click()
        self.board.two_player = False
        self.board.mode = "AI-3"
        self.update_status()

    def auto_move4(self):
        print("gui.py -> auto_move3", self.board.mode)
        self.reset_click()
        self.board.two_player = False
        self.board.mode = "AI-4"
        self.update_status()

    def two_player_move(self):
        print("gui.py -> two_player_move", self.board.mode)
        self.reset_click()
        self.board.two_player = True
        self.board.mode = "Two Player"
        self.update_status()

    def perform_random_move(self):
        print("gui.py -> perform_random_move", self.board.mode)
        if not self.board.game.game_over(self.board.vertical):
            row, col = self.board.game.get_random_move(self.board.vertical)
            self.board.perform_move(row, col)

        if not self.board.two_player:
            if not self.board.game.game_over(self.board.vertical):
                if(self.board.mode == "AI"):
                    (row, col), best_value, total_leaves = \
                        self.board.game.get_alpha_beta_move(self.board.vertical, limit = 1)
                    self.board.perform_move(row, col)
                elif(self.board.mode == "AI-2"):
                    row = col = fitness_value = -1
                    while not self.board.game.is_legal_move(row, col, self.board.vertical):
                        (row, col), fitness_value = \
                        self.board.game.get_genetic_algorithm_move(self.board.vertical, population_size = 10, generations = 10)
                    self.board.perform_move(row, col)
                elif(self.board.mode == "AI-3"):
                    row = col = best_value = -1
                    while not self.board.game.is_legal_move(row, col, self.board.vertical):
                        (row, col), best_value = \
                            self.board.game.get_fuzzy_logic_move(self.board.vertical)
                    self.board.perform_move(row, col)
                elif(self.board.mode == "AI-4"):
                    row = col = best_value = -1
                    while not self.board.game.is_legal_move(row, col, self.board.vertical):
                        (row, col), best_value = \
                            self.board.game.get_A_star_move(self.board.vertical)
                    self.board.perform_move(row, col)

    def perform_alpha_beta_move(self):
        print("gui.py -> perform_alpha_beta_move -----------------------------------------------------------------------------------")
        print(self.board.mode)
        if not self.board.game.game_over(self.board.vertical):
            (row, col), best_value, total_leaves = \
                self.board.game.get_alpha_beta_move(self.board.vertical, 1)
            self.board.perform_move(row, col)

        if not self.board.two_player:
            if not self.board.game.game_over(self.board.vertical):
                (row, col), best_value, total_leaves = \
                    self.board.game.get_alpha_beta_move(self.board.vertical, limit = 1)
                self.board.perform_move(row, col)


    def perform_genetic_algorithm_move(self):
        print("gui.py -> perform_genetic_algorithm_move -----------------------------------------------------------------------------------")
        print(self.board.mode)
        if not self.board.game.game_over(self.board.vertical):
            row = col = fitness_value = -1
            while not self.board.game.is_legal_move(row, col, self.board.vertical):
                (row, col), fitness_value = \
                self.board.game.get_genetic_algorithm_move(self.board.vertical, population_size = 10, generations = 10)
            self.board.perform_move(row, col)

        if not self.board.two_player:
            if not self.board.game.game_over(self.board.vertical):
                row = col = fitness_value = -1
                while not self.board.game.is_legal_move(row, col, self.board.vertical):
                    (row, col), fitness_value = \
                    self.board.game.get_genetic_algorithm_move(self.board.vertical, population_size = 10, generations = 10)
                self.board.perform_move(row, col)

    def perform_fuzzy_logic_move(self):
        print("gui.py-> perform_fuzzy_logic_move -----------------------------------------------------------------------------------")
        print(self.board.mode)
        if not self.board.game.game_over(self.board.vertical):
            row = col = best_value = -1
            while not self.board.game.is_legal_move(row, col, self.board.vertical):
                (row, col), best_value = \
                    self.board.game.get_fuzzy_logic_move(self.board.vertical)
            self.board.perform_move(row, col)

        if not self.board.two_player:
            if not self.board.game.game_over(self.board.vertical):
                row = col = best_value = -1
                while not self.board.game.is_legal_move(row, col, self.board.vertical):
                    (row, col), best_value = \
                        self.board.game.get_fuzzy_logic_move(self.board.vertical)
                self.board.perform_move(row, col)


    def perform_A_star_move(self):
        print("gui.py -> perform_A_star_move -----------------------------------------------------------------------------------")
        print(self.board.mode)
        if not self.board.game.game_over(self.board.vertical):
            row = col = best_value = -1
            while not self.board.game.is_legal_move(row, col, self.board.vertical):
                (row, col), best_value = self.board.game.get_A_star_move(self.board.vertical)
            self.board.perform_move(row, col)

        if not self.board.two_player:
            if not self.board.game.game_over(self.board.vertical):
                row = col = best_value = -1
                while not self.board.game.is_legal_move(row, col, self.board.vertical):
                    (row, col), best_value = self.board.game.get_A_star_move(self.board.vertical)
                self.board.perform_move(row, col)


if __name__ == "__main__":
    app = DoRaGUI()
    app.mainloop()