"""
The class that parses the resume from file
Handlles building, optimizing, etc
"""

from .sections import Section
from ..general_helper.isa_bot import AIBot
import random


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

    def __pre_make(self) -> bool:
        """
        Gget the list of attributes for gpt parsing
        DOES NOT assume that the resume is not empty
        Result:
        - Modifies self.attribute_targets
        - Returns True if the next step should be done, False otherwise
        """
        if not self.sections or not self.template:
            print("DEBUG: No sections or template found , EMPTY RESUME, cannot make")
            return False

        # Get the attributes for gpt parsing
        full_attributes = {"technical": [], "soft": [], "relevance": []}
        for section in self.sections:
            section_skills = section.get_skills_dict()
            for cate, _ in full_attributes.items():
                full_attributes[cate].extend(section_skills[cate])
                full_attributes[cate] = list(set(full_attributes[cate]))
        self.attribute_targets = full_attributes
        return True

    def make(self, job_req: str) -> bool:
        """
        Make the resume build ready
        Using AI, generate the requirement
        Then make each section
        Result:
        - Calls __pre_make()
        - Makes requirement dict, update self.requirements
        - Calls make() for each section, stores the item_core_info in self.section_make_results
            - Shape of section_make_results:
            listof listof listof item_core_info(dict)
            each list corresponds to: section -> item -> version
        - Returns True if successful, False otherwise
        """
        if not self.__pre_make():
            return False

        # Generate the requirements dictionary
        reminder = (
            "Remember, your answer MUST be ONLY a python dictionary, "
            "as it will be parsed by a program\n"
            "Note that you must cover every attribute in the attributes dictionary I provided,\n"
        )
        job_prompt = "The following is a job description for a position: " + job_req

        instruction = (
            "Generate me a python dictionary reflecting "
            "how much each of these attributes matters for the job "
            "and how much showcasing them in the resume will help the candidate land the job.\n"
            "Here are the attributes you need to consider, "
            "they are divided into categories, note that soft means soft skills, "
            "and relevance contains passions/interest "
            "that the person might showcase in the resume.\n"
            f"Attributes: {self.attribute_targets}\n"
        )
        response_spec = (
            "Your response should be a python dictionary with the following structure:\n"
            "{\n"
            '    "technical": {"attribute_name": score, ...},\n'
            '    "soft": {"attribute_name": score, ...},\n'
            '    "relevance": {"attribute_name": score, ...}\n'
            "}\n"
            "Where score is an integer from 0 to 5, representing "
            "how important the attribute is for the job.\n"
            "Scoring standard:\n"
            "0: Not relevant/important at all\n"
            "1: remotely relevant or tangible, can draw vague "
            "connection to the job and the companys interest\n"
            "2: relevant to the industry that the job is in, "
            "but not closely related to the jobs content\n"
            "3~5: relevant to the job requirements, "
            "with 5 being a direct mention of equivalent skills in the job description or "
            "that the skill is required for the jobs responsibilities.\n"
        )
        prompt = job_prompt + instruction + response_spec + reminder
        prompt_instruction = (
            "When you are asked a question, first analyze it, then output ONLY a python "
            "dictionary that contains the answer. Sample output: "
            "(NEGLECT THE CONTENT OF THE DICT BELOW, only look at how it is formatted):\n"
            "{\n"
            '    "technical": {"python": 4, "java": 1},\n'
            '    "soft": {"self_regulation": 3},\n'
            '    "relevance": {"cars": 4, "music": 0}\n'
            "}\n"
            "Note: the dictionary should contain keys of type string and values of type int. "
            "Do not output anything else. Also, whenever giving something a score, make it out of 3"
        )
        req_status, requirements_dict = self.bot.pythoned_response_instruction(
            prompt,
            prompt_instruction,
            datatype=dict,
            # model=self.template.model,
            token_limit=2000,
            retries=3,
            temperature=0.1,
        )
        # Note: for now, use default AI model
        if not req_status:
            print("DEBUG: Failed to get requirements from AI")
            return False
        print("DEBUG: Requirements generated in resume:", requirements_dict)
        self.requirements = requirements_dict
        # Make each section using self.requirements
        for section in self.sections:
            item_core_info = section.make(self.requirements)
            for item_info_list in item_core_info:
                self.make_results_flattened.append(item_info_list)
            if item_core_info is None:
                print(f"DEBUG: Failed to make section {section.sect_id}")
                return False
            self.section_make_results.append(item_core_info)
        print("DEBUG: ready for optimization")
        return True

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
        print(
            "DEBUG: Optimizing resume with evaluator, make_results:flattened is:",
            self.make_results_flattened,
        )
        width = len(self.make_results_flattened)
        # Width is the number of items in the resume
        height = int(self.template.remaining_height_calculator(len(self.sections)))
        # Height is the physical height of the resume in pixels
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
        result_len = len(self.sections)
        self.optimization_result = [[] for _ in range(result_len)]
        for ici in max_result:
            ids = ici["id"]
            section_id = ids[0]
            self.optimization_result[section_id].append(ids)
        print("DEBUG: Optimization FINISHED")
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
