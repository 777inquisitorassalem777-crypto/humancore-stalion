# PNEVMA Symbiosis Unified v1.0

Unified research sandbox integrating lineages:

| Source lineage | Integrated as |
|----------------|---------------|
| **PRC** (Reflective Core) | ReflectiveLoop, Pneuma metrics, PyramidProbe |
| **Neuro-Symbolic Hybrid** | NeuralScorer + SymbolicEngine with hard veto |
| **Stalion ethics** | AbsoluteEthics (non-overridable prohibitions) |
| **EDGE Omega** | LivingBalance, SpiralLedger (hash chain) |

## Hard constraints
- `self_modify = False`
- Absolute prohibitions cannot be disabled
- No combat/robot actuator control
- Research / simulation only

## Run
```bash
python run.py --demo
python tests/test_symbiosis.py
```

## Layers (order)
1. AbsoluteEthics (hard block)
2. NeuroSymbolicHybrid (veto / score)
3. LivingBalance (diagnostic)
4. ReflectiveLoop (memory + coherence)
5. SpiralLedger (append-only audit)
