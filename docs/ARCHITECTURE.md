# CCOS-Ω Architecture v0.1

## Runtime flow
1. Input arrives through CLI or FastAPI.
2. `WorldModel` stores observations.
3. `NarrativeMemory` stores an event with time, importance, affect, participants and value impact.
4. `IdentityEngine` updates adaptive values and autobiographical beliefs while keeping core anchors unchanged.
5. `IntuitionEngine` generates analogy, inversion, cross-domain and contradiction-search candidates.
6. `ReflectivePlanner` emits a transparent template plan.
7. `EthicalGyroscope` applies simple harm/truthfulness thresholds.
8. `EvolutionEngine` records a candidate improvement proposal; no source-code mutation occurs.

## Memory Gravity
The prototype score is:

`MG = similarity × importance × frequency_factor × emotion_factor × recency_decay × causal_relevance × value_relevance`

It is a heuristic, not a validated law. `similarity` is token Jaccard similarity; recency uses exponential decay by cycle.

## Identity
Core values are treated as stable anchors. Adaptive values may shift by a small amount based on explicitly supplied `impact_on_values`. This is a design decision for testability, not a universal theory of identity.

## Pneuma / Soul Emergence Index
`PneumaState` maps philosophical ideas to normalized computational dimensions. `soul_emergence_index()` computes a geometric mean over selected dimensions. This score measures only the chosen internal variables; it does not measure or prove subjective experience, personhood, or a metaphysical soul.

## Evolution governance
The engine proposes candidate patterns and can record test outcomes. Promotion is only marked `eligible_for_review` when every supplied test result is truthy. This is not automatic production deployment. Changes to core code require review, regression tests, and versioned releases.
