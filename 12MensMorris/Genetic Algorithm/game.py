# game.py

class MorrisGame:
    def __init__(self):
        self.board = [None] * 24  # 24 positions on the board
        self.players = ['X', 'O']
        self.current_player = 'X'
        self.phase = 'placing'  # 'placing', 'moving'
        self.moves_made = 0
        self.player_pieces = {'X': 12, 'O': 12}  # Each player has 12 pieces

    def print_board(self):
        positions = [i if x is None else x for i, x in enumerate(self.board)]
        print(f"{positions[0]}-{positions[1]}-{positions[2]}   {positions[3]}-{positions[4]}-{positions[5]}")
        print(f"| \\ | / |   | \\ | / |")
        print(f"{positions[6]}-{positions[7]}-{positions[8]}   {positions[9]}-{positions[10]}-{positions[11]}")
        print(f"| / | \\ |   | / | \\ |")
        print(f"{positions[12]}-{positions[13]}-{positions[14]}   {positions[15]}-{positions[16]}-{positions[17]}")
        print(f"{positions[18]}-{positions[19]}-{positions[20]}   {positions[21]}-{positions[22]}-{positions[23]}")

    def is_valid_move(self, position):
        return self.board[position] is None

    def is_valid_move_moving_phase(self, from_pos, to_pos):
        if self.board[from_pos] == self.current_player and self.board[to_pos] is None:
            return True
        return False

    def make_move(self, from_pos, to_pos=None):
        if self.phase == 'placing':
            if self.is_valid_move(from_pos):
                self.board[from_pos] = self.current_player
                self.player_pieces[self.current_player] -= 1
                self.moves_made += 1
                if self.check_mill(from_pos):
                    return 'mill'
                if self.player_pieces[self.current_player] == 0:
                    self.phase = 'moving'
                self.switch_player()
                return True
        elif self.phase == 'moving':
            if self.is_valid_move_moving_phase(from_pos, to_pos):
                self.board[to_pos] = self.current_player
                self.board[from_pos] = None
                if self.check_mill(to_pos):
                    return 'mill'
                self.switch_player()
                return True
        return False

    def remove_opponent_piece(self, position):
        if self.board[position] == self.get_opponent():
            self.board[position] = None
            return True
        return False

    def get_opponent(self):
        return 'O' if self.current_player == 'X' else 'X'

    def check_mill(self, position):
        mill_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11),
            (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),
            (0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7),
            (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23)
        ]
        for combo in mill_combinations:
            if position in combo:
                if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == self.current_player:
                    return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_all_valid_moves(self):
        if self.phase == 'placing':
            return [i for i in range(24) if self.is_valid_move(i)]
        elif self.phase == 'moving':
            moves = []
            for from_pos in range(24):
                if self.board[from_pos] == self.current_player:
                    for to_pos in range(24):
                        if self.is_valid_move_moving_phase(from_pos, to_pos):
                            moves.append((from_pos, to_pos))
            return moves

    def get_all_valid_moves_for_player(self, player):
        if self.phase == 'placing':
            return [i for i in range(24) if self.board[i] is None]
        elif self.phase == 'moving':
            moves = []
            for from_pos in range(24):
                if self.board[from_pos] == player:
                    for to_pos in range(24):
                        if self.board[to_pos] is None:
                            moves.append((from_pos, to_pos))
            return moves

    def undo_move(self, from_pos, to_pos=None):
        if self.phase == 'placing':
            self.board[from_pos] = None
            self.player_pieces[self.current_player] += 1
            self.moves_made -= 1
        elif self.phase == 'moving':
            self.board[from_pos] = self.current_player
            self.board[to_pos] = None

    def check_winner(self):
        if self.moves_made == 24:  # All pieces have been placed
            player_mills = self.count_mills('X')
            opponent_mills = self.count_mills('O')
            if player_mills > opponent_mills:
                return 'X'
            elif opponent_mills > player_mills:
                return 'O'
            else:
                return 'Draw'
        return False

    def count_mills(self, player):
        mills = 0
        mill_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11),
            (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),
            (0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7),
            (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23)
        ]
        for combo in mill_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == player:
                mills += 1
        return mills

    def get_last_move(self):
        return self.board
