"""Email validation and filtering module.

Handles RFC 5322 syntax validation, whitespace stripping, blank line removal,
intra-file deduplication, and daily duplicate prevention.
"""

import csv
import re
from datetime import datetime
from pathlib import Path
from typing import List, Set, Tuple
from logger import logger

# Regex pattern for email syntax validation adhering to standard RFC 5322
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)


def is_valid_email(email: str) -> bool:
    """Validate email syntax using regular expression.

    Args:
        email: Email address string to test.

    Returns:
        True if syntax is valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def load_and_clean_emails(file_path: Path) -> Tuple[List[str], int, int]:
    """Read email recipient file, strip whitespace, skip blank lines and invalid emails,
    and deduplicate entries.

    Args:
        file_path: Path to emails.txt file.

    Returns:
        Tuple of (clean_unique_emails_list, invalid_count, duplicate_in_file_count).
    """
    if not file_path.exists():
        logger.warning(f"Emails file not found at: {file_path}")
        return [], 0, 0

    clean_emails: List[str] = []
    seen: Set[str] = set()
    invalid_count = 0
    duplicate_in_file_count = 0

    with open(file_path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        raw_line = line.strip()

        # Skip empty lines or commented lines
        if not raw_line or raw_line.startswith("#"):
            continue

        email = raw_line.lower()

        # Check validity
        if not is_valid_email(email):
            logger.warning(f"Invalid email format skipped: '{raw_line}'")
            invalid_count += 1
            continue

        # Check duplicate within file
        if email in seen:
            duplicate_in_file_count += 1
            continue

        seen.add(email)
        clean_emails.append(email)

    return clean_emails, invalid_count, duplicate_in_file_count


def get_sent_emails_today(success_file_path: Path, csv_log_path: Path) -> Set[str]:
    """Retrieve set of email addresses already sent today to prevent duplicate dispatches.

    Args:
        success_file_path: Path to success_emails.txt.
        csv_log_path: Path to logs/email_log.csv.

    Returns:
        Set of lowercase email addresses sent today.
    """
    sent_emails: Set[str] = set()
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Read from success_emails.txt if available
    if success_file_path.exists():
        try:
            with open(success_file_path, mode="r", encoding="utf-8") as f:
                for line in f:
                    email = line.strip().lower()
                    if email and is_valid_email(email):
                        sent_emails.add(email)
        except Exception as e:
            logger.error(f"Error reading success_emails.txt: {e}")

    # Cross-reference with CSV log for today's SUCCESS records
    if csv_log_path.exists():
        try:
            with open(csv_log_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("Date") == today_str and row.get("Status") == "SUCCESS":
                        recipient = row.get("Recipient", "").strip().lower()
                        if recipient:
                            sent_emails.add(recipient)
        except Exception as e:
            logger.error(f"Error reading CSV log: {e}")

    return sent_emails


def filter_pending_emails(emails: List[str], sent_today: Set[str]) -> Tuple[List[str], int]:
    """Filter list of emails to exclude those sent today.

    Args:
        emails: List of validated email addresses.
        sent_today: Set of email addresses already sent today.

    Returns:
        Tuple of (pending_emails, duplicate_today_count).
    """
    pending = []
    duplicate_today_count = 0

    for email in emails:
        if email.lower() in sent_today:
            duplicate_today_count += 1
            logger.info(f"Skipping duplicate email sent today: {email}")
        else:
            pending.append(email)

    return pending, duplicate_today_count
