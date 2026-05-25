import pdfplumber
import docx
import json
import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load config
with open("job-copilot/config.yaml", "r") as f:
    config = yaml.safe_load(f)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_resume_with_ai(resume_text):
    """Uses OpenAI to extract structured JSON from raw resume text."""
    prompt = f"""
    Extract the following information from the resume text and return it as a structured JSON object:
    - name
    - email
    - phone
    - skills: {{ "technical": [], "soft": [] }}
    - experience: [ {{ "title": "", "company": "", "dates": "", "description": "", "years": 0 }} ]
    - education: [ {{ "degree": "", "institution": "", "date": "" }} ]
    - certifications: []
    - summary: ""

    Resume Text:
    {resume_text}
    """

    response = client.chat.completions.create(
        model=config.get("openai_model", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are an expert HR data extractor. Output ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" },
        max_tokens=2000
    )
    
    return json.loads(response.choices[0].message.content)

def save_resume_data(data, output_path="job-copilot/resume.json"):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def process_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please use PDF or DOCX.")
    
    structured_data = parse_resume_with_ai(text)
    save_resume_data(structured_data)
    return structured_data

if __name__ == "__main__":
    # Example usage (would be triggered by UI)
    # print(process_resume("path/to/resume.pdf"))
    pass
