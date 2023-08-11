from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import json
import io

from .s3 import storeFileInBucket


def upload_pdf_to_s3(balanceSheet, news, report_id):
    """
    Generates a PDF report containing balance sheet and news data,
    and uploads it to an S3 bucket.

    :param balanceSheet: Balance sheet data in JSON format.
    :param news: News data in JSON format.
    :param report_id: Unique ID for the report.
    """
    pdf = generate_pdf(balanceSheet, news, report_id)
    pdf.seek(0)
    storeFileInBucket(pdf, fileKey=f"{report_id}.pdf")


def generate_pdf(balanceSheet, news, report_id):
    """
    Generates a PDF report with balance sheet and news data.

    :param balanceSheet: Balance sheet data in JSON format.
    :param news: News data in JSON format.
    :param report_id: Unique ID for the report.
    :return: io.BytesIO containing the generated PDF.
    """
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    story = []

    # Add title
    title_style = getSampleStyleSheet()["Title"]
    story.append(Paragraph(f"Report {report_id}", title_style))
    story.append(Spacer(1, 20))

    # Write balance sheet JSON string line by line
    json_style = getSampleStyleSheet()["BodyText"]
    for line in json.dumps(balanceSheet, indent=4).split('\n'):
        story.append(Paragraph(line, json_style))
    story.append(Spacer(1, 20))

    # Write news JSON string line by line
    for line in json.dumps(news, indent=4).split('\n'):
        story.append(Paragraph(line, json_style))
    
    doc.build(story)

    pdf_buffer.seek(0)
    return pdf_buffer