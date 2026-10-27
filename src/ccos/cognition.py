from dataclasses import dataclass
from .models import Plan

@dataclass
class Hypothesis:
    text: str
    method: str
    novelty: float
    coherence: float
    utility: float

class IntuitionEngine:
    """Divergent-search generator. Candidates are hypotheses, not facts."""
    def generate(self, problem: str, memories: list[str]) -> list[Hypothesis]:
        p = problem.strip()
        if not p:
            return []
        candidates = [
            Hypothesis(f"Use an analogy to reframe: {p}", "analogy", 0.65, 0.7, 0.6),
            Hypothesis(f"Try the inverse of the usual approach to: {p}", "inversion", 0.8, 0.55, 0.5),
            Hypothesis(f"Combine the problem with a related past event: {memories[0] if memories else 'no matching memory'}", "cross_domain_transfer", 0.75, 0.65, 0.55),
            Hypothesis(f"Identify a contradiction or hidden assumption in: {p}", "contradiction_search", 0.7, 0.8, 0.7),
        ]
        return sorted(candidates, key=lambda h: h.novelty * h.coherence * h.utility, reverse=True)

class NoveltyEngine:
    def score(self, novelty: float, coherence: float, utility: float) -> float:
        vals = [max(0.0, min(1.0, float(v))) for v in (novelty, coherence, utility)]
        return vals[0] * vals[1] * vals[2]

class ReflectivePlanner:
    def plan(self, goal: str, context: list[str] | None = None) -> Plan:
        context = context or []
        steps = [
            f"Clarify success criteria for: {goal}",
            "Retrieve relevant memories and world facts",
            "Generate at least two candidate strategies",
            "Check feasibility, uncertainty, and possible harm",
            "Choose a reversible first action and evaluate the result",
        ]
        rationale = f"Template plan based on {len(context)} context item(s); no external LLM is invoked."
        return Plan(goal=goal, steps=steps, rationale=rationale, estimated_risk=0.2, score=0.5)
