import pytest
from db.entities.game import Game
from .checker import check_winner


def test_checker_empty():
    res = check_winner(Game(
        field=[
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ],
        size=3
    ))
    assert res is None


@pytest.mark.parametrize("field,size", [
    ([
        [1, 1, 1],
        [0, 2, 0],
        [0, 0, 2]
    ], 3),
    ([
        [2, 0, 0],
        [1, 1, 1],
        [0, 0, 2]
    ], 3)
])
def test_checker_horizontal(field, size):
    res = check_winner(Game(
        field=field,
        size=size
    ))
    assert res == 1


@pytest.mark.parametrize("field,size", [
    ([
        [0, 2, 0],
        [0, 2, 0],
        [0, 2, 2]
    ], 3),
    ([
        [2, 0, 0],
        [2, 1, 1],
        [2, 0, 2]
    ], 3)
])
def test_checker_vertical(field, size):
    res = check_winner(Game(
        field=field,
        size=size
    ))
    assert res == 2


# {{0,2,2},{1,2,1},{2,1,1}}
@pytest.mark.parametrize("field,size,winner", [
    ([
        [1, 2, 0],
        [0, 1, 0],
        [0, 2, 1]
    ], 3, 1),
    ([
        [2, 0, 1],
        [2, 1, 1],
        [1, 0, 2]
    ], 3, 1),
    ([
        [0, 2, 2],
        [1, 2, 1],
        [2, 1, 1]
    ], 3, 2)
])
def test_checker_diagonal(field, size, winner):
    res = check_winner(Game(
        field=field,
        size=size
    ))
    assert res == winner
