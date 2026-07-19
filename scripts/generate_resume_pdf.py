import os

def create_resume_pdf(output_path):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Text helper for escaping special characters in PDF string
    def pdf_escape(text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    # Object map references
    catalog_ref = "1 0 R"
    pages_ref = "2 0 R"
    page1_ref = "3 0 R"
    font_reg_ref = "5 0 R"
    font_bold_ref = "6 0 R"
    page2_ref = "7 0 R"
    page3_ref = "9 0 R"

    # Margin settings
    left_margin = 54
    right_margin = 54
    page_width = 595.28
    page_height = 841.89
    
    # Professional dark blue header color: RGB (0.17, 0.37, 0.54) -> #2C5F8A
    color_blue = "0.17 0.37 0.54 rg"
    color_black = "0 0 0 rg"
    color_gray = "0.35 0.35 0.35 rg"

    # Helper for wrapping paragraphs
    def wrap_text(text, max_chars):
        words = text.split(' ')
        lines = []
        curr_line = []
        curr_len = 0
        for w in words:
            if curr_len + len(w) + 1 > max_chars:
                lines.append(' '.join(curr_line))
                curr_line = [w]
                curr_len = len(w)
            else:
                curr_line.append(w)
                curr_len += len(w) + 1
        if curr_line:
            lines.append(' '.join(curr_line))
        return lines

    # ------------------ PAGE 1 GENERATOR ------------------
    page1_stream = []
    
    # Left Column (X=54 to X=360)
    p1_left_y = 790
    
    def p1_left_text(text, font, size, dy=0, is_para=False, max_c=58, line_h=13, color=color_black):
        nonlocal p1_left_y
        p1_left_y += dy
        page1_stream.append(color)
        
        if is_para:
            lines = wrap_text(text, max_c)
            for idx, line in enumerate(lines):
                esc_line = pdf_escape(line)
                page1_stream.append(f"BT /{font} {size} Tf {left_margin} {p1_left_y} Td ({esc_line}) Tj ET")
                if idx < len(lines) - 1:
                    p1_left_y -= line_h
            p1_left_y -= 4
        else:
            page1_stream.append(f"BT /{font} {size} Tf {left_margin} {p1_left_y} Td ({pdf_escape(text)}) Tj ET")

    # Right Column (X=390 to X=540)
    p1_right_y = 790
    p1_right_x = 390
    
    def p1_right_text(text, font, size, dy=0, is_para=False, max_c=32, line_h=12, color=color_black):
        nonlocal p1_right_y
        p1_right_y += dy
        page1_stream.append(color)
        
        if is_para:
            lines = wrap_text(text, max_c)
            for idx, line in enumerate(lines):
                esc_line = pdf_escape(line)
                page1_stream.append(f"BT /{font} {size} Tf {p1_right_x} {p1_right_y} Td ({esc_line}) Tj ET")
                if idx < len(lines) - 1:
                    p1_right_y -= line_h
            p1_right_y -= 4
        else:
            page1_stream.append(f"BT /{font} {size} Tf {p1_right_x} {p1_right_y} Td ({pdf_escape(text)}) Tj ET")

    # Name & Subtitle (Left column)
    p1_left_text("CHANDRAN S", "F2", 28, color=color_black)
    
    summary_text = (
        "Architect and BIM Specialist with over 7.7 years of professional experience, "
        "including 1.5 years of specialized Dynamo programming (Python). Expertise in "
        "Revit (Architecture, Structure, MEP) and computational design, delivering "
        "automation solutions."
    )
    p1_left_text(summary_text, "F1", 9.5, -24, is_para=True, max_c=58, line_h=13)
    
    # Left Column: EXPERIENCE
    p1_left_text("EXPERIENCE", "F2", 11, -20, color=color_blue)
    
    # Job 1: Studio Schicketanz
    p1_left_y -= 15
    p1_left_text("Studio Schicketanz, Bangalore -- Architectural Job Captain", "F2", 9.5, color=color_black)
    p1_left_text("DEC 2022 - PRESENT", "F2", 7.5, -11, color=color_gray)
    job1_desc = (
        "Lead Revit modelling and production of construction documentation (LOD 300-400) for luxury "
        "residential projects. Delivered full construction support and documentation for 4+ high-class "
        "residences in Carmel-by-the-Sea, CA."
    )
    p1_left_text(job1_desc, "F1", 9, -12, is_para=True, max_c=62, line_h=12)
    
    # Job 2: Jarinam Parallel Space
    p1_left_y -= 10
    p1_left_text("Jarinam Parallel Space, Bangalore -- Architect", "F2", 9.5, color=color_black)
    p1_left_text("DEC 2021 - DEC 2022", "F2", 7.5, -11, color=color_gray)
    job2_desc = (
        "Produced detailed construction documentation and coordinated with consultants for mid-size "
        "projects. Created Revit models (LOD 300-350) for residential and commercial projects."
    )
    p1_left_text(job2_desc, "F1", 9, -12, is_para=True, max_c=62, line_h=12)
    
    # Job 3: Pinnacle Technology Services
    p1_left_y -= 10
    p1_left_text("Pinnacle Technology Services, Hyderabad -- Revit Jr. Modeller", "F2", 9.5, color=color_black)
    p1_left_text("JUL 2021 - DEC 2021", "F2", 7.5, -11, color=color_gray)
    job3_desc = (
        "Delivered BIM services for international clients (Netherlands housing projects). Developed "
        "coordinated Revit models and ensured quality compliance."
    )
    p1_left_text(job3_desc, "F1", 9, -12, is_para=True, max_c=62, line_h=12)
    
    # Job 4: Neural Design & Constructions
    p1_left_y -= 10
    p1_left_text("Neural Design & Constructions (P) Ltd, Madurai -- Architect", "F2", 9.5, color=color_black)
    p1_left_text("JUN 2019 - JUN 2021", "F2", 7.5, -11, color=color_gray)
    job4_desc = (
        "Delivered architectural design and BIM coordination for residential and commercial projects."
    )
    p1_left_text(job4_desc, "F1", 9, -12, is_para=True, max_c=62, line_h=12)
    
    # Job 5: Freelance Architect
    p1_left_y -= 10
    p1_left_text("Freelance Architect, Madurai -- Architect", "F2", 9.5, color=color_black)
    p1_left_text("SEP 2017 - JUN 2019", "F2", 7.5, -11, color=color_gray)
    job5_desc = (
        "Managed residential and public projects concept design, development, procurement, and supervision."
    )
    p1_left_text(job5_desc, "F1", 9, -12, is_para=True, max_c=62, line_h=12)

    # Right Column Content
    p1_right_text("LinkedIn:", "F2", 9, color=color_black)
    p1_right_text("www.linkedin.com/in/ar-chandr", "F1", 9, -12)
    p1_right_text("an-shanmugam-421b7b149", "F1", 9, -11)
    p1_right_text("Bangalore | KA | India", "F2", 9, -15)
    p1_right_text("+91 7904053633", "F2", 9, -14)
    p1_right_text("7904053633CR@GMAIL.COM", "F2", 9, -14)
    
    # Right Column: SKILLS
    p1_right_text("SKILLS", "F2", 11, -28, color=color_blue)
    p1_right_y -= 14
    
    skills = [
        "Dynamo (Python scripting,\nRevit automation)",
        "Python (custom nodes/logic),\nC# (basic Revit API)",
        "Autodesk Revit (Arch, Struct,\nMEP, LOD 300-400)",
        "Computational geometry\n(Rhino & Grasshopper)",
        "AutoCAD, SketchUp & V-Ray,\nLumion, 3ds Max",
        "Adobe Photoshop, InDesign,\nMicrosoft Office"
    ]
    for s in skills:
        p1_right_text(s, "F1", 9, is_para=True, max_c=25, line_h=11)
        p1_right_y -= 5
        
    # Right Column: LANGUAGES
    p1_right_text("LANGUAGES", "F2", 11, -15, color=color_blue)
    p1_right_text("English, Tamil", "F1", 9, -15, color=color_black)

    page1_stream_content = "\n".join(page1_stream).encode('latin1')
    page1_stream_len = len(page1_stream_content)

    # ------------------ PAGE 2 GENERATOR ------------------
    page2_stream = []
    p2_y = 790
    
    def p2_text(text, font, size, dy=0, is_para=False, max_c=80, line_h=13, color=color_black, x=left_margin):
        nonlocal p2_y
        p2_y += dy
        page2_stream.append(color)
        
        if is_para:
            lines = wrap_text(text, max_c)
            for idx, line in enumerate(lines):
                esc_line = pdf_escape(line)
                page2_stream.append(f"BT /{font} {size} Tf {x} {p2_y} Td ({esc_line}) Tj ET")
                if idx < len(lines) - 1:
                    p2_y -= line_h
            p2_y -= 4
        else:
            page2_stream.append(f"BT /{font} {size} Tf {x} {p2_y} Td ({pdf_escape(text)}) Tj ET")

    # Education Section
    p2_text("EDUCATION", "F2", 11, color=color_blue)
    p2_y -= 15
    p2_text("Meenakshi College of Engineering, Chennai -- Master of Architecture", "F2", 10)
    p2_text("2017 - 2019  |  CGPA: 7.55/10", "F1", 9, -13, color=color_gray)
    
    p2_y -= 14
    p2_text("Tamilnadu School of Architecture, Coimbatore -- Bachelor of Architecture", "F2", 10)
    p2_text("2012 - 2017  |  CGPA: 7.02/10", "F1", 9, -13, color=color_gray)

    # Projects Section
    p2_text("PROJECTS", "F2", 11, -24, color=color_blue)
    p2_text("Featured Projects", "F2", 10, -16)
    
    featured_projects = [
        "4 High-end Residences, Carmel-by-the-Sea, CA",
        "Star Palms, Banaswadi, Bengaluru",
        "Commercial Complex, 100FT Road, Bengaluru",
        "PHC, Chennai",
        "Pandian Nagar Row House, Madurai",
        "Hafeez Contractor Apartments, Pune",
        "Lane Cove Warehouse, Australia",
        "Dubai Warehouse"
    ]
    p2_y -= 6
    for fp in featured_projects:
        p2_y -= 12
        page2_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p2_y} Td (\\225) Tj ET")
        page2_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p2_y} Td ({pdf_escape(fp)}) Tj ET")

    # Key Projects & Deliverables
    p2_text("KEY PROJECTS & DELIVERABLES", "F2", 11, -22, color=color_blue)
    p2_text("Project Lead & Delivery:", "F2", 10, -16)
    
    lead_projects = [
        ("Dolgov Main House (SS-002), Palo Alto, CA: ", "Led full BIM modeling, detailing, and permit packages for residential remodel."),
        ("Cappo Scenic (SS-001), Monterey County, CA: ", "Managed lifecycle delivery, including planning approvals, permits, and contractor coordination for multi-component remodel."),
        ("Charl Cherry Art Studio (SS-008), Monterey County, CA: ", "Led ADA compliance, permit submissions, and MEP coordination for commercial construction."),
        ("Moss Residence (SS-006) & Yeung Remodel (SS-005): ", "Directed design, coordination, and permit packages for historical building remodels."),
        ("McCarthy Residence (SS-014), Knoop 250 (SS-004), & Weiss Emerald Bay (SS-012): ", "Spearheaded BIM modeling, documentation, and coordination for residential projects.")
    ]
    
    for title, desc in lead_projects:
        p2_y -= 15
        full_text = title + desc
        
        # Word wrap the full text
        lines = wrap_text(full_text, 78)
        
        # Draw bullet point
        page2_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p2_y} Td (\\225) Tj ET")
        
        for idx, line in enumerate(lines):
            # Check if this line starts with the bold part
            if idx == 0:
                # We can print the bold part and then regular text.
                # To keep it simple in PDF, let's look for character index of title in line
                if title in line:
                    rem_line = line[len(title):]
                    page2_stream.append(f"BT /F2 9.5 Tf {left_margin + 16} {p2_y} Td ({pdf_escape(title)}) Tj ET")
                    # Calculate approximate width of title to start regular text
                    # Bold Helvetica 9.5pt ~ 6pt width per character
                    shift_x = left_margin + 16 + (len(title) * 4.9)
                    page2_stream.append(f"BT /F1 9.5 Tf {shift_x} {p2_y} Td ({pdf_escape(rem_line)}) Tj ET")
                else:
                    page2_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p2_y} Td ({pdf_escape(line)}) Tj ET")
            else:
                page2_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p2_y} Td ({pdf_escape(line)}) Tj ET")
                
            if idx < len(lines) - 1:
                p2_y -= 12

    page2_stream_content = "\n".join(page2_stream).encode('latin1')
    page2_stream_len = len(page2_stream_content)

    # ------------------ PAGE 3 GENERATOR ------------------
    page3_stream = []
    p3_y = 790
    
    def p3_text(text, font, size, dy=0, is_para=False, max_c=80, line_h=13, color=color_black, x=left_margin):
        nonlocal p3_y
        p3_y += dy
        page3_stream.append(color)
        
        if is_para:
            lines = wrap_text(text, max_c)
            for idx, line in enumerate(lines):
                esc_line = pdf_escape(line)
                page3_stream.append(f"BT /{font} {size} Tf {x} {p3_y} Td ({esc_line}) Tj ET")
                if idx < len(lines) - 1:
                    p3_y -= line_h
            p3_y -= 4
        else:
            page3_stream.append(f"BT /{font} {size} Tf {x} {p3_y} Td ({pdf_escape(text)}) Tj ET")

    # Technical Collaboration
    p3_text("Technical Collaboration & Team Support:", "F2", 10, color=color_black)
    
    team_projects_title = "Lunquist Residence (SS-010), Kani Remodel (SS-003), Connors Residence (SS-009), Bayview (SS-013), Kartalis Residence (SS-011), Nelson's Residence (SS-007), & Lot 67 (SS-015): "
    team_projects_desc = "Supported CD production, Revit modeling (LOD 300-350), and multi-discipline coordination."
    full_team_text = team_projects_title + team_projects_desc
    
    p3_y -= 15
    lines = wrap_text(full_team_text, 78)
    page3_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p3_y} Td (\\225) Tj ET")
    
    for idx, line in enumerate(lines):
        if idx == 0:
            # We can print the bold part and then regular text.
            if team_projects_title in line:
                rem_line = line[len(team_projects_title):]
                page3_stream.append(f"BT /F2 9.5 Tf {left_margin + 16} {p3_y} Td ({pdf_escape(team_projects_title)}) Tj ET")
                # Calculate approximate width of title
                shift_x = left_margin + 16 + (len(team_projects_title) * 4.9)
                page3_stream.append(f"BT /F1 9.5 Tf {shift_x} {p3_y} Td ({pdf_escape(rem_line)}) Tj ET")
            else:
                # If the title wraps, print title first as multi-line bold
                # But for our text it fits or wraps. To be safe:
                page3_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p3_y} Td ({pdf_escape(line)}) Tj ET")
        else:
            page3_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p3_y} Td ({pdf_escape(line)}) Tj ET")
        if idx < len(lines) - 1:
            p3_y -= 12

    # BIM Automation Suite
    p3_text("BIM AUTOMATION SUITE: CS REVIT LABS", "F2", 11, -30, color=color_blue)
    p3_text("Developed using C# (.NET Framework 4.8), Revit API, WPF/XAML, Python, and Google Gemini API.", "F1", 9.5, -15, color=color_gray)
    
    labs_bullets = [
        ("Model Management: ", "Automated backup, batch worksets, and coordination sets."),
        ("Documentation & Annotation: ", "Bulk-generated floor plans/elevations (SheetCraft), Keynote/Detail browsers, and auto-tagging."),
        ("QA/QC & Graphics: ", "Graphic QC checks, project spell check via LLM integration, and line style organization."),
        ("MEP & Developer Tools: ", "Appliance placement automation, batch export sets, and code sandbox for live scripting.")
    ]
    
    p3_y -= 10
    for title, desc in labs_bullets:
        p3_y -= 18
        full_bullet = title + desc
        lines = wrap_text(full_bullet, 78)
        
        # Bullet dot
        page3_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p3_y} Td (\\225) Tj ET")
        
        for idx, line in enumerate(lines):
            if idx == 0:
                if title in line:
                    rem_line = line[len(title):]
                    page3_stream.append(f"BT /F2 9.5 Tf {left_margin + 16} {p3_y} Td ({pdf_escape(title)}) Tj ET")
                    shift_x = left_margin + 16 + (len(title) * 4.9)
                    page3_stream.append(f"BT /F1 9.5 Tf {shift_x} {p3_y} Td ({pdf_escape(rem_line)}) Tj ET")
                else:
                    page3_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p3_y} Td ({pdf_escape(line)}) Tj ET")
            else:
                page3_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p3_y} Td ({pdf_escape(line)}) Tj ET")
            if idx < len(lines) - 1:
                p3_y -= 12

    page3_stream_content = "\n".join(page3_stream).encode('latin1')
    page3_stream_len = len(page3_stream_content)

    # ------------------ DEFINE ALL PDF OBJECTS ------------------
    obj_catalog = f"<< /Type /Catalog /Pages {pages_ref} >>".encode('latin1')
    obj_pages = f"<< /Type /Pages /Kids [{page1_ref} {page2_ref} {page3_ref}] /Count 3 >>".encode('latin1')
    
    obj_page1 = f"<< /Type /Page /Parent {pages_ref} /Resources << /Font << /F1 {font_reg_ref} /F2 {font_bold_ref} >> >> /MediaBox [0 0 {page_width} {page_height}] /Contents 4 0 R >>".encode('latin1')
    obj_page1_content = f"<< /Length {page1_stream_len} >>\nstream\n".encode('latin1') + page1_stream_content + "\nendstream".encode('latin1')
    
    obj_font_reg = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>".encode('latin1')
    obj_font_bold = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>".encode('latin1')
    
    obj_page2 = f"<< /Type /Page /Parent {pages_ref} /Resources << /Font << /F1 {font_reg_ref} /F2 {font_bold_ref} >> >> /MediaBox [0 0 {page_width} {page_height}] /Contents 8 0 R >>".encode('latin1')
    obj_page2_content = f"<< /Length {page2_stream_len} >>\nstream\n".encode('latin1') + page2_stream_content + "\nendstream".encode('latin1')

    obj_page3 = f"<< /Type /Page /Parent {pages_ref} /Resources << /Font << /F1 {font_reg_ref} /F2 {font_bold_ref} >> >> /MediaBox [0 0 {page_width} {page_height}] /Contents 10 0 R >>".encode('latin1')
    obj_page3_content = f"<< /Length {page3_stream_len} >>\nstream\n".encode('latin1') + page3_stream_content + "\nendstream".encode('latin1')

    # Object map
    pdf_objs = [
        (1, obj_catalog),
        (2, obj_pages),
        (3, obj_page1),
        (4, obj_page1_content),
        (5, obj_font_reg),
        (6, obj_font_bold),
        (7, obj_page2),
        (8, obj_page2_content),
        (9, obj_page3),
        (10, obj_page3_content)
    ]
    
    # Compile bytes
    pdf_bytes = bytearray()
    pdf_bytes.extend(b"%PDF-1.4\n")
    
    offsets = {}
    for obj_id, content in pdf_objs:
        offsets[obj_id] = len(pdf_bytes)
        pdf_bytes.extend(f"{obj_id} 0 obj\n".encode('latin1'))
        pdf_bytes.extend(content)
        pdf_bytes.extend("\nendobj\n".encode('latin1'))
        
    start_xref = len(pdf_bytes)
    
    xref_header = f"xref\n0 {len(pdf_objs) + 1}\n0000000000 65535 f \n".encode('latin1')
    pdf_bytes.extend(xref_header)
    
    for i in range(1, len(pdf_objs) + 1):
        pdf_bytes.extend(f"{offsets[i]:010d} 00000 n \n".encode('latin1'))
        
    trailer = f"trailer\n<< /Size {len(pdf_objs) + 1} /Root {catalog_ref} >>\nstartxref\n{start_xref}\n%%EOF\n".encode('latin1')
    pdf_bytes.extend(trailer)
    
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

if __name__ == "__main__":
    out_file = os.path.abspath(r"c:\Users\tissu\source\repos\Cs Protfolio website_personal\docs\Ar_Chandran_Shanmugam_Resume.pdf")
    create_resume_pdf(out_file)
    print(f"Final 3-page Resume PDF successfully generated at {out_file}")
