"""Utility functions for Email Automation System.

Contains company name extraction from email domain, salutation generation,
tracking file persistence, and rate limiting delay helpers.
"""

import random
import re
from pathlib import Path
from typing import Optional

# Generic / Webmail domains that should NOT be used for company name personalization
GENERIC_DOMAINS = {
    "gmail.com",
    "googlemail.com",
    "yahoo.com",
    "yahoo.co.in",
    "yahoo.co.uk",
    "hotmail.com",
    "outlook.com",
    "live.com",
    "msn.com",
    "icloud.com",
    "me.com",
    "mac.com",
    "proton.me",
    "protonmail.com",
    "aol.com",
    "zoho.com",
    "gmx.com",
    "gmx.net",
    "rediffmail.com",
    "yandex.com",
    "mail.com",
    "fastmail.com",
}


def extract_company_name(email: str) -> Optional[str]:
    """Extract and format company name from recipient email domain.

    Example:
        hr@microsoft.com -> "Microsoft"
        careers@tech-solutions.co.in -> "Tech Solutions"
        jobs@tata.com -> "Tata"
        hr@gmail.com -> None

    Args:
        email: Recipient email address.

    Returns:
        Cleaned, Title-Cased company name, or None if domain is generic webmail.
    """
    if "@" not in email:
        return None

    domain = email.split("@")[-1].strip().lower()

    if domain in GENERIC_DOMAINS:
        return None

    # Remove common top-level domain extensions (.com, .co.in, .org, .net, .io, etc.)
    # Strip subdomains if present (e.g. hr.company.com -> company)
    parts = domain.split(".")
    
    # Filter out TLD parts like 'com', 'co', 'in', 'org', 'net', 'io', 'ai', 'tech'
    common_tlds = {"com", "co", "in", "org", "net", "io", "ai", "tech", "uk", "us", "ca", "au", "biz", "info"}
    filtered_parts = [p for p in parts if p not in common_tlds]

    if not filtered_parts:
        raw_name = parts[0]
    else:
        raw_name = filtered_parts[-1]

    # Convert hyphen or underscore separated strings to spaces
    words = re.split(r"[-_]+", raw_name)
    cleaned_words = [word.capitalize() for word in words if word and not word.isdigit()]

    if not cleaned_words:
        return None

    return " ".join(cleaned_words)


def generate_salutation(email: str) -> str:
    """Generate personalized email salutation.

    Args:
        email: Recipient email address.

    Returns:
        Salutation string, e.g., "Dear Microsoft Hiring Team," or "Dear Hiring Team,".
    """
    company_name = extract_company_name(email)
    if company_name:
        return f"Dear {company_name} Hiring Team,"
    return "Dear Hiring Team,"


def append_email_to_file(file_path: Path, email: str) -> None:
    """Safely append an email address to a text file.

    Args:
        file_path: Target file path (e.g. success_emails.txt, failed_emails.txt).
        email: Recipient email address.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode="a", encoding="utf-8") as f:
        f.write(f"{email.strip()}\n")


def get_random_rate_limit_delay(min_seconds: int = 25, max_seconds: int = 60) -> float:
    """Generate a random delay float in seconds between min_seconds and max_seconds.

    Args:
        min_seconds: Minimum delay in seconds (default: 25).
        max_seconds: Maximum delay in seconds (default: 60).

    Returns:
        Random floating point duration in seconds.
    """
    return random.uniform(min_seconds, max_seconds)
