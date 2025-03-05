from tkinter import Tk, BOTH, Canvas
import time


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

    def draw(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        point_top_left = Point(top_left_x, top_left_y)
        point_top_right = Point(bottom_right_x, top_left_y)
        point_bottom_left = Point(top_left_x, bottom_right_y)
        point_bottom_right = Point(bottom_right_x, bottom_right_y)
        if self.has_left_wall:
            left_line = Line(point1=point_top_left, point2=point_bottom_left)
            self.win.draw_line(left_line, "black")
        if self.has_top_wall:
            top_line = Line(point1=point_top_left, point2=point_top_right)
            self.win.draw_line(top_line, "black")
        if self.has_bottom_wall:
            bottom_line = Line(point1=point_bottom_left, point2=point_bottom_right)
            self.win.draw_line(bottom_line, "black")
        if self.has_right_wall:
            right_line = Line(point1=point_top_right, point2=point_bottom_right)
            self.win.draw_line(right_line, "black")

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
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()

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


def main():
    win = Window(800, 600)
    maze = Maze(
        x1=50,
        y1=50,
        num_rows=10,
        num_cols=10,
        cell_size_x=20,
        cell_size_y=20,
        win=win,
    )
    win.wait_for_close()


if __name__ == "__main__":
    main()
