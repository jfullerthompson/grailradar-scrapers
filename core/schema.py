"""
Locked v1 Typesense schema and validation rules.

This file defines:
- The canonical Typesense document shape
- Hard validation (fail fast)
- Deterministic objectID generation

This is the single source of truth.
"""

import hashlib
import time
from typing import Dict, Any


# -------------------------
# Locked v1 field definition
# -------------------------

REQUIRED_FIELDS = {
    "objectID": str,
    "title": str,
    "auctioneer": str,
    "product_url": str,
    "price_current": (int, float),
    "price_currency": str,
    "end_timestamp": int,
    "added_timestamp": int,
}

OPTIONAL_FIELDS = {
    "image_url": str,
}

ALL_FIELDS = {**REQUIRED_FIELDS, **OPTIONAL_FIELDS}


# -------------------------
# ObjectID generation
# -------------------------

def generate_object_id(auctioneer: str, image_url: str) -> str:
    """
    Generate deterministic objectID from auctioneer + image_url.

    - Lowercased
    - Stripped
    - SHA256 hashed
    """
    if not auctioneer or not image_url:
        raise ValueError("auctioneer and image_url are required for objectID generation")

    base = f"{auctioneer.strip().lower()}|{image_url.strip().lower()}"
    return hashlib.sha256(base.encode("utf
