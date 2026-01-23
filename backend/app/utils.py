"""
Utility functions for the LinkedIn Web Crawler application.

This module contains helper functions for data validation, processing,
logging, and other common operations used throughout the backend.
"""

import logging
import re
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

# Configure logger for this module
logger = logging.getLogger(__name__)


def validate_profiles(profiles: List[str]) -> bool:
    """
    Validate a list of LinkedIn profile URLs.

    Checks if all provided URLs are valid LinkedIn profile URLs.
    A valid LinkedIn profile URL must:
    - Start with 'https://www.linkedin.com/'
    - Follow the expected path pattern for profiles

    Args:
        profiles (List[str]): List of profile URLs to validate

    Returns:
        bool: True if all profiles are valid, False otherwise

    Raises:
        ValueError: If profiles is not a list or contains non-string elements
    """
    if not isinstance(profiles, list):
        raise ValueError("Profiles must be provided as a list")

    if not profiles:
        logger.warning("Empty profiles list provided for validation")
        return False

    linkedin_pattern = re.compile(r'^https://www\.linkedin\.com/(in|pub)/[^/]+/?$')

    for profile in profiles:
        if not isinstance(profile, str):
            raise ValueError("All profile URLs must be strings")

        if not linkedin_pattern.match(profile):
            logger.warning(f"Invalid LinkedIn profile URL: {profile}")
            return False

    logger.info(f"Successfully validated {len(profiles)} LinkedIn profile URLs")
    return True


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing extra whitespace and normalizing.

    Args:
        text (str): The text to sanitize

    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        return ""

    # Remove extra whitespace and normalize
    sanitized = re.sub(r'\s+', ' ', text.strip())
    return sanitized


def extract_domain(url: str) -> Optional[str]:
    """
    Extract the domain from a URL.

    Args:
        url (str): The URL to parse

    Returns:
        Optional[str]: The domain if valid, None otherwise
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception as e:
        logger.error(f"Error extracting domain from URL {url}: {e}")
        return None


def delay_execution(seconds: float) -> None:
    """
    Introduce a delay in execution to respect rate limits.

    Args:
        seconds (float): Number of seconds to delay
    """
    logger.debug(f"Delaying execution for {seconds} seconds")
    time.sleep(seconds)


def format_profile_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format raw profile data into a standardized structure.

    Args:
        raw_data (Dict[str, Any]): Raw data extracted from LinkedIn

    Returns:
        Dict[str, Any]: Formatted profile data
    """
    formatted = {
        'name': sanitize_text(raw_data.get('name', '')),
        'headline': sanitize_text(raw_data.get('headline', '')),
        'location': sanitize_text(raw_data.get('location', '')),
        'about': sanitize_text(raw_data.get('about', '')),
        'experience': raw_data.get('experience', []),
        'education': raw_data.get('education', []),
        'skills': raw_data.get('skills', []),
        'url': raw_data.get('url', ''),
        'scraped_at': time.time()  # Timestamp when data was scraped
    }

    logger.debug(f"Formatted profile data for: {formatted.get('name', 'Unknown')}")
    return formatted


def is_valid_linkedin_url(url: str) -> bool:
    """
    Check if a URL is a valid LinkedIn URL.

    Args:
        url (str): The URL to check

    Returns:
        bool: True if valid LinkedIn URL, False otherwise
    """
    if not isinstance(url, str):
        return False

    try:
        parsed = urlparse(url)
        return parsed.scheme == 'https' and parsed.netloc == 'www.linkedin.com'
    except Exception:
        return False


def get_current_timestamp() -> float:
    """
    Get the current Unix timestamp.

    Returns:
        float: Current timestamp
    """
    return time.time()


def log_function_call(func_name: str, *args, **kwargs) -> None:
    """
    Log a function call for debugging purposes.

    Args:
        func_name (str): Name of the function being called
        *args: Positional arguments
        **kwargs: Keyword arguments
    """
    logger.debug(f"Calling {func_name} with args: {args}, kwargs: {kwargs}")
