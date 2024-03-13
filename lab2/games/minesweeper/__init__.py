from . import minesweeper

def name() -> str:
    return "minesweeper"

def factory() -> minesweeper.MineSweeper:
    return minesweeper.MineSweeper
