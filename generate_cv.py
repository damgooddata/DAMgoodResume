"""
Pure-Python PDF generator for David Morgan's optimized CV.
No external dependencies required.
"""
import re

# ---------------------------------------------------------------------------
# Helvetica character widths (1000-unit em square, from Adobe AFM metrics)
# ---------------------------------------------------------------------------
HELV_W = {
    ' ':278,'!':278,'"':355,'#':556,'$':556,'%':889,'&':667,"'":191,
    '(':333,')':333,'*':389,'+':584,',':278,'-':333,'.':278,'/':278,
    '0':556,'1':556,'2':556,'3':556,'4':556,'5':556,'6':556,'7':556,
    '8':556,'9':556,':':278,';':278,'<':584,'=':584,'>':584,'?':556,
    '@':1015,'A':667,'B':667,'C':722,'D':722,'E':667,'F':611,'G':778,
    'H':722,'I':278,'J':500,'K':667,'L':556,'M':833,'N':722,'O':778,
    'P':667,'Q':778,'R':722,'S':667,'T':611,'U':722,'V':667,'W':944,
    'X':667,'Y':667,'Z':611,'[':278,'\\':278,']':278,'^':469,'_':556,
    '`':333,'a':556,'b':556,'c':500,'d':556,'e':556,'f':278,'g':556,
    'h':556,'i':222,'j':222,'k':500,'l':222,'m':833,'n':556,'o':556,
    'p':556,'q':556,'r':333,'s':500,'t':278,'u':556,'v':500,'w':722,
    'x':500,'y':500,'z':500,'{':334,'|':260,'}':334,'~':584,
    '\xb7':350, '\x95':350, '\xb0':400,
}
HELV_BOLD_W = {
    ' ':278,'!':333,'"':474,'#':556,'$':556,'%':889,'&':722,"'":238,
    '(':333,')':333,'*':389,'+':584,',':278,'-':333,'.':278,'/':333,
    '0':556,'1':556,'2':556,'3':556,'4':556,'5':556,'6':556,'7':556,
    '8':556,'9':556,':':333,';':333,'<':584,'=':584,'>':584,'?':611,
    '@':975,'A':722,'B':722,'C':722,'D':722,'E':667,'F':611,'G':778,
    'H':722,'I':278,'J':556,'K':722,'L':611,'M':833,'N':722,'O':778,
    'P':667,'Q':778,'R':722,'S':667,'T':611,'U':722,'V':667,'W':944,
    'X':667,'Y':667,'Z':611,'[':333,'\\':278,']':333,'^':584,'_':556,
    '`':333,'a':556,'b':611,'c':556,'d':611,'e':556,'f':333,'g':611,
    'h':611,'i':278,'j':278,'k':556,'l':278,'m':889,'n':611,'o':611,
    'p':611,'q':611,'r':389,'s':556,'t':333,'u':611,'v':556,'w':778,
    'x':556,'y':556,'z':500,'{':389,'|':280,'}':389,'~':584,
    '\xb7':350, '\x95':350, '\xb0':400,
}


def tw(text, size, bold=False):
    w = HELV_BOLD_W if bold else HELV_W
    return sum(w.get(c, 556) for c in text) * size / 1000.0


def pdf_escape(s):
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


# ---------------------------------------------------------------------------
# PDF builder
# ---------------------------------------------------------------------------
class PDF:
    def __init__(self, w=612, h=792):
        self.pw, self.ph = w, h
        self.objects = []
        self.page_ids = []
        self.streams = {}

        # Reserve slots 1=Catalog, 2=Pages
        self.objects.append(None)
        self.objects.append(None)

        # Standard fonts (obj 3, 4, 5)
        self._helv_id      = self._add_obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>')
        self._helv_bold_id = self._add_obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>')
        self._helv_obl_id  = self._add_obj(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>')

    def _add_obj(self, content_bytes):
        self.objects.append(content_bytes)
        return len(self.objects)   # 1-indexed

    def new_page(self):
        pid = len(self.objects) + 1
        self.page_ids.append(pid)
        self.streams[pid] = []
        self.objects.append(None)  # placeholder
        return pid

    def draw(self, page_id, cmd_bytes):
        self.streams[page_id].append(cmd_bytes)

    # ---- drawing primitives -----------------------------------------------
    def set_fill_rgb(self, page_id, r, g, b):
        self.draw(page_id, f'{r:.3f} {g:.3f} {b:.3f} rg\n'.encode())

    def set_stroke_rgb(self, page_id, r, g, b):
        self.draw(page_id, f'{r:.3f} {g:.3f} {b:.3f} RG\n'.encode())

    def rect_fill(self, page_id, x, y, w, h):
        self.draw(page_id, f'{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f\n'.encode())

    def text(self, page_id, x, y, text_str, size, bold=False, oblique=False, color=(0, 0, 0)):
        if not text_str:
            return
        font_name = 'F2' if bold else ('F3' if oblique else 'F1')
        r, g, b = color
        escaped = pdf_escape(text_str)
        cmd = (f'BT\n{r:.3f} {g:.3f} {b:.3f} rg\n'
               f'/{font_name} {size} Tf\n'
               f'{x:.2f} {y:.2f} Td\n'
               f'({escaped}) Tj\n'
               f'ET\n')
        self.draw(page_id, cmd.encode('latin-1', errors='replace'))

    def image(self, page_id, img_id, x, y, w, h):
        self.draw(page_id, (
            f'q\n{w:.2f} 0 0 {h:.2f} {x:.2f} {y:.2f} cm\n'
            f'/Im{img_id} Do\nQ\n'
        ).encode())

    def add_jpeg(self, jpeg_bytes, w_px, h_px):
        header = (f'<< /Type /XObject /Subtype /Image '
                  f'/Width {w_px} /Height {h_px} '
                  f'/ColorSpace /DeviceRGB /BitsPerComponent 8 '
                  f'/Filter /DCTDecode /Length {len(jpeg_bytes)} >>\n'
                  f'stream\n').encode()
        return self._add_obj(header + jpeg_bytes + b'\nendstream')

    # ---- finalize ---------------------------------------------------------
    def write(self, filename):
        # Finalize page streams
        page_stream_ids = {}
        for pid in self.page_ids:
            stream_content = b''.join(self.streams[pid])
            sid = self._add_obj(
                f'<< /Length {len(stream_content)} >>\nstream\n'.encode()
                + stream_content + b'\nendstream'
            )
            page_stream_ids[pid] = sid

        # Collect image object ids
        img_obj_ids = []
        for i, obj in enumerate(self.objects):
            if obj and isinstance(obj, bytes) and b'/XObject' in obj and b'/Image' in obj:
                img_obj_ids.append(i + 1)
        img_res_str = ' '.join(f'/Im{oid} {oid} 0 R' for oid in img_obj_ids)

        # Finalize page objects
        kids_str = ' '.join(f'{pid} 0 R' for pid in self.page_ids)
        for pid in self.page_ids:
            sid = page_stream_ids[pid]
            xobj_part = f'/XObject << {img_res_str} >> ' if img_res_str else ''
            page_dict = (
                f'<< /Type /Page /Parent 2 0 R '
                f'/MediaBox [0 0 {self.pw} {self.ph}] '
                f'/Contents {sid} 0 R '
                f'/Resources << '
                f'/Font << /F1 {self._helv_id} 0 R /F2 {self._helv_bold_id} 0 R '
                f'/F3 {self._helv_obl_id} 0 R >> '
                f'{xobj_part}'
                f'>> >>'
            )
            self.objects[pid - 1] = page_dict.encode()

        self.objects[0] = b'<< /Type /Catalog /Pages 2 0 R >>'
        self.objects[1] = f'<< /Type /Pages /Kids [{kids_str}] /Count {len(self.page_ids)} >>'.encode()

        # Serialize
        output = b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n'
        offsets = []
        for i, obj in enumerate(self.objects):
            offsets.append(len(output))
            obj_num = i + 1
            if isinstance(obj, bytes):
                output += f'{obj_num} 0 obj\n'.encode() + obj + b'\nendobj\n'
            else:
                output += f'{obj_num} 0 obj\n{obj}\nendobj\n'.encode()

        xref_off = len(output)
        output += f'xref\n0 {len(self.objects)+1}\n'.encode()
        output += b'0000000000 65535 f \n'
        for off in offsets:
            output += f'{off:010d} 00000 n \n'.encode()
        output += (f'trailer\n<< /Size {len(self.objects)+1} /Root 1 0 R >>\n'
                   f'startxref\n{xref_off}\n%%EOF\n').encode()

        with open(filename, 'wb') as f:
            f.write(output)
        print(f'PDF written: {filename} ({len(output):,} bytes, {len(self.page_ids)} pages)')


# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
PW, PH = 612, 792
ML, MR = 36, 36
MT, MB = 36, 36
CW = PW - ML - MR   # 540

NAVY  = (0.106, 0.227, 0.361)
BLUE  = (0.180, 0.427, 0.643)
BLACK = (0.102, 0.102, 0.102)
GRAY  = (0.40,  0.40,  0.40)
LGRAY = (0.80,  0.80,  0.80)
WHITE = (1.0,   1.0,   1.0)


# ---------------------------------------------------------------------------
# High-level drawing helpers
# ---------------------------------------------------------------------------

def draw_section_header(pdf, pid, y, title):
    """Draw dark navy band with white title. Returns y below band."""
    band_h = 13
    pdf.set_fill_rgb(pid, *NAVY)
    pdf.rect_fill(pid, ML, y - band_h, CW, band_h)
    pdf.text(pid, ML + 5, y - band_h + 3.5, title.upper(), 8.5, bold=True, color=WHITE)
    return y - band_h - 4


def render_para(pdf, pid, x, y, text_segs, size, max_w, leading=1.4):
    """
    Render paragraph with mixed bold/normal/color runs.
    text_segs: list of (str, bold:bool, r, g, b)
    Returns new y.
    """
    # Build flat token list: (word_or_space, bold, r, g, b)
    tokens = []
    for (txt, bold, r, g, b) in text_segs:
        parts = re.split(r'(\s)', txt)
        for part in parts:
            if part == ' ' or part == '\n':
                tokens.append((' ', bold, r, g, b))
            elif part:
                tokens.append((part, bold, r, g, b))

    line_h = size * leading
    lines = []
    cur_line = []
    cur_w = 0.0

    for (tok, bold, r, g, b) in tokens:
        if tok == ' ':
            if cur_line:
                sp_w = tw(' ', size, bold)
                cur_line.append((' ', bold, r, g, b))
                cur_w += sp_w
        else:
            ww = tw(tok, size, bold)
            if cur_w + ww > max_w + 0.5 and cur_line:
                # Strip trailing space from current line
                while cur_line and cur_line[-1][0] == ' ':
                    cur_line.pop()
                lines.append(cur_line)
                cur_line = [(tok, bold, r, g, b)]
                cur_w = ww
            else:
                cur_line.append((tok, bold, r, g, b))
                cur_w += ww

    if cur_line:
        while cur_line and cur_line[-1][0] == ' ':
            cur_line.pop()
        lines.append(cur_line)

    for line in lines:
        cx = x
        for (tok, bold, r, g, b) in line:
            pdf.text(pid, cx, y, tok, size, bold=bold, color=(r, g, b))
            cx += tw(tok, size, bold)
        y -= line_h

    return y


def render_bullet(pdf, pid, x, y, text_segs, size, max_w, indent=10, leading=1.38):
    """Render a bullet point. Returns new y."""
    bullet = '\x95'
    bw = tw(bullet + ' ', size)
    pdf.text(pid, x + indent, y, bullet, size, color=NAVY)
    return render_para(pdf, pid, x + indent + bw, y, text_segs, size,
                       max_w - indent - bw, leading=leading)


# ---------------------------------------------------------------------------
# Job entry renderer
# ---------------------------------------------------------------------------
def draw_job(pdf, pid, y, title, company, dates, location, bullets):
    """Draw a job entry with auto page-break. Returns (pid, y)."""
    SIZE_J = 8.8
    LH = SIZE_J * 1.38
    INDENT = 10
    MAX_W = CW

    if y < MB + 80:
        pid = pdf.new_page()
        y = PH - MT
        y = draw_section_header(pdf, pid, y, 'Professional Experience (continued)')

    # Title row
    date_w = tw(dates, 8.5)
    pdf.text(pid, ML, y, title, 9.8, bold=True, color=NAVY)
    title_end = ML + tw(title, 9.8, bold=True)
    pdf.text(pid, title_end, y, '  -  ', 9.8, color=GRAY)
    comp_x = title_end + tw('  -  ', 9.8)
    pdf.text(pid, comp_x, y, company, 9.8, bold=True, color=BLUE)
    pdf.text(pid, PW - MR - date_w, y, dates, 8.5, oblique=True, color=GRAY)
    y -= LH * 1.1

    # Location
    pdf.text(pid, ML, y, location, 8.2, oblique=True, color=GRAY)
    y -= LH * 0.95

    # Bullets
    for bsegs in bullets:
        if y < MB + 22:
            pid = pdf.new_page()
            y = PH - MT
            y = draw_section_header(pdf, pid, y, 'Professional Experience (continued)')
        y = render_bullet(pdf, pid, ML, y, bsegs, SIZE_J, MAX_W,
                          indent=INDENT, leading=1.38)
        y -= 1.5

    return pid, y - 3


# ---------------------------------------------------------------------------
# Build the full CV
# ---------------------------------------------------------------------------
def build_cv(output_path):
    pdf = PDF()

    # Load headshot
    with open('/home/user/DAMgoodResume/headshot.jpg', 'rb') as f:
        photo_data = f.read()
    img_id = pdf.add_jpeg(photo_data, 408, 409)

    pid = pdf.new_page()
    y = PH - MT

    # ── HEADER ────────────────────────────────────────────────────────────
    PHOTO_SIZE = 72
    photo_x = ML
    photo_y = y - PHOTO_SIZE

    pdf.image(pid, img_id, photo_x, photo_y, PHOTO_SIZE, PHOTO_SIZE)

    # Navy border around photo
    pdf.set_stroke_rgb(pid, *NAVY)
    pdf.draw(pid, f'2 w {photo_x:.1f} {photo_y:.1f} {PHOTO_SIZE:.1f} {PHOTO_SIZE:.1f} re S\n'.encode())

    # Text to right of photo
    tx = ML + PHOTO_SIZE + 14
    name_y = y - 9
    pdf.text(pid, tx, name_y, 'David Morgan', 22, bold=True, color=NAVY)

    title_y = name_y - 15
    title_str = 'Techno-Functional Supply Chain Developer  |  Python  \xb7  Salesforce Apex  \xb7  WMS Engineering  \xb7  Full Stack React'
    pdf.text(pid, tx, title_y, title_str, 9.5, bold=True, color=BLUE)

    loc_y = title_y - 11
    pdf.text(pid, tx, loc_y, 'Atlanta, GA (Remote / Open to Relocation)', 8.5, color=GRAY)

    contact_y = loc_y - 10
    contact2 = 'www.damgooddata.com   |   linkedin.com/in/dam-good-data   |   github.com/damgooddata'
    pdf.text(pid, tx, contact_y, contact2, 8.5, color=BLUE)

    # Dividing rule
    rule_y = y - PHOTO_SIZE - 7
    pdf.set_stroke_rgb(pid, *NAVY)
    pdf.draw(pid, f'2.5 w {ML:.1f} {rule_y:.1f} m {PW-MR:.1f} {rule_y:.1f} l S\n'.encode())
    y = rule_y - 7

    # ── PROFESSIONAL SUMMARY ───────────────────────────────────────────────
    y = draw_section_header(pdf, pid, y, 'Professional Summary')

    summary_segs = [
        ('Techno-Functional Supply Chain Developer with ', False, *BLACK),
        ('20+ years', True, *NAVY),
        (' engineering production-grade automation platforms at the intersection of logistics operations and scalable software systems. '
         'Proven track record architecting Python-driven platforms delivering ', False, *BLACK),
        ('$25M+ in annual profit', True, *NAVY),
        (', building React full-stack web applications that ', False, *BLACK),
        ('compressed multi-million-dollar grant review cycles by one full month', True, *NAVY),
        (', and developing Salesforce Apex solutions with Lightning Web Components (LWC), Orchestrated Flows, and multi-platform API integrations (Bill.com, Slack, GoodGrants). '
         'Deep operational fluency in Manhattan Active WMS, FTZ compliance, and warehouse systems engineering ensures every line of code is grounded in real-world supply chain context. '
         'Equally capable writing bulkified Apex triggers, designing FastAPI microservices, building event-driven ETL pipelines on GCP, or architecting RAG-based AI knowledge systems -- '
         'uniquely positioned as the developer who bridges complex business logic and high-performance code.', False, *BLACK),
    ]
    y = render_para(pdf, pid, ML, y, summary_segs, 8.5, CW, leading=1.45)
    y -= 5

    # ── TECHNICAL SKILLS ───────────────────────────────────────────────────
    y = draw_section_header(pdf, pid, y, 'Technical Skills')

    skills = [
        ('Languages & Frameworks:', 'Python 3.x, FastAPI, Flask, React, JavaScript (ES6+), Java, Apex, SQL, HTML5/CSS3, VBA'),
        ('Salesforce Platform:', 'Apex, Lightning Web Components (LWC), Orchestrated Flows, Flow Builder, SOQL, REST/SOAP/Bulk/Pub-Sub APIs, Approval Processes'),
        ('WMS & Supply Chain:', 'Manhattan Active WM, EDI Integration, FTZ Compliance, PO Lifecycle Management, MHE Systems, Inventory Reconciliation'),
        ('Data & Databases:', 'SQL Server, PostgreSQL, SSIS, Talend ETL, Apache Spark, Microsoft Access, Power BI, Looker Studio, Databox'),
        ('Cloud & DevOps:', 'Google Cloud Run, Microsoft Azure, GCP Cron Jobs, Power Platform (Apps/Automate/BI), Git, Docker, CI/CD Pipelines'),
        ('Integrations & APIs:', 'REST, SOAP, JSON, XML, Bill.com, Slack, Shopify, Clio, GoodGrants, Google Workspace APIs, SharePoint, STIBO PIM'),
        ('AI / ML / RAG:', 'RAG Architecture, LangChain, ChromaDB, LLM API Integration, Vector Database Indexing, Prompt Engineering'),
        ('Specialized Techniques:', 'Levenshtein Fuzzy Matching, Checksum Algorithms, Geo-Point Classification, Activity-Based Costing, Web Scraping, Reverse Engineering'),
    ]

    COL_W = CW / 2 - 6
    SK_SIZE = 8.2
    row_gap = SK_SIZE * 1.35

    for i in range(0, len(skills), 2):
        row_y = y
        label, val = skills[i]
        segs_l = [(label + ' ', True, *NAVY), (val, False, *BLACK)]
        new_y_l = render_para(pdf, pid, ML, row_y, segs_l, SK_SIZE, COL_W, leading=1.35)

        if i + 1 < len(skills):
            label2, val2 = skills[i + 1]
            segs_r = [(label2 + ' ', True, *NAVY), (val2, False, *BLACK)]
            new_y_r = render_para(pdf, pid, ML + CW / 2 + 6, row_y, segs_r, SK_SIZE, COL_W, leading=1.35)
            y = min(new_y_l, new_y_r)
        else:
            y = new_y_l
        y -= 1

    y -= 4

    # ── PROFESSIONAL EXPERIENCE ────────────────────────────────────────────
    y = draw_section_header(pdf, pid, y, 'Professional Experience')

    # ─ DAMgoodData ─
    bullets_dam = [
        [('Architected a ', False, *BLACK), ('React full-stack grant management platform', True, *NAVY),
         (' for The Yass Prize / Center for Educational Reform, replacing static Word documents with a real-time, '
          'bidirectional GoodGrants API-integrated review system featuring user authentication, CAPTCHA, '
          'role-based access, and admin dashboard -- ', False, *BLACK),
         ('compressing the annual grant review period by 1 full month', True, *NAVY),
         (' across multi-phase peer review of hundreds of applicants.', False, *BLACK)],

        [('Engineered ', False, *BLACK), ('Salesforce Apex + Lightning Web Components (LWC)', True, *NAVY),
         (' expense automation with Orchestrated Flows, dynamic approval routing (manager hierarchy & expense value thresholds), ', False, *BLACK),
         ('Bill.com API', True, *NAVY), (' automated vendor bill creation, and ', False, *BLACK),
         ('Slack API', True, *NAVY),
         (' embedded approve/reject buttons -- eliminating a multi-step manual workflow with automated vendor onboarding.', False, *BLACK)],

        [('Built ', False, *BLACK), ('Python data orchestration platform on Google Cloud Run', True, *NAVY),
         (' with cron-scheduled ETL jobs, Google Drive/Sheets/Docs API pipelines, and Looker Studio dashboards '
          'for Global Frontier Missions -- eliminating manual field data consolidation across siloed Google Forms and Sheets.', False, *BLACK)],

        [('Developed ', False, *BLACK), ('RAG-based AI knowledge retrieval system', True, *NAVY),
         (' using LangChain, ChromaDB vector database, and LLM API integration served via Python backend -- '
          'enabling context-aware SOP navigation (deployed live as "Computron" at www.damgooddata.com).', False, *BLACK)],

        [('Built ', False, *BLACK), ('SEO-optimized React website', True, *NAVY),
         (' with headless CMS architecture and automated Google My Business API review integration for '
          'Shaka Roofing -- maintaining storm-specific testimonials for targeted organic search ranking.', False, *BLACK)],

        [('Engineered custom ', False, *BLACK), ('Shopify JavaScript plugin', True, *NAVY),
         (' for RipLaces with real-time product image preview and automated kit bundle cart management; '
          'developed Python law-firm marketing app with ', False, *BLACK),
         ('Levenshtein fuzzy matching', True, *NAVY),
         (', dynamic column mapping, and duplicate detection for multi-county arrest record processing (Soyars & Morgan Law).', False, *BLACK)],

        [('Reverse-engineered Microsoft Access swim meet database; built ', False, *BLACK),
         ('checksum-validated Excel import tool', True, *NAVY),
         (' for NYC Public Schools -- eliminating manual stat entry for multi-school athletic events.', False, *BLACK)],
    ]
    pid, y = draw_job(pdf, pid, y, 'Founder & Principal Software Engineer', 'DAMgoodData',
                      'Aug 2020 - Present', 'Remote  |  www.damgooddata.com', bullets_dam)

    # Divider
    pdf.set_stroke_rgb(pid, *LGRAY)
    pdf.draw(pid, f'0.5 w {ML:.1f} {y:.1f} m {PW-MR:.1f} {y:.1f} l S\n'.encode())
    y -= 5

    # ─ Floor & Decor Senior ─
    bullets_fnd_sr = [
        [('Engineered ', False, *BLACK), ('Python automation platform generating $25M in annual profit', True, *NAVY),
         (' through vendor subsidy and cost recovery programs -- architecting email-triggered invoice processing, '
          'SharePoint access management via STIBO PIM integration, 10,000+ automated vendor remittance emails per '
          'cycle, and AP-ready consolidated output; ', False, *BLACK),
         ('replaced a full-time manual position entirely', True, *NAVY), ('.', False, *BLACK)],

        [('Built ', False, *BLACK), ('real-time physical inventory reconciliation system', True, *NAVY),
         (' with direct Manhattan Active WMS integration, 15-minute SQL refresh cycles, and math-based '
          'case-vs-eaches error detection -- compressing annual warehouse inventory cycle from ', False, *BLACK),
         ('~1 week to 2 business days', True, *NAVY),
         (' across 1M+ sq ft distribution centers; system adopted as native Manhattan WMS module by IT.', False, *BLACK)],

        [('Developed custom ', False, *BLACK), ('multi-user mobile scanning application', True, *NAVY),
         (' (10 concurrent stations) for LA warehouse relocation: pallet manifest tracking, 24,000-lb bay-load alerts, '
          'driver photo ID capture, seal barcode verification, automated BOL/packing list generation, and Manhattan '
          'WMS put-away confirmation -- achieving ', False, *BLACK),
         ('near-zero inventory loss', True, *NAVY), (' across the full relocation.', False, *BLACK)],

        [('Automated domestic logistics invoice pipeline: ', True, *NAVY),
         ('Outlook email trigger -> strict format validation -> GL code algorithm -> manager review -> '
          'fiscal-week auto-approval -> AP consolidated file; eliminated headcount addition.', False, *BLACK)],

        [('Built freight claims intake with ', False, *BLACK), ('Microsoft Power Apps + Power Automate', True, *NAVY),
         (' achieving ', False, *BLACK), ('60% reduction in claim resolution time', True, *NAVY),
         (' ; revamped Python/Java data pipelines for ', False, *BLACK),
         ('50% improvement in throughput', True, *NAVY),
         (' ; converted 30+ Excel reports to scheduled Power BI dashboards.', False, *BLACK)],
    ]
    pid, y = draw_job(pdf, pid, y, 'Senior Merchandising Financial Analyst', 'Floor & Decor',
                      'Mar 2021 - Apr 2024', 'Atlanta, GA', bullets_fnd_sr)

    if y < MB + 100:
        pid = pdf.new_page()
        y = PH - MT
        y = draw_section_header(pdf, pid, y, 'Professional Experience (continued)')
    else:
        pdf.set_stroke_rgb(pid, *LGRAY)
        pdf.draw(pid, f'0.5 w {ML:.1f} {y:.1f} m {PW-MR:.1f} {y:.1f} l S\n'.encode())
        y -= 5

    # ─ Floor & Decor SCM ─
    bullets_fnd_scm = [
        [('Architected company-wide ', False, *BLACK), ('supply chain BI infrastructure', True, *NAVY),
         (' : migrated legacy Access databases to SQL Server, integrated ', False, *BLACK),
         ('Manhattan Active WMS', True, *NAVY),
         (' raw data layer, and deployed SSIS + Talend ETL pipelines in a scheduled network environment -- '
          'replacing an Access "reporting server under a desk" with a production-grade analytics platform.', False, *BLACK)],

        [('Engineered Houston DC warehouse expansion support: real-time ', False, *BLACK),
         ('Manhattan WMS location updates', True, *NAVY),
         (' across nightly relocation cycles, enabling construction while operations continued uninterrupted.', False, *BLACK)],

        [('Built ', False, *BLACK), ('PO Lifecycle data cube', True, *NAVY),
         (' unifying 30+ purchase order status reports into a single controlled Power BI environment '
          'with network-scheduled refresh.', False, *BLACK)],

        [('Implemented ', False, *BLACK), ('FTZ freight accrual system', True, *NAVY),
         (' tracking actual vs. landed cost per SKU; built tariff risk monitoring enabling rapid supplier '
          'diversification. Designed EDI feed and API integration architecture for supply chain data acquisition.', False, *BLACK)],
    ]
    pid, y = draw_job(pdf, pid, y, 'Supply Chain Reporting Manager', 'Floor & Decor',
                      'Jun 2016 - Mar 2021', 'Atlanta, GA', bullets_fnd_scm)

    pdf.set_stroke_rgb(pid, *LGRAY)
    pdf.draw(pid, f'0.5 w {ML:.1f} {y:.1f} m {PW-MR:.1f} {y:.1f} l S\n'.encode())
    y -= 5

    # ─ Southeastern Grocers ─
    bullets_seg = [
        [('Built automated vendor invoice audit tool recovering ', False, *BLACK),
         ('$2.3M in unpaid rebates', True, *NAVY),
         (' during a 6-month audit across the full Southeastern Grocers store network (Winn-Dixie & Bi-Lo).', False, *BLACK)],

        [('Engineered ', False, *BLACK), ('commodity-based delivery frequency optimization system', True, *NAVY),
         (' with seasonal demand monitoring dashboard, managing all delivery schedules under C&S Wholesale '
          'dual-penalty SLA constraints (lost sales fines + excess inventory fees) for all store locations.', False, *BLACK)],

        [('Managed ', False, *BLACK), ('promotional demand forecasting', True, *NAVY),
         (' for advertised deals (BOGO, 2-for-X), modeling lift factors and cross-promotion cannibalization; '
          'assisted conversion of 120+ acquisition stores.', False, *BLACK)],
    ]
    pid, y = draw_job(pdf, pid, y, 'Supply Chain Auditor', 'Southeastern Grocers (Winn-Dixie / Bi-Lo)',
                      'Apr 2013 - Jun 2016', 'Jacksonville, FL', bullets_seg)

    pdf.set_stroke_rgb(pid, *LGRAY)
    pdf.draw(pid, f'0.5 w {ML:.1f} {y:.1f} m {PW-MR:.1f} {y:.1f} l S\n'.encode())
    y -= 5

    # ─ Interline Brands ─
    bullets_int = [
        [('Redesigned DC/RDC regional assignment model yielding ', False, *BLACK),
         ('$93K annual cost avoidance', True, *NAVY),
         (' ; automated LTL RFP analysis pipeline (full analysis in <1 day) generating ', False, *BLACK),
         ('$67K additional carrier savings', True, *NAVY), ('.', False, *BLACK)],

        [('Developed parcel claims recovery process recapturing ', False, *BLACK),
         ('$120K+ annually', True, *NAVY),
         (' ; managed ', False, *BLACK), ('$10M parcel budget', True, *NAVY), ('.', False, *BLACK)],

        [('Built ', False, *BLACK), ('Proof of Delivery (POD) system', True, *NAVY),
         (' with driver training programs and KPI compliance reporting; engineered ', False, *BLACK),
         ('Electronic Bill of Lading (E-BOL)', True, *NAVY),
         (' for automated shipping document generation at dispatch; built real-time customer freight '
          'calculator integrated into order entry system.', False, *BLACK)],
    ]
    pid, y = draw_job(pdf, pid, y, 'Regional Logistics Analyst / Transportation Analyst', 'Interline Brands Inc.',
                      'Aug 2007 - Nov 2012', 'Jacksonville, FL', bullets_int)

    pdf.set_stroke_rgb(pid, *LGRAY)
    pdf.draw(pid, f'0.5 w {ML:.1f} {y:.1f} m {PW-MR:.1f} {y:.1f} l S\n'.encode())
    y -= 5

    # ─ UPS ─
    bullets_ups = [
        [('Led pre-employment screening and seasonal driver recruitment; supervised 12+ direct reports '
          'as Pre-Load Supervisor; dispatched 20 daily routes as PAS Dispatch Supervisor; served on the '
          'Northeast Florida ', False, *BLACK),
         ('PAS (Package Assist System) Implementation Team', True, *NAVY), ('.', False, *BLACK)],
    ]
    pid, y = draw_job(pdf, pid, y, 'HR / PAS Dispatch / Pre-Load Supervisor', 'UPS',
                      'Oct 2003 - May 2007', 'Jacksonville, FL', bullets_ups)

    y -= 4

    # ── EDUCATION & CERTIFICATIONS ─────────────────────────────────────────
    if y < MB + 55:
        pid = pdf.new_page()
        y = PH - MT

    y = draw_section_header(pdf, pid, y, 'Education & Certifications')

    edu_y = y
    # Education (left half)
    pdf.text(pid, ML, edu_y, 'B.S. Business Administration - Logistics & Supply Chain Management',
             8.8, bold=True, color=NAVY)
    edu_y -= 11
    pdf.text(pid, ML, edu_y, 'University of North Florida  |  Jacksonville, FL', 8.5, color=GRAY)
    edu_y -= 9
    pdf.text(pid, ML, edu_y,
             'Core Studies: Florida State College of Jacksonville (transferred to UNF)',
             8.2, oblique=True, color=GRAY)

    # Certifications (right half)
    cert_x = ML + CW / 2
    pdf.text(pid, cert_x, y, 'Salesforce Platform API Superbadge  -  Salesforce Trailhead',
             8.8, bold=True, color=NAVY)
    c2y = y - 11
    pdf.text(pid, cert_x, c2y, 'AI Portfolio: "Computron" RAG Chatbot  -  www.damgooddata.com',
             8.5, color=BLUE)
    c2y -= 9
    pdf.text(pid, cert_x, c2y,
             'Domain: Manhattan Active WM  \xb7  FTZ Compliance  \xb7  Supply Chain Intelligence',
             8.2, color=GRAY)

    pdf.write(output_path)


if __name__ == '__main__':
    build_cv('/home/user/DAMgoodResume/David_Morgan_CV_new.pdf')
    print('Done!')
