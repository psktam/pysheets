import utils

from dataclasses import dataclass


@dataclass
class Operation:
    """Data-only structure for codifying what an operation actually is."""

    id: int
    """
    A unique identifier for this operation.
    """

    inputs: list 
    """
    Ordered list of different input types for the given function.
    """

    function: object
    """
    Encodes the logic that will actually be applied to the given inputs.
    """

    output_anchor: dict
    """
    Dictionary that specifies where the output will get written to. You provide 
    this part a single Coordinate and an enum indicating which corner of the 
    box this is going to correspond to.
    """


def apply_operation(op: Operation, table):
    """
    For the given operation, apply it to the the provided table. We will decide
    how much operations are allowed to look at tables.
    """
    realized_inputs = [selector.select(table) for selector in op.inputs]
    outputs = op.function.call(realized_inputs)
    local_region = utils.region_from_cells(outputs.keys())

    if local_region is utils.EMPTY_REGION:
        return outputs

    anchor_coordinates = op.output_anchor["coordinate"].resolve(table)
    anchor_corner = op.output_anchor["corner"]
    offset = utils.get_corner(local_region, anchor_corner)
    final_offset = (
        anchor_coordinates[0] - offset[0],
        anchor_coordinates[1] - offset[1]
    )

    return {
        (cell[0] + final_offset[0], cell[1] + final_offset[1]): value
        for (cell, value) in outputs.items()
    }
