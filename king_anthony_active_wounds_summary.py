#!/usr/bin/env python3
"""Generate PDF summary of five active wounds for Anthony A. King."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from fpdf import FPDF, FontFace

OUTPUT_PATH = Path("/workspace/King_Anthony_Active_Wounds_Summary.pdf")
PREVIEW_DIR = Path("/workspace/pdf_preview")


class WoundSummaryPDF(FPDF):
    def __init__(self) -> None:
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.set_margins(left=15, top=15, right=15)
        self.set_auto_page_break(auto=True, margin=18)

    @property
    def content_width(self) -> float:
        return self.w - self.l_margin - self.r_margin

    def reset_cursor(self) -> None:
        self.set_xy(self.l_margin, self.get_y())

    def section_title(self, title: str) -> None:
        self.reset_cursor()
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(235, 235, 235)
        self.multi_cell(self.content_width, 7, title, fill=True)
        self.ln(2)
        self.reset_cursor()

    def paragraph(self, text: str, size: int = 10, style: str = "") -> None:
        self.reset_cursor()
        self.set_font("Helvetica", style, size)
        self.multi_cell(self.content_width, 5, text)
        self.ln(1)
        self.reset_cursor()


def build_pdf() -> Path:
    pdf = WoundSummaryPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(pdf.content_width, 8, "Active Wound Summary", align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        pdf.content_width,
        5,
        "Patient: Anthony A. King    M/R #: 136508    Account #: 110220002599",
        align="C",
    )
    pdf.ln(4)
    pdf.reset_cursor()

    pdf.section_title("Patient Demographics")
    for line in [
        "Name: Anthony A. King",
        "DOB: 05/10/1957 (69 years old at time of charting)",
        "Sex: Male",
        "Weight: 229.3 lb (104.0 kg)",
        "Facility: Stockton Regional Rehab Hospital",
        "Admit date to rehab: 06/23/2026",
        "Attending physician: Pratik Gandhi, DO",
    ]:
        pdf.paragraph(line)

    pdf.section_title("Five Active Wounds - Measurements and Source Documents")
    pdf.paragraph(
        "All wound measurements were documented on 07/01/2026 wound addendum forms. "
        "Nursing orders describe wound locations and dressings but do not include measurements.",
        size=9,
    )

    table_width = pdf.content_width
    wound_rows = [
        [
            "1",
            "Right Back\nTraumatic, partial thickness, open",
            "19 cm x 8 cm\nArea: 152 cm2",
            "Wound Addendum\nSite: Back\nDate: 07/01/2026",
            "wound_addendum_back_62dd.pdf",
        ],
        [
            "2",
            "Right Heel\nPressure injury, DTI\nFluid-filled blister",
            "8 cm x 8 cm\nArea: 64 cm2",
            "Wound Addendum\nSite: Right Heel\nDate: 07/01/2026",
            "wound_addendum_right_heel_d70b.pdf",
        ],
        [
            "3",
            "Right 5th Toe\nPressure injury, DTI\nFluid-filled blister",
            "2 cm x 2 cm\nArea: 4 cm2",
            "Wound Addendum\nSite: Right Foot (5th toe)\nDate: 07/01/2026",
            "wound_addendum_right_foot.._9564.pdf",
        ],
        [
            "4",
            "Right Dorsal-Lateral Foot\nTraumatic, partial thickness\nOpen blister",
            "8 cm x 4.5 cm\nArea: 36 cm2",
            "Wound Addendum\nSite: Right Foot (dorsal lateral)\nDate: 07/01/2026",
            "wound_addendum_right_foot_c8b2.pdf",
        ],
        [
            "5",
            "Left Plantar Foot\nPressure injury, DTI\nFluid-filled blister",
            "8 cm x 9 cm\nArea: 72 cm2",
            "Wound Addendum\nSite: Left Foot\nDate: 07/01/2026",
            "wound_addendum_left_foot_a9c2.pdf",
        ],
    ]

    pdf.reset_cursor()
    with pdf.table(
        width=table_width,
        col_widths=(10, 45, 30, 50, table_width - 135),
        line_height=5,
        text_align="LEFT",
        headings_style=FontFace(size_pt=9, emphasis="BOLD"),
    ) as table:
        table.row(["#", "Wound Site", "Size (L x W)", "Source Document", "File Name"])
        for row in wound_rows:
            table.row(row)

    pdf.ln(3)
    pdf.reset_cursor()
    pdf.section_title("Wound Clinical Notes")

    note_rows = [
        [
            "1",
            "Right Back (19 cm x 8 cm)",
            "Etiology: Traumatic. Wound bed: 10% granulation, 70% slough, 20% eschar. "
            "Treatment changed to Collagenase (Santyl) on 07/01/2026. "
            "Nursing order (no size): wound_care_1_79cf.pdf",
        ],
        [
            "2",
            "Right Heel (8 cm x 8 cm)",
            "Etiology: Pressure injury / DTI. Status 07/01/2026: Worsened, larger in size. "
            "Nursing order (no size): wound_care_5_9d02.pdf",
        ],
        [
            "3",
            "Right 5th Toe (2 cm x 2 cm)",
            "Etiology: Pressure injury / DTI. Status 07/01/2026: Worsened, decreased in size, discolored. "
            "Nursing order (no size): wound_care_3_e3ae.pdf",
        ],
        [
            "4",
            "Right Dorsal-Lateral Foot (8 cm x 4.5 cm)",
            "Etiology: Traumatic. Status 07/01/2026: Worsened, larger in size, increased drainage. "
            "Nursing order (no size): wound_care_4_dc4a.pdf",
        ],
        [
            "5",
            "Left Plantar Foot (8 cm x 9 cm)",
            "Etiology: Pressure injury / DTI. Status 07/01/2026: No change. "
            "Nursing order (no size): wound_care_2_ee6e.pdf",
        ],
    ]

    pdf.reset_cursor()
    with pdf.table(
        width=table_width,
        col_widths=(10, 52, table_width - 62),
        line_height=5,
        text_align="LEFT",
        headings_style=FontFace(size_pt=9, emphasis="BOLD"),
    ) as table:
        table.row(["#", "Wound", "Clinical Notes"])
        for row in note_rows:
            table.row(row)

    pdf.ln(3)
    pdf.reset_cursor()
    pdf.section_title("Supporting Documents Reviewed (No Wound Measurements)")

    supporting_rows = [
        ["wound_referral_7d5f.pdf", "Admission H&P - describes bilateral foot wounds and hospital course."],
        ["wound_care_consult_5175.pdf", "Wound care consult order - evaluate multiple wounds."],
        ["wound_care_1_79cf.pdf", "Nursing order - Right Back dressing (Collagenase)."],
        ["wound_care_2_ee6e.pdf", "Nursing order - Left Foot/plantar DTI blister."],
        ["wound_care_3_e3ae.pdf", "Nursing order - Right 5th Toe DTI blister."],
        ["wound_care_4_dc4a.pdf", "Nursing order - Right dorsal lateral foot open blister."],
        ["wound_care_5_9d02.pdf", "Nursing order - Right heel fluid-filled blister."],
    ]

    pdf.reset_cursor()
    with pdf.table(
        width=table_width,
        col_widths=(58, table_width - 58),
        line_height=5,
        text_align="LEFT",
        headings_style=FontFace(size_pt=9, emphasis="BOLD"),
    ) as table:
        table.row(["File Name", "Description"])
        for row in supporting_rows:
            table.row(row)

    pdf.ln(4)
    pdf.section_title("Summary")
    pdf.paragraph(
        "Total documented open surface area across all five wounds: approximately 328 cm2. "
        "Re-measure at clinic intake is recommended. Three wounds were documented as worsening "
        "on the 07/01/2026 addendum assessments."
    )

    pdf.ln(2)
    pdf.reset_cursor()
    pdf.set_font("Helvetica", "I", 8)
    pdf.multi_cell(pdf.content_width, 4, f"Generated {date.today().isoformat()}", align="C")

    pdf.output(str(OUTPUT_PATH))
    return OUTPUT_PATH


def render_preview(pdf_path: Path, out_dir: Path) -> list[Path]:
    import fitz

    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.png"):
        old.unlink()

    doc = fitz.open(pdf_path)
    images: list[Path] = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image_path = out_dir / f"page_{i + 1}.png"
        pix.save(image_path)
        images.append(image_path)
    doc.close()
    return images


def verify_pdf(pdf_path: Path) -> None:
    import fitz

    required_snippets = [
        "19 cm x 8 cm",
        "8 cm x 8 cm",
        "2 cm x 2 cm",
        "8 cm x 4.5 cm",
        "8 cm x 9 cm",
        "wound_addendum_back_62dd.pdf",
        "Collagenase",
        "328 cm2",
        "Clinical Notes",
    ]

    doc = fitz.open(pdf_path)
    full_text = "\n".join(page.get_text("text") for page in doc)

    for snippet in required_snippets:
        if snippet not in full_text:
            raise RuntimeError(f"Missing expected text in PDF: {snippet}")

    for page_num, page in enumerate(doc, start=1):
        rect = page.rect
        for block in page.get_text("blocks"):
            x0, _, x1, _, content, *_ = block
            if x1 > rect.width + 1:
                raise RuntimeError(
                    f"Page {page_num} text exceeds right margin: {content[:80]!r}"
                )
            if x0 < -1:
                raise RuntimeError(
                    f"Page {page_num} text exceeds left margin: {content[:80]!r}"
                )
    doc.close()


def main() -> None:
    pdf_path = build_pdf()
    verify_pdf(pdf_path)
    images = render_preview(pdf_path, PREVIEW_DIR)
    print(pdf_path)
    for image in images:
        print(image)


if __name__ == "__main__":
    main()
