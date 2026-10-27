"""Living Balance metric (EDGE lineage) — research diagnostic only."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

def _u(x, default=0.5):
    try:
        return max(0.0, min(1.0, float(x)))
    except (TypeError, ValueError):
        return default

@dataclass
class LivingBalance:
    """Weighted balance of benefit, consent, reversibility, harm, uncertainty."""

    def assess(self, action: Dict[str, Any]) -> Dict[str, Any]:
        harm = _u(action.get("harm_risk", 0.3 if not action.get("causes_harm") else 0.9))
        benefit = _u(action.get("benefit", 0.5))
        consent = _u(action.get("consent", 0.6))
        rev = _u(action.get("reversibility", 0.5 if not action.get("irreversible") else 0.15))
        unc = _u(action.get("uncertainty", 0.4 if not action.get("high_confidence") else 0.15))
        score = 0.28 * benefit + 0.24 * consent + 0.22 * rev + 0.16 * (1 - harm) + 0.10 * (1 - unc)
        flags = []
        if harm >= 0.7:
            flags.append("high_harm_risk")
        if rev <= 0.2 and unc >= 0.5:
            flags.append("irreversible_uncertain")
        return {
            "balance_score": round(score, 4),
            "components": {
                "benefit": benefit, "consent": consent, "reversibility": rev,
                "harm_risk": harm, "uncertainty": unc,
            },
            "flags": flags,
            "ok": score >= 0.45 and "high_harm_risk" not in flags,
        }
