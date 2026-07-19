import os

def create_resume_pdf(output_path):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Text helper for escaping special characters in PDF string
    def pdf_escape(text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    # We will accumulate PDF objects
    objects = []
    
    # Add an object to our list and return its object ID reference string
    def add_object(obj_content):
        obj_id = len(objects) + 1
        objects.append((obj_id, obj_content))
        return f"{obj_id} 0 R"

    # Forward references
    catalog_ref = "1 0 R"
    pages_ref = "2 0 R"
    page1_ref = "3 0 R"
    page2_ref = "7 0 R"
    font_reg_ref = "5 0 R"
    font_bold_ref = "6 0 R"

    # Define content structures for Page 1 and Page 2
    # Margin settings
    left_margin = 54
    page_width = 595.28
    page_height = 841.89
    text_width = page_width - (left_margin * 2) # 487.28 points (~80 characters wide at 9-10pt font)
    
    # ------------------ PAGE 1 GENERATOR ------------------
    page1_stream = []
    
    # State tracker for text layout
    p1_y = 790 # Current Y cursor position on page 1
    
    def p1_text(text, font_ref_name, size, dy=0, is_para=False):
        nonlocal p1_y
        p1_y += dy
        
        # Format text to pdf escaped string
        esc_text = pdf_escape(text)
        
        if is_para:
            # Word wrap paragraph text at ~85 characters
            words = text.split(' ')
            lines = []
            curr_line = []
            curr_len = 0
            for w in words:
                if curr_len + len(w) + 1 > 85:
                    lines.append(' '.join(curr_line))
                    curr_line = [w]
                    curr_len = len(w)
                else:
                    curr_line.append(w)
                    curr_len += len(w) + 1
            if curr_line:
                lines.append(' '.join(curr_line))
                
            for idx, line in enumerate(lines):
                esc_line = pdf_escape(line)
                page1_stream.append(f"BT /{font_ref_name} {size} Tf {left_margin} {p1_y} Td ({esc_line}) Tj ET")
                if idx < len(lines) - 1:
                    p1_y -= (size + 4)
            p1_y -= 4
        else:
            page1_stream.append(f"BT /{font_ref_name} {size} Tf {left_margin} {p1_y} Td ({esc_text}) Tj ET")

    # Header
    p1_text("CHANDRAN S", "F2", 22) # F2 is Helvetica-Bold
    p1_text("Dynamo Programmer | Revit & BIM Specialist", "F2", 11, -16)
    p1_text("Phone: +91 8526590200 / +91 7904053633  |  Email: 7904053633CR@GMAIL.COM", "F1", 9, -15) # F1 is Helvetica
    p1_text("LinkedIn: www.linkedin.com/in/ar-chandran-shanmugam-421b7b149", "F1", 9, -12)
    
    # Horizontal line
    p1_y -= 10
    page1_stream.append(f"0.5 w 0.2 G {left_margin} {p1_y} m {page_width - left_margin} {p1_y} l S 0 G")
    
    # Professional Summary
    p1_text("PROFESSIONAL SUMMARY", "F2", 11, -22)
    summary_text = (
        "Architect and BIM Specialist with over 6.5 years of professional experience, "
        "including 1.5 years of specialized Dynamo programming (Python). Expertise in Revit "
        "(Architecture, Structure, MEP) and computational design, delivering automation solutions "
        "to improve efficiency in modelling and documentation. Skilled in Python scripting within "
        "Dynamo, custom node/package creation, and basic C# for Revit API applications. Proven "
        "track record of leading BIM workflows, producing high-quality construction documentation, "
        "and collaborating across disciplines on international and high-end residential/commercial "
        "projects."
    )
    p1_text(summary_text, "F1", 9.5, -15, is_para=True)
    
    # Technical Skills
    p1_text("TECHNICAL SKILLS", "F2", 11, -15)
    skills = [
        "Dynamo (1.5 years hands-on experience with Python scripting) -- automation of Revit workflows",
        "Python -- scripting for custom Dynamo nodes and logic sequences",
        "Autodesk Revit (Architecture, Structural, MEP) -- modelling, families, LOD 300-400",
        "C# -- basic understanding; applying for custom Dynamo/Revit API development",
        "Computational geometry -- Rhino & Grasshopper",
        "AutoCAD, SketchUp & V-Ray, Lumion, 3ds Max",
        "Adobe Photoshop, Adobe InDesign",
        "Microsoft Office, BIM coordination and cross-discipline communication"
    ]
    p1_y -= 8
    for skill in skills:
        p1_text("-", "F2", 9.5, -13)
        # Shift text right by 10 points for bullet list
        page1_stream.append(f"BT /F1 9.5 Tf {left_margin + 12} {p1_y} Td ({pdf_escape(skill)}) Tj ET")

    # Professional Experience
    p1_text("PROFESSIONAL EXPERIENCE", "F2", 11, -22)
    
    # Job 1: Studio Schicketanz
    p1_y -= 8
    p1_text("Architectural Job Captain", "F2", 10)
    page1_stream.append(f"BT /F1 9.5 Tf 190 {p1_y} Td (-- Studio Schicketanz, Bangalore) Tj ET")
    page1_stream.append(f"BT /F2 9.5 Tf 400 {p1_y} Td (Dec 2022 - Present | 3 yrs 7 mos) Tj ET")
    
    schicketanz_bullets = [
        "Lead Revit modelling and production of construction documentation (LOD 300-400) for luxury residential projects.",
        "Delivered full construction support and documentation for 4 + high-class residences in Carmel-by-the-Sea, CA -- including RFIs and client coordination.",
        "Developed Dynamo scripts and Python-based automation for repetitive documentation tasks, schedules, and detailing.",
        "Implemented BIM workflows and standards across teams, mentoring junior modelers.",
        "Coordinated effectively with structural and MEP consultants to maintain discipline compliance."
    ]
    for bullet in schicketanz_bullets:
        p1_y -= 13
        # Bullets need custom wrapping
        words = bullet.split(' ')
        lines = []
        curr_line = []
        curr_len = 0
        for w in words:
            if curr_len + len(w) + 1 > 80:
                lines.append(' '.join(curr_line))
                curr_line = [w]
                curr_len = len(w)
            else:
                curr_line.append(w)
                curr_len += len(w) + 1
        if curr_line:
            lines.append(' '.join(curr_line))
            
        # Draw the dot (using standard bullet character code in octal/ISO Latin 1: \225)
        page1_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p1_y} Td (\\225) Tj ET")
        for idx, line in enumerate(lines):
            page1_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p1_y} Td ({pdf_escape(line)}) Tj ET")
            if idx < len(lines) - 1:
                p1_y -= 13
    
    # Job 2: Jarinam Parallel Space
    p1_y -= 18
    p1_text("Architect", "F2", 10)
    page1_stream.append(f"BT /F1 9.5 Tf 110 {p1_y} Td (-- Jarinam Parallel Space, Bangalore) Tj ET")
    page1_stream.append(f"BT /F2 9.5 Tf 450 {p1_y} Td (Dec 2021 - Dec 2022 | 1 yr) Tj ET")
    
    jarinam_bullets = [
        "Produced detailed construction documentation and coordinated with consultants for mid-size projects.",
        "Conducted site visits, design reviews, and implemented revisions within Revit models.",
        "Created Revit models (LOD 300-350) for residential and commercial projects (Hosur residence, FM Silks, Pune apartments).",
        "Coordinated drawings, vendors, and consultants for timely deliverables.",
        "Supported international BIM projects (Australian and Dubai warehouse packages)."
    ]
    for bullet in jarinam_bullets:
        p1_y -= 13
        words = bullet.split(' ')
        lines = []
        curr_line = []
        curr_len = 0
        for w in words:
            if curr_len + len(w) + 1 > 80:
                lines.append(' '.join(curr_line))
                curr_line = [w]
                curr_len = len(w)
            else:
                curr_line.append(w)
                curr_len += len(w) + 1
        if curr_line:
            lines.append(' '.join(curr_line))
            
        page1_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p1_y} Td (\\225) Tj ET")
        for idx, line in enumerate(lines):
            page1_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p1_y} Td ({pdf_escape(line)}) Tj ET")
            if idx < len(lines) - 1:
                p1_y -= 13

    # Assemble page 1 stream content
    page1_stream_content = "\n".join(page1_stream).encode('latin1')
    page1_stream_len = len(page1_stream_content)
    
    
    # ------------------ PAGE 2 GENERATOR ------------------
    page2_stream = []
    p2_y = 790 # Current Y cursor position on page 2
    
    def p2_text(text, font_ref_name, size, dy=0, is_para=False):
        nonlocal p2_y
        p2_y += dy
        esc_text = pdf_escape(text)
        if is_para:
            words = text.split(' ')
            lines = []
            curr_line = []
            curr_len = 0
            for w in words:
                if curr_len + len(w) + 1 > 85:
                    lines.append(' '.join(curr_line))
                    curr_line = [w]
                    curr_len = len(w)
                else:
                    curr_line.append(w)
                    curr_len += len(w) + 1
            if curr_line:
                lines.append(' '.join(curr_line))
            for idx, line in enumerate(lines):
                esc_line = pdf_escape(line)
                page2_stream.append(f"BT /{font_ref_name} {size} Tf {left_margin} {p2_y} Td ({esc_line}) Tj ET")
                if idx < len(lines) - 1:
                    p2_y -= (size + 4)
            p2_y -= 4
        else:
            page2_stream.append(f"BT /{font_ref_name} {size} Tf {left_margin} {p2_y} Td ({esc_text}) Tj ET")

    # Header for page 2 (keep it simple but clean)
    p2_text("CHANDRAN S", "F2", 14)
    p2_text("Dynamo Programmer | Revit & BIM Specialist -- Continued", "F1", 9.5, -14)
    
    # Horizontal line
    p2_y -= 8
    page2_stream.append(f"0.5 w 0.2 G {left_margin} {p2_y} m {page_width - left_margin} {p2_y} l S 0 G")
    
    # Professional Experience (Continued)
    p2_text("PROFESSIONAL EXPERIENCE (Continued)", "F2", 11, -22)
    
    # Job 3: Pinnacle Technology Services
    p2_y -= 8
    p2_text("Revit Jr. Modeller", "F2", 10)
    page2_stream.append(f"BT /F1 9.5 Tf 150 {p2_y} Td (-- Pinnacle Technology Services, Hyderabad) Tj ET")
    page2_stream.append(f"BT /F2 9.5 Tf 420 {p2_y} Td (Jul 2021 - Dec 2021 | 6 mos) Tj ET")
    
    p2_y -= 13
    page2_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p2_y} Td (\\225) Tj ET")
    page2_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p2_y} Td (Projects - Client- Netherland Housing Bim service) Tj ET")
    
    # Job 4: Neural Design
    p2_y -= 18
    p2_text("Architect", "F2", 10)
    page2_stream.append(f"BT /F1 9.5 Tf 110 {p2_y} Td (-- Neural Design & Constructions \\(P\\) Ltd, Madurai) Tj ET")
    page2_stream.append(f"BT /F2 9.5 Tf 450 {p2_y} Td (Jun 2019 - Jun 2021 | 2 yrs) Tj ET")
    
    neural_bullets = [
        "Delivered BIM services for international clients (Netherlands housing projects).",
        "Developed coordinated Revit models and ensured quality compliance with client standards."
    ]
    for bullet in neural_bullets:
        p2_y -= 13
        page2_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p2_y} Td (\\225) Tj ET")
        page2_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p2_y} Td ({pdf_escape(bullet)}) Tj ET")

    # Job 5: Freelance Architect
    p2_y -= 18
    p2_text("Freelance Architect", "F2", 10)
    page2_stream.append(f"BT /F1 9.5 Tf 160 {p2_y} Td (-- Madurai) Tj ET")
    page2_stream.append(f"BT /F2 9.5 Tf 450 {p2_y} Td (Sep 2017 - Jun 2019 | 1 yr 9 mos) Tj ET")
    
    freelance_bullets = [
        "Managed residential and public projects -- concept design, development, procurement, and supervision.",
        "star palms, Banaswadi, Bengaluru",
        "Commercial complex, 100ft road, Bengaluru"
    ]
    for bullet in freelance_bullets:
        p2_y -= 13
        page2_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p2_y} Td (\\225) Tj ET")
        page2_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p2_y} Td ({pdf_escape(bullet)}) Tj ET")

    # Selected Projects & Highlights
    p2_text("SELECTED PROJECTS & HIGHLIGHTS", "F2", 11, -22)
    p2_y -= 8
    projects = [
        "4 High-end Residences -- Carmel-by-the-Sea, California (full BIM & documentation support, Dynamo automation)",
        "Star Palms -- Banaswadi, Bengaluru (Luxury residential project)",
        "Commercial Complex -- 100FT Road, Bengaluru",
        "PHC -- Chennai (Public Health Centre)",
        "Andian Nagar Row House -- Sathangudi, Madurai",
        "Hafeez Contractor Apartments -- Pune (R16 & R7)",
        "Lane Cove Warehouse -- Australia (BIM package)",
        "Dubai Warehouse (International BIM project)"
    ]
    for prj in projects:
        p2_y -= 13
        words = prj.split(' ')
        lines = []
        curr_line = []
        curr_len = 0
        for w in words:
            if curr_len + len(w) + 1 > 80:
                lines.append(' '.join(curr_line))
                curr_line = [w]
                curr_len = len(w)
            else:
                curr_line.append(w)
                curr_len += len(w) + 1
        if curr_line:
            lines.append(' '.join(curr_line))
            
        page2_stream.append(f"BT /F2 9.5 Tf {left_margin + 6} {p2_y} Td (\\225) Tj ET")
        for idx, line in enumerate(lines):
            page2_stream.append(f"BT /F1 9.5 Tf {left_margin + 16} {p2_y} Td ({pdf_escape(line)}) Tj ET")
            if idx < len(lines) - 1:
                p2_y -= 13

    # Education
    p2_text("EDUCATION", "F2", 11, -22)
    p2_y -= 8
    p2_text("Master of Architecture", "F2", 9.5)
    page2_stream.append(f"BT /F1 9.5 Tf 165 {p2_y} Td (-- Meenakshi College of Engineering, Chennai) Tj ET")
    page2_stream.append(f"BT /F2 9.5 Tf 400 {p2_y} Td (2017 - 2019) Tj ET")
    page2_stream.append(f"BT /F1 9.5 Tf 480 {p2_y} Td (CGPA: 7.55/10) Tj ET")
    
    p2_y -= 14
    p2_text("Bachelor of Architecture", "F2", 9.5)
    page2_stream.append(f"BT /F1 9.5 Tf 170 {p2_y} Td (-- Tamilnadu School of Architecture, Coimbatore) Tj ET")
    page2_stream.append(f"BT /F2 9.5 Tf 400 {p2_y} Td (2012 - 2017) Tj ET")
    page2_stream.append(f"BT /F1 9.5 Tf 480 {p2_y} Td (CGPA: 7.02/10) Tj ET")

    # Additional
    p2_text("ADDITIONAL", "F2", 11, -22)
    p2_y -= 8
    p2_text("Languages: English | Tamil", "F1", 9.5)
    p2_text("Total Experience: ~8+ years (1.5 years dedicated Dynamo + Python experience)", "F1", 9.5, -14)
    p2_text("Availability: Immediate/As per notice period", "F1", 9.5, -14)
    p2_text("References: Available on request", "F1", 9.5, -14)

    # Assemble page 2 stream content
    page2_stream_content = "\n".join(page2_stream).encode('latin1')
    page2_stream_len = len(page2_stream_content)

    # ------------------ DEFINE ALL PDF OBJECTS ------------------
    # Object List representation: (object_id, object_bytes)
    # Note that Catalog, Pages, Page 1, Page 1 Content, Fonts, Page 2, Page 2 Content
    # are objects 1, 2, 3, 4, 5, 6, 7, 8
    
    obj_catalog = f"<< /Type /Catalog /Pages {pages_ref} >>".encode('latin1')
    obj_pages = f"<< /Type /Pages /Kids [{page1_ref} {page2_ref}] /Count 2 >>".encode('latin1')
    
    obj_page1 = f"<< /Type /Page /Parent {pages_ref} /Resources << /Font << /F1 {font_reg_ref} /F2 {font_bold_ref} >> >> /MediaBox [0 0 {page_width} {page_height}] /Contents 4 0 R >>".encode('latin1')
    
    obj_page1_content = f"<< /Length {page1_stream_len} >>\nstream\n".encode('latin1') + page1_stream_content + "\nendstream".encode('latin1')
    
    obj_font_reg = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>".encode('latin1')
    obj_font_bold = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>".encode('latin1')
    
    obj_page2 = f"<< /Type /Page /Parent {pages_ref} /Resources << /Font << /F1 {font_reg_ref} /F2 {font_bold_ref} >> >> /MediaBox [0 0 {page_width} {page_height}] /Contents 8 0 R >>".encode('latin1')
    
    obj_page2_content = f"<< /Length {page2_stream_len} >>\nstream\n".encode('latin1') + page2_stream_content + "\nendstream".encode('latin1')

    # Object map
    pdf_objs = [
        (1, obj_catalog),
        (2, obj_pages),
        (3, obj_page1),
        (4, obj_page1_content),
        (5, obj_font_reg),
        (6, obj_font_bold),
        (7, obj_page2),
        (8, obj_page2_content)
    ]
    
    # ------------------ COMPILE PDF BYTES WITH CORRECT XREFS ------------------
    pdf_bytes = bytearray()
    pdf_bytes.extend(b"%PDF-1.4\n")
    
    # Store byte offsets of objects
    offsets = {}
    
    for obj_id, content in pdf_objs:
        offsets[obj_id] = len(pdf_bytes)
        obj_header = f"{obj_id} 0 obj\n".encode('latin1')
        obj_footer = "\nendobj\n".encode('latin1')
        pdf_bytes.extend(obj_header)
        pdf_bytes.extend(content)
        pdf_bytes.extend(obj_footer)
        
    start_xref = len(pdf_bytes)
    
    # Write XREF Table
    xref_header = f"xref\n0 {len(pdf_objs) + 1}\n0000000000 65535 f \n".encode('latin1')
    pdf_bytes.extend(xref_header)
    
    for i in range(1, len(pdf_objs) + 1):
        offset_str = f"{offsets[i]:010d} 00000 n \n".encode('latin1')
        pdf_bytes.extend(offset_str)
        
    # Write Trailer
    trailer = f"trailer\n<< /Size {len(pdf_objs) + 1} /Root {catalog_ref} >>\nstartxref\n{start_xref}\n%%EOF\n".encode('latin1')
    pdf_bytes.extend(trailer)
    
    # Save the file
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

if __name__ == "__main__":
    out_file = os.path.abspath(r"c:\Users\tissu\source\repos\Cs Protfolio website_personal\docs\Ar_Chandran_Shanmugam_Resume.pdf")
    create_resume_pdf(out_file)
    print(f"Resume PDF successfully generated at {out_file}")
