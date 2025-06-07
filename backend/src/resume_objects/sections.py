'''
The section class

represents a section in a resume. Abstracts the building process for the resume.
for the optimization process, only the scores and heights are passed on to the resume class

variables needed: 
- template: LTemplate
- items: list of Item objects
- aux_info with type as section
- style: str. Options: (x means a digit)
    - nx: normal section with x headers per item
    - nxl: normal section with x headers per item, middle item to left if applicable
    - p: each item is a paragraph
    - l: dotted list section
    - l2: dotted list section with 2 columns

functions needed: 
- build: builds the section with template into pylatex object
    - builds from a given list of item-versions
- make: make items build ready, stores the item builds and returns score-height dict for optimization

'''

from .latex_templates import LTemplate
from .items import Item

class Section:
    '''
    variables needed: 
    - template: LTemplate
    - items: list of Item objects
    - aux_info with type as section
    - style: str. Options: (x means a digit)
        - nx: normal section with x headers per item
        - nxl: normal section with x headers per item, middle item to left if applicable
        - p: each item is a paragraph
        - l: dotted list section
        - l2: dotted list section with 2 columns

    functions needed: 
    - build: builds the section with template into pylatex object
        - builds from a given list of item-versions
    - make: make items build ready, stores the item builds and returns score-height dict for optimization

    '''
    def __init__(self, class_dict: dict = None, templ: LTemplate) -> None:
        self.template = templ
        # template musn't be None or empty or things will break
        self.items = []
        self.aux_info = {}
        self.item_make_results = None
        if class_dict is not None:
            if class_dict["aux_info"]["type"] != "section":
                raise ValueError(
                    f"Type mismatch: expected 'section', got "
                    f"'{class_dict['aux_info']['type']}' instead"
                )
            self.aux_info = class_dict.get("aux_info", {})
            for item_dict in class_dict.get("items", []):
                self.items.append(Item(item_dict))
        else:
            self.aux_info = {"type": "section"}

    def make(self, processor: dict) -> list:
        '''
        make items build ready
        stores the item builds and returns score-height dict for optimization
        DOES NOT BUILD THE SECTION
        processor is a dict storing AI decision of skills,
            and scoring function for each category.
        Returns:
        - list of list of tuples
            - each tuple is (score, height)
        '''
        if not self.items:
            raise ValueError("No items to process in the section")
        # Normal section with headers
        results = []
        for item in self.items:
            item_build = item.build(processor, self.template)
            self.item_make_results = item_build
            version_tuples = []
            for version in item_build:
                score = version.get("score")
                height = version.get("height")
                version_tuples.append((score, height))
            results.append(version_tuples)
        return results

    
