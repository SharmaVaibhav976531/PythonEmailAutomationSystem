# ✉️ Production-Grade Python Email Automation System

A robust, enterprise-ready Python Email Automation System built specifically for high-volume job application dispatches via **Gmail SMTP**. It features automated **APScheduler** daily execution, **RFC 5322** email syntax validation, **smart rate limiting**, **dynamic company name extraction**, **multi-attempt retry logic with exponential backoff**, **dual structured CSV & text logging**, and **anti-duplicate history tracking**.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack & Dependencies](#-tech-stack--dependencies)
- [Folder Structure & Codebase Map](#-folder-structure--codebase-map)
- [Architecture & System Workflows](#-architecture--system-workflows)
- [Installation Guide](#-installation-guide)
- [Python Version Requirements](#-python-version-requirements)
- [Virtual Environment Management](#-virtual-environment-management)
- [Installing Dependencies](#-installing-dependencies)
- [Gmail Configuration & App Password Setup](#-gmail-configuration--app-password-setup)
- [Environment Variables (.env)](#-environment-variables-env)
- [Recipient Email Management (emails.txt)](#-recipient-email-management-emailstxt)
- [Resume Attachment Management](#-resume-attachment-management)
- [Running the Project](#-running-the-project)
- [APScheduler Engine & Daily Timings](#-apscheduler-engine--daily-timings)
- [Logging & Audit System](#-logging--audit-system)
- [Retry Engine & Exponential Backoff](#-retry-engine--exponential-backoff)
- [Duplicate Protection & Anti-Spam Safeguards](#-duplicate-protection--anti-spam-safeguards)
- [Email Validation & Syntax Verification](#-email-validation--syntax-verification)
- [Live Progress Bar (tqdm)](#-live-progress-bar-tqdm)
- [Comprehensive Error Handling Matrix](#-comprehensive-error-handling-matrix)
- [Troubleshooting Guide](#-troubleshooting-guide)
- [Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [Security & Credential Safety](#-security--credential-safety)
- [Production Best Practices](#-production-best-practices)
- [Future Enhancement Roadmap](#-future-enhancement-roadmap)
- [License, Author & Contact Info](#-license-author--contact-info)

---

## 🎯 Project Overview

### Why This Project Exists
Applying to 100+ hiring managers and HR representatives manually is exhausting, prone to copy-paste errors, lacks consistent follow-up timing, and risks Gmail spam flags if sent too rapidly. 

This project automates job application email dispatches from your local machine while adhering strictly to production engineering practices, rate-limiting safety guidelines, and error recovery protocols.

### What Problem It Solves
1. **Eliminates Manual Repetitive Tasks**: Sends personalized cover emails and attaches resume PDFs automatically.
2. **Prevents Spam Penalties**: Introduces randomized delays (25s to 60s) between dispatches to comply with Gmail anti-spam algorithms.
3. **Prevents Duplicate Emails**: Tracks sent emails in daily history logs so no recruiter is spammed twice on the same day.
4. **Ensures Automated Schedule**: Runs daily at optimal hiring hours (**09:00 AM, 10:00 AM, 01:00 PM, and 02:00 PM**) without manual intervention.
5. **Personalizes Applications at Scale**: Extracts company names from recruiter email domains (e.g. `hr@google.com` $\rightarrow$ `Dear Google Hiring Team,`).

### Main Objective
To provide a zero-cost, local, scalable Python solution for developers to send high-volume, personalized job application emails reliably with real-time feedback and audit trails.

---

## ✨ Features

- **⏱️ Automated Daily Scheduling**: Integrated `APScheduler` cron engine that runs daily at **09:00 AM**, **10:00 AM**, **01:00 PM**, and **02:00 PM**.
- **🔒 Gmail TLS SMTP Authentication**: Connects over secure TLS (port 587) using Google 16-character App Passwords.
- **🏷️ Smart Company Name Personalization**: Parses corporate domain names (e.g., `careers@microsoft.com` $\rightarrow$ `Dear Microsoft Hiring Team,`), while falling back gracefully for webmail services like Gmail/Yahoo (`Dear Hiring Team,`).
- **🛡️ RFC 5322 Syntax Validation**: Validates email formats, strips surrounding whitespace, skips blank lines, and ignores syntax-invalid entries.
- **🔄 Multi-Attempt Retry with Exponential Backoff**: Automatically retries transient network or SMTP glitches up to 3 times ($2\text{s} \rightarrow 4\text{s} \rightarrow 8\text{s}$ backoff) while fast-failing on credential errors.
- **⏳ Dynamic Rate Limiting**: Introduces a randomized sleep duration (between 25 and 60 seconds) between consecutive dispatches.
- **📊 Real-Time Progress Bar (`tqdm`)**: Visual terminal progress bar displaying current recipient, sent count, failure count, remaining count, and live delay counters.
- **📝 Dual Audit Logging**:
  - `logs/email_log.csv`: Structured CSV recording `Date`, `Time`, `Recipient`, `Status`, `Error`, and `SMTP_Response`.
  - `logs/email_log.txt` & `email_log.txt`: Plain-text chronological log output.
- **📁 Persistence Tracking Files**:
  - `success_emails.txt`: Appends successfully delivered recipient addresses.
  - `failed_emails.txt`: Appends failed addresses for later inspection.
- **📑 Automatic PDF Attachment**: Encodes and attaches your resume PDF via MIME `application/pdf`.
- **📊 Execution Summary Report**: Generates an end-of-batch statistics summary detailing processed, sent, failed, skipped, invalid, duplicate counts, and execution duration.
- **⚡ Command-Line Operations**: Supports execution modes: `--schedule` (default cron loop), `--now` (immediate single run), and `--validate` (syntax and credential check).

---

## 🛠️ Tech Stack & Dependencies

### Programming Language
- **Python**: 3.10 or higher

### Standard Python Libraries (No External Installation Required)
- `smtplib`: Low-level SMTP client interface for email transmission over TLS.
- `email.mime`: MIME multipart structure builder (`MIMEMultipart`, `MIMEText`, `MIMEApplication`).
- `csv`: Structured CSV reader and writer for execution logs.
- `logging`: Built-in logging framework for text log generation.
- `argparse`: Command-line argument parser (`--now`, `--schedule`, `--validate`).
- `re`: Regular expression engine for RFC 5322 email syntax validation and domain parsing.
- `random`: Uniform pseudo-random number generator for rate-limiting delays.
- `time`: System clock and sleep interface.
- `datetime`: Timestamp generation and elapsed time formatting.
- `pathlib`: Cross-platform object-oriented filesystem path manipulation.
- `dataclasses`: Clean configuration object modeling.
- `socket`: TCP/IP network connection error handling.
- `sys`: Process exit signals and execution termination.

### Third-Party Libraries (`requirements.txt`)
- `APScheduler` (`==3.11.3`): Advanced Python task scheduler for cron job execution.
- `python-dotenv` (`==1.2.2`): Loads `.env` environment variables into `os.environ`.
- `tqdm` (`==4.70.0`): Console progress bar library.
- `tzlocal` (`==5.4.4`): Cross-platform local timezone lookup helper for APScheduler.

---

## 📁 Folder Structure & Codebase Map

```
JobMailer/
│
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

### How Modules Communicate With Each Other

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

1. **`main.py`** parses arguments and either starts **`scheduler.py`** or invokes `execute_email_batch()`.
2. **`config.py`** loads `.env` variables and validates credentials and resume paths.
3. **`email_validator.py`** loads `emails.txt`, removes blank lines, verifies RFC 5322 syntax, and filters out recipients emailed today.
4. **`utils.py`** extracts company names from email domains and generates custom salutations (`Dear Google Hiring Team,`).
5. **`email_sender.py`** builds the MIME message, attaches `resume/Vaibhav_Sharma_Resume.pdf`, and dispatches via Gmail SMTP with retries.
6. **`logger.py`** records every dispatch attempt to `logs/email_log.csv`, `logs/email_log.txt`, `success_emails.txt`, and `failed_emails.txt`.

---

## 🏗️ Architecture & System Workflows

### End-to-End Execution Sequence Diagram

```
User -> main.py: Runs python main.py
main.py -> config.py: validate() credentials & paths
config.py --> main.py: Config Verified
main.py -> email_validator.py: load_and_clean_emails(emails.txt)
email_validator.py --> main.py: Return Valid Recipient List
main.py -> email_validator.py: get_sent_emails_today()
email_validator.py --> main.py: Return Today's Sent Set
main.py -> utils.py: generate_salutation(recipient)
utils.py --> main.py: "Dear Google Hiring Team,"
main.py -> email_sender.py: send_email_with_retry(recipient)
email_sender.py -> SMTP Server: Connect TLS (port 587) & Authenticate
SMTP Server --> email_sender.py: 250 OK Response
email_sender.py --> main.py: (True, "250 OK", "None", attempt)
main.py -> logger.py: log_email_event(SUCCESS)
main.py -> utils.py: append_email_to_file(success_emails.txt)
main.py -> main.py: Sleep random delay (25s - 60s)
main.py -> Terminal: Output Execution Summary Report
```

---

## 📥 Installation Guide

### Linux Setup (Ubuntu / Debian / Mint)

```bash
# Update package list and install Python 3.10+ & venv
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# Clone or navigate to the project directory
cd ~/Desktop/Projects/projects/JobMailer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### macOS Setup

```bash
# Open Terminal and navigate to directory
cd ~/Desktop/Projects/projects/JobMailer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Windows Setup (Command Prompt / PowerShell)

```cmd
:: Navigate to project folder
cd C:\Users\YourUsername\Projects\JobMailer

:: Create virtual environment
python -m venv venv

:: Activate virtual environment (Command Prompt)
venv\Scripts\activate.bat

:: Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

:: Install dependencies
pip install -r requirements.txt
```

---

## 🐍 Python Version Requirements

This project requires **Python 3.10** or higher.

### Check Installed Python Version
```bash
python3 --version
# Output should be: Python 3.10.x or Python 3.11.x or Python 3.12.x
```

### Installing Python if Missing
- **Linux (Ubuntu/Debian)**: `sudo apt install python3 python3-pip`
- **macOS**: `brew install python`
- **Windows**: Download installer from [python.org](https://www.python.org/downloads/) (Check **"Add Python to PATH"** during installation).

---

## 📦 Virtual Environment Management

Using a virtual environment isolates project dependencies from your system Python installation, preventing package version conflicts.

| Task | Command (Linux / macOS) | Command (Windows) |
| :--- | :--- | :--- |
| **Create venv** | `python3 -m venv venv` | `python -m venv venv` |
| **Activate venv** | `source venv/bin/activate` | `venv\Scripts\activate.bat` |
| **Deactivate venv** | `deactivate` | `deactivate` |

---

## 📑 Installing Dependencies

Install frozen production requirements using `pip`:

```bash
pip install -r requirements.txt
```

### Contents of `requirements.txt`:
```txt
APScheduler==3.11.3
python-dotenv==1.2.2
tqdm==4.70.0
tzlocal==5.4.4
```

---

## 🔐 Gmail Configuration & App Password Setup

> ⚠️ **CRITICAL SECURITY REQUIREMENT**: Standard Gmail account passwords **CANNOT** be used for SMTP authentication. Google blocks direct password logins and throws `534 5.7.9 Application-specific password required`. You MUST generate a 16-character **App Password**.

### Step-by-Step App Password Generation Guide

1. **Step 1**: Open your web browser and log into **[Google Account](https://myaccount.google.com/)**.
2. **Step 2**: Click on **Security** in the left navigation menu.
3. **Step 3**: Scroll down to *How you sign in to Google* and ensure **2-Step Verification** is turned **ON**.
4. **Step 4**: Open **[Google App Passwords](https://myaccount.google.com/apppasswords)** directly.
5. **Step 5**: In the **App Name** text field, type `JobMailer` or `Python Email Automation`.
6. **Step 6**: Click the **Create** button.
7. **Step 7**: Google will generate a yellow modal box containing a **16-character passcode** (e.g., `abcd efgh ijkl mnop`).
8. **Step 8**: Copy the passcode and **remove all spaces** (`abcdefghijklmnop`).
9. **Step 9**: Paste the passcode into your **[.env](file:///home/vaibhavsharma/Desktop/Projects/projects/JobMailer/.env)** file:
   ```env
   EMAIL_ADDRESS=sharmavaibhav97631@gmail.com
   EMAIL_APP_PASSWORD=abcdefghijklmnop
   ```

### Why Gmail App Passwords Are Required
In May 2022, Google turned off support for "Less Secure Apps" (direct password authentication over SMTP) to protect user accounts from credential stuffing attacks. App Passwords generate a unique, revokable token exclusively for programmatic SMTP access.

---

## ⚙️ Environment Variables (.env)

Configuration settings are loaded dynamically using `python-dotenv` from the root `.env` file.

```env
# Sender Email Address
EMAIL_ADDRESS=sharmavaibhav97631@gmail.com

# 16-Character Gmail App Password (No spaces)
EMAIL_APP_PASSWORD=abcdefghijklmnop

# SMTP Server Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Resume PDF Path
RESUME_PATH=resume/Vaibhav_Sharma_Resume.pdf
```

### Environment Variables Glossary

| Variable | Description | Default | Required? |
| :--- | :--- | :--- | :--- |
| `EMAIL_ADDRESS` | Your full Gmail address | `sharmavaibhav97631@gmail.com` | **Yes** |
| `EMAIL_APP_PASSWORD` | 16-character Google App Password | None | **Yes** |
| `SMTP_SERVER` | Gmail SMTP server hostname | `smtp.gmail.com` | **Yes** |
| `SMTP_PORT` | SMTP port (587 for TLS, 465 for SSL) | `587` | **Yes** |
| `RESUME_PATH` | Relative or absolute path to resume PDF | `resume/Vaibhav_Sharma_Resume.pdf` | **Yes** |

---

## 📩 Recipient Email Management (emails.txt)

Place all recipient HR email addresses in **`emails.txt`**, one email per line:

```txt
# Target HR Recipients List
hr@google.com
careers@microsoft.com
talent@amazon.com
recruitment@tcs.com
jobs@infosys.com
```

### Automated Rules Handled by `email_validator.py`:
- **Trims Whitespace**: Removes leading/trailing spaces and tabs.
- **Ignores Blank Lines**: Empty lines are skipped without throwing errors.
- **Ignores Comments**: Lines starting with `#` are ignored.
- **Validates Syntax**: Non-RFC 5322 compliant emails are logged as `INVALID` and skipped.
- **In-File Deduplication**: If an email appears multiple times in `emails.txt`, only the first instance is kept.

---

## 📄 Resume Attachment Management

1. Place your latest PDF resume inside the `resume/` directory.
2. Name the file `Vaibhav_Sharma_Resume.pdf` (or update `RESUME_PATH` in `.env`).
3. The system verifies that the resume file exists **BEFORE** connecting to the SMTP server. If missing, execution halts safely with a clear warning.

---

## 🚀 Running the Project

### 1. Daily Scheduler Mode (Default Production Mode)
Runs the continuous background scheduler that dispatches emails daily at **09:00 AM**, **10:00 AM**, **01:00 PM**, and **02:00 PM**:

```bash
python main.py
```
*Or explicitly:*
```bash
python main.py --schedule
```

### 2. Immediate Batch Mode (Test / Manual Run)
Dispatches the email batch immediately right now without waiting for the scheduled times:

```bash
python main.py --now
```

### 3. System Setup Validation Mode
Verifies `.env` settings, syntax of `emails.txt`, and resume PDF presence without sending any emails:

```bash
python main.py --validate
```

---

## ⏰ APScheduler Engine & Daily Timings

The system utilizes `APScheduler`'s `BlockingScheduler` with `CronTrigger` rules:

```python
scheduled_times = [
    ("09:00 AM", 9, 0),
    ("10:00 AM", 10, 0),
    ("01:00 PM", 13, 0),
    ("02:00 PM", 14, 0),
]
```

- **Execution Hours**: 9:00 AM, 10:00 AM, 1:00 PM (13:00), 2:00 PM (14:00).
- **Graceful Termination**: Press `Ctrl + C` in the terminal to stop the scheduler loop cleanly.

---

## 📊 Logging & Audit System

Every email dispatch event is logged across four outputs:

```
JobMailer/
├── logs/
│   ├── email_log.csv      # Structured CSV output
│   └── email_log.txt      # Text log output
├── email_log.txt          # Root log synchronization
├── success_emails.txt     # List of delivered emails
└── failed_emails.txt      # List of failed email attempts
```

### CSV Log File Format (`logs/email_log.csv`)
| Date | Time | Recipient | Status | Error | SMTP_Response |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-08-03` | `09:00:15` | `hr@google.com` | `SUCCESS` | `None` | `250 OK` |
| `2026-08-03` | `09:01:05` | `careers@bad-domain.xyz` | `FAILED` | `SMTP Transmission Error` | `TRANSMISSION_ERROR` |

---

## 🔄 Retry Engine & Exponential Backoff

When a network drop or temporary SMTP timeout occurs:
1. Attempt 1 fails $\rightarrow$ System logs warning and sleeps **2.0 seconds**.
2. Attempt 2 fails $\rightarrow$ System logs warning and sleeps **4.0 seconds**.
3. Attempt 3 fails $\rightarrow$ System logs failure, records recipient in `failed_emails.txt`, and moves to the next email.

> 💡 **Smart Credential Check**: If an authentication error (`SMTPAuthenticationError`) occurs, retries are immediately aborted to avoid locking your Gmail account.

---

## 🛡️ Duplicate Protection & Anti-Spam Safeguards

To prevent spamming hiring managers:
- Before sending, `email_validator.py` checks `success_emails.txt` and `logs/email_log.csv` for emails sent on the current date.
- Any email already sent today is automatically skipped.

---

## 🔍 Email Validation & Syntax Verification

`email_validator.py` uses RFC 5322 compliant regular expressions:

$$\text{EMAIL\_REGEX} = \texttt{\^{}[a-zA-Z0-9.!CheckPattern]+@[a-zA-Z0-9.-]+\textbackslash.[a-zA-Z]\{2,\}\$}$$

Validates characters, domain `@` symbols, subdomains, and top-level domain extensions (.com, .in, .org, etc.).

---

## 📈 Live Progress Bar (tqdm)

Terminal progress display format:
```
Sending Emails:  45%|█████████████▋               | 45/101 [18:45<22:15, 23.8s/email]
Postfix Status: Current: hr@google.com | Sent: 42 | Failed: 1 | Rem: 56
```

---

## 🚨 Comprehensive Error Handling Matrix

| Error Condition | Caught Exception | System Behavior |
| :--- | :--- | :--- |
| **Invalid Gmail App Password** | `smtplib.SMTPAuthenticationError` | Aborts retry immediately, logs `AUTH_FAILURE`, continues to next email. |
| **Network / Timeout** | `socket.timeout`, `OSError` | Executes up to 3 retries with exponential backoff. |
| **Missing Resume PDF** | `FileNotFoundError` | Halts batch dispatch safely before connecting to SMTP. |
| **Missing `.env` File** | `ValueError` | Displays configuration validation error and exits. |
| **Keyboard Interrupt** | `KeyboardInterrupt` | Catches `Ctrl+C`, closes progress bar, exits cleanly without corrupting logs. |

---

## ❓ Troubleshooting Guide

### 1. `SMTPAuthenticationError: (534, b'5.7.9 Application-specific password required')`
- **Cause**: Using standard Gmail password instead of App Password.
- **Fix**: Enable 2-Step Verification and generate a 16-character App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

### 2. `ModuleNotFoundError: No module named 'tqdm'` or `'dotenv'`
- **Cause**: Virtual environment not activated or requirements not installed.
- **Fix**: Run `source venv/bin/activate` followed by `pip install -r requirements.txt`.

### 3. `FileNotFoundError: Resume file missing at 'resume/Vaibhav_Sharma_Resume.pdf'`
- **Cause**: PDF resume is missing from the `resume/` directory.
- **Fix**: Copy your resume PDF to `resume/Vaibhav_Sharma_Resume.pdf`.

---

## 💬 Frequently Asked Questions (FAQ)

#### Q1: Is this automation free to use?
**Yes.** It uses standard Python libraries and Gmail's free SMTP server. No paid services or subscriptions are required.

#### Q2: How many emails can I send per day?
Gmail limits free `@gmail.com` accounts to **500 emails per 24-hour period**. We recommend keeping daily batches under **400 emails**.

#### Q3: Why does the system delay 25 to 60 seconds between emails?
Random delays mimic human sending behavior and prevent Gmail's automated spam filters from flagging your account.

#### Q4: Can I run this system in the background on a server?
**Yes.** You can run it on a Linux server using `nohup` or `tmux`:
```bash
nohup python main.py > automation.log 2>&1 &
```

---

## 🔒 Security & Credential Safety

- **Never Commit Credentials**: The `.gitignore` file explicitly excludes `.env`, `logs/`, and tracking files from version control.
- **App Password Isolation**: App Passwords can be revoked at any time from your Google Security page without changing your main account password.

---

## 🚀 Future Enhancement Roadmap

- [ ] **HTML Email Templates**: Support for rich HTML email rendering with inline styling.
- [ ] **Web Dashboard**: Flask / FastAPI dashboard for real-time tracking.
- [ ] **Docker Containerization**: `Dockerfile` and `docker-compose.yml` support for lightweight deployment.
- [ ] **Database Integration**: PostgreSQL / SQLite storage backend for recipient history tracking.

---

## 📜 License & Author

### Author
**Vaibhav Sharma**  
*Python Backend Developer*  
- 📞 **Phone**: +91-7533813494  
- 📧 **Email**: [sharmavaibhav97631@gmail.com](mailto:sharmavaibhav97631@gmail.com)  
- 💼 **LinkedIn**: [vaibhav-sharma-a3027335a](https://www.linkedin.com/in/vaibhav-sharma-a3027335a/)  

### License
This project is licensed under the **MIT License**.
