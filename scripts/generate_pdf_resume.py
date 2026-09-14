import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class ATSResumeCanvas(canvas.Canvas):
    """Canvas for single-column ATS resume with clean page numbers."""
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
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "CHANDRAN SHANMUGAM, M.Arch | Job Captain & Architectural Delivery Lead")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)
            
        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 32, 576, 32)
        
        footer_text = "chandran.s.dev@gmail.com | +91 79040 53633 | Portfolio: chandran1515.github.io/Cs-Portfolio-Website-Personal"
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(36, 20, footer_text)
        self.drawRightString(576, 20, page_text)
        self.restoreState()

def build_resume_pdf():
    docs_dir = "docs"
    os.makedirs(docs_dir, exist_ok=True)
    pdf_path = os.path.join(docs_dir, "Ar_Chandran_Shanmugam_Resume.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    # Custom ATS Styles
    name_style = ParagraphStyle(
        'ATSName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=0,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'ATSSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor('#2563EB'),
        alignment=0,
        spaceAfter=4
    )
    
    contact_style = ParagraphStyle(
        'ATSContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    section_heading = ParagraphStyle(
        'ATSSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=8,
        spaceAfter=4,
        textTransform='uppercase'
    )
    
    body_style = ParagraphStyle(
        'ATSBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=3
    )
    
    job_title_style = ParagraphStyle(
        'ATSJobTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=4,
        spaceAfter=1
    )
    
    company_style = ParagraphStyle(
        'ATSCompany',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#475569'),
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'ATSBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    story = []

    # 1. HEADER
    story.append(Paragraph("CHANDRAN SHANMUGAM, M.Arch", name_style))
    story.append(Paragraph("Job Captain | Architectural Specialist & VDC Delivery Lead | LEED Green Associate (Pursuing)", subtitle_style))
    story.append(Paragraph("Location: Bangalore, India | Email: chandran.s.dev@gmail.com | Phone: +91 79040 53633<br/>LinkedIn: linkedin.com/in/chandran-shanmugam-421b7b149 | Portfolio: chandran1515.github.io/Cs-Portfolio-Website-Personal", contact_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0F172A"), spaceBefore=2, spaceAfter=6))

    # 2. PROFESSIONAL SUMMARY
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=4))
    summary_text = (
        "Seasoned <b>Job Captain & Architectural Specialist</b> with <b>8+ years</b> of professional experience leading high-end residential, "
        "commercial, healthcare, industrial, and sustainable architectural design projects from Design Development (DD) through Construction Administration (CA). "
        "Proven track record producing permitted California architectural drawing packages, international LOD 300–400 BIM models, and "
        "<b>LEED / Title 24 sustainable energy compliance</b> across 20+ complex projects in the US, Australia, Netherlands, Dubai, and India. "
        "Strong architectural design authority complemented by advanced VDC expertise in <b>Autodesk Construction Cloud (ACC/BIM 360)</b>, "
        "<b>Navisworks Manage</b>, and custom <b>C#/.NET Revit API & pyRevit automation</b>—streamlining pre-construction coordination and eliminating field constructability conflicts prior to site mobilization."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 3))

    # 3. CORE COMPETENCIES
    story.append(Paragraph("CORE COMPETENCIES", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=4))
    story.append(Paragraph("• <b>Architectural Design & Detailing:</b> Architectural Design Authority | Design Development (DD) & CD Production | Building Envelope & Waterproofing Detailing | Sustainable Design & LEED Standards | Passive Solar & Massing | Site Planning | California Building Code (CBC/CRC) | Title 24 Energy Compliance | ADA / Accessibility Guidelines | International Building Code (IBC) | Construction Administration (CA) & Site Inspections", bullet_style))
    story.append(Paragraph("• <b>VDC & Project Delivery Apps:</b> Virtual Design & Construction (VDC) | BIM Execution Plan (BEP) | Multi-Discipline Clash Coordination (Navisworks Manage) | Autodesk Construction Cloud (ACC / BIM 360) | Procore | Bluebeam Revu | AutoCAD | Rhino 3D / Grasshopper", bullet_style))
    story.append(Paragraph("• <b>BIM Automation & Technical Stack:</b> C# (.NET Framework / Revit API) | pyRevit | Python | Dynamo | Automated QA/QC Model Auditing | Custom Add-In Development | Git / GitHub", bullet_style))
    story.append(Spacer(1, 4))

    # 4. WORK EXPERIENCE
    story.append(Paragraph("WORK EXPERIENCE", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=4))

    # Studio Schicketanz
    story.append(Paragraph("STUDIO SCHICKETANZ | Bangalore, India (HQ: Carmel-by-the-Sea, CA)", job_title_style))
    story.append(Paragraph("Job Captain & Architectural Delivery Lead | Sep 2022 – Present", company_style))
    story.append(Paragraph("• <b>Directed architectural design development (DD to CD)</b> and permit set creation for 4+ luxury coastal residences in Carmel-by-the-Sea, CA, designing custom wood-and-steel joinery, high-performance building envelope details, and slope-adapted foundations.", bullet_style))
    story.append(Paragraph("• <b>Spearheaded LEED & Title 24 energy efficiency compliance</b>, optimizing building envelope thermal performance, passive solar orientation, and natural day-lighting to achieve <b>100% first-pass plan check approvals</b> with California building departments.", bullet_style))
    story.append(Paragraph("• <b>Managed multi-discipline consultant coordination</b> across structural engineers, MEP consultants, civil engineers, and general contractors via <b>Autodesk Construction Cloud (ACC / BIM 360)</b>, <b>Procore</b>, and <b>Bluebeam Revu</b>.", bullet_style))
    story.append(Paragraph("• <b>Executed detailed construction administration (CA) support</b>, reviewing contractor submittals, answering field RFIs, and issuing constructability detail revisions to maintain design fidelity during construction.", bullet_style))
    story.append(Paragraph("• <b>Engineered custom C#/.NET Revit API add-ins</b> (<i>SheetCraft</i>, Keynote Browser, Auto-Tagger), automating repetitive view creation and sheet setup to <b>reduce CD production setup time by 40%</b> across 15+ California building projects.", bullet_style))
    story.append(Paragraph("• <b>Coordinated LOD 300–400 BIM models in Navisworks Manage</b>, conducting pre-construction clash detection and automated pyRevit/Dynamo QA/QC audits to resolve constructability conflicts before site mobilization.", bullet_style))
    story.append(Spacer(1, 3))

    # Jarinam Parallelspace
    story.append(Paragraph("JARINAM PARALLELSPACE PRIVATE LIMITED | Bangalore, India (Remote)", job_title_style))
    story.append(Paragraph("BIM Architect | Dec 2021 – Oct 2022", company_style))
    story.append(Paragraph("• <b>Coordinated LOD 300–350 architectural BIM packages</b> for international commercial and industrial developments, including the <b>Lane Cove Warehouse</b> (Australia) and <b>Fitton Engineering Warehouse</b> (Dubai).", bullet_style))
    story.append(Paragraph("• <b>Developed high-LOD multi-family residential BIM models</b>, leading drawing production for <b>Hafeez Contractor Apartment R16 & R7 developments</b> in Pune and custom <b>Hosur Residential Estate</b>.", bullet_style))
    story.append(Paragraph("• <b>Managed interior architectural modeling & BIM detailing</b> for commercial retail spaces, including <b>Form Silks Commercial Interior</b> in Bangalore.", bullet_style))
    story.append(Paragraph("• <b>Executed interdisciplinary BIM clash detection</b> in Navisworks Manage and enforced BIM Execution Plan (BEP) modeling standards across project teams.", bullet_style))
    story.append(Spacer(1, 3))

    # Pinnacle Technology Services
    story.append(Paragraph("PINNACLE TECHNOLOGY SERVICES PVT LTD | Hyderabad, India (Remote)", job_title_style))
    story.append(Paragraph("Revit Jr. Modeller | Jul 2021 – Dec 2021", company_style))
    story.append(Paragraph("• <b>Delivered constructible LOD 300–350 architectural BIM models</b> for international clients, specializing in <b>Netherlands Housing BIM developments</b>.", bullet_style))
    story.append(Paragraph("• <b>Modeled detailed architectural components, wall sections, and floor plan assemblies</b>, adhering strictly to European architectural graphic standards and client CAD/BIM specifications.", bullet_style))
    story.append(Spacer(1, 3))

    # Neural Design & Construction
    story.append(Paragraph("NEURAL DESIGN AND CONSTRUCTION LTD. | Madurai, Tamil Nadu, India", job_title_style))
    story.append(Paragraph("Architect & Project Lead | Jun 2019 – Jun 2021", company_style))
    story.append(Paragraph("• <b>Spearheaded architectural design and CD packages</b> for flagship projects including <b>Urban Primary Health Centre (UPHC @ Chennai)</b>, <b>Pandian Nagar Row House (Madurai)</b>, <b>Mr. Suriya Pandi Residence</b>, <b>Thagapandi Residence</b>, <b>Madurai Tin Industrial Factory</b>, and <b>Courtallam Eco-Resort</b>.", bullet_style))
    story.append(Paragraph("• <b>Gained extensive project management experience</b>, leading client meetings, contractor negotiations, vendor procurement, and supervising component installation on site.", bullet_style))
    story.append(Paragraph("• <b>Integrated sustainable building materials and passive cooling strategies</b> tailored to South Indian climate conditions.", bullet_style))
    story.append(Spacer(1, 3))

    # Freelance Architect
    story.append(Paragraph("FREELANCE ARCHITECT | Madurai & Bengaluru, India", job_title_style))
    story.append(Paragraph("Architect & Design Consultant | Sep 2017 – Jun 2019", company_style))
    story.append(Paragraph("• <b>Designed and delivered complete architectural packages</b> for <b>Star Palms Residential Complex</b> (Banaswadi, Bengaluru) and <b>Commercial Complex</b> (100ft Road, Bengaluru).", bullet_style))
    story.append(Paragraph("• <b>Managed client consultations, contractor negotiations, material procurement</b>, and on-site construction supervision to ensure structural integrity and timely delivery.", bullet_style))
    story.append(Spacer(1, 3))

    # Iver Architects
    story.append(Paragraph("IVER ARCHITECTS | Chennai, India", job_title_style))
    story.append(Paragraph("Architectural Intern (Post Graduate) | Dec 2018 – Mar 2019", company_style))
    story.append(Paragraph("• <b>Developed architectural design proposals, DD packages, and working drawings</b> for commercial and residential projects, conducting site visits, plan renderings, and client presentations.", bullet_style))
    story.append(Spacer(1, 3))

    # Ineidos
    story.append(Paragraph("INEIDOS | Bangalore, India", job_title_style))
    story.append(Paragraph("Architectural Intern (Under Graduate) | Dec 2015 – Jul 2016", company_style))
    story.append(Paragraph("• <b>Created concept design diagrams, research documents, technical working drawings</b>, and perspective renderings from schematic design through Design Development.", bullet_style))
    story.append(Spacer(1, 4))

    # 5. FEATURED PROJECTS
    story.append(Paragraph("FEATURED ARCHITECTURAL & SUSTAINABILITY PROJECTS", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=4))
    story.append(Paragraph("• <b>Carmel Coastal Luxury Residences (Carmel-by-the-Sea, CA, USA):</b> Managed architectural design development, building envelope waterproofing, Title 24 energy compliance, and LOD 400 BIM coordination for luxury coastal residences.", bullet_style))
    story.append(Paragraph("• <b>Urban Primary Health Centre (UPHC Chennai, India):</b> Led architectural design proposals, DD, and CD documentation for public healthcare infrastructure.", bullet_style))
    story.append(Paragraph("• <b>Lane Cove & Fitton Engineering Warehouses (Australia & Dubai):</b> Modeled LOD 300–350 industrial architectural BIM packages and structural interfaces.", bullet_style))
    story.append(Paragraph("• <b>Star Palms & 100ft Road Commercial Complex (Bengaluru, India):</b> Designed multi-story commercial and residential developments from concept to construction administration.", bullet_style))
    story.append(Paragraph("• <b>Custom Revit API Suite (SheetCraft & CS Labs Tools):</b> Programmed C#/.NET tools for automated sheet setup, batch view placement, and model QA/QC, adopted firm-wide to save ~12 hours per project per designer.", bullet_style))
    story.append(Spacer(1, 4))

    # 6. EDUCATION & CREDENTIALS
    story.append(Paragraph("EDUCATION & CREDENTIALS", section_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=4))
    story.append(Paragraph("• <b>Master of Architecture (M.Arch)</b> — Meenakshi College of Engineering, Anna University, Chennai (2019)", bullet_style))
    story.append(Paragraph("• <b>Bachelor of Architecture (B.Arch)</b> — Tamilnadu School of Architecture, Coimbatore (2017)", bullet_style))
    story.append(Paragraph("• <b>Registered Architect</b> — Council of Architecture (COA), India", bullet_style))
    story.append(Paragraph("• <b>LEED Green Associate</b> (Pursuing / Sustainable Building Certification)", bullet_style))

    doc.build(story, canvasmaker=ATSResumeCanvas)
    print(f"PDF generated successfully at {pdf_path}")

if __name__ == "__main__":
    build_resume_pdf()
