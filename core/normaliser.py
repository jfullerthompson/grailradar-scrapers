"""
Normalises raw scraper items into locked v1 Typesense documents.
"""

import time
from typing import Dict, Any, Optional

from core.schema import build_typesense_document


class NormalisationError(Exception):
    pass


def normalise_item(
    raw: Dict[str, Any],
    *,
    auctioneer: str,
    default_currency: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Convert a raw scraper item into a Typesense document.

    Returns:
    - Typesense document dict
    - None if item should be dropped
    """

    # -------------------------
    # Required raw fields
    # -------------------------
    title = raw.get("title")
    image_url = raw.get("image_url")
    product_url = raw.get("product_url")
    end_timestamp = raw.get("end_timestamp")

    if not all([title, image_url, product_url, end_timestamp]):
        return None  # drop item

    # -------------------------
    # 🚫 Drop ended auctions (safety guard)
    # -------------------------
    now = int(time.time())
    if end_timestamp < now:
        return None

      # -------------------------
    # Price selection
    # -------------------------
    price = None

    if raw.get("price_current", 0) > 0:
        price = raw["price_current"]
    elif raw.get("price_start", 0) > 0:
        price = raw["price_start"]
    elif raw.get("price_estimate_low", 0) > 0:
        price = raw["price_estimate_low"]

    if price is None:
        return None

    # -------------------------
    # Currency
    # -------------------------
    currency = raw.get("price_currency") or default_currency
    if not currency:
        return None

    # -------------------------
    # Build Typesense document
    # -------------------------
    try:
        return build_typesense_document(
            title=title,
            auctioneer=auctioneer,
            image_url=image_url,
            product_url=product_url,
            price_current=price,
            price_currency=currency,
            end_timestamp=end_timestamp,
        )
    except Exception as e:
        raise NormalisationError(str(e))


