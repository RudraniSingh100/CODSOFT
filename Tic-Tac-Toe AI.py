import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe AI")

        self.difficulty = None
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        # Scores
        self.user_score = 0
        self.ai_score = 0

        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack()
        self.score_label = tk.Label(self.top_frame, text="You: 0 | AI: 0", font=("Helvetica", 16))
        self.score_label.pack()

        self.diff_frame = tk.Frame(self.window)
        self.diff_frame.pack()

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()

        self.create_difficulty_buttons()

        self.restart_button = tk.Button(self.window, text="Restart", font=('Helvetica', 14),
                                        command=self.reset_game)
        self.restart_button.pack(pady=10)

        self.window.mainloop()

    def create_difficulty_buttons(self):
        for widget in self.diff_frame.winfo_children():
            widget.destroy()

        tk.Label(self.diff_frame, text="Choose difficulty:", font=("Helvetica", 16)).pack()
        easy_btn = tk.Button(self.diff_frame, text="Easy", font=("Helvetica", 14),
                             command=lambda: self.set_difficulty("easy"))
        medium_btn = tk.Button(self.diff_frame, text="Medium", font=("Helvetica", 14),
                               command=lambda: self.set_difficulty("medium"))
        hard_btn = tk.Button(self.diff_frame, text="Hard", font=("Helvetica", 14),
                             command=lambda: self.set_difficulty("hard"))
        easy_btn.pack(side=tk.LEFT, padx=10)
        medium_btn.pack(side=tk.LEFT, padx=10)
        hard_btn.pack(side=tk.LEFT, padx=10)

    def set_difficulty(self, level):
        self.difficulty = level
        for widget in self.diff_frame.winfo_children():
            widget.destroy()
        self.create_game_buttons()

    def create_game_buttons(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.button_frame, text="", font=('Helvetica', 32), height=1, width=3,
                                command=lambda row=i, col=j: self.human_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def human_move(self, row, col):
        if self.board[row][col] == "" and self.current_player == "X":
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="❌")
            if self.check_winner(self.board, "X"):
                self.highlight_winner("X")
                self.user_score += 1
                self.update_score()
                self.window.after(1000, lambda: self.game_over("You win!"))
            elif self.is_draw(self.board):
                self.window.after(100, lambda: self.game_over("It's a draw!"))
            else:
                self.current_player = "O"
                self.window.after(400, self.ai_move)

    def ai_move(self):
        if self.difficulty == "easy":
            self.random_ai_move()
        elif self.difficulty == "medium":
            if random.random() < 0.5:
                self.random_ai_move()
            else:
                self.minimax_ai_move()
        else:
            self.minimax_ai_move()

    def random_ai_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = "O"
            self.buttons[i][j].config(text="⭕")
            self.after_ai_move()

    def minimax_ai_move(self):
        best_score = -float("inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax_ab(self.board, 0, False, -float("inf"), float("inf"))
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            i, j = best_move
            self.board[i][j] = "O"
            self.buttons[i][j].config(text="⭕")
            self.after_ai_move()

    def minimax_ab(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner(board, "O"):
            return 1
        elif self.check_winner(board, "X"):
            return -1
        elif self.is_draw(board):
            return 0

        if is_maximizing:
            max_eval = -float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "O"
                        eval = self.minimax_ab(board, depth + 1, False, alpha, beta)
                        board[i][j] = ""
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            return max_eval
            return max_eval
        else:
            min_eval = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "X"
                        eval = self.minimax_ab(board, depth + 1, True, alpha, beta)
                        board[i][j] = ""
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            return min_eval
            return min_eval

    def after_ai_move(self):
        if self.check_winner(self.board, "O"):
            self.highlight_winner("O")
            self.ai_score += 1
            self.update_score()
            self.window.after(1000, lambda: self.game_over("AI wins!"))
        elif self.is_draw(self.board):
            self.window.after(100, lambda: self.game_over("It's a draw!"))
        else:
            self.current_player = "X"

    def check_winner(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2-i] == player for i in range(3)):
            return True
        return False

    def highlight_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                for j in range(3):
                    self.buttons[i][j].config(bg="lightgreen")
                return
            if all(self.board[j][i] == player for j in range(3)):
                for j in range(3):
                    self.buttons[j][i].config(bg="lightgreen")
                return
        if all(self.board[i][i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][i].config(bg="lightgreen")
            return
        if all(self.board[i][2-i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][2-i].config(bg="lightgreen")
            return

    def is_draw(self, board):
        return all(board[i][j] != "" for i in range(3) for j in range(3))

    def update_score(self):
        self.score_label.config(text=f"You: {self.user_score} | AI: {self.ai_score}")

    def game_over(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.create_difficulty_buttons()

if __name__ == "__main__":
    TicTacToe()
