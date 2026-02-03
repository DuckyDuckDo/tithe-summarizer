from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

import pandas as pd
from pathlib import Path
from datetime import date

# ================= CONFIG =================
CSV_PATH = "Tithe By Person.csv"
OUTPUT_DIR = Path("Donation_Receipts_2025")

TAX_YEAR = 2025
ISSUE_DATE = "02/8/2026"

CHARITY_NAME_EN = "Vietnamese Gospel Outreach Ministry of N.E"
CHARITY_NAME_VI = "HỘI THÁNH TRUYỀN BÁ PHÚC ÂM N.E"

ADDRESS = "101 Main Street, Saugus, MA 01906"
PASTOR = "Quản Nhiệm: Rev. Bùi Hữu Trí"
EMAIL = "Email: Huutri_b@yahoo.com"
PHONE = "Phone: 781-789-8255 (cell) | 781-558-2995 (office)"
EIN = "42-1569926"

TREASURER = "David Do"
FUND = "General Fund"
# =========================================

OUTPUT_DIR.mkdir(exist_ok=True)

# Load data (no header expected)
df = pd.read_csv(CSV_PATH, header=None, names=["Name", "Amount"])
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df = df.dropna()

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    alignment=TA_CENTER,
    fontSize=14,
    leading=16,
    spaceAfter=8,
    fontName = "DejaVu",
)

center_style = ParagraphStyle(
    "Center",
    parent=styles["Normal"],
    alignment=TA_CENTER,
    fontSize=10,
    leading=14,
    fontName = "DejaVu",
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    fontName = "DejaVu",
)

for _, row in df.iterrows():
    name = row["Name"]
    amount = row["Amount"]

    safe_name = name.replace(" ", "_").replace("/", "-")
    pdf_path = str(OUTPUT_DIR / f"{safe_name}_{TAX_YEAR}.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=LETTER,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    elements = []

    # ---------- HEADER ----------
    elements.append(Paragraph(CHARITY_NAME_EN, title_style))
    elements.append(Paragraph(CHARITY_NAME_VI, center_style))
    elements.append(Spacer(1, 0.1 * inch))

    elements.append(Paragraph(ADDRESS, center_style))
    elements.append(Paragraph(PASTOR, center_style))
    elements.append(Paragraph(EMAIL, center_style))
    elements.append(Paragraph(PHONE, center_style))
    elements.append(Paragraph(f"Tax ID (EIN): {EIN}", center_style))

    elements.append(Spacer(1, 0.2 * inch))

    # ---------- TITLE ----------
    elements.append(Paragraph("Biên Nhận Dâng Hiến / Contribution Receipt", title_style))
    elements.append(Paragraph(f"Năm / Year {TAX_YEAR}", center_style))

    elements.append(Spacer(1, 0.2 * inch))

    # ---------- BODY ----------
    elements.append(Paragraph(
        "Chân thành cảm tạ Chúa đã dùng quý vị và gia đình trong sự dâng hiến rộng rãi, "
        "cầu nguyện, mở rộng vương quốc Đức Chúa Trời. "
        "Nguyện xin Chúa ban thêm ơn cho quý vị một cách dồi dào.",
        body_style
    ))

    elements.append(Spacer(1, 0.1 * inch))

    elements.append(Paragraph(
        "Praise the Lord for He has used you and your family in the past year through generous contributions, "
        "prayers, for the expansion of the kingdom of God. "
        "May the Lord continue to bless you and your family abundantly.",
        body_style
    ))

    elements.append(Spacer(1, 0.2 * inch))

    # ---------- DETAILS ----------
    table_data = [
        ["Đã nhận từ / Received from:", name],
        ["Số tiền / Amount:", f"${amount:,.2f}"],
        ["Quỹ / Fund:", FUND],
        ["Ngày phát hành / Date issued:", ISSUE_DATE],
    ]

    table = Table(table_data, colWidths=[2.6 * inch, 3.4 * inch])
    table.setStyle([
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu")])
    elements.append(table)

    elements.append(Spacer(1, 0.3 * inch))

    # ---------- SIGNATURE ----------
    elements.append(Paragraph("Thủ Quỹ / Treasurer", body_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(TREASURER, body_style))

    elements.append(Spacer(1, 0.4 * inch))

    # ---------- FOOTER ----------
    elements.append(Paragraph(
        "Số tiền trên có thể được trừ thuế.<br/>"
        "Tax deductible, you may use this receipt for tax purpose.<br/>"
        "No goods or services were provided in exchange for this contribution.",
        body_style
    ))

    doc.build(elements)

print(f"Generated {len(df)} receipts in '{OUTPUT_DIR}'")
