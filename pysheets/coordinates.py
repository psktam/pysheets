from utils import Corner, get_corner


class Coordinate:

    def resolve(self, table):
        raise NotImplementedError("Implement meeeeeeeeee.")


class DirectCoordinate(Coordinate):
    """
    This is a bit brittle, but it allows you to just directly pick a coordinate
    cell and provide it as input. It should even allow empty cells.
    """

    def __init__(self, row, col):
        self._row, self._col = row, col
    
    def resolve(self, table):
        return table.get((self._row, self._col))


class OpCorner(Coordinate):

    def __init__(self, op_id, corner):
        self._op_id = op_id
        self._corner = corner

    def resolve(self, table):
        region = table.get_region(self._op_id)
        return get_corner(region, self._corner)
    

class OffsetCoordinate(Coordinate):

    def __init__(self, internal_coordinate, offset):
        self._internal_coordinate = internal_coordinate
        self._offset = offset
    
    def resolve(self, table):
        base_cell = self._internal_coordinate.resolve(table)
        return (base_cell[0] + self._offset[0], base_cell[1] + self._offset[1])
