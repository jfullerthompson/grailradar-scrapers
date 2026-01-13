"""
Main entrypoint.

Flow:
- Run scrapers
- Normalise raw items
- Upsert to Typesense
- Hard delete items no longer present
"""

import os
from typing import List, Set

from core.normaliser import normalise_item
from core.typesense_client import TypesenseClient


def run_scraper(scraper) -> List[dict]:
    return scraper.fetch_items()


def run(scrapers: List[object], *, dry_run: bool = False) -> None:
    ts = TypesenseClient()

    all_docs = []
    seen_ids: Set[str] = set()

    for scraper in scrapers:
        raw_items = run_scraper(scraper)

        for raw in raw_items:
            doc = normalise_item(
                raw,
                auctioneer=scraper.auctioneer,
                default_currency=getattr(scraper, "default_currency", None),
            )
            if not doc:
                continue

            all_docs.append(doc)
            seen_ids.add(doc["objectID"])

    if dry_run:
        print(f"[DRY RUN] Would upsert {len(all_docs)} docs")
        return

    # Upsert current items
    ts.upsert_documents(all_docs)

    # Hard delete missing items
    # (This assumes each run represents full live inventory per auctioneer)
    if seen_ids:
        ts.delete_by_ids(list(seen_ids))


if __name__ == "__main__":
    DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

    # Import scrapers here
    from scrapers.sample import SampleScraper  # placeholder

    run(
        scrapers=[
            SampleScraper(),
        ],
        dry_run=DRY_RUN,
    )
