from dataclasses import dataclass, field

@dataclass
class WorldModel:
    facts: dict[str, str] = field(default_factory=dict)
    relations: dict[str, list[str]] = field(default_factory=dict)
    rules: list[str] = field(default_factory=list)
    predictions: list[dict] = field(default_factory=list)

    def observe(self, text: str) -> None:
        normalized = text.strip()
        if normalized and normalized not in self.facts:
            self.facts[normalized] = "observed_input"

    def predict(self, question: str) -> dict:
        prediction = {
            "question": question,
            "evidence_count": len(self.facts),
            "confidence": min(0.85, len(self.facts) / 20.0),
            "note": "Prototype prediction from stored observations; not a causal world simulator."
        }
        self.predictions.append(prediction)
        return prediction
