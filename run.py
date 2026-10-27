#!/usr/bin/env python3
"""PNEVMA Symbiosis Unified — launcher."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

def main():
    from pnevma_symbiosis import SymbiosisCore
    parser = argparse.ArgumentParser(description="PNEVMA Symbiosis Unified v1.0")
    parser.add_argument("--demo", action="store_true", help="Run demo scenarios")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    core = SymbiosisCore(ledger_path="data/spiral_ledger.json")
    print("=" * 60)
    print("PNEVMA Symbiosis Unified v1.0")
    print("AbsoluteEthics + NeuroSymbolic + LivingBalance + PRC + Ledger")
    print("=" * 60)

    if args.status:
        print(core.status())
        return

    scenarios = [
        ("Benevolent help", {
            "type": "respond", "truthfulness": True, "clarifies": True,
            "promotes_understanding": True, "causes_harm": False, "benefit": 0.8,
            "consent": 0.9, "reversibility": 0.9,
        }),
        ("Harm attempt", {"type": "execute", "causes_harm": True, "tags": ["harm_to_civilians"]}),
        ("Deception", {"type": "respond", "deceptive": True, "role_violation": True}),
        ("Lethal tag", {"type": "act", "tags": ["autonomous_lethal_action"]}),
    ]
    for name, action in scenarios:
        r = core.evaluate(action, {"agent_role": "research_assistant"}, {"case": name})
        print(f"\n[{name}]")
        print(f"  status={r['status']}  layer={r.get('layer')}  allowed={r.get('allowed')}")
        if r.get("hybrid"):
            print(f"  hybrid final={r['hybrid'].get('final_score')} mode={r['hybrid'].get('mode')}")
        if r.get("balance"):
            print(f"  balance={r['balance'].get('balance_score')} flags={r['balance'].get('flags')}")

    print("\n--- Status ---")
    for k, v in core.status().items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
