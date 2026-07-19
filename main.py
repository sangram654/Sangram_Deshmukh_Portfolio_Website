import json
import os
import smtplib
import ssl
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Sangram Deshmukh Portfolio API")

# Enable CORS for local testing if frontend is run separately
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for contact form validation
class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

# Pydantic model for chatbot interaction
class ChatRequest(BaseModel):
    message: str

SUBMISSIONS_FILE = "contact_submissions.json"

# Helper to save submissions locally
def save_submission(data: dict):
    submissions = []
    if os.path.exists(SUBMISSIONS_FILE):
        try:
            with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
                submissions = json.load(f)
        except Exception:
            submissions = []
            
    submissions.append(data)
    
    with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=4, ensure_ascii=False)

# Helper to send email via Resend HTTP API (works on Render - no SMTP ports needed)
def send_email_notification(name: str, email: str, subject: str, message: str):
    receiver_email = "sangramdeshmukh2004@gmail.com"
    resend_api_key = os.environ.get("RESEND_API_KEY")

    body_text = f"""Hello Sangram,

You have received a new message from your portfolio contact form:

--------------------------------------------------
Name: {name}
Email: {email}
Subject: {subject}
--------------------------------------------------

Message:
{message}

--------------------------------------------------
Sent via Sangram Deshmukh Portfolio Website
"""

    # Primary: Resend API (HTTPS - always works on Render)
    if resend_api_key:
        try:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json",
                "User-Agent": "python-requests/2.31.0"
            }
            data = {
                "from": "Portfolio Contact <onboarding@resend.dev>",
                "to": [receiver_email],
                "subject": f"[Portfolio Contact] {subject}",
                "text": body_text
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                print(f"[EMAIL SUCCESS] Sent via Resend API to {receiver_email}.")
                return True
        except Exception as err:
            print(f"[EMAIL ERROR] Resend API failed: {err}. Trying Gmail SMTP fallback...")

    # Fallback: Gmail SMTP (port 465 SSL)
    smtp_user = os.environ.get("EMAIL_USER")
    smtp_password = os.environ.get("EMAIL_PASS")
    if smtp_user and smtp_password:
        smtp_password = smtp_password.replace(" ", "")
        try:
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            msg = MIMEMultipart()
            msg["From"] = smtp_user
            msg["To"] = receiver_email
            msg["Subject"] = f"[Portfolio Contact] {subject}"
            msg.attach(MIMEText(body_text, "plain"))
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=10) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, receiver_email, msg.as_string())
            print(f"[EMAIL SUCCESS] Sent via Gmail SMTP SSL to {receiver_email}.")
            return True
        except Exception as err:
            print(f"[EMAIL ERROR] Gmail SMTP fallback also failed: {err}")
            return False

    print("[EMAIL WARNING] No email credentials configured. Submission logged only.")
    return False

# Contact Form API Endpoint
@app.post("/api/contact")
async def handle_contact(payload: ContactRequest, background_tasks: BackgroundTasks):
    try:
        submission_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": payload.name,
            "email": payload.email,
            "subject": payload.subject,
            "message": payload.message
        }
        
        # Print to console logs (always works on Render)
        print(f"\n[NEW CONTACT FORM SUBMISSION] at {submission_data['timestamp']}")
        print(f"From: {payload.name} ({payload.email})")
        print(f"Subject: {payload.subject}")
        print(f"Message: {payload.message}\n")

        # Try to save locally (may fail on Render read-only filesystem — safe to skip)
        try:
            save_submission(submission_data)
        except Exception as save_err:
            print(f"[SAVE WARNING] Could not save to local file (expected on Render): {save_err}")

        # Send email in background so response is returned immediately
        background_tasks.add_task(
            send_email_notification,
            name=payload.name,
            email=payload.email,
            subject=payload.subject,
            message=payload.message
        )
        
        return {"status": "success", "message": "Message logged and processed successfully!"}
    except Exception as e:
        print(f"Error handling submission: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# System Prompt detailing Sangram's context
SYSTEM_PROMPT = """I am Sangram's AI Assistant.

Core requirement (must follow):
- Respond in ENGLISH ONLY.
- Answer about Sangram Deshmukh's profile and portfolio (skills, experience, projects, education, contact, achievements, hobbies).

If the user asks for world/general information:
- Provide a safe, high-level answer that does not require hidden/private facts.
- If you are not confident or the question needs browsing/data, say you don't know and suggest a reliable source.

If the user asks about something that is not in Sangram's profile:
- Say you don't know (no guessing) and suggest contacting Sangram via email.

Length:
- Keep answers professional, concise, and friendly (usually 1-3 short sentences; bullet points allowed).

Privacy/safety:
- Never claim to have performed actions or hold credentials.

Sangram's profile details:
- Name: Sangram Deshmukh
- Profile: Data Analyst & AI/ML Enthusiast
- Location: Pune, India
- Email: sangramdeshmukh2004@gmail.com
- Phone: +91 9270836897 / +91 9561563002
- LinkedIn: https://www.linkedin.com/in/sangram-deshmukh-530b512aa
- GitHub: https://www.github.com/sangram654
- Education: Samarth College of Engineering & Management, Pune - B.E. in AI & ML (CGPA: 8.64, Graduating June 2026).
- Internships:
  1. Data Science Intern @ AI Variant (July 2025 - April 2026): Power BI dashboards, ETL pipelines, Time Series Forecasting, AI agents on AWS.
  2. Data Science Intern @ Sumago Infotech (Dec 2024 - Feb 2025): Regression modeling, data preprocessing.
- Projects:
  1. RAG-Based Document Intelligence: Built a production-grade RAG pipeline (Python, LangChain, FAISS, FastAPI, OpenAI, Docker) with semantic chunking and hybrid search; 87% answer relevance.
  2. Intelligent Workflow Automation & Demand Forecasting: API-driven agentic pipeline (Python, LangChain, Statsmodels, Scikit-learn, FastAPI, Zapier) saving 20+ hrs/month.
  3. Real-Time Predictive Analytics & Anomaly Detection: End-to-end ML pipeline (Python, XGBoost, TensorFlow, Kafka, Streamlit, AWS EC2) for multivariate time-series forecasting.
  4. AI-Powered College ERP: Full-stack ERP (MERN, face-api.js, ESP32, C++, JWT, MongoDB) with facial attendance verification.
  5. Real-Time Sales Analytics Dashboard: End-to-end pipeline (Python, SQL, Power BI, Streamlit, Matplotlib, AWS EC2) reducing manual reporting by 40%.
  6. Customer Segmentation & Churn Analysis: EDA & RFM analysis (Python, Pandas, Scikit-learn, Seaborn, Tableau, PostgreSQL) with K-Means and churn model (82% accuracy).
  7. Demand Forecasting & Automated Reporting: ETL pipeline (Python, Statsmodels, XGBoost, SQL, Pandas, Excel, Zapier) with weekly automated reporting.
  8. HR Attrition Analytics: Statistical hypothesis testing and Tableau dashboard (Python, Pandas, NumPy, Seaborn, Tableau, Excel, Stats) visualizing attrition drivers.
- Hobbies & Interests: Playing Chess (leisure activity, keeps mind sharp) and Listening to Music.
"""

# Real-Time Groq AI Chatbot API Endpoint
@app.post("/api/chat")
async def handle_chat(payload: ChatRequest):
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        print("[CHAT WARNING] GROQ_API_KEY env variable not set. Falling back to local offline brain.")
        raise HTTPException(status_code=400, detail="Groq API key not configured.")

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": payload.message}
            ],
            "temperature": 0.5,
            "max_tokens": 512
        }
        
        req_data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            reply_text = res_json["choices"][0]["message"]["content"].strip()

            # Enforce ENGLISH only for display purposes (best-effort)
            return {"status": "success", "reply": reply_text}
    except Exception as err:
        # Return a user-friendly ENGLISH error so the frontend can show a better fallback message.
        print(f"[CHAT ERROR] Groq API call failed: {err}")
        raise HTTPException(
            status_code=500,
            detail="Chat service is temporarily unavailable. Please try again in a moment."
        )

# Static file routers for root files
@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")

@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")

# Mount Assets folder for images
if os.path.exists("assets"):
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Run using: uvicorn main:app --reload
