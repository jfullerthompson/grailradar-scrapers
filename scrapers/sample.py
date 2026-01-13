"""
Sample scraper.

Reference implementation for all auctioneer scrapers.
Scrapers must return ALL available price fields.
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

        now = int(time.time())

        return [
            {
                "title": "Sample Baseball Card Lot",
                "image_url": "https://example.com/image1.jpg",
                "product_url": "https://example.com/lot/1",

                # Prices (return everything available)
                "price_current": 0,          # no bids yet
                "price_start": 100.00,       # starting bid
                "price_estimate_low": 1000.00,
                "price_estimate_high": 1500.00,

                "price_currency": "USD",
                "end_timestamp": now + 3600,  # ends in 1 hour
            },
            {
                "title": "Sample Memorabilia Lot",
                "image_url": "https://example.com/image2.jpg",
                "product_url": "https://example.com/lot/2",

                "price_current": 250.00,     # live bid exists
                "price_start": 50.00,
                "price_estimate_low": 500.00,
                "price_estimate_high": 800.00,

                "price_currency": "USD",
                "end_timestamp": now + 7200,
            },
        ]
