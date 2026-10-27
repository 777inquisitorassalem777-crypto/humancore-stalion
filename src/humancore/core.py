from dataclasses import asdict
from .memory import ChainMemory
from .safety import Action, Context, FormalEthicalVeto

class HumanCoreOmega:
    """A deterministic computational metaphor, not a sentient system."""
    def __init__(self):
        self.memory = ChainMemory()
        self.veto = FormalEthicalVeto()
        self.cycles = 0
        self.pneuma = 0.5
        self.coherence = 1.0

    def cycle(self, text="", action=None, context=None):
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if len(text) > 4096:
            raise ValueError("text exceeds 4096 characters")
        action = Action() if action is None else action
        context = Context() if context is None else context
        verdict = self.veto.check(action, context)
        self.cycles += 1
        target = 0.25 if verdict.result == "block" else 0.75
        self.pneuma += 0.05 * (target - self.pneuma)
        self.coherence = 1.0 - abs(self.pneuma - target)
        result = {
            "cycle": self.cycles, "context_text": text,
            "pneuma": {"pneuma": self.pneuma},
            "logos": {"coherence": self.coherence},
            "ethics": {**asdict(verdict), "blocked": verdict.result == "block"},
            "decision": {"action": "idle" if verdict.result == "block" else action.kind,
                         "simulation_speed": verdict.speed},
            "self_model": {"kind": "computational_metaphor", "consciousness_claim": False}}
        self.memory.append(result)
        return result

    def breathe(self, *args, **kwargs):
        return self.cycle(*args, **kwargs)

    def report(self):
        return {"cycles": self.cycles, "pneuma": self.pneuma,
                "coherence": self.coherence,
                "memory_valid": self.memory.verify(self.memory.records),
                "simulation_only": True}
