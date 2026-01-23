"""
Configuration settings for the LinkedIn Web Crawler application.

This module defines all configuration parameters using Pydantic BaseSettings
for type safety and environment variable support. Settings are loaded from
environment variables with fallback to default values.
"""

import os
import secrets
from typing import List, Optional
from pydantic import BaseSettings, Field, validator


class AppSettings(BaseSettings):
    """
    Core application settings.

    Defines the basic configuration for running the FastAPI application,
    including server settings, environment mode, and API configuration.
    """

    # Application metadata
    app_name: str = Field(default="LinkedIn Web Crawler", description="Name of the application")
    app_version: str = Field(default="1.0.0", description="Version of the application")
    app_description: str = Field(
        default="A web service for crawling LinkedIn profiles",
        description="Description of the application"
    )

    # Server settings
    host: str = Field(default="0.0.0.0", description="Host address to bind the server")
    port: int = Field(default=8000, description="Port number for the server")
    debug: bool = Field(default=False, description="Enable debug mode for development")

    # API settings
    api_v1_prefix: str = Field(default="/api/v1", description="Prefix for API version 1 endpoints")
    docs_url: str = Field(default="/docs", description="URL for API documentation")
    redoc_url: str = Field(default="/redoc", description="URL for ReDoc documentation")

    # CORS settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed origins for CORS"
    )
    cors_allow_credentials: bool = Field(default=True, description="Allow credentials in CORS")
    cors_allow_methods: List[str] = Field(
        default=["*"],
        description="Allowed HTTP methods for CORS"
    )
    cors_allow_headers: List[str] = Field(
        default=["*"],
        description="Allowed headers for CORS"
    )

    # Security settings
    secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Secret key for JWT tokens and sessions"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Expiration time for access tokens in minutes"
    )

    class Config:
        """Pydantic configuration for environment variable loading."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class CrawlerSettings(BaseSettings):
    """
    Web crawler specific settings.

    Configures the behavior of the LinkedIn profile crawler,
    including timeouts, delays, and scraping parameters.
    """

    # Browser settings
    browser_headless: bool = Field(
        default=True,
        description="Run browser in headless mode (no GUI)"
    )
    browser_timeout: int = Field(
        default=30,
        description="Timeout for browser operations in seconds"
    )
    page_load_timeout: int = Field(
        default=20,
        description="Timeout for page loading in seconds"
    )

    # Scraping delays and limits
    request_delay: float = Field(
        default=2.0,
        description="Delay between requests in seconds to avoid rate limiting"
    )
    max_profiles_per_session: int = Field(
        default=50,
        description="Maximum number of profiles to crawl per session"
    )
    max_concurrent_requests: int = Field(
        default=1,
        description="Maximum number of concurrent scraping requests"
    )

    # Retry settings
    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts for failed requests"
    )
    retry_delay: float = Field(
        default=1.0,
        description="Delay between retry attempts in seconds"
    )

    # LinkedIn specific settings
    linkedin_login_url: str = Field(
        default="https://www.linkedin.com/login",
        description="LinkedIn login page URL"
    )
    linkedin_base_url: str = Field(
        default="https://www.linkedin.com",
        description="Base LinkedIn URL"
    )

    class Config:
        """Pydantic configuration for environment variable loading."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class DatabaseSettings(BaseSettings):
    """
    Database configuration settings.

    Currently configured for future database integration.
    Uncomment and configure when adding database support.
    """

    # Database connection (for future use)
    # database_url: str = Field(
    #     default="sqlite:///./linkedin_crawler.db",
    #     description="Database connection URL"
    # )
    # database_echo: bool = Field(
    #     default=False,
    #     description="Enable SQL query logging"
    # )

    class Config:
        """Pydantic configuration for environment variable loading."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class LoggingSettings(BaseSettings):
    """
    Logging configuration settings.

    Controls how logging is handled throughout the application.
    """

    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format"
    )
    log_file: Optional[str] = Field(
        default="logs/app.log",
        description="Path to log file (optional)"
    )

    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate that log level is one of the allowed values."""
        allowed_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {', '.join(allowed_levels)}")
        return v.upper()

    class Config:
        """Pydantic configuration for environment variable loading."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instances
app_settings = AppSettings()
crawler_settings = CrawlerSettings()
database_settings = DatabaseSettings()
logging_settings = LoggingSettings()


def get_settings():
    """
    Get all application settings as a dictionary.

    Useful for debugging and configuration inspection.

    Returns:
        dict: Dictionary containing all settings
    """
    return {
        "app": app_settings.dict(),
        "crawler": crawler_settings.dict(),
        "database": database_settings.dict(),
        "logging": logging_settings.dict(),
    }


def create_env_file_example():
    """
    Create an example .env file with all available configuration options.

    This function generates a sample environment file that can be used
    as a template for configuration.
    """
    env_content = """# LinkedIn Web Crawler Configuration
# Copy this file to .env and modify the values as needed

# Application Settings
APP_NAME=LinkedIn Web Crawler
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
DEBUG=false

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Security Settings
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Crawler Settings
BROWSER_HEADLESS=true
BROWSER_TIMEOUT=30
PAGE_LOAD_TIMEOUT=20
REQUEST_DELAY=2.0
MAX_PROFILES_PER_SESSION=50
MAX_CONCURRENT_REQUESTS=1
MAX_RETRIES=3
RETRY_DELAY=1.0

# Logging Settings
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Database Settings (for future use)
# DATABASE_URL=sqlite:///./linkedin_crawler.db
# DATABASE_ECHO=false
"""

    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)

    print("Created .env.example file with configuration template")


# Create example env file if this module is run directly
if __name__ == "__main__":
    create_env_file_example()