from tkinter import Tk, BOTH, Canvas
import time, random


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze solver")
        self.w = Canvas(self.__root, width=width, height=height)
        self.w.pack()
        self.window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.w.update_idletasks()
        self.w.update()

    def wait_for_close(self):
        self.window_running = True
        while self.window_running:
            self.redraw()

    def close(self):
        self.window_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.w, fill_color)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2,
        )


class Cell:
    def __init__(
        self,
        x1,
        x2,
        y1,
        y2,
        win,
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
    ):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.win = win
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.visited = False

    def draw(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        point_top_left = Point(top_left_x, top_left_y)
        point_top_right = Point(bottom_right_x, top_left_y)
        point_bottom_left = Point(top_left_x, bottom_right_y)
        point_bottom_right = Point(bottom_right_x, bottom_right_y)
        line_color = "black"  # Default wall color
        bg_color = "#d9d9d9"  # Background color

        if self.has_left_wall:
            left_line = Line(point1=point_top_left, point2=point_bottom_left)
            self.win.draw_line(left_line, line_color)
        else:
            left_line = Line(point1=point_top_left, point2=point_bottom_left)
            self.win.draw_line(left_line, bg_color)  # Draw background color

        if self.has_top_wall:
            top_line = Line(point1=point_top_left, point2=point_top_right)
            self.win.draw_line(top_line, line_color)
        else:
            top_line = Line(point1=point_top_left, point2=point_top_right)
            self.win.draw_line(top_line, bg_color)

        if self.has_bottom_wall:
            bottom_line = Line(point1=point_bottom_left, point2=point_bottom_right)
            self.win.draw_line(bottom_line, line_color)
        else:
            bottom_line = Line(point1=point_bottom_left, point2=point_bottom_right)
            self.win.draw_line(bottom_line, bg_color)

        if self.has_right_wall:
            right_line = Line(point1=point_top_right, point2=point_bottom_right)
            self.win.draw_line(right_line, line_color)
        else:
            right_line = Line(point1=point_top_right, point2=point_bottom_right)
            self.win.draw_line(right_line, bg_color)

    def draw_move(self, to_cell, undo=False):
        cur_cell_mid_x = (self.x1 + self.x2) / 2
        cur_cell_mid_y = (self.y1 + self.y2) / 2
        to_cell_mid_x = (to_cell.x1 + to_cell.x2) / 2
        to_cell_mid_y = (to_cell.y1 + to_cell.y2) / 2
        cur_cell_point = Point(cur_cell_mid_x, cur_cell_mid_y)
        to_cell_point = Point(to_cell_mid_x, to_cell_mid_y)
        new_line = Line(cur_cell_point, to_cell_point)
        if undo == False:
            self.win.draw_line(new_line, "red")
        else:
            self.win.draw_line(new_line, "gray")


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed != None:
            random.seed(seed)
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.num_cols):
            self._cells.append([])
            for j in range(self.num_rows):
                cell_x1 = self.x1 + i * self.cell_size_x
                cell_y1 = self.y1 + j * self.cell_size_y
                cell_x2 = cell_x1 + self.cell_size_x
                cell_y2 = cell_y1 + self.cell_size_y
                cell = Cell(
                    x1=cell_x1,
                    x2=cell_x2,
                    y1=cell_y1,
                    y2=cell_y2,
                    win=self.win,
                )
                self._cells[i].append(cell)
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        x1 = cell.x1
        y1 = cell.y1
        x2 = cell.x2
        y2 = cell.y2
        cell.draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        # Break entrance (top-left)
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        # Break exit (bottom-right)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            possible_directions = []

            # Check adjacent cells and add unvisited ones to possible_directions
            if i > 0 and not self._cells[i - 1][j].visited:
                possible_directions.append(("L", i - 1, j))  # Left
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                possible_directions.append(("R", i + 1, j))  # Right
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_directions.append(("U", i, j - 1))  # Up
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                possible_directions.append(("D", i, j + 1))  # Down

            if not possible_directions:
                self._draw_cell(i, j)
                return  # No unvisited neighbors, backtrack

            # Choose a random direction
            direction, next_i, next_j = random.choice(possible_directions)

            # Break walls between current and next cell
            if direction == "L":
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif direction == "R":
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif direction == "U":
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif direction == "D":
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False

            self._draw_cell(i, j)
            self._draw_cell(next_i, next_j)

            # Recursively call _break_walls_r on the next cell
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        solved = self._solve_r(i =  0, j = 0)
        if solved:
            return  True
        else:
            return False
        
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[self.num_cols - 1][self.num_rows - 1]:
            return True
        if i > 0 and not self._cells[i-1][j].visited and self._cells[i][j].has_left_wall == False:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            result = self._solve_r(i=i-1, j=j)
            if result == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], undo = True)                
        if i < self.num_cols - 1 and not self._cells[i+1][j].visited and self._cells[i][j].has_right_wall == False:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            result = self._solve_r(i=i+1, j=j)
            if result == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], undo = True)
        if j > 0 and not self._cells[i][j-1].visited and self._cells[i][j].has_top_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            result = self._solve_r(i=i, j=j-1)
            if result == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], undo = True)
        if j < self.num_rows - 1 and not self._cells[i][j+1].visited and self._cells[i][j].has_bottom_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            result = self._solve_r(i=i, j=j+1)
            if result == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], undo = True)
        return False
        

def main():
    win = Window(800, 600)
    maze = Maze(
        x1=50,
        y1=50,
        num_rows=16,
        num_cols=16,
        cell_size_x=30,
        cell_size_y=30,
        win=win,
    )
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
