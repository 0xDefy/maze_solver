import unittest
from main import Maze, Window  # Import Window as well


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        # Create a dummy Window instance for the Maze constructor
        win = Window(800, 600)  # Or any width and height
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )


if __name__ == "__main__":
    unittest.main()
