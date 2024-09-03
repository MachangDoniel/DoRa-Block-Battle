import tkinter as tk
from tkinter import messagebox
import random
import DoRa
from PIL import Image, ImageTk

# variable
limit = 1
population_size = 100
generations = 100
delay = 100

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.background_image = tk.PhotoImage(file="images/background.jpg")
        # Other initialization code...

class Square(tk.Canvas):
    COLOR_EMPTY = "gray"
    COLOR_FILLED_R = "red"
    COLOR_FILLED_B = "blue"

    def __init__(self, master, size=50):
        tk.Canvas.__init__(self, master, height=size, width=size,
                           background=Square.COLOR_EMPTY, highlightthickness=2,
                           highlightbackground="yellow")
        self.state = False
        self.vertical_color = True

    def set_state(self, state, vertical_color):
        self.state = state
        self.vertical_color = vertical_color
        color = Square.COLOR_FILLED_B if self.state and self.vertical_color else \
                Square.COLOR_FILLED_R if self.state else \
                Square.COLOR_EMPTY
        self.configure(background=color)

class Board(tk.Frame):
    def __init__(self, master, game, rows, cols):
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

        # Check for a winner after each move
        if self.game.game_over(self.vertical):
            winner = "Horizontal" if self.vertical else "Vertical"
            self.show_winner(winner)

    def show_winner(self, winner):
        result = messagebox.showinfo("Game Over", f"{winner} wins!")
        if result == 'ok':
            self.master.reset_click()

    def perform_ai_move(self):
        if self.moved and not self.game.game_over(self.vertical):
            (row, col), best_value, total_leaves = self.game.get_alpha_beta_move(self.vertical, 1)
            self.perform_move(row, col)

    def perform_ai2_move(self):
        if self.moved and not self.game.game_over(self.vertical):
            row = col = fitness_value = -1
            while not self.game.is_legal_move(row, col, self.vertical):
                (row, col), fitness_value = self.game.get_genetic_algorithm_move(self.vertical, population_size=10, generations=10)
            self.perform_move(row, col)

    def perform_ai3_move(self):
        if self.moved and not self.game.game_over(self.vertical):
            row = col = best_value = -1
            while not self.game.is_legal_move(row, col, self.vertical):
                (row, col), best_value = self.game.get_fuzzy_logic_move(self.vertical)
            self.perform_move(row, col)

    def perform_ai4_move(self):
        if self.moved and not self.game.game_over(self.vertical):
            row = col = best_value = -1
            while not self.game.is_legal_move(row, col, self.vertical):
                (row, col), best_value = self.game.get_A_star_move(self.vertical)
            self.perform_move(row, col)

    def perform_move_AI(self, row, col):
        self.perform_move(row, col)

        if self.mode == "AI" and self.moved:
            self.after(delay, self.perform_ai_move)

        elif self.mode == "AI-2" and self.moved:
            self.after(delay, self.perform_ai2_move)

        elif self.mode == "AI-3" and self.moved:
            self.after(delay, self.perform_ai3_move)

        elif self.mode == "AI-4" and self.moved:
            self.after(delay, self.perform_ai4_move)

    def update_squares(self):
        game_board = self.game.get_board()
        for row in range(self.rows):
            for col in range(self.cols):
                square = self.squares[row][col]
                square.set_state(game_board[row][col], square.vertical_color)

class DoRaGUI(tk.Tk):
    def __init__(self):
        print('gui.py -> DoRaGUI __init__')
        tk.Tk.__init__(self)
        self.title("DoRa Block Battle")
        self.geometry('800x600')
        self.minsize(800, 600)

        self.board_size = 7  # Default board size

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (MainPage, TossPage, BoardPage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Ensure the SettingsPage is initialized correctly
        self.after(100, lambda: self.show_frame("MainPage"))

    def show_frame(self, page_name):
        print('gui.py -> show_frame', page_name)
        frame = self.frames[page_name]
        frame.tkraise()




class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        original_image = Image.open("images/bg.jpg")
        self.background_image = ImageTk.PhotoImage(original_image)

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        self.size_var = tk.IntVar(value=self.controller.board_size)  # Default size from controller

        tk.Label(self.canvas, text="Select Board Size (n x n):", font=("Arial", 24)).pack(pady=20)
        tk.Radiobutton(self.canvas, text="5 x 5", variable=self.size_var, value=5, font=("Arial", 16)).pack()
        tk.Radiobutton(self.canvas, text="6 x 6", variable=self.size_var, value=6, font=("Arial", 16)).pack()
        tk.Radiobutton(self.canvas, text="7 x 7", variable=self.size_var, value=7, font=("Arial", 16)).pack()
        tk.Radiobutton(self.canvas, text="8 x 8", variable=self.size_var, value=8, font=("Arial", 16)).pack()
        tk.Radiobutton(self.canvas, text="9 x 9", variable=self.size_var, value=9, font=("Arial", 16)).pack()
        tk.Radiobutton(self.canvas, text="10 x 10", variable=self.size_var, value=10, font=("Arial", 16)).pack()

        btn_apply = tk.Button(self.canvas, text="Apply", font=("Arial", 16), command=self.apply_settings)
        btn_apply.pack(pady=20)

        self.pack_propagate(False)
        self.configure(width=800, height=600)

    def apply_settings(self):
        size = self.size_var.get()
        self.controller.board_size = size  # Update the board size in the controller
        tk.messagebox.showinfo("Board Size", f"Selected board size: {size} x {size}")
        self.controller.show_frame("MainPage")





class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        print('gui.py -> MainPage __init__')
        tk.Frame.__init__(self, parent)
        self.controller = controller

        original_image = Image.open("images/bg.jpg")
        self.background_image = ImageTk.PhotoImage(original_image)

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        btn_start = tk.Button(self.canvas, bg="green", fg="white", text="Start", font=("Arial", 16), command=self.start_game)
        self.canvas.create_window(400, 250, window=btn_start)

        btn_settings = tk.Button(self.canvas, bg="blue", fg="white", text="Settings", font=("Arial", 16), command=self.show_settings)
        self.canvas.create_window(400, 300, window=btn_settings)  # Adjust position as needed

        self.pack_propagate(False)
        self.configure(width=800, height=600)

    def start_game(self):
        print('gui.py -> start_game')
        self.controller.show_frame("TossPage")

    def show_settings(self):
        print('gui.py -> show_settings')
        self.controller.show_frame("SettingsPage")



class TossPage(tk.Frame):
    def __init__(self, parent, controller):
        print('gui.py -> TossPage __init__')
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Load and resize the background image
        original_image = Image.open("images/bg.jpg")
        # resized_image = original_image.resize((800, 600), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(original_image)

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Add the background image to the canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Create the label and buttons directly on the canvas
        self.label = tk.Label(self.canvas, fg="orange", bg="white", text="", font=("Arial", 24))
        self.canvas.create_window(400, 100, window=self.label)  # Adjust position as needed

        self.btn_toss = tk.Button(self.canvas, bg="green", fg="white", text="Toss", font=("Arial", 16),
                                  command=self.toss)
        self.canvas.create_window(400, 200, window=self.btn_toss)  # Adjust position as needed

        self.btn_next = tk.Button(self.canvas, bg="green", fg="white", text=">>", font=("Arial", 16),
                                  command=self.go_to_board)
        self.btn_next_window = self.canvas.create_window(400, 300, window=self.btn_next)  # Adjust position as needed
        self.canvas.itemconfigure(self.btn_next_window, state='hidden')  # Hide the Next button initially

        self.mode = "AI"  # Default mode
        self.pack_propagate(False)  # Prevent frame from resizing to fit its content
        self.configure(width=800, height=600)  # Set the size of the frame

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
        self.canvas.itemconfigure(self.btn_next_window, state='normal')  # Show the Next button after the toss

    def go_to_board(self):
        print('gui.py -> go_to_board')
        self.controller.show_frame("BoardPage")
        self.controller.frames["BoardPage"].set_up(self.mode, self.controller.vertical)


class BoardPage(tk.Frame):
    def __init__(self, parent, controller):
        print('gui.py -> BoardPage __init__')
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.board = None

        # Use grid layout for the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def set_up(self, mode, vertical):
        print('gui.py -> set_up - Mode:', mode)
        if self.board is not None:
            self.board.destroy()

        board_size = self.controller.board_size  # Get board size from controller
        game = DoRa.create_DoRa_game(board_size, board_size)
        self.board = Board(self, game, board_size, board_size)
        self.board.two_player = (mode == "Two Player")
        self.board.mode = mode
        self.board.vertical = vertical
        self.board.toss = True
        self.board.grid(row=0, column=0, sticky="nsew")

        menu = tk.Frame(self)
        menu.grid(row=0, column=1, sticky="ns")

        self.status_label = tk.Label(menu, fg="red", font=("Arial", 16))
        self.status_label.pack(padx=1, pady=(1, 10))
        self.update_status()

        tk.Label(menu, fg="blue", text="Press 'r' to perform a random move.").pack(padx=1, pady=1, anchor=tk.W)
        tk.Label(menu, fg="blue", text="Press 'a' to perform a best move of alpha_beta pruning.").pack(padx=1, pady=1, anchor=tk.W)
        tk.Label(menu, fg="blue", text="Press 'g' to perform a best move of genetic_algorithm.").pack(padx=1, pady=1, anchor=tk.W)
        tk.Label(menu, fg="blue", text="Press 'f' to perform a best move of fuzzy_logic.").pack(padx=1, pady=1, anchor=tk.W)
        tk.Label(menu, fg="blue", text="Press 's' to perform a best move of A_star.").pack(padx=1, pady=1, anchor=tk.W)

        tk.Button(menu, bg="#4caf50", fg="white", text="Two Player", command=self.two_player_move).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#4caf50", fg="white", text="Play with AI", command=self.auto_move).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#4caf50", fg="white", text="Play with AI-2", command=self.auto_move2).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#4caf50", fg="white", text="Play with AI-3", command=self.auto_move3).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#4caf50", fg="white", text="Play with AI-4", command=self.auto_move4).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, bg="#ff5050", fg="white", text="Reset Game", command=self.reset_click).pack(fill=tk.X, padx=1, pady=1)
        
        # Add the return button
        tk.Button(menu, bg="#ffbb33", fg="white", text="Return", command=self.return_to_previous).pack(fill=tk.X, padx=1, pady=1)

        menu.grid(row=0, column=1, sticky="ns")

        self.focus_set()

        self.bind("r", lambda event: self.perform_random_move())
        self.bind("a", lambda event: self.perform_alpha_beta_move())
        self.bind("g", lambda event: self.perform_genetic_algorithm_move())
        self.bind("f", lambda event: self.perform_fuzzy_logic_move())
        self.bind("s", lambda event: self.perform_A_star_move())

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
        print("gui.py -> perform_fuzzy_logic_move -----------------------------------------------------------------------------------")
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
                (row, col), best_value = \
                    self.board.game.get_A_star_move(self.board.vertical)
            self.board.perform_move(row, col)

        if not self.board.two_player:
            if not self.board.game.game_over(self.board.vertical):
                row = col = best_value = -1
                while not self.board.game.is_legal_move(row, col, self.board.vertical):
                    (row, col), best_value = \
                        self.board.game.get_A_star_move(self.board.vertical)
                self.board.perform_move(row, col)

    def return_to_previous(self):
        print("gui.py -> return_to_previous")
        self.controller.show_frame("MainPage")






if __name__ == "__main__":
    app = DoRaGUI()
    app.mainloop()