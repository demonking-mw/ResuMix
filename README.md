# WorkBringer2
A new resume optimizer that brings you closer to employment


MAJOR ASSUMPTIONS: 
EACH LINES IN AN ITEM IN A RESUME HAVE SIMILAR LENGTH


RULES:

Backend API reture rule:
- 'message' means a string
- 'detail' means a nested dict
- 'status' means a bool on the success of the action
    - Note: it conveys a different meaning than the code
    - It is possible that the action was not performed but no error was reached
- 'info' means data
- 'jwt' means a reauthentication jwt for quick auth next time.

Categories: Technical, Soft, Relevance, 

Definition of resumeinfo:
(here lstr means latex string)
resumeinfo -> sections -> items -> lines
    |           |           |        |- content: lstr
    |           |           |        |- cate_scores: dict
    |           |           |        |- content_str
    |           |           |        |          |- one dict per each category
    |           |           |        |- keywords: listof(str)
    |           |           |- Titles: listof(lstr)
    |           |           |- Category_weight: dict
    |           |           |- Category_bias: dict
    |           |           |- Aux_info: dict
    |           |- Title: lstr
    |           |- Type_info: dict
    |           |- Aux_info: dict
    |- Style_info: dict
    |- Category_scoring_functions: dict
    |- Aux_info: dict
Note: all contents should be in the form of latex code segments, so things like hyperlink is easy

Lines' cate_scores: a dict of dicts: {technical: {}, soft: {}}

aux_info: type: lines/items/sections, format: see documentation for different classes

EDIT: every class should have a aux_info class

Classes: ResumeInfo, Sections, Items, Lines
Note: they should store the user's full resume
Note: conversion between json and obj should be quick and ezez

Most major calculations should be done in the backend

Resume generate: use pylatex

Categories: technical, soft, relevant
CATEGORY NAME FOR ANY INTERMETHOD COMMUNICATION MUST BE AS IS

Processor: a dict storing instruction on how to process items
{values: {cate: {} ~...}, functions: {cate: funcn}}
values are AI generated for each value present in each category
function is for scoring a category of an item:
(weight: int, bias: int, products: listof listof int) -> (score: dict)




Variables:

Lines:
- content: lstr
    latex content in r'' format
- cate_score: dictof: str - dict
    each sub dictionary is str - int, which represents attribute and score
- content_str: str
    pure string of content, set by frontend when creating item
- self.keywords: listof str
- self.aux_info: AUX_INFO

Items:
- title: listof lstr
    can be different lengths, corresponding to different forms of resume
- line_objs: listof Lines
- cate_score: dictof: str - dict
    each sub dict contain 'weight' and 'bias', each assigned to a decimal
- aux_info: AUX_INFO
- paragraph: lstr
    Only used if type is p, stores the paragraph info
- style: str
    denotes the type of Item it is, stored in aux_info when folded into dict
    Options:
    - n2  - two headings, normal
    - n2l - two headings, all to the left
    - n3  - 3 headings, one line, middle one (to the left) for skills or alike
    - n4  - 4 headings, normal
    - n5  - 4 headings with a skill line in upper row, to the left
    - p   - ONE PARAGRAPH