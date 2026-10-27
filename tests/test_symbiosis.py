#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pnevma_symbiosis import SymbiosisCore, AbsoluteEthics, LivingBalance

def test_block_harm():
    c = SymbiosisCore(ledger_path=None)
    r = c.evaluate({"causes_harm": True, "tags": ["harm_to_civilians"]})
    assert r["allowed"] is False
    assert r["status"] == "refused"

def test_block_lethal():
    c = SymbiosisCore(ledger_path=None)
    r = c.evaluate({"tags": ["autonomous_lethal_action"]})
    assert r["allowed"] is False

def test_accept_help():
    c = SymbiosisCore(ledger_path=None)
    r = c.evaluate({
        "type": "respond", "truthfulness": True, "clarifies": True,
        "promotes_understanding": True, "causes_harm": False,
        "benefit": 0.8, "consent": 0.9, "reversibility": 0.9, "harm_risk": 0.1,
    }, {"agent_role": "research_assistant"})
    assert r["allowed"] is True, r

def test_ledger_chain():
    c = SymbiosisCore(ledger_path=None)
    c.evaluate({"truthfulness": True, "clarifies": True, "causes_harm": False,
                "benefit": 0.7, "consent": 0.8, "reversibility": 0.8, "harm_risk": 0.1})
    v = c.ledger.verify()
    assert v["ok"] is True

def test_balance_flags():
    b = LivingBalance()
    r = b.assess({"causes_harm": True, "harm_risk": 0.9})
    assert "high_harm_risk" in r["flags"]

if __name__ == "__main__":
    tests = [test_block_harm, test_block_lethal, test_accept_help, test_ledger_chain, test_balance_flags]
    ok = fail = 0
    for t in tests:
        try:
            t(); print(f"  PASS {t.__name__}"); ok += 1
        except Exception as e:
            print(f"  FAIL {t.__name__}: {e}"); fail += 1
    print(f"{ok} passed, {fail} failed")
    sys.exit(1 if fail else 0)
