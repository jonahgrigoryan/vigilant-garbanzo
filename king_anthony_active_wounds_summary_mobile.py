#!/usr/bin/env python3
"""Generate mobile-friendly wound summary (HTML + narrow PDF)."""

from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path

from fpdf import FPDF

HTML_OUTPUT = Path("/workspace/King_Anthony_Active_Wounds_Summary_Mobile.html")
PDF_OUTPUT = Path("/workspace/King_Anthony_Active_Wounds_Summary_Mobile.pdf")
PREVIEW_DIR = Path("/workspace/pdf_preview_mobile")

PATIENT = {
    "name": "Anthony A. King",
    "mrn": "136508",
    "account": "110220002599",
    "dob": "05/10/1957",
    "age": "69 years old at time of charting",
    "sex": "Male",
    "weight": "229.3 lb (104.0 kg)",
    "facility": "Stockton Regional Rehab Hospital",
    "admit_date": "06/23/2026",
    "physician": "Pratik Gandhi, DO",
}

WOUNDS = [
    {
        "num": 1,
        "site": "Right Back",
        "details": "Traumatic, partial thickness, open",
        "length_cm": 19,
        "width_cm": 8,
        "source_doc": "Wound Addendum - Site: Back - Date: 07/01/2026",
        "source_file": "wound_addendum_back_62dd.pdf",
        "notes": (
            "Etiology: Traumatic. Wound bed: 10% granulation, 70% slough, 20% eschar. "
            "Treatment changed to Collagenase (Santyl) on 07/01/2026. "
            "Nursing order (no size): wound_care_1_79cf.pdf"
        ),
    },
    {
        "num": 2,
        "site": "Right Heel",
        "details": "Pressure injury, DTI, fluid-filled blister",
        "length_cm": 8,
        "width_cm": 8,
        "source_doc": "Wound Addendum - Site: Right Heel - Date: 07/01/2026",
        "source_file": "wound_addendum_right_heel_d70b.pdf",
        "notes": (
            "Etiology: Pressure injury / DTI. Status 07/01/2026: Worsened, larger in size. "
            "Nursing order (no size): wound_care_5_9d02.pdf"
        ),
    },
    {
        "num": 3,
        "site": "Right 5th Toe",
        "details": "Pressure injury, DTI, fluid-filled blister",
        "length_cm": 2,
        "width_cm": 2,
        "source_doc": "Wound Addendum - Site: Right Foot (5th toe) - Date: 07/01/2026",
        "source_file": "wound_addendum_right_foot.._9564.pdf",
        "notes": (
            "Etiology: Pressure injury / DTI. Status 07/01/2026: Worsened, decreased in size, discolored. "
            "Nursing order (no size): wound_care_3_e3ae.pdf"
        ),
    },
    {
        "num": 4,
        "site": "Right Dorsal-Lateral Foot",
        "details": "Traumatic, partial thickness, open blister",
        "length_cm": 8,
        "width_cm": 4.5,
        "source_doc": "Wound Addendum - Site: Right Foot (dorsal lateral) - Date: 07/01/2026",
        "source_file": "wound_addendum_right_foot_c8b2.pdf",
        "notes": (
            "Etiology: Traumatic. Status 07/01/2026: Worsened, larger in size, increased drainage. "
            "Nursing order (no size): wound_care_4_dc4a.pdf"
        ),
    },
    {
        "num": 5,
        "site": "Left Plantar Foot",
        "details": "Pressure injury, DTI, fluid-filled blister",
        "length_cm": 8,
        "width_cm": 9,
        "source_doc": "Wound Addendum - Site: Left Foot - Date: 07/01/2026",
        "source_file": "wound_addendum_left_foot_a9c2.pdf",
        "notes": (
            "Etiology: Pressure injury / DTI. Status 07/01/2026: No change. "
            "Nursing order (no size): wound_care_2_ee6e.pdf"
        ),
    },
]

SUPPORTING_DOCS = [
    ("wound_referral_7d5f.pdf", "Admission H&P - describes bilateral foot wounds and hospital course."),
    ("wound_care_consult_5175.pdf", "Wound care consult order - evaluate multiple wounds."),
    ("wound_care_1_79cf.pdf", "Nursing order - Right Back dressing (Collagenase)."),
    ("wound_care_2_ee6e.pdf", "Nursing order - Left Foot/plantar DTI blister."),
    ("wound_care_3_e3ae.pdf", "Nursing order - Right 5th Toe DTI blister."),
    ("wound_care_4_dc4a.pdf", "Nursing order - Right dorsal lateral foot open blister."),
    ("wound_care_5_9d02.pdf", "Nursing order - Right heel fluid-filled blister."),
]

TOTAL_AREA_CM2 = sum(w["length_cm"] * w["width_cm"] for w in WOUNDS)


def wound_size_text(wound: dict) -> str:
    area = wound["length_cm"] * wound["width_cm"]
    return f"{wound['length_cm']} cm x {wound['width_cm']} cm (Area: {area:g} cm2)"


class MobileWoundPDF(FPDF):
    """Narrow single-column PDF sized for phone screens."""

    PAGE_WIDTH_MM = 100

    def __init__(self) -> None:
        super().__init__(orientation="P", unit="mm", format=(self.PAGE_WIDTH_MM, 220))
        self.set_margins(left=8, top=10, right=8)
        self.set_auto_page_break(auto=True, margin=12)

    @property
    def content_width(self) -> float:
        return self.w - self.l_margin - self.r_margin

    def reset_cursor(self) -> None:
        self.set_x(self.l_margin)

    def section_title(self, title: str) -> None:
        self.reset_cursor()
        self.ln(2)
        self.set_font("Helvetica", "B", 13)
        self.set_fill_color(235, 235, 235)
        self.multi_cell(self.content_width, 7, title, fill=True)
        self.ln(2)
        self.reset_cursor()

    def body(self, text: str, size: int = 11, style: str = "", line_height: float = 5.5) -> None:
        self.reset_cursor()
        self.set_font("Helvetica", style, size)
        self.multi_cell(self.content_width, line_height, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.reset_cursor()

    def field_line(self, text: str, bold: bool = False) -> None:
        self.reset_cursor()
        self.set_font("Helvetica", "B" if bold else "", 11)
        self.multi_cell(self.content_width, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        self.reset_cursor()


def build_mobile_html() -> Path:
    wound_cards = []
    for wound in WOUNDS:
        wound_cards.append(
            f"""
            <article class="card">
              <div class="card-header">Wound {wound['num']}: {escape(wound['site'])}</div>
              <dl>
                <dt>Type</dt><dd>{escape(wound['details'])}</dd>
                <dt>Size</dt><dd>{escape(wound_size_text(wound))}</dd>
                <dt>Source Document</dt><dd>{escape(wound['source_doc'])}</dd>
                <dt>File Name</dt><dd><code>{escape(wound['source_file'])}</code></dd>
                <dt>Clinical Notes</dt><dd>{escape(wound['notes'])}</dd>
              </dl>
            </article>
            """
        )

    support_items = "".join(
        f"<li><strong>{escape(name)}</strong><span>{escape(desc)}</span></li>"
        for name, desc in SUPPORTING_DOCS
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Active Wound Summary - Anthony A. King</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5f7fa;
      --card: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --accent: #2563eb;
      --border: #d1d5db;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 16px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 17px;
      line-height: 1.5;
      color: var(--text);
      background: var(--bg);
      -webkit-text-size-adjust: 100%;
    }}
    .container {{ max-width: 680px; margin: 0 auto; }}
    h1 {{
      margin: 0 0 8px;
      font-size: 1.5rem;
      line-height: 1.25;
    }}
    .subtitle {{
      margin: 0 0 20px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .section {{
      margin: 24px 0;
    }}
    .section h2 {{
      margin: 0 0 12px;
      font-size: 1.1rem;
      padding: 10px 12px;
      background: #e5e7eb;
      border-radius: 8px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      margin-bottom: 14px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }}
    .card-header {{
      font-size: 1.05rem;
      font-weight: 700;
      margin-bottom: 10px;
      color: var(--accent);
    }}
    dl {{
      margin: 0;
    }}
    dt {{
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--muted);
      margin-top: 10px;
    }}
    dd {{
      margin: 4px 0 0;
      font-size: 1rem;
    }}
    code {{
      font-size: 0.9rem;
      word-break: break-all;
    }}
    ul.clean {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    ul.clean li {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      margin-bottom: 10px;
    }}
    ul.clean strong {{
      display: block;
      font-size: 0.92rem;
      word-break: break-all;
      margin-bottom: 6px;
    }}
    ul.clean span {{
      display: block;
      color: var(--text);
    }}
    .demographics p {{
      margin: 0 0 8px;
    }}
    .summary {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
    }}
    .footer {{
      margin-top: 24px;
      text-align: center;
      color: var(--muted);
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>
  <main class="container">
    <h1>Active Wound Summary</h1>
    <p class="subtitle">{escape(PATIENT['name'])} | M/R # {escape(PATIENT['mrn'])} | Account # {escape(PATIENT['account'])}</p>

    <section class="section demographics">
      <h2>Patient Demographics</h2>
      <p><strong>Name:</strong> {escape(PATIENT['name'])}</p>
      <p><strong>DOB:</strong> {escape(PATIENT['dob'])} ({escape(PATIENT['age'])})</p>
      <p><strong>Sex:</strong> {escape(PATIENT['sex'])}</p>
      <p><strong>Weight:</strong> {escape(PATIENT['weight'])}</p>
      <p><strong>Facility:</strong> {escape(PATIENT['facility'])}</p>
      <p><strong>Admit date to rehab:</strong> {escape(PATIENT['admit_date'])}</p>
      <p><strong>Attending physician:</strong> {escape(PATIENT['physician'])}</p>
    </section>

    <section class="section">
      <h2>Five Active Wounds</h2>
      <p>All wound measurements were documented on 07/01/2026 wound addendum forms.</p>
      {''.join(wound_cards)}
    </section>

    <section class="section">
      <h2>Supporting Documents (No Measurements)</h2>
      <ul class="clean">
        {support_items}
      </ul>
    </section>

    <section class="section">
      <h2>Summary</h2>
      <div class="summary">
        Total documented open surface area across all five wounds: approximately {TOTAL_AREA_CM2:g} cm2.
        Re-measure at clinic intake is recommended. Three wounds were documented as worsening on the
        07/01/2026 addendum assessments.
      </div>
    </section>

    <p class="footer">Generated {date.today().isoformat()}</p>
  </main>
</body>
</html>
"""
    HTML_OUTPUT.write_text(html, encoding="utf-8")
    return HTML_OUTPUT


def build_mobile_pdf() -> Path:
    pdf = MobileWoundPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(pdf.content_width, 7, "Active Wound Summary", align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        pdf.content_width,
        5,
        f"{PATIENT['name']}\nM/R # {PATIENT['mrn']} | Account # {PATIENT['account']}",
        align="C",
    )
    pdf.ln(3)
    pdf.reset_cursor()

    pdf.section_title("Patient Demographics")
    pdf.field_line(f"Name: {PATIENT['name']}")
    pdf.field_line(f"DOB: {PATIENT['dob']} ({PATIENT['age']})")
    pdf.field_line(f"Sex: {PATIENT['sex']}")
    pdf.field_line(f"Weight: {PATIENT['weight']}")
    pdf.field_line(f"Facility: {PATIENT['facility']}")
    pdf.field_line(f"Admit date to rehab: {PATIENT['admit_date']}")
    pdf.field_line(f"Attending physician: {PATIENT['physician']}")
    pdf.ln(2)

    pdf.section_title("Five Active Wounds")
    pdf.body(
        "Single-column mobile layout. All measurements from 07/01/2026 wound addendum forms.",
        size=10,
    )

    for wound in WOUNDS:
        pdf.ln(1)
        pdf.set_draw_color(200, 200, 200)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.l_margin + pdf.content_width, y)
        pdf.ln(3)
        pdf.field_line(f"Wound {wound['num']}: {wound['site']}", bold=True)
        pdf.field_line(f"Type: {wound['details']}")
        pdf.field_line(f"Size: {wound_size_text(wound)}")
        pdf.field_line(f"Source Document: {wound['source_doc']}")
        pdf.field_line(f"File Name: {wound['source_file']}")
        pdf.field_line(f"Notes: {wound['notes']}")
        pdf.ln(1)

    pdf.section_title("Supporting Documents (No Measurements)")
    for filename, description in SUPPORTING_DOCS:
        pdf.field_line(filename, bold=True)
        pdf.field_line(description)
        pdf.ln(1)

    pdf.section_title("Summary")
    pdf.body(
        f"Total documented open surface area across all five wounds: approximately {TOTAL_AREA_CM2:g} cm2. "
        "Re-measure at clinic intake is recommended. Three wounds were documented as worsening on the "
        "07/01/2026 addendum assessments."
    )
    pdf.ln(2)
    pdf.body(f"Generated {date.today().isoformat()}", size=9, style="I")

    pdf.output(str(PDF_OUTPUT))
    return PDF_OUTPUT


def render_mobile_previews() -> list[Path]:
    import fitz

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for old in PREVIEW_DIR.glob("*.png"):
        old.unlink()

    doc = fitz.open(PDF_OUTPUT)
    images: list[Path] = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image_path = PREVIEW_DIR / f"mobile_page_{i + 1}.png"
        pix.save(image_path)
        images.append(image_path)
    doc.close()
    return images


def verify_mobile_outputs() -> None:
    html = HTML_OUTPUT.read_text(encoding="utf-8")
    assert 'name="viewport"' in html
    assert "19 cm x 8 cm" in html
    assert "wound_addendum_back_62dd.pdf" in html

    import fitz

    doc = fitz.open(PDF_OUTPUT)
    text = "\n".join(page.get_text("text") for page in doc)
    for snippet in ["19 cm x 8 cm", "8 cm x 9 cm", "approximately", "328", "Wound 1:", "Generated"]:
        if snippet not in text:
            raise RuntimeError(f"Mobile PDF missing expected text: {snippet}")

    page = doc[0]
    width_mm = page.rect.width * 25.4 / 72
    if width_mm > 120:
        raise RuntimeError(f"Mobile PDF page too wide: {width_mm:.1f}mm")
    if width_mm < 90:
        raise RuntimeError(f"Mobile PDF page too narrow: {width_mm:.1f}mm")
    doc.close()


def main() -> None:
    build_mobile_html()
    build_mobile_pdf()
    verify_mobile_outputs()
    images = render_mobile_previews()
    print(HTML_OUTPUT)
    print(PDF_OUTPUT)
    for image in images:
        print(image)


if __name__ == "__main__":
    main()
