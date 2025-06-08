'''
The class that parses the resume from file
Handlles building, optimizing, etc
'''

from .sections import Section
from ..general_helper.isa_bot import AIBot

class Resume:
    '''
    Recursively builds each section -> item -> line
    variables:
    - sections: list of Section objects
    - template: LTemplate
    - aux_info: dict with type as resume
    '''
    def __init__(self, template, class_dict=None):
        self.template = template
        self.sections = []
        self.aux_info = {"type": "resume"}
        self.section_make_results = []
        self.requirements = {}
        self.attribute_targets = {} # dict of cate -> list of attributes
        self.bot = AIBot()  # AI bot for generating scores
        if class_dict is not None:
            if class_dict["aux_info"]["type"] != "resume":
                raise ValueError(
                    f"Type mismatch: expected 'resume', got {class_dict['aux_info']['type']}"
                )
            self.aux_info = class_dict["aux_info"]
            self.sections = [
                Section(template, sect["sect_id"], sect) for sect in class_dict["sections"]
            ]
        else:
            self.aux_info = {"type": "resume"}

    def __pre_make(self) -> bool:
        '''
        Gget the list of attributes for gpt parsing
        DOES NOT assume that the resume is not empty
        Result:
        - Modifies self.attribute_targets
        - Returns True if the next step should be done, False otherwise
        '''
        if not self.sections or not self.template:
            print("DEBUG: No sections or template found , EMPTY RESUME, cannot make")
            return False

        # Get the attributes for gpt parsing
        full_attributes = {
            "technical": [],
            "soft": [],
            "relevance": []
        }
        for section in self.sections:
            section_skills = section.get_skills_dict()
            for cate, _ in full_attributes.items():
                full_attributes[cate].extend(section_skills[cate])
                full_attributes[cate] = list(set(full_attributes[cate]))
        return True

    def make(self, job_req: str) -> bool:
        '''
        Make the resume build ready
        Using AI, generate the requirement
        Then make each section
        Result:
        - Calls __pre_make()
        - Makes requirement dict, update self.requirements
        - Calls make() for each section, stores the item_core_info in self.section_make_results
        - Returns True if successful, False otherwise
        '''
        if not self.__pre_make():
            return False

        # Generate the requirements dictionary
        reminder = (
            "Remember, your answer MUST be ONLY a python dictionary, "
            "as it will be parsed by a program\n"
            'Note that you must cover every attribute in the attributes dictionary I provided,\n'
        )
        job_prompt = (
            'The following is a job description for a position: '
            + job_req
        )
        instruction = (
            'Generate me a python dictionary reflecting '
            'how much each of these attributes matters for the job '
            'and how much showcasing them in the resume will help the candidate land the job.\n'
            'Here are the attributes you need to consider, '
            'they are divided into categories, note that soft means soft skills, '
            'and relevance contains passions/interest '
            'that the person might showcase in the resume.\n'
            f'Attributes: {self.template.attribute_targets}\n'
        )
        response_spec = (
            'Your response should be a python dictionary with the following structure:\n'
            '{\n'
            '    "technical": {"attribute_name": score, ...},\n'
            '    "soft": {"attribute_name": score, ...},\n'
            '    "relevance": {"attribute_name": score, ...}\n'
            '}\n'
            'Where score is an integer from 0 to 5, representing '
            'how important the attribute is for the job.\n'
            'Scoring standard:\n'
            '0: Not relevant/important at all\n'
            '1: remotely relevant or tangible, can draw vague '
            'connection to the job and the companys interest\n'
            '2: relevant to the industry that the job is in, '
            'but not closely related to the jobs content\n'
            '3~5: relevant to the job requirements, '
            'with 5 being a direct mention of equivalent skills in the job description or '
            'that the skill is required for the jobs responsibilities.\n'
        )
        prompt = (
            job_prompt + instruction + response_spec + reminder
        )
        prompt_instruction = (
            "When you are asked a question, first analyze it, then output ONLY a python "
            "dictionary that contains the answer. Sample output "
            "(NEGLECT THE CONTENT OF THE DICT BELOW, only look at how it is formatted):\n"
            '{\n'
            '    "technical": {"python": 4, "java": 1},\n'
            '    "soft": {"self_regulation": 3},\n'
            '    "relevance": {"cars": 4, "music": 0}\n'
            '}\n'
            "Note: the dictionary should contain keys of type string and values of type int. "
            "Do not output anything else. Also, whenever giving something a score, make it out of 3"
        )
        requirements_dict = self.bot.pythoned_response_instruction(
            prompt,
            prompt_instruction,
            datatype=dict,
            model=self.template.model,
            token_limit=2000,
            retries=3,
            temperature=0.1
        )
        if not requirements_dict:
            print("DEBUG: Failed to get requirements from AI")
            return False
        self.requirements = requirements_dict

        # Make each section using self.requirements
        for section in self.sections:
            item_core_info = section.make(self.requirements)
            if item_core_info is None:
                print(f"DEBUG: Failed to make section {section.sect_id}")
                return False
            self.section_make_results.append(item_core_info)
        print("DEBUG: ready for optimization")
        return True
