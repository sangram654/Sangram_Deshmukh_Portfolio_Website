# 🚀 Sangram Deshmukh Portfolio Website

A modern, AI-powered personal portfolio website built with **FastAPI** backend and vanilla **HTML/CSS/JavaScript** frontend. Features a real-time Groq AI chatbot, automated email notifications via Resend API, and is fully deployed on Render.

🌐 **Live Site:** [https://sangram-deshmukh-portfolio-website.onrender.com](https://sangram-deshmukh-portfolio-website.onrender.com)

📦 **GitHub Repo:** [https://github.com/sangram654/Sangram_Deshmukh_Portfolio_Website](https://github.com/sangram654/Sangram_Deshmukh_Portfolio_Website)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Local Setup (From Scratch)](#-local-setup-from-scratch)
- [Environment Variables](#-environment-variables)
- [Running Locally](#-running-locally)
- [Deployment on Render](#-deployment-on-render)
- [Email Integration (Resend API)](#-email-integration-resend-api)
- [AI Chatbot (Groq API)](#-ai-chatbot-groq-api)
- [Custom Domain Setup](#-custom-domain-setup)
- [API Endpoints](#-api-endpoints)

---

## 📌 Project Overview

This is the personal portfolio of **Sangram Deshmukh**, a Data Analyst and aspiring Data Scientist from Pune, India. The portfolio showcases:

- Professional skills in Python, SQL, Power BI, Tableau, Machine Learning
- Featured projects (Sales Dashboard, HR Analytics, etc.)
- Work experience and education
- Contact form with real email delivery
- AI-powered chatbot trained on Sangram's profile

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎨 Modern UI | Dark mode, glassmorphism, animated gradients |
| 🤖 AI Chatbot | Real-time Groq (Llama 3) powered chatbot about Sangram's profile |
| 📧 Email Automation | Contact form submissions sent directly to Gmail via Resend API |
| 📱 Fully Responsive | Works on mobile, tablet, and desktop |
| 🌙 Dark/Light Mode | Theme toggle with smooth transition |
| ⚡ FastAPI Backend | High-performance Python backend with async support |
| 🔒 Secure | `.env` based secrets, `.gitignore` protected, CORS configured |
| ☁️ Cloud Hosted | Deployed on Render with auto-deploy from GitHub |

---

## 🛠 Tech Stack

### Frontend
- **HTML5** — Semantic structure
- **CSS3** — Custom properties, animations, glassmorphism
- **Vanilla JavaScript** — DOM manipulation, Fetch API, chatbot logic

### Backend
- **Python 3.10+**
- **FastAPI** — Web framework with async support
- **Uvicorn** — ASGI server
- **Pydantic** — Data validation
- **python-dotenv** — Environment variable management

### APIs & Services
- **Groq API** (Llama 3.3 70B) — AI chatbot responses
- **Resend API** — Email delivery (HTTPS-based, works on cloud)
- **Render** — Cloud hosting platform

---

## 📁 Project Structure

```
Sangram_Deshmukh_Portfolio_Website/
│
├── index.html              # Main frontend HTML (all sections)
├── styles.css              # All CSS styles, animations, dark mode
├── script.js               # Frontend JS: chatbot, contact form, scroll effects
├── main.py                 # FastAPI backend: API endpoints, email, chatbot
├── requirements.txt        # Python dependencies
├── contact_submissions.json # Local storage for form submissions
│
├── assets/                 # Images, profile photo, etc.
│
├── .env                    # Secret keys (NOT committed to GitHub)
├── .gitignore              # Ignores .env, __pycache__, etc.
└── README.md               # This file
```

---

## 🏁 Local Setup (From Scratch)

### Prerequisites
- Python 3.10 or higher installed
- `pip` package manager
- Git installed

### Step 1 — Clone the Repository

```bash
git clone https://github.com/sangram654/Sangram_Deshmukh_Portfolio_Website.git
cd Sangram_Deshmukh_Portfolio_Website
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `fastapi>=0.100.0`
- `uvicorn>=0.20.0`
- `pydantic[email]>=2.0.0`
- `python-dotenv>=1.0.0`

### Step 3 — Create `.env` File

Create a `.env` file in the project root:

```env
# Gmail credentials (for SMTP fallback)
EMAIL_USER = your_gmail@gmail.com
EMAIL_PASS = your_gmail_app_password

# Groq API (for AI chatbot)
GROQ_API_KEY = gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Resend API (for email delivery on cloud)
RESEND_API_KEY = re_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **Never commit `.env` to GitHub!** It is already listed in `.gitignore`.

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `EMAIL_USER` | Yes | Your Gmail address |
| `EMAIL_PASS` | Yes | Gmail App Password (not your login password) |
| `GROQ_API_KEY` | Yes | Groq API key for AI chatbot |
| `RESEND_API_KEY` | Yes | Resend API key for email delivery |

### How to get Gmail App Password:
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Security → 2-Step Verification (must be ON)
3. App Passwords → Generate → Copy the 16-character password

### How to get Groq API Key:
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Login → API Keys → Create Key

### How to get Resend API Key:
1. Go to [resend.com](https://resend.com)
2. Sign up → Dashboard → API Keys → Create API Key

---

## ▶️ Running Locally

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open your browser: [http://localhost:8000](http://localhost:8000)

The `--reload` flag auto-restarts the server on code changes.

---

## ☁️ Deployment on Render

This project is deployed on **Render** (free tier).

### Step 1 — Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2 — Create Render Web Service
1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click **New → Web Service**
3. Connect your GitHub repo: `sangram654/Sangram_Deshmukh_Portfolio_Website`

### Step 3 — Configure Build Settings

| Setting | Value |
|---|---|
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

### Step 4 — Add Environment Variables

In Render Dashboard → **Environment** tab, add:

| Key | Value |
|---|---|
| `EMAIL_USER` | `sangramdeshmukh2004@gmail.com` |
| `EMAIL_PASS` | `your_app_password` |
| `GROQ_API_KEY` | `gsk_your_groq_key` |
| `RESEND_API_KEY` | `re_your_resend_key` |

### Step 5 — Deploy
Click **Create Web Service** → Render will build and deploy automatically.

🔄 **Auto Deploy:** Every future `git push origin main` will trigger automatic redeployment on Render.

---

## 📧 Email Integration (Resend API)

When a visitor fills the contact form, the backend:

1. Validates the form data (name, email, subject, message)
2. Logs submission to `contact_submissions.json`
3. Sends email via **Resend API** (HTTP-based, no SMTP port issues on cloud)
4. Falls back to **Gmail SMTP (port 465 SSL)** if Resend fails

> **Why Resend instead of SMTP?**  
> Cloud hosting platforms like Render block outbound SMTP ports (25, 587) to prevent spam. Resend uses HTTPS, which is always allowed.

**Free tier:** 3,000 emails/month — more than enough for a portfolio.

---

## 🤖 AI Chatbot (Groq API)

The chatbot on the portfolio is powered by **Groq's Llama 3.3 70B** model.

- Visitors can ask questions about Sangram's skills, projects, experience
- The backend sends a system prompt with Sangram's full profile as context
- Groq returns intelligent, dynamic responses in milliseconds
- If the API fails, a client-side keyword-based fallback responds instead

**API Endpoint:** `POST /api/chat`  
**Request body:** `{ "message": "Tell me about your projects" }`

---

## 🌐 Custom Domain Setup

To use a custom domain like `sangramdeshmukh.com`:

### Step 1 — Buy Domain
Purchase from [Namecheap](https://namecheap.com), [Hostinger](https://hostinger.in), or [BigRock](https://bigrock.in)
- `.com` — ₹800–₹1500/year
- `.in` — ₹500–₹900/year

### Step 2 — Add to Render
1. Render Dashboard → Your Service → **Settings** → **Custom Domains**
2. Click **Add Custom Domain** → Enter your domain

### Step 3 — Update DNS
In your domain provider's DNS settings, add:

```
Type: CNAME
Name: www  (or @)
Value: your-service-name.onrender.com
```

### Step 4 — SSL
Render automatically issues a **free SSL certificate** (HTTPS) for your custom domain.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the portfolio HTML |
| `POST` | `/api/contact` | Handles contact form submission + sends email |
| `POST` | `/api/chat` | AI chatbot query via Groq API |

### POST `/api/contact`
```json
Request:
{
  "name": "Visitor Name",
  "email": "visitor@example.com",
  "subject": "Hello",
  "message": "I want to connect!"
}

Response:
{
  "status": "success",
  "message": "Message logged and processed successfully!"
}
```

### POST `/api/chat`
```json
Request:
{
  "message": "What are Sangram's top skills?"
}

Response:
{
  "reply": "Sangram's top skills include Python, SQL, Power BI..."
}
```

---

## 👤 Author

**Sangram Deshmukh**
- 📧 Email: sangramdeshmukh2004@gmail.com
- 📱 Phone: +91 9270836897 / +91 9561563002
- 💼 LinkedIn: [linkedin.com/in/sangram-deshmukh-530b512aa](https://www.linkedin.com/in/sangram-deshmukh-530b512aa)
- 🐙 GitHub: [github.com/sangram654](https://github.com/sangram654)
- 📍 Location: Pune, India

---

## 📄 License

This project is personal portfolio work. Feel free to use it as inspiration for your own portfolio!
