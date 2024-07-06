# main.py
import random
import tkinter as tk
from tkinter import messagebox
from game import MorrisGame
from ga import GeneticAlgorithm


class MorrisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("12 Men's Morris")

        self.main_menu = tk.Frame(root)
        self.main_menu.pack()

        self.play_button = tk.Button(self.main_menu, text="Play Game", command=self.play_game)
        self.play_button.pack(pady=10)

        self.train_button = tk.Button(self.main_menu, text="Train AI", command=self.train_ai)
        self.train_button.pack(pady=10)

        self.game_frame = tk.Frame(root)
        self.ga = GeneticAlgorithm()
        self.game = MorrisGame()
        self.best_game = None

    def play_game(self):
        self.main_menu.pack_forget()
        self.game_frame.pack()
        self.run_game()

    def train_ai(self):
        self.main_menu.pack_forget()
        self.game_frame.pack()
        self.best_game = self.ga.evolve(self.game)
        messagebox.showinfo("Training Complete", "AI Training Complete!")

    def run_game(self):
        self.game = MorrisGame()

        def on_click(event):
            if self.game.current_player == 'X':
                position = int(event.widget["text"])
                result = self.game.make_move(position)
                self.update_board()
                if result == 'mill':
                    self.prompt_remove_opponent_piece()
                else:
                    self.check_game_end()
                    self.game.switch_player()
                    self.root.after(1000, self.computer_turn)

        self.setup_board(on_click)

    def setup_board(self, on_click=None):
        self.game_frame.pack()

        self.buttons = []
        positions = [
            (0, 0), (0, 3), (0, 6),
            (1, 1), (1, 3), (1, 5),
            (2, 2), (2, 3), (2, 4),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
            (4, 2), (4, 3), (4, 4),
            (5, 1), (5, 3), (5, 5),
            (6, 0), (6, 3), (6, 6)
        ]

        for i, (row, col) in enumerate(positions):
            button = tk.Button(self.game_frame, text=str(i), width=10, height=5)
            button.grid(row=row, column=col, padx=5, pady=5)
            if on_click:
                button.bind("<Button-1>", lambda event, i=i: on_click(event))
            self.buttons.append(button)

        self.update_board()

    def update_board(self):
        for i in range(24):
            if self.game.board[i] == 'X':
                self.buttons[i].config(bg='blue')
            elif self.game.board[i] == 'O':
                self.buttons[i].config(bg='red')
            else:
                self.buttons[i].config(bg='white')

    def prompt_remove_opponent_piece(self):
        self.info_label = tk.Label(self.game_frame, text="Select opponent's piece to remove")
        self.info_label.grid(row=7, columnspan=7)

        for i in range(24):
            if self.game.board[i] == self.game.get_opponent():
                self.buttons[i].config(command=lambda i=i: self.remove_piece(i))

    def remove_piece(self, position):
        self.game.remove_opponent_piece(position)
        self.update_board()
        self.info_label.destroy()
        self.check_game_end()
        self.game.switch_player()
        self.root.after(1000, self.computer_turn)

    def check_game_end(self):
        result = self.game.check_winner()
        if result == 'X':
            messagebox.showinfo("Game Over", "Player X wins!")
            self.root.quit()
        elif result == 'O':
            messagebox.showinfo("Game Over", "Player O wins!")
            self.root.quit()
        elif result == 'Draw':
            messagebox.showinfo("Game Over", "It's a draw!")
            self.root.quit()

    def computer_turn(self):
        if self.game.current_player == 'O' and self.best_game:
            valid_moves = self.game.get_all_valid_moves()
            best_move = random.choice(valid_moves)  # Temporary, replace with best_move from GA
            if best_move:
                result = self.game.make_move(best_move[0], best_move[1] if isinstance(best_move, tuple) else None)
                self.update_board()
                if result == 'mill':
                    self.root.after(1000, self.computer_remove_piece)
                else:
                    self.check_game_end()
                    self.game.switch_player()

    def computer_remove_piece(self):
        for pos in range(24):
            if self.game.board[pos] == 'X':
                self.game.remove_opponent_piece(pos)
                break
        self.update_board()
        self.check_game_end()
        self.game.switch_player()


if __name__ == "__main__":
    root = tk.Tk()
    app = MorrisApp(root)
    root.mainloop()
