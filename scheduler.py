"""Scheduler module for Email Automation System.

Configures APScheduler to trigger daily automated email dispatches at
09:00 AM, 10:00 AM, 01:00 PM, and 02:00 PM continuously until manually stopped.
"""

import sys
import time
from typing import Callable
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from logger import logger


class EmailScheduler:
    """Manages background/blocking cron schedule for daily email automation."""

    def __init__(self, task_function: Callable[[], None]) -> None:
        """Initialize scheduler with target automation task function.

        Args:
            task_function: Callback function to execute on scheduled triggers.
        """
        self.task_function = task_function
        self.scheduler = BlockingScheduler()

    def setup_jobs(self) -> None:
        """Register cron jobs for daily execution at 09:00, 10:00, 13:00, and 14:00."""
        scheduled_times = [
            ("09:00 AM", 9, 0),
            ("10:00 AM", 10, 0),
            ("01:00 PM", 13, 0),
            ("02:00 PM", 14, 0),
        ]

        for label, hour, minute in scheduled_times:
            trigger = CronTrigger(hour=hour, minute=minute)
            self.scheduler.add_job(
                func=self.task_function,
                trigger=trigger,
                id=f"email_job_{hour:02d}_{minute:02d}",
                name=f"Daily Email Dispatch at {label}",
                replace_existing=True,
            )
            logger.info(f"Registered Scheduled Job: Daily at {label} ({hour:02d}:{minute:02d})")

    def start(self) -> None:
        """Start the BlockingScheduler loop."""
        self.setup_jobs()
        logger.info("==================================================")
        logger.info("APScheduler Daily Email Automation Service Started")
        logger.info("Schedule Times: 09:00 AM | 10:00 AM | 01:00 PM | 02:00 PM")
        logger.info("Press Ctrl+C to terminate automation process.")
        logger.info("==================================================")

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("\nShutdown signal received. Stopping Email Scheduler gracefully...")
            self.scheduler.shutdown(wait=False)
            logger.info("Email Automation Scheduler stopped.")
            sys.exit(0)
