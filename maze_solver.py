"""CSC111 final project, main module

Descriptions
===============================

This module include the functions to solve the maze.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. All rights reserved.

This file is Copyright (c) 2021  Chenxu Wang, Runshi Yang, Yifei Sun and Haojun Qiu
"""
from typing import Optional
from maze_generator import BinaryTreeMaze, _Cell


class NoSolutionError(Exception):
    """Returned when there is so valid solve in this maze"""


def maze_solver(maze: BinaryTreeMaze, point: _Cell, path: list[_Cell]) -> Optional[list]:
    """A maze solver detecting a path and returning backwards

    Precondition:
    - self.Cells != []
    """
    path.append(point)
    south = point.get_neighbours('south')
    east = point.get_neighbours('east')

    if point.row_index == maze.overall_row - 1 and \
            point.column_index == maze.overall_column - 1:
        return path

    elif path[0].state == 'blocked' or (path[0].get_neighbours('south').state == 'blocked'
                                        and path[0].get_neighbours('east').state == 'blocked'):
        raise NoSolutionError

    if point.walls[1] == 0 and south.state == 'naive':
        south.state = 'visited'
        point.update_cell_state()
        return maze_solver(maze, south, path)

    elif point.walls[2] == 0 and east.state == 'naive':
        east.state = 'visited'
        point.update_cell_state()
        return maze_solver(maze, east, path)

    else:
        point.update_cell_state()
        while path[-1].state != 'start':
            path[-1].state = 'blocked'
            path.pop()
        return maze_solver(maze, path[-1], path)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['typing', 'maze_generator', 'pickle'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
