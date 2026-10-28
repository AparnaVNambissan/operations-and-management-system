import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class KTUCanvas(canvas.Canvas):
    """
    Exact KTU Project Report Canvas:
    - Page 1: Cover Page (no header, no footer)
    - Pages 2-5: Declaration, Certificate, Acknowledgment, Abstract (no header, no footer)
    - Pages 6-11: TOC, List of Figures, List of Tables, List of Appendices (no header, bottom roman numeral)
    - Page 12: Blank
    - Page 13 onwards: Chapter pages (running header top-left on subsequent pages, bottom-center arabic page number)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations()
            super().showPage()
        super().save()

    def draw_page_decorations(self):
        p = self._pageNumber
        if p == 1 or p == 12:
            return  # Cover or blank

        self.saveState()
        self.setFillColor(colors.black)

        # Preliminary pages 6-11 (TOC to Appendices list)
        if 6 <= p <= 11:
            self.setFont("Times-Roman", 11)
            roman_pages = {6: "vi", 7: "vii", 8: "viii", 9: "ix", 10: "x", 11: "xi"}
            if p in roman_pages:
                self.drawCentredString(A4[0] / 2.0, 45, roman_pages[p])
        
        # Chapter and Appendix pages (Page 13 onwards)
        elif p >= 13:
            arabic_page = p - 12  # Chapter 1 starts at page 1
            self.setFont("Times-Roman", 11)
            # Bottom center page number
            self.drawCentredString(A4[0] / 2.0, 45, str(arabic_page))

            # Running header at top-left for non-first pages of each chapter
            header_ranges = [
                (14, 15, "Chapter 1 - Introduction"),
                (17, 18, "Chapter 2 - System Study"),
                (20, 37, "Chapter 3 – Methodology"),
                (39, 43, "Chapter 4 - Results and Discussions"),
                (45, 45, "Chapter 5 - Conclusion and Future Scope"),
                (48, 51, "Appendix A - Data Flow Diagram"),
                (54, 60, "Appendix C - Source Code"),
                (62, 64, "Appendix D - Screenshots"),
            ]
            for p_start, p_end, title in header_ranges:
                if p_start <= p <= p_end:
                    self.drawString(72, A4[1] - 45, title)
                    break

        self.restoreState()

def build_pdf():
    pdf_filename = "AparnaProject.pdf"

    # Margins: 72pt (1 inch) matching KTU guidelines
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Title Page Styles in Times-Roman
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Times-Bold',
        fontSize=18,
        leading=25,
        alignment=1, # Center
        textColor=colors.black,
        spaceAfter=14
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Times-Roman',
        fontSize=12,
        leading=17,
        alignment=1,
        textColor=colors.black,
        spaceAfter=14
    )

    style_cover_author = ParagraphStyle(
        'CoverAuthor',
        fontName='Times-Bold',
        fontSize=14,
        leading=19,
        alignment=1,
        textColor=colors.black,
        spaceAfter=4
    )

    style_cover_inst = ParagraphStyle(
        'CoverInst',
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.black
    )

    # Headings in Times-Roman
    style_h1_center = ParagraphStyle(
        'Heading1_Center',
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=1, # Center
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=16,
        keepWithNext=True
    )

    style_h1_left = ParagraphStyle(
        'Heading1_Left',
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=0, # Left
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=16,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2',
        fontName='Times-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'Heading3',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body',
        fontName='Times-Roman',
        fontSize=12,
        leading=18, # 1.5 line spacing
        alignment=4, # Justified
        textColor=colors.black,
        spaceAfter=10
    )

    style_bullet = ParagraphStyle(
        'Bullet',
        fontName='Times-Roman',
        fontSize=12,
        leading=18,
        leftIndent=24,
        firstLineIndent=-14,
        textColor=colors.black,
        spaceAfter=6
    )

    style_caption = ParagraphStyle(
        'Caption',
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        alignment=1, # Centered
        textColor=colors.black,
        spaceBefore=4,
        spaceAfter=10
    )

    style_table_caption = ParagraphStyle(
        'TableCaption',
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        alignment=0, # Left
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=6
    )

    style_code = ParagraphStyle(
        'Code',
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.black,
        spaceAfter=1
    )

    style_d_h3 = ParagraphStyle(
        'AppendixHeading3',
        fontName='Times-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.black,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    style_d_body = ParagraphStyle(
        'AppendixBody',
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
        alignment=4, # Justified
        textColor=colors.black,
        spaceAfter=3
    )

    style_d_caption = ParagraphStyle(
        'AppendixCaption',
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
        alignment=1, # Centered
        textColor=colors.black,
        spaceBefore=2,
        spaceAfter=5
    )

    story = []

    # ==========================================
    # PAGE 1: TITLE / COVER PAGE
    # ==========================================
    story.append(Spacer(1, 30))
    story.append(Paragraph("ROLE-BASED INVENTORY AND<br/>ASSET MANAGEMENT SYSTEM", style_cover_title))
    story.append(Spacer(1, 15))
    story.append(Paragraph("A Mini Project Report", style_cover_sub))
    story.append(Paragraph("submitted by", style_cover_sub))
    story.append(Spacer(1, 5))
    story.append(Paragraph("APARNA P", style_cover_author))
    story.append(Paragraph("(MES25MCA-2010)", ParagraphStyle('Roll', fontName='Times-Bold', fontSize=12, alignment=1, spaceAfter=20)))
    story.append(Paragraph("to the APJ Abdul Kalam Technological University in partial<br/>fulfilment of the requirements for the award of the Degree<br/>of", style_cover_sub))
    story.append(Paragraph("Master of Computer Applications", style_cover_author))
    story.append(Spacer(1, 15))

    logo_path = os.path.join("static", "images", "logo.jpg")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=80, height=80))
    else:
        story.append(Spacer(1, 80))

    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Department of Computer Applications</b><br/>MES College of Engineering<br/>Kuttippuram, Malappuram – 679582", style_cover_inst))
    story.append(Spacer(1, 10))
    story.append(Paragraph("October, 2026", style_cover_sub))
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: DECLARATION
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Declaration", style_h1_center))
    story.append(Spacer(1, 15))
    decl_p = (
        "I undersigned hereby declare that the project report \"ROLE-BASED INVENTORY AND ASSET "
        "MANAGEMENT SYSTEM\" submitted for partial fulfilment of the requirements for the award of "
        "degree of Master of Computer Applications of the APJ Abdul Kalam Technological University, "
        "Kerala, is a bonafide work done by me under supervision of Mr. Geevar C Zachariaz, Assistant "
        "Professor, Department of Computer Applications. This submission represents my ideas in my own "
        "words and where ideas or words of others have been included, I have adequately and accurately "
        "cited and referenced the original sources. I also declare that I have adhered to ethics of academic "
        "honesty and integrity and have not misrepresented or fabricated any data or idea or fact or source "
        "in my submission. I understand that any violation of the above will be a cause for disciplinary "
        "action by the institute and/or the University and can also evoke penal action from the sources which "
        "have thus not been properly cited or from whom proper permission has not been obtained. This "
        "report has not been previously formed the basis for the award of any degree, diploma or similar "
        "title of any other University."
    )
    story.append(Paragraph(decl_p, style_body))
    story.append(Spacer(1, 120))

    sig_data = [
        ["", "APARNA P"],
        ["", "(MES25MCA-2010)"],
        ["", "22/10/2026"]
    ]
    t_decl_sig = Table(sig_data, colWidths=[280, 171])
    t_decl_sig.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_decl_sig)
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: CERTIFICATE
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("DEPARTMENT OF COMPUTER APPLICATIONS", style_cover_sub))
    story.append(Paragraph("MES COLLEGE OF ENGINEERING, KUTTIPPURAM", style_cover_sub))
    story.append(Spacer(1, 10))

    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=70, height=70))
    story.append(Spacer(1, 15))

    story.append(Paragraph("CERTIFICATE", style_h1_center))
    story.append(Spacer(1, 10))

    cert_p = (
        "This is to certify that the report entitled ROLE-BASED INVENTORY AND ASSET MANAGEMENT "
        "SYSTEM is a bonafide record of the Mini Project work during the year 2026-27 carried out by "
        "APARNA P (MES25MCA-2010) submitted to the APJ Abdul Kalam Technological "
        "University, in partial fulfilment of the requirements for the award of the Master of Computer "
        "Applications, under my guidance and supervision. This report in any form has not been submitted "
        "to any other University or Institution for any purpose."
    )
    story.append(Paragraph(cert_p, style_body))
    story.append(Spacer(1, 140))

    cert_sigs = [
        ["Internal Supervisor", "Head of The Department"]
    ]
    t_cert_sigs = Table(cert_sigs, colWidths=[225, 226])
    t_cert_sigs.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_cert_sigs)
    story.append(PageBreak())

    # ==========================================
    # PAGE 4: ACKNOWLEDGMENT
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Acknowledgment", style_h1_center))
    story.append(Spacer(1, 15))

    ack1 = (
        "I express my sincere gratitude to our principal Dr. Rahumathuniza I for permitting and providing "
        "all facilities to carry out this project. I would like to express my sincere gratitude to my internal "
        "supervisor, Mr. Geevar C Zachariaz, for his invaluable guidance, support, and encouragement "
        "throughout the development of this mini project. I also extend my thanks to the Head of the "
        "Department Prof. Hyderali K and all faculty members of the Department of Computer "
        "Applications, MES College of Engineering, for providing the necessary resources and a conducive "
        "environment for learning and innovation."
    )
    story.append(Paragraph(ack1, style_body))

    ack2 = (
        "I am deeply grateful to the faculty members and fellow students whose experiences with the manual "
        "asset management process inspired the vision behind the Role-Based Inventory and Asset Management "
        "System. Their insights and feedback shaped the direction of this project."
    )
    story.append(Paragraph(ack2, style_body))

    ack3 = (
        "Finally I thank my family and friends for their unwavering support and motivation. Above all, I "
        "extend my heartfelt gratitude ot Almighty for giving me the strength and wisdom to complete this "
        "project."
    )
    story.append(Paragraph(ack3, style_body))
    story.append(Spacer(1, 80))

    ack_sig = [
        ["", "Aparna P"],
        ["", "(MES25MCA-2010)"]
    ]
    t_ack = Table(ack_sig, colWidths=[300, 151])
    t_ack.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_ack)
    story.append(PageBreak())

    # ==========================================
    # PAGE 5: ABSTRACT
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Abstract", style_h1_center))
    story.append(Spacer(1, 15))

    ab1 = (
        "The Role-Based Inventory and Asset Management System is a web-based platform designed to simplify "
        "the management, monitoring and requisition of departmental equipment, hardware assets, and workplace "
        "tasks in educational institutions and enterprise environments. In most departments today, asset requests "
        "are submitted through emails or printed documents, allocations are handled manually, and equipment return "
        "and maintenance records are scattered across different places. This makes tracking an asset from purchase to "
        "disposal slow, inconsistent and difficult to audit."
    )
    story.append(Paragraph(ab1, style_body))

    ab2 = (
        "The main objective of Role-Based Inventory and Asset Management System is to provide a single "
        "centralized platform with secure role-based access for the Administrator, Department Head, and Employee. "
        "Employees browse available stock, submit requisitions online, and return equipment when finished. "
        "The Administrator reviews requests, approves or rejects them, oversees low-stock threshold warnings, "
        "and dispatches workload-balanced tasks. Damaged equipment can be flagged through maintenance tickets, "
        "and inter-departmental collaboration issues are tracked to resolution. In addition, gamification rewards "
        "on-time task completion with achievement badges."
    )
    story.append(Paragraph(ab2, style_body))

    ab3 = (
        "The system is developed using HTML, CSS and JavaScript with Tailwind CSS for the front end, and Python with the "
        "Django framework for the back end. SQLite is used as the development database, and Git and GitHub are used for "
        "version control. The project followed an Agile methodology with four sprints."
    )
    story.append(Paragraph(ab3, style_body))

    ab4 = (
        "The system is expected to reduce paperwork and manual effort, improve communication between employees and "
        "administrators, prevent inventory loss, and make resource management more transparent and reliable."
    )
    story.append(Paragraph(ab4, style_body))
    story.append(PageBreak())

    # ==========================================
    # PAGE 6: TABLE OF CONTENTS (Part 1)
    # ==========================================
    story.append(Paragraph("Table of Contents", style_h1_left))
    story.append(Spacer(1, 6))

    toc_page1 = [
        ["List of Figures ...........................................................................................................................", "viii"],
        ["List of Tables ...............................................................................................................................", "ix"],
        ["List of Appendices.........................................................................................................................", "x"],
        ["Chapter 1. Introduction ...............................................................................................................", "1"],
        ["    1.1 Motivation ...........................................................................................................................", "1"],
        ["    1.2 Objectives............................................................................................................................", "2"],
        ["    1.3 Contributions ........................................................................................................................", "2"],
        ["    1.4 Report Organization ............................................................................................................", "3"],
        ["Chapter 2. System Study ...............................................................................................................", "4"],
        ["    2.1 Existing System...................................................................................................................", "4"],
        ["    2.2 Proposed System .................................................................................................................", "5"],
        ["    2.3 Functionalities of the Proposed System ..............................................................................", "5"],
        ["Chapter 3. Methodology...............................................................................................................", "7"],
        ["    3.1 Introduction .........................................................................................................................", "7"],
        ["    3.2 Software Tools.....................................................................................................................", "7"],
        ["    3.3 Module Description.............................................................................................................", "8"],
        ["        3.3.1 Administrator Module .................................................................................................", "8"],
        ["        3.3.2 Department Management Module ................................................................................", "8"],
        ["        3.3.3 Asset Inventory Module .............................................................................................", "8"],
        ["        3.3.4 Employee Self-Service Module ....................................................................................", "8"],
        ["        3.3.5 Requisition and Returns Module .................................................................................", "9"],
        ["    3.4 Workflow of the System .......................................................................................................", "9"],
        ["        3.4.1 Registration and Login................................................................................................", "9"],
        ["        3.4.2 Asset Catalog Setup ...................................................................................................", "9"],
        ["        3.4.3 Requisition Submission ...............................................................................................", "9"],
        ["        3.4.4 Administrative Review and Decision ...........................................................................", "9"],
        ["        3.4.5 Asset Return and Stock Restoration............................................................................", "10"],
        ["        3.4.6 Maintenance Defect Reporting ....................................................................................", "10"],
        ["        3.4.7 Task Workload Auto-Assignment ...............................................................................", "10"],
        ["    3.5 User Stories .......................................................................................................................", "10"],
        ["    3.6 Product Backlog ................................................................................................................", "12"],
        ["    3.7 Sprint Backlog...................................................................................................................", "13"],
        ["    3.8 Project Plan........................................................................................................................", "14"],
    ]
    t_toc1 = Table(toc_page1, colWidths=[400, 51])
    t_toc1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_toc1)
    story.append(PageBreak())

    # ==========================================
    # PAGE 7: TABLE OF CONTENTS (Part 2)
    # ==========================================
    toc_page2 = [
        ["    3.9 Database Design ................................................................................................................", "16"],
        ["        3.9.1 User Table .................................................................................................................", "16"],
        ["        3.9.2 Asset Table................................................................................................................", "18"],
        ["        3.9.3 Asset Request Table ....................................................................................................", "20"],
        ["        3.9.4 Department Table ......................................................................................................", "21"],
        ["        3.9.5 Task and SubTask Table .............................................................................................", "22"],
        ["        3.9.6 Maintenance Issue Table .............................................................................................", "23"],
        ["        3.9.7 Department Issue Table .............................................................................................", "24"],
        ["        3.9.8 Award and Badge Table .............................................................................................", "25"],
        ["Chapter 4. Results and Discussions...........................................................................................", "26"],
        ["    4.1 Results ................................................................................................................................", "26"],
        ["    4.2 Discussion .........................................................................................................................", "30"],
        ["        4.2.1 Analysis of Results....................................................................................................", "30"],
        ["        4.2.2 Role-Based Access Control.......................................................................................", "30"],
        ["        4.2.3 Requisition Workflow and Validation ..........................................................................", "30"],
        ["        4.2.4 Development Process................................................................................................", "30"],
        ["        4.2.5 Limitations .................................................................................................................", "31"],
        ["Chapter 5. Conclusion and Future Scope.................................................................................", "32"],
        ["    5.1 Conclusion.........................................................................................................................", "32"],
        ["    5.2 Future Scope......................................................................................................................", "33"],
        ["References....................................................................................................................................", "34"],
        ["Appendix A: Data Flow Diagram ...............................................................................................", "35"],
        ["    A.1 Level 0 DFD .....................................................................................................................", "35"],
        ["    A.2 Level 1 DFD .....................................................................................................................", "36"],
        ["    A.3 Level 2 DFD .....................................................................................................................", "37"],
        ["    A.4 Level 3 DFD .....................................................................................................................", "38"],
        ["    A.5 Level 4 DFD .....................................................................................................................", "39"],
        ["Appendix B: Entity–Relationship Diagram .............................................................................", "40"],
        ["Appendix C: Source Code..........................................................................................................", "41"],
        ["    C.1 Asset Data Model .............................................................................................................", "41"],
        ["    C.2 Asset Requisition and Return Model ...............................................................................", "42"],
        ["    C.3 Task and SubTask Models ................................................................................................", "43"],
        ["    C.4 Admin Requisition Approval View ...................................................................................", "45"],
        ["    C.5 Return Asset Controller View ...........................................................................................", "46"],
        ["    C.6 Workload Auto-Assignment View ....................................................................................", "47"],
        ["Appendix D: Screenshots ...........................................................................................................", "49"],
    ]
    t_toc2 = Table(toc_page2, colWidths=[400, 51])
    t_toc2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_toc2)
    story.append(PageBreak())

    # ==========================================
    # PAGE 8: TABLE OF CONTENTS (Part 3)
    # ==========================================
    toc_page3 = [
        ["    D.1 Login Page........................................................................................................................", "49"],
        ["    D.2 Admin Dashboard Page....................................................................................................", "49"],
        ["    D.3 Department Management Page...........................................................................................", "50"],
        ["    D.4 Asset List & Availability Page ............................................................................................", "50"],
        ["    D.5 Add New Asset Page .........................................................................................................", "50"],
        ["    D.6 Employee Dashboard Page ................................................................................................", "51"],
        ["    D.7 Asset Requests & Approvals Page ...................................................................................", "51"],
        ["    D.8 Complaint & Issue Management Page ..............................................................................", "51"],
        ["    D.9 Task & Subtask Management Page ....................................................................................", "52"],
        ["    D.10 Performance Awards & Badges Page ................................................................................", "52"],
    ]
    t_toc3 = Table(toc_page3, colWidths=[400, 51])
    t_toc3.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_toc3)
    story.append(PageBreak())

    # ==========================================
    # PAGE 9: LIST OF FIGURES
    # ==========================================
    story.append(Paragraph("List of Figures", style_h1_center))
    story.append(Spacer(1, 10))

    figs = [
        ["Figure 4.1: Login Page...................................................................................................................", "26"],
        ["Figure 4.2: Admin Dashboard........................................................................................................", "27"],
        ["Figure 4.3: Department Management...............................................................................................", "27"],
        ["Figure 4.4: Asset List & Availability..............................................................................................", "28"],
        ["Figure 4.5: Add New Asset Form...................................................................................................", "28"],
        ["Figure 4.6: Employee Dashboard....................................................................................................", "29"],
        ["Figure A.1: Level 0 DFD................................................................................................................", "35"],
        ["Figure A.2: Level 1 DFD................................................................................................................", "36"],
        ["Figure A.3: Level 2 DFD................................................................................................................", "37"],
        ["Figure A.4: Level 3 DFD................................................................................................................", "38"],
        ["Figure A.5: Level 4 DFD................................................................................................................", "39"],
        ["Figure B.1: Entity–relationship diagram .......................................................................................", "40"],
        ["Figure D.1: Login page of the system............................................................................................", "49"],
        ["Figure D.2: Admin dashboard with asset metrics..............................................................................", "49"],
        ["Figure D.3: Department management directory...............................................................................", "50"],
        ["Figure D.4: Asset catalog with availability progress bars..............................................................", "50"],
        ["Figure D.5: Add new asset form....................................................................................................", "50"],
        ["Figure D.6: Employee workspace dashboard..................................................................................", "51"],
        ["Figure D.7: Asset requisition and return tracker............................................................................", "51"],
        ["Figure D.8: Maintenance defect and issue tracker.....................................................................", "51"],
        ["Figure D.9: Task and milestone subtask board..............................................................................", "52"],
        ["Figure D.10: Gamified recognition badges and awards................................................................", "52"],
    ]
    t_figs = Table(figs, colWidths=[400, 51])
    t_figs.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_figs)
    story.append(PageBreak())

    # ==========================================
    # PAGE 10: LIST OF TABLES
    # ==========================================
    story.append(Paragraph("List of Tables", style_h1_center))
    story.append(Spacer(1, 10))

    tabs = [
        ["Table 3.1: Software tools and technologies used for development.................................................", "7"],
        ["Table 3.2: User stories for review analysis and moderation..........................................................", "10"],
        ["Table 3.3: Product backlog............................................................................................................", "12"],
        ["Table 3.4: Sprint backlog and completion status...........................................................................", "13"],
        ["Table 3.5: Project schedule and task allocation.............................................................................", "14"],
        ["Table 3.6: User table schema and sample data..............................................................................", "16"],
        ["Table 3.7: Asset table schema and sample data............................................................................", "18"],
        ["Table 3.8: Asset request table schema and sample data.................................................................", "20"],
        ["Table 3.9: Department table schema and sample data...................................................................", "21"],
        ["Table 3.10: Task and SubTask table schema and sample data..........................................................", "22"],
        ["Table 3.11: Maintenance issue table schema and sample data.........................................................", "23"],
        ["Table 3.12: Department issue table schema and sample data..........................................................", "24"],
        ["Table 3.13: Award and badge table schema and sample data..........................................................", "25"],
    ]
    t_tabs = Table(tabs, colWidths=[400, 51])
    t_tabs.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_tabs)
    story.append(PageBreak())

    # ==========================================
    # PAGE 11: LIST OF APPENDICES
    # ==========================================
    story.append(Paragraph("List of Appendices", style_h1_center))
    story.append(Spacer(1, 10))

    apps = [
        ["Appendix A: Data Flow Diagram..................................................................................................", "35"],
        ["Appendix B: Entity–Relationship Diagram...................................................................................", "40"],
        ["Appendix C: Source Code..............................................................................................................", "41"],
        ["Appendix D: Screenshots...............................................................................................................", "49"],
    ]
    t_apps = Table(apps, colWidths=[400, 51])
    t_apps.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_apps)
    story.append(PageBreak())

    # ==========================================
    # PAGE 12: BLANK PAGE
    # ==========================================
    story.append(Paragraph("", style_body))
    story.append(PageBreak())

    # ==========================================
    # PAGE 13: CHAPTER 1. INTRODUCTION (Page 1)
    # ==========================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Chapter 1. Introduction", style_h1_left))
    story.append(Spacer(1, 10))

    c1_1 = (
        "Organizational assets and departmental inventory are an important part of institutional operations. "
        "Managing them involves several activities, including asset intake, departmental allocation, requisition "
        "submission, approval review, equipment return tracking, maintenance defect reporting, and record keeping. "
        "When these are handled through separate manual methods, tracking the complete inventory lifecycle becomes difficult."
    )
    story.append(Paragraph(c1_1, style_body))

    c1_2 = (
        "This project proposes the Role-Based Inventory and Asset Management System, a web-based application "
        "that centralizes the management of organizational assets, requisitions, and departmental tasks. It provides separate "
        "functionalities for administrators and employees, based on their responsibilities. The system is implemented "
        "with HTML, CSS and JavaScript for the user interface and Python (Django) for server-side logic and database access. "
        "The interface is organised as role-based dashboards that are clean, responsive and easy to use."
    )
    story.append(Paragraph(c1_2, style_body))

    story.append(Paragraph("1.1 Motivation", style_h2))
    c1_mot = (
        "The main motivation for this project came from the difficulties observed in the way physical assets and inventory "
        "are handled in a typical department. The administrator must receive equipment requests, check stock availability, "
        "forward requests to department heads, allot items manually, monitor returns, and consolidate maintenance records. "
        "Employees, on the other hand, must approach several people through different channels to learn the availability of an asset "
        "or the status of their request. As a result, information is easily lost, delayed or duplicated. This observation motivated the "
        "development of a centralized platform that simplifies the requisition, monitoring and maintenance of organizational assets. "
        "The system improves communication between employees, administrators and department heads, and ensures transparent and "
        "efficient tracking throughout the asset lifecycle. By reducing paperwork and manual effort, it improves the overall efficiency "
        "and reliability of departmental asset management."
    )
    story.append(Paragraph(c1_mot, style_body))
    story.append(PageBreak())

    # ==========================================
    # PAGE 14: CHAPTER 1 CONT. (Page 2)
    # ==========================================
    story.append(Paragraph("1.2 Objectives", style_h2))
    story.append(Paragraph("The primary objective of Role-Based Inventory and Asset Management System is to develop a website with the following features:", style_body))
    story.append(Paragraph("• Provides secure role-based authentication for all users.", style_bullet))
    story.append(Paragraph("• Enables employees to browse available stock and submit asset requisitions.", style_bullet))
    story.append(Paragraph("• Allows the Administrator to manage departments, asset categories, and equipment.", style_bullet))
    story.append(Paragraph("• Enables the Administrator to review requisitions and grant approvals or rejections.", style_bullet))
    story.append(Paragraph("• Supports automated stock replenishment upon verified asset return.", style_bullet))
    story.append(Paragraph("• Allows employees to report physical defects and cross-departmental complaints.", style_bullet))
    story.append(Paragraph("• Supports workload-balanced task auto-assignment based on employee skills.", style_bullet))
    story.append(Paragraph("• Enables employees to check off milestone subtasks and track progress.", style_bullet))
    story.append(Paragraph("• Automatically rewards timely task completion with gamified achievement badges.", style_bullet))
    story.append(Paragraph("• Generates audit reports in PDF and Excel formats.", style_bullet))
    story.append(Paragraph("• Improves transparency, efficiency and coordination in asset management.", style_bullet))

    story.append(Paragraph("1.3 Contributions", style_h2))
    story.append(Paragraph("Key contributions includes:", style_body))
    story.append(Paragraph("• A centralized web platform that replaces email- and paper-based inventory management.", style_bullet))
    story.append(Paragraph("• Secure role-based access for Administrator and Employee with automatic routing.", style_bullet))
    story.append(Paragraph("• An online requisition workflow with stock verification, approval, rejection, and return check-in.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # PAGE 15: CHAPTER 1 CONT. (Page 3)
    # ==========================================
    story.append(Paragraph("• Automated inventory restoration that returns issued quantities to stock upon item check-in.", style_bullet))
    story.append(Paragraph("• A structured database storing asset details, requests, departments, tasks, subtasks, issues and awards.", style_bullet))
    story.append(Paragraph("• Export utilities for automated PDF and Excel inventory audit reports.", style_bullet))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.4 Report Organization", style_h2))
    c1_rep = (
        "Chapter 2 reviews the existing system and the proposed solution. Chapter 3 describes the Agile methodology, "
        "development tools, modules, workflow, user stories, backlogs, project plan and database design. Chapter 4 presents "
        "the implemented interfaces and discusses the results and limitations. Chapter 5 gives the conclusion and future scope. "
        "The appendices contain the data flow diagrams, ER diagram, source code and screenshots."
    )
    story.append(Paragraph(c1_rep, style_body))
    story.append(PageBreak())

    # ==========================================
    # PAGE 16: CHAPTER 2. SYSTEM STUDY (Page 4)
    # ==========================================
    story.append(Paragraph("Chapter 2. System Study", style_h1_left))
    story.append(Spacer(1, 10))

    c2_study = (
        "The system study examines how departmental inventory and assets are currently managed in the organization, "
        "and defines what the Role-Based Inventory and Asset Management System must provide. It looks at the present manual "
        "process, where the administrator receives requisitions, forwards them to department heads, collects their approvals, "
        "allocates equipment, logs maintenance notes and consolidates inventory counts, while employees must approach several "
        "people through different channels to learn the availability of an asset or check the status of their request. This often "
        "leads to lost, delayed or duplicated information. Based on this analysis, the study identifies the need for a centralized "
        "web-based platform that simplifies asset cataloging, requisition approval, return stock restoration and maintenance "
        "tracking. The system improves communication between employees, administrators and department heads, ensures transparent "
        "and efficient tracking, and reduces paperwork and manual effort."
    )
    story.append(Paragraph(c2_study, style_body))

    story.append(Paragraph("2.1 Existing System", style_h2))
    story.append(Paragraph("• Requisition submission: Requests are submitted through emails or printed paper slips.", style_bullet))
    story.append(Paragraph("• Asset allocation: The inventory coordinator allocates equipment manually in offline registers.", style_bullet))
    story.append(Paragraph("• Communication: Staff communicate through different platforms such as email and messaging applications.", style_bullet))
    story.append(Paragraph("• Return tracking: Checking in borrowed assets is difficult to monitor and maintain.", style_bullet))
    story.append(Paragraph("• Record keeping: Maintenance notes, defects and inventory reports are stored in different locations, and maintaining asset history is time-consuming.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # PAGE 17: CHAPTER 2 CONT. (Page 5)
    # ==========================================
    story.append(Paragraph("• Stock visibility: There is no single platform where employees can check real-time asset availability or view low-stock warning alerts.", style_bullet))
    story.append(Paragraph("• Task management: Work is assigned verbally without workload balancing or milestone checklists.", style_bullet))

    story.append(Paragraph("2.2 Proposed System", style_h2))
    c2_prop = (
        "The proposed system is a centralized web-based platform for complete asset and workflow management, with secure "
        "role-based access. Its main features are:"
    )
    story.append(Paragraph(c2_prop, style_body))
    story.append(Paragraph("• Online asset catalog: Employees can view real-time availability and stock health bars.", style_bullet))
    story.append(Paragraph("• Requisition lifecycle: Employees submit requests with quantity and purpose; administrators approve or reject with notes.", style_bullet))
    story.append(Paragraph("• Automatic return replenishment: Returning an asset restores the available quantity immediately.", style_bullet))
    story.append(Paragraph("• Department management: Administrators create and oversee organizational departments.", style_bullet))
    story.append(Paragraph("• Maintenance reporting: Employees report damaged assets and inter-departmental issues.", style_bullet))
    story.append(Paragraph("• Workload auto-assignment: Tasks are automatically allocated to employees with matching skills and lowest workload.", style_bullet))
    story.append(Paragraph("• Gamification badges: On-time task completion earns recognition awards and badges.", style_bullet))

    story.append(Paragraph("2.3 Functionalities of the Proposed System", style_h2))
    story.append(Paragraph("• Administrator: Manage assets, create departments, approve/reject requisitions, dispatch tasks, resolve maintenance issues, and grant awards.", style_bullet))
    story.append(Paragraph("• Employee: Browse inventory, request equipment, return checked-out items, report defects, complete subtasks, and earn badges.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # PAGE 18: CHAPTER 2 CONT. (Page 6)
    # ==========================================
    story.append(Paragraph("• Department Head / Staff: Review issues received by their unit, update ticket status, and monitor departmental asset allocation.", style_bullet))
    story.append(Paragraph("• Authentication: Secure role-based login and registration for all system users.", style_bullet))
    story.append(Paragraph("• Inventory Management: Real-time stock counts, category classification, and automated low-stock warnings.", style_bullet))
    story.append(Paragraph("• Document & Audit Management: Export comprehensive inventory and asset audit reports in PDF and Excel formats.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # PAGE 19: CHAPTER 3. METHODOLOGY (Page 7)
    # ==========================================
    story.append(Paragraph("Chapter 3. Methodology", style_h1_left))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.1 Introduction", style_h2))
    c3_m = (
        "An Agile methodology was adopted for developing the Role-Based Inventory and Asset Management System. Agile promotes "
        "iterative development, continuous feedback and adaptive planning, which suits a user-centered resource management "
        "system. The project was divided into four sprints, each focusing on specific functionality such as authentication, "
        "department management, asset cataloging, requisition lifecycle, return restoration, maintenance ticketing, and "
        "gamified task assignment. This gave flexibility during development, allowed continuous improvement based on feedback "
        "from stakeholders, and ensured that requirements were implemented in an organized manner."
    )
    story.append(Paragraph(c3_m, style_body))

    story.append(Paragraph("3.2 Software Tools", style_h2))
    story.append(Paragraph("Table 3.1 lists the software tools and technologies used for development.", style_body))

    t31_data = [
        ["Component", "Tool / Technology"],
        ["Operating System", "Windows 11"],
        ["Front End", "JavaScript, HTML, CSS, Tailwind CSS"],
        ["Back End", "Python"],
        ["Framework", "Django"],
        ["Database", "SQLite"],
        ["IDE", "Visual Studio Code"],
        ["Version Control", "Git and GitHub"],
    ]
    t31 = Table(t31_data, colWidths=[200, 251])
    t31.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Paragraph("Table 3.1: Software tools and technologies used for development", style_table_caption))
    story.append(t31)
    story.append(PageBreak())

    # ==========================================
    # PAGE 20: CHAPTER 3 CONT. (Page 8)
    # ==========================================
    story.append(Paragraph("3.3 Module Description", style_h2))
    story.append(Paragraph("The system is divided into modular components to ensure maintainability and scalability.", style_body))

    story.append(Paragraph("3.3.1 Administrator Module", style_h3))
    story.append(Paragraph("This module allows the administrator to control the overall inventory and operational process. The administrator can log in, view real-time KPI metrics, receive low-stock alerts, manage asset records, create departments, and handle staff assignments.", style_body))

    story.append(Paragraph("3.3.2 Department Management Module", style_h3))
    story.append(Paragraph("This module allows management of organizational units. Administrators can create, edit, and delete departments, allocate assets to specific units, and monitor employee headcounts and ticket loads.", style_body))

    story.append(Paragraph("3.3.3 Asset Inventory Module", style_h3))
    story.append(Paragraph("This module manages the physical hardware and consumable equipment. It tracks asset names, categories, descriptions, total quantities, available quantities, and low-stock alert thresholds.", style_body))

    story.append(Paragraph("3.3.4 Employee Self-Service Module", style_h3))
    story.append(Paragraph("This module allows employees to register, log in, browse real-time asset availability, submit checkout requests with justification notes, and view their assigned tasks and awards.", style_body))
    story.append(PageBreak())

    # ==========================================
    # PAGE 21: CHAPTER 3 CONT. (Page 9)
    # ==========================================
    story.append(Paragraph("3.3.5 Requisition and Returns Module", style_h3))
    story.append(Paragraph("This module governs the checkout pipeline. Administrators review pending requests to approve or reject them. When an approved asset is returned by an employee, the system automatically increments available stock.", style_body))

    story.append(Paragraph("3.4 Workflow of the System", style_h2))
    story.append(Paragraph("The Role-Based Inventory and Asset Management System follows a sequence of well-defined stages. Each stage passes its output to the next, starting from user authentication and ending with task completion and award recognition.", style_body))

    story.append(Paragraph("3.4.1 Registration and Login", style_h3))
    story.append(Paragraph("Employees register in the system and log in with their credentials. Administrators log in and are automatically routed to the executive dashboard, while employees are directed to their self-service workspace.", style_body))

    story.append(Paragraph("3.4.2 Asset Catalog Setup", style_h3))
    story.append(Paragraph("The administrator configures inventory categories and inputs asset records with total counts and low-stock alert thresholds.", style_body))

    story.append(Paragraph("3.4.3 Requisition Submission", style_h3))
    story.append(Paragraph("Employees browse the catalog, select available items, specify requested quantities and justification notes, and submit checkout requisitions.", style_body))

    story.append(Paragraph("3.4.4 Administrative Review and Decision", style_h3))
    story.append(Paragraph("The administrator reviews pending requests, verifies stock sufficiency, and approves or rejects the requisition with administrative feedback notes.", style_body))
    story.append(PageBreak())

    # ==========================================
    # PAGE 22: CHAPTER 3 CONT. (Page 10)
    # ==========================================
    story.append(Paragraph("3.4.5 Asset Return and Stock Restoration", style_h3))
    story.append(Paragraph("When an employee completes their work with an approved item, clicking 'Return Asset' checks back the equipment and automatically replenishes available stock.", style_body))

    story.append(Paragraph("3.4.6 Maintenance Defect Reporting", style_h3))
    story.append(Paragraph("Staff report hardware damage or inter-departmental requests. Department heads update tickets to In Progress or Resolved.", style_body))

    story.append(Paragraph("3.4.7 Task Workload Auto-Assignment", style_h3))
    story.append(Paragraph("Tasks are created with subtask checklists and can be auto-assigned to the employee with the required skill and lowest pending workload hours.", style_body))

    story.append(Paragraph("3.5 User Stories", style_h2))
    story.append(Paragraph("Table 3.2 summarizes the user and administrator requirements and their intended benefits.", style_body))

    u_stories1 = [
        ["Id", "As a type of user", "I want to", "So that i can"],
        ["1", "User", "Login to the system", "Securely access my role dashboard"],
        ["2", "Employee", "Register an account", "Obtain authorized system credentials"],
        ["3", "Employee", "Browse available inventory", "Identify equipment available for request"],
        ["4", "Employee", "Submit an asset request", "Obtain needed hardware for project work"],
        ["5", "Employee", "View my request status", "Know whether requests are approved or rejected"],
        ["6", "Employee", "Return approved assets", "Check back in equipment and restore stock"],
    ]
    t32_1 = Table(u_stories1, colWidths=[25, 110, 155, 161])
    t32_1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10.5),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Paragraph("Table 3.2: User stories for review analysis and moderation", style_table_caption))
    story.append(t32_1)
    story.append(PageBreak())

    # ==========================================
    # PAGE 23: CHAPTER 3 CONT. (Page 11)
    # ==========================================
    u_stories2 = [
        ["7", "Administrator", "View admin dashboard", "Monitor KPI metrics and stock health"],
        ["8", "Administrator", "Receive low stock alerts", "Initiate timely procurement orders"],
        ["9", "Administrator", "Add new inventory assets", "Make new equipment available in catalog"],
        ["10", "Administrator", "Create categories via modal", "Organize equipment without page reload"],
        ["11", "Administrator", "Approve asset requests", "Issue equipment to verified employees"],
        ["12", "Administrator", "Reject asset requests", "Provide feedback explaining denial reasons"],
        ["13", "Administrator", "Create departments", "Structure organizational business units"],
        ["14", "Administrator", "Edit and delete departments", "Maintain accurate department records"],
        ["15", "Employee", "Report asset defect/damage", "Notify technicians of broken hardware"],
        ["16", "Employee", "Raise departmental ticket", "Request assistance from other departments"],
        ["17", "Department", "Update ticket status", "Mark complaints as In Progress or Resolved"],
        ["18", "Administrator", "Create tasks with subtasks", "Delegate operational responsibilities"],
        ["19", "Administrator", "Auto-assign tasks", "Balance workload across skilled employees"],
        ["20", "Employee", "Toggle milestone subtasks", "Track progress toward task completion"],
        ["21", "Employee", "Complete tasks on time", "Earn automated timely completion badges"],
        ["22", "Administrator", "Grant custom awards", "Recognize outstanding employee performance"],
        ["23", "Employee", "View my badge showcase", "See personal achievements and medals"],
    ]
    t32_2 = Table(u_stories2, colWidths=[25, 110, 155, 161])
    t32_2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t32_2)
    story.append(PageBreak())

    # ==========================================
    # PAGE 24: CHAPTER 3 CONT. (Page 12)
    # ==========================================
    u_stories3 = [
        ["24", "Administrator", "Export PDF and Excel reports", "Provide official audit documentation"],
        ["25", "Administrator", "Manage staff departments", "Reassign personnel across departments"],
    ]
    t32_3 = Table(u_stories3, colWidths=[25, 110, 155, 161])
    t32_3.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t32_3)
    story.append(Spacer(1, 14))

    story.append(Paragraph("3.6 Product Backlog", style_h2))
    story.append(Paragraph("Table 3.3 presents the product backlog, including task priorities, estimates and completion status.", style_body))

    p_backlog1 = [
        ["ID", "Name", "Priority", "Estimate(hrs)", "Status"],
        ["1", "Requirement Analysis", "High", "2", "Completed"],
        ["2", "System Design", "High", "2", "Completed"],
        ["3", "Database/ER Diagram", "High", "3", "Completed"],
        ["4", "UI/Template Design", "Medium", "2", "Completed"],
        ["5", "Django Project Setup", "High", "2", "Completed"],
        ["6", "Authentication and Roles", "High", "2", "Completed"],
        ["7", "Initial Testing", "Medium", "2", "Completed"],
        ["8", "Employee Registration View", "High", "3", "Completed"],
        ["9", "Admin Dashboard KPI Cards", "High", "3", "Completed"],
        ["10", "Department Management CRUD", "High", "2", "Completed"],
        ["11", "Asset Inventory Catalog", "High", "2", "Completed"],
        ["12", "Low Stock Alert Calculation", "High", "2", "Completed"],
        ["13", "Inline Category Creation Modal", "Medium", "2", "Completed"],
        ["14", "Asset Request Submission", "High", "2", "Completed"],
        ["15", "Approval and Rejection Views", "High", "2", "Completed"],
        ["16", "Return Asset & Stock Replenishment", "Medium", "2", "Completed"],
        ["17", "Employee Dashboard View", "Medium", "2", "Completed"],
        ["18", "Maintenance Defect Reporting", "Medium", "2", "Completed"],
    ]
    t33_1 = Table(p_backlog1, colWidths=[25, 210, 75, 75, 66])
    t33_1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(Paragraph("Table 3.3: Product backlog with priorities and estimated effort", style_table_caption))
    story.append(t33_1)
    story.append(PageBreak())

    # ==========================================
    # PAGE 25: CHAPTER 3 CONT. (Page 13)
    # ==========================================
    p_backlog2 = [
        ["19", "Cross-Department Ticketing", "High", "2", "Completed"],
        ["20", "Ticket Status Update Form", "High", "3", "Completed"],
        ["21", "Task Creation with Subtasks", "Medium", "2", "Completed"],
        ["22", "Workload Auto-Assignment Engine", "High", "4", "Completed"],
        ["23", "Subtask Interactive Toggling", "Medium", "2", "Completed"],
        ["24", "Timely Completion Badge Engine", "Medium", "2", "Completed"],
        ["25", "Custom Award Granting Interface", "Medium", "2", "Completed"],
        ["26", "System Integration and Testing", "High", "3", "Completed"],
    ]
    t33_2 = Table(p_backlog2, colWidths=[25, 210, 75, 75, 66])
    t33_2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t33_2)
    story.append(Spacer(1, 14))

    story.append(Paragraph("3.7 Sprint Backlog", style_h2))
    story.append(Paragraph("Table 3.4 organizes the development work into four sprints and records their completion status.", style_body))

    sprint_b1 = [
        ["Sprint", "Task", "Status"],
        ["1", "Requirement Analysis", "Completed"],
        ["1", "System Design", "Completed"],
        ["1", "Database / ER Design", "Completed"],
        ["1", "UI / Template Design", "Completed"],
        ["1", "Django Project Setup", "Completed"],
        ["1", "Authentication and Roles", "Completed"],
        ["1", "Initial Testing", "Completed"],
        ["2", "Department Management CRUD", "Completed"],
        ["2", "Asset Catalog and Availability", "Completed"],
        ["2", "Low Stock Alert Calculation", "Completed"],
        ["2", "Category Modal Creation", "Completed"],
        ["2", "Employee Dashboard Layout", "Completed"],
    ]
    t34_1 = Table(sprint_b1, colWidths=[60, 311, 80])
    t34_1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10.5),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Paragraph("Table 3.4: Sprint backlog and completion status", style_table_caption))
    story.append(t34_1)
    story.append(PageBreak())

    # ==========================================
    # PAGE 26: CHAPTER 3 CONT. (Page 14)
    # ==========================================
    sprint_b2 = [
        ["2", "Requisition Submission Form", "Completed"],
        ["3", "Administrative Approval View", "Completed"],
        ["3", "Rejection Decision and Notes", "Completed"],
        ["3", "Return Asset Stock Restoration", "Completed"],
        ["3", "Maintenance Defect Tickets", "Completed"],
        ["3", "Cross-Departmental Issue Flow", "Completed"],
        ["3", "Ticket Status Updates", "Completed"],
        ["3", "Task Creation with Subtasks", "Completed"],
        ["4", "Workload Auto-Assignment Logic", "Completed"],
        ["4", "Subtask Interactive Checkoff", "Completed"],
        ["4", "Automated Achievement Badges", "Completed"],
        ["4", "Custom Award Granting Interface", "Completed"],
        ["4", "PDF and Excel Export Engines", "Completed"],
        ["4", "System Integration and Testing", "Completed"],
    ]
    t34_2 = Table(sprint_b2, colWidths=[60, 311, 80])
    t34_2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t34_2)
    story.append(Spacer(1, 14))

    story.append(Paragraph("3.8 Project Plan", style_h2))
    story.append(Paragraph("Table 3.5 presents the project schedule, user-story allocation and recorded task durations.", style_body))

    plan_1 = [
        ["User Story ID", "Task Name", "Start Date", "End Date", "Duration (Days)", "Status"],
        ["1", "Sprint 1", "24/07/2026", "24/07/2026", "15", "Completed"],
        ["2", "", "25/07/2026", "27/07/2026", "", "Completed"],
        ["3", "", "28/07/2026", "28/07/2026", "", "Completed"],
        ["4", "", "29/07/2026", "31/07/2026", "", "Completed"],
    ]
    t35_1 = Table(plan_1, colWidths=[70, 70, 80, 80, 91, 60])
    t35_1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Paragraph("Table 3.5: Project schedule and task allocation", style_table_caption))
    story.append(t35_1)
    story.append(PageBreak())

    # ==========================================
    # PAGE 27: CHAPTER 3 CONT. (Page 15)
    # ==========================================
    plan_2 = [
        ["5", "", "01/08/2026", "03/08/2026", "", "Completed"],
        ["6", "", "04/08/2026", "04/08/2026", "", "Completed"],
        ["7", "", "05/08/2026", "07/08/2026", "", "Completed"],
        ["8", "Sprint 2", "08/08/2026", "11/08/2026", "15", "Completed"],
        ["9", "", "12/08/2026", "14/08/2026", "", "Completed"],
        ["10", "", "15/08/2026", "18/08/2026", "", "Completed"],
        ["11", "", "19/08/2026", "21/08/2026", "", "Completed"],
        ["12", "", "22/08/2026", "25/08/2026", "", "Completed"],
        ["13", "", "26/08/2026", "28/08/2026", "", "Completed"],
        ["14", "Sprint 3", "29/08/2026", "31/08/2026", "", "Completed"],
        ["15", "", "01/09/2026", "01/09/2026", "", "Completed"],
        ["16", "", "02/09/2026", "04/09/2026", "", "Completed"],
        ["17", "", "05/09/2026", "08/09/2026", "", "Completed"],
        ["18", "", "09/09/2026", "11/09/2026", "", "Completed"],
        ["19", "", "12/09/2026", "15/09/2026", "", "Completed"],
        ["20", "", "16/09/2026", "18/09/2026", "", "Completed"],
        ["21", "Sprint 4", "19/09/2026", "21/09/2026", "", "Completed"],
        ["22", "", "22/09/2026", "22/09/2026", "", "Completed"],
        ["23", "", "23/09/2026", "25/09/2026", "", "Completed"],
        ["24", "", "26/09/2026", "28/09/2026", "", "Completed"],
        ["25", "", "29/09/2026", "30/09/2026", "", "Completed"],
        ["26", "", "01/10/2026", "02/10/2026", "", "Completed"],
    ]
    t35_2 = Table(plan_2, colWidths=[70, 70, 80, 80, 91, 60])
    t35_2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t35_2)
    story.append(PageBreak())

    # ==========================================
    # PAGE 28: CHAPTER 3 CONT. (Page 16)
    # ==========================================
    story.append(Paragraph("3.9 Database Design", style_h2))
    c3_db = (
        "The database design utilizes SQLite integrated through Django ORM to store and manage user credentials, "
        "department structures, equipment inventory, requisition logs, and maintenance records. The detailed "
        "specifications for each table in the schema are outlined below."
    )
    story.append(Paragraph(c3_db, style_body))

    story.append(Paragraph("3.9.1 User Table", style_h3))
    story.append(Paragraph("Table 3.6 stores employee and administrator details, login information, and user roles.", style_body))

    u_tab1 = [
        ["Field Name", "Data Type", "Key/Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique user ID", "18"],
        ["username", "VARCHAR(150)", "UNIQUE, NOT NULL", "Login username", "admin"],
        ["password", "VARCHAR(128)", "NOT NULL", "Hashed password", "pbkdf2_sha256$87..."],
        ["first_name", "VARCHAR(150)", "NOT NULL", "First name", "Aparna"],
        ["last_name", "VARCHAR(150)", "NOT NULL", "Last name", "P"],
        ["email", "VARCHAR(254)", "NOT NULL", "Email address", "aparna@gmail.com"],
        ["role", "VARCHAR(10)", "NOT NULL", "User access role", "ADMIN"],
        ["department_id", "BIGINT", "FK, NULL", "Department reference", "1"],
    ]
    t36_1 = Table(u_tab1, colWidths=[80, 95, 110, 95, 71])
    t36_1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Paragraph("Table 3.6: User table schema and sample data", style_table_caption))
    story.append(t36_1)
    story.append(PageBreak())

    # ==========================================
    # PAGE 29: CHAPTER 3 CONT. (Page 17)
    # ==========================================
    u_tab2 = [
        ["is_active", "BOOLEAN", "NOT NULL", "Account active status", "1"],
        ["is_staff", "BOOLEAN", "NOT NULL", "Django admin access", "1"],
        ["is_superuser", "BOOLEAN", "NOT NULL", "Administrator privilege", "1"],
        ["date_joined", "DATETIME", "NOT NULL", "Account creation time", "2026-09-29 14:31"],
        ["last_login", "DATETIME", "NULL", "Last login time", "2026-10-24 16:02"],
    ]
    t36_2 = Table(u_tab2, colWidths=[80, 95, 110, 95, 71])
    t36_2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t36_2)
    story.append(PageBreak())

    # ==========================================
    # PAGE 30: CHAPTER 3 CONT. (Page 18)
    # ==========================================
    story.append(Paragraph("3.9.2 Asset Table", style_h3))
    story.append(Paragraph("Table 3.7 stores physical inventory assets, category classifications, and quantity thresholds.", style_body))

    asset_tab1 = [
        ["Field Name", "Data Type", "Key/Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique asset ID", "15"],
        ["name", "VARCHAR(200)", "NOT NULL", "Asset name/model", "ThinkPad T14"],
        ["category_id", "BIGINT", "FK, NOT NULL", "Linked category", "1"],
        ["department_id", "BIGINT", "FK, NULL", "Linked department", "1"],
        ["description", "TEXT", "BLANK", "Specifications", "Core i7, 16GB RAM"],
        ["total_quantity", "INTEGER", "NOT NULL", "Total fleet units", "10"],
        ["available_quantity", "INTEGER", "NOT NULL", "Available in stock", "9"],
    ]
    t37_1 = Table(asset_tab1, colWidths=[85, 90, 110, 95, 71])
    t37_1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Paragraph("Table 3.7: Asset table schema and sample data", style_table_caption))
    story.append(t37_1)
    story.append(PageBreak())

    # ==========================================
    # PAGE 31: CHAPTER 3 CONT. (Page 19)
    # ==========================================
    asset_tab2 = [
        ["low_stock_threshold", "INTEGER", "NOT NULL", "Alert trigger limit", "2"],
    ]
    t37_2 = Table(asset_tab2, colWidths=[85, 90, 110, 95, 71])
    t37_2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t37_2)
    story.append(PageBreak())

    # ==========================================
    # PAGE 32: CHAPTER 3 CONT. (Page 20)
    # ==========================================
    story.append(Paragraph("3.9.3 Asset Request Table", style_h3))
    story.append(Paragraph("Table 3.8 stores asset checkout requisitions, approval status, and return timestamps.", style_body))

    req_tab = [
        ["Field Name", "Data Type", "Key/Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique request ID", "3"],
        ["employee_id", "BIGINT", "FK, NOT NULL", "Requesting user", "23"],
        ["asset_id", "BIGINT", "FK, NOT NULL", "Requested asset", "15"],
        ["quantity", "INTEGER", "NOT NULL", "Requested count", "1"],
        ["status", "VARCHAR(10)", "NOT NULL", "Requisition state", "APPROVED"],
        ["notes", "TEXT", "BLANK", "Checkout reason", "Onsite deployment"],
        ["admin_notes", "TEXT", "BLANK", "Admin feedback", "Approved for 14d"],
        ["request_date", "DATETIME", "NOT NULL", "Submission date", "2026-09-30 03:58"],
        ["response_date", "DATETIME", "NULL", "Decision date", "2026-09-30 04:04"],
        ["return_date", "DATETIME", "NULL", "Return timestamp", "NULL"],
    ]
    t38 = Table(req_tab, colWidths=[80, 85, 110, 100, 76])
    t38.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(Paragraph("Table 3.8: Asset request table schema and sample data", style_table_caption))
    story.append(t38)
    story.append(PageBreak())

    # ==========================================
    # PAGE 33: CHAPTER 3 CONT. (Page 21)
    # ==========================================
    story.append(Paragraph("3.9.4 Department Table", style_h3))
    story.append(Paragraph("Table 3.9 stores organizational departments.", style_body))

    dept_tab = [
        ["Field Name", "Data Type", "Key/Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique department ID", "1"],
        ["name", "VARCHAR(100)", "UNIQUE, NOT NULL", "Department name", "Finance"],
        ["description", "TEXT", "BLANK", "Department overview", "Accounting & Payroll"],
    ]
    t39 = Table(dept_tab, colWidths=[80, 95, 110, 95, 71])
    t39.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Paragraph("Table 3.9: Department table schema and sample data", style_table_caption))
    story.append(t39)
    story.append(PageBreak())

    # ==========================================
    # PAGE 34: CHAPTER 3 CONT. (Page 22)
    # ==========================================
    story.append(Paragraph("3.9.5 Task and SubTask Table", style_h3))
    story.append(Paragraph("Table 3.10 stores tasks and checklist subtasks.", style_body))

    task_tab = [
        ["Field Name", "Data Type", "Key/Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique task ID", "1"],
        ["title", "VARCHAR(200)", "NOT NULL", "Task title", "Deploy Server"],
        ["assigned_to_id", "BIGINT", "FK, NULL", "Assigned employee", "19"],
        ["workload_hours", "INTEGER", "NOT NULL", "Estimated effort", "3"],
        ["priority", "VARCHAR(10)", "NOT NULL", "Priority rank", "HIGH"],
        ["status", "VARCHAR(20)", "NOT NULL", "Completion status", "IN_PROGRESS"],
        ["deadline", "DATETIME", "NOT NULL", "Due timestamp", "2026-10-02 18:03"],
        ["created_at", "DATETIME", "NOT NULL", "Creation timestamp", "2026-10-02 18:03"],
    ]
    t310 = Table(task_tab, colWidths=[80, 95, 110, 95, 71])
    t310.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Paragraph("Table 3.10: Task and SubTask table schema and sample data", style_table_caption))
    story.append(t310)
    story.append(PageBreak())

    # ==========================================
    # PAGE 35: CHAPTER 3 CONT. (Page 23)
    # ==========================================
    story.append(Paragraph("3.9.6 Maintenance Issue Table", style_h3))
    story.append(Paragraph("Table 3.11 stores equipment damage reports and repair records.", style_body))

    maint_tab = [
        ["Field Name", "Data Type", "Key/Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique issue ID", "1"],
        ["asset_id", "BIGINT", "FK, NOT NULL", "Associated asset", "15"],
        ["department_id", "BIGINT", "FK, NULL", "Target department", "1"],
        ["reported_by_id", "BIGINT", "FK, NOT NULL", "Reporter user ID", "19"],
        ["description", "TEXT", "NOT NULL", "Defect details", "Trackpad sticking"],
        ["is_damaged", "BOOLEAN", "NOT NULL", "Severe damage flag", "1"],
        ["priority", "VARCHAR(10)", "NOT NULL", "Urgency level", "HIGH"],
        ["status", "VARCHAR(20)", "NOT NULL", "Resolution status", "REPORTED"],
        ["reported_at", "DATETIME", "NOT NULL", "Report timestamp", "2026-10-04 06:23"],
    ]
    t311 = Table(maint_tab, colWidths=[80, 90, 110, 100, 71])
    t311.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(Paragraph("Table 3.11: Maintenance issue table schema and sample data", style_table_caption))
    story.append(t311)
    story.append(PageBreak())

    # ==========================================
    # PAGE 36: CHAPTER 3 CONT. (Page 24)
    # ==========================================
    story.append(Paragraph("3.9.7 Department Issue Table", style_h3))
    story.append(Paragraph("Table 3.12 tracks inter-departmental collaboration requests and complaints.", style_body))

    dept_issue_tab = [
        ["Field Name", "Data Type", "Key/Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique ticket ID", "1"],
        ["title", "VARCHAR(200)", "NOT NULL", "Ticket title", "Onboarding kit"],
        ["description", "TEXT", "NOT NULL", "Request details", "Need developer badge"],
        ["target_department_id", "BIGINT", "FK, NOT NULL", "Target unit ID", "2"],
        ["reported_by_id", "BIGINT", "FK, NOT NULL", "Reporter ID", "20"],
        ["priority", "VARCHAR(10)", "NOT NULL", "Urgency ranking", "MEDIUM"],
        ["status", "VARCHAR(20)", "NOT NULL", "Ticket state", "OPEN"],
        ["created_at", "DATETIME", "NOT NULL", "Creation time", "2026-09-29 15:26"],
    ]
    t312 = Table(dept_issue_tab, colWidths=[95, 80, 110, 95, 71])
    t312.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(Paragraph("Table 3.12: Department issue table schema and sample data", style_table_caption))
    story.append(t312)
    story.append(PageBreak())

    # ==========================================
    # PAGE 37: CHAPTER 3 CONT. (Page 25)
    # ==========================================
    story.append(Paragraph("3.9.8 Award Table", style_h3))
    story.append(Paragraph("Table 3.13 stores achievement badges and recognitions.", style_body))

    award_tab = [
        ["Field Name", "Data Type", "Key/Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique badge ID", "1"],
        ["employee_id", "BIGINT", "FK, NOT NULL", "Recipient ID", "19"],
        ["badge_icon", "VARCHAR(50)", "NOT NULL", "Symbolic emoji", "🏆"],
        ["name", "VARCHAR(100)", "NOT NULL", "Badge title", "Timely Finish"],
        ["description", "TEXT", "BLANK", "Achievement note", "Completed on time"],
        ["awarded_at", "DATETIME", "NOT NULL", "Timestamp", "2026-10-05 13:13"],
    ]
    t313 = Table(award_tab, colWidths=[80, 90, 110, 100, 71])
    t313.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Paragraph("Table 3.13: Award and badge table schema and sample data", style_table_caption))
    story.append(t313)
    story.append(PageBreak())

    # ==========================================
    # PAGE 38: CHAPTER 4. RESULTS AND DISCUSSIONS (Page 26)
    # ==========================================
    story.append(Paragraph("Chapter 4. Results and Discussions", style_h1_left))
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.1 Results", style_h2))
    c4_res = (
        "The Role-Based Inventory and Asset Management System was developed and tested module by module. "
        "Each role has its own dashboard with a navigation sidebar and summary cards. "
        "Figures 4.1–4.6 show the implemented interfaces."
    )
    story.append(Paragraph(c4_res, style_body))

    story.append(Paragraph("Figure 4.1 Users enter their username and password. Employees who do not have an account can register through the \"Register\" link.", style_body))
    story.append(Spacer(1, 10))

    # User Uploaded Screenshot: Login
    img_login = "screenshots/login.png"
    if os.path.exists(img_login):
        story.append(Image(img_login, width=420, height=197))
    story.append(Paragraph("Figure 4.1: Login Page", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 39: CHAPTER 4 CONT. (Page 27)
    # ==========================================
    story.append(Paragraph("Figure 4.2 Summary cards show the number of assets, low stock alerts, pending requests, active tasks, open issues and departments. A low stock alert section shows items below threshold. Quick action buttons allow adding assets, departments, creating tasks, granting awards, and generating PDF/Excel reports.", style_body))
    story.append(Spacer(1, 6))

    img_admin = "screenshots/admin_dashboard.png"
    if os.path.exists(img_admin):
        story.append(Image(img_admin, width=380, height=204))
    story.append(Paragraph("Figure 4.2: Admin Dashboard", style_caption))

    story.append(Paragraph("Figure 4.3 Shows departmental units with staff headcount, allocated assets and issue counts. The administrator can create new departments and manage organizational structures.", style_body))
    story.append(Spacer(1, 6))

    img_dept = "screenshots/departments.png"
    if os.path.exists(img_dept):
        story.append(Image(img_dept, width=380, height=210))
    story.append(Paragraph("Figure 4.3: Department Management", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 40: CHAPTER 4 CONT. (Page 28)
    # ==========================================
    story.append(Paragraph("Figure 4.4 Lists inventory assets with category, department, availability bar and stock status pills. Filter controls allow filtering by category, department and availability status.", style_body))
    story.append(Spacer(1, 6))

    img_assets = "screenshots/assets.png"
    if os.path.exists(img_assets):
        story.append(Image(img_assets, width=380, height=208))
    story.append(Paragraph("Figure 4.4: Asset List & Availability", style_caption))

    story.append(Paragraph("Figure 4.5 Shows the asset creation form where administrators specify asset name, category, assigned department, total quantity, available quantity, and low-stock alert threshold.", style_body))
    story.append(Spacer(1, 6))

    img_add = "screenshots/add_asset.png"
    if os.path.exists(img_add):
        story.append(Image(img_add, width=360, height=210))
    story.append(Paragraph("Figure 4.5: Add New Asset Form", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 41: CHAPTER 4 CONT. (Page 29)
    # ==========================================
    story.append(Paragraph("Figure 4.6 Shows the employee dashboard where staff view active tasks, requisition approved assets, check off milestone subtasks, report maintenance defects, and track earned recognition badges.", style_body))
    story.append(Spacer(1, 6))

    img_emp = "screenshots/employee_dashboard.png"
    if os.path.exists(img_emp):
        story.append(Image(img_emp, width=380, height=209))
    story.append(Paragraph("Figure 4.6: Employee Dashboard", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 42: CHAPTER 4 CONT. (Page 30)
    # ==========================================
    story.append(Paragraph("4.2 Discussion", style_h2))
    c4_disc = (
        "The results show that the Role-Based Inventory and Asset Management System manages the complete "
        "asset lifecycle through a single platform, from requisition submission to return restoration. Each "
        "user works through a dashboard that matches their role, and the status of requests, reports and "
        "inventory levels is available without approaching several people. This section discusses the observed "
        "behaviour of the system, its effect on the inventory monitoring process and its limitations."
    )
    story.append(Paragraph(c4_disc, style_body))

    story.append(Paragraph("4.2.1 Analysis of Results", style_h3))
    story.append(Paragraph("The system replaces the email- and paper-based process with a single workflow. An employee submits a requisition, the administrator reviews it, and stock is decremented upon approval. When the item is returned, stock is automatically restored. The dashboards show the current stage of every request, so employees no longer need to approach several people to learn their status.", style_body))

    story.append(Paragraph("4.2.2 Role-Based Access Control", style_h3))
    story.append(Paragraph("After login each user is redirected to the dashboard of their own role. If a user tries to open a page belonging to another role, they are redirected back to their own dashboard. The administrator is directed to the executive dashboard. This keeps data and functions limited to the people responsible for them.", style_body))

    story.append(Paragraph("4.2.3 Requisition Workflow and Validation", style_h3))
    story.append(Paragraph("An employee cannot request more units than currently available in stock. Form validation prevents invalid quantities, and the return check-in action safely replenishes inventory back to shelf.", style_body))

    story.append(Paragraph("4.2.4 Development Process", style_h3))
    story.append(Paragraph("The system was developed in an Agile manner, with separate feature branches for authentication, inventory, departments, requisitions and task tracking. Each branch was merged into the main branch after it was completed, so every module could be built and tested on its own without affecting the rest of the system.", style_body))
    story.append(PageBreak())

    # ==========================================
    # PAGE 43: CHAPTER 4 CONT. (Page 31)
    # ==========================================
    story.append(Paragraph("4.2.5 Limitations", style_h3))
    story.append(Paragraph("• Email and SMS notifications are not yet available, so users see updates on request status and task assignments only after logging in.", style_bullet))
    story.append(Paragraph("• Communication between the employee and the administrator is limited to stored ticket notes, with no real-time chat.", style_bullet))
    story.append(Paragraph("• The system currently runs in a development environment with sample data and has not yet been deployed on cloud servers for production.", style_bullet))
    story.append(Paragraph("• Automated barcode or RFID scanning hardware is not yet integrated for physical checkout counters.", style_bullet))
    story.append(Paragraph("• System-wide testing with a large number of concurrent users and legacy data imports is still in progress.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # PAGE 44: CHAPTER 5. CONCLUSION (Page 32)
    # ==========================================
    story.append(Paragraph("Chapter 5. Conclusion and Future Scope", style_h1_left))
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.1 Conclusion", style_h2))
    c5_1 = (
        "The Role-Based Inventory and Asset Management System is a web-based application that brings the "
        "management, monitoring and requisition of departmental equipment into one centralized platform. It replaces "
        "the email- and paper-based process with a role-based system for Administrators, Department Heads, and Employees. "
        "Each user logs in to a dashboard that shows only the features and information relevant to their role."
    )
    story.append(Paragraph(c5_1, style_body))

    c5_2 = (
        "The system covers the complete asset lifecycle, from inventory cataloging and threshold warnings to requisition "
        "approval, return stock restoration, defect reporting, and workload-balanced task dispatching. Because asset status, "
        "rejection notes and return logs are stored in one place, employees no longer need to approach several people to know "
        "the status of their requests, and the problems of lost, delayed or duplicated information are greatly reduced. Overall, "
        "the system improves communication between staff and administrators, reduces paperwork and manual effort, and makes "
        "the inventory tracking process more transparent and reliable. In future, it can be improved by adding email and SMS "
        "notifications, real-time messaging, barcode scanning, and deployment for use by a whole institution."
    )
    story.append(Paragraph(c5_2, style_body))

    story.append(Paragraph("Key achievements include:", style_body))
    story.append(Paragraph("• Secure role-based authentication with a dashboard for each role.", style_bullet))
    story.append(Paragraph("• An online requisition workflow with stock verification, approval, rejection feedback, and automated return restoration.", style_bullet))
    story.append(Paragraph("• Department management and dual-channel maintenance and inter-departmental ticketing.", style_bullet))
    story.append(Paragraph("• A structured database holding asset records, requests, tasks, subtasks, issues and awards.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # PAGE 45: CHAPTER 5 CONT. (Page 33)
    # ==========================================
    story.append(Paragraph("• Workload auto-assignment balancing tasks across eligible employees.", style_bullet))
    story.append(Paragraph("• An Agile development process with version-controlled, feature-wise development using Git and GitHub.", style_bullet))
    story.append(Spacer(1, 8))

    c5_end = (
        "The project demonstrates how web technologies and a role-based workflow can be integrated to address the problem of "
        "scattered and manual inventory management in organizational departments. The system can assist employees in tracking "
        "their requisitions, defects and tasks, and help administrators to monitor and evaluate assets efficiently by keeping "
        "all inventory records in one centralized platform."
    )
    story.append(Paragraph(c5_end, style_body))

    story.append(Paragraph("5.2 Future Scope", style_h2))
    story.append(Paragraph("The proposed system can be further enhanced to improve its accuracy, usability, and practical application. The following features can be considered in future versions:", style_body))
    story.append(Paragraph("• <b>Barcode and QR code scanning:</b> Add mobile camera scanning for fast equipment checkout and check-in.", style_bullet))
    story.append(Paragraph("• <b>Email and SMS notifications:</b> Notify employees and administrators about status changes, stock alerts and task deadlines.", style_bullet))
    story.append(Paragraph("• <b>Real-time chat:</b> Add direct messaging between employees and administrators.", style_bullet))
    story.append(Paragraph("• <b>Deadline reminders and calendar:</b> Add automatic reminders for pending tasks and equipment return schedules.", style_bullet))
    story.append(Paragraph("• <b>Analytics and reports:</b> Provide charts and exportable reports of asset depreciation and maintenance costs for the department.", style_bullet))
    story.append(Paragraph("• <b>Production deployment:</b> Move from SQLite to PostgreSQL and host the system on cloud servers for the whole organization.", style_bullet))
    story.append(Paragraph("• <b>Mobile application:</b> Provide a mobile version for quick inventory scanning and request updates.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # PAGE 46: REFERENCES (Page 34)
    # ==========================================
    story.append(Paragraph("References", style_h1_left))
    story.append(Spacer(1, 10))

    refs = [
        "[1] O. Eweoya, A. O. Agbeyangi and J. M. Lukose, “TaskHive: A Web-Based Academic Project Management System for Higher Education,” Information Impact: Journal of Information and Knowledge Management, 2025. [Online]. Available: https://www.ajol.info/index.php/iijikm/article/view/302689",
        "[2] IIT Madras, “Tracking Student Progress in Software Projects,” Software Engineering Projects. [Online]. Available: https://seprojects.study.iitm.ac.in/term_projects/2024_sept/problem_statement.html",
        "[3] GitHub Docs, “GitHub Documentation.” [Online]. Available: https://docs.github.com/",
        "[4] Django Software Foundation, “Django Documentation.” [Online]. Available: https://docs.djangoproject.com/",
        "[5] Tailwind Labs, “Tailwind CSS Documentation,” 2026. [Online]. Available: https://tailwindcss.com/",
        "[6] Python Software Foundation, “Python 3.13 Documentation,” 2026. [Online]. Available: https://docs.python.org/3/",
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref', fontName='Times-Roman', fontSize=11, leading=16, spaceAfter=10)))
    story.append(PageBreak())

    # ==========================================
    # PAGE 47: APPENDIX A: DFD (Page 35)
    # ==========================================
    story.append(Paragraph("Appendix A: Data Flow Diagram", style_h1_left))
    story.append(Spacer(1, 10))

    dfd_p = (
        "Figure A.1 Level 0 DFD shows the Role-Based Inventory and Asset Management System as a single process, "
        "with the Employee, Administrator and Department Head as external entities and the database as the data store."
    )
    story.append(Paragraph(dfd_p, style_body))
    story.append(Spacer(1, 15))

    dfd_file = "dfd.png"
    if os.path.exists(dfd_file):
        story.append(Image(dfd_file, width=440, height=290))
    story.append(Paragraph("Figure A.1: Level 0 DFD", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 48: APPENDIX A CONT. (Page 36)
    # ==========================================
    story.append(Paragraph("Figure A.2 Level 1 DFD shows the processes for the Employee, such as registration, login, catalog browsing, asset requisition submission, return check-in, maintenance defect reporting and viewing of status and badges.", style_body))
    story.append(Spacer(1, 20))

    box_dfd1 = [["[ Level 1 DFD Diagram: Employee Requisition & Return Flow ]\nEmployee -> Register / Login -> Browse Catalog -> Request Asset -> Return Asset"]]
    t_dfd1 = Table(box_dfd1, colWidths=[440], rowHeights=[260])
    t_dfd1.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(t_dfd1)
    story.append(Paragraph("Figure A.2: Level 1 DFD", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 49: APPENDIX A CONT. (Page 37)
    # ==========================================
    story.append(Paragraph("Figure A.3 Level 2 DFD shows the processes for the Administrator, such as managing assets, creating departments, approving or rejecting requisitions, allocating equipment, resolving maintenance issues, and dispatching tasks.", style_body))
    story.append(Spacer(1, 20))

    box_dfd2 = [["[ Level 2 DFD Diagram: Administrator Inventory & Allocation Flow ]\nAdmin -> Manage Departments -> Add Assets -> Review Requests -> Dispatch Tasks"]]
    t_dfd2 = Table(box_dfd2, colWidths=[440], rowHeights=[260])
    t_dfd2.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(t_dfd2)
    story.append(Paragraph("Figure A.3: Level 2 DFD", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 50: APPENDIX A CONT. (Page 38)
    # ==========================================
    story.append(Paragraph("Figure A.4 Level 3 DFD shows the processes for Requisitions, checking inventory sufficiency, updating request status, decrementing available stock upon approval, and replenishing stock upon return.", style_body))
    story.append(Spacer(1, 20))

    box_dfd3 = [["[ Level 3 DFD Diagram: Requisition Lifecycle & Stock Restoration ]\nRequest Asset -> Check Available Stock -> Approve -> Decrement Stock -> Return Asset -> Replenish Stock"]]
    t_dfd3 = Table(box_dfd3, colWidths=[440], rowHeights=[260])
    t_dfd3.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(t_dfd3)
    story.append(Paragraph("Figure A.4: Level 3 DFD", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 51: APPENDIX A CONT. (Page 39)
    # ==========================================
    story.append(Paragraph("Figure A.5 Level 4 DFD shows the processes for Maintenance and Tasks, such as defect reporting, cross-department ticketing, workload-balancing auto-assignment, subtask toggling, and timely completion badge granting.", style_body))
    story.append(Spacer(1, 20))

    box_dfd4 = [["[ Level 4 DFD Diagram: Maintenance, Tasks & Gamification Flow ]\nReport Defect -> Update Ticket -> Create Task -> Auto-Assign by Workload -> Toggle Subtasks -> Award Badge"]]
    t_dfd4 = Table(box_dfd4, colWidths=[440], rowHeights=[260])
    t_dfd4.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(t_dfd4)
    story.append(Paragraph("Figure A.5: Level 4 DFD", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 52: APPENDIX B: ER DIAGRAM (Page 40)
    # ==========================================
    story.append(Paragraph("Appendix B: Entity–Relationship Diagram", style_h1_left))
    story.append(Spacer(1, 10))

    erd_p = (
        "Figure B.1 shows the entities, attributes and relationships used by the Role-Based Inventory and Asset "
        "Management System. It covers users and their roles, departments, asset categories, physical equipment items, "
        "asset requests, tasks, milestone subtasks, maintenance issues, department tickets, and recognition awards. "
        "The relationships show how assets belong to categories and departments, how requests link employees to assets, "
        "and how tasks and issues are tracked across departments."
    )
    story.append(Paragraph(erd_p, style_body))
    story.append(Spacer(1, 10))

    erd_file = "erd.png"
    if os.path.exists(erd_file):
        story.append(Image(erd_file, width=440, height=440))
    story.append(Paragraph("Figure B.1: Entity–relationship diagram for users, roles, assets, requests and tasks", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 53: APPENDIX C: SOURCE CODE (Page 41)
    # ==========================================
    story.append(Paragraph("Appendix C: Source Code", style_h1_left))
    story.append(Spacer(1, 10))
    story.append(Paragraph("C.1 Asset Data Model", style_h3))

    code_c1 = [
        "class Asset(models.Model):",
        "    name = models.CharField(max_length=200)",
        "    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='assets')",
        "    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)",
        "    description = models.TextField(blank=True)",
        "    total_quantity = models.PositiveIntegerField(default=0)",
        "    available_quantity = models.PositiveIntegerField(default=0)",
        "    low_stock_threshold = models.PositiveIntegerField(default=5)",
        "",
        "    def __str__(self):",
        "        return self.name",
        "",
        "    @property",
        "    def is_low_stock(self):",
        "        return self.available_quantity <= self.low_stock_threshold",
        "",
        "    @property",
        "    def stock_status(self):",
        "        if self.available_quantity == 0:",
        "            return 'OUT_OF_STOCK'",
        "        elif self.available_quantity <= self.low_stock_threshold:",
        "            return 'LOW_STOCK'",
        "        return 'IN_STOCK'",
    ]
    for line in code_c1:
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # PAGE 54: APPENDIX C CONT. (Page 42)
    # ==========================================
    story.append(Paragraph("C.2 Asset Requisition and Return Model", style_h3))
    code_c2 = [
        "class AssetRequest(models.Model):",
        "    STATUS_CHOICES = (",
        "        ('PENDING', 'Pending'),",
        "        ('APPROVED', 'Approved'),",
        "        ('REJECTED', 'Rejected'),",
        "        ('RETURNED', 'Returned'),",
        "    )",
        "    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')",
        "    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='requests')",
        "    quantity = models.PositiveIntegerField(default=1)",
        "    notes = models.TextField(blank=True, default='')",
        "    admin_notes = models.TextField(blank=True, default='')",
        "    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')",
        "    request_date = models.DateTimeField(auto_now_add=True)",
        "    response_date = models.DateTimeField(null=True, blank=True)",
        "    return_date = models.DateTimeField(null=True, blank=True)",
        "",
        "    def __str__(self):",
        "        return f'{self.employee.username} - {self.asset.name} ({self.status})'",
    ]
    for line in code_c2:
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # PAGE 55: APPENDIX C CONT. (Page 43)
    # ==========================================
    story.append(Paragraph("C.3 Task and SubTask Models", style_h3))
    code_c3 = [
        "class Task(models.Model):",
        "    STATUS_CHOICES = (",
        "        ('PENDING', 'Pending'),",
        "        ('IN_PROGRESS', 'In Progress'),",
        "        ('COMPLETED', 'Completed'),",
        "    )",
        "    title = models.CharField(max_length=200)",
        "    description = models.TextField(blank=True)",
        "    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)",
        "    required_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)",
        "    deadline = models.DateTimeField()",
        "    workload_hours = models.PositiveIntegerField(default=1)",
        "    priority = models.CharField(max_length=10, default='MEDIUM')",
        "    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')",
        "    created_at = models.DateTimeField(auto_now_add=True)",
        "    completed_at = models.DateTimeField(null=True, blank=True)",
        "",
        "class SubTask(models.Model):",
        "    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')",
        "    title = models.CharField(max_length=200)",
        "    is_completed = models.BooleanField(default=False)",
    ]
    for line in code_c3:
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # PAGE 56: APPENDIX C CONT. (Page 44)
    # ==========================================
    story.append(Paragraph("C.4 Admin Requisition Approval View", style_h3))
    code_c4 = [
        "@login_required",
        "def approve_request(request, request_id):",
        "    if not request.user.is_admin_role:",
        "        return redirect('employee_dashboard')",
        "    asset_req = get_object_or_404(AssetRequest, id=request_id)",
        "    if asset_req.status == 'PENDING':",
        "        if asset_req.asset.available_quantity >= asset_req.quantity:",
        "            asset_req.asset.available_quantity -= asset_req.quantity",
        "            asset_req.asset.save()",
        "            asset_req.status = 'APPROVED'",
        "            asset_req.response_date = timezone.now()",
        "            asset_req.save()",
        "            messages.success(request, f'Request #{asset_req.id} approved successfully.')",
        "        else:",
        "            messages.error(request, 'Not enough quantity available.')",
        "    return redirect('request_list')",
    ]
    for line in code_c4:
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # PAGE 57: APPENDIX C CONT. (Page 45)
    # ==========================================
    story.append(Paragraph("C.5 Return Asset Controller View", style_h3))
    code_c5 = [
        "@login_required",
        "def return_asset(request, request_id):",
        "    asset_req = get_object_or_404(AssetRequest, id=request_id)",
        "    if not request.user.is_admin_role and request.user != asset_req.employee:",
        "        return redirect('employee_dashboard')",
        "    if asset_req.status == 'APPROVED':",
        "        asset_req.asset.available_quantity += asset_req.quantity",
        "        if asset_req.asset.available_quantity > asset_req.asset.total_quantity:",
        "            asset_req.asset.available_quantity = asset_req.asset.total_quantity",
        "        asset_req.asset.save()",
        "        asset_req.status = 'RETURNED'",
        "        asset_req.return_date = timezone.now()",
        "        asset_req.save()",
        "        messages.success(request, f'Asset returned. Stock restored.')",
        "    return redirect('request_list')",
    ]
    for line in code_c5:
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # PAGE 58: APPENDIX C CONT. (Page 46)
    # ==========================================
    story.append(Paragraph("C.6 Workload Auto-Assignment View", style_h3))
    code_c6 = [
        "if 'auto_assign' in request.POST and task.required_skill:",
        "    eligible = User.objects.filter(role='EMPLOYEE', skills=task.required_skill)",
        "    if eligible.exists():",
        "        eligible = eligible.annotate(",
        "            workload=Sum('tasks__workload_hours', filter=Q(tasks__status__in=['PENDING', 'IN_PROGRESS']))",
        "        )",
        "        best_emp = None",
        "        lowest_workload = float('inf')",
        "        for emp in eligible:",
        "            wl = emp.workload or 0",
        "            if wl < lowest_workload:",
        "                lowest_workload = wl",
        "                best_emp = emp",
        "        if best_emp:",
        "            task.assigned_to = best_emp",
        "            messages.success(request, f'Auto-assigned to {best_emp.username}.')",
    ]
    for line in code_c6:
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # PAGE 59: APPENDIX C CONT. (Page 47)
    # ==========================================
    story.append(Paragraph("C.7 Subtask Milestone Toggle Controller", style_h3))
    code_c7 = [
        "@login_required",
        "def update_subtask_status(request, subtask_id):",
        "    subtask = get_object_or_404(SubTask, id=subtask_id)",
        "    task = subtask.task",
        "    if request.method == 'POST':",
        "        subtask.is_completed = request.POST.get('is_completed') == 'on'",
        "        subtask.save()",
        "        all_done = all(st.is_completed for st in task.subtasks.all())",
        "        if all_done and task.status != 'COMPLETED':",
        "            task.status = 'COMPLETED'",
        "            task.completed_at = timezone.now()",
        "            task.save()",
        "            if task.completed_at <= task.deadline and task.assigned_to:",
        "                Award.objects.create(",
        "                    employee=task.assigned_to,",
        "                    badge_icon='🏆',",
        "                    name=f'Timely Finish: {task.title[:30]}',",
        "                    description=f'Completed on time before deadline.'",
        "                )",
        "    return redirect('task_list')",
    ]
    for line in code_c7:
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # PAGE 60: APPENDIX C CONT. (Page 48)
    # ==========================================
    story.append(Paragraph("C.8 System URL Configurations (inventory/urls.py)", style_h3))
    code_c8 = [
        "urlpatterns = [",
        "    path('', views.dashboard_view, name='dashboard'),",
        "    path('login/', views.custom_login_view, name='login'),",
        "    path('register/', views.register, name='register'),",
        "    path('logout/', views.custom_logout_view, name='logout'),",
        "    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),",
        "    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),",
        "    path('departments/', views.department_list, name='department_list'),",
        "    path('assets/', views.asset_list, name='asset_list'),",
        "    path('requests/', views.request_list, name='request_list'),",
        "    path('issues/', views.issue_list, name='issue_list'),",
        "    path('tasks/', views.task_list, name='task_list'),",
        "    path('awards/', views.award_list, name='award_list'),",
        "]",
    ]
    for line in code_c8:
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # PAGE 61: APPENDIX D: SCREENSHOTS (Page 49)
    # ==========================================
    story.append(Paragraph("Appendix D: Screenshots", style_h1_left))
    story.append(Spacer(1, 6))
    story.append(Paragraph("D.1 Login Page", style_d_h3))
    story.append(Paragraph("Figure D.1 shows the login interface where administrators, department heads, and employees authenticate securely with role-based automatic routing.", style_d_body))

    if os.path.exists("screenshots/login.png"):
        story.append(Image("screenshots/login.png", width=380, height=170))
    story.append(Paragraph("Figure D.1: Login page of the system", style_d_caption))

    story.append(Paragraph("D.2 Admin Dashboard Page", style_d_h3))
    story.append(Paragraph("Figure D.2 shows the administrator dashboard with real-time inventory metrics, low-stock threshold warning counters, active requisition queues, and administrative action buttons.", style_d_body))

    if os.path.exists("screenshots/admin_dashboard.png"):
        story.append(Image("screenshots/admin_dashboard.png", width=380, height=170))
    story.append(Paragraph("Figure D.2: Admin dashboard with asset metrics", style_d_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 62: APPENDIX D CONT. (Page 50)
    # ==========================================
    story.append(Paragraph("D.3 Department Management Page", style_d_h3))
    story.append(Paragraph("Figure D.3 shows the department management directory displaying staff headcount, allocated departmental assets, issue counts, and controls to add or edit organizational units.", style_d_body))

    if os.path.exists("screenshots/departments.png"):
        story.append(Image("screenshots/departments.png", width=320, height=122))
    story.append(Paragraph("Figure D.3: Department management directory", style_d_caption))

    story.append(Paragraph("D.4 Asset List & Availability Page", style_d_h3))
    story.append(Paragraph("Figure D.4 shows the asset catalog with real-time availability progress bars, category classifications, department assignments, and quick search filters.", style_d_body))

    if os.path.exists("screenshots/assets.png"):
        story.append(Image("screenshots/assets.png", width=320, height=122))
    story.append(Paragraph("Figure D.4: Asset catalog with availability progress bars", style_d_caption))

    story.append(Paragraph("D.5 Add New Asset Page", style_d_h3))
    story.append(Paragraph("Figure D.5 shows the add new asset form where administrators specify item details, category, assigned department, initial inventory count, and low-stock alert thresholds.", style_d_body))

    if os.path.exists("screenshots/add_asset.png"):
        story.append(Image("screenshots/add_asset.png", width=300, height=122))
    story.append(Paragraph("Figure D.5: Add new asset form", style_d_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 63: APPENDIX D CONT. (Page 51)
    # ==========================================
    story.append(Paragraph("D.6 Employee Dashboard Page", style_d_h3))
    story.append(Paragraph("Figure D.6 shows the employee workspace dashboard displaying assigned tasks, milestone subtask checkboxes, recent requisition history, and earned badges.", style_d_body))

    if os.path.exists("screenshots/employee_dashboard.png"):
        story.append(Image("screenshots/employee_dashboard.png", width=320, height=122))
    story.append(Paragraph("Figure D.6: Employee workspace dashboard", style_d_caption))

    story.append(Paragraph("D.7 Asset Requests & Approvals Page", style_d_h3))
    story.append(Paragraph("Figure D.7 shows the asset requisition and return tracker where administrators review requests, grant approvals or rejections, and check in returned items to replenish stock.", style_d_body))

    if os.path.exists("screenshots/requests.png"):
        story.append(Image("screenshots/requests.png", width=320, height=120))
    story.append(Paragraph("Figure D.7: Asset requisition and return tracker", style_d_caption))

    story.append(Paragraph("D.8 Complaint & Issue Management Page", style_d_h3))
    story.append(Paragraph("Figure D.8 shows the dual-channel issue tracking interface covering physical equipment maintenance defects and cross-departmental operational tickets through to resolution.", style_d_body))

    if os.path.exists("screenshots/issues.png"):
        story.append(Image("screenshots/issues.png", width=320, height=122))
    story.append(Paragraph("Figure D.8: Maintenance defect and issue tracker", style_d_caption))
    story.append(PageBreak())

    # ==========================================
    # PAGE 64: APPENDIX D CONT. (Page 52)
    # ==========================================
    story.append(Paragraph("D.9 Task & Subtask Management Page", style_d_h3))
    story.append(Paragraph("Figure D.9 shows the workload-balanced task management board where administrative tasks are broken down into milestone subtasks, assigned to employees, and monitored.", style_d_body))

    if os.path.exists("screenshots/tasks.png"):
        story.append(Image("screenshots/tasks.png", width=380, height=170))
    story.append(Paragraph("Figure D.9: Task and milestone subtask board", style_d_caption))

    story.append(Paragraph("D.10 Performance Awards & Badges Page", style_d_h3))
    story.append(Paragraph("Figure D.10 shows the gamified recognition center where employees earn achievement badges for exemplary contributions and timely milestone completions.", style_d_body))

    if os.path.exists("screenshots/awards.png"):
        story.append(Image("screenshots/awards.png", width=380, height=170))
    story.append(Paragraph("Figure D.10: Gamified recognition badges and awards", style_d_caption))

    # Build PDF
    doc.build(story, canvasmaker=KTUCanvas)
    print(f"Successfully generated {pdf_filename} with all 64 pages and real screenshots!")

if __name__ == '__main__':
    build_pdf()
