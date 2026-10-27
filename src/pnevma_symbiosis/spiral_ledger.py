"""Append-only spiral ledger with hash chain (EDGE lineage, simplified)."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional
import hashlib, json, time, uuid

class SpiralLedger:
    def __init__(self, path: Optional[str] = None):
        self.path = Path(path) if path else None
        self.events: List[Dict[str, Any]] = []
        self._prev = "GENESIS"
        if self.path and self.path.exists():
            try:
                data = json.loads(self.path.read_text(encoding="utf-8"))
                self.events = data.get("events", [])
                if self.events:
                    self._prev = self.events[-1].get("event_hash", "GENESIS")
            except Exception:
                pass

    def append(self, kind: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        seq = len(self.events) + 1
        eid = str(uuid.uuid4())[:12]
        ts = time.time()
        body = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False)
        digest = hashlib.sha256(f"{seq}|{eid}|{ts}|{kind}|{body}|{self._prev}".encode()).hexdigest()
        ev = {
            "seq": seq, "event_id": eid, "ts": ts, "kind": kind,
            "payload": payload, "prev_hash": self._prev, "event_hash": digest,
        }
        self.events.append(ev)
        self._prev = digest
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps({"events": self.events}, indent=2, default=str), encoding="utf-8")
        return ev

    def verify(self) -> Dict[str, Any]:
        prev = "GENESIS"
        for i, ev in enumerate(self.events, 1):
            body = json.dumps(ev["payload"], sort_keys=True, default=str, ensure_ascii=False)
            h = hashlib.sha256(
                f"{ev['seq']}|{ev['event_id']}|{ev['ts']}|{ev['kind']}|{body}|{prev}".encode()
            ).hexdigest()
            if ev["seq"] != i or ev["prev_hash"] != prev or ev["event_hash"] != h:
                return {"ok": False, "failed_seq": ev["seq"]}
            prev = h
        return {"ok": True, "events": len(self.events), "head_hash": prev}
