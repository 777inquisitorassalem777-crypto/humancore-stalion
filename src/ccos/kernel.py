from .models import NarrativeEvent, PneumaState, AffectState
from .memory import NarrativeMemory
from .identity import IdentityEngine
from .ethics import EthicalGyroscope
from .world import WorldModel
from .cognition import IntuitionEngine, ReflectivePlanner, NoveltyEngine
from .culture import CultureEngine
from .evolution import EvolutionEngine

class CCOSKernel:
    def __init__(self):
        self.cycle = 0
        self.memory = NarrativeMemory()
        self.identity = IdentityEngine()
        self.pneuma = PneumaState()
        self.affect = AffectState()
        self.ethics = EthicalGyroscope()
        self.world = WorldModel()
        self.intuition = IntuitionEngine()
        self.planner = ReflectivePlanner()
        self.novelty = NoveltyEngine()
        self.culture = CultureEngine()
        self.evolution = EvolutionEngine()
        self.relationships: dict[str, dict[str, float]] = {}

    def remember(self, text: str, importance: float = 0.5, emotion: float = 0.0,
                 participants: list[str] | None = None, impact_on_values: dict[str, float] | None = None,
                 interpretation: str = "") -> dict:
        self.cycle += 1
        event = NarrativeEvent(
            text=text, cycle=self.cycle, importance=importance, emotion=emotion,
            participants=participants or [], impact_on_values=impact_on_values or {},
            interpretation=interpretation
        )
        self.memory.record(event)
        self.identity.observe_event(event)
        self.world.observe(text)
        self.pneuma.continuity = min(1.0, 0.5 + min(len(self.memory), 100) / 200.0)
        self.pneuma.meaning = min(1.0, 0.4 + importance * 0.4)
        self.pneuma.reflection = min(1.0, 0.4 + self.identity.state.revision * 0.02)
        self.pneuma.clamp()
        return event.to_dict()

    def process(self, text: str) -> dict:
        event = self.remember(text, importance=0.6)
        retrieved = self.memory.recall(text, self.cycle, limit=3)
        memories = [item.text for item, score in retrieved if score > 0]
        hypotheses = self.intuition.generate(text, memories)
        plan = self.planner.plan(f"Respond constructively to: {text}", memories)
        ethical = self.ethics.evaluate("respond to user", benefit=0.6, harm=0.05)
        reflection = (
            f"Stored event {event['id']}; retrieved {len(memories)} related memory item(s); "
            f"generated {len(hypotheses)} candidate hypotheses. "
            f"Ethical heuristic: {ethical.rationale}."
        )
        self.evolution.propose(
            description="Review whether this interaction suggests a reusable pattern",
            evidence=f"cycle={self.cycle}; input_length={len(text)}; memory_count={len(self.memory)}"
        )
        return {
            "cycle": self.cycle,
            "event": event,
            "retrieved_memories": [{"event": e.to_dict(), "score": round(s, 6)} for e, s in retrieved],
            "hypotheses": [vars(h) for h in hypotheses],
            "plan": vars(plan),
            "ethical_evaluation": vars(ethical),
            "reflection": reflection,
            "pneuma_state": vars(self.pneuma),
            "soul_emergence_index": round(self.pneuma.soul_emergence_index(), 6),
            "note": "Functional metrics only; not evidence of subjective consciousness."
        }

    def plan_for(self, goal: str) -> dict:
        memories = [e.text for e, score in self.memory.recall(goal, self.cycle, 5) if score > 0]
        return vars(self.planner.plan(goal, memories))

    def reflect(self, question: str) -> dict:
        memories = self.memory.recall(question, self.cycle, 5)
        hypotheses = self.intuition.generate(question, [e.text for e, _ in memories])
        return {
            "question": question,
            "relevant_memories": [{"text": e.text, "score": round(s, 5)} for e, s in memories],
            "hypotheses": [vars(h) for h in hypotheses],
            "identity_drift": self.identity.drift(),
            "caution": "Hypotheses are candidates and require evidence."
        }

    def biography(self) -> list[dict]:
        return [event.to_dict() for event in self.memory.recent(1000)]

    def status(self) -> dict:
        return {
            "cycle": self.cycle,
            "memory_size": len(self.memory),
            "identity_revision": self.identity.state.revision,
            "identity_drift": self.identity.drift(),
            "evolution_proposals": len(self.evolution.proposals),
            "culture_concepts": len(self.culture.concepts),
            "pneuma_state": vars(self.pneuma),
            "soul_emergence_index": round(self.pneuma.soul_emergence_index(), 6)
        }
