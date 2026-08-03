"""Main entry point for Email Automation System.

Orchestrates credential validation, email syntax checking, duplicate filtering,
rate-limited sending, live progress visualization, detailed event logging,
and execution summary reporting.
"""

import argparse
import sys
import time
from datetime import datetime, timedelta
from typing import List

from tqdm import tqdm

from config import config
from email_sender import send_email_with_retry
from email_validator import (
    filter_pending_emails,
    get_sent_emails_today,
    load_and_clean_emails,
)
from logger import log_email_event, logger
from scheduler import EmailScheduler
from utils import append_email_to_file, get_random_rate_limit_delay


def execute_email_batch() -> None:
    """Execute complete email automation batch run."""
    start_time = datetime.now()
    logger.info(f"--- Starting Job Email Automation Run at {start_time.strftime('%Y-%m-%d %H:%M:%S')} ---")

    # Step 1: Validate Configuration & Resume File
    try:
        config.validate()
    except ValueError as val_err:
        logger.error(f"Configuration Error:\n{val_err}")
        print("\n❌ Configuration Error! Please check your .env file credentials.")
        return

    resume_path = config.absolute_resume_path
    if not resume_path.exists():
        logger.error(f"Resume PDF missing at path: '{resume_path}'")
        print(f"\n❌ Resume file missing! Please place your resume PDF at '{resume_path}'.")
        return

    # Step 2: Load Recipient Emails from emails.txt
    raw_emails, invalid_count, duplicate_in_file_count = load_and_clean_emails(config.emails_file)

    if not raw_emails and invalid_count == 0 and duplicate_in_file_count == 0:
        logger.warning(f"No emails found in '{config.emails_file}'. Add HR recipient emails (one per line).")
        print(f"\n⚠️  '{config.emails_file.name}' is empty. Add recipient emails before running.")
        return

    # Step 3: Check Daily Duplicates
    sent_today = get_sent_emails_today(config.success_file, config.log_csv)
    pending_emails, duplicate_today_count = filter_pending_emails(raw_emails, sent_today)

    total_emails = len(raw_emails) + invalid_count + duplicate_in_file_count
    total_skipped = invalid_count + duplicate_in_file_count + duplicate_today_count

    print("\n" + "=" * 60)
    print(" 🚀 PYTHON EMAIL AUTOMATION BATCH INITIALIZED")
    print("=" * 60)
    print(f" • Total Email Records Found : {total_emails}")
    print(f" • Valid & Pending Emails    : {len(pending_emails)}")
    print(f" • Invalid Format Skipped    : {invalid_count}")
    print(f" • File Duplicates Skipped   : {duplicate_in_file_count}")
    print(f" • Already Sent Today        : {duplicate_today_count}")
    print("=" * 60 + "\n")

    if not pending_emails:
        print("✅ No pending emails to send. All valid recipients have already been emailed today.")
        return

    sent_count = 0
    failed_count = 0

    # Step 4: Dispatch Emails with Rate-Limiting & tqdm Progress Bar
    pbar = tqdm(
        total=len(pending_emails),
        desc="Sending Emails",
        unit="email",
        dynamic_ncols=True,
        bar_format="{l_bar}{bar:30}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
    )

    for idx, recipient in enumerate(pending_emails, start=1):
        remaining_count = len(pending_emails) - idx
        pbar.set_postfix_str(f"Current: {recipient} | Sent: {sent_count} | Failed: {failed_count} | Rem: {remaining_count}")

        # Send Email with Retry Logic
        success, smtp_code, error_msg, attempts = send_email_with_retry(recipient, config)

        if success:
            sent_count += 1
            log_email_event(recipient=recipient, status="SUCCESS", smtp_response=smtp_code)
            append_email_to_file(config.success_file, recipient)
        else:
            failed_count += 1
            log_email_event(recipient=recipient, status="FAILED", error=error_msg, smtp_response=smtp_code)
            append_email_to_file(config.failed_file, recipient)

        pbar.update(1)

        # Rate Limiting: Delay between 25 and 60 seconds (skip delay after final email)
        if idx < len(pending_emails):
            delay_sec = get_random_rate_limit_delay(25, 60)
            pbar.set_postfix_str(f"Rate Limiting Delay: {delay_sec:.1f}s | Next: {pending_emails[idx]}")
            time.sleep(delay_sec)

    pbar.close()

    # Step 5: Final Execution Summary Report
    end_time = datetime.now()
    execution_duration = end_time - start_time
    minutes, seconds = divmod(int(execution_duration.total_seconds()), 60)

    print("\n" + "=" * 60)
    print(" 📊 AUTOMATION EXECUTION SUMMARY REPORT")
    print("=" * 60)
    print(f" Total Emails Processed : {total_emails}")
    print(f" Successfully Sent      : {sent_count}")
    print(f" Failed Dispatches      : {failed_count}")
    print(f" Skipped Emails         : {total_skipped}")
    print(f"   ├─ Invalid Format    : {invalid_count}")
    print(f"   ├─ In-File Duplicate : {duplicate_in_file_count}")
    print(f"   └─ Already Sent Today: {duplicate_today_count}")
    print(f" Total Execution Time   : {minutes}m {seconds}s")
    print(" Log Files Location     : logs/email_log.csv | logs/email_log.txt")
    print("=" * 60 + "\n")


def validate_setup_only() -> None:
    """Validate system setup, configuration, emails.txt, and resume attachment."""
    print("\n🔍 RUNNING SYSTEM VALIDATION CHECK...")

    # Check .env configuration
    try:
        config.validate()
        print(" ✅ .env File & Credentials Syntax: VALID")
    except Exception as e:
        print(f" ❌ .env Configuration Error: {e}")

    # Check Resume PDF
    resume_path = config.absolute_resume_path
    if resume_path.exists() and resume_path.is_file():
        print(f" ✅ Resume PDF File: FOUND ({resume_path})")
    else:
        print(f" ❌ Resume PDF File: MISSING at '{resume_path}'")

    # Check emails.txt
    if config.emails_file.exists():
        valid_emails, invalid, dupes = load_and_clean_emails(config.emails_file)
        print(f" ✅ Recipient File (emails.txt): FOUND ({len(valid_emails)} valid emails, {invalid} invalid, {dupes} duplicate lines)")
    else:
        print(f" ❌ Recipient File (emails.txt): MISSING at '{config.emails_file}'")

    print("\nValidation check completed.\n")


def main() -> None:
    """Parse CLI arguments and dispatch execution."""
    parser = argparse.ArgumentParser(
        description="Production-Ready Python Email Automation System for Job Applications"
    )
    parser.add_argument(
        "--now",
        action="store_true",
        help="Execute email dispatch batch immediately once instead of starting the scheduler."
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Start continuous daily scheduler (09:00, 10:00, 13:00, 14:00)."
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate configuration, resume file, and recipient list without sending emails."
    )

    args = parser.parse_args()

    if args.validate:
        validate_setup_only()
    elif args.now:
        execute_email_batch()
    else:
        # Default behavior: run daily scheduler
        print("Starting Job Email Automation Scheduler...")
        scheduler = EmailScheduler(task_function=execute_email_batch)
        scheduler.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUser interrupted execution. Exiting cleanly.")
        sys.exit(0)
