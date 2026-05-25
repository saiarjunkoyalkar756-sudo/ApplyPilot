# Job Application Auto-Apply (Local Setup)

The "Auto-Apply" feature uses Playwright in **headful mode** (with a visible browser window) to fill out job applications on your behalf. Since this requires a graphical environment, you should run this project on your **local machine** (Windows, Mac, or Linux with a desktop).

## Setup Instructions

1.  **Clone the project** and navigate to the root directory.
2.  **Install dependencies:**
    ```bash
    pip install -r job-copilot/requirements.txt
    ```
3.  **Install Playwright Browsers:**
    ```bash
    playwright install chromium
    ```
4.  **Configure `.env`:**
    Ensure your `OPENAI_API_KEY` (or OpenRouter key) is set in `job-copilot/.env`.
5.  **Run the Dashboard:**
    ```bash
    python3 job-copilot/main.py
    ```
6.  **Using Auto-Apply:**
    - Go to the **Job Matches** tab.
    - Select a job from the dropdown.
    - Click **🚀 Auto-Apply (Headful)**.
    - A browser window will open, navigate to the job page, and start filling the form.
    - **Human-in-the-loop:** The script will pause before the final submission. Check your terminal/console for the prompt and press **ENTER** to submit, or 'c' to cancel.

## Supported Platforms
- Greenhouse
- Lever
- Workday (Basic detection)
- LinkedIn (Basic detection)
- Indeed (Basic detection)
- Generic forms (Fallback)

## Debugging
- Screenshots of failed attempts are saved in `job-copilot/debug/screenshots/`.
- Session cookies are saved in `job-copilot/cookies/` to help with logins on future applications.
