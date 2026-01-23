"""
LinkedIn Credentials Management Module

This module provides secure credential management for LinkedIn authentication.
It supports multiple credential sources and includes validation and security features.
"""

import os
import json
import logging
from typing import Tuple, Optional, Dict, Any
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class CredentialsManager:
    """
    Secure credentials management for LinkedIn authentication

    Supports multiple credential sources:
    1. Environment variables (recommended for production)
    2. JSON configuration file
    3. Interactive input (development only)
    """

    # Default file paths
    DEFAULT_CONFIG_FILE = Path.home() / ".linkedin_credentials.json"
    CONFIG_FILE = Path("config") / "credentials.json"

    # Environment variable names
    ENV_USERNAME = "LINKEDIN_USERNAME"
    ENV_PASSWORD = "LINKEDIN_PASSWORD"

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize credentials manager

        Args:
            config_file: Path to JSON config file (optional)
        """
        self.config_file = config_file or self._find_config_file()
        self._credentials_cache: Optional[Tuple[str, str]] = None

    def _find_config_file(self) -> Optional[Path]:
        """
        Find the best available config file

        Priority: project config > user home config
        """
        if self.CONFIG_FILE.exists():
            return self.CONFIG_FILE
        elif self.DEFAULT_CONFIG_FILE.exists():
            return self.DEFAULT_CONFIG_FILE
        return None

    def get_credentials(self, use_cache: bool = True) -> Tuple[str, str]:
        """
        Get LinkedIn credentials from the best available source

        Args:
            use_cache: Whether to use cached credentials if available

        Returns:
            Tuple of (username, password)

        Raises:
            CredentialsError: If credentials cannot be obtained
        """
        # Return cached credentials if available and requested
        if use_cache and self._credentials_cache:
            logger.debug("Using cached credentials")
            return self._credentials_cache

        # Try different credential sources in order of preference
        sources = [
            ("Environment variables", self._get_from_env),
            ("Config file", self._get_from_file),
            ("Interactive input", self._get_from_input),
        ]

        for source_name, source_func in sources:
            try:
                logger.info(f"Attempting to get credentials from: {source_name}")
                credentials = source_func()
                if credentials and self._validate_credentials(*credentials):
                    self._credentials_cache = credentials
                    logger.info(f"Successfully obtained credentials from: {source_name}")
                    return credentials
            except Exception as e:
                logger.warning(f"Failed to get credentials from {source_name}: {e}")
                continue

        raise CredentialsError("Unable to obtain valid LinkedIn credentials from any source")

    def _get_from_env(self) -> Optional[Tuple[str, str]]:
        """
        Get credentials from environment variables

        Returns:
            Tuple of (username, password) or None if not found
        """
        username = os.getenv(self.ENV_USERNAME)
        password = os.getenv(self.ENV_PASSWORD)

        if username and password:
            return username, password
        return None

    def _get_from_file(self) -> Optional[Tuple[str, str]]:
        """
        Get credentials from JSON config file

        Returns:
            Tuple of (username, password) or None if not found
        """
        if not self.config_file or not self.config_file.exists():
            return None

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            username = config.get('username') or config.get('email')
            password = config.get('password')

            if username and password:
                return username, password

        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error reading config file {self.config_file}: {e}")

        return None

    def _get_from_input(self) -> Optional[Tuple[str, str]]:
        """
        Get credentials from interactive input (development only)

        WARNING: This method echoes input to console and should only be used in development

        Returns:
            Tuple of (username, password) or None if cancelled
        """
        try:
            print("\n=== LinkedIn Credentials Required ===")
            print("WARNING: Input will be visible on screen")
            print("For production, use environment variables or config file\n")

            username = input("LinkedIn Email/Username: ").strip()
            if not username:
                return None

            password = input("LinkedIn Password: ").strip()
            if not password:
                return None

            return username, password

        except (KeyboardInterrupt, EOFError):
            print("\nCredential input cancelled")
            return None

    def _validate_credentials(self, username: str, password: str) -> bool:
        """
        Validate credential format and requirements

        Args:
            username: LinkedIn username/email
            password: LinkedIn password

        Returns:
            True if credentials appear valid
        """
        if not username or not password:
            return False

        # Basic email format validation for username
        if '@' in username:
            if not self._is_valid_email(username):
                logger.warning("Username appears to be an invalid email format")
                return False

        # Password strength check (basic)
        if len(password) < 6:
            logger.warning("Password is too short (minimum 6 characters)")
            return False

        return True

    def _is_valid_email(self, email: str) -> bool:
        """
        Basic email format validation

        Args:
            email: Email address to validate

        Returns:
            True if email format is valid
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def save_credentials(self, username: str, password: str, file_path: Optional[Path] = None) -> bool:
        """
        Save credentials to a JSON config file

        Args:
            username: LinkedIn username/email
            password: LinkedIn password
            file_path: Path to save config file (optional)

        Returns:
            True if saved successfully
        """
        if not self._validate_credentials(username, password):
            raise CredentialsError("Invalid credentials provided")

        config_path = file_path or self.CONFIG_FILE
        config_path.parent.mkdir(parents=True, exist_ok=True)

        config = {
            "username": username,
            "password": password,
            "_comment": "LinkedIn credentials - Keep this file secure!",
            "_created": str(Path(__file__).parent),
        }

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            # Set restrictive permissions if on Unix-like system
            try:
                os.chmod(config_path, 0o600)  # Owner read/write only
            except OSError:
                pass  # Windows or permission denied

            logger.info(f"Credentials saved to {config_path}")
            return True

        except IOError as e:
            logger.error(f"Failed to save credentials: {e}")
            return False

    def clear_cache(self) -> None:
        """
        Clear cached credentials (forces re-fetch on next request)
        """
        self._credentials_cache = None
        logger.debug("Credentials cache cleared")


class CredentialsError(Exception):
    """
    Exception raised when credential operations fail
    """
    pass


# Global credentials manager instance
_credentials_manager = CredentialsManager()


def get_credentials() -> Tuple[str, str]:
    """
    Get LinkedIn credentials using the global credentials manager

    This is a convenience function that maintains backward compatibility
    with the original simple interface.

    Returns:
        Tuple of (username, password)

    Raises:
        CredentialsError: If credentials cannot be obtained
    """
    return _credentials_manager.get_credentials()


def save_credentials(username: str, password: str, file_path: Optional[Path] = None) -> bool:
    """
    Save credentials using the global credentials manager

    Args:
        username: LinkedIn username/email
        password: LinkedIn password
        file_path: Optional path to save config file

    Returns:
        True if saved successfully
    """
    return _credentials_manager.save_credentials(username, password, file_path)
