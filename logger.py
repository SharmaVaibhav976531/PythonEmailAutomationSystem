"""Logging module for Email Automation System.

Provides console logging, plain-text log files, and structured CSV logging
for email dispatch attempts, status, errors, and SMTP responses.
"""

import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from config import config

# Configure Standard Python Logging
logger = logging.getLogger("JobMailer")
logger.setLevel(logging.INFO)

# Formatter
log_formatter = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# File Handler (logs/email_log.txt)
file_handler = logging.FileHandler(config.log_txt, encoding="utf-8")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# Add Handlers if not already present
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def init_csv_log(csv_path: Path) -> None:
    """Initialize CSV log file with header if it does not exist."""
    if not csv_path.exists():
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "Recipient", "Status", "Error", "SMTP_Response"])


def log_email_event(
    recipient: str,
    status: str,
    error: Optional[str] = None,
    smtp_response: Optional[str] = None,
    log_time: Optional[datetime] = None
) -> None:
    """Record email dispatch event into console, txt log, and structured CSV log.

    Args:
        recipient: Target email address.
        status: Dispatch outcome (SUCCESS, FAILED, SKIPPED, RETRY).
        error: Description of error if failed, otherwise None.
        smtp_response: Raw response string from SMTP server, if available.
        log_time: Optional override timestamp (defaults to current time).
    """
    now = log_time or datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    clean_error = str(error).replace("\n", " ") if error else "None"
    clean_smtp = str(smtp_response).replace("\n", " ") if smtp_response else "None"

    # Log to logger
    log_msg = f"Recipient: {recipient} | Status: {status} | Error: {clean_error} | SMTP: {clean_smtp}"
    if status == "SUCCESS":
        logger.info(log_msg)
    elif status in ("FAILED", "ERROR"):
        logger.error(log_msg)
    else:
        logger.warning(log_msg)

    # Write to CSV log
    init_csv_log(config.log_csv)
    try:
        with open(config.log_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([date_str, time_str, recipient, status, clean_error, clean_smtp])
    except Exception as e:
        logger.error(f"Failed writing to CSV log: {e}")

    # Synchronize with root email_log.txt if requested
    try:
        root_txt_log = config.base_dir / "email_log.txt"
        with open(root_txt_log, mode="a", encoding="utf-8") as f:
            f.write(f"[{date_str} {time_str}] {log_msg}\n")
    except Exception as e:
        logger.error(f"Failed writing to root log: {e}")
