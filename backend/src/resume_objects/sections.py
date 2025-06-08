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

from pylatex import NoEscape  # pylint: disable=import-error
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
    - make: make items build ready, 
        stores the item builds and returns score-height dict for optimization

    '''
    def __init__(self, templ: LTemplate, sect_id: int, class_dict: dict = None) -> None:
        self.template = templ
        self.title = ""
        self.sect_id = sect_id
        # template musn't be None or empty or things will break
        self.items = []
        self.aux_info = {}
        self.item_make_results = []
        if class_dict is not None:
            if class_dict["aux_info"]["type"] != "section":
                raise ValueError(
                    f"Type mismatch: expected 'section', got "
                    f"'{class_dict['aux_info']['type']}' instead"
                )
            self.title = class_dict.get("title", "")
            self.aux_info = class_dict.get("aux_info", {})
            for item_dict in class_dict.get("items", []):
                self.items.append(Item(item_dict))
        else:
            self.aux_info = {"type": "section"}

    def make(self, requirements: dict) -> list:
        '''
        make items build ready
        stores the item builds and returns score-height dict for optimization
        DOES NOT BUILD THE SECTION
        requirements is a dict storing AI decision of skills,
            and scoring function for each category.
        Returns:
        - list of list of item_core_info
        item_core_info is a dict with keys:
            - id: list (augmented with section id already)
            - score: float
            - height: int
        
        '''
        if not self.items:
            raise ValueError("No items to process in the section")
        # Normal section with headers
        results = []
        item_count = 0
        for item in self.items:
            item_build = item.build(requirements, self.template)
            self.item_make_results.append(item_build)
            version_icis = []
            version_count = 0
            for version in item_build:
                item_version_core_info = {
                    "id": [self.sect_id, item_count, version_count],
                    "score": version.get("score"),
                    "height": version.get("height")
                }
                version_icis.append(item_version_core_info)
                version_count += 1
            results.append(version_icis)
            item_count += 1
        return results

    def build(self, decision: list, templ: LTemplate) -> NoEscape:
        '''
        Builds the section with template into pylatex object
        THIS IS AFTER THE OPTIMIZATION PROCESS
        Takes in a list of item_version_ids (augmented with section id) called decision
        '''
        # Sort the decision list by the second element in each sublist
        sorted_decision = sorted(decision, key=lambda x: x[1])
        build_target_NEs = []
        for item_version_id in sorted_decision:
            item_id = item_version_id[1]
            version_id = item_version_id[2]
            item_version_build = self.item_make_results[item_id][version_id]
            item_build = item_version_build.get("object")
            build_target_NEs.append(item_build)
        # Build the section using the template's section_builder
        section_build = templ.section_builder(self.title, build_target_NEs)
        # NOT TESTED YET!!
        return section_build

    def to_dict(self) -> dict:
        '''
        Returns the dict representation of the section
        '''
        return {
            "title": self.title,
            "items": [item.to_dict() for item in self.items],
            "aux_info": self.aux_info,
        }
