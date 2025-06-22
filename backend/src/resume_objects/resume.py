"""
The class that parses the resume from file
Handlles building, optimizing, etc
"""

import random
from datetime import datetime

from .sections import Section
from .line_eval import line_eval
from ..general_helper.isa_bot import AIBot


class Resume:
    """
    Recursively builds each section -> item -> line
    variables:
    - sections: list of Section objects
    - template: LTemplate
    - aux_info: dict with type as resume
    NOTE: to_dict not built yet
    """

    def __init__(self, template, class_dict=None):
        self.template = template
        self.sections = []
        self.aux_info = {"type": "resume"}
        self.items_make_results = []  # new version
        self.section_make_results = []
        self.section_build_results = []
        self.requirements = {}
        self.attribute_targets = {}  # dict of cate -> list of attributes
        self.bot = AIBot()  # AI bot for generating scores
        self.optimization_result = None  # set by optimize(), see docstring for shape
        self.make_results_flattened = (
            []
        )  # Flattened list of item_core_info for optimization
        self.heading_name = ""
        self.heading_subsequent_content = []
        if class_dict is not None:
            if class_dict["aux_info"]["type"] != "resume":
                raise ValueError(
                    f"Type mismatch: expected 'resume', got {class_dict['aux_info']['type']}"
                )
            self.aux_info = class_dict["aux_info"]
            self.sections = [
                Section(template, sect["sect_id"], sect)
                for sect in class_dict["sections"]
            ]
            if "heading_info" in class_dict:
                self.heading_name = class_dict["heading_info"]["heading_name"]
                self.heading_subsequent_content = class_dict["heading_info"][
                    "subsequent_content"
                ]
            # accessing keys in class_dict is deliberately with [],
            #   as missing keys should result in error
        else:
            self.aux_info = {"type": "resume"}

    def make(self, job_req: str) -> bool:
        """
        Make the resume build ready
        Using AI, generate the requirement
        Then make each section
        Result:
        - Makes requirement dict, update self.requirements
        - Calls make() for each section, stores the item_core_info in self.section_make_results
            - Shape of section_make_results:
            listof listof listof item_core_info(dict)
            each list corresponds to: section -> item -> version
        - Returns True if successful, False otherwise



        New version:
        Scores each line under the resume

        Result:
        assign score to line
        assign section_make_result and make_results_flattened
        return successfulness
        """
        # New version
        all_sects = self.sections
        all_items = []
        for sect in all_sects:
            all_items.extend(sect.items)
        all_lines = []
        for itm in all_items:
            all_lines.extend(itm.line_objs)
        # parse the job requirement
        parse_req = (
            "generate a list of core requirements, each in a single sentence, from the resume. The list of sentences collectively should reflect all of what the job recruiter is looking for. the length of your result list should be between 1 to 12 items. JOB REQUIREMENT: "
            + job_req
        )
        parse_instruction = "your response must be strictly a python list of strings, as it will be parsed by a program."
        req_success, job_requirement_list = self.bot.pythoned_response_instruction(
            parse_req, parse_instruction, datatype=list
        )
        if not req_success:
            print("DEBUG: parse requirement failed")
            return False
        # parse_instruction is proper
        # call line_eval
        if not line_eval(job_requirement_list, all_lines):
            print("DEBUG: line_eval failed")
            return False
        for section in self.sections:
            item_core_info = section.make()  # Deprecate requirements
            for item_info_list in item_core_info:
                self.make_results_flattened.append(item_info_list)
            if item_core_info is None:
                print(f"DEBUG: Failed to make section {section.sect_id}")
                return False
            self.section_make_results.append(item_core_info)

    def optimize(self, evaluator: callable, shuffle_times=2) -> bool:
        """
        Optimize the resume using the AI decision generated in make()

        Input: evaluator:
        (section_make_results: list of item_core_info, ai_result: dict of str -> dict)
        -> score: int

        GIVEN: evaluator is very close to a linear function, and it is none-decreasing

        Result:
        - updates self.optimization_result
        - returns True if successful, False otherwise

        shape of self.optimization_result:
        listof section_decision,
            section_decision is a list of item_version_ids

        Process: apply the algorithm on the flattened list, then sort them to sections and return
        """

        # Here it's given that line_eval worked
        #

        start_time = datetime.now()
        print("DEBUG: Optimizing resume with evaluator")
        width = len(self.make_results_flattened)
        # Width is the number of items in the resume
        height = int(self.template.remaining_height_calculator(len(self.sections)))
        # Height is the physical height of the resume in pixels
        time_comp_count = 0
        if not self.make_results_flattened:
            print("DEBUG: No items to optimize, empty resume")
            return False
        data_list = self.make_results_flattened
        max_variant_score = 0
        max_result = []  # a list of ici
        for _ in range(shuffle_times):
            random.shuffle(data_list)
            dp_list = [[[] for _ in range(width)] for _ in range(height)]
            # Each item in dp_list is a list of ici (with id, score, height)
            for w in range(width):
                for h in range(height):
                    max_score = (
                        evaluator(
                            [item for item in dp_list[h][w - 1]],
                            self.requirements,
                        )
                        if w > 0
                        else 0
                    )
                    dp_list[h][w] = dp_list[h][w - 1] if w > 0 else []
                    # This represents not adding the item in question
                    for version in data_list[w]:
                        time_comp_count += 1
                        if version["height"] <= h:
                            # If first item
                            if w == 0:

                                score = evaluator([version], self.requirements)
                                if score > max_score:
                                    max_score = score
                                    dp_list[h][w] = [version]
                            # If not first item
                            else:
                                resume_score_list = [
                                    item
                                    for item in dp_list[h - version["height"]][w - 1]
                                ]
                                resume_score_list.append(version)
                                score = evaluator(resume_score_list, self.requirements)
                                if score > max_score:
                                    max_score = score
                                    dp_list[h][w] = dp_list[h - version["height"]][
                                        w - 1
                                    ] + [version]
            current_max_score = evaluator(
                [item for item in dp_list[height - 1][width - 1]],
                self.requirements,
            )
            if current_max_score > max_variant_score:
                max_variant_score = current_max_score
                max_result = dp_list[height - 1][width - 1]
        # ABOVE NOT TESTED, CAN BE VERY WRONG
        # Currently not building the swap algorithm, as DP should be decent for the job.
        # Will implement if need arises
        print("DEBUG: time complexity:", time_comp_count)
        result_len = len(self.sections)
        self.optimization_result = [[] for _ in range(result_len)]
        for ici in max_result:
            ids = ici["id"]
            section_id = ids[0]
            self.optimization_result[section_id].append(ids)
        print("DEBUG: Optimization FINISHED")
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("DEBUG: Optimization timespan: ", elapsed_time)
        return True

    def build(self) -> bytes:
        """
        Build the resume using the template and the optimization result
        Procedure:
        1. builde each section, extend the build list
        2. toss the section_build_results into the template's build function
        3. pass the result on by returning it
        Use template's resume build function to build
        """
        self.section_build_results = []
        if not self.optimization_result:
            print("DEBUG: No optimization result, cannot build")
            return b""
        for section in self.sections:
            if not section.items:
                print(f"DEBUG: Section {section.sect_id} has no items, skipping")
                continue
            section_build = section.build(
                self.optimization_result[section.sect_id], self.template
            )
            # Result of seciton_build should be a 1d list
            self.section_build_results.extend(section_build)
        # Call the resume build function in the template
        print("DEBUG: Building resume with template")
        return self.template.resume_builder(self)

    def to_dict(self) -> dict:
        """
        Compile the class into a dict for storage
        """
        result = {
            "aux_info": self.aux_info,
            "heading_info": {
                "heading_name": self.heading_name,
                "subsequent_content": self.heading_subsequent_content,
            },
            "sections": [section.to_dict() for section in self.sections],
        }
        if self.heading_name or self.heading_subsequent_content:
            result["heading_info"] = {
                "heading_name": self.heading_name,
                "subsequent_content": self.heading_subsequent_content,
            }
        return result
