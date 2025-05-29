"""
Tests the lines class, mainly the score generator
"""

from ..resume_objects.lines import Line

myline = Line()

myline.content = "Developed a uav similation engine based on YOLO in python, and trained it to achieve an overall accuracy of 91%."
myline.content_str = r"Developed a uav similation engine based on YOLO in python, and trained it to achieve an overall accuracy of 91%."
myline.gen_score()
print(myline.to_dict())
print("Total token used: ", myline.total_tokens())
