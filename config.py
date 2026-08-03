"""Configuration module for Email Automation System.

Handles environment variable loading, default values, directory initialization,
and configuration validation.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Application configuration settings loaded from environment variables."""

    email_address: str = field(default_factory=lambda: os.getenv("EMAIL_ADDRESS", "").strip())
    email_app_password: str = field(default_factory=lambda: os.getenv("EMAIL_APP_PASSWORD", "").strip())
    smtp_server: str = field(default_factory=lambda: os.getenv("SMTP_SERVER", "smtp.gmail.com").strip())
    smtp_port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "587")))
    resume_path: str = field(default_factory=lambda: os.getenv("RESUME_PATH", "resume/Vaibhav_Sharma_Resume.pdf").strip())

    # File & Directory Paths
    base_dir: Path = field(default_factory=lambda: Path(__file__).parent.resolve())
    logs_dir: Path = field(init=False)
    resume_dir: Path = field(init=False)
    emails_file: Path = field(init=False)
    success_file: Path = field(init=False)
    failed_file: Path = field(init=False)
    log_csv: Path = field(init=False)
    log_txt: Path = field(init=False)

    def __post_init__(self) -> None:
        """Initialize resolved paths and create necessary directories."""
        self.logs_dir = self.base_dir / "logs"
        self.resume_dir = self.base_dir / "resume"
        self.emails_file = self.base_dir / "emails.txt"
        self.success_file = self.base_dir / "success_emails.txt"
        self.failed_file = self.base_dir / "failed_emails.txt"
        self.log_csv = self.logs_dir / "email_log.csv"
        self.log_txt = self.logs_dir / "email_log.txt"

        # Create directories if they do not exist
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.resume_dir.mkdir(parents=True, exist_ok=True)

    def validate(self) -> None:
        """Validate configuration settings and check for missing values or placeholders.

        Raises:
            ValueError: If critical configuration parameters are missing or default placeholders.
        """
        errors = []

        if not self.email_address:
            errors.append("EMAIL_ADDRESS is missing in .env file.")
        elif "@" not in self.email_address:
            errors.append(f"EMAIL_ADDRESS '{self.email_address}' is invalid.")

        if not self.email_app_password:
            errors.append("EMAIL_APP_PASSWORD is missing in .env file.")
        elif "your_16_digit_app_password_here" in self.email_app_password.lower():
            errors.append("EMAIL_APP_PASSWORD contains placeholder value. Please set your Gmail App Password.")

        if not self.smtp_server:
            errors.append("SMTP_SERVER is missing in .env file.")

        if not self.smtp_port:
            errors.append("SMTP_PORT is missing in .env file.")

        if errors:
            raise ValueError("Configuration Validation Failed:\n" + "\n".join(f"- {err}" for err in errors))

    @property
    def absolute_resume_path(self) -> Path:
        """Return absolute path to resume PDF."""
        path = Path(self.resume_path)
        if path.is_absolute():
            return path
        return self.base_dir / path


# Instantiate singleton configuration instance
config = Config()
