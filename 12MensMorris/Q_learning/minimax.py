# minimax.py

import math

class MinimaxAlgorithm:
    def __init__(self, game):
        self.game = game

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game.check_winner():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = -math.inf
            for move in self.game.get_all_valid_moves():
                if isinstance(move, int):  # "placing" phase
                    self.game.make_move(move)
                else:  # "moving" phase
                    self.game.make_move(move[0], move[1])
                eval = self.minimax(depth - 1, alpha, beta, False)
                if isinstance(move, int):
                    self.game.undo_move(move)
                else:
                    self.game.undo_move(move[0], move[1])
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.game.get_all_valid_moves():
                if isinstance(move, int):  # "placing" phase
                    self.game.make_move(move)
                else:  # "moving" phase
                    self.game.make_move(move[0], move[1])
                eval = self.minimax(depth - 1, alpha, beta, True)
                if isinstance(move, int):
                    self.game.undo_move(move)
                else:
                    self.game.undo_move(move[0], move[1])
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self):
        player_pieces = self.game.board.count('X')
        opponent_pieces = self.game.board.count('O')

        player_mills = self.count_mills('X')
        opponent_mills = self.count_mills('O')

        player_moves = len(self.game.get_all_valid_moves_for_player('X'))
        opponent_moves = len(self.game.get_all_valid_moves_for_player('O'))

        evaluation = (player_pieces - opponent_pieces) + (player_mills - opponent_mills) * 10 + (player_moves - opponent_moves) * 0.1

        print(f"Evaluation: {evaluation} | Player Mills: {player_mills}, Opponent Mills: {opponent_mills}, Player Moves: {player_moves}, Opponent Moves: {opponent_moves}")
        return evaluation

    def count_mills(self, player):
        mills = 0
        mill_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11),
            (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),
            (0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7),
            (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23)
        ]
        for combo in mill_combinations:
            if self.game.board[combo[0]] == self.game.board[combo[1]] == self.game.board[combo[2]] == player:
                mills += 1
        return mills

    def find_best_move(self, depth):
        best_move = None
        best_value = -math.inf
        for move in self.game.get_all_valid_moves():
            if isinstance(move, int):  # "placing" phase
                self.game.make_move(move)
                move_value = self.minimax(depth - 1, -math.inf, math.inf, False)
                self.game.undo_move(move)
            else:  # "moving" phase
                self.game.make_move(move[0], move[1])
                move_value = self.minimax(depth - 1, -math.inf, math.inf, False)
                self.game.undo_move(move[0], move[1])
            if move_value > best_value:
                best_value = move_value
                best_move = move
            print(f"Move: {move} | Move Value: {move_value}")
        print(f"Best Move: {best_move} | Best Value: {best_value}")
        return best_move
