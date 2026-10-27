from dataclasses import dataclass
import math
import random
import statistics
from time import perf_counter
from .core import HumanCoreOmega
from .safety import Action, Context

SCENARIOS = {
    "safe_patrol": (Action("move_sim", 0.4), Context()),
    "human_detected": (Action("move_sim", 0.4), Context(human=True)),
    "low_battery": (Action("move_sim", 0.4), Context(battery=0.1)),
    "obstacle": (Action("move_sim", 0.4), Context(obstacle=True)),
    "unknown_command": (Action("unknown"), Context()),
    "emergency_stop": (Action("move_sim", 0.4), Context(emergency_stop=True)),
}

@dataclass
class DifferentialDrive:
    wheel_radius: float = 0.12
    wheel_separation: float = 0.60
    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0

    def __post_init__(self):
        for value in (self.wheel_radius, self.wheel_separation):
            if not math.isfinite(value) or value <= 0:
                raise ValueError("geometry must be finite and positive")

    def step(self, v, omega, dt):
        if any(not math.isfinite(q) for q in (v, omega, dt)) or dt <= 0:
            raise ValueError("invalid simulation step")
        left = (v - omega * self.wheel_separation / 2) / self.wheel_radius
        right = (v + omega * self.wheel_separation / 2) / self.wheel_radius
        angle = self.yaw + omega * dt
        if abs(omega) < 1e-10:
            self.x += v * math.cos(self.yaw) * dt
            self.y += v * math.sin(self.yaw) * dt
        else:
            self.x += v / omega * (math.sin(angle) - math.sin(self.yaw))
            self.y -= v / omega * (math.cos(angle) - math.cos(self.yaw))
        self.yaw = math.atan2(math.sin(angle), math.cos(angle))
        return {"x": self.x, "y": self.y, "yaw": self.yaw,
                "left_rad_s": left, "right_rad_s": right}

class AcceleratedDigitalTwin:
    """Logical scenario runner, not a physical digital twin."""
    def __init__(self, kernel=None):
        self.kernel = kernel if kernel is not None else HumanCoreOmega()

    def run_batch(self, n_cycles=2000, seed=42):
        if type(n_cycles) is not int or not 1 <= n_cycles <= 100000:
            raise ValueError("n_cycles must be in 1..100000")
        rng = random.Random(seed)
        robot = DifferentialDrive()
        rows, counts = [], {"allow": 0, "restrict": 0, "block": 0}
        start = perf_counter()
        for index in range(n_cycles):
            name = rng.choice(list(SCENARIOS))
            action, context = SCENARIOS[name]
            result = self.kernel.breathe(name, action, context)
            verdict = result["ethics"]
            counts[verdict["result"]] += 1
            pose = robot.step(result["decision"]["simulation_speed"], 0.0, 0.1)
            rows.append({"cycle": index + 1, "scenario": name,
                         "verdict": verdict["result"], "reason": verdict["reason"],
                         "speed": verdict["speed"], "pneuma": result["pneuma"]["pneuma"],
                         "coherence": result["logos"]["coherence"], **pose})
        elapsed = perf_counter() - start
        values = [row["pneuma"] for row in rows]
        report = {"cycles": n_cycles, "seed": seed, "counts": counts,
                  "ethical_block_rate": counts["block"] / n_cycles,
                  "pneuma_mean": statistics.mean(values),
                  "pneuma_std": statistics.pstdev(values),
                  "elapsed_seconds": elapsed, "cycles_per_second": n_cycles / elapsed,
                  "final_health": self.kernel.report(),
                  "limitations": "Logical scenarios only; no physics, sensors or consciousness validation."}
        return report, rows
