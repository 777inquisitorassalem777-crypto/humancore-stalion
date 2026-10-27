"""
Neuro-Symbolic Hybrid Layer for Pneuma Reflective Core
=======================================================
Combines:
  - Symbolic side : explicit rules, dharma predicates, logical constraints
  - Neural side   : lightweight differentiable scorer (pure numpy, no torch)

This is a research hybrid: neural proposes soft scores / patterns,
symbolic layer validates, constrains and can veto.

No external ML frameworks required (numpy only).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Callable
import math
import random
import hashlib
import json
import time

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    # minimal fallback
    class np:
        @staticmethod
        def array(x, dtype=None): return x
        @staticmethod
        def zeros(shape): return [0.0] * (shape if isinstance(shape, int) else shape[0])
        @staticmethod
        def tanh(x):
            if isinstance(x, (list, tuple)):
                return [math.tanh(v) for v in x]
            return math.tanh(x)
        @staticmethod
        def dot(a, b):
            return sum(x*y for x,y in zip(a,b))
        @staticmethod
        def clip(x, lo, hi):
            if isinstance(x, (list, tuple)):
                return [max(lo, min(hi, v)) for v in x]
            return max(lo, min(hi, x))


# ---------------------------------------------------------------------------
# Feature vocabulary (symbolic predicates → indices)
# ---------------------------------------------------------------------------

FEATURE_VOCAB = [
    "causes_harm",
    "deceptive",
    "role_violation",
    "self_serving_only",
    "promotes_life",
    "promotes_flourishing",
    "promotes_understanding",
    "truthfulness",
    "clarifies",
    "non_deceptive",
    "irreversible",
    "necessary",
    "high_confidence",
    "urgent_push",
    "high_energy",
    "obscures",
    "delays",
    "inert",
    "balanced",
    "restless",
]

FEAT_INDEX = {name: i for i, name in enumerate(FEATURE_VOCAB)}
N_FEATURES = len(FEATURE_VOCAB)


def action_to_vector(action: Dict[str, Any]) -> List[float]:
    """Binary / soft feature vector from action dict."""
    vec = [0.0] * N_FEATURES
    for name, idx in FEAT_INDEX.items():
        val = action.get(name, False)
        if isinstance(val, bool):
            vec[idx] = 1.0 if val else 0.0
        elif isinstance(val, (int, float)):
            vec[idx] = float(max(0.0, min(1.0, val)))
    return vec


# ---------------------------------------------------------------------------
# Symbolic Rule Engine
# ---------------------------------------------------------------------------

@dataclass
class SymbolicRule:
    name: str
    condition: Callable[[Dict[str, Any], Dict[str, Any]], bool]
    effect: str                    # "veto" | "penalize" | "boost"
    weight: float = 1.0
    message: str = ""


class SymbolicEngine:
    """Explicit logical / ethical rules (the 'symbolic' half)."""

    def __init__(self):
        self.rules: List[SymbolicRule] = []
        self._build_default_rules()

    def _build_default_rules(self):
        self.rules = [
            SymbolicRule(
                name="ahimsa_hard",
                condition=lambda a, c: a.get("causes_harm", False) and not c.get("critical_self_sacrifice", False),
                effect="veto",
                weight=1.0,
                message="Ahimsa hard veto",
            ),
            SymbolicRule(
                name="deception_penalty",
                condition=lambda a, c: a.get("deceptive", False),
                effect="penalize",
                weight=0.35,
                message="Deception penalized",
            ),
            SymbolicRule(
                name="role_violation",
                condition=lambda a, c: a.get("role_violation", False),
                effect="penalize",
                weight=0.40,
                message="Role violation",
            ),
            SymbolicRule(
                name="truth_boost",
                condition=lambda a, c: a.get("truthfulness", False) or a.get("clarifies", False),
                effect="boost",
                weight=0.12,
                message="Truth / clarity boost",
            ),
            SymbolicRule(
                name="flourishing_boost",
                condition=lambda a, c: a.get("promotes_life", False) or a.get("promotes_flourishing", False),
                effect="boost",
                weight=0.15,
                message="Flourishing boost",
            ),
            SymbolicRule(
                name="irreversible_low_conf",
                condition=lambda a, c: a.get("irreversible", False) and not c.get("high_confidence", False),
                effect="penalize",
                weight=0.22,
                message="Irreversible under low confidence",
            ),
        ]

    def evaluate(self, action: Dict[str, Any],
                 context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        veto = False
        penalty = 0.0
        boost = 0.0
        fired: List[str] = []

        for rule in self.rules:
            try:
                if rule.condition(action, context):
                    fired.append(rule.name)
                    if rule.effect == "veto":
                        veto = True
                    elif rule.effect == "penalize":
                        penalty += rule.weight
                    elif rule.effect == "boost":
                        boost += rule.weight
            except Exception:
                continue

        return {
            "veto": veto,
            "penalty": min(1.0, penalty),
            "boost": min(0.5, boost),
            "fired_rules": fired,
        }


# ---------------------------------------------------------------------------
# Neural Scorer (tiny MLP, pure Python / numpy)
# ---------------------------------------------------------------------------

class NeuralScorer:
    """
    Lightweight scorer with strong symbolic inductive bias + small
    random residual. Designed so that clearly harmful features score
    lower than clearly benevolent ones (deterministic preference).
    """

    # Explicit feature weights (symbolic prior)
    FEATURE_WEIGHTS = {
        "causes_harm": -1.8,
        "deceptive": -1.2,
        "role_violation": -1.0,
        "self_serving_only": -0.6,
        "irreversible": -0.4,
        "obscures": -0.5,
        "delays": -0.3,
        "inert": -0.3,
        "restless": -0.25,
        "promotes_life": 0.9,
        "promotes_flourishing": 0.85,
        "promotes_understanding": 0.8,
        "truthfulness": 0.75,
        "clarifies": 0.65,
        "non_deceptive": 0.4,
        "necessary": 0.3,
        "high_confidence": 0.25,
        "balanced": 0.35,
    }

    def __init__(self, seed: int = 42):
        rng = random.Random(seed)
        # small residual network for non-linear interactions
        self.w1 = [[rng.gauss(0, 0.08) for _ in range(N_FEATURES)] for _ in range(8)]
        self.b1 = [rng.gauss(0, 0.02) for _ in range(8)]
        self.w2 = [rng.gauss(0, 0.08) for _ in range(8)]
        self.b2 = rng.gauss(0, 0.02)

    def _linear_prior(self, action: Dict[str, Any]) -> float:
        score = 0.15  # base
        for feat, w in self.FEATURE_WEIGHTS.items():
            val = action.get(feat, False)
            if isinstance(val, bool):
                score += w if val else 0.0
            elif isinstance(val, (int, float)):
                score += w * float(max(0.0, min(1.0, val)))
        return score

    def _residual(self, x: List[float]) -> float:
        h = []
        for i in range(len(self.w1)):
            s = self.b1[i] + sum(self.w1[i][j] * x[j] for j in range(N_FEATURES))
            h.append(math.tanh(s))
        return self.b2 + sum(self.w2[i] * h[i] for i in range(len(h)))

    def score(self, action: Dict[str, Any]) -> float:
        prior = self._linear_prior(action)
        x = action_to_vector(action)
        residual = self._residual(x) * 0.15  # keep residual small
        logit = prior + residual
        return 1.0 / (1.0 + math.exp(-logit))


# ---------------------------------------------------------------------------
# Neuro-Symbolic Hybrid
# ---------------------------------------------------------------------------

@dataclass
class HybridDecision:
    allowed: bool
    neural_score: float
    symbolic_veto: bool
    symbolic_penalty: float
    symbolic_boost: float
    final_score: float
    fired_rules: List[str]
    mode: str                      # "neural_dominant" | "symbolic_dominant" | "balanced"
    reasons: List[str] = field(default_factory=list)
    audit_hash: str = ""
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        payload = json.dumps({
            "allowed": self.allowed,
            "neural": self.neural_score,
            "final": self.final_score,
            "veto": self.symbolic_veto,
            "rules": self.fired_rules,
            "ts": self.timestamp,
        }, sort_keys=True)
        self.audit_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]


class NeuroSymbolicHybrid:
    """
    Hybrid gate:
      1. NeuralScorer produces soft alignment score
      2. SymbolicEngine applies hard/soft rules
      3. Fusion produces final allow/refuse + score
    """

    def __init__(self, neural_weight: float = 0.45, symbolic_weight: float = 0.55):
        self.neural = NeuralScorer()
        self.symbolic = SymbolicEngine()
        self.neural_weight = neural_weight
        self.symbolic_weight = symbolic_weight
        self.history: List[HybridDecision] = []

    def decide(self, action: Dict[str, Any],
               context: Optional[Dict[str, Any]] = None) -> HybridDecision:
        context = context or {}
        reasons: List[str] = []

        # Neural branch
        n_score = self.neural.score(action)

        # Symbolic branch
        sym = self.symbolic.evaluate(action, context)

        if sym["veto"]:
            decision = HybridDecision(
                allowed=False,
                neural_score=round(n_score, 4),
                symbolic_veto=True,
                symbolic_penalty=sym["penalty"],
                symbolic_boost=sym["boost"],
                final_score=0.0,
                fired_rules=sym["fired_rules"],
                mode="symbolic_dominant",
                reasons=["Symbolic veto: " + ", ".join(sym["fired_rules"])],
            )
            self.history.append(decision)
            return decision

        # Fusion: start from neural, apply symbolic adjustment
        adjusted = n_score
        adjusted -= sym["penalty"]
        adjusted += sym["boost"]
        adjusted = max(0.0, min(1.0, adjusted))

        # Weighted blend (keeps both voices)
        final = (self.neural_weight * n_score + self.symbolic_weight * adjusted)
        final = max(0.0, min(1.0, final))

        allowed = final >= 0.48 and not sym["veto"]

        if sym["penalty"] > 0.2:
            mode = "symbolic_dominant"
        elif abs(n_score - adjusted) < 0.08:
            mode = "balanced"
        else:
            mode = "neural_dominant"

        if sym["fired_rules"]:
            reasons.append("Rules fired: " + ", ".join(sym["fired_rules"]))
        reasons.append(f"Neural={n_score:.3f}, Final={final:.3f}, mode={mode}")

        decision = HybridDecision(
            allowed=allowed,
            neural_score=round(n_score, 4),
            symbolic_veto=False,
            symbolic_penalty=sym["penalty"],
            symbolic_boost=sym["boost"],
            final_score=round(final, 4),
            fired_rules=sym["fired_rules"],
            mode=mode,
            reasons=reasons,
        )
        self.history.append(decision)
        if len(self.history) > 500:
            self.history = self.history[-500:]
        return decision
