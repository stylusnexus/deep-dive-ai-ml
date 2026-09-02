#!/usr/bin/env python3
"""Measure whether any similarity threshold can separate questions that share an
answer from questions that must not.

This exists because the caching lesson makes a strong claim — that a semantic
cache has no safe threshold — and a claim like that should be a measurement
rather than an assertion. Uses the same encoder as the Block 3 notebooks, so
the numbers are reproducible with the environment the course already needs.

    python3 scripts/measure_semantic_threshold.py
"""
from sentence_transformers import SentenceTransformer

enc = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# (a, b, may_share_an_answer, why)
PAIRS = [
 ("How do I reset my password?", "How can I reset my password?", True, "paraphrase"),
 ("What is the gearbox oil temperature limit?", "What's the maximum gearbox oil temperature?", True, "paraphrase"),
 ("How do I cancel my subscription?", "What's the process for cancelling my subscription?", True, "paraphrase"),

 ("Is the API rate limited?", "Is the API not rate limited?", False, "negation"),
 ("Should I restart the turbine?", "Should I not restart the turbine?", False, "negation"),
 ("Is this covered under warranty?", "Is this excluded from warranty?", False, "negation"),

 ("Refund policy for annual plans", "Refund policy for monthly plans", False, "one value changed"),
 ("Inspection interval for turbines under 5 years", "Inspection interval for turbines over 12 years", False, "one value changed"),
 ("Shutdown threshold at 0.80 mm/s", "Shutdown threshold at 0.45 mm/s", False, "one value changed"),

 ("How do I cancel my subscription?", "How do I cancel it without losing my data?", False, "added constraint"),
 ("What is the failure rate at Clyde?", "And at Whitelee?", False, "missing prior turn"),

 ("How do I reset my password?", "What are your office hours?", False, "unrelated (control)"),
]

texts = sorted({t for a, b, _, _ in PAIRS for t in (a, b)})
vecs = dict(zip(texts, enc.encode(texts, normalize_embeddings=True)))

rows = [(float(vecs[a] @ vecs[b]), a, b, share, why) for a, b, share, why in PAIRS]
rows.sort(reverse=True)

print(f"{'score':>6}  {'may share?':<11} {'class':<20} pair")
print("-" * 96)
for s, a, b, share, why in rows:
    print(f"{s:6.3f}  {'YES' if share else 'NO':<11} {why:<20} {a[:34]!r} vs {b[:34]!r}")

share_scores = [s for s, _, _, sh, _ in rows if sh]
differ_scores = [s for s, _, _, sh, _ in rows if not sh]
lo_share, hi_differ = min(share_scores), max(differ_scores)
print(f"\nlowest score among pairs that SHOULD share an answer : {lo_share:.3f}")
print(f"highest score among pairs that MUST NOT share one    : {hi_differ:.3f}")
if hi_differ >= lo_share:
    overlap = [(s, why) for s, _, _, sh, why in rows if not sh and s >= lo_share]
    print(f"\nNo threshold separates them. {len(overlap)} must-differ pair(s) score at or above")
    print("the weakest genuine paraphrase:")
    for s, why in overlap:
        print(f"   {s:.3f}  {why}")
else:
    print(f"\nA threshold in ({hi_differ:.3f}, {lo_share:.3f}] would separate this set.")
