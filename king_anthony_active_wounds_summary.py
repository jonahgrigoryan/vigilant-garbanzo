#!/usr/bin/env python3
"""Generate PDF summary of five active wounds for Anthony A. King."""

from fpdf import FPDF
from datetime import date

OUTPUT_PATH = "/workspace/King_Anthony_Active_Wounds_Summary.pdf"


def main():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    w = pdf.epw  # effective page width

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(w, 8, "Active Wound Summary", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(w, 6, "Patient: Anthony A. King  |  M/R #: 136508  |  Account #: 110220002599", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(w, 7, "Patient Demographics", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    for line in [
        "Name: Anthony A. King",
        "DOB: 05/10/1957 (69 years old at time of charting)",
        "Sex: Male | Weight: 229.3 lb (104.0 kg)",
        "Facility: Stockton Regional Rehab Hospital",
        "Admit date to rehab: 06/23/2026",
        "Attending physician: Pratik Gandhi, DO",
    ]:
        pdf.cell(w, 5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(w, 7, "Five Active Wounds - Size and Source Document", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(
        w,
        4,
        "All wound measurements (length x width in cm) were documented on 07/01/2026 wound addendum "
        "forms. Nursing orders describe wound locations and dressings but do not include measurements.",
    )
    pdf.ln(4)

    wounds = [
        {
            "num": 1,
            "site": "Right Back (traumatic, partial thickness, open wound)",
            "size": "19 cm x 8 cm (approx. 152 cm2)",
            "file": "wound_addendum_back_62dd.pdf",
            "doc": "Wound Addendum - Site: Back - Assessment date: 07/01/2026",
            "notes": [
                "Etiology: Other / Traumatic",
                "Wound bed: 10% granulation, 70% slough, 20% eschar",
                "Treatment changed to Collagenase (Santyl) on 07/01/2026",
                "Related nursing order (no size): wound_care_1_79cf.pdf",
            ],
        },
        {
            "num": 2,
            "site": "Right Heel (pressure injury, DTI, fluid-filled blister)",
            "size": "8 cm x 8 cm (approx. 64 cm2)",
            "file": "wound_addendum_right_heel_d70b.pdf",
            "doc": "Wound Addendum - Site: Right Heel - Assessment date: 07/01/2026",
            "notes": [
                "Etiology: Pressure Injury | Staging: Deep Tissue Injury (DTI)",
                "Status on 07/01/2026: Worsened - noted larger in size",
                "Related nursing order (no size): wound_care_5_9d02.pdf",
            ],
        },
        {
            "num": 3,
            "site": "Right 5th Toe (pressure injury, DTI, fluid-filled blister)",
            "size": "2 cm x 2 cm (approx. 4 cm2)",
            "file": "wound_addendum_right_foot.._9564.pdf",
            "doc": "Wound Addendum - Site: Right Foot (5th toe) - Assessment date: 07/01/2026",
            "notes": [
                "Etiology: Pressure Injury | Staging: Deep Tissue Injury (DTI)",
                "Status on 07/01/2026: Worsened - decreased in size, discolored",
                "Related nursing order (no size): wound_care_3_e3ae.pdf",
            ],
        },
        {
            "num": 4,
            "site": "Right Dorsal-Lateral Foot (traumatic, partial thickness, open blister)",
            "size": "8 cm x 4.5 cm (approx. 36 cm2)",
            "file": "wound_addendum_right_foot_c8b2.pdf",
            "doc": "Wound Addendum - Site: Right Foot (dorsal lateral) - Assessment date: 07/01/2026",
            "notes": [
                "Etiology: Other / Traumatic",
                "Status on 07/01/2026: Worsened - larger in size, increased drainage",
                "Related nursing order (no size): wound_care_4_dc4a.pdf",
            ],
        },
        {
            "num": 5,
            "site": "Left Plantar Foot (pressure injury, DTI, fluid-filled blister)",
            "size": "8 cm x 9 cm (approx. 72 cm2)",
            "file": "wound_addendum_left_foot_a9c2.pdf",
            "doc": "Wound Addendum - Site: Left Foot - Assessment date: 07/01/2026",
            "notes": [
                "Etiology: Pressure Injury | Staging: Deep Tissue Injury (DTI)",
                "Status on 07/01/2026: No change",
                "Related nursing order (no size): wound_care_2_ee6e.pdf",
            ],
        },
    ]

    for wound in wounds:
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(w, 5, f"Wound {wound['num']}: {wound['site']}")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(w, 5, f"Documented size: {wound['size']}")
        pdf.multi_cell(w, 5, f"Source document: {wound['doc']}")
        pdf.set_font("Helvetica", "I", 9)
        pdf.multi_cell(w, 4, f"File: {wound['file']}")
        pdf.set_font("Helvetica", "", 9)
        for note in wound["notes"]:
            pdf.multi_cell(w, 4, f"  - {note}")
        pdf.ln(3)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(w, 7, "Supporting Documents Reviewed (no wound measurements)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    supporting = [
        ("wound_referral_7d5f.pdf", "Admission H&P - describes bilateral foot wounds and hospital course."),
        ("wound_care_consult_5175.pdf", "Wound care consult order - evaluate multiple wounds."),
        ("wound_care_1_79cf.pdf", "Nursing order - Right Back dressing (Collagenase)."),
        ("wound_care_2_ee6e.pdf", "Nursing order - Left Foot/plantar DTI blister."),
        ("wound_care_3_e3ae.pdf", "Nursing order - Right 5th Toe DTI blister."),
        ("wound_care_4_dc4a.pdf", "Nursing order - Right dorsal lateral foot open blister."),
        ("wound_care_5_9d02.pdf", "Nursing order - Right heel fluid-filled blister."),
    ]

    pdf.set_font("Helvetica", "", 9)
    for filename, description in supporting:
        pdf.set_font("Helvetica", "B", 9)
        pdf.multi_cell(w, 4, filename)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(w, 4, description)
        pdf.ln(1)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(w, 7, "Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        w,
        5,
        "Total documented open surface area across all five wounds: approximately 328 cm2. "
        "Re-measure at clinic intake is recommended; three wounds were documented as worsening "
        "on the 07/01/2026 addendum assessments.",
    )

    pdf.set_y(-12)
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(w, 5, f"Generated {date.today().isoformat()}", align="C")

    pdf.output(OUTPUT_PATH)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
