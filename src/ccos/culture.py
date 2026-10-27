from dataclasses import dataclass, field

@dataclass
class CulturalConcept:
    tradition: str
    concept: str
    interpretation: str
    status: str = "hypothesis"
    source_note: str = ""

class CultureEngine:
    """Stores tradition-derived interpretations as interpretations, not universal facts."""
    def __init__(self):
        self.concepts: list[CulturalConcept] = []

    def add(self, tradition: str, concept: str, interpretation: str, source_note: str = "") -> CulturalConcept:
        item = CulturalConcept(tradition, concept, interpretation, "hypothesis", source_note)
        self.concepts.append(item)
        return item

    def list(self) -> list[dict]:
        return [vars(item).copy() for item in self.concepts]
