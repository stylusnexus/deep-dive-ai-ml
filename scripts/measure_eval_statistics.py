#!/usr/bin/env python3
"""Simulations behind the statistics lesson, so its numbers are measured.

Two claims that lessons usually assert:

  1. Dividing a sample variance by n rather than n-1 underestimates it, and the
     size of the error is what decides whether Bessel's correction matters to you.
  2. Peeking at a running experiment and stopping when it looks significant
     inflates the false-positive rate well past the nominal one.

Both are checked here against data with a known answer, which is the only way the
lesson can quote a figure rather than a belief.

    python3 scripts/measure_eval_statistics.py
"""
import math
import random

random.seed(11)


def bessel() -> None:
    print("Bessel's correction — true variance is 1.000 by construction\n")
    print(f"  {'n':>4}  {'divide by n':>14}  {'divide by n-1':>14}")
    for n in (5, 10, 30, 100, 1000):
        biased, corrected = [], []
        for _ in range(20_000):
            s = [random.gauss(0.0, 1.0) for _ in range(n)]
            m = sum(s) / n
            ss = sum((x - m) ** 2 for x in s)
            biased.append(ss / n)
            corrected.append(ss / (n - 1))
        b = sum(biased) / len(biased)
        c = sum(corrected) / len(corrected)
        print(f"  {n:>4}  {b:>8.3f} ({100*(b-1):+5.1f}%)  {c:>8.3f} ({100*(c-1):+5.1f}%)")
    print("\n  The estimate is too small because the mean was fitted to the same data:")
    print("  deviations from a fitted mean are systematically smaller than deviations")
    print("  from the true one. At eval-sized n the error is large; at n=1000 it is not.\n")


def welch_p(a: list[float], b: list[float]) -> float:
    na, nb = len(a), len(b)
    ma, mb = sum(a) / na, sum(b) / nb
    va = sum((x - ma) ** 2 for x in a) / (na - 1)
    vb = sum((x - mb) ** 2 for x in b) / (nb - 1)
    se = math.sqrt(va / na + vb / nb)
    if se == 0:
        return 1.0
    t = abs(ma - mb) / se
    return 2 * (1 - 0.5 * (1 + math.erf(t / math.sqrt(2))))


def peeking(trials: int = 4000, n: int = 200, peeks: int = 10) -> None:
    print("Peeking — both arms drawn from the SAME distribution, so every")
    print("'significant' result below is a false positive by construction\n")
    fixed = peeked = 0
    for _ in range(trials):
        a = [random.gauss(0, 1) for _ in range(n)]
        b = [random.gauss(0, 1) for _ in range(n)]
        if welch_p(a, b) < 0.05:
            fixed += 1
        for step in range(1, peeks + 1):
            k = n * step // peeks
            if k > 5 and welch_p(a[:k], b[:k]) < 0.05:
                peeked += 1
                break
    print(f"  tested once at the end           : {100*fixed/trials:.1f}%")
    print(f"  peeked {peeks} times, stopped when p<0.05 : {100*peeked/trials:.1f}%")
    print(f"\n  Nominal rate is 5%. The first line landing on it is the instrument")
    print(f"  check; peeking multiplied the error rate by {peeked/max(fixed,1):.1f}x.\n")


def paired_p(a: list[float], b: list[float]) -> float:
    d = [x - y for x, y in zip(a, b)]
    n = len(d)
    md = sum(d) / n
    vd = sum((x - md) ** 2 for x in d) / (n - 1)
    se = math.sqrt(vd / n)
    if se == 0:
        return 1.0
    t = abs(md) / se
    return 2 * (1 - 0.5 * (1 + math.erf(t / math.sqrt(2))))


def pairing(trials: int = 3000, n: int = 20) -> None:
    """The same data, tested two ways. An eval runs the same questions through both
    systems, so the two score sets are paired — and question difficulty, which is
    usually the largest source of variance, is shared by each pair. A paired test
    subtracts it out. An unpaired test leaves it in the noise term and drowns."""
    print("Pairing — 20 questions, a real effect of +0.30, difficulty varying by ~1.0\n")
    unp = pair = 0
    for _ in range(trials):
        difficulty = [random.gauss(0, 1.0) for _ in range(n)]
        a = [d + random.gauss(0, 0.25) for d in difficulty]
        b = [d + 0.30 + random.gauss(0, 0.25) for d in difficulty]
        if welch_p(a, b) < 0.05:
            unp += 1
        if paired_p(a, b) < 0.05:
            pair += 1
    print(f"  unpaired test detects it: {100*unp/trials:5.1f}% of the time")
    print(f"  paired   test detects it: {100*pair/trials:5.1f}% of the time")
    print("\n  Identical data and an identical effect. The unpaired test is not wrong,")
    print("  it is answering a question nobody asked — whether two unrelated piles of")
    print("  numbers differ — when the question was whether B beats A question by question.\n")


if __name__ == "__main__":
    bessel()
    pairing()
    peeking()
