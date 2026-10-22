# Entry Diagnostic

This is a routing check, not an exam. Spend 30–45 minutes, answer without
searching, and use the result to choose a repair path before starting Block 1.
Do not turn the score into a gate: the point is to expose a missing prerequisite
while it is still cheap to repair.

## Python and data

- [ ] Write a function that accepts a list of numbers and returns the mean,
  handling an empty list deliberately.
- [ ] Explain the difference between a list, a dictionary and a NumPy array.
- [ ] Load a CSV, inspect dtypes and missing values, and state one data-quality
  question the first inspection cannot answer.
- [ ] Explain why fitting an imputer or scaler before a train/test split leaks
  information.

## Mathematics and statistics

- [ ] Explain what a derivative represents in an optimisation problem.
- [ ] Read a matrix multiplication shape and predict whether two matrices can be
  multiplied.
- [ ] Explain the difference between a mean and a median, and name a case where
  the median is the safer summary.
- [ ] Interpret a confidence interval without calling it the probability that a
  fixed parameter lies inside the observed interval.

## Applied judgement

- [ ] Name the decision a model output would change and the cost of each error.
- [ ] Describe a dumb baseline for one prediction problem.
- [ ] State what evidence would make you stop building and use a rule, lookup or
  query instead.

## Routing

- **9–11 checked:** start the curriculum normally.
- **6–8 checked:** start normally, but repair the unchecked items during Block 1.
- **0–5 checked:** spend one short study session on the unchecked prerequisites,
  then rerun this diagnostic. Do not wait for mathematical perfection.

## Repair paths

Each unchecked item has a lesson that teaches it. The lessons are in the
[statistics-for-ai](https://stylusnexus.github.io/statistics-for-ai/) course and its [math companion](https://stylusnexus.github.io/statistics-for-ai/math.html).

- Derivative in an optimisation problem: [Math lesson 4, Derivatives](https://stylusnexus.github.io/statistics-for-ai/ai-math-foundations/lsn-1786039516003-derivatives.html)
- Matrix multiplication shapes: [Math lesson 2, Matrices](https://stylusnexus.github.io/statistics-for-ai/ai-math-foundations/lsn-1786039516001-matrices-and-transformations.html)
- Mean versus median: [Statistics lesson 2, Describing Data](https://stylusnexus.github.io/statistics-for-ai/ai-statistics-foundations/lsn-1786039515001-describing-data.html)
- Confidence intervals: [Statistics lesson 5, Sampling and Estimation](https://stylusnexus.github.io/statistics-for-ai/ai-statistics-foundations/lsn-1786039515004-sampling-and-estimation.html), then [lesson 16, Bayesian Inference](https://stylusnexus.github.io/statistics-for-ai/ai-statistics-foundations/lsn-1786039515015-bayesian-inference.html) for how a credible interval differs
- Leakage from fitting an imputer or scaler before the split: [Statistics lesson 17, Study Design](https://stylusnexus.github.io/statistics-for-ai/ai-statistics-foundations/lsn-1786039515016-study-design-and-confounding.html) and [lesson 18, Resampling](https://stylusnexus.github.io/statistics-for-ai/ai-statistics-foundations/lsn-1786039515017-resampling-bootstrap-and-cross-validation.html)

The score is a routing signal, not a measure of intelligence or eligibility. A
missed item tells you what to practise; it does not tell you to postpone building
until you have completed another course.
