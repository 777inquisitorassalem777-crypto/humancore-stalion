from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

@dataclass
class EvolutionProposal:
    description: str
    evidence: str
    status: str = "proposed"
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    test_results: dict = field(default_factory=dict)

class EvolutionEngine:
    """Propose and test changes; never edits source code or disables safeguards."""
    def __init__(self):
        self.proposals: list[EvolutionProposal] = []

    def propose(self, description: str, evidence: str) -> EvolutionProposal:
        proposal = EvolutionProposal(description=description, evidence=evidence)
        self.proposals.append(proposal)
        return proposal

    def record_test_result(self, proposal_id: str, results: dict) -> EvolutionProposal:
        for proposal in self.proposals:
            if proposal.id == proposal_id:
                proposal.test_results = dict(results)
                proposal.status = "eligible_for_review" if results and all(results.values()) else "rejected_or_needs_work"
                return proposal
        raise KeyError(f"Unknown proposal id: {proposal_id}")
