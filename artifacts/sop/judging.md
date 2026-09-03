# Judging and reading results — when there is no right answer

For scoring open-ended output, and for deciding whether a number that moved
actually moved. Run it before trusting a comparison, not after publishing one.

## Before the judge runs
- [ ] ☠ Rubric written: dimensions that fail independently, observable criteria
      rather than adjectives, three or four levels, an anchor example per level
- [ ] ☠ Two people scored ten items against it independently and agreed — if they
      did not, the rubric describes nothing and the judge will produce confident noise
- [ ] Judge is from a different family than the system under test, and never the
      model under test
- [ ] Deterministic checks exhausted first — a verifier beats a judge wherever one exists

## Blinding
- [ ] ☠ Source blinded: which model or variant produced each output
- [ ] ☠ Condition blinded: which arm is the treatment
- [ ] ☠ Calibration set hand-labelled *blind* — labelling ground truth while knowing
      the source makes the agreement rate a measure of your expectations
- [ ] Pairwise rather than absolute, and presented in both orders
- [ ] Recorded whether the reader could plausibly have guessed anyway — style tells
      survive blinding

## Reading the number
- [ ] ☠ Concurrent baseline, not a stored one (see measurement, step 2)
- [ ] Paired comparison where the data is paired — same items through both systems.
      An unpaired test on paired data leaves item difficulty in the noise and can
      hide a real effect entirely
- [ ] Sample variance divided by n−1, not n — the error is worth a tenth of the
      variance at eval-set sizes
- [ ] Per-arm distribution reported, not only the means — a change that helps most
      and badly harms a few moves the mean upward
- [ ] ☠ Stopping point fixed before any data arrived; no peeking and stopping when
      it crosses
- [ ] Agreement rate published alongside any judge score

> A rubric without blinding gives consistent bias. Blinding without a rubric gives
> honest noise. Neither substitutes for the other.
