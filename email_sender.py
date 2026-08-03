"""Email sender module for Email Automation System.

Constructs MIME emails with custom attachments and personalized body text,
establishes Gmail SMTP connections with TLS, and implements retry logic
with exponential backoff.
"""

import smtplib
import socket
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Tuple

from config import Config, config
from logger import logger
from utils import generate_salutation


def build_email_message(
    sender_email: str,
    recipient_email: str,
    subject: str,
    salutation: str,
    resume_path: Path
) -> MIMEMultipart:
    """Construct multipart MIME email message with body and resume PDF attachment.

    Args:
        sender_email: Sender's Gmail address.
        recipient_email: Target HR recipient email address.
        subject: Email subject line.
        salutation: Personalized salutation string.
        resume_path: Path to resume PDF file to attach.

    Returns:
        Configured MIMEMultipart object ready for dispatch.
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    body_text = f"""{salutation}

I hope you are doing well.

I am writing to express my interest in opportunities for the role of Python Backend Developer, Python Django Developer, Django Developer, Backend Software Engineer, or Software Engineer within your organization.

I have 2+ years of professional experience in backend development, specializing in Python, Django, Django REST Framework (DRF), REST API Development, PostgreSQL, MongoDB, Redis, Celery, WebSockets, and AI-powered chatbot solutions. I have worked on enterprise-grade applications, including Restaurant ERP & Inventory Management Systems, Ride-Hailing Platforms, and AI-powered Chatbot platforms.

My experience includes designing scalable backend systems, developing secure REST APIs, implementing Role-Based Access Control (RBAC), integrating Razorpay Payment Gateway, optimizing PostgreSQL databases, and building asynchronous processing workflows using Redis and Celery. I have also worked on AI-powered chatbot solutions using spaCy NLP and Retrieval-Augmented Generation (RAG), implementing WebSocket-based real-time communication, developing chatbot APIs, and building scalable backend architectures for intelligent conversational applications.

Profile Summary:

Experience: 2+ Years

Primary Skills:
Python, Django, Django REST Framework (DRF), Flask, FastAPI, REST APIs, PostgreSQL, MongoDB, MySQL, Redis, Celery, WebSockets, Django Channels, RBAC, Razorpay Integration, AI Chatbots, spaCy NLP, Retrieval-Augmented Generation (RAG), Swagger/OpenAPI, Git, Docker, Linux, Jenkins, AWS Fundamentals

Current CTC:
₹3.0 LPA

Expected CTC:
₹4.0 LPA

Notice Period:
Immediate Joiner

Current Location:
Gurugram, Haryana

Open to:
On-site, Hybrid, Remote, and Relocation

My resume is attached for your kind review. I would sincerely appreciate it if you could consider my profile for any relevant current or upcoming opportunities. If my experience aligns with your requirements, I would be happy to discuss my profile further.

Thank you for your time and consideration.

Kind Regards,

Vaibhav Sharma
Python Backend Developer
📞 +91-7533813494
📧 sharmavaibhav97631@gmail.com

LinkedIn:
https://www.linkedin.com/in/vaibhav-sharma-a3027335a/

Resume:
https://docs.google.com/document/d/1AbV3t0liEU3z5MTm8AGv04_mzbTeMx10PwxayqhHd84/edit?usp=sharing
"""

    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    # Attach Resume PDF if present
    if resume_path.exists() and resume_path.is_file():
        try:
            with open(resume_path, "rb") as pdf_file:
                part = MIMEApplication(pdf_file.read(), Name=resume_path.name)
                part["Content-Disposition"] = f'attachment; filename="{resume_path.name}"'
                msg.attach(part)
        except Exception as e:
            logger.error(f"Failed attaching resume PDF '{resume_path}': {e}")
            raise FileNotFoundError(f"Failed reading resume attachment: {e}")
    else:
        logger.warning(f"Resume PDF file not found at: {resume_path}")

    return msg


def send_email_with_retry(
    recipient: str,
    cfg: Config = config,
    max_retries: int = 3,
    initial_delay: float = 2.0
) -> Tuple[bool, str, str, int]:
    """Send job application email to recipient with automatic retry and exponential backoff.

    Args:
        recipient: Target recipient email address.
        cfg: Config instance.
        max_retries: Maximum attempt count (default: 3).
        initial_delay: Initial retry wait duration in seconds (default: 2.0).

    Returns:
        Tuple of (success_boolean, smtp_response_str, error_msg_str, attempt_count).
    """
    subject = "Application for Python Backend Developer | Immediate Joiner | Vaibhav Sharma"
    salutation = generate_salutation(recipient)
    resume_path = cfg.absolute_resume_path

    if not resume_path.exists():
        error_msg = f"Resume file missing at '{resume_path}'. Email sending aborted."
        logger.error(error_msg)
        return False, "NO_RESUME", error_msg, 0

    attempt = 0
    delay = initial_delay

    while attempt < max_retries:
        attempt += 1
        server = None
        try:
            logger.info(f"Attempt {attempt}/{max_retries}: Connecting to SMTP {cfg.smtp_server}:{cfg.smtp_port} for {recipient}")

            # Connect to SMTP server
            if cfg.smtp_port == 465:
                server = smtplib.SMTP_SSL(cfg.smtp_server, cfg.smtp_port, timeout=30)
            else:
                server = smtplib.SMTP(cfg.smtp_server, cfg.smtp_port, timeout=30)
                server.ehlo()
                server.starttls()
                server.ehlo()

            # Authenticate
            server.login(cfg.email_address, cfg.email_app_password)

            # Build message
            msg = build_email_message(cfg.email_address, recipient, subject, salutation, resume_path)

            # Send Email
            response_dict = server.send_message(msg)
            server.quit()

            smtp_code = "250 OK"
            logger.info(f"Email successfully delivered to {recipient}")
            return True, smtp_code, "None", attempt

        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"SMTP Authentication Failed: Check EMAIL_ADDRESS and EMAIL_APP_PASSWORD in .env ({e})"
            logger.error(error_msg)
            if server:
                try:
                    server.quit()
                except Exception:
                    pass
            # Permanent credential error - do not retry
            return False, "AUTH_FAILURE", error_msg, attempt

        except (smtplib.SMTPException, socket.timeout, socket.error, OSError) as e:
            error_msg = f"SMTP Transmission Error on attempt {attempt}/{max_retries}: {e}"
            logger.warning(error_msg)
            if server:
                try:
                    server.quit()
                except Exception:
                    pass

            if attempt < max_retries:
                logger.info(f"Retrying in {delay:.1f} seconds (exponential backoff)...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                return False, "TRANSMISSION_ERROR", error_msg, attempt

        except Exception as e:
            error_msg = f"Unexpected Exception sending to {recipient}: {e}"
            logger.error(error_msg)
            if server:
                try:
                    server.quit()
                except Exception:
                    pass

            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
            else:
                return False, "UNEXPECTED_ERROR", error_msg, attempt

    return False, "MAX_RETRIES_EXCEEDED", "All retry attempts failed", max_retries
