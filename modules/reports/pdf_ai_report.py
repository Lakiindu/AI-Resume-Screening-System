from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_ai_report(data):
    """
    Generates a professional AI Candidate Evaluation PDF.
    """

    buffer = BytesIO()

    pdf = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    elements = []

    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "AI Resume Screening System",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "AI Candidate Evaluation Report",
            heading_style
        )
    )

    elements.append(Spacer(1, 20))

    # --------------------------------------------------
    # Candidate Information
    # --------------------------------------------------

    elements.append(Paragraph("<b>Candidate Information</b>", heading_style))

    candidate_table = Table([
        ["Candidate", data["candidate_name"]],
        ["Email", data["email"]],
        ["Phone", data["phone"]],
        ["Applied Job", data["job_title"]],
        ["Department", data["department"]],
        ["Location", data["location"]]
    ])

    candidate_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),
        ("BOTTOMPADDING",(0,0),(-1,-1),8)
    ]))

    elements.append(candidate_table)

    elements.append(Spacer(1,20))

    # --------------------------------------------------
    # AI Match Score
    # --------------------------------------------------

    elements.append(
        Paragraph("<b>AI Evaluation</b>", heading_style)
    )

    score_table = Table([
        ["TF-IDF Similarity", f'{data["tfidf_score"]:.2f}%'],
        ["Skill Match", f'{data["skill_score"]:.2f}%'],
        ["Final Score", f'{data["final_score"]:.2f}%'],
        ["Recommendation", data["recommendation"]]
    ])

    score_table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightblue),
        ("BOTTOMPADDING",(0,0),(-1,-1),8)
    ]))

    elements.append(score_table)

    elements.append(Spacer(1,20))

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------

    elements.append(
        Paragraph("<b>Matched Skills</b>", heading_style)
    )

    elements.append(
        Paragraph(
            data["matched_skills"] or "None",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1,12))

    elements.append(
        Paragraph("<b>Missing Skills</b>", heading_style)
    )

    elements.append(
        Paragraph(
            data["missing_skills"] or "None",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1,20))

    # --------------------------------------------------
    # Resume Analysis
    # --------------------------------------------------

    elements.append(
        Paragraph("<b>Resume Analysis</b>", heading_style)
    )

    analysis = Table([
        ["Education", data["education"] or "Not detected"],
        ["Experience", data["experience"] or "Not detected"],
        ["Projects", data["projects"] or "Not detected"],
        ["Certificates", data["certificates"] or "Not detected"],
        ["Languages", data["languages"] or "Not detected"]
    ])

    analysis.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.beige),
        ("BOTTOMPADDING",(0,0),(-1,-1),8)
    ]))

    elements.append(analysis)

    elements.append(Spacer(1,25))

    # --------------------------------------------------
    # AI Recommendation
    # --------------------------------------------------

    recommendation = f"""
    Based on AI analysis, the candidate achieved a
    final match score of <b>{data['final_score']:.2f}%</b>.

    Recommendation:
    <b>{data['recommendation']}</b>.
    """

    elements.append(
        Paragraph("<b>AI Recommendation</b>", heading_style)
    )

    elements.append(
        Paragraph(recommendation, styles["BodyText"])
    )

    elements.append(Spacer(1,20))

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "<i>Generated automatically by AI Resume Screening System.</i>",
            styles["Italic"]
        )
    )

    pdf.build(elements)

    buffer.seek(0)

    return buffer