"""
Sample scraper.

Reference implementation for all auctioneer scrapers.
Scrapers must return ALL available price fields.

IMPORTANT:
- end_timestamp MUST be UTC unix epoch MILLISECONDS (int, 13-digit)
"""

import time
from typing import List, Dict, Any

from core.base_scraper import BaseScraper


class SampleScraper(BaseScraper):
    auctioneer = "sample"
    default_currency = "USD"

    def fetch_items(self) -> List[Dict[str, Any]]:
        """
        Return a complete list of LIVE auction items.

        Rules:
        - Only live auctions
        - Pagination handled here
        - Return raw dicts (not normalised)
        - Return ALL available prices
        """

        # current time in UTC epoch milliseconds
        now_ms = int(time.time() * 1000)

        return [
            {
                "title": "Sample Baseball Card Lot",
                "

