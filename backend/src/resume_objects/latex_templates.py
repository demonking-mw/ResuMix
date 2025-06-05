from dataclasses import dataclass
from typing import Callable



@dataclass
class LTemplate:
    '''
    A class to represent a LaTeX template for resumes.
    Contains:
    - Wrapper code: latex code that needs to be inserted at the top of the doc
    - item_height_calculator: function taking in an item and returning its height
        - I/O: (item: Item) -> int
    - remaining_height_calculator: function taking in the number of sections and return the total height allowed
        - I/O: (sections: int) -> int
            - Note: section count should exclude headers
    '''
    wrapper_code: str
    item_height_calculator: Callable
    remaining_height_calculator: Callable
    # This class is for internal use only, handling bad input is not done AT ALL

# # Example usage of LTemplate

# def sample_item_height_calculator(item):
#     # Assume each item has a 'lines' attribute
#     return getattr(item, 'lines', 1) * 10

# def sample_remaining_height_calculator(sections):
#     # Assume each section gets 100 units of height
#     return 100 * sections

# sample_wrapper_code = r"""
# \documentclass{article}
# \usepackage{geometry}
# \geometry{margin=1in}
# """

# sample_template = LTemplate(
#     wrapper_code=sample_wrapper_code,
#     item_height_calculator=sample_item_height_calculator,
#     remaining_height_calculator=sample_remaining_height_calculator
# )