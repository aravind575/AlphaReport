from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import json
import io

def generate_pdf(data, report_id):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    story = []

    # Add a title
    title_style = getSampleStyleSheet()["Title"]
    story.append(Paragraph(f"Report {report_id}", title_style))
    story.append(Spacer(1, 20))

    # Write JSON string line by line
    json_style = getSampleStyleSheet()["BodyText"]
    for line in json.dumps(data, indent=4).split('\n'):
        story.append(Paragraph(line, json_style))
    
    doc.build(story)

    pdf_buffer.seek(0)
    with open('report.pdf', 'wb') as pdf_file:
        pdf_file.write(pdf_buffer.getvalue())
