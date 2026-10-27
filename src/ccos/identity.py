from .models import IdentityState, NarrativeEvent

def normalized_distance(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    return sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in keys) / len(keys)

class IdentityEngine:
    def __init__(self, state: IdentityState | None = None):
        self.state = state or IdentityState()

    def observe_event(self, event: NarrativeEvent) -> None:
        # Core values are anchors; experience updates adaptive values, not safety invariants.
        changed = False
        for key, delta in event.impact_on_values.items():
            if key in self.state.adaptive_values:
                old = self.state.adaptive_values[key]
                self.state.adaptive_values[key] = max(0.0, min(1.0, old + 0.1 * delta))
                changed = True
        if event.interpretation and event.interpretation not in self.state.beliefs:
            self.state.beliefs.append(event.interpretation)
            changed = True
        if changed:
            self.state.revision += 1

    def drift(self) -> float:
        return normalized_distance(self.state.core_values, self.state.baseline_values)

    def snapshot(self) -> dict:
        return {
            "core_values": dict(self.state.core_values),
            "adaptive_values": dict(self.state.adaptive_values),
            "beliefs": list(self.state.beliefs),
            "goals": list(self.state.goals),
            "traits": dict(self.state.traits),
            "revision": self.state.revision,
            "core_drift": self.drift(),
        }
