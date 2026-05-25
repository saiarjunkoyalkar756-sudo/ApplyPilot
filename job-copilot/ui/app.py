import streamlit as st
import pandas as pd
import json
import os
import yaml
import asyncio
from modules.tracker import get_db_connection, record_application
from modules.parser import process_resume
from modules.scraper import run_scrapers
from modules.matcher import score_all_new_jobs
from modules.resume_builder import generate_tailored_content, create_pdf_resume
from modules.applier import apply_to_job

st.set_page_config(page_title="Job Copilot", layout="wide")

def load_config():
    with open("job-copilot/config.yaml", "r") as f:
        return yaml.safe_load(f)

def save_config(config):
    with open("job-copilot/config.yaml", "w") as f:
        yaml.dump(config, f)

def get_jobs_df():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM jobs ORDER BY match_score DESC", conn)
    conn.close()
    return df

def get_pipeline_df():
    conn = get_db_connection()
    query = """
    SELECT j.title, j.company, a.applied_date, a.status, a.resume_version 
    FROM applications a 
    JOIN jobs j ON a.job_id = j.id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("🚀 Job Copilot")

tabs = st.tabs(["📁 Upload & Config", "🎯 Job Matches", "📈 Pipeline", "📊 Analytics"])

# --- TAB 1: Upload & Config ---
with tabs[0]:
    st.header("Resume Upload")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        with open(f"job-copilot/temp_resume{os.path.splitext(uploaded_file.name)[1]}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        if st.button("Parse Resume"):
            with st.spinner("Parsing resume with AI..."):
                data = process_resume(f"job-copilot/temp_resume{os.path.splitext(uploaded_file.name)[1]}")
                st.success("Resume parsed and saved!")
                st.json(data)

    st.divider()
    st.header("Preferences")
    config = load_config()
    target_roles = st.text_input("Target Roles (comma separated)", value=", ".join(config['target_roles']))
    locations = st.text_input("Locations (comma separated)", value=", ".join(config['locations']))
    if st.button("Save Preferences"):
        config['target_roles'] = [r.strip() for r in target_roles.split(",")]
        config['locations'] = [l.strip() for l in locations.split(",")]
        save_config(config)
        st.success("Preferences saved!")

# --- TAB 2: Job Matches ---
with tabs[1]:
    st.header("Matching Roles")
    col1, col2 = st.columns(2)
    if col1.button("🔍 Scrape New Jobs"):
        with st.spinner("Scraping job boards (LinkedIn)..."):
            asyncio.run(run_scrapers())
            st.success("Scraping complete!")
    
    if col2.button("💯 Score Matches"):
        with st.spinner("Calculating match scores..."):
            score_all_new_jobs()
            st.success("Scoring complete!")

    df = get_jobs_df()
    if not df.empty:
        # Style the dataframe
        st.dataframe(df[['title', 'company', 'location', 'match_score', 'status', 'url']], use_container_width=True)
        
        selected_job_id = st.selectbox("Select a job to tailor application", df['id'].tolist(), format_func=lambda x: f"{df[df['id']==x]['title'].values[0]} at {df[df['id']==x]['company'].values[0]}")
        
        col_tailor, col_apply = st.columns(2)
        
        if col_tailor.button("🛠️ Generate Tailored Resume"):
            job = df[df['id'] == selected_job_id].iloc[0]
            resume_data = json.load(open("job-copilot/resume.json"))
            with st.spinner("Tailoring resume..."):
                content = generate_tailored_content(resume_data, job['title'] + " " + (job['description'] or ""))
                resume_path = f"job-copilot/outputs/tailored_resumes/{job['company'].replace(' ', '_')}_resume.pdf"
                create_pdf_resume(resume_data, content['tailored_bullets'], resume_path)
                st.success(f"Tailored resume generated at {resume_path}")
                st.download_button("Download Tailored Resume", open(resume_path, "rb"), file_name=os.path.basename(resume_path))
                
        if col_apply.button("🚀 Auto-Apply (Headful)"):
            with st.spinner("Launching browser and filling form..."):
                # We need to run the async function
                asyncio.run(apply_to_job(selected_job_id))
                st.success("Application process complete! Check browser or database for status.")
                st.rerun()

        # Mark as applied (simple version for now)
        if st.button("Confirm Applied (Manual)"):
            resume_path = "job-copilot/resume.json" # Placeholder
            record_application(selected_job_id, resume_path)
            st.rerun()

# --- TAB 3: Pipeline ---
with tabs[2]:
    st.header("Application Pipeline")
    pipeline_df = get_pipeline_df()
    if not pipeline_df.empty:
        st.table(pipeline_df)
    else:
        st.info("No applications yet. Go to 'Job Matches' to start applying!")

# --- TAB 4: Analytics ---
with tabs[3]:
    st.header("Analytics")
    if not pipeline_df.empty:
        st.write(f"Total Applications: {len(pipeline_df)}")
        # Simple count by status
        status_counts = pipeline_df['status'].value_counts()
        st.bar_chart(status_counts)
    else:
        st.info("Analytics will appear once you have some applications.")
