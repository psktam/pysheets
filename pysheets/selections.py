from collections import OrderedDict
from itertools import product


class Selection:
    
    def select(self, table):
        raise NotImplementedError



class EmptySelection(Selection):

    def select(self, table):
        return []


class BoxSelection(Selection):

    def __init__(self, upper_left, lower_right):
        self._upper_left = upper_left
        self._lower_right = lower_right

    def select(self, table):
        first_row, first_col = self._upper_left.resolve(table)
        last_row, last_cal = self._lower_right.resolve(table)

        # Box selection returns selections from left to right, then 
        # top-to-bottom
        selection = OrderedDict()

        rows = range(first_row, last_row)
        columns = range(first_col, last_cal)

        for (row, col) in product(rows, columns):
            selection[row, col] = table[row, col]
        return selection