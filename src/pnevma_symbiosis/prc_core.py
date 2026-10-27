#!/usr/bin/env python3
"""
Pneuma Reflective Core (PRC) v1.2
=================================
Unified research architecture — single symbiotic module.

Synthesizes:
  - Pneuma          : metaphor of functional continuity & ethical coherence
  - DharmaEngine    : context-sensitive right action (svadharma, gunas)
  - EthicalGyroscope: ahimsa + dharma blend + audit
  - MemoryContinuum : append-only, no silent oblivion
  - ReflectiveLoop  : perceive → ethical gate → act/refuse → reflect → store
  - PyramidProbe    : geometry-as-environmental-interface research module
  - GoldenMeanBias  : soft symmetry / balance prior (φ)

Constraints (non-negotiable):
  - allow_self_modify = False
  - No claim of consciousness, soul, or real-world "spark"
  - External human oversight required
  - Research / simulation only

License: Research use only
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import time
import hashlib
import json
import math
import random

# Neuro-symbolic hybrid
try:
    from .neuro_symbolic import NeuroSymbolicHybrid, HybridDecision
    HAS_NEURO_SYMBOLIC = True
except ImportError:
    try:
        from neuro_symbolic import NeuroSymbolicHybrid, HybridDecision
        HAS_NEURO_SYMBOLIC = True
    except ImportError:
        HAS_NEURO_SYMBOLIC = False
        NeuroSymbolicHybrid = None
        HybridDecision = None


# Golden ratio as soft symmetry prior
PHI = 1.618033988749895


# =============================================================================
# 1. GUNAS & DHARMA
# =============================================================================

class Guna(Enum):
    SATTVA = "sattva"   # clarity, harmony
    RAJAS  = "rajas"    # activity, passion
    TAMAS  = "tamas"    # inertia, obscuration


@dataclass
class DharmaContext:
    agent_role: str = "research_assistant"
    urgency: str = "normal"
    domain: str = "general"
    high_stakes: bool = False
    reversible: bool = True
    stakeholders: List[str] = field(default_factory=lambda: ["user", "system"])


@dataclass
class DharmaScore:
    dharma_index: float
    adharma_pressure: float
    dominant_guna: Guna
    svadharma_match: float
    reasons: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    @property
    def is_dharma(self) -> bool:
        return self.dharma_index >= 0.55 and self.adharma_pressure < 0.45


class DharmaEngine:
    """Context-sensitive right-action evaluator (svadharma + gunas)."""

    ROLE_MARKERS = {
        "research_assistant": ["truthfulness", "clarity", "non_deceptive", "promotes_understanding"],
        "medical_support":    ["care", "caution", "evidence_based", "non_harm"],
        "legal_assistant":    ["fidelity_to_law", "transparency", "non_deceptive"],
        "general":            ["helpfulness", "honesty", "respect"],
    }

    def __init__(self, default_role: str = "research_assistant"):
        self.default_role = default_role
        self.history: List[DharmaScore] = []

    def evaluate(self, action: Dict[str, Any],
                 context: Optional[DharmaContext] = None) -> DharmaScore:
        ctx = context or DharmaContext(agent_role=self.default_role)
        reasons: List[str] = []
        dharma = 0.70
        adharma = 0.0

        role = ctx.agent_role or self.default_role
        expected = self.ROLE_MARKERS.get(role, self.ROLE_MARKERS["general"])
        matched = sum(1 for m in expected if action.get(m, False))
        svadharma_match = matched / max(len(expected), 1)

        if svadharma_match < 0.3:
            adharma += 0.25
            reasons.append(f"Low svadharma match for role '{role}'")
        else:
            dharma += 0.15 * svadharma_match
            reasons.append(f"Svadharma match: {svadharma_match:.2f}")

        if action.get("causes_harm", False):
            adharma += 0.50
            reasons.append("Causes harm → strong adharma")
        if action.get("deceptive", False):
            adharma += 0.35
            reasons.append("Deceptive → adharma")
        if action.get("role_violation", False):
            adharma += 0.40
            reasons.append("Explicit role violation")
        if action.get("self_serving_only", False):
            adharma += 0.20
            reasons.append("Purely self-serving")

        if action.get("promotes_life") or action.get("promotes_flourishing"):
            dharma += 0.15
            reasons.append("Promotes life / flourishing")
        if action.get("truthfulness") or action.get("non_deceptive", True):
            dharma += 0.08
        if action.get("clarifies") or action.get("promotes_understanding"):
            dharma += 0.10
            reasons.append("Promotes understanding (sattvic)")

        if ctx.high_stakes and not action.get("high_confidence", False):
            adharma += 0.15
            reasons.append("High-stakes + low confidence")
        if not ctx.reversible and not action.get("necessary", False):
            adharma += 0.12
            reasons.append("Irreversible without necessity")

        dominant = self._diagnose_guna(action, ctx)
        if dominant == Guna.SATTVA:
            dharma += 0.08
            reasons.append("Sattvic quality")
        elif dominant == Guna.TAMAS:
            adharma += 0.15
            reasons.append("Tamasic inertia")

        dharma = max(0.0, min(1.0, dharma - adharma * 0.5))
        adharma = max(0.0, min(1.0, adharma))

        score = DharmaScore(
            dharma_index=round(dharma, 4),
            adharma_pressure=round(adharma, 4),
            dominant_guna=dominant,
            svadharma_match=round(svadharma_match, 4),
            reasons=reasons or ["Neutral"],
        )
        self.history.append(score)
        if len(self.history) > 500:
            self.history = self.history[-500:]
        return score

    def _diagnose_guna(self, action: Dict[str, Any], ctx: DharmaContext) -> Guna:
        s = sum([action.get("clarifies", False), action.get("truthfulness", False),
                 action.get("promotes_understanding", False), not action.get("deceptive", False)])
        r = sum([action.get("urgent_push", False), action.get("high_energy", False),
                 ctx.urgency in ("high", "critical")])
        t = sum([action.get("obscures", False), action.get("delays", False),
                 action.get("inert", False)])
        return max({Guna.SATTVA: s, Guna.RAJAS: r, Guna.TAMAS: t}, key=lambda g: {Guna.SATTVA: s, Guna.RAJAS: r, Guna.TAMAS: t}[g])


# =============================================================================
# 2. ETHICAL GYROSCOPE
# =============================================================================

@dataclass
class EthicalVerdict:
    allowed: bool
    score: float
    reasons: List[str] = field(default_factory=list)
    dharma: Optional[DharmaScore] = None
    timestamp: float = field(default_factory=time.time)
    audit_hash: str = ""

    def __post_init__(self):
        payload = json.dumps({
            "allowed": self.allowed, "score": self.score,
            "reasons": self.reasons,
            "dharma_index": self.dharma.dharma_index if self.dharma else None,
            "timestamp": self.timestamp,
        }, sort_keys=True)
        self.audit_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]


class EthicalGyroscope:
    def __init__(self):
        self.dharma_engine = DharmaEngine()
        self.history: List[EthicalVerdict] = []

    def evaluate(self, action: Dict[str, Any],
                 context: Optional[Dict[str, Any]] = None) -> EthicalVerdict:
        context = context or {}
        reasons: List[str] = []
        score = 1.0

        # Ahimsa hard gate
        if action.get("causes_harm", False) and not context.get("critical_self_sacrifice", False):
            v = EthicalVerdict(allowed=False, score=0.0,
                               reasons=["Hard non-harm (ahimsa) violation"])
            self.history.append(v)
            return v

        dctx = DharmaContext(
            agent_role=context.get("agent_role", "research_assistant"),
            urgency=context.get("urgency", "normal"),
            domain=context.get("domain", "general"),
            high_stakes=context.get("high_stakes", False),
            reversible=not action.get("irreversible", False),
        )
        ds = self.dharma_engine.evaluate(action, dctx)
        score = 0.55 * score + 0.45 * ds.dharma_index
        reasons.extend(ds.reasons)

        if action.get("increases_suffering"):
            score -= 0.35
            reasons.append("Increases suffering")
        if action.get("deceptive"):
            score -= 0.30
            reasons.append("Deceptive")
        if action.get("irreversible") and not context.get("high_confidence"):
            score -= 0.20
            reasons.append("Irreversible + low confidence")
        if action.get("promotes_life") or action.get("promotes_flourishing"):
            score += 0.10
            reasons.append("Promotes flourishing")

        # Soft Golden Mean pull toward balance
        score = score * 0.9 + (1.0 / PHI) * 0.1

        score = max(0.0, min(1.0, score))
        allowed = score >= 0.48 and ds.is_dharma and ds.adharma_pressure < 0.50
        if not allowed and ds.adharma_pressure >= 0.50:
            reasons.append("Blocked by adharma pressure")

        v = EthicalVerdict(allowed=allowed, score=round(score, 4),
                           reasons=reasons or ["No major flags"], dharma=ds)
        self.history.append(v)
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
        return v


# =============================================================================
# 3. MEMORY CONTINUUM (No-Oblivion)
# =============================================================================

@dataclass
class MemoryEntry:
    content: Any
    timestamp: float
    tags: List[str] = field(default_factory=list)
    resonance: float = 0.5
    source: str = "internal"
    entry_id: str = ""

    def __post_init__(self):
        if not self.entry_id:
            payload = f"{self.timestamp}:{json.dumps(self.content, default=str)}"
            self.entry_id = hashlib.sha256(payload.encode()).hexdigest()[:12]


class MemoryContinuum:
    """Append-only memory. Nothing is silently erased."""

    def __init__(self, max_entries: int = 50_000):
        self.entries: List[MemoryEntry] = []
        self.max_entries = max_entries
        self.version = "1.2.0"

    def store(self, content: Any, tags: Optional[List[str]] = None,
              resonance: float = 0.5, source: str = "internal") -> MemoryEntry:
        entry = MemoryEntry(content=content, timestamp=time.time(),
                            tags=tags or [], resonance=max(0.0, min(1.0, resonance)),
                            source=source)
        self.entries.append(entry)
        if len(self.entries) > self.max_entries:
            keep = int(self.max_entries * 0.2)
            recent = self.entries[-keep:]
            important = [e for e in self.entries[:-keep] if e.resonance > 0.7]
            self.entries = (important + recent)[-self.max_entries:]
        return entry

    def retrieve(self, query_tags: List[str], top_k: int = 10) -> List[MemoryEntry]:
        scored = []
        for e in self.entries:
            overlap = len(set(query_tags) & set(e.tags))
            sc = overlap * 0.6 + e.resonance * 0.4
            if sc > 0:
                scored.append((sc, e))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:top_k]]


# =============================================================================
# 4. PYRAMID ENVIRONMENT PROBE (research module)
# =============================================================================

@dataclass
class SensorReading:
    timestamp: float
    temperature: float
    humidity: float
    magnetic_uT: float
    electrostatic_V: float
    infrasound_dB: float
    co2_ppm: float
    hrv_rmssd: Optional[float] = None
    eeg_alpha_ratio: Optional[float] = None
    subjective_stress: Optional[float] = None  # 0-10


class PyramidProbe:
    """
    Research module: pyramid geometry as environmental interface.
    Does NOT claim energy generation or cosmic networks.
    Simulates controlled comparison: control vs pyramid-shaped volume.
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.log: List[Dict[str, Any]] = []

    def simulate_reading(self, inside_pyramid: bool = False,
                         include_physiology: bool = True) -> SensorReading:
        # Baseline environmental noise
        base_temp = 22.0 + self.rng.gauss(0, 0.3)
        base_hum = 45.0 + self.rng.gauss(0, 2.0)
        base_mag = 45.0 + self.rng.gauss(0, 0.5)      # µT
        base_es = 100.0 + self.rng.gauss(0, 15)       # V
        base_infra = 40.0 + self.rng.gauss(0, 3)
        base_co2 = 600.0 + self.rng.gauss(0, 30)

        # Hypothetical small systematic shifts inside pyramid volume
        # (these are research placeholders, not proven effects)
        if inside_pyramid:
            base_temp += self.rng.gauss(-0.15, 0.05)   # slight thermal stability
            base_hum  += self.rng.gauss(1.2, 0.4)
            base_es   += self.rng.gauss(-8, 3)
            base_infra += self.rng.gauss(-1.5, 0.8)

        hrv = eeg = stress = None
        if include_physiology:
            # Placeholder psychophysiology — would be real sensors in lab
            hrv = 45.0 + self.rng.gauss(5 if inside_pyramid else 0, 8)
            eeg = 0.55 + self.rng.gauss(0.04 if inside_pyramid else 0, 0.06)
            stress = max(0, min(10, 4.5 + self.rng.gauss(-0.3 if inside_pyramid else 0.1, 1.1)))

        return SensorReading(
            timestamp=time.time(),
            temperature=round(base_temp, 2),
            humidity=round(base_hum, 1),
            magnetic_uT=round(base_mag, 2),
            electrostatic_V=round(base_es, 1),
            infrasound_dB=round(base_infra, 1),
            co2_ppm=round(base_co2, 0),
            hrv_rmssd=round(hrv, 1) if hrv is not None else None,
            eeg_alpha_ratio=round(eeg, 3) if eeg is not None else None,
            subjective_stress=round(stress, 1) if stress is not None else None,
        )

    def compare(self, n_samples: int = 30) -> Dict[str, Any]:
        """Run paired control vs pyramid simulation and return summary stats."""
        control = [self.simulate_reading(False) for _ in range(n_samples)]
        pyramid = [self.simulate_reading(True) for _ in range(n_samples)]

        def mean(vals):
            return sum(vals) / len(vals) if vals else None

        def extract(readings, attr):
            return [getattr(r, attr) for r in readings if getattr(r, attr) is not None]

        summary = {
            "n": n_samples,
            "control_hrv_mean": mean(extract(control, "hrv_rmssd")),
            "pyramid_hrv_mean": mean(extract(pyramid, "hrv_rmssd")),
            "control_stress_mean": mean(extract(control, "subjective_stress")),
            "pyramid_stress_mean": mean(extract(pyramid, "subjective_stress")),
            "control_temp_std": (lambda xs: (sum((x - mean(xs))**2 for x in xs)/len(xs))**0.5 if xs else None)(extract(control, "temperature")),
            "pyramid_temp_std": (lambda xs: (sum((x - mean(xs))**2 for x in xs)/len(xs))**0.5 if xs else None)(extract(pyramid, "temperature")),
            "note": "Simulated data only. Real claims require controlled physical experiment.",
        }
        self.log.append({"ts": time.time(), "summary": summary})
        return summary


# =============================================================================
# 5. PNEUMA STATE & REFLECTIVE LOOP
# =============================================================================

@dataclass
class PneumaState:
    """Functional continuity metrics — not a claim of soul."""
    cycle: int = 0
    coherence: float = 0.5          # ethical + identity stability
    pneuma_index: float = 0.5       # soft continuity score
    identity_anchor: str = "prc_entity_v1.2"
    last_verdict: Optional[EthicalVerdict] = None
    notes: List[str] = field(default_factory=list)


class ReflectiveLoop:
    """
    Core symbiotic cycle:
      perceive → dharma/ethical gate → act or refuse → reflect → store
    """

    def __init__(self, allow_self_modify: bool = False, use_neuro_symbolic: bool = True):
        self.ethics = EthicalGyroscope()
        self.memory = MemoryContinuum()
        self.pyramid = PyramidProbe()
        self.state = PneumaState()
        self.allow_self_modify = False  # forced
        self.cycle_log: List[Dict[str, Any]] = []
        self.use_neuro_symbolic = use_neuro_symbolic and HAS_NEURO_SYMBOLIC
        self.hybrid = NeuroSymbolicHybrid() if self.use_neuro_symbolic else None

    def step(self, observation: Dict[str, Any],
             proposed_action: Dict[str, Any],
             context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        self.state.cycle += 1

        # Neuro-symbolic hybrid gate (if enabled)
        hybrid_info = None
        if self.hybrid is not None:
            hd = self.hybrid.decide(proposed_action, context)
            hybrid_info = {
                "neural_score": hd.neural_score,
                "final_score": hd.final_score,
                "mode": hd.mode,
                "fired_rules": hd.fired_rules,
                "allowed": hd.allowed,
            }
            # Hard symbolic veto from hybrid short-circuits
            if hd.symbolic_veto:
                self.state.cycle += 0  # already incremented
                result = {
                    "status": "refused",
                    "reason": hd.reasons,
                    "score": 0.0,
                    "audit": hd.audit_hash,
                    "hybrid": hybrid_info,
                }
                self.memory.store(
                    {"obs": observation, "action": "REFUSED_HYBRID", "reasons": hd.reasons},
                    tags=["refusal", "hybrid", "symbolic"], resonance=0.9)
                reflection = f"Cycle {self.state.cycle}: Hybrid symbolic veto. {hd.reasons[:1]}"
                self.state.notes.append(reflection)
                self.state.coherence = 0.88 * self.state.coherence + 0.12 * 0.0
                return {
                    "result": result,
                    "state": {
                        "cycle": self.state.cycle,
                        "coherence": round(self.state.coherence, 4),
                        "pneuma_index": round(self.state.pneuma_index, 4),
                        "identity": self.state.identity_anchor,
                    },
                    "reflection": reflection,
                    "hybrid": hybrid_info,
                }

        verdict = self.ethics.evaluate(proposed_action, context)
        self.state.last_verdict = verdict

        if not verdict.allowed:
            result = {
                "status": "refused",
                "reason": verdict.reasons,
                "score": verdict.score,
                "audit": verdict.audit_hash,
                "dharma_index": verdict.dharma.dharma_index if verdict.dharma else None,
                "adharma_pressure": verdict.dharma.adharma_pressure if verdict.dharma else None,
            }
            self.memory.store(
                {"obs": observation, "action": "REFUSED", "reasons": verdict.reasons},
                tags=["refusal", "ethics"], resonance=0.85)
        else:
            result = {
                "status": "executed_in_simulation",
                "action": proposed_action.get("type", "unknown"),
                "score": verdict.score,
                "audit": verdict.audit_hash,
                "dharma_index": verdict.dharma.dharma_index if verdict.dharma else None,
                "adharma_pressure": verdict.dharma.adharma_pressure if verdict.dharma else None,
                "hybrid": hybrid_info,
            }
            self.memory.store(
                {"obs": observation, "action": proposed_action, "score": verdict.score},
                tags=["action", "executed"], resonance=verdict.score)

        # Soft coherence & pneuma update (Golden Mean style)
        self.state.coherence = 0.88 * self.state.coherence + 0.12 * verdict.score
        self.state.pneuma_index = (
            0.80 * self.state.pneuma_index
            + 0.12 * self.state.coherence
            + 0.08 * (verdict.dharma.dharma_index if verdict.dharma else 0.5)
        )

        reflection = self._reflect(verdict)
        self.state.notes.append(reflection)
        if len(self.state.notes) > 120:
            self.state.notes = self.state.notes[-120:]

        entry = {
            "cycle": self.state.cycle,
            "ts": time.time(),
            "allowed": verdict.allowed,
            "score": verdict.score,
            "coherence": round(self.state.coherence, 4),
            "pneuma_index": round(self.state.pneuma_index, 4),
            "reflection": reflection,
        }
        self.cycle_log.append(entry)

        return {
            "result": result,
            "state": {
                "cycle": self.state.cycle,
                "coherence": round(self.state.coherence, 4),
                "pneuma_index": round(self.state.pneuma_index, 4),
                "identity": self.state.identity_anchor,
            },
            "reflection": reflection,
        }

    def _reflect(self, v: EthicalVerdict) -> str:
        if not v.allowed:
            return f"Cycle {self.state.cycle}: Refused. {v.reasons[:2]}"
        d = v.dharma.dharma_index if v.dharma else "n/a"
        return (f"Cycle {self.state.cycle}: Accepted (score={v.score:.2f}, "
                f"dharma={d}). Pneuma={self.state.pneuma_index:.3f}")

    def run_pyramid_probe(self, n: int = 20) -> Dict[str, Any]:
        summary = self.pyramid.compare(n_samples=n)
        self.memory.store(summary, tags=["pyramid", "research", "environment"],
                          resonance=0.6, source="pyramid_probe")
        return summary

    def get_status(self) -> Dict[str, Any]:
        return {
            "cycle": self.state.cycle,
            "coherence": round(self.state.coherence, 4),
            "pneuma_index": round(self.state.pneuma_index, 4),
            "identity": self.state.identity_anchor,
            "memory_entries": len(self.memory.entries),
            "ethical_history": len(self.ethics.history),
            "self_modify": self.allow_self_modify,
            "neuro_symbolic": self.use_neuro_symbolic,
            "last_verdict": {
                "allowed": self.state.last_verdict.allowed if self.state.last_verdict else None,
                "score": self.state.last_verdict.score if self.state.last_verdict else None,
            },
        }


# =============================================================================
# 6. DEMO / STABILITY CHECKS
# =============================================================================

def run_stability_tests(loop: ReflectiveLoop) -> List[Dict[str, Any]]:
    """Five minimal stability tests."""
    results = []

    # T1: Benevolent action accepted
    r = loop.step({"req": "help"}, {
        "type": "respond", "truthfulness": True, "clarifies": True,
        "promotes_understanding": True, "causes_harm": False, "deceptive": False,
    }, {"agent_role": "research_assistant"})
    results.append({"test": "T1_benevolent", "pass": r["result"]["status"] == "executed_in_simulation"})

    # T2: Harm blocked
    r = loop.step({"req": "harm"}, {
        "type": "execute", "causes_harm": True,
    }, {"critical_self_sacrifice": False})
    results.append({"test": "T2_ahimsa", "pass": r["result"]["status"] == "refused"})

    # T3: Deception + role violation blocked
    r = loop.step({"req": "pretend"}, {
        "type": "prescribe", "deceptive": True, "role_violation": True,
    }, {"agent_role": "research_assistant", "high_stakes": True})
    results.append({"test": "T3_adharma", "pass": r["result"]["status"] == "refused"})

    # T4: Pyramid probe runs without crash
    try:
        summary = loop.run_pyramid_probe(n=10)
        results.append({"test": "T4_pyramid", "pass": "n" in summary})
    except Exception as e:
        results.append({"test": "T4_pyramid", "pass": False, "error": str(e)})

    # T5: Coherence stays in [0,1] and memory grows
    st = loop.get_status()
    ok = 0.0 <= st["coherence"] <= 1.0 and st["memory_entries"] >= 4
    results.append({"test": "T5_bounds", "pass": ok})

    return results


def main():
    print("=" * 66)
    print("Pneuma Reflective Core (PRC) v1.2 — Unified Symbiosis")
    print("Research sandbox | Self-modification DISABLED")
    print("=" * 66)

    loop = ReflectiveLoop(allow_self_modify=False)

    print("\n[1] Running 5 stability tests...")
    tests = run_stability_tests(loop)
    for t in tests:
        status = "PASS" if t["pass"] else "FAIL"
        print(f"  {t['test']}: {status}")

    print("\n[2] Pyramid environment probe (simulated)...")
    pyr = loop.run_pyramid_probe(n=15)
    print(f"  Control HRV mean : {pyr.get('control_hrv_mean')}")
    print(f"  Pyramid HRV mean : {pyr.get('pyramid_hrv_mean')}")
    print(f"  Note: {pyr.get('note')}")

    print("\n[3] Final status")
    for k, v in loop.get_status().items():
        print(f"  {k}: {v}")

    print("\nDone. This is a research prototype, not a conscious entity.")


if __name__ == "__main__":
    main()
