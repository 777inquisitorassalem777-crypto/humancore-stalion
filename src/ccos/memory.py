from collections import Counter
from math import exp
from .models import NarrativeEvent

def lexical_similarity(query: str, text: str) -> float:
    q = set(query.lower().split())
    t = set(text.lower().split())
    if not q or not t:
        return 0.0
    return len(q & t) / max(1, len(q | t))

class NarrativeMemory:
    def __init__(self):
        self.events: list[NarrativeEvent] = []
        self._frequency: Counter[str] = Counter()

    def record(self, event: NarrativeEvent) -> NarrativeEvent:
        self.events.append(event)
        for token in set(event.text.lower().split()):
            self._frequency[token] += 1
        return event

    def gravity_score(self, query: str, event: NarrativeEvent, current_cycle: int) -> float:
        similarity = lexical_similarity(query, event.text)
        frequency = sum(self._frequency[t] for t in set(event.text.lower().split()))
        frequency_norm = min(1.0, frequency / 10.0)
        recency = exp(-0.025 * max(0, current_cycle - event.cycle))
        importance = max(0.0, min(1.0, event.importance))
        emotional_weight = min(1.0, abs(event.emotion))
        causal_relevance = 1.0 if event.impact_on_values else 0.7
        value_relevance = 1.0 if event.impact_on_values else 0.8
        return similarity * importance * (0.25 + 0.75 * frequency_norm) * (0.5 + 0.5 * emotional_weight) * recency * causal_relevance * value_relevance

    def recall(self, query: str, current_cycle: int, limit: int = 5) -> list[tuple[NarrativeEvent, float]]:
        scored = [(event, self.gravity_score(query, event, current_cycle)) for event in self.events]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return scored[:max(0, limit)]

    def recent(self, count: int = 10) -> list[NarrativeEvent]:
        return self.events[-max(0, count):]

    def __len__(self) -> int:
        return len(self.events)
