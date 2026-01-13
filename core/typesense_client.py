"""
Typesense client for upserting and hard-deleting documents.
"""

import os
from typing import List, Dict, Any

import typesense


class TypesenseClient:
    def __init__(self):
        self.client = typesense.Client({
            "nodes": [{
                "host": os.getenv("TYPESENSE_HOST"),
                "port": os.getenv("TYPESENSE_PORT", "443"),
                "protocol": os.getenv("TYPESENSE_PROTOCOL", "https"),
            }],
            "api_key": os.getenv("TYPESENSE_API_KEY"),
            "connection_timeout_seconds": 10,
        })

        self.collection = os.getenv("TYPESENSE_COLLECTION")
        if not self.collection:
            raise EnvironmentError("TYPESENSE_COLLECTION not set")

    # -------------------------
    # Upsert
    # -------------------------

    def upsert_documents(self, docs: List[Dict[str, Any]]) -> None:
        if not docs:
            return

        self.client.collections[self.collection].documents.import_(
            docs,
            {"action": "upsert"},
        )

    # -------------------------
    # Hard delete
    # -------------------------

    def delete_by_ids(self, object_ids: List[str]) -> None:
        if not object_ids:
            return

        # Chunk to avoid URL length issues
        CHUNK = 100
        for i in range(0, len(object_ids), CHUNK):
            batch = object_ids[i : i + CHUNK]
            filter_by = "objectID:=[" + ",".join(batch) + "]"
            self.client.collections[self.collection].documents.delete(
                {"filter_by": filter_by}
            )
