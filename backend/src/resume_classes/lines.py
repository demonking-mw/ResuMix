import re

'''
The Lines Class

This class is used to represent a line in a resume.
It contains the information stored about the line, and related functions to parse it.
'''

class Lines:
    '''
    Functions needed:
    - gen_score: have AI cook
    - adj_score: adjust score by general input in learning phase
    - gen_keyword: generate keywords with AI
    - strip: generate the string only content for stuff such as gpt
    Variables needed:
    - contents: lstr
    - content_str: str
    - sect_score (possibly, for gpt parsing): dict
    - keywords: listof(str)
    '''

    def __init__(self, class_dict: dict) -> None:
        '''
        Takes the info from storage to build the class
        OR create an empty class if info is None
        '''
        self.content = r""         # content is latex code segment
        self.cate_score = {}       # dict of str: int
        # This stands for category score
        self.content_str = ""      # content_str is pure string
        self.keywords = []         # list of pure strings
        # getter and setters are not needed
        if class_dict is not None:
            if "aux_info" not in class_dict:
                raise ValueError("Missing 'aux_info', should not happen in prod")
            if 'type' not in class_dict['aux_info'] or class_dict['aux_info']['type'] != 'lines':
                raise ValueError("Invalid input: 'type' must be 'lines'")
            # At this point, info is a Lines class
            self.content = class_dict['content'] if 'content' in class_dict else r""
            self.cate_score = (
                class_dict['cate_score']
                if 'cate_score' in class_dict
                else {}
            )
            self.content_str = class_dict['content_str'] if 'content_str' in class_dict else ""
            self.keywords = class_dict['keywords'] if 'keywords' in class_dict else []


    def content_flatten(self) -> None:
        '''
        Modifies self.content_str
        '''
        # Remove LaTeX commands and extract plain text
        # Handle hyperlinks: extract the second argument if present, otherwise the first
        self.content = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', self.content)
        self.content_str = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', self.content)
        self.content_str = re.sub(r'\\[a-zA-Z]+\s*', '', self.content_str)
        self.content_str = re.sub(r'\{([^}]*)\}', r'\1', self.content_str)
        self.content_str = re.sub(r'\s+', ' ', self.content_str).strip()
        # This should be useless if the frontend works as expected

    def gen_score(self, adj_factor: float = 1.0, forced: bool = False) -> bool:
        '''
        Generate a set of scores for this line
        WILL OVERWRITE EXISTING
        Effect: modify self.cate_score
        '''
        if self.cate_score is not None and not forced:
            return False
        # NOT IMPLEMENTED YET
        return True
    