"""
Tests the item class
So far only the to_latex
"""

from ..resume_objects.lines import Line
from ..resume_objects.items import Item

print("DEBUG: checkpoint0")

myline = Line()

myline.content = r"Developed a uav similation engine based on YOLO in python, and trained it to achieve an overall accuracy of 91%."
myline.content_str = "Developed a uav similation engine based on YOLO in python, and trained it to achieve an overall accuracy of 91%."
print("DEBUG: checkpoint1")
myitem = Item()
myitem.titles = ["Test", "have fun testing", "whatever", "some location"]
myitem.line_objs.append(myline)
result = myitem.make_specific()
print("DEBUG: checkpoint2")
print(result["object"].dumps())
