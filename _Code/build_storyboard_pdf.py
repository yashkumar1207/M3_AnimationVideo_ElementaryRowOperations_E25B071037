"""
Generate the required 6-Scene Storyboard PDF for Elementary Row Operations.

Outputs:
    ../Storyboard_Elementary_Row_Operations_E25B071037.pdf
"""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

CODE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CODE_DIR.parent
OUT_PDF = ROOT_DIR / "Storyboard_Elementary_Row_Operations_E25B071037.pdf"
TIMINGS_FILE = CODE_DIR / "beat_timings.json"


def fmt_dur(timings: dict[str, float], keys: list[str], fallback: str) -> str:
    if not timings:
        return fallback
    total = sum(timings.get(k, 0.0) for k in keys)
    if total <= 0:
        return fallback
    mins = int(total // 60)
    secs = int(round(total % 60))
    return f"{mins}:{secs:02d}"


def build_pdf() -> None:
    timings = {}
    if TIMINGS_FILE.exists():
        timings = json.loads(TIMINGS_FILE.read_text(encoding="utf-8"))

    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=landscape(A4),
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="M3 Storyboard - Elementary Row Operations - E25B071037",
        author="Yash Kumar (E25B071037)",
    )

    styles = getSampleStyleSheet()
    navy = colors.HexColor("#102A43")
    blue_accent = colors.HexColor("#1D4ED8")
    light_bg = colors.HexColor("#F1F5F9")
    border_col = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle("TitleStyle", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, textColor=navy, spaceAfter=2)
    subtitle_style = ParagraphStyle("SubStyle", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, textColor=colors.HexColor("#334E68"), spaceAfter=6)
    box_style = ParagraphStyle("BoxStyle", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=13, textColor=colors.HexColor("#0F172A"))
    th_style = ParagraphStyle("TH", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, textColor=colors.white)
    td_style = ParagraphStyle("TD", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=colors.HexColor("#1E293B"))
    td_bold = ParagraphStyle("TDBold", parent=td_style, fontName="Helvetica-Bold", textColor=navy)

    elements = [
        Paragraph("LINEAR ALGEBRA AND CALCULUS (M3) • 6-SCENE ANIMATION STORYBOARD", title_style),
        Paragraph(
            "<b>Topic:</b> Elementary Row Operations (Swap, Scaling, Replacement &amp; Solution Invariance) &nbsp;|&nbsp; "
            "<b>Student:</b> Yash Kumar &nbsp;|&nbsp; <b>Student ID:</b> E25B071037 &nbsp;|&nbsp; "
            f"<b>Duration:</b> {fmt_dur(timings, list(timings.keys()), '3:24')} (under 4 min)",
            subtitle_style,
        ),
    ]

    obj_table = Table(
        [
            [
                Paragraph(
                    "<b>One-Sentence Learning Objective:</b> By the end of this video, the viewer will be able to "
                    "perform all three elementary row operations (row swap, nonzero scaling, and row replacement) on an "
                    "augmented matrix and explain geometrically and algebraically why they preserve the exact solution set.",
                    box_style,
                )
            ]
        ],
        colWidths=[268 * mm],
    )
    obj_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), light_bg),
                ("BOX", (0, 0), (-1, -1), 0.8, blue_accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(obj_table)
    elements.append(Spacer(1, 5))

    rows = [
        [
            Paragraph("Scene &amp; Time", th_style),
            Paragraph("Purpose", th_style),
            Paragraph("Visual Plan (1080p Manim)", th_style),
            Paragraph("Narration &amp; Mathematical Plan", th_style),
        ],
        [
            Paragraph(f"<b>0. Opening Frame</b><br/>({fmt_dur(timings, ['00_opening'], '0:08')})", td_bold),
            Paragraph("Identify project, topic, and presenter.", td_style),
            Paragraph(
                "Title card with course name, 'Elementary Row Operations', augmented matrix reduction preview, "
                "Student Name (Yash Kumar), and Student ID (E25B071037).",
                td_style,
            ),
            Paragraph("Introduce presenter and core promise: row operations simplify matrices without breaking solutions.", td_style),
        ],
        [
            Paragraph(f"<b>1. Hook / Context</b><br/>({fmt_dur(timings, ['01_hook_problem', '01_hook_puzzle'], '0:24')})", td_bold),
            Paragraph("Spark curiosity and motivate invariant intersection.", td_style),
            Paragraph(
                "Left: system 2x+6y=10, x+2y=4 and augmented matrix. Right: two lines meeting at glowing dot (2,1). "
                "Animate matrix simplifying to [1 0 | 2; 0 1 | 1] while lines rotate to x=2 and y=1 around the fixed dot.",
                td_style,
            ),
            Paragraph("Pose the puzzle: how do we simplify a matrix step by step without moving the intersection point?", td_style),
        ],
        [
            Paragraph(f"<b>2. Concept Introduction</b><br/>({fmt_dur(timings, ['02_concept_three', '02_concept_goal'], '0:30')})", td_bold),
            Paragraph("Define the three moves, notation, and learning goal.", td_style),
            Paragraph(
                "Three cards: Swap (R<sub>i</sub> ↔ R<sub>j</sub>), Scaling (R<sub>i</sub> ← cR<sub>i</sub>, c ≠ 0), Replacement (R<sub>i</sub> ← R<sub>i</sub> + kR<sub>j</sub>). "
                "Notation bar for R<sub>i</sub> and [A | b], plus Learning Objective banner.",
                td_style,
            ),
            Paragraph("Define all notation before use and state the three legal row operations cleanly.", td_style),
        ],
        [
            Paragraph(f"<b>3. Visual Intuition</b><br/>({fmt_dur(timings, ['03_intuition_swap_scale', '03_intuition_replace'], '0:40')})", td_bold),
            Paragraph("Build geometric intuition for why solutions stay fixed.", td_style),
            Paragraph(
                "Show why swap leaves lines untouched, why nonzero scaling keeps the same line (with c=0 warning), "
                "and animate R<sub>2</sub> ← R<sub>2</sub> + kR<sub>1</sub> pivoting Line 2 around (2,1) as k slides from 0 to −2.",
                td_style,
            ),
            Paragraph("Explain geometrically why each of the three moves preserves the intersection point (2, 1).", td_style),
        ],
        [
            Paragraph(
                f"<b>4. Worked Example</b><br/>({fmt_dur(timings, ['04_example_setup', '04_example_swap', '04_example_replace', '04_example_scale_finish'], '1:02')})",
                td_bold,
            ),
            Paragraph("Demonstrate all 3 operations step by step.", td_style),
            Paragraph(
                "Animated matrix on left, step-by-step arithmetic on right: (1) physical row swap R<sub>1</sub> ↔ R<sub>2</sub>, "
                "(2) R<sub>2</sub> ← R<sub>2</sub> − 2R<sub>1</sub> giving (0, 2, 2), (3) R<sub>2</sub> ← ½R<sub>2</sub> giving (0, 1, 1), and R<sub>1</sub> ← R<sub>1</sub> − 2R<sub>2</sub> giving x=2, y=1.",
                td_style,
            ),
            Paragraph("Walk through every intermediate arithmetic calculation clearly with zero skipped steps.", td_style),
        ],
        [
            Paragraph(f"<b>5. Verification &amp; Interpretation</b><br/>({fmt_dur(timings, ['05_verify_check', '05_verify_reverse'], '0:30')})", td_bold),
            Paragraph("Verify solution and prove reversibility.", td_style),
            Paragraph(
                "Substitute (2,1) into 2(2)+6(1)=10 and 2+2(1)=4 alongside overlapping lines on the graph. "
                "Show the inverse of each move: R<sub>i</sub>↔R<sub>j</sub>, (1/c)R<sub>i</sub>, and R<sub>i</sub>−kR<sub>j</sub>.",
                td_style,
            ),
            Paragraph("Connect algebra back to the graph and explain why reversibility guarantees no lost or extra solutions.", td_style),
        ],
        [
            Paragraph(f"<b>6. Summary &amp; Credits</b><br/>({fmt_dur(timings, ['06_summary'], '0:22')})", td_bold),
            Paragraph("Reinforce 3 takeaways and cite sources / AI tools.", td_style),
            Paragraph(
                "3 numbered takeaway cards + textbook references (Lay, Strang, Anton &amp; Rorres), "
                "royalty-free Python ambient music credit, and AI assistance disclosure.",
                td_style,
            ),
            Paragraph("Recap the three core takeaways cleanly and thank the viewer.", td_style),
        ],
    ]

    table = Table(rows, colWidths=[34 * mm, 44 * mm, 96 * mm, 94 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), navy),
                ("GRID", (0, 0), (-1, -1), 0.5, border_col),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    elements.append(table)
    doc.build(elements)
    print(f"Generated storyboard PDF: {OUT_PDF}")


if __name__ == "__main__":
    build_pdf()
