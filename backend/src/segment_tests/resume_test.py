from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
    ListFlowable, ListItem
)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.units import inch

doc = SimpleDocTemplate(
    "resume_recreated.pdf",
    pagesize=letter,
    rightMargin=40, leftMargin=40, topMargin=22, bottomMargin=22
)

styles = getSampleStyleSheet()

# Main body font size and leading
styles["Normal"].fontSize = 10
styles["Normal"].fontName = "Times-Roman"
styles["Normal"].leading = 11.5

styles.add(ParagraphStyle(
    name='ResumeTitle',
    fontSize=17, fontName='Times-Bold', alignment=TA_CENTER,
    leading=19, spaceBefore=0, spaceAfter=2, wordWrap='LTR'
))
styles.add(ParagraphStyle(
    name='Contact',
    fontSize=9, fontName='Times-Roman',
    alignment=TA_CENTER, leading=10.5, spaceAfter=9, spaceBefore=0, wordWrap='LTR'
))
styles.add(ParagraphStyle(
    name='Section',
    fontSize=11, leading=12.5, fontName='Times-Bold',
    alignment=TA_LEFT, spaceBefore=10, spaceAfter=0, allCaps=True, wordWrap='LTR',
    tracking=1
))
styles.add(ParagraphStyle(
    name='SubHeading',
    fontSize=10, leading=11, fontName='Times-Bold', alignment=TA_LEFT, wordWrap='LTR'
))
styles.add(ParagraphStyle(
    name='Meta',
    fontSize=9, fontName='Times-Italic', alignment=TA_RIGHT, leading=10.3
))
styles.add(ParagraphStyle(
    name='Small',
    fontSize=9, fontName='Times-Roman', leading=10
))
styles.add(ParagraphStyle(
    name='RoleItalic',
    fontSize=9.7, fontName='Times-Italic', leading=10.3
))
styles.add(ParagraphStyle(
    name='ListBullet',
    fontSize=9.8, fontName='Times-Roman', leftIndent=13,
    bulletIndent=5, spaceBefore=0.2, spaceAfter=0.2, leading=11.5
))
styles.add(ParagraphStyle(
    name='RightItal',
    fontSize=9, fontName='Times-Italic', alignment=TA_RIGHT, leading=10
))

def heading():
    name = "<b>ARAS GÜNGÖRE</b>"
    contact = (
        '📱 +90 531 420 4536 | ✉ arasgungore09@gmail.com | '
        '<b>LinkedIn</b> | <b>GitHub</b> | <b>Portfolio</b> | '
        '📍 Istanbul, Turkey'
    )
    return [
        Spacer(1, 0.1*inch),
        Paragraph(name, styles['ResumeTitle']),
        Paragraph(contact, styles['Contact'])
    ]

def section(title):
    return [
        Spacer(1, 0.07*inch),
        Paragraph(title.upper(), styles['Section']),
        HRFlowable(width="100%", thickness=0.7, lineCap='round', color='black', spaceBefore=1, spaceAfter=4)
    ]

def education_section():
    content = []
    content += section("Education")
    t = Table([
        [Paragraph("<b>Boğaziçi University</b>", styles['SubHeading']),
         Paragraph("Istanbul, Turkey", styles['Meta'])],
        [Paragraph('<i>B.Sc. in Electrical and Electronics Engineering;</i> <b>GPA: 3.62/4.00</b><br/>'
                   '<i>Minor Degree in Computer Science;</i> <b>GPA: 3.58/4.00</b>', styles['Normal']),
         Paragraph("Sep 2018 – Jun 2023<br/>Oct 2020 – Jun 2023", styles['RightItal'])]
    ], colWidths=[4.1 * inch, 2.1 * inch])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    content.append(t)
    content.append(
        Paragraph('<b>National University Admission Exam (YKS):</b> '
                  'Ranked 75<sup>th</sup> in Mathematics and Science among ca. 2.3 million candidates with a test score of 489.92/500. (Jul 2018)',
                  styles['Small']))
    return content

def skills_section():
    content = []
    content += section("Skills")
    content.append(Paragraph('<b>Languages:</b> C/C++, C#, Java, Python, Go, JavaScript, TypeScript, SQL, Swift, Scala, MATLAB, R', styles['Normal']))
    content.append(Paragraph('<b>Technologies:</b> Qt, Flask, Django, Node.js, React.js, MySQL, MongoDB, Git, SVN, Docker, AWS, Kubernetes, GCP, Kafka, RabbitMQ, OpenCV, PyTorch, TensorFlow', styles['Normal']))
    content.append(Paragraph('<b>Methodologies:</b> Agile, Scrum, OOP, Functional Programming, DevOps, CI/CD, TDD', styles['Normal']))
    return content

def experience_entry(title, role, right1, right2, highlights):
    tbl = Table([
        [Paragraph(f"<b>{title}</b>", styles['SubHeading']), Paragraph(right1, styles['Meta'])],
        [Paragraph(f"<i>{role}</i>", styles['RoleItalic']), Paragraph(right2, styles['Meta'])]
    ], colWidths=[2.8*inch, 3.6*inch])
    tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0)
    ]))
    return [
        tbl,
        ListFlowable(
            [ListItem(Paragraph(h, styles['ListBullet'])) for h in highlights],
            bulletType='bullet', leftPadding=17, bulletColor='black', bulletFontSize=7.5
        )
    ]

def experience_section():
    content = []
    content += section("Experience")
    # Avikon block
    content += experience_entry(
        "Avikon", "Avikon", "Monkey Island", "Istanbul, Turkey",
        [
            "Designed a Qt-based chat application utilizing TCP for real-time communication within a client-server architecture, demonstrating expertise in socket programming, data serialization, and message routing.",
            "Crafted message types in IDL and designed a data-centric publish-subscribe architecture based on a flyweight design pattern to implement OpenDDS for a radar system’s command and control interface. Utilized QoS policies to facilitate the transmission of both volatile and persistent data across different topics.",
            "Implemented a fully asynchronous AMQP-based C++ client with a layered architecture for RabbitMQ message broker to ensure seamless message handling among multiple topics.",
            "Developed a cross-platform asynchronous program to refine UAV detection for a GIS application. Benchmarked point-in-polygon algorithms with a GeoJSON polygon database concurrently fetched from MongoDB."
        ]
    )
    # Add more jobs following above format...
    return content

elements = []
elements += heading()
elements += education_section()
elements += skills_section()
elements += experience_section()

doc.build(elements)
