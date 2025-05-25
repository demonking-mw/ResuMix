"""
Tests the lines class, mainly the score generator
"""

from ..resume_classes.lines import Lines

myline = Lines()

myline.content = "Developed a uav similation engine based on YOLO in python, and trained it to achieve an overall accuracy of 91%."
myline.content_str = r"Developed a uav similation engine based on YOLO in python, and trained it to achieve an overall accuracy of 91%."
myline.gen_score()
print(myline.to_dict())
