"""
LinkedIn Web Crawler Application Package.

This package contains the core components of the LinkedIn web crawler service,
including API routes, configuration, utilities, and crawler functionality.

The application is built using FastAPI for the web framework and Selenium
for browser automation to scrape LinkedIn profiles ethically and responsibly.
"""

# Package metadata
__version__ = "1.0.0"
__author__ = "LinkedIn Crawler Team"
__description__ = "A web service for crawling LinkedIn profiles with ethical scraping practices"
__license__ = "MIT"

# Standard library imports
import logging
from typing import Optional

# Third-party imports
from fastapi import FastAPI

# Local imports - core modules
from .config import (
    app_settings,
    crawler_settings,
    database_settings,
    logging_settings,
    get_settings
)
from .routes import router as api_router
from .crawler import LinkedInCrawler
from .credentials import CredentialManager
from .utils import (
    validate_profiles,
    sanitize_text,
    format_profile_data,
    delay_execution
)

# Configure package-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging_settings.log_level)

# Create console handler if not already configured
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_settings.log_level)
    formatter = logging.Formatter(logging_settings.log_format)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    This function initializes the main FastAPI app with all necessary
    middleware, routes, and settings for the LinkedIn crawler service.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Create FastAPI app with settings
    app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        description=app_settings.app_description,
        debug=app_settings.debug,
        docs_url=app_settings.docs_url,
        redoc_url=app_settings.redoc_url,
    )

    # Configure CORS
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=app_settings.cors_allow_credentials,
        allow_methods=app_settings.cors_allow_methods,
        allow_headers=app_settings.cors_allow_headers,
    )

    # Include API routes
    app.include_router(
        api_router,
        prefix=app_settings.api_v1_prefix,
        tags=["LinkedIn Crawler API"]
    )

    # Add startup and shutdown event handlers
    @app.on_event("startup")
    async def startup_event():
        """Handle application startup tasks."""
        logger.info("Starting LinkedIn Web Crawler application")
        logger.info(f"Version: {__version__}")
        logger.info(f"Debug mode: {app_settings.debug}")

        # Initialize crawler components if needed
        # This could include setting up browser instances or connections

    @app.on_event("shutdown")
    async def shutdown_event():
        """Handle application shutdown tasks."""
        logger.info("Shutting down LinkedIn Web Crawler application")

        # Cleanup tasks
        # Close browser instances, save state, etc.

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint to verify service status.

        Returns:
            dict: Health status information
        """
        return {
            "status": "healthy",
            "version": __version__,
            "service": app_settings.app_name
        }

    logger.info("FastAPI application created successfully")
    return app


def get_crawler_instance() -> LinkedInCrawler:
    """
    Get a configured LinkedIn crawler instance.

    This factory function creates a new crawler instance with
    the current configuration settings.

    Returns:
        LinkedInCrawler: Configured crawler instance
    """
    credential_manager = CredentialManager()
    crawler = LinkedInCrawler(
        credential_manager=credential_manager,
        headless=crawler_settings.browser_headless,
        timeout=crawler_settings.browser_timeout
    )
    logger.debug("Created new LinkedIn crawler instance")
    return crawler


# Package-level exports
# These make it easy to import commonly used components
__all__ = [
    # Core classes
    "LinkedInCrawler",
    "CredentialManager",

    # Configuration
    "app_settings",
    "crawler_settings",
    "database_settings",
    "logging_settings",
    "get_settings",

    # Utility functions
    "validate_profiles",
    "sanitize_text",
    "format_profile_data",
    "delay_execution",

    # Application factory
    "create_application",
    "get_crawler_instance",

    # Metadata
    "__version__",
    "__author__",
    "__description__",
    "__license__",
]


# Initialize package logger
logger.info("LinkedIn Crawler app package initialized")