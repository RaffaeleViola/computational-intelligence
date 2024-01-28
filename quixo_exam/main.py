import math
import random

import numpy as np

from game import Game, Move, Player
from quixo_exam.monteCarloTreeSearch import MonteCarloPlayer
from quixo_exam.qtable import Qtable
from quixo_exam.training import is_accetptable, next_acts
from minmax import minmax
from tqdm import tqdm
from trainingQlearning import MyQPlayer


def all_acceptable(game: Game):
    next_actions = next_acts(game, 0)
    for move in next_actions:
        for direct in [Move.TOP, Move.LEFT, Move.RIGHT, Move.BOTTOM]:
            if not is_accetptable(move, direct, game):
                continue
            print((move, direct))
    print()


class RandomPlayer(Player):
    
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # game.print()
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # copy the game to avoid modifying it
        tmp_game = Game()
        tmp_game._board = game.get_board()
        tmp_game.current_player_idx = game.current_player_idx
        montecarlo = MonteCarloPlayer(tmp_game.current_player_idx, mcts_steps=100)
        depth = 4
        if (tmp_game.get_board() == -1).sum() < 6:
            return montecarlo.make_move(tmp_game)
        move, val = minmax(tmp_game, (tmp_game.current_player_idx + 1)%2 , depth, -math.inf, math.inf, tmp_game.current_player_idx)
        # check if the move makes the opponent winning
        check_winner_game = Game()
        check_winner_game._board = tmp_game.get_board()
        check_winner_game.current_player_idx = tmp_game.current_player_idx
        check_winner_game._Game__move(move[0], move[1], tmp_game.current_player_idx)
        # if it is use montecarlo tree search
        if check_winner_game.check_winner() not in [-1, check_winner_game.current_player_idx]:
            return montecarlo.make_move(tmp_game)
        return move


class InputPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        game.print()
        match = {"T": Move.TOP, "B": Move.BOTTOM, "L": Move.LEFT, "R": Move.RIGHT}
        ply = input("format <x-y-T/B/L/R>\n")
        words = ply.strip().split("-")
        x, y, m = int(words[0]), int(words[1]), match[words[2]]
        return (x, y), m


if __name__ == '__main__':
    win_rate = 0
    draw_rate = 0
    for _ in tqdm(range(100)):
        g = Game()
        g.print()
        # player1 = MonteCarloPlayer(player_id=0, mcts_steps=80)
        player2 = MyPlayer()
        player1 = RandomPlayer()
        winner = g.play(player1, player2)
        if winner == 1:
            win_rate += 1
        elif winner == -1:
            draw_rate += 1
        print(f"\n{win_rate}/100\n")
    print(f"\ndraw_rate: {draw_rate}/100\n")

