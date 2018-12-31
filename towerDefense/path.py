from cell import *

class Path:
    '''Define a sequence of Cells from one edge of the board
    to the other, on which the invaders will walk.
    '''

    def __init__(self, grid_size):
        # 0th item is cell where the invaders start.  Last item
        # is where they exit the board.

        # grid_size is the size of the board.  Used to check that a path
        # starts and ends on an edge.

        self._path = []
        self._grid_size = grid_size

    def add_cell(self, cell):
        assert isinstance(cell, Cell)
        if self._path == []:
            # empty list, so check that cell is on the edge.
            assert cell.get_x() == 0 or cell.get_x() == self._grid_size - 1 or \
                   cell.get_y() == 0 or cell.get_y() == self._grid_size - 1
        else:
            # Verify that the cell is adjacent to the last cell in the path.
            last_cell = self._path[-1]
            # Need to be adjacent horizontally or vertically -- not just diagonal.
            assert cell.get_x() == last_cell.get_x() or cell.get_y() == last_cell.get_y()
            assert abs(cell.get_x() - last_cell.get_x()) <= 1 and \
                   abs(cell.get_y() - last_cell.get_y()) <= 1

        self._path.append(cell)

    def __len__(self):
        return len(self._path)

    def get_cell(self, idx):
        return self._path[idx]


if __name__ == '__main__':
    p = Path(4)
    cells = [Cell(None, 0, 3, 5), Cell(None, 1, 3, 5), Cell(None, 2, 3, 5),
             Cell(None, 3, 3, 5)]
    for c in cells:
        p.add_cell(c)
    assert len(p) == 4

    # Test starting cell not on an edge
    p = Path(4)
    try:
        p.add_cell(Cell(None, 2, 2, 5))
        assert False
    except AssertionError:
        pass

    # Test adding diagonally-adjacent cell -- not allowed.
    p = Path(4)
    p.add_cell(Cell(None, 3, 3, 5))
    try:
        p.add_cell(Cell(None, 2, 2, 5))
        assert False
    except AssertionError:
        pass
    
    # Test adding totally non-adjacent cell -- not allowed.
    p = Path(4)
    p.add_cell(Cell(None, 3, 3, 5))
    try:
        p.add_cell(Cell(None, 1, 3, 5))
        assert False
    except AssertionError:
        pass

    print("All unit tests passed.")
    






