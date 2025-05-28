"""
The item class

it represent an item, stores its optimized states in the process of generation,
outputs pdf-able format for generation or json for storing things back into db

Item Build:
Listof item objects(dicts):
- category scores: dict of cate name and calculated scores
- Latex code for item
- Height
"""

from pylatex import Fragment

from pylatex import Command, NoEscape
from .lines import Line


class Item:
    """
    Functions needed:
    - build: takes in a weight set, make the best item with different length
        - result of build: list of dictionaries
    - to_dict: convert back to dictionary
    -
    Variables needed:
    - Title: list
    - Lines: list of Lines class
    - Cate_scores: dict (weight and bias)
    - Aux_info: dict (with identification info)
        - header_format: char: l/j/n/r, see build for detail
    """

    def __init__(self, class_dict: dict = None) -> None:
        self.titles = []
        self.line_objs = []
        self.cate_scores = {}
        self.aux_info = {}
        if class_dict is not None:
            if class_dict["aux_info"]["type"] != "items":
                raise ValueError(
                    f"Type mismatch: expected 'items', got "
                    f"'{class_dict['aux_info']['type']}' instead"
                )
            self.titles = class_dict.get("titles")
            for line_dict in class_dict.get("lines"):
                self.line_objs.append(Line(line_dict))
            self.cate_scores = class_dict.get("cate_scores")
            self.aux_info = class_dict.get("aux_info")

    def make_specific(self, lines_sel: list = None) -> dict:
        """
        make a build dict with selected lines
        dictionary contains: pylatex object, scores
        """
        selected_lines = []
        if lines_sel is None:
            selected_lines = self.line_objs
        else:
            for line_no in lines_sel:
                selected_lines.append(self.line_objs[line_no])
        entry_container = Fragment()

        # Append the \resumeSubheading command
        if len(self.titles) == 4:
            # 4 titles item
            entry_container.append(
                Command(
                    "resumeSubheading",
                    arguments=[
                        NoEscape(self.titles[0]),
                        NoEscape(self.titles[1]),
                        NoEscape(self.titles[2]),
                        NoEscape(self.titles[3]),
                    ],
                )
            )
        else:
            print("ERROR: OTHER LENGHTS ARE NOT IMPLEMENTED")
        entry_container.append(Command("resumeItemListStart"))
        for line in selected_lines:
            # line is the Lines object, do not forget that
            entry_container.append(
                Command("resumeItem", arguments=NoEscape(line.content))
            )
        entry_container.append(Command("resumeItemListEnd"))
        return {"object": entry_container, "score": self.calc_scores()}

    def calc_scores(self) -> dict:
        """
        returns the category scores of the item under a specific build
        NOT IMPLEMENTED YET
        """
        return {}

    def to_dict(self) -> dict:
        """
        turn the object back to a dict for storage in db
        """
        # Ensure aux_info has 'type' and it is 'items'

        self.aux_info["type"] = "items"
        return {
            "titles": self.titles if self.titles is not None else [],
            "lines": (
                [line.to_dict() for line in self.line_objs]
                if self.line_objs is not None
                else []
            ),
            "cate_scores": self.cate_scores if self.cate_scores is not None else {},
            "aux_info": self.aux_info,
        }
