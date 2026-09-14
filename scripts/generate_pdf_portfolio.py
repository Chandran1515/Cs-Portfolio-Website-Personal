import os
import glob
import json
import shutil
from io import BytesIO
from PIL import Image as PILImage

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
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
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 756, "Ar. Chandran Shanmugam | Architectural Design & BIM Technical Portfolio")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 36, 576, 36)
        
        footer_text = "Email: chandranarch15@gmail.com | Portfolio: https://chandran1515.github.io/Cs-Portfolio-Website-Personal/"
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(36, 24, footer_text)
        self.drawRightString(576, 24, page_text)
        self.restoreState()


def get_scaled_image(img_path, max_w, max_h, max_pixel_dim=1200):
    if not img_path or not os.path.exists(img_path):
        return None
    try:
        with PILImage.open(img_path) as im:
            if im.mode in ('RGBA', 'LA', 'P'):
                im = im.convert('RGB')
            
            w, h = im.size
            if w <= 0 or h <= 0:
                return None
            
            if max(w, h) > max_pixel_dim:
                ratio = max_pixel_dim / float(max(w, h))
                new_w = int(w * ratio)
                new_h = int(h * ratio)
                im = im.resize((new_w, new_h), PILImage.Resampling.LANCZOS)
                w, h = new_w, new_h

            buf = BytesIO()
            im.save(buf, format='JPEG', quality=85, optimize=True)
            buf.seek(0)
            
            aspect = h / float(w)
            target_w = max_w
            target_h = target_w * aspect
            if target_h > max_h:
                target_h = max_h
                target_w = target_h / aspect

            return RLImage(buf, width=target_w, height=target_h)
    except Exception as e:
        print(f"Error processing image {img_path}: {e}")
        return None


def build_pdf():
    pdf_path = os.path.join("docs", "Ar_Chandran_Shanmugam_Portfolio_2026.pdf")
    os.makedirs("docs", exist_ok=True)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0066FF'),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=8,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    badge_lead = ParagraphStyle(
        'BadgeLead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0066FF')
    )

    badge_team = ParagraphStyle(
        'BadgeTeam',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#475569')
    )

    story = []

    # ==================== PAGE 1: FULL EXECUTIVE COVER SHEET ====================
    story.append(Paragraph("Ar. Chandran Shanmugam", title_style))
    story.append(Paragraph("Architect &amp; Technical Delivery Specialist | BIM &amp; Revit Lead", subtitle_style))
    
    # Credential summary box
    summary_html = """
    <b>Total Experience:</b> 8+ Years Architectural &amp; BIM Specialist &nbsp;|&nbsp; 
    <b>California Experience:</b> 3.5+ Years (Studio Schicketanz, Sep 2022 – Apr 2026)<br/>
    <b>Location:</b> California, USA &nbsp;|&nbsp; 
    <b>Email:</b> chandranarch15@gmail.com &nbsp;|&nbsp; 
    <b>License/Reg:</b> Council of Architecture Registered Architect
    """
    
    summary_table_data = [
        [Paragraph(summary_html, ParagraphStyle('SumBox', parent=body_style, fontSize=8, leading=11.5, textColor=colors.HexColor('#1E293B')))]
    ]
    summary_table = Table(summary_table_data, colWidths=[540])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))

    # Executive Overview
    story.append(Paragraph("Professional Profile &amp; Technical Capabilities", h1_style))
    overview_text = (
        "Architect and BIM Technical Delivery Specialist with over <b>8+ years of total experience</b>, including "
        "<b>3.5+ years of dedicated California high-end architectural delivery</b> at Studio Schicketanz (Carmel-by-the-Sea, CA). "
        "Specialized in leading complex multi-component luxury residential estates and commercial art studios through "
        "full project lifecycles—from Design Development (DD) through Construction Documentation (CD), Permitting, and Construction Administration (CA).<br/><br/>"
        "Expert in high-performance building envelope detailing, waterproofing, window/door schedule management, Title 24 energy code compliance, "
        "and multi-disciplinary BIM coordination (Structural, MEP, Civil, Geotech). Developer of <b>CS Revit Labs</b>—a suite of custom C#/Python Revit "
        "add-ins for automated QA/QC, sheet creation, keynote management, and workset management."
    )
    story.append(Paragraph(overview_text, body_style))
    story.append(Spacer(1, 6))

    # Key Statistics Grid
    stats_data = [
        [
            Paragraph("<b>8+ Years</b><br/><font color='#64748B'>Total Arch &amp; BIM Exp</font>", ParagraphStyle('St1', parent=body_style, alignment=1, fontSize=8, leading=11)),
            Paragraph("<b>3.5+ Years</b><br/><font color='#64748B'>California Exp (Studio Schicketanz)</font>", ParagraphStyle('St2', parent=body_style, alignment=1, fontSize=8, leading=11)),
            Paragraph("<b>15 Projects</b><br/><font color='#64748B'>Permitted CA Sets Delivered</font>", ParagraphStyle('St3', parent=body_style, alignment=1, fontSize=8, leading=11)),
            Paragraph("<b>8 Projects</b><br/><font color='#64748B'>As Project Lead</font>", ParagraphStyle('St4', parent=body_style, alignment=1, fontSize=8, leading=11))
        ]
    ]
    stats_table = Table(stats_data, colWidths=[135, 135, 135, 135])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#BFDBFE')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DBEAFE')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 8))

    # Core Technical Skillset Table
    skills_data = [
        [Paragraph("<b>Primary BIM &amp; CAD:</b>", meta_label), Paragraph("Autodesk Revit (Advanced/Primary), AutoCAD, Navisworks Manage", meta_val)],
        [Paragraph("<b>Visualization:</b>", meta_label), Paragraph("Enscape, Adobe Creative Cloud (Photoshop, Illustrator, InDesign)", meta_val)],
        [Paragraph("<b>BIM Automation:</b>", meta_label), Paragraph("CS Revit Labs (C# / Revit API / Python / PyRevit), Dynamo", meta_val)],
        [Paragraph("<b>Codes &amp; Standards:</b>", meta_label), Paragraph("California Building Code (CBC/CRC), Title 24, ADA Accessibility, CALGreen", meta_val)],
        [Paragraph("<b>Project Scope:</b>", meta_label), Paragraph("Luxury Residential, ADUs, Historic Renovations, Commercial Art Studios", meta_val)]
    ]
    skills_table = Table(skills_data, colWidths=[120, 420])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#F1F5F9'))
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 8))

    # Project Index Summary Box on Page 1
    index_html = """
    <b>15 Permitted California Projects Portfolio Index (Studio Schicketanz 2022–2026):</b><br/>
    • <b>Cappo Scenic (SS-001)</b> [Project Lead | CD Set] &nbsp;|&nbsp; 
    • <b>Dolgov Main House (SS-002 Palo Alto)</b> [Project Lead | Ongoing]<br/>
    • <b>Charl Cherry Art Studio (SS-008)</b> [Project Lead | Commercial] &nbsp;|&nbsp; 
    • <b>Moss Historic House (SS-006)</b> [Project Lead | Landmark]<br/>
    • <b>Yeung Studio (SS-005)</b> [Project Lead] &nbsp;|&nbsp; 
    • <b>Weiss Emerald Bay (SS-012)</b> [Project Lead | Orange County] &nbsp;|&nbsp; 
    • <b>McCarthy &amp; Knoop 250</b> [Project Leads]
    """
    index_table_data = [[Paragraph(index_html, ParagraphStyle('IdxBox', parent=body_style, fontSize=7.8, leading=11, textColor=colors.HexColor('#1E293B')))]]
    index_table = Table(index_table_data, colWidths=[540])
    index_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(index_table)

    # Clean PageBreak after Page 1 Cover Sheet!
    story.append(PageBreak())

    # ==================== PAGE 2+: CALIFORNIA PROJECTS SECTION ====================
    story.append(Paragraph("California Architectural &amp; BIM Projects (Studio Schicketanz 2022–2026)", h1_style))
    story.append(Paragraph(
        "Complete portfolio of 15 permitted California building projects spanning Monterey County, Palo Alto, and Orange County. "
        "Delivered full BIM models, technical detailing, building enclosure drawings, and construction coordination.", body_style
    ))
    story.append(Spacer(1, 8))

    projects = [
        {
            "id": "SS-001",
            "name": "Cappo Scenic",
            "jurisdiction": "Monterey County",
            "role": "Project Lead",
            "status": "CD Set Delivered",
            "type": "Luxury Residential Remodel & ADU",
            "img": "images/projects/cappo/cover.png",
            "desc": "Lead architect for a high-end coastal estate remodel featuring a main house, new subterranean garage, detached ADU, and exterior deck. Authored full Revit model, structural/MEP coordination, and complete CD permit set."
        },
        {
            "id": "SS-002",
            "name": "Dolgov Main House",
            "jurisdiction": "City of Palo Alto",
            "role": "Project Lead",
            "status": "Ongoing (Planning & Building)",
            "type": "Single-Family New Construction",
            "img": "images/projects/dolgov/cover.png",
            "desc": "Project lead for a modern residence in Palo Alto. Managed Planning department approvals, Title 24 compliance, green building standards, and detailed architectural construction documentation."
        },
        {
            "id": "SS-008",
            "name": "Charl Cherry Art Studio",
            "jurisdiction": "Monterey County",
            "role": "Project Lead",
            "status": "Ongoing",
            "type": "Commercial Art Studio",
            "img": "images/projects/charl-cherry/1_carl cherry.png",
            "desc": "Project lead for a custom commercial art studio building. Handled spatial layout, high-performance lighting design, fire/life-safety compliance, and comprehensive detail drafting in Revit."
        },
        {
            "id": "SS-006",
            "name": "Moss Residence",
            "jurisdiction": "Monterey County",
            "role": "Project Lead",
            "status": "CD Set Delivered",
            "type": "Historic Landmark Preservation",
            "img": "images/projects/moss/Moss.jpg",
            "desc": "Led technical delivery for a sensitive historic residence renovation. Coordinated historic architectural guidelines, exterior envelope waterproofing, custom timber detailing, and permit approval."
        },
        {
            "id": "SS-005",
            "name": "Yeung Remodel",
            "jurisdiction": "Monterey County",
            "role": "Project Lead",
            "status": "CD Set Delivered",
            "type": "Residential Main House & Studio",
            "img": "images/projects/yeung-studio/Yeung.png",
            "desc": "Project lead for a comprehensive main house and detached studio remodel. Authored complete Revit construction drawings, interior millwork elevations, and exterior cladding connections."
        },
        {
            "id": "SS-012",
            "name": "Weiss Emerald Bay",
            "jurisdiction": "Orange County",
            "role": "Project Lead",
            "status": "CD Set Delivered",
            "type": "High-End Coastal Interior Remodel",
            "img": "images/projects/weiss/weiss.png",
            "desc": "Led luxury interior remodel in Emerald Bay, Laguna Beach. Coordinated bespoke architectural millwork, interior lighting packages, and mechanical integration."
        },
        {
            "id": "SS-014",
            "name": "McCarthy Residence",
            "jurisdiction": "Monterey County",
            "role": "Project Lead",
            "status": "CD Set Delivered",
            "type": "Residential Construction Set",
            "img": "images/projects/mccarthy/Mccarthy.jpg",
            "desc": "Project lead responsible for full CD set production, window/door schedules, enclosure detailing, and county plan-check correction responses."
        },
        {
            "id": "SS-004",
            "name": "Knoop 250",
            "jurisdiction": "Monterey County",
            "role": "Project Lead",
            "status": "CD Set Delivered",
            "type": "Residential Remodel & Addition",
            "img": "images/projects/knoop/knoop 250.png",
            "desc": "Led architectural design development and working drawing set for a custom residential remodel in Carmel. Modeled structural framing and custom roof details."
        },
        {
            "id": "SS-010",
            "name": "Lunquist Residence",
            "jurisdiction": "Monterey County",
            "role": "Team Contributor",
            "status": "CD Set Delivered",
            "type": "Custom Residential",
            "img": "images/projects/lunquist/Lundquist.jpg",
            "desc": "BIM specialist responsible for complex roof framing details, interior wall sections, and consultant sheet alignment."
        },
        {
            "id": "SS-003",
            "name": "Kani Remodel",
            "jurisdiction": "Monterey County",
            "role": "Team Contributor",
            "status": "CD Set Delivered",
            "type": "Residential Remodel",
            "img": "images/projects/kani/kani.jpg",
            "desc": "Contributed architectural details, door/window schedules, and floor plan revisions for permit submission."
        },
        {
            "id": "SS-009",
            "name": "Connors Residence",
            "jurisdiction": "Monterey County",
            "role": "Team Contributor",
            "status": "CD Set Delivered",
            "type": "Residential Remodel",
            "img": "images/projects/connors/connors.png",
            "desc": "Assisted in Revit model management, site plan layout, and building envelope sheet preparation."
        },
        {
            "id": "SS-013",
            "name": "Bayview",
            "jurisdiction": "Monterey County",
            "role": "Team Contributor",
            "status": "CD Set Delivered",
            "type": "Coastal Residence",
            "img": None,
            "desc": "Supported project team with REVIT model updating, coordination items, and plan set formatting."
        },
        {
            "id": "SS-011",
            "name": "Kartalis Residence",
            "jurisdiction": "Monterey County",
            "role": "Team Contributor",
            "status": "CD Set Delivered",
            "type": "Custom Residential",
            "img": "images/projects/kartalis/kartalis cover.png",
            "desc": "Drafted exterior elevation details and floor plans for county submittal set."
        },
        {
            "id": "SS-007",
            "name": "Nelson's Residence",
            "jurisdiction": "Monterey County",
            "role": "Team Contributor",
            "status": "CD Set Delivered",
            "type": "Construction Docs",
            "img": "images/projects/nelson/Nelson.jpg",
            "desc": "BIM drafting, sheet setup, title block standards, and structural coordination sheets."
        },
        {
            "id": "SS-015",
            "name": "Lot 67",
            "jurisdiction": "Monterey County",
            "role": "Team Contributor",
            "status": "CD Set Delivered",
            "type": "Construction Docs",
            "img": "images/projects/lot67/lot 67.jpg",
            "desc": "Produced building sections, wall callouts, and schedule graphics for building permit package."
        }
    ]

    for p in projects:
        role_text = f"<font color='#0066FF'><b>★ {p['role']}</b></font>" if p['role'] == 'Project Lead' else f"<b>{p['role']}</b>"
        
        info_cell_html = f"""
        <b><font size='10.5' color='#0F172A'>{p['name']}</font></b> &nbsp; <font color='#64748B'>[{p['id']}]</font><br/>
        {role_text} &nbsp;|&nbsp; <b>Jurisdiction:</b> {p['jurisdiction']} &nbsp;|&nbsp; <b>Status:</b> {p['status']}<br/>
        <font color='#475569'><b>Category:</b> {p['type']}</font><br/><br/>
        {p['desc']}
        """
        
        info_para = Paragraph(info_cell_html, body_style)
        
        rl_img = get_scaled_image(p['img'], max_w=165, max_h=100) if p['img'] else None
        
        if rl_img:
            card_table_data = [[info_para, rl_img]]
            card_table = Table(card_table_data, colWidths=[355, 185])
        else:
            card_table_data = [[info_para]]
            card_table = Table(card_table_data, colWidths=[540])
            
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 7),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'CENTER')
        ]))

        story.append(KeepTogether([card_table, Spacer(1, 7)]))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0066FF"), spaceBefore=8, spaceAfter=12))

    # ==================== SECTION: CS REVIT LABS & BIM AUTOMATION ====================
    story.append(Paragraph("CS Revit Labs — Custom BIM &amp; Revit Automation", h1_style))
    revit_desc = (
        "To elevate drafting efficiency, accuracy, and QA/QC speed across high-end architectural projects, "
        "Ar. Chandran developed <b>CS Revit Labs</b>—a proprietary suite of custom Revit add-ins and automation scripts. "
        "These tools eliminate manual repetitive work, enforce graphic standards, and accelerate permit set delivery."
    )
    story.append(Paragraph(revit_desc, body_style))
    story.append(Spacer(1, 6))

    tools_data = [
        [Paragraph("<b>AI Control Centre</b>", meta_label), Paragraph("Centralized execution hub for Revit API utilities and project batch scripts.", meta_val)],
        [Paragraph("<b>Auto Tagging &amp; Keynote Browser</b>", meta_label), Paragraph("Intelligent automatic element tagging and keynote management across multi-discipline sheets.", meta_val)],
        [Paragraph("<b>Coordination Set Generator</b>", meta_label), Paragraph("One-click creation and export of DWG/PDF consultant coordination packages.", meta_val)],
        [Paragraph("<b>Graphic QC Checker</b>", meta_label), Paragraph("Automated model audit tool to check line styles, view templates, and sheet compliance before printing.", meta_val)],
        [Paragraph("<b>Sheet Craft &amp; Worksets</b>", meta_label), Paragraph("Batch workset creator and sheet generator for high-speed setup during DD phase.", meta_val)]
    ]
    
    revit_img_path = "images/projects/CS Revit Labs/cs revit labs plugin SS.jpg"
    rl_revit_img = get_scaled_image(revit_img_path, max_w=190, max_h=120)

    tools_table = Table(tools_data, colWidths=[150, 180])
    tools_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#F1F5F9'))
    ]))

    if rl_revit_img:
        labs_layout_data = [[tools_table, rl_revit_img]]
        labs_layout = Table(labs_layout_data, colWidths=[330, 210])
        labs_layout.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('PADDING', (0,0), (-1,-1), 4)
        ]))
        story.append(labs_layout)
    else:
        story.append(tools_table)

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0066FF"), spaceBefore=8, spaceAfter=12))

    # ==================== SECTION: PRIOR WORK & RESUME SUMMARY ====================
    story.append(Paragraph("Education, Credentials &amp; Prior Experience (2019–2022)", h1_style))
    
    prior_html = """
    <b>Bachelor of Architecture (B.Arch)</b><br/>
    Registered Architect with Council of Architecture (CoA)<br/><br/>
    <b>International Portfolio (2019–2022):</b><br/>
    Prior to joining Studio Schicketanz in California, Chandran delivered diverse residential, institutional, and commercial projects internationally. 
    Full prior project documentation is available in the supplemental publication: 
    <font color='#0066FF'><b>docs/Portfolio_2019_to_2022.pdf</b></font>.
    """
    story.append(Paragraph(prior_html, body_style))
    story.append(Spacer(1, 12))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF portfolio at: {pdf_path}")

    # Copy to Documents and Desktop
    doc_dst = os.path.expanduser('~/Documents/Ar_Chandran_Shanmugam_Portfolio_2026.pdf')
    desk_dst = os.path.expanduser('~/Desktop/Ar_Chandran_Shanmugam_Portfolio_2026.pdf')
    shutil.copy(pdf_path, doc_dst)
    shutil.copy(pdf_path, desk_dst)
    print(f"Copied {pdf_path} to {doc_dst} and {desk_dst}")

if __name__ == "__main__":
    build_pdf()
