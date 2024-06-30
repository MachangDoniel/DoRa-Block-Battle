import tkinter as tk
import random
import DoRa


class Square(tk.Canvas):
    COLOR_EMPTY = "gray"
    COLOR_FILLED_R = "red"
    COLOR_FILLED_B = "blue"

    def __init__(self, master, size=50):
        tk.Canvas.__init__(self, master, height=size, width=size,
                           background=Square.COLOR_EMPTY, highlightthickness=2,
                           highlightbackground="black")
        self.state = False
        self.vertical_color = True

    def set_state(self, state, vertical_color):
        self.state = state
        self.vertical_color = vertical_color
        if self.state:
            color = Square.COLOR_FILLED_B if self.vertical_color else Square.COLOR_FILLED_R
        else:
            color = Square.COLOR_EMPTY
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
                square.bind("<Button-1>",
                            lambda event, row=row, col=col: self.perform_move_2(row, col))
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

    def perform_move_2(self, row, col):
        if not self.two_player:
            self.perform_move(row, col)
        else:
            self.perform_move(row, col)

    def update_squares(self):
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
        frame = self.frames[page_name]
        frame.tkraise()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="DoRa Game", font=("Arial", 24))
        label.pack(pady=20)

        btn_start = tk.Button(self, text="Start", font=("Arial", 16),
                              command=self.start_game)
        btn_start.pack(pady=10)

    def start_game(self):
        self.controller.show_frame("TossPage")


class TossPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mode = "Two Player"

        self.label = tk.Label(self, text="", font=("Arial", 24))
        self.label.pack(pady=20)

        self.btn_toss = tk.Button(self, text="Toss", font=("Arial", 16),
                                  command=self.toss)
        self.btn_toss.pack(pady=10)

        self.btn_next = tk.Button(self, text="Next", font=("Arial", 16),
                                  command=self.go_to_board)
        self.btn_next.pack(pady=10)
        self.btn_next.pack_forget()  # Hide the Next button initially

    def toss(self):
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
        self.controller.show_frame("BoardPage")
        self.controller.frames["BoardPage"].set_up(self.mode, self.controller.vertical)


class BoardPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.board = None

    def set_up(self, mode, vertical):
        if self.board is not None:
            self.board.destroy()

        game = DoRa.create_DoRa_game(6, 6)
        self.board = Board(self, game, 6, 6)
        self.board.two_player = (mode == "Two Player")
        self.board.mode = mode
        self.board.vertical = vertical
        self.board.toss = True
        self.board.pack(side=tk.LEFT, padx=1, pady=1)

        menu = tk.Frame(self)

        self.status_label = tk.Label(menu, font=("Arial", 16))
        self.status_label.pack(padx=1, pady=(1, 10))
        self.update_status()

        tk.Label(menu, text="Press 'r' to perform a random move.").pack(padx=1, pady=1, anchor=tk.W)
        
        tk.Button(menu, text="Two Player", command=self.two_player_move).pack(fill=tk.X, padx=1, pady=1)
        tk.Button(menu, text="Reset Game", command=self.reset_click).pack(fill=tk.X, padx=1, pady=1)

        menu.pack(side=tk.RIGHT)

        self.focus_set()

        self.bind("r", lambda event: self.perform_random_move())

    def return_to_toss(self):
        self.controller.show_frame("TossPage")
        self.controller.frames["TossPage"].reset_toss()

    def reset_game(self):
        # Reset game logic here if needed
        pass

    def update_status(self):
        if self.board.game.game_over(self.board.vertical):
            winner = "Horizontal" if self.board.vertical else "Vertical"
            self.status_label.config(text=self.board.mode + "\n" + "Winner: " + winner)
        else:
            turn = "Vertical" if self.board.vertical else "Horizontal"
            self.status_label.config(text=f"{self.board.mode}\nTurn: {turn}")

    def reset_click(self):
        self.board.game.reset()
        self.board.update_squares()
        self.update_status()

    def auto_move(self):
        self.reset_click()
        self.board.two_player = False
        self.board.mode = "AI"
        self.update_status()

    def two_player_move(self):
        self.reset_click()
        self.board.two_player = True
        self.board.mode = "Two Player"
        self.update_status()

    def perform_random_move(self):
        if not self.board.game.game_over(self.board.vertical):
            row, col = self.board.game.get_random_move(self.board.vertical)
            self.board.perform_move(row, col)

        if not self.board.two_player:
            if not self.board.game.game_over(self.board.vertical):
                (row, col), best_value, total_leaves = \
                    self.board.game.get_alpha_beta_move(self.board.vertical, 1)
                self.board.perform_move(row, col)

    def perform_alpha_beta_move(self):
        if not self.board.game.game_over(self.board.vertical):
            (row, col), best_value, total_leaves = \
                self.board.game.get_alpha_beta_move(self.board.vertical, 1)
            self.board.perform_move(row, col)

        if not self.board.two_player:
            if not self.board.game.game_over(self.board.vertical):
                (row, col), best_value, total_leaves = \
                    self.board.game.get_alpha_beta_move(self.board.vertical, 1)
                self.board.perform_move(row, col)



if __name__ == "__main__":
    app = DoRaGUI()
    app.mainloop()
