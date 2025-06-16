"""
dataclass to store latex templates for resumes
Note: it also contains two functions to calculate the height of an item
    and the remaining height of a doc.
Note: template is now for reportlab, latex might be added later
"""

import io

from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetric import stringWidth
from reportlab.platypus import Paragraph, HRFlowable, Frame
from reportlab.lib.pagesizes import A4

from .styles import ResumeStyle
from .resume import Resume


class LTemplate:
    """
    A class to represent a Reportlab template for resumes.
    Contains:
    - preamble: latex code that needs to be inserted at the top of the doc
    - item_height_calculator: function taking in an item and returning its height
        - I/O: (item: Item) -> int
    - remaining_height_calculator:
            function taking in the number of sections and return the total height allowed
        - I/O: (sections: int) -> int
            - Note: section count should exclude static sections
    - item_builder:
            function taking in a list of headings and a list of items, builds the Reportlab paragraphs
        - I/O: (headings: list, items: listof lstr) -> listof Paragraphs
    - section_builder:
            function taking in a title and a list of Item builds, builds a big list of Paragraphs and shinanigans
        - Note: the divider and the title are handled by this function
        - I/O: (title: str, items: listof Paragraph) -> listof Paragraph
    """


    def __init__(self, resume_style: ResumeStyle) -> None:
        '''
        Init the class, set resume style
        This will only need to be done once when creating the resume class
        '''
        self.style_sheet = resume_style

    def remaining_height_calculator(self, sections: int) -> int:
        '''
        calculates the allocatable height for the resume
        ignore the heading, which is fixed height
        also ignore space taken for heading of each section
        sections: the number of sections in the resume other than the haeding
        ASSUMES: each section are styled like 'default' in terms of spacing
        POTENTIAL BUG: if assumption not hold, some content might not show up
        returns: the height of the resume in points
        '''
        if sections <= 0:
            raise ValueError("Sections count must be non-negative")
        # Calculate the dead height per section
        default_sect_style = self.style_sheet.section_style_lib['default']
        # default MUST exist in any resume style

        # Here sect_style top margin is moved to resume_style for consistency
        # Only consider to maintain height_buffer for failsafe
        dead_height_per_section = (
            default_sect_style.height_buffer
            + self.style_sheet.font_lib['section_title_font'].space_before
            + self.style_sheet.font_lib['section_title_font'].leading
            + self.style_sheet.resume_style['split_line_space_before']
            + self.style_sheet.resume_style['split_line_after']
            + self.style_sheet.resume_style['split_line_height']
        )
        header_style = self.style_sheet.section_style_lib['header']
        header_height = (
            header_style.top_margin
            + self.style_sheet.font_lib['resume_heading_name_font'].space_before
            + self.style_sheet.font_lib['resume_heading_name_font'].leading
            + self.style_sheet.font_lib['resume_heading_desc_font'].space_before
            + self.style_sheet.font_lib['resume_heading_desc_font'].leading
        )
        rem_height = (
            int(A4[1])
            - self.style_sheet.resume_style['top_margin']
            - self.style_sheet.resume_style['bottom_margin']
            - header_height
            - sections * dead_height_per_section
        )
        return rem_height


    def item_height_calculator(self, item: 'Item') -> int:
        """
        Function to calculate the height of an item.
        Uses info from default_section
        Deprecate the use of section_style, move to having left_indent for paragraphs
        :param item: An instance of Item.
        :return: Height of the item in some unit (e.g., points).
        """
        total_height = 0
        titles = item.titles
        line_width = (
            A4[0]
            - self.style_sheet.default_section_attributes.wrap_forgive
        )
        # wrap_forgive will be deprecated once proven useless

        if len(titles) == 0:
            raise ValueError("Item must have at least one title")
        # Adding the item title height
        total_height += self.style_sheet.font_lib["subtitle_font"].space_before
        total_height += self.style_sheet.font_lib["subright_font"].leading
        if len(titles) > 3:
            # Assume 2 rows since 3 rows is basically never used
            total_height += self.style_sheet.font_lib["subtitle2_font"].space_before
            total_height += self.style_sheet.font_lib["subright2_font"].leading
        for line in item.line_objs:
            line_rstring = line.content
            line_style = self.style_sheet.font_lib['standard_text_font'].get_paragraph_style()
            line_para = Paragraph('- ' + line_rstring, line_style)
            _, line_height = line_para.wrap(line_width, 694200)
            total_height += line_height
        return total_height

    def item_builder(self, headings: list, content: list = None, item_type: str = 'n', bullet_point: bool = True, section_style_name: str = 'default') -> list:
        '''
        builds the item in the form of a list of Paragraph class(es)
        CONTENT IS ALLOWED TO BE NONE!!
        handles different heading lengths
        acceptable heading length: 1~6, with anything higher than 3 being two rows
        note: consider extending when adding

        item_type allowed:
        - n: normally styled
        - l: everything to the left (handy for project one-liner)
        - p: paragraph
            - Acceptable in either heading list or content list, prioritize heading
            - Only read one if in heading list, anything else is neglected
            - multiple can be read if in content list
                - useful for skills section perhaps
            - the paragraph will be styled with standard_text_font

        RETURN: a list of Paragraphs
        '''
        if not headings and not content:
            raise ValueError("Headings list must not be empty")
        if item_type == 'n':
            # Normal resume build:
            section_content = []
            head_len = len(headings)
            # here number represents paragraph number. looks like:
            # 1   2
            # 3   4
            para1 = None
            para2 = None
            para3 = None
            para4 = None
            if head_len == 1 or head_len == 2 or head_len == 4:
                # First item without augmentation
                para1 = headings[0]
                if head_len > 1:
                    # For length 2 or 4
                    para2 = headings[1]
                if head_len == 4:
                    para3 = headings[2]
                    para4 = headings[3]

            if head_len == 3 or head_len == 5 or head_len == 6:
                # First item with augmentation
                first_str = headings[0]
                subsequent_size = self.style_sheet.font_lib['subtitle_middle'].font_size
                subsequent_font = self.style_sheet.font_lib['subtitle_middle'].font_name
                styled_subsequent = (
                    f'<font name="{subsequent_font}" size="{subsequent_size}">'
                    f'{headings[2]}</font>'
                )
                para1 = first_str + styled_subsequent
                para2 = headings[2] # here no augmentation needed
                if head_len == 5:
                    para3 = headings[3]
                    para4 = headings[4]
                if head_len == 6:
                    # Here augmentation is needed again
                    # Shares the same styling for the first middle segment
                    #   since this should be rare enough
                    second_first_str = headings[3]
                    styled_subsequent2 = (
                        f'<font name="{subsequent_font}" size="{subsequent_size}">'
                        f'{headings[4]}</font>'
                    )
                    para3 = second_first_str + styled_subsequent2
                    para4 = headings[5]
            if para1:
                section_content.append(
                    Paragraph(
                        para1,
                        self.style_sheet.font_lib['subtitle_font'].get_paragraph_style()
                    )
                )
            if para2:
                section_content.append(
                    Paragraph(
                        para2,
                        self.style_sheet.font_lib['subright_font'].get_paragraph_style()
                    )
                )
            if para3:
                section_content.append(
                    Paragraph(
                        para3,
                        self.style_sheet.font_lib['subtitle2_font'].get_paragraph_style()
                    )
                )
            if para4:
                section_content.append(
                    Paragraph(
                        para4,
                        self.style_sheet.font_lib['subright2_font'].get_paragraph_style()
                    )
                )
        elif item_type == 'l':
            raise ValueError("Left-aligned items are not supported yet")
        elif item_type == 'p':
            if headings:
                # It has at least one line, use it
                section_content.append(
                    Paragraph(
                        headings[0],
                        self.style_sheet.font_lib['standard_text_font'].get_paragraph_style()
                    )
                )
                # Avoid adding any other content
                # since paragraph is meant for one content
                return section_content

        # building the content
        item_content = r""
        for line in content:
            line_result = r''
            if bullet_point:
                # Allowed use of section_style
                bullet_style = self.style_sheet.section_style_lib.get(
                    section_style_name,
                    self.style_sheet.section_style_lib['default']
                )
                line_result += bullet_style.bullet_symbol
            line_result += line
            item_content += line_result + r'\n'
        item_content = item_content.strip()
        if item_content:
            section_content.append(
                Paragraph(
                    item_content,
                    self.style_sheet.font_lib['standard_text_font'].get_paragraph_style()
                )
            )
        return section_content

    def section_builder(self, title: str, items: list) -> list:
        '''
        builds the section in the form of a list of items.
        styling:
        - prioritize section_style_type
        - then try to search with title
        - then use default section style
        '''
        # sect_style_lib was removed due to redundancy
        # Create the actual section
        section_content = []
        # Add the section title and the bar line
        section_content.append(
            Paragraph(
                title,
                self.style_sheet.font_lib['section_title_font'].get_paragraph_style()
            )
        )
        # Add that damn line
        section_content.append(
            HRFlowable(
                width=self.style_sheet.resume_style['split_line_width'],
                thickness=self.style_sheet.resume_style['split_line_thickness'],
                spaceBefore=self.style_sheet.resume_style['split_line_space_before'],
                spaceAfter= self.style_sheet.resume_style['split_line_space_after'],
            )
        )
        for item_build in items:
            section_content.extend(item_build)
            # DEPRECIATING SECTION STYLE
            # indentation is styled with the font
        return section_content

    def resume_builder(self, resume_object: Resume) -> bytes:
        '''
        Makes the resume, then hand it back as bytes
        Using section_build_results: listof(Paragraph() or equivalent reportlab items)
        '''
        main_content = resume_object.section_build_results
        # All the content in the middle

        # Buffer to return resume instead of saving
        buffer = io.BytesIO()

        # Preping canvas
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setLineWidth(self.style_sheet.resume_style['split_line_thickness'])

        margin_l = self.style_sheet.resume_style['left_margin']
        margin_r = self.style_sheet.resume_style['right_margin']
        margin_t = self.style_sheet.resume_style['top_margin']
        margin_b = self.style_sheet.resume_style['bottom_margin']

        master_frame = Frame(
            margin_l,
            margin_b,
            A4[0] - margin_l - margin_r,
            A4[1] - margin_t - margin_b
        )

        full_content_list = []
        # It's a 1d list, build directly
        title_para = Paragraph(
            resume_object.heading_name,
            self.style_sheet.font_lib['resume_heading_name_font'].get_paragraph_style()
        )
        # In this template, join the heading subsequent list
        subsequent_text = " | ".join(resume_object.heading_subsequent_content)
        sub_para = Paragraph(
            subsequent_text,
            self.style_sheet.font_lib['resume_heading_desc_font'].get_paragraph_style()
        )
        full_content_list.append(title_para)
        full_content_list.append(sub_para)

        # build the rest
        if not main_content:
            print("No content to render in the resume.")
        full_content_list.extend(main_content)

        # add list to frame, save, and extract the bytes
        master_frame.addFromList(full_content_list, c)
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

