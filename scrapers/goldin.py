import time
import requests
from typing import List, Dict, Any

from core.base_scraper import BaseScraper


class GoldinScraper(BaseScraper):
    auctioneer = "Goldin"
    default_currency = "USD"

    def fetch_items(self) -> List[Dict[str, Any]]:
        """
        Fetch all live Goldin lots and return raw item dicts.
        Normalisation + Typesense handled elsewhere.
        """
        url = "https://d1wu47wucybvr3.cloudfront.net/api/lots_v2"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://goldin.co",
            "Referer": "https://goldin.co/buy",
            "User-Agent": "Mozilla/5.0",
        }

        all_items: List[Dict[str, Any]] = []
        size = 24
        offset = 0

        while True:
            payload = {
                "search": {
                    "queryType": "Featured",
                    "size": size,
                    "from": offset,
                }
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=20,
            )
            response.raise_for_status()

            data = response.json()
            lots = data.get("searchalgolia", {}).get("lots", [])

            if not lots:
                break

            for lot in lots:
                lot_id = lot.get("lot_id")
                img_name = lot.get("primary_image_name")

                image_url = (
                    f"https://d2tt46f3mh26nl.cloudfront.net/public/Lots/{lot_id}/{img_name}@1x"
                    if lot_id and img_name
                    else None
                )

                item = {
                    "title": str(lot.get("title", "")).strip(),
                    "image_url": image_url,
                    "product_url": f"https://goldin.co/item/{lot.get('meta_slug')}",
                    "price_current": float(lot.get("current_bid", 0)),
                    "price_start": float(lot.get("min_bid", 0)),
                    "price_estimate_low": float(lot.get("low_estimate", 0)),
                    "price_estimate_high": float(lot.get("high_estimate", 0)),
                    "price_currency": self.default_currency,
                    "end_timestamp": int(lot.get("auction_end_date", 0)),
                }

                all_items.append(item)

            offset += size
            time.sleep(0.5)

        return all_items
