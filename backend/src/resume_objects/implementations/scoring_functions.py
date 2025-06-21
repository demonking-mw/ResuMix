"""
This file stores a series of resume scoring functions.

FUNCTION DIMENSIONS:
(section_make_results: list of item_core_info, ai_result: dict of str -> dict)
-> score: int

section_make_results:
- listof(item_core_info)
    - item_core_info:
    - item_core_info is a dict with keys:
            - id: list (augmented with section id already)
            - score: dict of category -> dict of score, bias
            - height: int
    Creation of item_core_info:
    item_version_core_info = {
        "id": [self.sect_id, item_count, version_count],
        "score": version.get("score"),
        "height": version.get("height"),
    }

- ai_result:
    Example:
    "{\n"
    '    "technical": {"python": 4, "java": 1},\n'
    '    "soft": {"self_regulation": 3},\n'
    '    "relevance": {"cars": 4, "music": 0}\n'
    "}\n"

output: int
"""


def simple_sum_function(section_make_results: list, ai_result: dict) -> int:
    """
    A simple scoring function that sums the product of all items in the section with the decision.
    :param section_make_results: List of item_core_info dictionaries.
    :return: Total score as an integer.
    """
    # Logic: for each item, take the max of each trait and piecewise multiply with the decision
    total_score = 0
    for item_version in section_make_results:
        if "id" not in item_version:
            print("DEBUG: item_version missing 'id':", item_version)
        cate_list = ["technical", "soft", "relevance"]
        for cate in cate_list:
            if cate not in ai_result:
                raise ValueError(f"Category '{cate}' not found in AI result")
            item_score = item_version["score"].get(cate)  # will error if not found
            if item_score:
                for skill, score in item_score["scores"].items():
                    if skill in ai_result[cate]:
                        total_score += score * ai_result[cate][skill]
                total_score += item_score["bias"]
    return total_score
