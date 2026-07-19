import json
import os
import smtplib
import urllib.request
import urllib.parse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
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

# Helper to send email notification
def send_email_notification(name: str, email: str, subject: str, message: str):
    smtp_user = os.environ.get("EMAIL_USER")
    smtp_password = os.environ.get("EMAIL_PASS")
    receiver_email = os.environ.get("SMTP_RECEIVER", "sangramdeshmukh2004@gmail.com")

    if not smtp_user or not smtp_password:
        print("[EMAIL WARNING] EMAIL_USER or EMAIL_PASS variables not set in .env. Skipping email dispatch.")
        return False

    # Normalize Gmail App Password (strip spaces)
    smtp_password = smtp_password.replace(" ", "")

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = receiver_email
        msg["Subject"] = f"[Portfolio Contact] {subject}"

        body = f"""Hello Sangram,

You have received a new message from your portfolio contact form:

--------------------------------------------------
Name: {name}
Email: {email}
Subject: {subject}
--------------------------------------------------

Message:
{message}

--------------------------------------------------
Sent via Portfolio FastAPI Backend
"""
        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, receiver_email, msg.as_string())
        server.quit()
        
        print(f"[EMAIL SUCCESS] Notification email successfully sent to {receiver_email}.")
        return True
    except Exception as err:
        print(f"[EMAIL ERROR] Failed to send email: {err}")
        return False

# Contact Form API Endpoint
@app.post("/api/contact")
async def handle_contact(payload: ContactRequest):
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
        
        # Send email dispatch
        send_email_notification(
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
SYSTEM_PROMPT = """You are Sangram's AI Assistant. Your goal is to answer inquiries about Sangram Deshmukh's profile professionally, politely, and dynamically.
Here are Sangram's profile details:
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

Instructions:
- Keep answers professional, concise, and friendly (max 2-3 sentences where possible).
- Do not make up facts. If asked about something not present, politely say you don't know and invite them to mail Sangram directly.
- You can respond in both English or Hindi/Hinglish depending on how the user asks.
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
            
            return {"status": "success", "reply": reply_text}
    except Exception as err:
        print(f"[CHAT ERROR] Groq API call failed: {err}")
        raise HTTPException(status_code=500, detail="Failed to communicate with LLM API.")

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
