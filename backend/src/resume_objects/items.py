"""
The item class

it represent an item, provides its optimized states in the process of generation,
outputs pdf-able format for generation or json for storing things back into db

Item Build:
Listof item objects(dicts):
- category scores: dict of cate name and calculated scores
- Latex code for item
- Height
"""

import warnings
from typing import List
from itertools import combinations

from .lines import Line
from .latex_templates import LTemplate


class Item:
    """
    Functions needed:
    - to_dict: convert back to dictionary
    - calc_score: calculate the score of the item
        - the function is an input!!
        - takes the data of each Line object and cook
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
        self.style = ""
        if class_dict is not None:
            if class_dict["aux_info"]["type"] != "items":
                raise ValueError(
                    f"Type mismatch: expected 'items', got "
                    f"'{class_dict['aux_info']['type']}' instead"
                )
            self.style = class_dict["aux_info"]["style"]
            self.titles = class_dict.get("titles")
            for line_dict in class_dict.get("lines"):
                self.line_objs.append(Line(line_dict))
            self.cate_scores = class_dict.get("cate_scores")
            self.aux_info = class_dict.get("aux_info")
        else:
            self.cate_scores = {
                "weight": 1.0,
                "bias": 1.0,
            }

    def top_k_lines(self, lines: List[Line], k: int) -> List[Line]:
        """
        returns the top k Line objects with the highest line scores in ascending order
        """
        sorted_lines = sorted(
            lines,
            key=lambda line: (
                line.score is not None,
                line.score if line.score is not None else 0,
            ),
        )
        return sorted_lines[-k:]

    def make(self, templ: LTemplate) -> List[dict]:
        """
        returns an array where the ith element is a dict of the total score of
        using the first i highest scoring lines of this item.
        """
        list_of_items: List[dict] = []
        length = len(self.line_objs)
        for i in range(1, length + 1):
            top_k = self.top_k_lines(self.line_objs, i)
            total_score = 0
            for j in top_k:
                total_score += j.score or 0
            total_score = (
                total_score * self.cate_scores["weight"] + self.cate_scores["bias"]
            )
            item = {
                "numLines": i,
                "score": total_score,
                "height": templ.item_height_calculator(self, top_k),
                "lines_selected": top_k,
            }
            list_of_items.append(item)
        return list_of_items

    def to_dict(self) -> dict:
        """
        turn the object back to a dict for storage in db
        """
        # Ensure aux_info has 'type' and it is 'items'

        self.aux_info["type"] = "items"
        if self.style:
            self.aux_info["style"] = self.style
        else:
            self.aux_info["style"] = "n"

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
