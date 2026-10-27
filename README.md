# CCOS-Ω Research Core v0.1

Runnable Python MVP for persistent narrative agents in games and simulations.

## Included
- Narrative episodic memory and Memory Gravity retrieval
- Identity continuity and adaptive values
- PneumaState as an explicit operational metaphor, not a claim of actual soul/consciousness
- Intuition and novelty candidate generation
- Ethical action scoring
- Reflective planning and a simple world model
- Relationships and culture notes
- Test-gated evolution proposals (does not rewrite its own code)
- FastAPI, CLI, pytest tests, Docker
- Deterministic synthetic benchmark task generator

## Quick start (Python 3.10+)
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
python -m ccos
```

API:
```bash
uvicorn ccos.api:app --reload
```
Then open http://127.0.0.1:8000/docs

## API
- `POST /process` process an input and advance a cycle
- `POST /remember` store a narrative event
- `GET /status` runtime status
- `GET /identity` identity state
- `GET /biography` narrative history
- `POST /plan` create a candidate plan
- `POST /reflect` reflect on a question

## Architecture
Input → World Model → Narrative Memory → Identity/Affect → Intuition → Planner → Ethical evaluation → Reflection → Experience → versioned evolution proposal.

## Limitations
This is an early MVP, not AGI, a production-ready game engine, or evidence of subjective consciousness. The Soul Emergence Index is an observable functional composite only. Memory Gravity is a heuristic requiring ablation tests and comparisons with baselines. Storage is in-memory by default. The benchmark generator produces synthetic tasks, not a validated scientific benchmark. Evolution proposes changes but cannot autonomously rewrite the kernel.
