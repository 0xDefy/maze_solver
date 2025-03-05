import unittest
from main import Maze, Window, Cell  # Import Cell as well


class Tests(unittest.TestCase):
    def setUp(self):
        # Create a dummy Window instance for all tests
        self.win = Window(800, 600)
        self.num_cols = 5
        self.num_rows = 5
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
        # Break walls to ensure cells are visited
        self.m1._break_walls_r(0, 0)

    def test_reset_cells_visited(self):
        # Reset the visited property of all cells
        self.m1._reset_cells_visited()

        # Check if all cells are unvisited
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.assertFalse(
                    self.m1._cells[i][j].visited,
                    f"Cell at ({i}, {j}) should be unvisited",
                )

if __name__ == "__main__":
    unittest.main()
