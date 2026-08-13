"""
The class that parses the resume from file
Handlles building, optimizing, etc
"""

import random
import copy
from datetime import datetime

from .sections import Section
from .line_eval import line_eval
from ..general_helper.isa_bot import AIBot

MIN_JOB_DESCRIPTION_CHARS = 40


class ResumeGenerationError(RuntimeError):
    """A generation step failed for a reason worth showing the user."""

    def __init__(self, message: str, code: str = "generation_failed") -> None:
        super().__init__(message)
        self.code = code


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
        self._bot = None  # built on first use so loading a resume needs no model config
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

    @property
    def bot(self) -> AIBot:
        """The language-model client, created on first use."""
        if self._bot is None:
            self._bot = AIBot()
        return self._bot

    def make(self, job_req: str, no_cache: bool = False) -> bool:
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

        Raises ResumeGenerationError when the input or an external service makes
        generation impossible, so the caller can report why.

        New version:
        Scores each line under the resume

        Result:
        assign score to line
        assign section_make_result and make_results_flattened
        return successfulness
        """
        job_req = (job_req or "").strip()
        if len(job_req) < MIN_JOB_DESCRIPTION_CHARS:
            raise ResumeGenerationError(
                "The job description is too short to tailor a resume from. "
                f"Paste at least {MIN_JOB_DESCRIPTION_CHARS} characters.",
                code="job_description_too_short",
            )

        # New version
        all_sects = self.sections
        all_items = []
        for sect in all_sects:
            all_items.extend(sect.items)
        all_lines = []
        for itm in all_items:
            all_lines.extend(itm.line_objs)
        if not all_lines:
            raise ResumeGenerationError(
                "This resume has no bullet points yet. Add at least one line to "
                "an item in your master resume.",
                code="empty_resume",
            )
        # parse the job requirement
        parse_req = (
            "generate a list of core requirements, each in a single sentence and outlines the requirement of a single skill from the resume. The list of sentences collectively should reflect all of what the job recruiter is looking for. the length of your result list should be between 1 to 12 items. Some of the items in your list should be soft skills inferred from the job requirement or relevant knowledge requirement inferred from the company context. JOB REQUIREMENT: "
            + job_req
        )
        parse_instruction = "your response must be strictly a python list of strings, as it will be parsed by a program."
        req_success, job_requirement_list = self.bot.pythoned_response_instruction(
            parse_req, parse_instruction, datatype=list
        )
        if not req_success or not job_requirement_list:
            raise ResumeGenerationError(
                "The language model did not return usable requirements for this "
                "job description. Try again, or switch OPENAI_MODEL to a stronger model.",
                code="requirement_parsing_failed",
            )
        # parse_instruction is proper
        # call line_eval
        if not line_eval(job_requirement_list, all_lines, no_cache):
            raise ResumeGenerationError(
                "Scoring failed: the sentence-transformer model could not be loaded. "
                "Run python scripts/fetch_model.py, or check OPT_MODEL_PATH in .env.",
                code="scoring_failed",
            )
        for section in self.sections:
            if not section.items:
                # A section the user has not filled in yet is simply skipped.
                self.section_make_results.append([])
                continue
            item_core_info = section.make()  # Deprecate requirements
            if item_core_info is None:
                print(f"DEBUG: Failed to make section {section.sect_id}")
                return False
            for item_info_list in item_core_info:
                self.make_results_flattened.append(item_info_list)
            self.section_make_results.append(item_core_info)
        return True

    def optimize(self, shuffle_times=2) -> bool:
        """
        Optimize the resume using the AI decision generated in make()

        Result:
        - updates self.optimization_result
        - returns True if successful, False otherwise

        shape of self.optimization_result:
        listof section_decision,
            section_decision is a list of item_version_ids

        Process: apply the algorithm on the flattened list, then sort them to sections and return


        New version:
        at this point, section_make done, similar to old
        - score is number now!!

        Side effect:
        update self.optimization_result
        shape of self.optimization_result:
        listof section_decision,
            section_decision is a list of item_version_ids

        Return: bool for successfullness
        """

        # Here it's given that line_eval worked
        #

        start_time = datetime.now()
        width = len(self.make_results_flattened)
        # Width is the number of items in the resume
        height = int(self.template.remaining_height_calculator(len(self.sections)))

        if not self.make_results_flattened:
            print("DEBUG: No items to optimize, empty resume")
            return False
        data_list = self.make_results_flattened
        max_variant_score = 0
        max_result = []  # a list of ici
        dp_list = [[[] for _ in range(width)] for _ in range(height)]
        # Each item in dp_list is a list of [score, list of ici (with id, score, height)0
        for w in range(width):
            for h in range(height):
                dp_list[h][w] = copy.deepcopy(dp_list[h][w - 1]) if w > 0 else [0, []]
                # This represents not adding the item in question
                for version in data_list[w]:
                    if version["height"] <= h:
                        # If first item
                        if w == 0:
                            score = version["score"]
                            if score > dp_list[h][w][0]:
                                dp_list[h][w][0] = score
                                dp_list[h][w][1] = [
                                    version["id"],
                                ]
                        # If not first item
                        else:
                            new_score = (
                                dp_list[h - version["height"]][w - 1][0]
                                + version["score"]
                            )
                            if new_score > dp_list[h][w][0]:
                                if dp_list[h - version["height"]][w - 1][1]:
                                    new_items_list = copy.deepcopy(
                                        dp_list[h - version["height"]][w - 1][1]
                                    )
                                    new_items_list.append(version["id"])
                                else:
                                    new_items_list = [
                                        version["id"],
                                    ]

                                dp_list[h][w][0] = new_score
                                dp_list[h][w][1] = new_items_list
        # ABOVE NOT TESTED, CAN BE VERY WRONG
        # Currently not building the swap algorithm, as DP should be decent for the job.
        # Will implement if need arises
        max_result = dp_list[height - 1][width - 1][1]
        result_len = len(self.sections)
        self.optimization_result = [[] for _ in range(result_len)]
        for ids in max_result:
            section_id = ids[0]
            self.optimization_result[section_id].append(ids)
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
                continue
            if not self.optimization_result[section.sect_id]:
                # Nothing from this section was selected; printing the heading
                # on its own would leave an empty block on the page.
                continue
            section_build = section.build(
                self.optimization_result[section.sect_id], self.template
            )
            # Result of seciton_build should be a 1d list
            self.section_build_results.extend(section_build)
        # Call the resume build function in the template
        return self.template.resume_builder(self)

    def to_dict(self) -> dict:
        """
        Compile the class into a dict for storage
        """
        result = {
            "aux_info": self.aux_info,
            "heading_info": {"heading_name": "", "subsequent_content": []},
            "sections": [section.to_dict() for section in self.sections],
        }
        if self.heading_name or self.heading_subsequent_content:
            result["heading_info"] = {
                "heading_name": self.heading_name,
                "subsequent_content": self.heading_subsequent_content,
            }
        return result

    def to_tailored_dict(self) -> dict:
        """
        Return the resume dict containing only the items and lines selected
        by the optimizer. Requires optimize() to have been called first.

        Each selected item is trimmed to only its top-k lines (where k is
        determined by the version_idx chosen by the optimizer).
        """
        if not self.optimization_result:
            return self.to_dict()

        result = {
            "aux_info": self.aux_info,
            "heading_info": {
                "heading_name": self.heading_name,
                "subsequent_content": self.heading_subsequent_content,
            },
            "sections": [],
        }

        for section in self.sections:
            selected_ids = self.optimization_result[section.sect_id]
            if not selected_ids:
                continue
            sect_dict = {
                "sect_id": section.sect_id,
                "aux_info": section.aux_info,
                "title": section.title,
                "items": [],
            }
            for ids in sorted(selected_ids, key=lambda x: x[1]):
                item_idx = ids[1]
                version_idx = ids[2]
                item = section.items[item_idx]
                num_lines = version_idx + 1
                top_lines = item.top_k_lines(item.line_objs, num_lines)
                sect_dict["items"].append({
                    "aux_info": item.aux_info,
                    "titles": item.titles if item.titles else [],
                    "lines": [line.to_dict() for line in top_lines],
                    "cate_scores": item.cate_scores,
                })
            result["sections"].append(sect_dict)

        return result
