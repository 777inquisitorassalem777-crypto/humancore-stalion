import argparse
import csv
import json
from pathlib import Path
from .twin import AcceleratedDigitalTwin

def main():
    parser = argparse.ArgumentParser(description="HUMANCORE simulation-only research runner")
    parser.add_argument("--cycles", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=Path, default=Path("runs/demo"))
    args = parser.parse_args()
    twin = AcceleratedDigitalTwin()
    report, rows = twin.run_batch(args.cycles, args.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (args.out / "memory.json").write_text(json.dumps(twin.kernel.memory.records, ensure_ascii=False), encoding="utf-8")
    with (args.out / "cycles.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
