# train_agent.py

from game import MorrisGame
from q_learning import QLearningAgent
from minimax import MinimaxAlgorithm

def play_game(agent, minimax, max_depth):
    game = MorrisGame()
    agent.game = game
    minimax.game = game

    while not game.check_winner() and game.moves_made < 24:
        if game.current_player == 'X':
            # Q-Learning agent's turn
            state = agent.get_state()
            valid_moves = game.get_all_valid_moves()
            action = agent.choose_action(valid_moves)
            if action is None:
                break
            result = game.make_move(action[0], action[1])
            next_state = agent.get_state()
            next_valid_moves = game.get_all_valid_moves()
            reward = 1 if game.check_winner() else 0
            agent.update_q_value(state, action, reward, next_state, next_valid_moves)
            agent.decay_epsilon()
        else:
            # Minimax algorithm's turn
            best_move = minimax.find_best_move(max_depth)
            if best_move is None:
                break
            game.make_move(best_move[0], best_move[1])

        game.switch_player()

    # Save Q-Table after each game
    agent.save_q_table()

def main():
    game = MorrisGame()
    agent = QLearningAgent(game)
    minimax = MinimaxAlgorithm(game)

    num_games = 1000
    max_depth = 3

    for _ in range(num_games):
        play_game(agent, minimax, max_depth)

    print("Training complete.")

if __name__ == "__main__":
    main()
