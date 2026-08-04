# ✉️ Python Email Automation System

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![APScheduler](https://img.shields.io/badge/APScheduler-3.11.3-green.svg?style=for-the-badge&logo=clock&logoColor=white)
![SMTP Protocol](https://img.shields.io/badge/SMTP-Gmail_TLS-red.svg?style=for-the-badge&logo=gmail&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/Production-Ready-brightgreen.svg?style=for-the-badge)

**A modular, enterprise-ready Python Email Automation System for automated job application outreach via Gmail SMTP.**

[Features](#-features) • [Installation](#-installation-guide) • [Gmail Setup](#-gmail-smtp-configuration) • [Architecture](#-project-architecture) • [Troubleshooting](#-troubleshooting) • [FAQ](#-faq)

</div>

---

## 📌 Project Overview

### Why This Project Exists
Applying to 100+ hiring managers and HR recruiters manually is exhausting, prone to copy-paste errors, lacks consistent follow-up timing, and risks Gmail spam flags if sent too rapidly.

The **Python Email Automation System** was engineered to automate job application email dispatches directly from your local machine while adhering strictly to production software engineering standards, anti-spam rate limiting, and robust error recovery protocols.

### What Problem It Solves
1. **Eliminates Repetitive Manual Work**: Automatically formats personalized cover emails and attaches resume PDFs.
2. **Protects Against Gmail Spam Flags**: Implements randomized sleep delays (25s to 60s) between dispatches to comply with Gmail anti-spam algorithms.
3. **Prevents Duplicate Emails**: Tracks daily delivery history so recruiters are never emailed twice on the same date.
4. **Ensures Automated Schedule**: Runs daily at optimal hiring hours (**09:00 AM, 10:00 AM, 01:00 PM, and 02:00 PM**) without manual intervention.
5. **Personalizes Applications at Scale**: Extracts company names from recruiter email domains (e.g. `hr@google.com` $\rightarrow$ `Dear Google Hiring Team,`).

### Main Objective
To provide a zero-cost, local, scalable Python solution for developers to send high-volume, personalized job application emails reliably with real-time feedback and detailed audit trails.

---

## 🚀 Features

| Category | Feature | Description |
| :--- | :--- | :--- |
| **Scheduler** | **Daily APScheduler Engine** | Runs daily cron tasks at 09:00 AM, 10:00 AM, 01:00 PM, and 02:00 PM. |
| **Authentication**| **Gmail TLS SMTP Auth** | Establishes encrypted TLS connections (port 587) using 16-character App Passwords. |
| **Personalization**| **Smart Salutation Engine** | Parses domain names (e.g., `careers@microsoft.com` $\rightarrow$ `Dear Microsoft Hiring Team,`). |
| **Validation** | **RFC 5322 Syntax Checking** | Validates email syntax using regex, strips whitespace, and skips invalid entries. |
| **Anti-Spam** | **Dynamic Rate Limiting** | Introduces random sleep delays (25 to 60 seconds) between consecutive dispatches. |
| **Resilience** | **Exponential Backoff Retry** | Automatically retries failed sends up to 3 times ($2\text{s} \rightarrow 4\text{s} \rightarrow 8\text{s}$). |
| **Deduplication** | **Daily Sent History Guard** | Tracks successfully delivered emails to avoid duplicate sends on the same day. |
| **Attachment** | **Resume PDF Encoding** | Automatically attaches and MIME-encodes your resume PDF (`application/pdf`). |
| **Progress** | **Live Terminal `tqdm` Bar** | Displays real-time progress, sent/failed metrics, and rate-limiting countdowns. |
| **Audit Logs** | **Dual CSV & Text Logging** | Generates `logs/email_log.csv` and `logs/email_log.txt` for audit trails. |
| **Tracking** | **Success & Failure Lists** | Maintains clean text lists in `success_emails.txt` and `failed_emails.txt`. |
| **Summary** | **Execution Report** | Prints complete metrics summary (Total, Sent, Failed, Skipped, Time) after every run. |
| **CLI Modes** | **Flexible Operating Modes** | Supports `--schedule` (cron loop), `--now` (immediate run), and `--validate` (syntax check). |

---

## 🖼️ Project Screenshots

*(Add UI / Terminal execution screenshots here)*

```
+-----------------------------------------------------------------------------------+
| 🚀 PYTHON EMAIL AUTOMATION BATCH INITIALIZED                                      |
| • Total Email Records Found : 101                                                 |
| • Valid & Pending Emails    : 101                                                 |
| • Already Sent Today        : 0                                                   |
+-----------------------------------------------------------------------------------+
| Sending Emails:  45%|███████████████           | 45/101 [18:45<22:15, 23.8s/email] |
| Postfix: Current: hr@google.com | Sent: 42 | Failed: 1 | Rem: 56                      |
+-----------------------------------------------------------------------------------+
```

---

## 🛠️ Tech Stack

| Component | Library / Tool | Purpose |
| :--- | :--- | :--- |
| **Core Language** | `Python 3.10+` | Primary programming language runtime. |
| **Scheduler Engine** | `APScheduler (3.11.3)` | Cron-style task scheduling for daily automation. |
| **Secrets Manager** | `python-dotenv (1.2.2)` | Environment variable loading from `.env`. |
| **Console UI** | `tqdm (4.70.0)` | Live terminal progress bar rendering. |
| **Timezone Utility** | `tzlocal (5.4.4)` | Cross-platform system timezone resolver. |
| **SMTP Client** | `smtplib` *(Standard)* | Low-level TCP connection & TLS authentication. |
| **MIME Builder** | `email.mime` *(Standard)* | Multipart email & attachment composition. |
| **Syntax Validator**| `re` *(Standard)* | Regular expression engine for RFC 5322 validation. |
| **Audit Logger** | `logging`, `csv` *(Standard)*| Dual structured CSV and text log creation. |
| **CLI Parser** | `argparse` *(Standard)* | Command-line argument parsing (`--now`, `--schedule`, `--validate`). |
| **Path Resolver** | `pathlib` *(Standard)* | Cross-platform filesystem path handling. |

---

## 📁 Project Structure

```
JobMailer/
├── main.py                  # Main CLI entry point & batch execution controller
├── scheduler.py             # APScheduler daily cron job manager (09:00, 10:00, 13:00, 14:00)
├── email_sender.py          # MIME builder, SMTP client & exponential backoff retry engine
├── email_validator.py       # RFC 5322 regex validator & daily duplicate filtering logic
├── logger.py                # Dual console/file logger and CSV audit log recorder
├── config.py                # Environment loader, path resolver & credential validator
├── utils.py                 # Domain parser, salutation generator & rate-limiting delay helper
├── requirements.txt         # Frozen third-party Python package dependencies
├── emails.txt               # Recipient email list (1 address per line)
├── .env                     # Private secret credentials file (Git ignored)
├── .env.example             # Template file for environment setup
├── .gitignore               # Protection rules to keep secrets, logs & cache out of Git
├── README.md                # System documentation & operating manual
│
├── logs/                    # Log output directory (Auto-created)
│   ├── email_log.csv        # Structured CSV log file (Date, Time, Recipient, Status, Error, SMTP)
│   └── email_log.txt        # Detailed plain text execution log
│
└── resume/                  # Resume PDF attachment directory (Auto-created)
    └── Vaibhav_Sharma_Resume.pdf  # Target PDF resume file
```

### Module File Responsibilities & Communications

- **`config.py`**: Reads `.env` settings via `load_dotenv()`, resolves absolute paths for logs and resume files, and validates that critical settings are present.
- **`logger.py`**: Configures console logging, plain-text log files (`logs/email_log.txt`), and CSV output (`logs/email_log.csv`).
- **`email_validator.py`**: Reads `emails.txt`, cleans inputs, validates email syntax using RFC 5322 regex, and checks `success_emails.txt` to skip addresses already emailed today.
- **`utils.py`**: Extracts company names from corporate email domains (`hr@google.com` $\rightarrow$ `Google`), generates custom salutations (`Dear Google Hiring Team,`), and generates random delays (25s–60s).
- **`email_sender.py`**: Constructs MIME emails, attaches the resume PDF, connects via Gmail TLS SMTP (port 587), and handles up to 3 retries with exponential backoff ($2\text{s} \rightarrow 4\text{s} \rightarrow 8\text{s}$).
- **`scheduler.py`**: Sets up `APScheduler` cron jobs for daily execution at 09:00 AM, 10:00 AM, 01:00 PM, and 02:00 PM.
- **`main.py`**: Orchestrates CLI commands (`--now`, `--schedule`, `--validate`), drives the `tqdm` progress bar, and outputs the final summary report.

---

## 🏗️ Project Architecture

```
                       ┌──────────────┐
                       │   main.py    │
                       └──────┬───────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │ scheduler.py │    │  config.py   │    │  logger.py   │
  └──────┬───────┘    └──────┬───────┘    └──────────────┘
         │                   │
         ▼                   │
 ┌────────────────┐          │
 │execute_email_  │          │
 │     batch()    │          │
 └───────┬────────┘          │
         │                   │
         ├───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌──────────────────┐ ┌───────────────┐ ┌──────────────────┐
│email_validator.py│ │   utils.py    │ │ email_sender.py  │
└──────────────────┘ └───────────────┘ └──────────────────┘
```

---

## 🔄 Complete Execution Workflow

When you run `python main.py --now` or when the scheduler triggers at a scheduled time:

```
[1] Load Config (.env) ──> [2] Validate Credentials & Resume PDF
                                        │
[4] Load emails.txt <── [3] Environment Check Passed
         │
         ▼
[5] Validate RFC 5322 Syntax ──> [6] Check Today's Sent History (Deduplicate)
                                                 │
[8] Connect Gmail SMTP (TLS 587) <── [7] Prepare Pending Recipients List
         │
         ▼
[9] Authenticate App Password ──> [10] Generate Custom Salutation (utils.py)
                                                 │
[12] Attach Resume PDF <── [11] Build MIME Message Body
         │
         ▼
[13] Send Email (Retry up to 3x if error) ──> [14] Log Result (CSV, TXT, success_emails.txt)
                                                             │
[16] Next Recipient <── [15] Sleep Random Delay (25s - 60s) ─┘
         │
         ▼
[17] Batch Complete ──> [18] Display Execution Summary Report
```

---

## 💻 Installation Guide

### Linux / macOS Setup

```bash
# 1. Clone repository
git clone https://github.com/YourUsername/JobMailer.git
cd JobMailer

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Windows Setup

```cmd
:: 1. Navigate to project folder
cd C:\Users\YourUsername\Projects\JobMailer

:: 2. Create virtual environment
python -m venv venv

:: 3. Activate virtual environment (Command Prompt)
venv\Scripts\activate.bat

:: 4. Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

:: 5. Install dependencies
pip install -r requirements.txt
```

---

## 🐍 Python Version Requirements

Requires **Python 3.10** or higher.

### Check Installed Python Version
```bash
python3 --version
```

### Installing Python if Missing
- **Ubuntu/Debian**: `sudo apt update && sudo apt install -y python3 python3-venv python3-pip`
- **macOS**: `brew install python`
- **Windows**: Download installer from [python.org](https://www.python.org/downloads/) (Select **"Add Python to PATH"**).

---

## 🌐 Virtual Environment Management

Using a virtual environment isolates project dependencies from your system Python.

| Action | Linux / macOS | Windows |
| :--- | :--- | :--- |
| **Create** | `python3 -m venv venv` | `python -m venv venv` |
| **Activate** | `source venv/bin/activate` | `venv\Scripts\activate.bat` |
| **Deactivate** | `deactivate` | `deactivate` |

---

## 📦 Dependencies

Inside **`requirements.txt`**:

```txt
APScheduler==3.11.3
python-dotenv==1.2.2
tqdm==4.70.0
tzlocal==5.4.4
```

- **`APScheduler`**: Background cron job runner for daily automation.
- **`python-dotenv`**: Environment configuration manager.
- **`tqdm`**: Terminal progress visualization bar.
- **`tzlocal`**: System timezone resolver for scheduler triggers.

---

## 🔑 Gmail SMTP Configuration & App Password Setup

> ⚠️ **CRITICAL REQUIREMENT**: Standard Gmail passwords **CANNOT** be used for SMTP authentication. Google blocks password logins and throws `534 5.7.9 Application-specific password required`. You MUST generate a 16-character **App Password**.

### Step-by-Step App Password Generation Guide

1. **Step 1**: Go to **[Google Account Settings](https://myaccount.google.com/)**.
2. **Step 2**: Click on **Security** in the left menu.
3. **Step 3**: Under *How you sign in to Google*, ensure **2-Step Verification** is **ON**.
4. **Step 4**: Open **[Google App Passwords](https://myaccount.google.com/apppasswords)**.
5. **Step 5**: In **App Name**, type `JobMailer` or `Python Email Automation`.
6. **Step 6**: Click **Create**.
7. **Step 7**: Google generates a **16-character passcode** (e.g. `abcd efgh ijkl mnop`).
8. **Step 8**: Copy the code and **remove all spaces** (`abcdefghijklmnop`).
9. **Step 9**: Paste into your **[.env](file:///home/vaibhavsharma/Desktop/Projects/projects/JobMailer/.env)** file:

```env
EMAIL_ADDRESS=sharmavaibhav97631@gmail.com
EMAIL_APP_PASSWORD=abcdefghijklmnop
```

> [!IMPORTANT]
> **Never use your normal Gmail password.** Always use the 16-character App Password.

---

## 🔐 Environment Variables (.env)

Configuration parameters stored in `.env`:

```env
# Sender Email Address
EMAIL_ADDRESS=sharmavaibhav97631@gmail.com

# 16-Character Gmail App Password (No spaces)
EMAIL_APP_PASSWORD=abcdefghijklmnop

# SMTP Server Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Resume Attachment Path
RESUME_PATH=resume/Vaibhav_Sharma_Resume.pdf
```

---

## 📩 Recipient Email Management (emails.txt)

Add target HR email addresses to **`emails.txt`**, one per line:

```txt
hr@google.com
careers@microsoft.com
talent@amazon.com
recruitment@tcs.com
jobs@infosys.com
```

- **Blank lines**: Automatically ignored.
- **Comments**: Lines starting with `#` are skipped.
- **Whitespace**: Automatically trimmed.
- **Deduplication**: Duplicate entries within the file or sent today are skipped automatically.

---

## 📄 Resume Attachment Management

1. Place your resume PDF in the `resume/` directory.
2. Ensure filename matches `RESUME_PATH` in `.env` (default: `resume/Vaibhav_Sharma_Resume.pdf`).
3. The system verifies PDF existence **before** initiating SMTP connections.

---

## 🚀 Running the Project

### Mode 1: Daily Scheduler (Default)
Runs continuous daily schedule at **09:00 AM, 10:00 AM, 01:00 PM, and 02:00 PM**:

```bash
python main.py
```

### Mode 2: Immediate Dispatch Mode
Triggers immediate execution batch right now:

```bash
python main.py --now
```

### Mode 3: Validation Mode
Validates `.env` settings, syntax of `emails.txt`, and resume presence without sending emails:

```bash
python main.py --validate
```

---

## ⏰ Scheduler Timings

The daily schedule is managed by `APScheduler`:

- **09:00 AM** (Morning initial outreach batch)
- **10:00 AM** (Mid-morning follow-up batch)
- **01:00 PM** (Post-lunch afternoon batch)
- **02:00 PM** (Mid-afternoon final batch)

To stop the scheduler, press **`Ctrl + C`** in your terminal.

---

## 📊 Logging & Audit System

Log outputs generated during execution:

```
JobMailer/
├── logs/
│   ├── email_log.csv      # Structured CSV audit log
│   └── email_log.txt      # Plain-text chronological log
├── success_emails.txt     # List of delivered emails
└── failed_emails.txt      # List of failed email addresses
```

### CSV Fields (`logs/email_log.csv`)
`Date`, `Time`, `Recipient`, `Status`, `Error`, `SMTP_Response`

---

## 📈 Progress Bar Metrics (`tqdm`)

During execution, `tqdm` displays:

```
Sending Emails:  45%|███████████████           | 45/101 [18:45<22:15, 23.8s/email]
Postfix: Current: hr@google.com | Sent: 42 | Failed: 1 | Rem: 56
```

- **`45/101`**: Processed / Total pending recipients.
- **`Sent / Failed / Rem`**: Real-time counter status.
- **`Rate Limiting Delay`**: Displays active random sleep countdown between dispatches.

---

## 🔄 Retry Engine & Backoff

For transient network drops or socket timeouts:
- **Attempt 1**: Fails $\rightarrow$ Wait 2.0 seconds.
- **Attempt 2**: Fails $\rightarrow$ Wait 4.0 seconds (Exponential Backoff).
- **Attempt 3**: Fails $\rightarrow$ Mark as `FAILED`, log error, append to `failed_emails.txt`.

> [!NOTE]
> Credential failures (`SMTPAuthenticationError`) fast-fail without retrying to protect your account.

---

## 🛡️ Duplicate Protection

- Checks `success_emails.txt` and `logs/email_log.csv` for emails sent on today's date.
- Automatically skips recipients who have already received an email today.

---

## 🚨 Error Handling Matrix

| Error Condition | Handled Exception | System Behavior |
| :--- | :--- | :--- |
| **Invalid App Password** | `smtplib.SMTPAuthenticationError` | Aborts retry, logs `AUTH_FAILURE`, skips to next recipient. |
| **Network Timeout** | `socket.timeout`, `OSError` | Retries up to 3 times with exponential backoff. |
| **Missing Resume PDF** | `FileNotFoundError` | Halts batch prior to SMTP connection. |
| **Missing `.env` File** | `ValueError` | Displays validation error and exits cleanly. |
| **User Abort** | `KeyboardInterrupt` | Catches `Ctrl+C`, stops scheduler, exits without log corruption. |

---

## ❓ Troubleshooting Guide

### 1. `SMTPAuthenticationError: (534, b'5.7.9 Application-specific password required')`
- **Cause**: Standard password used instead of App Password.
- **Solution**: Enable 2-Step Verification and generate a 16-character App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

### 2. `ModuleNotFoundError: No module named 'tqdm'`
- **Cause**: Virtual environment not activated.
- **Solution**: Run `source venv/bin/activate` and `pip install -r requirements.txt`.

### 3. `FileNotFoundError: Resume file missing`
- **Cause**: Resume PDF not present in `resume/` folder.
- **Solution**: Place your resume PDF at `resume/Vaibhav_Sharma_Resume.pdf`.

---

## 💬 Frequently Asked Questions (FAQ)

#### Q1: Is this automation system completely free?
**Yes.** It relies entirely on Python standard libraries and free Gmail SMTP services.

#### Q2: What is the maximum daily sending limit?
Gmail limits free `@gmail.com` accounts to **500 emails per 24 hours**. We recommend keeping daily batches under 400.

#### Q3: Why is there a 25 to 60-second delay between emails?
Randomized delays prevent Gmail anti-spam algorithms from flagging your account as a bot.

#### Q4: Can I run this on a remote server?
**Yes.** You can use `nohup` or `tmux` on a Linux server:
```bash
nohup python main.py > automation.log 2>&1 &
```

---

## 🔒 Security Best Practices

- **Git Secret Safety**: Never commit `.env` or log files to public repositories (`.gitignore` enforces this).
- **App Password Isolation**: Revoke App Passwords anytime from your Google Account settings without altering your primary password.

---

## 🔮 Future Enhancement Roadmap

- [ ] **Docker Containerization**: `Dockerfile` and `docker-compose.yml` support.
- [ ] **HTML Email Templates**: Support for rich HTML email layouts.
- [ ] **Web Dashboard**: FastAPI / Flask monitoring interface.
- [ ] **Database Persistence**: SQLite / PostgreSQL integration.
- [ ] **Prometheus Metrics**: Export sending metrics for monitoring.

---

## 📜 License & Author

### Author
**Vaibhav Sharma**  
*Python Backend Developer*  
- 📞 **Phone**: +91-7533813494  
- 📧 **Email**: [sharmavaibhav97631@gmail.com](mailto:sharmavaibhav97631@gmail.com)  
- 💼 **LinkedIn**: [vaibhav-sharma-a3027335a](https://www.linkedin.com/in/vaibhav-sharma-a3027335a/)  

### License
Distributed under the **MIT License**.