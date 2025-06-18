'''
This file stores a series of resume scoring functions.

FUNCTION DIMENSIONS: 
(section_make_results: list of item_core_info, ai_result: dict of str -> dict)
-> score: int

item_core_info:
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
'''

def simple_sum_function(section_make_results: list, ai_result: dict) -> int:
    """
    A simple scoring function that sums the product of all items in the section with the decision.
    :param section_make_results: List of item_core_info dictionaries.
    :return: Total score as an integer.
    """
    total_score = 0
    for item_versions in section_make_results:
        for item_version in item_versions:
            total_score += item_version["score"]
    return total_score