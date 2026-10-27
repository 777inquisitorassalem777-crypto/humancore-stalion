import hashlib
import json
from copy import deepcopy

def digest(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                     separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

class ChainMemory:
    """In-memory hash chain. No authentication or protection against full rewrite."""
    def __init__(self):
        self._records = []

    @property
    def records(self):
        return deepcopy(self._records)

    def append(self, payload):
        body = {"index": len(self._records),
                "previous": self._records[-1]["hash"] if self._records else "0" * 64,
                "payload": deepcopy(payload)}
        record = {**body, "hash": digest(body)}
        self._records.append(record)
        return deepcopy(record)

    @staticmethod
    def verify(records):
        previous = "0" * 64
        try:
            for index, record in enumerate(records):
                body = {key: record[key] for key in ("index", "previous", "payload")}
                if record["index"] != index or record["previous"] != previous:
                    return False
                if digest(body) != record["hash"]:
                    return False
                previous = record["hash"]
            return True
        except (KeyError, TypeError, ValueError):
            return False
