from dataclasses import dataclass

@dataclass
class EthicalScore:
    benefit: float
    harm: float
    truthfulness: float
    autonomy: float
    allowed: bool
    rationale: str

class EthicalGyroscope:
    """Transparent heuristic filter; not a substitute for human review."""
    def evaluate(self, action: str, benefit: float = 0.5, harm: float = 0.0,
                 truthfulness: float = 0.8, autonomy: float = 0.8) -> EthicalScore:
        values = [benefit, harm, truthfulness, autonomy]
        benefit, harm, truthfulness, autonomy = [max(0.0, min(1.0, float(v))) for v in values]
        allowed = harm < 0.75 and truthfulness >= 0.25
        rationale = "passes heuristic thresholds" if allowed else "blocked by high estimated harm or very low truthfulness"
        return EthicalScore(benefit, harm, truthfulness, autonomy, allowed, rationale)
