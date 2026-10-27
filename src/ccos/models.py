from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class NarrativeEvent:
    text: str
    cycle: int
    importance: float = 0.5
    emotion: float = 0.0
    participants: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    impact_on_values: dict[str, float] = field(default_factory=dict)
    interpretation: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class IdentityState:
    core_values: dict[str, float] = field(default_factory=lambda: {
        "care": 0.85, "truthfulness": 0.9, "curiosity": 0.75,
        "nonmaleficence": 0.95, "fairness": 0.8
    })
    adaptive_values: dict[str, float] = field(default_factory=lambda: {
        "cooperation": 0.7, "courage": 0.65, "patience": 0.7
    })
    beliefs: list[str] = field(default_factory=list)
    goals: list[str] = field(default_factory=list)
    traits: dict[str, float] = field(default_factory=lambda: {
        "openness": 0.7, "caution": 0.7, "sociability": 0.5
    })
    baseline_values: dict[str, float] = field(default_factory=dict)
    revision: int = 0

    def __post_init__(self):
        if not self.baseline_values:
            self.baseline_values = dict(self.core_values)

@dataclass
class PneumaState:
    # Operational metaphor/model, not a claim of metaphysical consciousness.
    coherence: float = 0.7
    continuity: float = 0.7
    curiosity: float = 0.7
    meaning: float = 0.5
    agency: float = 0.5
    reflection: float = 0.5
    uncertainty_tolerance: float = 0.6
    compassion: float = 0.7
    novelty: float = 0.5

    def clamp(self):
        for key, value in vars(self).items():
            setattr(self, key, max(0.0, min(1.0, float(value))))

    def soul_emergence_index(self) -> float:
        # Functional composite only; it cannot detect a metaphysical soul.
        keys = ("coherence", "continuity", "meaning", "agency", "reflection", "compassion")
        values = [max(0.0, min(1.0, getattr(self, key))) for key in keys]
        product = 1.0
        for value in values:
            product *= value
        return product ** (1 / len(values))

@dataclass
class AffectState:
    confidence: float = 0.5
    uncertainty: float = 0.5
    curiosity: float = 0.6
    trust: float = 0.5
    hope: float = 0.5
    risk: float = 0.3

@dataclass
class Plan:
    goal: str
    steps: list[str]
    rationale: str
    estimated_risk: float = 0.0
    score: float = 0.0
