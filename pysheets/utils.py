from itertools import product
from enum import Enum


EMPTY_REGION = object()
EMPTY_CELL = object()


class Corner(Enum):
    upper_left = "upper_left"
    upper_right = "upper_right"
    lower_left = "lower_left"
    lower_right = "lower_right"


def cells_from_region(region):
    ((first_row, first_col), (last_row, last_col)) = region
    return product(range(first_row, last_row), range(first_col, last_col))


def region_from_cells(cells):
    try:
        rows, cols = zip(*cells)
    except ValueError:
        return EMPTY_REGION
    
    return ((min(rows), min(cols)), (max(rows), max(cols)))


def get_corner(region, corner):
    ((first_row, first_col), (last_row, last_col)) = region
    return {
        Corner.upper_left: (first_row, first_col),
        Corner.upper_right: (first_row, last_col),
        Corner.lower_left: (last_row, first_col),
        Corner.lower_right: (last_row, last_col)
    }[corner]
