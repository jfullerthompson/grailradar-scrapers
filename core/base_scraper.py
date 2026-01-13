"""
Base scraper class.

Responsibilities:
- HTTP requests via ScraperAPI
- Retry + timeout handling
- Define the interface for auctioneer scrapers

Scrapers should:
- Inherit from BaseScraper
- Implement fetch_items()
- Return a list of raw dicts (auctioneer-specific)
"""

import os
import time
import requests
from typing import List, Dict, Any


SCRAPERAPI_ENDPOINT = "http://api.scraperapi.com"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3


class BaseScraper:
    auctioneer: str  # must be set by subclasses

    def __init__(self):
        self.api_key = os.getenv("SCRAPERAPI_KEY")
        if not self.api_key:
            raise EnvironmentError("SCRAPERAPI_KEY not set")

    # -------------------------
    # HTTP
    # -------------------------

    def get(self, url: str, *, params: Dict[str, Any] | None = None) -> str:
        """
        Fetch a page via ScraperAPI with retries.
        Returns response text.
        """
        params = params or {}

        payload = {
            "api_key": self.api_key,
            "url": url,
            "render": "false",
        }

        for attempt in range(1, DEFAULT_RETRIES + 1):
            try:
                response = requests.get(
                    SCRAPERAPI_ENDPOINT,
                    params={**payload, **params},
                    timeout=DEFAULT_TIMEOUT,
                )
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt == DEFAULT_RETRIES:
                    raise
                time.sleep(2 * attempt)

        raise RuntimeError("Unreachable")

    # -------------------------
    # Interface
    # -------------------------

    def fetch_items(self) -> List[Dict[str, Any]]:
        """
        Must be implemented by subclasses.

        Returns:
        - List of raw item dicts
        - Each dict can contain auctioneer-specific fields
        """
        raise NotImplementedError("fetch_items() must be implemented by scraper")
