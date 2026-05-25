import os
import yaml
import json
from openai import OpenAI
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

load_dotenv()

# Load config
with open("job-copilot/config.yaml", "r") as f:
    config = yaml.safe_load(f)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_tailored_content(resume_data, job_description):
    """Uses OpenAI to rewrite resume bullet points and generate a cover letter."""
    prompt = f"""
    Based on the following resume and job description, please provide:
    1. A tailored set of bullet points for the current experience that highlights relevant keywords from the JD.
    2. A 3-paragraph cover letter (Hook, Why fit, Call to action).

    Resume:
    {json.dumps(resume_data, indent=2)}

    Job Description:
    {job_description}

    Output JSON:
    {{
        "tailored_bullets": [],
        "cover_letter": ""
    }}
    """

    response = client.chat.completions.create(
        model=config.get("openai_model", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are an expert resume writer. Output ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" },
        max_tokens=2500
    )
    
    return json.loads(response.choices[0].message.content)

def create_pdf_resume(resume_data, tailored_bullets, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph(f"<b>{resume_data['name']}</b>", styles['Title']))
    story.append(Paragraph(f"{resume_data['email']} | {resume_data['phone']}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("<b>Summary</b>", styles['Heading2']))
    story.append(Paragraph(resume_data.get('summary', ''), styles['Normal']))
    story.append(Spacer(1, 12))

    # Experience
    story.append(Paragraph("<b>Experience</b>", styles['Heading2']))
    # For simplicity, we just use the tailored bullets if provided
    for bullet in tailored_bullets:
        story.append(Paragraph(f"• {bullet}", styles['Normal']))
    
    story.append(Spacer(1, 12))

    # Education
    story.append(Paragraph("<b>Education</b>", styles['Heading2']))
    for edu in resume_data.get('education', []):
        story.append(Paragraph(f"{edu['degree']} - {edu['institution']} ({edu['date']})", styles['Normal']))

    doc.build(story)

def create_cover_letter(content, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Cover Letter</b>", styles['Title']))
    story.append(Spacer(1, 24))
    
    # Split content by paragraphs
    paragraphs = content.split('\n\n')
    for p in paragraphs:
        story.append(Paragraph(p, styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)

if __name__ == "__main__":
    pass
