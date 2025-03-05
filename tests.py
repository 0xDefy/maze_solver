import unittest
from main import Maze, Window, Cell  # Import Cell as well


class Tests(unittest.TestCase):
    def setUp(self):
        # Create a dummy Window instance for all tests
        self.win = Window(800, 600)
        self.num_cols = 12
        self.num_rows = 10
        self.cell_size_x = 10
        self.cell_size_y = 10
        self.m1 = Maze(
            0,
            0,
            self.num_rows,
            self.num_cols,
            self.cell_size_x,
            self.cell_size_y,
            self.win,
        )

    def test_maze_create_cells(self):
        self.assertEqual(
            len(self.m1._cells),
            self.num_cols,
        )
        self.assertEqual(
            len(self.m1._cells[0]),
            self.num_rows,
        )

    def test_maze_cell_size(self):
        # Check if the cell sizes are correctly set during maze creation
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                cell = self.m1._cells[i][j]
                self.assertEqual(cell.x2 - cell.x1, self.cell_size_x)
                self.assertEqual(cell.y2 - cell.y1, self.cell_size_y)

    def test_maze_cell_positions(self):
        # Check if the cell positions are correctly calculated
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                cell = self.m1._cells[i][j]
                expected_x1 = 0 + i * self.cell_size_x
                expected_y1 = 0 + j * self.cell_size_y
                self.assertEqual(cell.x1, expected_x1)
                self.assertEqual(cell.y1, expected_y1)

    def test_maze_all_cells_are_cells(self):
        # Check if all elements in the _cells list are Cell objects
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.assertIsInstance(self.m1._cells[i][j], Cell)


if __name__ == "__main__":
    unittest.main()
