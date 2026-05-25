import json
import os
import yaml
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
from modules.tracker import get_db_connection, update_job_score

load_dotenv()

# Load config
with open("job-copilot/config.yaml", "r") as f:
    config = yaml.safe_load(f)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def get_resume_data(path="job-copilot/resume.json"):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def match_job_with_ai(resume_data, job_data):
    """Uses OpenAI to score the match between resume and job description."""
    prompt = f"""
    Compare the following resume data with the job description and provide a match score (0-100) and brief reasoning.
    
    Resume Data:
    {json.dumps(resume_data, indent=2)}
    
    Job Title: {job_data['title']}
    Company: {job_data['company']}
    Description: {job_data['description'] if job_data['description'] else "No description provided."}
    
    Output JSON:
    {{
        "score": 0-100,
        "reasoning": "",
        "missing_skills": [],
        "resume_tweaks": ""
    }}
    """

    response = client.chat.completions.create(
        model=config.get("openai_model", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are an expert career coach and ATS optimization specialist. Output ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" },
        max_tokens=2000
    )
    
    return json.loads(response.choices[0].message.content)

def score_all_new_jobs():
    resume_data = get_resume_data()
    if not resume_data:
        print("No resume data found. Please parse a resume first.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE match_score IS NULL')
    new_jobs = cursor.fetchall()
    conn.close()

    print(f"Scoring {len(new_jobs)} new jobs...")
    for job in new_jobs:
        job_dict = dict(job)
        result = match_job_with_ai(resume_data, job_dict)
        score = result.get("score", 0)
        update_job_score(job_dict['id'], score)
        print(f"Job {job_dict['id']}: {job_dict['title']} - Score: {score}")

if __name__ == "__main__":
    # score_all_new_jobs()
    pass
