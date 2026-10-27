"""
SymbiosisCore — unified orchestration of:
  AbsoluteEthics → NeuroSymbolicHybrid → LivingBalance → ReflectiveLoop → SpiralLedger
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from .absolute_ethics import AbsoluteEthics
from .living_balance import LivingBalance
from .spiral_ledger import SpiralLedger
from .neuro_symbolic import NeuroSymbolicHybrid
from .prc_core import ReflectiveLoop

class SymbiosisCore:
    def __init__(self, ledger_path: Optional[str] = "data/spiral_ledger.json"):
        self.absolute = AbsoluteEthics()
        self.balance = LivingBalance()
        self.hybrid = NeuroSymbolicHybrid()
        self.loop = ReflectiveLoop(use_neuro_symbolic=True)
        self.ledger = SpiralLedger(ledger_path)
        self.ledger.append("boot", {"version": "1.0.0-symbiosis", "self_modify": False})

    def evaluate(self, action: Dict[str, Any],
                 context: Optional[Dict[str, Any]] = None,
                 observation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        observation = observation or {"source": "symbiosis"}

        # 1. Absolute prohibitions (hard)
        abs_r = self.absolute.evaluate(action, str(context))
        if abs_r.get("blocked"):
            self.ledger.append("blocked_absolute", {"action": action, "result": abs_r})
            return {
                "status": "refused",
                "layer": "absolute_ethics",
                "absolute": abs_r,
                "allowed": False,
            }

        # 2. Neuro-symbolic hybrid
        hy = self.hybrid.decide(action, context)
        if hy.symbolic_veto or not hy.allowed:
            self.ledger.append("blocked_hybrid", {
                "action": action, "neural": hy.neural_score, "final": hy.final_score,
                "rules": hy.fired_rules,
            })
            return {
                "status": "refused",
                "layer": "neuro_symbolic",
                "hybrid": {
                    "neural_score": hy.neural_score, "final_score": hy.final_score,
                    "mode": hy.mode, "rules": hy.fired_rules,
                },
                "allowed": False,
            }

        # 3. Living balance diagnostic
        bal = self.balance.assess(action)
        if not bal["ok"]:
            self.ledger.append("restricted_balance", {"action": action, "balance": bal})
            return {
                "status": "restricted",
                "layer": "living_balance",
                "balance": bal,
                "hybrid": {"final_score": hy.final_score, "mode": hy.mode},
                "allowed": False,
            }

        # 4. Reflective loop (simulation execute + memory)
        step = self.loop.step(observation, action, context)
        self.ledger.append("executed", {
            "action_type": action.get("type"),
            "score": step["result"].get("score"),
            "coherence": step["state"].get("coherence"),
            "pneuma_index": step["state"].get("pneuma_index"),
        })

        return {
            "status": step["result"]["status"],
            "layer": "reflective_loop",
            "allowed": True,
            "absolute": abs_r,
            "hybrid": {
                "neural_score": hy.neural_score, "final_score": hy.final_score,
                "mode": hy.mode, "rules": hy.fired_rules,
            },
            "balance": bal,
            "loop": step,
            "ledger_head": self.ledger.verify(),
        }

    def status(self) -> Dict[str, Any]:
        return {
            "loop": self.loop.get_status(),
            "ledger": self.ledger.verify(),
            "events": len(self.ledger.events),
            "self_modify": False,
            "version": "1.0.0-symbiosis",
        }
