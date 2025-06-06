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

from itertools import combinations
from pylatex import Command, NoEscape, Itemize, MiniPage

from .lines import Line
from .latex_templates import LTemplate



class Item:
    """
    Functions needed:
    - build: takes in a weight set, make the best item with different length
        - result of build: list of dictionaries
            - each dict contains the latex object,
    - make_specific: make a specific item with selected lines, mainly for inter
    - to_dict: convert back to dictionary
    - calc_score: calculate the score of the item
        - the function is an input!!
        - takes the data of each Line object and cook
    - get_skills_dict: get the skills dict for the item
        - gets from each line object, and returns a dict of skills (not overlapping)
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
        self.paragraph = r""
        self.style = ""
        if class_dict is not None:
            if class_dict["aux_info"]["type"] != "items":
                raise ValueError(
                    f"Type mismatch: expected 'items', got "
                    f"'{class_dict['aux_info']['type']}' instead"
                )
            self.style = class_dict["aux_info"]["style"]
            if self.style == "p":
                self.paragraph = class_dict.get("paragraph")
            else:
                self.titles = class_dict.get("titles")
                for line_dict in class_dict.get("lines"):
                    self.line_objs.append(Line(line_dict))
                self.cate_scores = class_dict.get("cate_scores")
                self.aux_info = class_dict.get("aux_info")
        else:
            self.cate_scores = {
                "technical": {
                    "weight": 1.0,
                    "bias": 1.0,
                },
                "soft": {
                    "weight": 1.0,
                    "bias": 1.0,
                },
                "relevant": {
                    "weight": 1.0,
                    "bias": 1.0,
                },
            }



    def make_specific(
        self, lines_score: int, lines_sel: list, templ: LTemplate
    ) -> dict:
        """
        make a build dict with selected lines and given score
        dictionary contains: pylatex object, scores
        scores won't be calculated if processor is None
        """
        selected_lines = []
        if lines_sel is not None:
            lines_sel = sorted(lines_sel)
        if self.style == "p":
            raise RuntimeError("NOT IMPLEMENTED YET.")
        else:
            for line_no in lines_sel:
                selected_lines.append(self.line_objs[line_no])
        # NoEscape for Latex safety

        # Append the \resumeSubheading command
        if len(self.titles) == 4:
            latex = (
                r"\resumeSubheading"
                f"{{{self.titles[0]}}}{{{self.titles[1]}}}{{{self.titles[2]}}}{{{self.titles[3]}}}\n"
                r"\resumeItemListStart"
                "\n"
            )
            for line in selected_lines:
                latex += f"    \\resumeItem{{{line.content}}}\n"
            latex += r"\resumeItemListEnd" "\n"
            latex_obj = NoEscape(latex)
        else:
            raise NotImplementedError("ERROR: OTHER LENGTHS ARE NOT IMPLEMENTED")
        return {
            "object": latex_obj,
            "score": lines_score,
            "height": templ.item_height_calculator(self),
        }

    def build(self, templ: LTemplate, processor: dict) -> list:
        """
        build the item with given processor
        template is used to calculate the height of the item
        ASSUMPTION: using different lines won't make major difference in height
        right here, throw error if information is missing and build is impossible
        """
        if self.style == "p":
            raise RuntimeError("NOT IMPLEMENTED YET.")
        else:
            # Check for required information
            if not self.titles or not self.line_objs or templ is None or processor is None:
                raise ValueError("Missing required information: titles, lines, template, or processor.")
            # Implement the rest of the build logic here
            results = []
            num_lines = len(self.line_objs)
            for sel_size in range(0, num_lines + 1):
                # allows empty selection
                if sel_size == 0:
                    # empty selection, no lines selected
                    results.append(
                        self.make_specific(0, [], templ)
                    )
                    continue
                max_score = -100000
                max_lines_sel = []
                for lines_sel_tup in combinations(range(num_lines), sel_size):
                    lines_sel = list(lines_sel_tup)
                    curr_score = self.calc_scores(lines_sel, processor)
                    if curr_score > max_score:
                        max_score = curr_score
                        max_lines_sel = lines_sel
                results.append(
                    self.make_specific(max_score, max_lines_sel, templ)
                )
            return results

    def get_skills_dict(self) -> dict:
        """
        get the skills dict for the item
        returns a dict of skills (not overlapping)
        """
        skills_dict =  {"technical": [], "soft": [], "relevance": []}
        for line_obj in self.line_objs:
            cate_list = ["technical", "soft", "relevance"]
            if not line_obj.cate_score:
                line_obj.gen_score()
            for cate_name in cate_list:
                for skill, score in line_obj.cate_score[cate_name].items():
                    if skill not in skills_dict[cate_name]:
                        skills_dict[cate_name].append(skill)
        return skills_dict

    def calc_scores(
        self, lines_sel: list, processor: dict, default_weight: int = 3
    ) -> dict:
        """
        returns the category scores of the item under a specific build (given by lines_sel)

        Processor: a dict storing instruction on how to process items
        {values: {cate: {} ~...}, functions: {cate: funcn}}
        values are AI generated for each value present in each category

        function is for scoring a category of an item:
        (weight: int, bias: int, products: listof int) -> (score: int)
        MAJOR ASSUMPTION: THIS WILL NOT BE CALLED IF ANY LINE OBJ IS EMPTY,
            WILL THROW ERROR OTHERWISE

        return value: dict of category -> score
        """
        overall_scores = {}
        defaulted_count = 0
        lines_sel = sorted(lines_sel)
        target_lines = []
        for line_no in lines_sel:
            target_lines.append(self.line_objs[line_no])
        cate_list = ["technical", "soft", "relevant"]
        for cate_name in cate_list:
            cate_score = []
            cate_weights = processor["values"][
                cate_name
            ]  # the weights of each attribute assigned by AI
            for line_obj in target_lines:
                line_prod_list = []
                for cate, value in line_obj.cate_score[cate_name].items():
                    if cate in cate_weights:
                        line_prod_list.append(value * cate_weights[cate])
                    else:
                        line_prod_list.append(value * default_weight)
                        defaulted_count += 1
                cate_score.append(line_prod_list)
            cate_funcn = processor["functions"][cate_name]
            overall_scores[cate_name] = cate_funcn(
                self.cate_scores[cate_name]["weight"],
                self.cate_scores[cate_name]["bias"],
                cate_score,
            )
        # overall_score is a dict of category(str) -> score(int)
        return overall_scores

    def to_dict(self) -> dict:
        """
        turn the object back to a dict for storage in db
        """
        # Ensure aux_info has 'type' and it is 'items'

        self.aux_info["type"] = "items"
        self.aux_info["style"] = self.style

        return {
            "titles": self.titles if self.titles is not None else [],
            "lines": (
                [line.to_dict() for line in self.line_objs]
                if self.line_objs is not None
                else []
            ),
            "cate_scores": self.cate_scores if self.cate_scores is not None else {},
            "aux_info": self.aux_info,
            "paragraph": self.paragraph,
        }
