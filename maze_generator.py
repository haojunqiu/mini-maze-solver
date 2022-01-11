"""CSC111 final project, main module

Descriptions
===============================

This module include the class _Cell and BinaryTreeMaze.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. All rights reserved.

This file is Copyright (c) 2021  Chenxu Wang, Runshi Yang, Yifei Sun and Haojun Qiu
"""
from __future__ import annotations
import random
from typing import Any, Optional
import pickle
import pygame


class _Cell:
    """A cell class that represents a grid cell.

    Instance Attributes:
        - row_index: row index of cell in a maze
        - column_index: column index of cell in a maze
        - coordinates: a tuple representing the coordinates of the cell, in the form of
          (row_index, column_index)
        - neighbours: The cells that are adjacent of this cell
        - walls: a list of four element representing whether there is a wall at direction
         'west', 'south', 'east' and 'north'

    Representation Invariants:
        - self.row_index >= 0 and self.row_index <= overall_row
        - self.column_index >= 0 and self.column_index <= overall_column
        - self.coordinates == (self.row_index, self.column_index)
        - len(self.walls) == 4 and all(wall == 1 or wall == 0 for wall in self.walls)
    """
    row_index: int
    column_index: int
    coordinates: tuple[int, int]
    neighbours: set[_Cell]
    walls: list[int]
    state: str

    def __init__(self, neighbours: set[_Cell], row_index: int = 0,
                 column_index: int = 0) -> None:
        """Initialize a new grid cell """
        self.row_index = row_index
        self.column_index = column_index
        self.coordinates = (self.row_index, self.column_index)
        self.neighbours = neighbours
        self.walls = [1, 1, 1, 1]
        self.state = 'naive'

    def check_connected(self, other_cell: _Cell, visited: set[_Cell]) -> bool:
        """Return whether cell and other_cell are connected """

        if other_cell.coordinates == self.coordinates:
            return True
        else:
            visited.add(self)
            for u in self.neighbours:
                if u not in visited and u.check_connected(other_cell, visited):
                    return True
            return False

    def get_neighbours(self, direction: str) -> Optional[_Cell]:
        """Return the neighbours according to the directions provided, return None if
        self has no neighbour in direction given.

         Preconditions:
            - direction in {'north','south', 'west', 'east'}
        """
        if direction == 'north':
            target_coordinate = (self.row_index - 1, self.column_index)
        elif direction == 'south':
            target_coordinate = (self.row_index + 1, self.column_index)
        elif direction == 'east':
            target_coordinate = (self.row_index, self.column_index + 1)
        else:
            target_coordinate = (self.row_index, self.column_index - 1)
        for neighbour in self.neighbours:
            if neighbour.coordinates == target_coordinate:
                return neighbour
        return None

    def update_cell_state(self) -> None:
        """Update the cell's state according to condition only change them
        when they are blocked or a new start"""
        south = self.get_neighbours('south')
        east = self.get_neighbours('east')

        if self.walls[2] == 1 or east is None or east.state == 'blocked':
            if self.walls[1] == 1 or south is None or south.state == 'blocked':
                self.state = 'blocked'
        elif south is not None and south.state == 'naive' and self.walls[1] == 0:
            self.state = 'start'
        elif east is not None and east.state == 'naive' and self.walls[2] == 0:
            self.state = 'start'
        else:
            return

    def draw(self, width: int, screen: pygame.Surface, path: list = None) -> None:
        """Draw a grid on the screen given.
        The input width represent the width of each grid
        """
        if path is None:
            path = []

        blue = (0, 0, 255)
        black = (0, 0, 0)  # the color black
        # draw a line as the left
        if self.walls[0] == 1:
            pygame.draw.line(screen, black,
                             (self.column_index * width, self.row_index * width,),
                             (self.column_index * width, (self.row_index + 1) * width), 1)
        # draw a line as the bottom
        if self.walls[1] == 1:
            pygame.draw.line(screen, black,
                             (self.column_index * width, (self.row_index + 1) * width),
                             ((self.column_index + 1) * width, (self.row_index + 1) * width), 1)
        # draw a line as the right
        if self.walls[2] == 1:
            pygame.draw.line(screen, black,
                             ((self.column_index + 1) * width, (self.row_index + 1) * width),
                             ((self.column_index + 1) * width, self.row_index * width), 1)

        # draw a line as the top
        if self.walls[3] == 1:
            pygame.draw.line(screen, black,
                             ((self.column_index + 1) * width, self.row_index * width),
                             (self.column_index * width, self.row_index * width), 1)

        if self in path:
            rect = pygame.Rect(self.column_index * width, self.row_index * width, width, width)
            pygame.draw.rect(screen, blue, rect)


class BinaryTreeMaze:
    """A class that represents a binary generated maze
    Instance Attributes:
        - overall_row: an integer representing the number of rows in the maze
        - overall_column: an integer representing the number of columns in the maze
        - cells: a list of all the cells in the maze
    Representation Invariants:
        - all(cell.row_index <= self.overall_row for cell in self.Cells)
        - all(cell.column_index <= self.overall_column for cell in self.Cells)
    """
    overall_row: int
    overall_column: int
    cells: list[_Cell]

    def __init__(self, overall_row: int = 0,
                 overall_column: int = 0) -> None:
        """Initialize a new binary maze."""
        self.overall_row = overall_row
        self.overall_column = overall_column

        # Initialize cells, by appending _Cell object with its coordinates in the maze being set
        self.cells = []
        for row in range(0, self.overall_row):
            for column in range(0, self.overall_column):
                new_cell = _Cell(set(), row, column)
                self.add_cell(new_cell)

        self.initiate_start()

    def add_cell(self, cell: _Cell) -> None:
        """Add a cell to this maze.

        The new cell is not adjacent to any other vertices.
        """
        self.cells.append(cell)

    def initiate_start(self) -> None:
        """Initiate start of the maze"""
        self.cells[0].state = 'start'

    def add_neighbour(self, cell1: _Cell, cell2: _Cell) -> None:
        """Connect cell1 and cell2 in this maze.

        Raise a ValueError if cell1 or cell2 is not in the maze.
        """
        if cell1 in self.cells and cell2 in self.cells:
            if cell2 not in cell1.neighbours:
                cell1.neighbours.add(cell2)
                cell2.neighbours.add(cell1)
        else:
            raise ValueError

    def add_direction_neighbour(self, cell1: _Cell) -> None:
        """Add cell1's neighbours from all directions to cell1 in the current maze."""
        north = (cell1.row_index - 1, cell1.column_index)
        south = (cell1.row_index + 1, cell1.column_index)
        east = (cell1.row_index, cell1.column_index + 1)
        west = (cell1.row_index, cell1.column_index - 1)
        directions = [north, south, east, west]
        for cell2 in self.cells:
            if cell2.coordinates in directions:
                self.add_neighbour(cell1, cell2)

    def get_north_direction_neighbour(self, cell1: _Cell) -> Any:
        """Return cell1's north neighbour in the current maze."""
        north = (cell1.row_index - 1, cell1.column_index)
        for cell2 in self.cells:
            if cell2.coordinates == north:
                return cell2
        return None

    def get_west_direction_neighbour(self, cell1: _Cell) -> Any:
        """Return cell1's west neighbour in the current maze."""
        west = (cell1.row_index, cell1.column_index - 1)

        for cell2 in self.cells:
            if cell2.coordinates == west:
                return cell2
        return None

    def connected(self, cell1: _Cell, cell2: _Cell) -> bool:
        """Return whether cell1 and cell2 are connected cells in this maze."""
        if cell1 in self.cells and cell2 in self.cells:
            return cell1.check_connected(cell2, set())
        else:
            return False

    def draw_grids(self, width: int, screen: pygame.Surface, path: list = None) -> None:
        """Draw multiple grids with the input width on the screen given."""
        for cell in self.cells:
            cell.draw(width, screen, path)

    def binary_tree_algorithm(self) -> None:
        """Using the binary tree algorithm to modify the grids and
        Create a random generated maze."""
        for cell in self.cells:
            north = self.get_north_direction_neighbour(cell)
            west = self.get_west_direction_neighbour(cell)
            direction = random.choice(['north', 'west'])
            if north is None and west is None:
                cell.walls = [1, 1, 1, 1]  # do nothing
            elif direction == 'north' and north is None:
                cell.walls[0] = 0  # remove the west wall instead
                west.walls[2] = 0
                self.add_neighbour(cell, west)
            elif direction == 'north' and north is not None:
                cell.walls[3] = 0  # remove the north wall between two cells
                north.walls[1] = 0
                # make connection between cell and its north cell
                self.add_neighbour(cell, north)
            elif direction == 'west' and west is not None:
                cell.walls[0] = 0  # remove the west wall between two cells
                west.walls[2] = 0
                # make connection between cell and its west cell
                self.add_neighbour(cell, west)
            elif direction == 'west' and west is None:
                cell.walls[3] = 0  # remove the north wall instead
                north.walls[1] = 0
                self.add_neighbour(cell, north)

    def draw_maze(self, size: tuple, path: list = None) -> None:
        """Visualize the current maze using the size of the screen provided.

        Since we want each cell to be a square, the result width we get by dividing size with
        overall rows and columns must be the same.

        Preconditions:
            - int(size[0]/ self.overall_row) == int(size[1]/ self.overall_column)"""

        pygame.init()
        screen = pygame.display.set_mode(size)
        width = int(size[0] / self.overall_row)
        screen.fill(pygame.Color('grey'))
        self.draw_grids(width, screen, path)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


def pickle_maze(maze: BinaryTreeMaze, filename: str) -> None:
    """ save your favorite maze object in the file name provided
     using pickle library"""
    with open(filename, 'wb') as pickle_file:
        pickle.dump(maze, pickle_file)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pygame', 'random', 'typing', 'pickle'],
        'allowed-io': ['pickle_maze'],
        'max-line-length': 100,
        'disable': ['E1136'],
        'generated-members': ['pygame.*']
    })
