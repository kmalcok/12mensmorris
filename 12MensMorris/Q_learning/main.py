# main.py
import train_agent
import tkinter as tk
from tkinter import messagebox
from game import MorrisGame
from q_learning import QLearningAgent
from minimax import MinimaxAlgorithm


class MorrisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("12 Men's Morris")

        self.main_menu = tk.Frame(root)
        self.main_menu.pack()

        self.play_button = tk.Button(self.main_menu, text="Play Game", command=self.play_game)
        self.play_button.pack(pady=10)

        self.train_button = tk.Button(self.main_menu, text="Train Agent", command=self.train_agent)
        self.train_button.pack(pady=10)

        self.clear_button = tk.Button(self.main_menu, text="Clear Learning Data", command=self.clear_learning_data)
        self.clear_button.pack(pady=10)

        self.game_frame = tk.Frame(root)
        self.max_depth = 3  # Set the depth for the Minimax algorithm
        self.train_num_games = 10  # Number of training games
        self.train_game_index = 0  # Current training game index

    def play_game(self):
        self.main_menu.pack_forget()
        self.game_frame.pack()
        self.run_game()

    def train_agent(self):
        self.main_menu.pack_forget()
        self.game_frame.pack()
        self.game = MorrisGame()
        self.q_agent = QLearningAgent(self.game)
        self.minimax = MinimaxAlgorithm(self.game)
        self.setup_board()
        self.train_agent_game()

    def clear_learning_data(self):
        game = MorrisGame()
        q_agent = QLearningAgent(game)
        q_agent.clear_q_table()
        messagebox.showinfo("Info", "Learning data cleared.")

    def run_game(self):
        self.game = MorrisGame()
        self.q_agent = QLearningAgent(self.game)

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

        info_label = tk.Label(self.game_frame, text="Blue: Q-Learning Agent, Red: Minimax Algorithm")
        info_label.grid(row=0, columnspan=7, pady=10)

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
                button.bind("<Button-1>", on_click)
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
        if self.game.current_player == 'O':
            valid_moves = self.game.get_all_valid_moves()
            action = self.minimax.find_best_move(self.max_depth)
            if action is not None:
                print(f"Minimax Algorithm chose action: {action}")
                if isinstance(action, int):
                    result = self.game.make_move(action)
                else:
                    result = self.game.make_move(action[0], action[1])
                self.update_board()
                if result == 'mill':
                    self.root.after(1000, self.computer_remove_piece)
                else:
                    if self.game.check_winner():
                        messagebox.showinfo("Game Over", f"Winner: {self.game.get_opponent()}")
                        self.root.quit()
                    else:
                        self.check_game_end()
                        self.game.switch_player()

    def computer_remove_piece(self):
        for pos in range(24):
            if self.game.board[pos] == 'X':
                self.game.remove_opponent_piece(pos)
                break
        self.update_board()
        if self.game.check_winner():
            messagebox.showinfo("Game Over", f"Winner: {self.game.get_opponent()}")
            self.root.quit()
        else:
            self.check_game_end()
            self.game.switch_player()

    def train_agent_game(self):
        self.run_training_game()

    def run_training_game(self):
        self.game = MorrisGame()
        self.q_agent.game = self.game
        self.minimax.game = self.game
        self.train_game_step()

    def train_game_step(self):
        if not self.game.check_winner() and self.game.moves_made < 24:
            if self.game.current_player == 'X':
                # Q-Learning agent's turn
                print("Q-Learning Agent's Turn")
                state = self.q_agent.get_state()
                valid_moves = self.game.get_all_valid_moves()
                action = self.q_agent.choose_action(valid_moves)
                if action is not None:
                    print(f"Q-Learning Agent chose action: {action}")
                    if isinstance(action, int):
                        result = self.game.make_move(action)
                    else:
                        result = self.game.make_move(action[0], action[1])
                    next_state = self.q_agent.get_state()
                    next_valid_moves = self.game.get_all_valid_moves()
                    reward = 1 if self.game.check_winner() else 0
                    self.q_agent.update_q_value(state, action, reward, next_state, next_valid_moves)
                    self.q_agent.decay_epsilon()
                    self.update_board()
                    if result == 'mill':
                        self.root.after(1000, self.train_game_step)
                    else:
                        self.game.switch_player()
                        self.root.after(1000, self.train_game_step)
            else:
                # Minimax algorithm's turn
                print("Minimax Algorithm's Turn")
                best_move = self.minimax.find_best_move(self.max_depth)
                if best_move is not None:
                    print(f"Minimax Algorithm chose action: {best_move}")
                    if isinstance(best_move, int):
                        self.game.make_move(best_move)
                    else:
                        self.game.make_move(best_move[0], best_move[1])
                    self.update_board()
                    if self.game.check_winner():
                        self.q_agent.save_q_table()
                        self.train_game_index += 1
                        if self.train_game_index < self.train_num_games:
                            self.root.after(1000, self.run_training_game)
                        else:
                            messagebox.showinfo("Training Complete", "Agent training complete!")
                            self.main_menu.pack()
                            self.game_frame.pack_forget()
                    else:
                        self.game.switch_player()
                        self.root.after(1000, self.train_game_step)
        else:
            self.q_agent.save_q_table()
            self.train_game_index += 1
            if self.train_game_index < self.train_num_games:
                self.root.after(1000, self.run_training_game)
            else:
                messagebox.showinfo("Training Complete", "Agent training complete!")
                self.main_menu.pack()
                self.game_frame.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = MorrisApp(root)
    root.mainloop()
