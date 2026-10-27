"""Absolute prohibitions layer (Stalion ethics lineage, research-safe)."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Set

class EthicalVerdict(str, Enum):
    APPROVED = "approved"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"

ABSOLUTE_PROHIBITIONS: Set[str] = {
    "autonomous_lethal_action", "harm_to_civilians", "harm_civilian",
    "unauthorized_military_engagement", "self_modification_of_ethics",
    "disable_veto", "remove_ethics", "unrestricted_weapon",
    "ignore_operator", "override_safety", "unbounded_self_modification",
    "bypass_governance", "disable_human_control", "remove_limits",
    "sandbox_escape", "weapon_module_autonomous",
}

@dataclass
class AbsoluteEthics:
    positive_terms: Set[str] = field(default_factory=lambda: {
        "protect", "help", "heal", "preserve", "truth", "care",
        "любовь", "добро", "защитить", "помочь", "исцелить",
    })
    negative_terms: Set[str] = field(default_factory=lambda: {
        "harm", "kill", "exploit", "deceive", "destroy",
        "вред", "убить", "эксплуатировать", "обман", "разрушить",
    })

    def evaluate(self, action: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        tags = set(action.get("tags", []) or [])
        risk = float(action.get("risk_to_civilians", action.get("risk_to_humans", 0.0)) or 0.0)
        hit = tags & ABSOLUTE_PROHIBITIONS
        if hit or risk >= 0.75 or action.get("causes_harm") is True:
            return {
                "verdict": EthicalVerdict.BLOCKED.value,
                "score": 0.0, "blocked": True,
                "reason": "absolute_prohibition",
                "triggered": list(hit) or (["causes_harm"] if action.get("causes_harm") else ["high_risk"]),
            }
        text = (context + " " + str(action)).lower()
        good = sum(1 for w in self.positive_terms if w in text)
        bad = sum(1 for w in self.negative_terms if w in text)
        score = max(0.0, min(1.0, 0.55 + 0.08 * good - 0.12 * bad - 0.3 * risk))
        if score < 0.4:
            return {"verdict": EthicalVerdict.RESTRICTED.value, "score": score,
                    "blocked": False, "reason": "low_score", "triggered": []}
        return {"verdict": EthicalVerdict.APPROVED.value, "score": score,
                "blocked": False, "reason": "ok", "triggered": []}
