# 📖 Usage Guide: ApplyPilot

This guide provides step-by-step instructions on how to use the **ApplyPilot** platform to automate your job application process.

---

## 1. Starting the Platform

Before using the platform, ensure the infrastructure and microservices are running.

### Start Infrastructure
```bash
make start
```
This starts PostgreSQL, Redis, RabbitMQ, and other required services.

### Start Services
In separate terminals, run:
```bash
make start-auth      # Port 8001
make start-parser    # Port 8002
make start-scraper   # Port 8003
make start-matcher   # Port 8004
make start-resume    # Port 8005
make start-applier   # Port 8006
make start-frontend  # Port 3000
```

---

## 2. User Workflow

### Step 1: Authentication
1. Open the dashboard at `http://localhost:3000`.
2. Register a new account or log in.
3. Your `access_token` will be stored securely to authorize subsequent requests.

### Step 2: Upload & Parse Resume
1. Navigate to the **"Upload"** section.
2. Select your resume (PDF or DOCX).
3. Click **"Parse Resume"**.
4. The **Parser Service** will extract your skills, experience, and certifications into a structured JSON format.

### Step 3: Search for Jobs
1. Go to the **"Job Discovery"** tab.
2. Enter your target roles (e.g., "Python Developer") and locations (e.g., "Remote").
3. Click **"Scrape Jobs"**.
4. The **Scraper Service** will queue background tasks to fetch the latest listings from Indeed and LinkedIn.

### Step 4: Analyze Matches
1. Once scraping is complete, go to **"Match Scores"**.
2. Click **"Calculate Matches"**.
3. The **Matcher Service** will compare your parsed resume against the job descriptions and provide a percentage score (0-100%).
4. Filter for jobs with a score of **70%+**.

### Step 5: Tailor Your Application
1. Select a high-matching job.
2. Click **"Tailor Resume"**.
3. The **Resume Builder Service** uses AI to rewrite your bullet points to align with the specific job description and generates a tailored PDF.

### Step 6: Automate the Application
1. Click **"🚀 Auto-Apply"**.
2. The **Applier Service** will launch a Playwright browser instance.
3. You can watch the progress via the real-time screenshot stream in the dashboard.
4. **Human-in-the-loop:** If the "auto-submit" setting is off, the process will pause at the final page. Review the details and click **"Approve & Submit"**.

---

## 3. Monitoring & Analytics

### Application Pipeline
Track all your applications in the **"Pipeline"** view. Statuses include:
- `queued`: Waiting for a worker.
- `filling_form`: Browser automation in progress.
- `awaiting_approval`: Paused for your review.
- `submitted`: Application successfully sent.
- `rejected/ghosted`: Track long-term outcomes.

### Technical Monitoring
For developers, monitoring tools are available at:
- **Jaeger (Tracing):** `http://localhost:16686`
- **MailHog (Email testing):** `http://localhost:8025`
- **RabbitMQ Management:** `http://localhost:15672`

---

## 4. Troubleshooting

- **Scraper Blocked:** If you see "bot detection" errors, ensure you are using residential proxies in `config.yaml` or increase the `SCRAPER_DELAY_MIN` setting.
- **Parser Errors:** Ensure your PDF is text-based and not a scanned image. If scanned, the parser will require an OCR-enabled worker.
- **Database Connection:** If services fail to start, verify that the Postgres container is healthy by running `docker ps`.

---

**Happy Job Hunting with ApplyPilot!**
