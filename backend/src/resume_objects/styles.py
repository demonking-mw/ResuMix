"""
A class that stores all custom fonts
"""

from dataclasses import dataclass
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from . import style_info


@dataclass
class ResumeStyle:
    """
    A dataclass that strores resume style info
    """

    font_lib: dict[str, style_info.StyleInfo]
    default_section_style: style_info.SectionAttributes
    # section_att_lib: dict[str, style_info.StyleInfo]
    resume_style: dict


resume_style_0 = ResumeStyle(
    font_lib={
        # This is for the section title
        "section_title_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="section_title_font",
                font_name="Helvetica-Bold",
                font_size=13,
                text_color_hex="#000000",
                alignment=0,
                space_before=1,
                space_after=0,
                leading=13,
                left_indent=40,
            )
        ),
        "subtitle_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="subtitle_font",
                font_name="Times-Bold",
                font_size=12,
                text_color_hex="#000000",
                alignment=0,
                space_before=5,
                space_after=0,
                leading=0,
                left_indent=10,
            )
        ),
        "subright_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="subright_font",
                font_name="Times-Bold",
                font_size=12,
                text_color_hex="#000000",
                alignment=2,
                space_before=0,
                space_after=0,
                leading=14,
            )
        ),
        # for middle, only font_name and font_size should be used
        "submiddle_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="submiddle_font",
                font_name="Times-Roman",
                font_size=11,
                text_color_hex="#000000",
                alignment=2,
                space_before=0,
                space_after=0,
                leading=16,
                left_indent=0,
            )
        ),
        # 2 means the second title column in 4/5 heading scenarios
        "subtitle2_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="subtitle2_font",
                font_name="Times-Bold",
                font_size=12,
                text_color_hex="#000000",
                alignment=0,
                space_before=5,
                space_after=0,
                leading=0,
                left_indent=10,
            )
        ),
        "subright2_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="subright2_font",
                font_name="Times-Bold",
                font_size=12,
                text_color_hex="#000000",
                alignment=2,
                space_before=0,
                space_after=0,
                leading=16,
            )
        ),
        "standard_text_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="standard_text_font",
                font_name="Times-Roman",
                font_size=11,
                text_color_hex="#000000",
                alignment=0,
                space_before=0,
                space_after=0,
                leading=14,
                left_indent=30,
            )
        ),
        "resume_heading_name_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="name_font",
                font_name="Helvetica-Bold",
                font_size=16,
                text_color_hex="#000000",
                alignment=1,
                space_before=5,
                space_after=0,
                leading=25,
            )
        ),
        "resume_heading_desc_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="personal_info_font",
                font_name="Helvetica",
                font_size=11,
                text_color_hex="#000000",
                alignment=1,
                space_before=0,
                space_after=0,
                leading=15,
            )
        ),
        "point_left_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="point_left",
                font_name="Times-Roman",
                font_size=11,
                text_color_hex="#000000",
                alignment=0,
                space_before=0,
                space_after=0,
                leading=0,
            )
        ),
        "point_right_font": style_info.StyleInfo(
            font_attributes=style_info.FontAttributes(
                name="point_right",
                font_name="Times-Roman",
                font_size=11,
                text_color_hex="#000000",
                alignment=0,
                space_before=0,
                space_after=0,
                leading=14,
                left_indent=A4[0] / 2,
            )
        ),
    },
    # Change: here side_margin represents the left side margin for content, title is separate
    default_section_style=style_info.SectionAttributes(
        height_buffer=3,
        wrap_forgive=5,
        bullet_symbol="• ",
    ),
    resume_style={
        "left_margin": 15,
        "right_margin": 15,
        "top_margin": 5,
        "bottom_margin": 5,
        "split_line_width": "97%",
        "split_line_thickness": 1,
        "split_line_space_before": 2,
        "split_line_space_after": 6,
    },
    # section_style_lib={
    #     "default": style_info.SectionAttributes(
    #         side_margin=20,
    #         title_side_margin=20,
    #         top_margin=5,
    #         height_buffer=3,
    #         wrap_forgive=5,
    #         bullet_symbol="• ",
    #         paper_width=A4[0],
    #     ),
    #     "heading": style_info.SectionAttributes(
    #         side_margin=20,
    #         title_side_margin=20,
    #         top_margin=20,
    #         height_buffer=3,
    #         wrap_forgive=5,
    #         bullet_symbol="• ",
    #         paper_width=A4[0],
    #     ),
    # },
    # section_att_lib={
    #     "HEADING": style_info.StyleInfo(
    #         section_attributes=style_info.SectionAttributes(
    #             side_margin=20,
    #             title_side_margin=20,
    #             top_margin=5,
    #             height_buffer=10,
    #             wrap_forgive=20,
    #             paper_width=A4[0],
    #         ),
    #         subStyleInfo=None  # You can set this to the font_lib dict if needed
    #     ),
    #     "SKILLS": style_info.StyleInfo(
    #         section_attributes=style_info.SectionAttributes(
    #             side_margin=20,
    #             title_side_margin=20,
    #             top_margin=5,
    #             height_buffer=3,
    #             wrap_forgive=5,
    #             bullet_symbol="• ",
    #             paper_width=A4[0],
    #         ),
    #         subStyleInfo=None
    #     ),
    #     "EDUCATION": style_info.StyleInfo(
    #         section_attributes=style_info.SectionAttributes(
    #             side_margin=20,
    #             title_side_margin=20,
    #             top_margin=5,
    #             height_buffer=10,
    #             wrap_forgive=20,
    #             paper_width=A4[0],
    #         ),
    #         subStyleInfo=None
    #     ),
    #     "EXPERIENCE": style_info.StyleInfo(
    #         section_attributes=style_info.SectionAttributes(
    #             side_margin=20,
    #             title_side_margin=20,
    #             top_margin=5,
    #             height_buffer=3,
    #             wrap_forgive=5,
    #             bullet_symbol="• ",
    #             paper_width=A4[0],
    #         ),
    #         subStyleInfo=None
    #     ),
    #     "PROJECTS": style_info.StyleInfo(
    #         section_attributes=style_info.SectionAttributes(
    #             side_margin=20,
    #             title_side_margin=20,
    #             top_margin=5,
    #             height_buffer=3,
    #             wrap_forgive=5,
    #             bullet_symbol="• ",
    #             paper_width=A4[0],
    #         ),
    #         subStyleInfo=None
    #     ),
    # },
    # resume_style is the style for the whole resume
    # more specifically, it's for universal settings that needs no variants
)


class AllFonts:
    """
    Stores all font info
    """

    resume_title = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Bold",
        fontSize=14,
        textColor=colors.black,
        alignment=1,
        spaceAfter=0,
        leading=12,
    )
    #
    section_title = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Bold",
        fontSize=14,
        textColor=colors.black,
        alignment=1,
        spaceAfter=0,
        leading=15,
    )
    subsection_title = ParagraphStyle(
        name="SubTitleFont",
        fontName="Times-Bold",
        fontSize=13,
        textColor=colors.black,
        spaceBefore=8,
        alignment=0,
        spaceAfter=0,
        leading=0,
    )
    subright_title = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Bold",
        fontSize=13,
        textColor=colors.black,
        alignment=2,
        spaceAfter=0,
        leading=18,
    )
    text_font_standard_sec = ParagraphStyle(
        name="paraFont",
        fontName="Times-Roman",
        fontSize=11,
        textColor=colors.black,
        alignment=0,
        spaceAfter=0,
        leading=16,
    )
    name_font = ParagraphStyle(
        name="nameFont",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=colors.black,
        alignment=1,
        spaceAfter=3,
        leading=18,
    )

    personal_info_font = ParagraphStyle(
        name="personalInfoFont",
        fontName="Times-Bold",
        fontSize=12,
        textColor=colors.black,
        alignment=1,
        spaceAfter=0,
        leading=15,
    )
    point_left = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Roman",
        fontSize=11,
        textColor=colors.black,
        spaceBefore=0,
        alignment=0,
        spaceAfter=0,
        leading=0,
    )
    point_right = ParagraphStyle(
        name="SectTitleFont",
        fontName="Times-Roman",
        fontSize=11,
        textColor=colors.black,
        leftIndent=A4[0] / 2,
        alignment=0,
        spaceAfter=0,
        leading=14,
    )

    def __init__(self) -> None:
        print("fonts init")
