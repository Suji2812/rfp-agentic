import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import datetime

def generate_pdf_report(rfp: dict, recommendations: list):
    """
    recommendations: list of dicts with keys sku,name,score, pricing (dict)
    returns bytes of PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"RFP Response: {rfp.get('id')} - {rfp.get('title')}", styles['Title']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("RFP Summary:", styles['Heading2']))
    for k in ["deadline", "quantity"]:
        if k in rfp:
            story.append(Paragraph(f"<b>{k.capitalize()}:</b> {rfp[k]}", styles['Normal']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("RFP Specs:", styles['Heading3']))
    for spec_k, spec_v in rfp.get("specs", {}).items():
        story.append(Paragraph(f"- {spec_k}: {spec_v}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Table header
    table_data = [["Rank", "SKU", "Product", "Spec Match %", "Unit Price", "Test Cost", "Total Est. Cost"]]
    for idx, rec in enumerate(recommendations, 1):
        pricing = rec.get("pricing", {})
        table_data.append([
            idx,
            rec.get("sku"),
            rec.get("name"),
            f"{rec.get('score')}%",
            f"{pricing.get('unit_price', 'N/A')}",
            f"{pricing.get('test_cost', 'N/A')}",
            f"{pricing.get('total_cost', 'N/A')}"
        ])

    t = Table(table_data, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Add footnote
    story.append(Paragraph("Notes:", styles['Heading3']))
    story.append(Paragraph(
        "This is a demo/hackathon prototype. Spec matching uses simple heuristic scoring; "
        "pricing is from mock data.", styles['Normal']))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

