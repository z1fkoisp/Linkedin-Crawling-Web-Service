"""
LinkedIn Web Crawler - Selenium-based profile scraper
This module provides functionality to scrape publicly available LinkedIn profile data.
"""

import time
import logging
from typing import List, Dict, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# Configure logging for the crawler
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInCrawler:
    """
    LinkedIn Profile Crawler using Selenium WebDriver

    This class handles authentication and scraping of LinkedIn profile data.
    It uses Chrome in headless mode for automated browsing and data extraction.
    """

    # LinkedIn URLs and selectors as constants
    LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"
    USERNAME_SELECTOR = "username"
    PASSWORD_SELECTOR = "session_password"
    LOGIN_BUTTON_XPATH = '//*[@id="organic-div"]/form/div[3]/button'

    # Profile data selectors (may need updates as LinkedIn changes their DOM)
    NAME_SELECTOR = ('li', {'class': 'inline t-24 t-black t-normal break-words'})
    TITLE_SELECTOR = ('h2', {'class': 'mt1 t-18 t-black t-normal break-words'})
    LOCATION_SELECTOR = ('li', {'class': 't-16 t-black t-normal inline-block'})

    # Timing constants
    PAGE_LOAD_WAIT = 3
    ELEMENT_WAIT_TIMEOUT = 10
    SCRAPE_DELAY = 2

    def __init__(self, username: str, password: str, headless: bool = True):
        """
        Initialize the LinkedIn crawler

        Args:
            username: LinkedIn login email/username
            password: LinkedIn login password
            headless: Run browser in headless mode (default: True)
        """
        self.username = username
        self.password = password
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.is_logged_in = False

        logger.info("Initializing LinkedIn Crawler")
        self._init_driver()

    def _init_driver(self) -> None:
        """
        Initialize Chrome WebDriver with appropriate options
        """
        try:
            options = ChromeOptions()

            if self.headless:
                options.add_argument('--headless')

            # Anti-detection measures
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Performance optimizations
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')  # Speed up loading

            # User agent to appear more like a regular browser
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            self.driver = webdriver.Chrome(options=options)

            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            logger.info("Chrome WebDriver initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def login(self) -> bool:
        """
        Log into LinkedIn using provided credentials

        Returns:
            bool: True if login successful, False otherwise
        """
        if not self.driver:
            logger.error("WebDriver not initialized")
            return False

        try:
            logger.info("Attempting to log into LinkedIn")
            self.driver.get(self.LINKEDIN_LOGIN_URL)

            # Wait for login form to load
            WebDriverWait(self.driver, self.ELEMENT_WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, self.USERNAME_SELECTOR))
            )

            # Enter credentials
            username_field = self.driver.find_element(By.ID, self.USERNAME_SELECTOR)
            username_field.clear()
            username_field.send_keys(self.username)

            password_field = self.driver.find_element(By.NAME, self.PASSWORD_SELECTOR)
            password_field.clear()
            password_field.send_keys(self.password)

            # Click login button
            login_button = self.driver.find_element(By.XPATH, self.LOGIN_BUTTON_XPATH)
            login_button.click()

            # Wait for redirect or profile page
            time.sleep(self.PAGE_LOAD_WAIT)

            # Check if login was successful
            current_url = self.driver.current_url
            if "login" in current_url or "checkpoint" in current_url:
                logger.error("Login failed - still on login page or checkpoint")
                return False

            self.is_logged_in = True
            logger.info("Successfully logged into LinkedIn")
            return True

        except TimeoutException:
            logger.error("Login timeout - page took too long to load")
            return False
        except NoSuchElementException as e:
            logger.error(f"Login element not found: {e}")
            return False
        except Exception as e:
            logger.error(f"Login failed with error: {e}")
            return False

    def scrape_profile(self, url: str) -> Dict[str, Any]:
        """
        Scrape profile data from a LinkedIn profile URL

        Args:
            url: LinkedIn profile URL to scrape

        Returns:
            Dict containing profile data or error information
        """
        if not self.driver or not self.is_logged_in:
            return {"error": "Crawler not properly initialized or logged in"}

        try:
            logger.info(f"Scraping profile: {url}")
            self.driver.get(url)

            # Wait for page to load
            time.sleep(self.SCRAPE_DELAY)

            # Parse page content
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Extract profile data with error handling
            profile_data = {
                "name": self._extract_text(soup, self.NAME_SELECTOR),
                "title": self._extract_text(soup, self.TITLE_SELECTOR),
                "location": self._extract_text(soup, self.LOCATION_SELECTOR),
                "url": url
            }

            # Check if we got any data
            if not any(profile_data.values()):
                logger.warning(f"No data extracted from profile: {url}")
                return {"error": "No profile data found", "url": url}

            logger.info(f"Successfully scraped profile: {profile_data.get('name', 'Unknown')}")
            return profile_data

        except Exception as e:
            logger.error(f"Error scraping profile {url}: {e}")
            return {"error": "Scraping failed", "url": url}

    def _extract_text(self, soup: BeautifulSoup, selector: tuple) -> Optional[str]:
        """
        Extract text content from BeautifulSoup element

        Args:
            soup: BeautifulSoup object
            selector: Tuple of (tag, attributes) for finding element

        Returns:
            Extracted text or None if not found
        """
        try:
            element = soup.find(selector[0], selector[1])
            return element.text.strip() if element else None
        except Exception:
            return None

    def crawl_profiles(self, profiles: List[str]) -> List[Dict[str, Any]]:
        """
        Crawl multiple LinkedIn profiles

        Args:
            profiles: List of LinkedIn profile URLs

        Returns:
            List of profile data dictionaries
        """
        if not profiles:
            logger.warning("No profiles provided for crawling")
            return []

        logger.info(f"Starting to crawl {len(profiles)} profiles")

        # Ensure we're logged in
        if not self.is_logged_in:
            if not self.login():
                return [{"error": "Failed to login to LinkedIn"}]

        results = []

        for i, profile_url in enumerate(profiles, 1):
            logger.info(f"Processing profile {i}/{len(profiles)}: {profile_url}")

            try:
                profile_data = self.scrape_profile(profile_url)
                results.append(profile_data)

                # Add delay between requests to be respectful
                if i < len(profiles):
                    time.sleep(1)

            except Exception as e:
                logger.error(f"Failed to process profile {profile_url}: {e}")
                results.append({"error": "Processing failed", "url": profile_url})

        logger.info(f"Crawling completed. Processed {len(results)} profiles")
        return results

    def close(self) -> None:
        """
        Clean up resources and close the browser
        """
        if self.driver:
            logger.info("Closing WebDriver")
            self.driver.quit()
            self.driver = None
            self.is_logged_in = False

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures cleanup"""
        self.close()
