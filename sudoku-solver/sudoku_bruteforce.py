#!/usr/local/bin/python3
import numpy as np

BOARD_ROWS = 9
BOARD_COLUMNS = 9

class Sudoku(object):

    def __init__(self, grid):
        if grid.shape == (BOARD_ROWS, BOARD_COLUMNS):
            self.grid = grid
            self.subgrids = {}
            # 1 | 2 | 3
            self.subgrids[(3,3)] = grid[0:3,0:3]
            self.subgrids[(3,6)] = grid[0:3,3:6]
            self.subgrids[(3,9)] = grid[0:3,6:9]
            # 4 | 5 | 6
            self.subgrids[(6,3)] = grid[3:6,0:3]
            self.subgrids[(6,6)] = grid[3:6,3:6]
            self.subgrids[(6,9)] = grid[3:6,6:9]
            # 7 | 8 | 9
            self.subgrids[(9,3)] = grid[6:9,0:3]
            self.subgrids[(9,6)] = grid[6:9,3:6]
            self.subgrids[(9,9)] = grid[6:9,6:9]

    def conflicts(self,  row, col, value):
        return self.value_in_row(row, value) or self.value_in_col(col, value) or self.value_in_subgrid(row, col, value)

    def set_value(self, row_index, col_index, value):
        if self.grid[row_index, col_index] == 0 and self._index_valid(row_index, col_index): # field is unset.
            self.grid[row_index, col_index] = value

    def unset_field(self, row_index, col_index):
        if self._index_valid(row_index, col_index):
            self.grid[row_index, col_index] = 0

    def value_in_row(self, row_index, value):
        if self._row_index_valid(row_index):
            return value in self.grid[row_index]

    def value_in_subgrid(self, row, col, value):
        for limit, subgrid in self.subgrids.items():
            if row < limit[0] and col < limit[1]:
                return value in subgrid
        return False

    def value_in_col(self, col_index, value):
        if self._col_index_valid(value):
            return value in self.grid[:,col_index]
        return False

    def next_unassigned_location(self, start_row=0, start_col=0):
        for row in list(range(start_row,BOARD_ROWS)):
            for col in list(range(start_col, BOARD_COLUMNS)):
                if self.grid[row, col] == 0:
                    return (row, col)
        return (-1, -1) # all locations assigned


    # private helper methods
    def _index_valid(self, row, col):
        return self._row_index_valid(row) and self._col_index_valid(col)

    def _row_index_valid(self, row_index):
        return row_index < BOARD_ROWS

    def _col_index_valid(self, col_index):
        return col_index < BOARD_COLUMNS



def solve_sudoku(game):
    row,col = game.next_unassigned_location()
    if row == -1 or col == -1:
        return True # Solved! All locations filled out
    for value in list(range(1, 10)):
        if not game.conflicts(row, col, value):
            game.set_value(row, col, value) # insert value at location
            if solve_sudoku(game):
                return True
            game.unset_field(row,col) # unset and try again
    return False


def init_game():
    sudoku_grid = np.zeros((BOARD_ROWS,BOARD_COLUMNS), dtype=int) # empty grid
    sudoku_game = Sudoku(sudoku_grid)
    #print(sudoku_game.grid)

    # setup
    sudoku_game.set_value(0,0,5)
    sudoku_game.set_value(0,1,3)
    sudoku_game.set_value(0,4,7)

    sudoku_game.set_value(1,0,6)
    sudoku_game.set_value(1,3,1)
    sudoku_game.set_value(1,4,9)
    sudoku_game.set_value(1,5,5)

    sudoku_game.set_value(2,1,9)
    sudoku_game.set_value(2,2,8)
    sudoku_game.set_value(2,7,6)

    sudoku_game.set_value(3,0,8)
    sudoku_game.set_value(3,4,6)
    sudoku_game.set_value(3,8,3)

    sudoku_game.set_value(4,0,4)
    sudoku_game.set_value(4,3,8)
    sudoku_game.set_value(4,5,3)
    sudoku_game.set_value(4,8,1)

    sudoku_game.set_value(5,0,7)
    sudoku_game.set_value(5,4,2)
    sudoku_game.set_value(5,8,6)

    sudoku_game.set_value(6,1,6)
    sudoku_game.set_value(6,6,2)
    sudoku_game.set_value(6,7,8)

    sudoku_game.set_value(7,3,4)
    sudoku_game.set_value(7,4,1)
    sudoku_game.set_value(7,5,9)
    sudoku_game.set_value(7,8,5)

    sudoku_game.set_value(8,4,8)
    sudoku_game.set_value(8,7,7)
    sudoku_game.set_value(8,8,9)
    return sudoku_game


# test run
def run():
    game = init_game()
    print("Start grid:")
    print(game.grid)
    print("Solving...")
    solve_sudoku(game)
    print(game.grid)

run()
