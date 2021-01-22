from typing import Optional
from db.entities.game import Game


def check_winner(game: Game) -> Optional[int]:
    winner = None
    # check horizontal lines
    for j in range(game.size):
        everything_equal = True
        prev = game[0, j]
        for i in range(game.size):
            if prev != game[i, j] or game[i, j] == 0:
                everything_equal = False
        if everything_equal:
            winner = prev

    # check vertical lines
    for i in range(game.size):
        everything_equal = True

        prev = game[i, 0]
        for j in range(game.size):
            if prev != game[i, j] or game[i, j] == 0:
                everything_equal = False
        if everything_equal:
            winner = prev

    # check diagonals
    i = j = 0
    prev = game[i, j]
    everything_equal = True
    while i < game.size and j < game.size:
        if game[i, j] != prev or game[i, j] == 0:
            everything_equal = False
            break
        i += 1
        j += 1
    if everything_equal:
        winner = prev

    i = 0
    j = game.size - 1
    prev = game[i, j]
    everything_equal = True
    while i < game.size and j >= 0:
        if game[i, j] != prev or game[i, j] == 0:
            everything_equal = False
            break
        i += 1
        j -= 1
    if everything_equal:
        winner = prev

    return winner
