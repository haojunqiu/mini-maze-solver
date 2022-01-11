"""CSC111 final project, main module

Descriptions
===============================

This module perform our computations on the data.
By calling all the functions, it will produce all outputs we need.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. All rights reserved.

This file is Copyright (c) 2021  Chenxu Wang, Runshi Yang, Yifei Sun and Haojun Qiu
"""
import pygame
import sys
from maze_generator import BinaryTreeMaze, _Cell
from maze_solver import maze_solver
CELL = _Cell(set())
SIZE = (700, 700)
WIDTH = 30


def run_example1(cell: _Cell, size: tuple, width: int) -> None:
    """Run a pygame window that visualizes a cell according to the size
    and width provided

    Example call:
        - run_example1(CELL, SIZE, WIDTH)
    """
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('white'))
    cell.draw(width, screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def run_example2(size: tuple, width: int) -> None:
    """run a pygame window that visualizes a screen of grids
    according to the size and width provided

    Example call:
        - run_example2(SIZE, WIDTH)
    """
    pygame.init()
    screen = pygame.display.set_mode(size)
    rows = int(size[0] / width)
    columns = int(size[1] / width)
    screen.fill(pygame.Color('grey'))
    sys.setrecursionlimit(rows * columns)
    maze = BinaryTreeMaze(rows, columns)
    maze.draw_grids(width, screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def run_example3(size: tuple, width: int) -> None:
    """run a pygame window that visualizes a maze
    according to the size and width provided

    Example call:
        - run_example3(SIZE, WIDTH)
    """
    pygame.init()
    screen = pygame.display.set_mode(size)
    rows = int(size[0] / width)
    columns = int(size[1] / width)
    screen.fill(pygame.Color('grey'))
    maze = BinaryTreeMaze(rows, columns)
    maze.binary_tree_algorithm()
    maze.draw_grids(width, screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def run_example4(size: tuple, width: int) -> None:
    """Visualize a path generated from the maze we have produced

    Example call:
        - run_example4(SIZE, WIDTH)
    """
    rows = int(size[0] / width)
    columns = int(size[1] / width)
    sys.setrecursionlimit(2 * rows * columns)
    maze = BinaryTreeMaze(rows, columns)
    maze.binary_tree_algorithm()
    path = maze_solver(maze, maze.cells[0], [])
    maze.draw_maze(size, path)
