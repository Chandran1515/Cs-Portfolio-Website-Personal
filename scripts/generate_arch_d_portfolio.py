import os
import glob
from io import BytesIO
from PIL import Image as PILImage

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# ARCH D Sheet dimensions in points (1 inch = 72 pt)
PAGE_WIDTH = 36 * 72   # 2592 pt (36 inches)
PAGE_HEIGHT = 24 * 72  # 1728 pt (24 inches)

class ArchDCanvas(canvas.Canvas):
    def __init__(self, filename, **kwargs):
        kwargs['pagesize'] = (PAGE_WIDTH, PAGE_HEIGHT)
        super().__init__(filename, **kwargs)

def draw_cover_sheet(c):
    c.saveState()
    
    # Outer Border
    margin = 36
    c.setStrokeColor(colors.HexColor('#0F172A'))
    c.setLineWidth(3)
    c.rect(margin, margin, PAGE_WIDTH - margin*2, PAGE_HEIGHT - margin*2)
    
    c.setLineWidth(1)
    c.rect(margin + 6, margin + 6, PAGE_WIDTH - margin*2 - 12, PAGE_HEIGHT - margin*2 - 12)

    # Header Box
    c.setFillColor(colors.HexColor('#0F172A'))
    c.rect(margin + 12, PAGE_HEIGHT - margin - 220, PAGE_WIDTH - margin*2 - 24, 208, fill=1, stroke=0)

    c.setFillColor(colors.HexColor('#FFFFFF'))
    c.setFont("Helvetica-Bold", 36)
    c.drawString(margin + 40, PAGE_HEIGHT - margin - 70, "AR. CHANDRAN SHANMUGAM")
    
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor('#38BDF8'))
    c.drawString(margin + 40, PAGE_HEIGHT - margin - 105, "ARCHITECTURAL DESIGN & BIM TECHNICAL DELIVERY PORTFOLIO")
    
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.HexColor('#CBD5E1'))
    c.drawString(margin + 40, PAGE_HEIGHT - margin - 140, "15 Permitted California Building Projects (DD → CD → Permitting → CA)  |  Studio Schicketanz (Carmel-by-the-Sea, CA)")
    c.drawString(margin + 40, PAGE_HEIGHT - margin - 165, "Total Experience: 8+ Years  |  California Experience: 3.5+ Years  |  Email: chandranarch15@gmail.com")

    # Main Profile & Experience Content
    c.setFillColor(colors.HexColor('#0F172A'))
    c.setFont("Helvetica-Bold", 22)
    c.drawString(margin + 40, PAGE_HEIGHT - margin - 280, "EXECUTIVE PROFILE & TECHNICAL CORE COMPETENCIES")

    c.setFont("Helvetica", 15)
    c.setFillColor(colors.HexColor('#334155'))
    profile_lines = [
        "Architect and Technical Delivery Specialist with over 8+ years of total architectural experience, including 3.5+ years of dedicated California high-end",
        "architectural practice at Studio Schicketanz (Carmel-by-the-Sea, CA). Specialized in leading complex multi-component luxury residential estates and",
        "commercial art studios through complete project lifecycles—from Design Development (DD) through Construction Documentation (CD), Permitting, and CA.",
        "",
        "Expert in high-performance building envelope detailing, waterproofing, window/door schedule management, Title 24 energy code compliance, CBC/CRC codes,",
        "and multi-disciplinary BIM coordination (Structural, MEP, Civil, Geotech). Creator of CS Revit Labs—custom C#/Python Revit API tools for automated QA/QC."
    ]
    y_p = PAGE_HEIGHT - margin - 320
    for line in profile_lines:
        c.drawString(margin + 40, y_p, line)
        y_p -= 26

    # Key Statistics Box Grid
    stats = [
        ("8+ YEARS", "Total Arch & BIM Experience"),
        ("3.5+ YEARS", "California Exp (Studio Schicketanz)"),
        ("15 PROJECTS", "Permitted CA Building Sets"),
        ("8 PROJECTS", "As Project Lead Architect"),
        ("REVIT AUTOMATION", "CS Revit Labs C#/Python API Suite")
    ]
    stat_w = 470
    stat_h = 100
    for i, (val, lbl) in enumerate(stats):
        sx = margin + 40 + i * (stat_w + 24)
        sy = y_p - 110
        c.setFillColor(colors.HexColor('#EFF6FF'))
        c.setStrokeColor(colors.HexColor('#BFDBFE'))
        c.setLineWidth(1.5)
        c.roundRect(sx, sy, stat_w, stat_h, 8, fill=1, stroke=1)
        
        c.setFillColor(colors.HexColor('#0066FF'))
        c.setFont("Helvetica-Bold", 22)
        c.drawString(sx + 20, sy + 58, val)
        
        c.setFillColor(colors.HexColor('#475569'))
        c.setFont("Helvetica", 12.5)
        c.drawString(sx + 20, sy + 25, lbl)

    # Drawing Sheet Set Index Box
    y_index = sy - 60
    c.setFillColor(colors.HexColor('#0F172A'))
    c.setFont("Helvetica-Bold", 22)
    c.drawString(margin + 40, y_index, "FULL 24\" × 36\" ARCHITECTURAL DRAWING SHEET INDEX")

    # Index Table Columns
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.HexColor('#0066FF'))
    
    col1 = [
        "SHEET SET 01: CAPPO SCENIC ESTATE (SS-001) — 8 Full Sheets (Main House, ADU, Subterranean Garage, Deck)",
        "SHEET SET 02: PALO ALTO DOLGOV HOUSE (SS-002) — 6 Full Sheets (Site Plan, Floor Plans, Elevations, Sections, Schedules)",
        "SHEET SET 03: CHARL CHERRY ART STUDIO (SS-008) — 4 Full Sheets (Commercial Art Studio, Lighting & Fire Safety)",
        "SHEET SET 04: MOSS HISTORIC RESIDENCE (SS-006) — 4 Full Sheets (Historic Landmark Renovation & Waterproofing)"
    ]
    col2 = [
        "SHEET SET 05: YEUNG REMODEL & STUDIO (SS-005) — 4 Full Sheets (Main House & Detached Studio Working Drawings)",
        "SHEET SET 06: WEISS EMERALD BAY (SS-012) — 4 Full Sheets (Coastal Interior Remodel & Custom Millwork Set)",
        "SHEET SET 07: MCCARTHY, KNOOP, LUNQUIST, KANI, CONNORS, KARTALIS, NELSON, LOT 67 — Full CD Sets",
        "SHEET SET 08: CS REVIT LABS — Proprietary C# & Python Revit Add-in Tools & Batch Automation Suite"
    ]
    
    y_i = y_index - 35
    c.setFont("Helvetica", 13)
    c.setFillColor(colors.HexColor('#334155'))
    for s1, s2 in zip(col1, col2):
        c.drawString(margin + 40, y_i, f"•  {s1}")
        c.drawString(margin + 1260, y_i, f"•  {s2}")
        y_i -= 28

    c.restoreState()


def draw_full_bleed_sheet_page(c, img_path, proj_name, proj_id, sheet_title, sheet_num):
    c.saveState()

    # Sheet outer margin: 18 pt (0.25 inch) for standard architectural plotter margins
    margin = 18
    avail_w = PAGE_WIDTH - (margin * 2)
    avail_h = PAGE_HEIGHT - (margin * 2)

    if img_path and os.path.exists(img_path):
        try:
            with PILImage.open(img_path) as im:
                if im.mode in ('RGBA', 'LA', 'P'):
                    im = im.convert('RGB')
                w, h = im.size
                if w > 0 and h > 0:
                    aspect = h / float(w)
                    target_w = avail_w
                    target_h = target_w * aspect
                    if target_h > avail_h:
                        target_h = avail_h
                        target_w = target_h / aspect
                    
                    offset_x = margin + (avail_w - target_w) / 2.0
                    offset_y = margin + (avail_h - target_h) / 2.0
                    
                    # High quality optimized JPEG stream
                    buf = BytesIO()
                    im.save(buf, format='JPEG', quality=88, optimize=True)
                    buf.seek(0)
                    
                    img_reader = ImageReader(buf)
                    c.drawImage(img_reader, offset_x, offset_y, width=target_w, height=target_h)
        except Exception as e:
            print(f"Error embedding sheet image {img_path}: {e}")

    # Top Subtle Overlay Banner for PDF Navigation
    c.setFillColor(colors.HexColor('#0F172A'))
    c.rect(margin, PAGE_HEIGHT - margin - 32, avail_w, 32, fill=1, stroke=0)
    
    c.setFillColor(colors.HexColor('#FFFFFF'))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 14, PAGE_HEIGHT - margin - 22, f"STUDIO SCHICKETANZ  |  {proj_name.upper()} [{proj_id}]  —  {sheet_title.upper()}")
    
    c.setFillColor(colors.HexColor('#38BDF8'))
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(PAGE_WIDTH - margin - 14, PAGE_HEIGHT - margin - 22, f"SHEET {sheet_num}  |  24\" × 36\" ARCH D FORMAT")

    c.restoreState()


def build_arch_d_pdf():
    output_pdf = os.path.join("docs", "Ar_Chandran_Shanmugam_Portfolio_ARCH_D_24x36.pdf")
    c = ArchDCanvas(output_pdf)

    # 1. Cover Sheet (Page 1)
    draw_cover_sheet(c)
    c.showPage()

    # Define all project drawing sheet image files to embed on dedicated 24x36 pages
    sheet_sequence = [
        # CAPPO SCENIC ESTATE (SS-001)
        ("Cappo Scenic Coastal Estate", "SS-001", "Cover & Render View", "images/projects/cappo/cover.png", "A1.01"),
        ("Cappo Scenic Coastal Estate", "SS-001", "Overall Site & Floor Plan", "images/projects/cappo/cappo_1.png", "A1.02"),
        ("Cappo Scenic Coastal Estate", "SS-001", "Main House Framing & Foundation Plan", "images/projects/cappo/Cappo_2.png", "A1.03"),
        ("Cappo Scenic Coastal Estate", "SS-001", "Detached ADU Plan & Elevations", "images/projects/cappo/cappo adu_1.png", "A1.04"),
        ("Cappo Scenic Coastal Estate", "SS-001", "Detached ADU Construction Details", "images/projects/cappo/cappo adu_2.png", "A1.05"),
        ("Cappo Scenic Coastal Estate", "SS-001", "Subterranean Garage & Deck Plan", "images/projects/cappo/cappo deck_1.png", "A1.06"),
        ("Cappo Scenic Coastal Estate", "SS-001", "Exterior Wall Sections & Detailing", "images/projects/cappo/Cappo_4.png", "A1.07"),
        ("Cappo Scenic Coastal Estate", "SS-001", "Window/Door Schedules & Millwork", "images/projects/cappo/Cappo_5.png", "A1.08"),

        # PALO ALTO DOLGOV HOUSE (SS-002)
        ("Palo Alto Dolgov Residence", "SS-002", "Cover Sheet & Sheet Index", "images/projects/dolgov/cover.png", "A2.01"),
        ("Palo Alto Dolgov Residence", "SS-002", "Architectural Site & Floor Plan", "images/projects/dolgov/DOL M_0.png", "A2.02"),
        ("Palo Alto Dolgov Residence", "SS-002", "Exterior Building Elevations", "images/projects/dolgov/DOL M_1.png", "A2.03"),
        ("Palo Alto Dolgov Residence", "SS-002", "Building Sections & Assembly Details", "images/projects/dolgov/DOL M_2.png", "A2.04"),
        ("Palo Alto Dolgov Residence", "SS-002", "Enclosure Waterproofing & Callouts", "images/projects/dolgov/DOL M_3.png", "A2.05"),
        ("Palo Alto Dolgov Residence", "SS-002", "Door/Window Schedules & Energy Notes", "images/projects/dolgov/DOL M_4.png", "A2.06"),

        # CHARL CHERRY ART STUDIO (SS-008)
        ("Charl Cherry Commercial Art Studio", "SS-008", "3D Rendering & Cover View", "images/projects/charl-cherry/1_carl cherry.png", "A3.01"),
        ("Charl Cherry Commercial Art Studio", "SS-008", "Commercial Floor Plan & Layout", "images/projects/charl-cherry/2_carl cherry.png", "A3.02"),
        ("Charl Cherry Commercial Art Studio", "SS-008", "Building Sections & High-Ceiling Details", "images/projects/charl-cherry/3_carl cherry.png", "A3.03"),
        ("Charl Cherry Commercial Art Studio", "SS-008", "Exterior Cladding & Lighting Details", "images/projects/charl-cherry/4_carl cherry.png", "A3.04"),

        # MOSS HISTORIC RESIDENCE (SS-006)
        ("Moss Historic Landmark Residence", "SS-006", "Cover Sheet & Site Plan", "images/projects/moss/Moss.jpg", "A4.01"),
        ("Moss Historic Landmark Residence", "SS-006", "Historic Elevations & Timber Framing", "images/projects/moss/1_Moss.png", "A4.02"),
        ("Moss Historic Landmark Residence", "SS-006", "Building Sections & Exterior Waterproofing", "images/projects/moss/2_Moss.png", "A4.03"),
        ("Moss Historic Landmark Residence", "SS-006", "Millwork & Interior Finishes", "images/projects/moss/3_Moss.png", "A4.04"),

        # YEUNG REMODEL & STUDIO (SS-005)
        ("Yeung House & Detached Studio", "SS-005", "Main House Cover & Render", "images/projects/yeung-studio/Yeung.png", "A5.01"),
        ("Yeung House & Detached Studio", "SS-005", "Main House Floor Plan & Revisions", "images/projects/yeung-main-house-remodel/1_yeung MH.png", "A5.02"),
        ("Yeung House & Detached Studio", "SS-005", "Detached Studio Architectural Set", "images/projects/yeung-studio/1_yeung studio.png", "A5.03"),
        ("Yeung House & Detached Studio", "SS-005", "Exterior Cladding & Roof Details", "images/projects/yeung-studio/2_yeung studio.png", "A5.04"),

        # WEISS EMERALD BAY (SS-012)
        ("Weiss Emerald Bay Coastal Remodel", "SS-012", "Cover & Coastal View", "images/projects/weiss/weiss.png", "A6.01"),
        ("Weiss Emerald Bay Coastal Remodel", "SS-012", "Interior Architectural Elevations", "images/projects/weiss/weiss_1.png", "A6.02"),
        ("Weiss Emerald Bay Coastal Remodel", "SS-012", "Custom Cabinetry & Millwork Details", "images/projects/weiss/weiss_2.png", "A6.03"),
        ("Weiss Emerald Bay Coastal Remodel", "SS-012", "Mechanical & Lighting Reflected Ceiling Plan", "images/projects/weiss/weiss_3.png", "A6.04"),

        # MCCARTHY RESIDENCE (SS-014)
        ("McCarthy Residence Set", "SS-014", "Cover Sheet & Render", "images/projects/mccarthy/Mccarthy.jpg", "A7.01"),
        ("McCarthy Residence Set", "SS-014", "Architectural Working Drawings", "images/projects/mccarthy/1_Mccarthy.png", "A7.02"),

        # KNOOP 250 (SS-004)
        ("Knoop 250 Residence", "SS-004", "Cover Sheet & Render", "images/projects/knoop/knoop 250.png", "A8.01"),
        ("Knoop 250 Residence", "SS-004", "Floor Plan & Building Sections", "images/projects/knoop/1_ Knoop 250.png", "A8.02"),

        # LUNQUIST RESIDENCE (SS-010)
        ("Lunquist Residence", "SS-010", "Cover Sheet & Render", "images/projects/lunquist/Lundquist.jpg", "A9.01"),
        ("Lunquist Residence", "SS-010", "Architectural Working Drawings", "images/projects/lunquist/lunquist_1.png", "A9.02"),

        # KANI REMODEL (SS-003)
        ("Kani Remodel Residence", "SS-003", "Cover Sheet & Render", "images/projects/kani/kani.jpg", "A10.01"),
        ("Kani Remodel Residence", "SS-003", "Floor Plan & Elevation Details", "images/projects/kani/1_kani remodel.png", "A10.02"),

        # CONNORS RESIDENCE (SS-009)
        ("Connors Residence", "SS-009", "Cover Sheet & Render", "images/projects/connors/connors.png", "A11.01"),
        ("Connors Residence", "SS-009", "Architectural Working Drawings", "images/projects/connors/1_Connors.png", "A11.02"),

        # KARTALIS RESIDENCE (SS-011)
        ("Kartalis Residence", "SS-011", "Cover Sheet & Render", "images/projects/kartalis/kartalis cover.png", "A12.01"),
        ("Kartalis Residence", "SS-011", "Architectural Working Drawings", "images/projects/kartalis/1_kartalis .png", "A12.02"),

        # NELSON'S RESIDENCE (SS-007)
        ("Nelson's Residence", "SS-007", "Cover Sheet & Render", "images/projects/nelson/Nelson.jpg", "A13.01"),
        ("Nelson's Residence", "SS-007", "Architectural Working Drawings", "images/projects/nelson/1_nelson.png", "A13.02"),

        # LOT 67 (SS-015)
        ("Lot 67 Construction Set", "SS-015", "Cover Sheet & Render", "images/projects/lot67/lot 67.jpg", "A14.01"),
        ("Lot 67 Construction Set", "SS-015", "Architectural Working Drawings", "images/projects/lot67/1_lot 67.png", "A14.02"),

        # CS REVIT LABS (BIM AUTOMATION)
        ("CS Revit Labs BIM Automation Suite", "BIM-01", "Custom C# & Python Revit Add-in Tools", "images/projects/CS Revit Labs/cs revit labs plugin SS.jpg", "BIM-1.01")
    ]

    total_sheets = len(sheet_sequence)
    print(f"Generating ARCH D PDF set with {total_sheets + 1} dedicated 24x36 sheets...")

    for proj_name, proj_id, title, img_path, sheet_num in sheet_sequence:
        draw_full_bleed_sheet_page(c, img_path, proj_name, proj_id, title, sheet_num)
        c.showPage()

    c.save()
    print(f"Successfully generated full-sheet ARCH D PDF portfolio at: {output_pdf}")

if __name__ == '__main__':
    build_arch_d_pdf()
