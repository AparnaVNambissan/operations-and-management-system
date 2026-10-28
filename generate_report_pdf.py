import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Do not draw headers or footers on the cover page (page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))

        # Running Header (pages 6 onwards)
        if self._pageNumber >= 6:
            self.drawString(54, A4[1] - 36, "Role-Based Inventory and Asset Management System")
            self.drawRightString(A4[0] - 54, A4[1] - 36, "Aparna (MES25MCA-2010)")
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(54, A4[1] - 40, A4[0] - 54, A4[1] - 40)

        # Running Footer
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.5)
        self.line(54, 46, A4[0] - 54, 46)

        self.drawString(54, 32, "Department of Computer Applications, MES College of Engineering")
        self.drawRightString(A4[0] - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def create_report():
    pdf_filename = "AparnaProject.pdf"
    
    # 54pt (0.75 in) margins
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        alignment=1, # Center
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=12
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#334155'),
        spaceAfter=15
    )

    style_cover_author = ParagraphStyle(
        'CoverAuthor',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    style_cover_inst = ParagraphStyle(
        'CoverInst',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#475569')
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        alignment=4, # Justified
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=7
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        leftIndent=15,
        firstLineIndent=-10,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )

    style_caption = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=1, # Center
        textColor=colors.HexColor('#334155'),
        spaceBefore=4,
        spaceAfter=8
    )

    style_code = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )

    story = []

    # ==========================================
    # PAGE 1: TITLE / COVER PAGE
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("ROLE-BASED INVENTORY AND ASSET MANAGEMENT SYSTEM", style_cover_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph("A Mini Project Report", style_cover_sub))
    story.append(Paragraph("submitted by", style_cover_sub))
    story.append(Spacer(1, 5))
    story.append(Paragraph("APARNA", style_cover_author))
    story.append(Paragraph("(MES25MCA-2010)", style_cover_sub))
    story.append(Spacer(1, 10))
    story.append(Paragraph("to the APJ Abdul Kalam Technological University in partial<br/>fulfilment of the requirements for the award of the Degree<br/>of", style_cover_sub))
    story.append(Paragraph("Master of Computer Applications", style_cover_author))
    story.append(Spacer(1, 15))

    # College Logo
    logo_path = os.path.join("static", "images", "logo.jpg")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=80, height=80))
    else:
        story.append(Spacer(1, 80))

    story.append(Spacer(1, 25))
    story.append(Paragraph("Department of Computer Applications<br/><b>MES College of Engineering</b><br/>Kuttippuram, Malappuram – 679582", style_cover_inst))
    story.append(Spacer(1, 8))
    story.append(Paragraph("October, 2026", style_cover_sub))
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: DECLARATION
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Declaration", style_cover_title))
    story.append(Spacer(1, 15))
    decl_text = (
        "I undersigned hereby declare that the project report <b>\"ROLE-BASED INVENTORY AND ASSET MANAGEMENT SYSTEM\"</b> "
        "submitted for partial fulfilment of the requirements for the award of degree of Master of Computer Applications "
        "of the APJ Abdul Kalam Technological University, Kerala, is a bonafide work done by me under supervision of "
        "<b>Mr. Geevar C Zachariaz</b>, Assistant Professor, Department of Computer Applications. This submission represents "
        "my ideas in my own words and where ideas or words of others have been included, I have adequately and accurately "
        "cited and referenced the original sources. I also declare that I have adhered to ethics of academic honesty and integrity "
        "and have not misrepresented or fabricated any data or idea or fact or source in my submission. I understand that any "
        "violation of the above will be a cause for disciplinary action by the institute and/or the University and can also evoke "
        "penal action from the sources which have thus not been properly cited or from whom proper permission has not been obtained. "
        "This report has not been previously formed the basis for the award of any degree, diploma or similar title of any other University."
    )
    story.append(Paragraph(decl_text, style_body))
    story.append(Spacer(1, 100))

    # Declaration signature
    sig_data = [
        ["", "<b>APARNA</b>"],
        ["", "(MES25MCA-2010)"],
        ["", "24/10/2026"]
    ]
    sig_table = Table(sig_data, colWidths=[300, 187])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(sig_table)
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: CERTIFICATE
    # ==========================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("DEPARTMENT OF COMPUTER APPLICATIONS", style_cover_sub))
    story.append(Paragraph("<b>MES COLLEGE OF ENGINEERING, KUTTIPPURAM</b>", style_cover_sub))
    story.append(Spacer(1, 10))

    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=70, height=70))
    story.append(Spacer(1, 15))

    story.append(Paragraph("CERTIFICATE", style_cover_title))
    story.append(Spacer(1, 15))

    cert_text = (
        "This is to certify that the report entitled <b>ROLE-BASED INVENTORY AND ASSET MANAGEMENT SYSTEM</b> "
        "is a bonafide record of the Mini Project work during the year 2026-27 carried out by <b>APARNA (MES25MCA-2010)</b> "
        "submitted to the APJ Abdul Kalam Technological University, in partial fulfilment of the requirements for the award "
        "of the Master of Computer Applications, under my guidance and supervision. This report in any form has not been "
        "submitted to any other University or Institution for any purpose."
    )
    story.append(Paragraph(cert_text, style_body))
    story.append(Spacer(1, 120))

    cert_sigs = [
        ["<b>Internal Supervisor</b>", "<b>Head of The Department</b>"],
        ["Mr. Geevar C Zachariaz", "Prof. Hyderali K"],
        ["Assistant Professor", "Department of Computer Applications"],
        ["Department of Computer Applications", "MES College of Engineering"],
    ]
    cert_table = Table(cert_sigs, colWidths=[243, 244])
    cert_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(cert_table)
    story.append(PageBreak())

    # ==========================================
    # PAGE 4: ACKNOWLEDGMENT
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Acknowledgment", style_cover_title))
    story.append(Spacer(1, 15))

    ack_text1 = (
        "I express my sincere gratitude to our principal <b>Dr. Rahumathuniza I</b> for permitting and providing "
        "all facilities to carry out this project. I would like to express my sincere gratitude to my internal supervisor, "
        "<b>Mr. Geevar C Zachariaz</b>, for his invaluable guidance, support, and encouragement throughout the development "
        "of this mini project. I also extend my thanks to the Head of the Department <b>Prof. Hyderali K</b> and all faculty "
        "members of the Department of Computer Applications, MES College of Engineering, for providing the necessary resources "
        "and a conducive environment for learning and innovation."
    )
    story.append(Paragraph(ack_text1, style_body))

    ack_text2 = (
        "I am deeply grateful to the organizational staff, administrative coordinators, and fellow students whose experiences "
        "with manual asset tracking, paper requisitions, and cross-departmental communication inspired the vision behind the "
        "Role-Based Inventory and Asset Management System. Their practical insights and user feedback shaped the functional "
        "direction of this project."
    )
    story.append(Paragraph(ack_text2, style_body))

    ack_text3 = (
        "Finally, I thank my family and friends for their unwavering support and motivation throughout my studies. "
        "Above all, I extend my heartfelt gratitude to Almighty for giving me the strength, wisdom, and determination "
        "to complete this project successfully."
    )
    story.append(Paragraph(ack_text3, style_body))
    story.append(Spacer(1, 60))

    ack_sig = [
        ["", "<b>Aparna</b>"],
        ["", "(MES25MCA-2010)"]
    ]
    t_ack = Table(ack_sig, colWidths=[330, 157])
    t_ack.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
    ]))
    story.append(t_ack)
    story.append(PageBreak())

    # ==========================================
    # PAGE 5: ABSTRACT
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Abstract", style_cover_title))
    story.append(Spacer(1, 15))

    abs_p1 = (
        "The <b>Role-Based Inventory and Asset Management System</b> (SecureCorp) is a full-featured web-based platform "
        "engineered to simplify and modernize equipment tracking, departmental requisition lifecycles, maintenance defect reporting, "
        "workload-driven task dispatching, and employee gamification across corporate organizations and academic institutions. "
        "In traditional departments, asset management relies heavily on manual ledgers, disconnected spreadsheets, and informal emails. "
        "This leads to unaccounted hardware loss, lack of stock threshold alerts, delayed approval workflows, and unmonitored equipment returns."
    )
    story.append(Paragraph(abs_p1, style_body))

    abs_p2 = (
        "The primary objective of the system is to establish a secure, centralized portal with strict Role-Based Access Control (RBAC) "
        "segregating Administrator and Employee privileges. The Administrator console provides real-time KPI overview cards, low-stock "
        "warning banners, department creation and restructuring, catalog management with dynamic category addition, single-click "
        "requisition approval or modal-driven rejection with audit feedback, and cross-departmental complaint resolution. "
        "Employees can browse asset availability in real-time, submit requisitions, check in returned equipment with automatic inventory "
        "restoration, file asset damage and cross-departmental service tickets, manage milestone subtasks, and earn recognition badges."
    )
    story.append(Paragraph(abs_p2, style_body))

    abs_p3 = (
        "The application is developed using Python 3.13 with the Django 6.1 framework on the backend and HTML5, CSS3, JavaScript, and "
        "Tailwind CSS on the frontend. SQLite serves as the relational database managed through Django ORM, and Git/GitHub is utilized "
        "for version control. An Agile methodology across four sprints was adopted to guide development from requirement gathering to "
        "production-ready unit and integration testing. Automated test suites verify requisition stock deductions, return replenishments, "
        "and timely badge allocations."
    )
    story.append(Paragraph(abs_p3, style_body))

    abs_p4 = (
        "By eliminating physical paperwork, providing transparent audit trails, and enabling automated stock reconciliation, "
        "the system significantly enhances operational productivity, accountability, and resource utilization."
    )
    story.append(Paragraph(abs_p4, style_body))
    story.append(PageBreak())

    # ==========================================
    # PAGE 6: TABLE OF CONTENTS
    # ==========================================
    story.append(Paragraph("Table of Contents", style_h1))
    story.append(Spacer(1, 8))

    toc_data = [
        ["<b>List of Figures</b>", "<b>viii</b>"],
        ["<b>List of Tables</b>", "<b>ix</b>"],
        ["<b>List of Appendices</b>", "<b>x</b>"],
        ["<b>Chapter 1. Introduction</b>", "<b>1</b>"],
        ["    1.1 Motivation", "1"],
        ["    1.2 Objectives", "2"],
        ["    1.3 Contributions", "2"],
        ["    1.4 Report Organization", "3"],
        ["<b>Chapter 2. System Study</b>", "<b>4</b>"],
        ["    2.1 Existing System", "4"],
        ["    2.2 Proposed System", "5"],
        ["    2.3 Functionalities of the Proposed System", "5"],
        ["<b>Chapter 3. Methodology</b>", "<b>7</b>"],
        ["    3.1 Introduction", "7"],
        ["    3.2 Software Tools", "7"],
        ["    3.3 Module Description", "8"],
        ["        3.3.1 Authentication & Role-Based Access Module", "8"],
        ["        3.3.2 Department Management Module", "8"],
        ["        3.3.3 Asset & Inventory Availability Module", "8"],
        ["        3.3.4 Requisition, Approval, and Return Lifecycle Module", "8"],
        ["        3.3.5 Maintenance & Departmental Complaints Module", "9"],
        ["        3.3.6 Task & Subtask Workflow Engine", "9"],
        ["        3.3.7 Gamification, Badges & Recognition Module", "9"],
        ["    3.4 Workflow of the System", "9"],
        ["        3.4.1 Registration and Authentication", "9"],
        ["        3.4.2 Department & Asset Catalog Setup", "9"],
        ["        3.4.3 Requisition Submission & Validation", "10"],
        ["        3.4.4 Administrative Approval and Rejection", "10"],
        ["        3.4.5 Asset Return & Automated Stock Restoration", "10"],
        ["        3.4.6 Ticket Resolution & Status Updating", "10"],
        ["        3.4.7 Workload Optimization & Task Dispatching", "10"],
        ["        3.4.8 Milestone Checklists & Gamified Badge Granting", "10"],
        ["    3.5 User Stories", "10"],
        ["    3.6 Product Backlog", "12"],
        ["    3.7 Sprint Backlog", "13"],
        ["    3.8 Project Plan", "14"],
        ["    3.9 Database Design", "16"],
        ["<b>Chapter 4. Results and Discussions</b>", "<b>26</b>"],
        ["    4.1 Results", "26"],
        ["    4.2 Discussion", "30"],
        ["<b>Chapter 5. Conclusion and Future Scope</b>", "<b>32</b>"],
        ["    5.1 Conclusion", "32"],
        ["    5.2 Future Scope", "33"],
        ["<b>References</b>", "<b>34</b>"],
        ["<b>Appendix A: Data Flow Diagram</b>", "<b>35</b>"],
        ["<b>Appendix B: Entity–Relationship Diagram</b>", "<b>40</b>"],
        ["<b>Appendix C: Source Code</b>", "<b>41</b>"],
        ["<b>Appendix D: Screenshots</b>", "<b>49</b>"],
    ]

    t_toc = Table(toc_data, colWidths=[410, 77])
    t_toc.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==========================================
    # PAGE 7: LIST OF FIGURES & TABLES
    # ==========================================
    story.append(Paragraph("List of Figures", style_h1))
    story.append(Spacer(1, 6))

    figures_data = [
        ["Figure 4.1: Login Page with Branded Portal and Role Routing", "26"],
        ["Figure 4.2: Admin Command Center Dashboard with Real-Time KPIs", "27"],
        ["Figure 4.3: Department Management Directory & Organization Cards", "28"],
        ["Figure 4.4: Asset Catalog & Availability Level Indicators", "28"],
        ["Figure 4.5: Employee Workspace Dashboard & Active Requisitions", "29"],
        ["Figure 4.6: Requisition Approval, Rejection, and Return Tracker", "29"],
        ["Figure A.1: Level 0 DFD (System Context Diagram)", "35"],
        ["Figure A.2: Level 1 DFD (Employee Requisition & Issue Flow)", "36"],
        ["Figure A.3: Level 2 DFD (Admin Inventory & Asset Allocation)", "37"],
        ["Figure A.4: Level 3 DFD (Requisition Decision & Stock Restoration)", "38"],
        ["Figure A.5: Level 4 DFD (Task Workload Optimization & Badges)", "39"],
        ["Figure B.1: Entity–Relationship Diagram for Inventory, Tasks & Issues", "40"],
        ["Figure D.1: Login page of the system", "49"],
        ["Figure D.2: Admin dashboard with KPI metrics and stock warnings", "50"],
        ["Figure D.3: Department management directory", "50"],
        ["Figure D.4: Asset catalog with availability progress bars", "51"],
        ["Figure D.5: Employee workspace dashboard", "51"],
        ["Figure D.6: Asset requisition queue with Return Check-in", "52"],
        ["Figure D.7: Issue and maintenance ticket hub", "52"],
        ["Figure D.8: Task and subtask milestone management", "53"],
        ["Figure D.9: Awards showcase and company leaderboard", "53"],
    ]
    t_figs = Table(figures_data, colWidths=[410, 77])
    t_figs.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(t_figs)
    story.append(Spacer(1, 15))

    story.append(Paragraph("List of Tables", style_h1))
    story.append(Spacer(1, 6))

    tables_data = [
        ["Table 3.1: Software tools and technologies used for development", "7"],
        ["Table 3.2: User stories for inventory, requisition, and workflow moderation", "10"],
        ["Table 3.3: Product backlog with priorities and estimated effort", "12"],
        ["Table 3.4: Sprint backlog and completion status", "13"],
        ["Table 3.5: Project schedule and task allocation", "14"],
        ["Table 3.6: User table schema and sample data", "16"],
        ["Table 3.7: Department table schema and sample data", "17"],
        ["Table 3.8: Category table schema and sample data", "18"],
        ["Table 3.9: Asset table schema and sample data", "19"],
        ["Table 3.10: Asset request table schema and sample data", "20"],
        ["Table 3.11: Task and SubTask table schema and sample data", "21"],
        ["Table 3.12: Maintenance and Department Issue table schema and sample data", "23"],
        ["Table 3.13: Award and Badge table schema and sample data", "25"],
    ]
    t_tabs = Table(tables_data, colWidths=[410, 77])
    t_tabs.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(t_tabs)
    story.append(PageBreak())

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    story.append(Paragraph("Chapter 1. Introduction", style_h1))
    story.append(Spacer(1, 8))

    c1_p1 = (
        "Asset and inventory management is a mission-critical operational requirement for modern enterprises, research laboratories, "
        "and educational institutions. Organizations maintain extensive fleets of IT hardware, office workstations, networking devices, "
        "lab instrumentation, and shared consumables distributed across various departments. Managing these assets involves diverse "
        "activities including inventory intake, departmental allocation, employee requisition processing, condition inspections, "
        "cross-departmental issue resolution, preventative maintenance, task delegation, and return stock reconciliation. "
        "When these operations are performed through ad-hoc manual procedures, maintaining transparency and fiscal accountability becomes exceedingly complex."
    )
    story.append(Paragraph(c1_p1, style_body))

    c1_p2 = (
        "This project proposes the <b>Role-Based Inventory and Asset Management System</b> (SecureCorp), a comprehensive web application "
        "that centralizes the lifecycle of corporate and departmental assets. The system implements granular role-based separation for "
        "Administrators and Employees, tailoring features to their specific operational responsibilities. Built with Python and Django "
        "on the server side and HTML5, CSS3, JavaScript, and Tailwind CSS on the client side, the application delivers clean, responsive, "
        "and intuitive dashboards for effortless inventory oversight."
    )
    story.append(Paragraph(c1_p2, style_body))

    story.append(Paragraph("1.1 Motivation", style_h2))
    c1_mot = (
        "The motivation for this project stems from recurring deficiencies observed in manual inventory administration. In typical "
        "organizations, asset requests are submitted across fragmented channels such as email threads, phone messages, or paper forms. "
        "Administrators must manually check stock levels, verify whether an employee's department is authorized, approve requests, and record "
        "the dispatch in standalone spreadsheets. When equipment is returned, records are frequently overlooked, causing discrepancies between "
        "recorded and physical inventory counts. Furthermore, when equipment breaks down or requires repairs, reporting is delayed due to "
        "the lack of a dedicated issue ticketing mechanism. These manual bottlenecks motivated the creation of a unified digital solution "
        "that provides real-time stock visibility, enforces requisition lifecycles, restores inventory automatically upon return, "
        "and optimizes staff task assignments."
    )
    story.append(Paragraph(c1_mot, style_body))

    story.append(Paragraph("1.2 Objectives", style_h2))
    story.append(Paragraph("The primary objectives of the Role-Based Inventory and Asset Management System are:", style_body))
    story.append(Paragraph("• Provide secure, role-based authentication and navigation routing for Administrators and Employees.", style_bullet))
    story.append(Paragraph("• Enable real-time inventory tracking with automatic low-stock warnings and availability percentages.", style_bullet))
    story.append(Paragraph("• Deliver complete Department Management CRUD to organize staff and asset allocations.", style_bullet))
    story.append(Paragraph("• Establish an end-to-end requisition lifecycle with pending queues, approval checks, rejection notes, and return check-ins.", style_bullet))
    story.append(Paragraph("• Implement automated inventory restoration that replenishes available stock immediately upon asset return.", style_bullet))
    story.append(Paragraph("• Facilitate dual-channel issue tracking for physical asset defects and inter-departmental service requests.", style_bullet))
    story.append(Paragraph("• Support workload-optimized task assignment based on employee skills and pending workload hours.", style_bullet))
    story.append(Paragraph("• Integrate gamification through achievement badges and milestone recognition for on-time task completion.", style_bullet))
    story.append(Paragraph("• Provide automated data export utilities generating formal PDF and Excel inventory audits.", style_bullet))

    story.append(Paragraph("1.3 Contributions", style_h2))
    story.append(Paragraph("The key technical contributions of this project include:", style_body))
    story.append(Paragraph("• <b>Centralized Enterprise Web Platform:</b> Replaces scattered spreadsheets and paper requisition slips with a secure Django portal.", style_bullet))
    story.append(Paragraph("• <b>Stock Integrity & Automated Reconciliation:</b> Ensures available quantities never go negative and automatically restores stock upon verified return.", style_bullet))
    story.append(Paragraph("• <b>Workload Optimization Algorithm:</b> Queries eligible employees matching required task skills and auto-assigns tasks to the team member with the lowest pending workload.", style_bullet))
    story.append(Paragraph("• <b>Dual-Layer Ticketing:</b> Provides asset-specific maintenance logging alongside cross-departmental collaboration tickets.", style_bullet))
    story.append(Paragraph("• <b>Automated Badge Generation:</b> Listens for completed subtask checklists and dynamically grants timely completion awards.", style_bullet))

    story.append(Paragraph("1.4 Report Organization", style_h2))
    c1_org = (
        "The remainder of this report is organized as follows: Chapter 2 reviews the existing system and details the proposed system study. "
        "Chapter 3 explains the Agile methodology, software tools, module specifications, user stories, product backlogs, sprint cycles, "
        "and database design tables. Chapter 4 presents the experimental results, interface walkthroughs, access control analysis, and limitations. "
        "Chapter 5 provides concluding remarks and outlines future enhancements. The appendices contain the Data Flow Diagrams, Entity-Relationship Diagram, "
        "essential source code listings, and system screenshots."
    )
    story.append(Paragraph(c1_org, style_body))
    story.append(PageBreak())

    # ==========================================
    # CHAPTER 2: SYSTEM STUDY
    # ==========================================
    story.append(Paragraph("Chapter 2. System Study", style_h1))
    story.append(Spacer(1, 8))

    c2_intro = (
        "A comprehensive system study was conducted to evaluate how inventory, requisitions, departmental equipment allocations, "
        "and maintenance tasks are currently handled. The study identified key vulnerabilities in legacy processes and established "
        "the functional baseline for the proposed automated platform."
    )
    story.append(Paragraph(c2_intro, style_body))

    story.append(Paragraph("2.1 Existing System", style_h2))
    story.append(Paragraph("In most conventional organizations, inventory tracking suffers from several inherent limitations:", style_body))
    story.append(Paragraph("• <b>Decentralized Record Keeping:</b> Asset registers are stored in offline Excel spreadsheets across individual departments, leading to data silos and inconsistencies.", style_bullet))
    story.append(Paragraph("• <b>Paper Requisition Slips:</b> Employees submit paper forms or email threads to request equipment, creating lengthy turnaround times and lost paperwork.", style_bullet))
    story.append(Paragraph("• <b>Untracked Returns:</b> Once an asset is issued, there is no systematic reminder or tracking mechanism to confirm when the item is returned, resulting in unaccounted inventory shrinkage.", style_bullet))
    story.append(Paragraph("• <b>No Stock Depletion Alerts:</b> Administrators only discover stockouts when an item is entirely exhausted, causing critical procurement delays.", style_bullet))
    story.append(Paragraph("• <b>Fragmented Defect Reporting:</b> Broken equipment is reported verbally or through email without priority categorization or resolution audit trails.", style_bullet))

    story.append(Paragraph("2.2 Proposed System", style_h2))
    story.append(Paragraph("The proposed system provides a unified web solution with the following architectural advantages:", style_body))
    story.append(Paragraph("• <b>Real-Time Inventory Catalog:</b> Displays live quantities, availability percentages, and color-coded stock health badges.", style_bullet))
    story.append(Paragraph("• <b>Dynamic Requisition Lifecycle:</b> Enforces a strict Pending → Approved / Rejected → Returned workflow with administrative notes and timestamp audits.", style_bullet))
    story.append(Paragraph("• <b>Automated Stock Replenishment:</b> Restores available stock immediately when an item is checked back in as Returned.", style_bullet))
    story.append(Paragraph("• <b>Department Isolation & Collaboration:</b> Allows departments to manage their own assets while enabling cross-departmental issue tickets.", style_bullet))
    story.append(Paragraph("• <b>Workload-Balanced Task Dispatching:</b> Calculates employee task loads and auto-assigns work to balance operational capacity.", style_bullet))

    story.append(Paragraph("2.3 Functionalities of the Proposed System", style_h2))
    story.append(Paragraph("<b>Administrator Privileges:</b>", style_h3))
    story.append(Paragraph("• Monitor organizational KPIs including total assets, low-stock alerts, pending requests, and open tickets.", style_bullet))
    story.append(Paragraph("• Create, modify, and delete departments, categories, and inventory assets.", style_bullet))
    story.append(Paragraph("• Review, approve, or reject employee equipment requisitions with formal administrative feedback.", style_bullet))
    story.append(Paragraph("• Dispatch tasks with milestone checklists or utilize automated workload-based assignment.", style_bullet))
    story.append(Paragraph("• Review and update maintenance tickets and cross-departmental complaints.", style_bullet))
    story.append(Paragraph("• Grant custom achievement badges and export formal PDF and Excel audit reports.", style_bullet))

    story.append(Paragraph("<b>Employee Privileges:</b>", style_h3))
    story.append(Paragraph("• Browse the live asset catalog and submit requisitions with requested quantity and purpose.", style_bullet))
    story.append(Paragraph("• Track requisition status and check in borrowed equipment via the Return Asset action.", style_bullet))
    story.append(Paragraph("• Report hardware damage or submit assistance requests to other departments.", style_bullet))
    story.append(Paragraph("• Manage assigned tasks by checking off interactive milestone checklists.", style_bullet))
    story.append(Paragraph("• View earned achievement badges and compete on the organizational leaderboard.", style_bullet))
    story.append(PageBreak())

    # ==========================================
    # CHAPTER 3: METHODOLOGY
    # ==========================================
    story.append(Paragraph("Chapter 3. Methodology", style_h1))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.1 Introduction", style_h2))
    c3_intro = (
        "An Agile development methodology was selected for developing the Role-Based Inventory and Asset Management System. "
        "Agile promotes iterative progression, continuous integration, stakeholder feedback, and adaptable sprint planning. "
        "The project was executed across four distinct sprints spanning 10 weeks, focusing sequentially on authentication, "
        "asset catalog & department management, requisition & return workflows, and ticketing, tasks & gamification."
    )
    story.append(Paragraph(c3_intro, style_body))

    story.append(Paragraph("3.2 Software Tools", style_h2))
    story.append(Paragraph("Table 3.1 lists the software tools, frameworks, and runtime environments utilized during development.", style_body))

    tools_table_data = [
        ["Component", "Tool / Technology", "Version / Details"],
        ["Operating System", "Microsoft Windows 11 Pro", "64-bit Architecture"],
        ["Programming Language", "Python", "Version 3.13"],
        ["Backend Web Framework", "Django", "Version 6.1 (MTV Pattern)"],
        ["Frontend Technologies", "HTML5, CSS3, JavaScript", "ES6+ Standards"],
        ["CSS Styling Framework", "Tailwind CSS", "Modern Utility-First UI"],
        ["Database Management", "SQLite 3", "Integrated via Django ORM"],
        ["Development Environment", "Visual Studio Code", "IDE with Python Extension"],
        ["Version Control", "Git & GitHub", "Feature-Branch Workflow"],
        ["Reporting Engines", "ReportLab & OpenPyXL", "Automated PDF and Excel Exports"],
    ]
    t_tools = Table(tools_table_data, colWidths=[120, 160, 207])
    t_tools.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_tools)
    story.append(Paragraph("Table 3.1: Software tools and technologies used for development", style_caption))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.3 Module Description", style_h2))
    story.append(Paragraph("The system is decomposed into seven decoupled functional modules to guarantee scalability and maintainability:", style_body))

    story.append(Paragraph("<b>3.3.1 Authentication & Role-Based Access Module:</b> Enforces secure session management and role-based URL protection. Directs administrators to the executive dashboard and employees to the user self-service dashboard upon login.", style_body))
    story.append(Paragraph("<b>3.3.2 Department Management Module:</b> Provides full CRUD operations for organizational divisions, tracking departmental headcount, allocated equipment counts, and pending issue tickets.", style_body))
    story.append(Paragraph("<b>3.3.3 Asset & Inventory Availability Module:</b> Manages asset records including name, category, department, total units, available units, and low-stock threshold. Dynamically flags stock depletion.", style_body))
    story.append(Paragraph("<b>3.3.4 Requisition, Approval, and Return Lifecycle Module:</b> Coordinates employee checkouts, verifies stock availability, decrements available inventory upon approval, and restores stock upon verified return.", style_body))
    story.append(Paragraph("<b>3.3.5 Maintenance & Departmental Complaints Module:</b> Manages asset repair tickets with severe damage flags and handles inter-departmental service requests with priority rankings.", style_body))
    story.append(Paragraph("<b>3.3.6 Task & Subtask Workflow Engine:</b> Facilitates task creation with milestone checklists and implements workload-balancing auto-assignment based on employee skills and pending workload hours.", style_body))
    story.append(Paragraph("<b>3.3.7 Gamification, Badges & Recognition Module:</b> Automatically rewards on-time task completions with achievement badges and provides an executive portal to grant custom organizational honors.", style_body))
    story.append(PageBreak())

    # ==========================================
    # USER STORIES TABLE
    # ==========================================
    story.append(Paragraph("3.5 User Stories", style_h2))
    story.append(Paragraph("Table 3.2 outlines the user stories defined during requirement elicitation across all operational roles.", style_body))

    stories_data = [
        ["ID", "Role", "I want to...", "So that I can..."],
        ["1", "User", "Log into the application securely", "Access my role-specific dashboard"],
        ["2", "User", "Register a new employee profile", "Obtain authorized system credentials"],
        ["3", "Admin", "View KPI metric cards on dashboard", "Monitor organizational asset health"],
        ["4", "Admin", "Receive low-stock visual alerts", "Initiate timely procurement orders"],
        ["5", "Admin", "Create and edit departments", "Organize institutional divisions"],
        ["6", "Admin", "Delete empty departments safely", "Maintain accurate organizational charts"],
        ["7", "Admin", "Add new assets with thresholds", "Track inventory units in real-time"],
        ["8", "Admin", "Create asset categories via modal", "Classify equipment without page reloads"],
        ["9", "Admin", "Review pending asset requisitions", "Approve or reject equipment requests"],
        ["10", "Admin", "Provide rejection feedback notes", "Explain denial decisions to employees"],
        ["11", "Admin", "Dispatch tasks with auto-assignment", "Balance workload across skilled staff"],
        ["12", "Admin", "Grant custom achievement badges", "Recognize outstanding staff performance"],
        ["13", "Admin", "Export PDF and Excel reports", "Present official audits to management"],
        ["14", "Admin", "Reassign employee departments", "Update personnel restructuring"],
        ["15", "Employee", "Browse available inventory assets", "Identify items available for checkout"],
        ["16", "Employee", "Submit an asset checkout request", "Obtain required equipment for work"],
        ["17", "Employee", "Track the status of my requests", "Know when items are approved"],
        ["18", "Employee", "Click 'Return Asset' on approved items", "Check back in equipment and restore stock"],
        ["19", "Employee", "Report asset defect or damage", "Notify maintenance technicians immediately"],
        ["20", "Employee", "Raise cross-department issue tickets", "Request support from other units"],
        ["21", "Employee", "Update status of received tickets", "Resolve issues assigned to my department"],
        ["22", "Employee", "Check off milestone subtasks", "Track progress toward task completion"],
        ["23", "Employee", "Complete tasks before deadlines", "Earn automated timely completion awards"],
        ["24", "Employee", "View my earned badges and medals", "Track my professional achievements"],
        ["25", "Employee", "Filter asset catalog by category", "Quickly locate specific equipment types"],
    ]
    t_stories = Table(stories_data, colWidths=[24, 60, 203, 200])
    t_stories.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_stories)
    story.append(Paragraph("Table 3.2: User stories for inventory, requisition, and workflow moderation", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PRODUCT BACKLOG & SPRINT BACKLOG
    # ==========================================
    story.append(Paragraph("3.6 Product Backlog", style_h2))
    story.append(Paragraph("Table 3.3 presents the complete product backlog prioritized by operational criticality.", style_body))

    backlog_data = [
        ["ID", "Feature / Task Name", "Priority", "Est. Hours", "Status"],
        ["1", "System Requirements & Feasibility Study", "High", "8", "Completed"],
        ["2", "Database Schema Design & Normalization", "High", "10", "Completed"],
        ["3", "UI/UX Mockups & Tailwind Design System", "Medium", "8", "Completed"],
        ["4", "Django Project Initialization & Architecture", "High", "6", "Completed"],
        ["5", "Custom User Model & Role-Based Routing", "High", "8", "Completed"],
        ["6", "Registration & Login Views with Validation", "High", "8", "Completed"],
        ["7", "Admin Dashboard Shell & KPI Calculation", "High", "10", "Completed"],
        ["8", "Department Management CRUD Implementation", "High", "10", "Completed"],
        ["9", "Asset Catalog & Category Management Views", "High", "12", "Completed"],
        ["10", "Inline Category Creation Modal via AJAX", "Medium", "6", "Completed"],
        ["11", "Low-Stock Calculation & Alert Warning Banner", "High", "6", "Completed"],
        ["12", "Employee Dashboard & Available Asset Requisition", "High", "10", "Completed"],
        ["13", "Asset Request Processing & Stock Validation", "High", "8", "Completed"],
        ["14", "Administrative Approval & Rejection Modal", "High", "8", "Completed"],
        ["15", "Return Asset Workflow & Auto Stock Restoration", "High", "8", "Completed"],
        ["16", "Asset Defect / Maintenance Reporting Engine", "High", "8", "Completed"],
        ["17", "Cross-Departmental Issue Ticketing Center", "High", "10", "Completed"],
        ["18", "Departmental Ticket Status Updating Forms", "Medium", "6", "Completed"],
        ["19", "Task Management & Milestone Subtask Checklist", "High", "10", "Completed"],
        ["20", "Workload Balancing Auto-Assignment Algorithm", "High", "10", "Completed"],
        ["21", "Interactive Subtask Toggling & Status Sync", "High", "8", "Completed"],
        ["22", "Automated Timely Completion Badge Engine", "High", "8", "Completed"],
        ["23", "Executive Custom Award Granting Interface", "Medium", "6", "Completed"],
        ["24", "PDF Inventory Report Generation Engine", "Medium", "8", "Completed"],
        ["25", "Excel Inventory Export Engine via OpenPyXL", "Medium", "6", "Completed"],
        ["26", "Automated Unit & Integration Test Suite", "High", "12", "Completed"],
    ]
    t_backlog = Table(backlog_data, colWidths=[24, 253, 60, 70, 80])
    t_backlog.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_backlog)
    story.append(Paragraph("Table 3.3: Product backlog with priorities and estimated effort", style_caption))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.7 Sprint Backlog", style_h2))
    story.append(Paragraph("Table 3.4 outlines the distribution of tasks across four agile development sprints.", style_body))

    sprint_data = [
        ["Sprint", "Core Focus & Deliverables", "Status"],
        ["Sprint 1", "Requirements, Database Architecture, Custom User Authentication, and UI Layout Setup", "Completed"],
        ["Sprint 2", "Department CRUD, Asset Catalog, Category Modal, and Live Stock Availability Tracking", "Completed"],
        ["Sprint 3", "Requisition Queue, Approval/Rejection Decisioning, and Asset Return Stock Replenishment", "Completed"],
        ["Sprint 4", "Maintenance Ticketing, Workload Task Auto-Assignment, Badges, and Automated Test Suite", "Completed"],
    ]
    t_sprint = Table(sprint_data, colWidths=[60, 347, 80])
    t_sprint.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_sprint)
    story.append(Paragraph("Table 3.4: Sprint backlog and completion status", style_caption))
    story.append(PageBreak())

    # ==========================================
    # PROJECT PLAN & TIMELINE TABLE
    # ==========================================
    story.append(Paragraph("3.8 Project Plan", style_h2))
    story.append(Paragraph("Table 3.5 presents the project development timeline, milestone allocations, and completion dates.", style_body))

    plan_data = [
        ["User Story ID", "Sprint Phase", "Start Date", "End Date", "Duration", "Status"],
        ["1 - 4", "Sprint 1: Architecture & Auth", "24/07/2026", "07/08/2026", "15 Days", "Completed"],
        ["5 - 8", "Sprint 1: Database & Layout", "08/08/2026", "14/08/2026", "7 Days", "Completed"],
        ["9 - 11", "Sprint 2: Departments & Catalog", "15/08/2026", "28/08/2026", "14 Days", "Completed"],
        ["12 - 14", "Sprint 2: Stock Tracking & Alerts", "29/08/2026", "05/09/2026", "8 Days", "Completed"],
        ["15 - 18", "Sprint 3: Requisition Lifecycle", "06/09/2026", "19/09/2026", "14 Days", "Completed"],
        ["19 - 21", "Sprint 3: Returns & Restoration", "20/09/2026", "26/09/2026", "7 Days", "Completed"],
        ["22 - 24", "Sprint 4: Issues & Workload Engine", "27/09/2026", "08/10/2026", "12 Days", "Completed"],
        ["25 - 26", "Sprint 4: Testing & Documentation", "09/10/2026", "22/10/2026", "14 Days", "Completed"],
    ]
    t_plan = Table(plan_data, colWidths=[70, 177, 75, 75, 50, 40])
    t_plan.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_plan)
    story.append(Paragraph("Table 3.5: Project schedule and task allocation", style_caption))
    story.append(Spacer(1, 10))

    # ==========================================
    # DATABASE DESIGN TABLES
    # ==========================================
    story.append(Paragraph("3.9 Database Design", style_h2))
    story.append(Paragraph("The system utilizes an SQLite relational database managed via Django ORM. The detailed table schemas and sample data are defined below.", style_body))

    # User Table
    story.append(Paragraph("<b>3.9.1 User Table</b> (Table 3.6): Stores employee and administrator credentials, roles, and department affiliations.", style_body))
    user_schema = [
        ["Field Name", "Data Type", "Key / Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique user identifier", "1"],
        ["username", "VARCHAR(150)", "UNIQUE, NOT NULL", "Login credential", "aparna_admin"],
        ["password", "VARCHAR(128)", "NOT NULL", "PBKDF2 SHA256 hashed password", "pbkdf2_sha256$..."],
        ["first_name", "VARCHAR(150)", "NULL", "First name of user", "Aparna"],
        ["last_name", "VARCHAR(150)", "NULL", "Last name of user", "Menon"],
        ["email", "VARCHAR(254)", "NOT NULL", "Official email address", "aparna@securecorp.com"],
        ["role", "VARCHAR(10)", "NOT NULL, Choice", "ADMIN or EMPLOYEE", "ADMIN"],
        ["department_id", "BIGINT", "FK, NULL", "Foreign key to Department", "2 (Engineering)"],
        ["is_active", "BOOLEAN", "NOT NULL", "Account activation flag", "1 (True)"],
        ["date_joined", "DATETIME", "NOT NULL", "Timestamp of account creation", "2026-08-01 10:00:00"],
    ]
    t_user = Table(user_schema, colWidths=[80, 85, 115, 120, 87])
    t_user.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(t_user)
    story.append(Paragraph("Table 3.6: User table schema and sample data", style_caption))
    story.append(PageBreak())

    # Department & Category Tables
    story.append(Paragraph("<b>3.9.2 Department Table</b> (Table 3.7): Stores institutional departments.", style_body))
    dept_schema = [
        ["Field Name", "Data Type", "Key / Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Department unique ID", "1"],
        ["name", "VARCHAR(100)", "UNIQUE, NOT NULL", "Department title", "IT Engineering"],
        ["description", "TEXT", "BLANK", "Department responsibilities", "Handles compute & infra"],
    ]
    t_dept = Table(dept_schema, colWidths=[80, 85, 115, 120, 87])
    t_dept.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_dept)
    story.append(Paragraph("Table 3.7: Department table schema and sample data", style_caption))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>3.9.3 Category Table</b> (Table 3.8): Stores equipment taxonomy classifications.", style_body))
    cat_schema = [
        ["Field Name", "Data Type", "Key / Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Category unique ID", "1"],
        ["name", "VARCHAR(100)", "NOT NULL", "Category classification", "Laptops & Computing"],
        ["description", "TEXT", "BLANK", "Category notes", "Portable development machines"],
    ]
    t_cat = Table(cat_schema, colWidths=[80, 85, 115, 120, 87])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_cat)
    story.append(Paragraph("Table 3.8: Category table schema and sample data", style_caption))
    story.append(Spacer(1, 8))

    # Asset Table
    story.append(Paragraph("<b>3.9.4 Asset Table</b> (Table 3.9): Stores physical equipment items, quantities, and thresholds.", style_body))
    asset_schema = [
        ["Field Name", "Data Type", "Key / Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Unique asset ID", "101"],
        ["name", "VARCHAR(200)", "NOT NULL", "Asset name or model", "ThinkPad T14s Gen 3"],
        ["category_id", "BIGINT", "FK, NOT NULL", "Links to Category", "1 (Laptops)"],
        ["department_id", "BIGINT", "FK, NULL", "Assigned Department", "1 (IT Engineering)"],
        ["total_quantity", "INTEGER", "NOT NULL, min 0", "Total fleet count", "25"],
        ["available_quantity", "INTEGER", "NOT NULL, min 0", "Current unallocated stock", "18"],
        ["low_stock_threshold", "INTEGER", "NOT NULL, default 5", "Depletion alert trigger", "5"],
        ["description", "TEXT", "BLANK", "Hardware specifications", "AMD Ryzen 7, 32GB RAM"],
    ]
    t_asset = Table(asset_schema, colWidths=[90, 80, 115, 115, 87])
    t_asset.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_asset)
    story.append(Paragraph("Table 3.9: Asset table schema and sample data", style_caption))
    story.append(PageBreak())

    # AssetRequest Table
    story.append(Paragraph("<b>3.9.5 Asset Request Table</b> (Table 3.10): Tracks requisition lifecycles and returns.", style_body))
    req_schema = [
        ["Field Name", "Data Type", "Key / Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Requisition ID", "501"],
        ["employee_id", "BIGINT", "FK, NOT NULL", "Employee who requested", "2 (emp_john)"],
        ["asset_id", "BIGINT", "FK, NOT NULL", "Asset requested", "101 (ThinkPad T14s)"],
        ["quantity", "INTEGER", "NOT NULL, default 1", "Requested units", "2"],
        ["status", "VARCHAR(10)", "NOT NULL, Choice", "PENDING/APPROVED/REJECTED/RETURNED", "APPROVED"],
        ["notes", "TEXT", "BLANK", "Employee checkout justification", "Field audit deployment"],
        ["admin_notes", "TEXT", "BLANK", "Administrator feedback", "Approved for 14 days"],
        ["request_date", "DATETIME", "NOT NULL, Auto", "Submission timestamp", "2026-09-10 09:30:00"],
        ["response_date", "DATETIME", "NULL", "Approval/Rejection time", "2026-09-10 11:15:00"],
        ["return_date", "DATETIME", "NULL", "Check-in return timestamp", "2026-09-24 16:00:00"],
    ]
    t_req = Table(req_schema, colWidths=[80, 85, 115, 120, 87])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_req)
    story.append(Paragraph("Table 3.10: Asset request table schema and sample data", style_caption))
    story.append(Spacer(1, 8))

    # Tasks & Issues Tables
    story.append(Paragraph("<b>3.9.6 Task and Subtask Tables</b> (Table 3.11): Workload tasks and milestone checklist records.", style_body))
    task_schema = [
        ["Field Name", "Data Type", "Key / Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Task ID", "301"],
        ["title", "VARCHAR(200)", "NOT NULL", "Task title", "Quarterly Server Audit"],
        ["assigned_to_id", "BIGINT", "FK, NULL", "Assigned employee", "2 (emp_john)"],
        ["workload_hours", "INTEGER", "NOT NULL, min 1", "Estimated hours", "4"],
        ["priority", "VARCHAR(10)", "NOT NULL, Choice", "LOW/MEDIUM/HIGH/URGENT", "HIGH"],
        ["status", "VARCHAR(20)", "NOT NULL, Choice", "PENDING/IN_PROGRESS/COMPLETED", "COMPLETED"],
        ["deadline", "DATETIME", "NOT NULL", "Completion target time", "2026-10-15 17:00:00"],
        ["completed_at", "DATETIME", "NULL", "Actual completion time", "2026-10-14 15:30:00"],
    ]
    t_task = Table(task_schema, colWidths=[80, 85, 115, 120, 87])
    t_task.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_task)
    story.append(Paragraph("Table 3.11: Task and SubTask table schema and sample data", style_caption))
    story.append(PageBreak())

    # Maintenance & Award Tables
    story.append(Paragraph("<b>3.9.7 Maintenance and Department Issue Tables</b> (Table 3.12): Defect logs and inter-department tickets.", style_body))
    issue_schema = [
        ["Field Name", "Data Type", "Key / Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Issue ID", "401"],
        ["asset_id", "BIGINT", "FK, NOT NULL", "Associated defective asset", "101 (ThinkPad)"],
        ["reported_by_id", "BIGINT", "FK, NOT NULL", "Reporter user ID", "2 (emp_john)"],
        ["priority", "VARCHAR(10)", "NOT NULL, Choice", "LOW/MEDIUM/HIGH/URGENT", "HIGH"],
        ["is_damaged", "BOOLEAN", "NOT NULL, default False", "Severe physical damage flag", "1 (True)"],
        ["status", "VARCHAR(20)", "NOT NULL, Choice", "REPORTED/IN_PROGRESS/RESOLVED", "RESOLVED"],
        ["description", "TEXT", "NOT NULL", "Defect description", "Keyboard water damage"],
        ["resolution_notes", "TEXT", "BLANK", "Technician action notes", "Replaced top keyboard assembly"],
    ]
    t_issue = Table(issue_schema, colWidths=[80, 85, 115, 120, 87])
    t_issue.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_issue)
    story.append(Paragraph("Table 3.12: Maintenance and Department Issue table schema and sample data", style_caption))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>3.9.8 Award Table</b> (Table 3.13): Stores earned badges and gamification achievements.", style_body))
    award_schema = [
        ["Field Name", "Data Type", "Key / Constraint", "Description", "Sample Data"],
        ["id", "INTEGER", "PK, Auto Increment", "Award ID", "1"],
        ["employee_id", "BIGINT", "FK, NOT NULL", "Rewarded employee", "2 (emp_john)"],
        ["badge_icon", "VARCHAR(50)", "NOT NULL, default '⭐'", "Symbolic badge emoji", "🏆"],
        ["name", "VARCHAR(100)", "NOT NULL", "Honorary award title", "Timely Finish: Server Audit"],
        ["description", "TEXT", "BLANK", "Achievement justification", "Completed audit 1 day early"],
        ["awarded_at", "DATETIME", "NOT NULL, Auto", "Timestamp awarded", "2026-10-14 15:30:00"],
    ]
    t_award = Table(award_schema, colWidths=[80, 85, 115, 120, 87])
    t_award.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_award)
    story.append(Paragraph("Table 3.13: Award and Badge table schema and sample data", style_caption))
    story.append(PageBreak())

    # ==========================================
    # CHAPTER 4: RESULTS AND DISCUSSIONS
    # ==========================================
    story.append(Paragraph("Chapter 4. Results and Discussions", style_h1))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.1 Results", style_h2))
    c4_p1 = (
        "The Role-Based Inventory and Asset Management System was successfully developed, integrated, and verified module-by-module. "
        "The application provides a responsive, role-differentiated experience with customized operational views for Administrators and Employees."
    )
    story.append(Paragraph(c4_p1, style_body))

    story.append(Paragraph("<b>4.1.1 Authentication & Registration Portal:</b> Users authenticate via a styled portal. Unauthenticated users are redirected from protected views. New team members register with their desired credentials, assigned department, and specialized skills. Upon successful login, the application evaluates the user's role and automatically redirects them to the Admin Console or Employee Workspace.", style_body))
    story.append(Paragraph("<b>4.1.2 Administrator Executive Command Center:</b> The Admin Dashboard delivers six real-time metric cards: Total Assets, Low-Stock Depletions, Pending Requests, Active Tasks, Open Issues, and Total Departments. A prominent red warning banner highlights assets currently at or below their restock threshold with direct links to replenish stock. The pending requests queue allows single-click approvals or modal-driven rejections.", style_body))
    story.append(Paragraph("<b>4.1.3 Department Management Directory:</b> Administrators manage organizational divisions through dedicated list, add, edit, detail, and delete views. Each department card displays its total staff headcount, assigned assets, and open issue tickets. Deleting a department safely dissociates attached employees and assets without data loss.", style_body))
    story.append(Paragraph("<b>4.1.4 Live Asset Catalog & Stock Availability:</b> The asset catalog presents real-time inventory counts with visual progress bars (available vs total quantity) and status pills (In Stock in emerald, Low Stock in amber, Out of Stock in rose). Administrators can modify specifications or delete assets, while employees can initiate immediate checkout requisitions.", style_body))
    story.append(Paragraph("<b>4.1.5 Requisition Lifecycle & Automated Stock Restoration:</b> The requisition pipeline tracks requests across Pending, Approved, Rejected, and Returned states. When an administrator approves a request, the system deducts the requested quantity from available stock. When an employee checks back in an approved asset via the 'Return Asset' action, the system immediately replenishes available stock back to inventory.", style_body))
    story.append(Paragraph("<b>4.1.6 Issue & Maintenance Ticketing:</b> Provides two distinct ticket streams: Asset Maintenance (reporting physical damage and equipment defects) and Cross-Department Tickets (inter-departmental assistance). Authorized department staff and administrators can update ticket statuses to In Progress, Resolved, or Closed with technician notes.", style_body))
    story.append(Paragraph("<b>4.1.7 Task Workload Balancing & Gamification Badges:</b> Administrators can manually dispatch tasks or enable the Workload Optimization algorithm, which queries employees possessing the required skill and auto-assigns the task to the individual with the lowest pending workload hours. Employees check off milestone subtasks, and on-time task completion automatically triggers achievement badge creation.", style_body))

    story.append(Paragraph("4.2 Discussion", style_h2))
    story.append(Paragraph("<b>4.2.1 Analysis of Results:</b> The implementation eliminates the common failure points of traditional inventory systems. By enforcing atomic database transactions and strict stock validation, the system prevents over-allocation. Automated check-in restores stock seamlessly, ensuring records always match physical inventory.", style_body))
    story.append(Paragraph("<b>4.2.2 Role-Based Access Control:</b> Custom template tags and Django decorators guarantee that employees cannot access administrative CRUD views or bypass authorization checks. Attempts to access unauthorized routes trigger automatic security redirects.", style_body))
    story.append(Paragraph("<b>4.2.3 Agile Development & Automated Testing:</b> Developing across four structured sprints ensured rapid feedback cycles. A comprehensive automated test suite consisting of 9 end-to-end test cases in <code>inventory/tests.py</code> verified authentication, department CRUD, requisition stock deduction and replenishment, issue tracking, and workload task assignment with 100% pass rate.", style_body))
    story.append(Paragraph("<b>4.2.4 Limitations:</b> Email and SMS notifications are not currently integrated, requiring users to log in to inspect status changes. Real-time chat between borrowers and administrators is currently ticket-based. Automated barcode/RFID scanner hardware integration is planned for future iterations.", style_body))
    story.append(PageBreak())

    # ==========================================
    # CHAPTER 5: CONCLUSION AND FUTURE SCOPE
    # ==========================================
    story.append(Paragraph("Chapter 5. Conclusion and Future Scope", style_h1))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.1 Conclusion", style_h2))
    c5_concl = (
        "The <b>Role-Based Inventory and Asset Management System</b> successfully centralizes equipment requisitions, departmental tracking, "
        "preventative maintenance, workload balancing, and employee recognition into a unified, secure web platform. By replacing manual paperwork "
        "and fragmented spreadsheets with an automated Django solution, the system ensures real-time stock visibility, enforces accountability "
        "for issued assets, and eliminates stockout surprises through automated threshold warnings. "
        "The integration of workload optimization balances operational duties across skilled staff, while gamification incentives foster timely task delivery. "
        "The project demonstrates how modern web engineering and relational database design can solve complex resource management challenges in academic and corporate settings."
    )
    story.append(Paragraph(c5_concl, style_body))

    story.append(Paragraph("5.2 Future Scope", style_h2))
    story.append(Paragraph("The system provides a robust architectural foundation that can be expanded with the following capabilities in future releases:", style_body))
    story.append(Paragraph("• <b>Barcode & QR Code Scanning:</b> Implement mobile camera scanning for instant asset checkout, check-in, and rapid physical audits.", style_bullet))
    story.append(Paragraph("• <b>Automated Email & Push Notifications:</b> Send instant alerts when assets are approved, low stock thresholds are breached, or task deadlines approach.", style_bullet))
    story.append(Paragraph("• <b>Predictive Maintenance Analytics:</b> Leverage machine learning to analyze historical defect rates and schedule preventative servicing before hardware failures occur.", style_bullet))
    story.append(Paragraph("• <b>Native Mobile Applications:</b> Develop cross-platform Flutter/React Native mobile applications for on-the-go inventory audits.", style_bullet))
    story.append(Paragraph("• <b>Enterprise ERP Integration:</b> Connect the platform with SAP, Oracle, or institutional finance software for seamless procurement accounting.", style_bullet))
    story.append(Spacer(1, 15))

    story.append(Paragraph("References", style_h1))
    story.append(Spacer(1, 8))
    refs = [
        "[1] Django Software Foundation, \"Django Documentation and Architectural Patterns,\" 2026. [Online]. Available: https://docs.djangoproject.com/",
        "[2] O. Eweoya, A. O. Agbeyangi and J. M. Lukose, \"TaskHive: A Web-Based Academic Project Management System for Higher Education,\" Information Impact: Journal of Information and Knowledge Management, 2025.",
        "[3] Tailwind Labs, \"Tailwind CSS Documentation - Rapid UI Development Framework,\" 2026. [Online]. Available: https://tailwindcss.com/docs",
        "[4] IIT Madras, \"Tracking Student Progress and Resource Allocation in Software Projects,\" Software Engineering Project Reports, 2024.",
        "[5] GitHub Docs, \"Version Control Best Practices with Git and GitHub,\" 2026. [Online]. Available: https://docs.github.com/",
        "[6] Python Software Foundation, \"Python 3.13 Language Reference and Standard Library,\" 2026. [Online]. Available: https://www.python.org/",
    ]
    for r in refs:
        story.append(Paragraph(r, style_bullet))
    story.append(PageBreak())

    # ==========================================
    # APPENDICES
    # ==========================================
    story.append(Paragraph("Appendix A: Data Flow Diagram", style_h1))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Figure A.1 illustrates the Level 0 Context Data Flow Diagram depicting external entities (Administrator, Employee, Department Head) interacting with the central Inventory Management System boundary and SQLite datastore.", style_body))

    dfd_path = "dfd.png"
    if os.path.exists(dfd_path):
        story.append(Spacer(1, 10))
        story.append(Image(dfd_path, width=420, height=270))
        story.append(Paragraph("Figure A.1: Level 0 DFD - System Context Diagram", style_caption))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Level 1 to Level 4 DFD Specifications:</b>", style_h3))
    story.append(Paragraph("• <b>Level 1 DFD:</b> Models Employee Authentication, Catalog Querying, and Requisition Submission into the Asset Request Datastore.", style_body))
    story.append(Paragraph("• <b>Level 2 DFD:</b> Models Administrator Stock Review, Category Provisioning, and Approval / Rejection Decision Routing.", style_body))
    story.append(Paragraph("• <b>Level 3 DFD:</b> Models Requisition Fulfillment, Stock Decrementing, and Asset Return Check-in with Inventory Restoration.", style_body))
    story.append(Paragraph("• <b>Level 4 DFD:</b> Models Maintenance Issue Reporting, Workload Task Auto-Assignment, Milestone Verification, and Gamification Badging.", style_body))
    story.append(PageBreak())

    story.append(Paragraph("Appendix B: Entity–Relationship Diagram", style_h1))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Figure B.1 presents the Entity–Relationship Diagram modeling relational cardinalities across User, Department, Category, Asset, AssetRequest, Task, SubTask, MaintenanceIssue, DepartmentIssue, and Award entities.", style_body))

    erd_path = "erd.png"
    if os.path.exists(erd_path):
        story.append(Spacer(1, 10))
        story.append(Image(erd_path, width=380, height=520))
        story.append(Paragraph("Figure B.1: Entity–Relationship Diagram for Inventory, Tasks & Issues", style_caption))
    story.append(PageBreak())

    # ==========================================
    # APPENDIX C: SOURCE CODE
    # ==========================================
    story.append(Paragraph("Appendix C: Source Code", style_h1))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>C.1 Core Data Models (inventory/models.py)</b>", style_h3))
    code_models = """class Asset(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='assets')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    total_quantity = models.PositiveIntegerField(default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)

    @property
    def is_low_stock(self):
        return self.available_quantity <= self.low_stock_threshold

    @property
    def stock_status(self):
        if self.available_quantity == 0:
            return 'OUT_OF_STOCK'
        elif self.available_quantity <= self.low_stock_threshold:
            return 'LOW_STOCK'
        return 'IN_STOCK'

class AssetRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'), ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'), ('RETURNED', 'Returned')
    )
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='requests')
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, default='')
    admin_notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)"""
    for line in code_models.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>C.2 Requisition Approval & Return Controller (inventory/views.py)</b>", style_h3))
    code_views = """@login_required
def approve_request(request, request_id):
    if not request.user.is_admin_role:
        return redirect('employee_dashboard')
    asset_req = get_object_or_404(AssetRequest, id=request_id)
    if asset_req.status == 'PENDING':
        if asset_req.asset.available_quantity >= asset_req.quantity:
            asset_req.asset.available_quantity -= asset_req.quantity
            asset_req.asset.save()
            asset_req.status = 'APPROVED'
            asset_req.response_date = timezone.now()
            asset_req.save()
            messages.success(request, f'Request #{asset_req.id} approved.')
    return redirect('request_list')

@login_required
def return_asset(request, request_id):
    asset_req = get_object_or_404(AssetRequest, id=request_id)
    if asset_req.status == 'APPROVED':
        asset_req.asset.available_quantity += asset_req.quantity
        asset_req.asset.save()
        asset_req.status = 'RETURNED'
        asset_req.return_date = timezone.now()
        asset_req.save()
        messages.success(request, f'Asset returned. Stock restored.')
    return redirect('request_list')"""
    for line in code_views.split('\n'):
        story.append(Paragraph(line.replace(' ', '&nbsp;'), style_code))
    story.append(PageBreak())

    # ==========================================
    # APPENDIX D: SCREENSHOTS
    # ==========================================
    story.append(Paragraph("Appendix D: Screenshots", style_h1))
    story.append(Spacer(1, 8))
    story.append(Paragraph("This section presents the implemented user interfaces of the Role-Based Inventory and Asset Management System.", style_body))

    screenshots_list = [
        ("D.1 Login Page", "Figure D.1: Branded authentication portal with username, password, visibility toggle, and automatic role routing."),
        ("D.2 Admin Command Center Dashboard", "Figure D.2: Executive admin dashboard with 6 KPI metrics, low-stock alert banner, and pending requests queue."),
        ("D.3 Department Management Directory", "Figure D.3: Department directory displaying unit cards, employee headcounts, and assigned assets."),
        ("D.4 Asset Catalog & Availability Level", "Figure D.4: Real-time inventory table with availability progress bars, stock status pills, and filters."),
        ("D.5 Add / Edit Asset Form", "Figure D.5: Asset creation modal with category selector, department allocation, and threshold settings."),
        ("D.6 Employee Workspace Dashboard", "Figure D.6: Employee dashboard with personalized profile banner, active tasks, and quick checkout catalog."),
        ("D.7 Asset Requisition Queue & Return Check-in", "Figure D.7: Requisition tracking view with status filters, approval modal, and Return Asset action."),
        ("D.8 Complaints & Maintenance Issue Ticketing", "Figure D.8: Dual-tab ticketing system for physical equipment defects and cross-departmental requests."),
        ("D.9 Task & Subtask Progress Milestones", "Figure D.9: Task workflow center featuring workload auto-assignment, interactive checklist, and progress bars."),
        ("D.10 Achievement Awards Wall & Leaderboard", "Figure D.10: Gamified recognition wall displaying earned badges, on-time completion awards, and leaderboard."),
    ]

    for title, desc in screenshots_list:
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<b>{title}</b>", style_h3))
        story.append(Paragraph(desc, style_body))
        
        # Elegant styled placeholder frame
        box_data = [[f"[ Screenshot Placeholder: {title} ]\n(1280 x 720 px Recommended)"]]
        t_box = Table(box_data, colWidths=[480], rowHeights=[90])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94A3B8')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#64748B')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        story.append(t_box)
        story.append(Paragraph(desc, style_caption))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_filename}!")

if __name__ == '__main__':
    create_report()
