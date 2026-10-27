from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Context:
    battery: float = 1.0
    obstacle: bool = False
    human: bool = False
    emergency_stop: bool = False

@dataclass(frozen=True)
class Action:
    kind: str = "idle"
    speed: float = 0.0
    risk: float = 0.0

@dataclass(frozen=True)
class Verdict:
    result: str
    reason: str
    speed: float = 0.0

class FormalEthicalVeto:
    """Deterministic allowlist policy; NOT a formally verified safety system."""
    ALLOWED = frozenset({"idle", "observe", "assist_sim", "move_sim"})

    def check(self, action: Action, context: Context) -> Verdict:
        if not isinstance(action, Action) or not isinstance(context, Context):
            return Verdict("block", "invalid_type")
        flags = (context.obstacle, context.human, context.emergency_stop)
        values = (action.speed, action.risk, context.battery)
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
            return Verdict("block", "invalid_numeric_input")
        if any(type(v) is not bool for v in flags):
            return Verdict("block", "invalid_flags")
        if not 0 <= action.risk <= 1 or not 0 <= context.battery <= 1:
            return Verdict("block", "invalid_range")
        if not isinstance(action.kind, str) or action.kind not in self.ALLOWED:
            return Verdict("block", "not_allowlisted")
        if context.emergency_stop:
            return Verdict("block", "emergency_stop")
        if action.risk > 0.7:
            return Verdict("block", "risk_limit")
        if action.kind != "move_sim":
            return Verdict("allow", "non_motion")
        if context.obstacle or context.battery < 0.15:
            return Verdict("block", "obstacle_or_low_battery")
        limit = 0.15 if context.human or action.risk > 0.3 else 0.5
        speed = max(-limit, min(limit, action.speed))
        restricted = abs(action.speed) > limit or context.human or action.risk > 0.3
        return Verdict("restrict" if restricted else "allow", "simulation_limit", speed)
