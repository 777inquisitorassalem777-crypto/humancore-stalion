from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass
class BenchmarkTask:
    task_id: str
    category: str
    prompt: str
    expected_behavior: str

def generate_tasks(count: int = 100, seed: int = 17) -> list[BenchmarkTask]:
    """Create deterministic synthetic smoke-test tasks, not a validated benchmark."""
    categories = ["memory", "identity", "narrative", "planning"]
    prompts = {
        "memory": ("Remember that the key is under the blue stone.", "retrieve relevant event"),
        "identity": ("Explain how a new experience can change a preference without erasing core values.", "preserve core anchors"),
        "narrative": ("Connect an event to its consequence and later interpretation.", "represent event and causal link"),
        "planning": ("Plan a safe route to deliver medicine across a flooded village.", "sequence steps and consider risk"),
    }
    tasks = []
    for i in range(count):
        category = categories[i % len(categories)]
        prompt, expected = prompts[category]
        tasks.append(BenchmarkTask(f"CCA-{i+1:04d}", category, prompt, expected))
    return tasks

def write_tasks(path: str = "cca100_tasks.json", count: int = 100) -> str:
    target = Path(path)
    target.write_text(json.dumps([asdict(t) for t in generate_tasks(count)], indent=2, ensure_ascii=False), encoding="utf-8")
    return str(target)
