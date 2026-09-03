OUTDIR = "notebooks/09-electives"

_SETUP = '''import random
from collections import Counter, defaultdict

random.seed(9)

# Prices per million tokens. The shape is what matters, not any one vendor's number —
# change these to yours and every conclusion below recomputes.
IN_PER_M, OUT_PER_M = 3.00, 15.00
CACHE_WRITE_MULT, CACHE_READ_MULT = 1.25, 0.10

def cost(tokens_in, tokens_out, cached_in=0):
    fresh = tokens_in - cached_in
    return (fresh * IN_PER_M
            + cached_in * IN_PER_M * CACHE_READ_MULT
            + tokens_out * OUT_PER_M) / 1e6

print(f"input  ${IN_PER_M:.2f}/M   output ${OUT_PER_M:.2f}/M   "
      f"cache read {CACHE_READ_MULT:.0%} of input, write {CACHE_WRITE_MULT:.0%}")
print(f"one 2,000-token question with a 500-token answer: ${cost(2000, 500):.4f}")'''


_GROWTH = '''# A conversation re-sends its whole history every turn. That is not a detail,
# it is the shape of the bill.
SYSTEM, PER_USER, PER_REPLY = 1200, 150, 400

print(f"{'turn':>5}{'sent in':>10}{'this turn':>12}{'running':>11}")
history, running = SYSTEM, 0.0
for turn in range(1, 21):
    sent = history + PER_USER
    c = cost(sent, PER_REPLY)
    running += c
    history = sent + PER_REPLY
    if turn in (1, 2, 5, 10, 15, 20):
        print(f"{turn:>5}{sent:>10}{c:>12.4f}{running:>11.4f}")

first = cost(SYSTEM + PER_USER, PER_REPLY)
print(f"\\nturn 20 costs {c/first:.1f}x turn 1, and the question was the same size")
print(f"total for 20 turns: ${running:.3f}  —  20 independent one-shot calls: "
      f"${20*first:.3f}")'''


_CACHE = '''# The stable prefix is the lever. Cache it and the same conversation changes shape.
def conversation(turns, cache_prefix=False):
    history, total = SYSTEM, 0.0
    for t in range(turns):
        sent = history + PER_USER
        if cache_prefix and t > 0:
            total += cost(sent, PER_REPLY, cached_in=SYSTEM)
        elif cache_prefix:
            # first turn pays the write premium on the part being cached
            total += cost(sent - SYSTEM, PER_REPLY) + SYSTEM * IN_PER_M * CACHE_WRITE_MULT / 1e6
        else:
            total += cost(sent, PER_REPLY)
        history = sent + PER_REPLY
    return total

print(f"{'turns':>6}{'uncached':>11}{'cached':>10}{'saving':>9}")
for t in (2, 5, 10, 20, 50):
    a, b = conversation(t), conversation(t, cache_prefix=True)
    print(f"{t:>6}{a:>11.4f}{b:>10.4f}{100*(a-b)/a:>8.0f}%")

print("\\nthe saving is capped by the share of the prompt that is actually stable —")
print(f"here the system block is {SYSTEM} tokens and the history is not cacheable,")
print("so the percentage falls as the conversation grows past the fixed part")'''


_OUTCOME = '''# Cost per call is not cost per outcome. Retries, refusals and escalations are
# paid for and deliver nothing, and they are invisible in a per-call average.
random.seed(9)
REQUESTS = 1000
runs = []
for _ in range(REQUESTS):
    attempts, resolved = 1, True
    r = random.random()
    if r < 0.08:                 # transient failure, retried once
        attempts = 2
    elif r < 0.11:               # failed twice then escalated
        attempts, resolved = 3, False
    elif r < 0.16:               # answered, but the user re-asked
        attempts = 2
    runs.append((attempts, resolved))

calls = sum(a for a, _ in runs)
spend = sum(cost(2400, 450) * a for a, _ in runs)
resolved = sum(1 for _, ok in runs if ok)

print(f"requests            : {REQUESTS}")
print(f"model calls made    : {calls}")
print(f"resolved            : {resolved}")
print(f"\\ncost per call       : ${spend/calls:.4f}")
print(f"cost per request    : ${spend/REQUESTS:.4f}")
print(f"cost per RESOLVED   : ${spend/resolved:.4f}   <- the only one a business cares about")
print(f"\\nthe gap between the first and the last is {100*(spend/resolved)/(spend/calls)-100:.0f}% —")
print("all of it spent on work that did not produce an outcome")'''


_TAIL = '''# The average hides the tail, and the tail is where the money is.
random.seed(9)
sizes = []
for _ in range(2000):
    r = random.random()
    if r < 0.80:     sizes.append(int(random.gauss(1800, 400)))    # ordinary question
    elif r < 0.97:   sizes.append(int(random.gauss(9000, 2500)))   # a document attached
    else:            sizes.append(int(random.gauss(60000, 15000))) # someone pasted a report
sizes = [max(300, s) for s in sizes]
spends = sorted(cost(s, 500) for s in sizes)

def pct(p):
    return spends[int(p / 100 * (len(spends) - 1))]

mean = sum(spends) / len(spends)
print(f"mean   ${mean:.4f}")
for p in (50, 90, 99):
    print(f"p{p:<5} ${pct(p):.4f}   {pct(p)/mean:>5.1f}x the mean")

top = sorted(spends)[-int(0.03 * len(spends)):]
print(f"\\nthe top 3% of requests are {100*sum(top)/sum(spends):.0f}% of the spend")
print("an average tells you none of this, and a per-user cap set from the mean")
print("would let every one of those requests through")'''


_ATTRIB = '''# Attribution: the same invoice, split by the question that produced it.
FEATURES = {
 "summarise-document": dict(share=0.15, tin=12000, tout=600, retries=1.05),
 "answer-from-corpus": dict(share=0.55, tin=2400,  tout=450, retries=1.12),
 "classify-ticket":    dict(share=0.25, tin=600,   tout=40,  retries=1.02),
 "draft-reply":        dict(share=0.05, tin=1800,  tout=900, retries=1.30),
}
N = 10_000
rows = []
for name, f in FEATURES.items():
    n = int(N * f["share"])
    c = cost(f["tin"], f["tout"]) * f["retries"] * n
    rows.append((name, n, c, c / n))
total = sum(c for _, _, c, _ in rows)

print(f"{'feature':<22}{'requests':>10}{'spend':>10}{'share':>8}{'per req':>10}")
print("-" * 60)
for name, n, c, per in sorted(rows, key=lambda r: -r[2]):
    print(f"{name:<22}{n:>10}{c:>10.2f}{100*c/total:>7.0f}%{per:>10.4f}")
print(f"{'TOTAL':<22}{N:>10}{total:>10.2f}")

print(f"\\n{'feature':<22}{'share of requests':>19}{'share of spend':>16}{'ratio':>8}")
for name, n, c, per in sorted(rows, key=lambda r: -(r[2]/total)/(r[1]/N)):
    rq, sp = n / N, c / total
    print(f"{name:<22}{100*rq:>18.0f}%{100*sp:>15.0f}%{sp/rq:>8.1f}")
cheap = min(rows, key=lambda r: r[3])
dear  = max(rows, key=lambda r: r[3])
print(f"\\nper request, {dear[0]} costs {dear[3]/cheap[3]:.0f}x what {cheap[0]} does")
print("volume and spend are different rankings, and only one of them is the bill")'''


NOTEBOOKS = [
("01-where-the-money-goes.ipynb", [

("md", """# 09 · Where the Money Goes

An invoice tells you what you spent. It does not tell you what you spent it *on*, and
the gap between those two is where cost control actually happens.

Everything here is arithmetic — no model calls, no keys, no network. The prices at the
top are a shape rather than a quotation: change them to yours and every table below
recomputes. That is the point of doing it this way rather than reading a vendor's
calculator, because the conclusions are about structure and they survive a price
change."""),

("code", _SETUP),

("md", """## 1 · Why a conversation is not twenty questions

The single most surprising line on an LLM bill. A conversation re-sends its entire
history every turn, so the twentieth turn pays for the first nineteen again."""),

("code", _GROWTH),

("md", """Twenty turns of a conversation cost several times twenty independent questions of the
same size, and nothing about the twentieth question was harder. This is the arithmetic
behind the session-lifecycle lesson's advice to cap a session deliberately: the cost of
turn *n* is not the cost of turn *n*, it is the cost of everything before it."""),

("md", """## 2 · What caching actually buys

Prefix caching charges a premium to write and a fraction to read. Whether that is a
saving depends entirely on how much of your prompt is genuinely stable."""),

("code", _CACHE),

("md", """Read the direction of that last column rather than any single figure. The saving is
largest when the fixed part dominates and *shrinks as the conversation grows*, because
the history accumulating in front of the model is not cacheable and eventually
outweighs the system block.

Which gives the design rule directly: caching pays best on short, high-volume calls
with a large stable prefix, and pays least on the long sessions people assume it will
rescue."""),

("md", """## 3 · Cost per call, per request, and per outcome

Three numbers that get used interchangeably and are not the same. Retries, re-asks and
escalations are all paid for; only some of them produce anything."""),

("code", _OUTCOME),

("md", """The last line is the only one a business can act on. A per-call average makes a system
with a 15% retry rate look identical to one with none, because the retries are in the
denominator as well as the numerator.

Note also what it does to a comparison: a cheaper model that needs more retries can be
more expensive per resolved request while being cheaper per call, and a per-call
average will recommend it."""),

("md", """## 4 · The tail, which the mean hides"""),

("code", _TAIL),

("md", """This is the fourth place cost hides. A mean sits close to the ordinary request because
most requests are ordinary, and a small minority — a pasted report, an attached
document — carries a large share of the spend.

The operational consequence is specific: a limit derived from the mean does not
constrain the requests that matter. Bound the *input*, because that is the term you can
actually see before you spend anything."""),

("md", """## 5 · Attribution, which is the point of all of it"""),

("code", _ATTRIB),

("md", """The ratio column is the finding. A feature at 1.0 costs its fair share; above 1.0 it
consumes more of the bill than of the traffic. Here document summarisation takes a
sixth of the requests and nearly half the spend, while ticket classification is a
quarter of the traffic and a rounding error on the invoice.

That is the whole reason to attribute rather than divide. A per-request cost that
varies by more than an order of magnitude between features means "requests per day"
tells you almost nothing about what you will be charged, and optimising the busiest
path is the intuitive move and frequently the wrong one.

To make this real in your own system, the requirement is unglamorous: record tokens in,
tokens out, cache hits and retries **per request, at the time**, tagged with the feature
that caused it. None of the tables above can be reconstructed from an invoice
afterwards."""),

("md", """## What to carry away

- **A conversation's cost grows with its length, not its questions.** Cap sessions.
- **Caching pays on a large stable prefix**, and pays less the longer the session runs.
- **Divide by outcomes, not by calls.** Retries are in both halves of a per-call average.
- **Watch the tail.** A cap set from the mean constrains nothing that matters.
- **Tag spend at the time.** An invoice cannot be attributed after the fact.

This complements Block 0's routing lesson, which covers the architecture for spending
less. This is the measurement that tells you whether it worked."""),
]),
]
