from itertools import product

from .utils import cells_from_region, EMPTY_CELL


class Table:
    def __init__(self):
        self._cells = {}
        self._op_regions = {}
        self._cursor = 0
        self._op_sequence = []

    def apply_operation_at_current_location(self, operation):
        """
        Insert the given operation at the given cursor location. Yes, we have to
        be stateful here.
        """
        self._op_sequence.insert(self._cursor, operation)

        self.advance_cursor_to_position(self._cursor + 1)

    def advance_cursor_to_position(self, new_position):
        """
        Run through the op sequence from the current position to the provided
        position, and apply each action in turn.

        This can _only_ work if we're moving "forwards" through the history.
        """
        for idx in range(self._cursor, new_position):
            op = self._op_sequence[idx]
            # There's a bit of a circular dependence here. Not sure how I feel
            # about this, but maybe this is the way to go. Care should be taken
            # that any op can only _read_ the input table, and may not modify 
            # it.

            outputs, region = op.apply(self)

            for cell in cells_from_region(region):
                if cell in self._cells:
                    raise ValueError("The computed outputs would overwrite already existing data.")
                try:
                    self._cells[cell] = outputs.pop(cell)
                except KeyError:
                    self._cells[cell] = None

            if len(outputs) > 0:
                raise ValueError(
                    "Specified output region does not actually match the "
                    "shape of the provided outputs."
                )

            self._op_regions[op.id] = region
        
        self._cursor = new_position

    def rewind_cursor(self, new_position):
        """
        Runs through the op sequence in reverse, and removes the data from each
        operation.
        """
        for idx in range(self._cursor - 1, new_position - 1, -1):
            op = self._op_sequence[idx]
            region = self._op_regions[op.id]

            for cell in cells_from_region(region):
                self._cells.pop(cell)
            
        self._cursor = new_position

    def get(self, cell):
        return self._cells.get(cell, EMPTY_CELL)
    
    def get_region(self, op_id):
        return self._op_regions[op_id]
    