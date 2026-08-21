# Project Intake Sheet

Fill this in **before** writing code. Every project, every substantial lab.

The point isn't the document — it's that after four or five of these, the
questions start asking themselves. That's the whole mechanism. Judgment is
a habit, not a lecture.

Re-read your completed sheet **after** the project against what actually
happened. That comparison is where the learning is.

---

**Project:** Wind turbine failure prediction
**Date:** 
**Block:** 2

> Fill this in before running `src/train.py`. Questions 2 and 6 in particular —
> the baseline and the cost of each error type — decide how you read every
> number the script produces.

### 1. Is this even a machine learning problem?

Could a rule, a lookup table, a SQL query, or a human doing it twice a day solve this?
If yes, say so and stop. Most "AI projects" die here and should.

> 

### 2. What is the dumb baseline, and did you build it?

Predict the mean. Always guess the majority class. Return the most recent value.
Keyword search instead of embeddings. **Build it first.** If your model can't beat it,
you've learned something cheap.

> Baseline:
> Baseline score:

### 3. What data exists?

How much, where from, who owns it, is it labeled, how good are the labels,
and is it representative of what you'll see in production?

> 

### 4. What decision does the output drive?

Not "insight." A decision. Who makes it, how often, and what do they do differently
depending on the answer? If nothing changes, the project has no value.

> 

### 5. What does "good enough" mean, as a number?

Decide this before you see any results, or you will rationalise whatever you get.

> Metric:
> Threshold:
> Chosen because:

### 6. What does being wrong cost, and is it symmetric?

A false negative on fraud detection and a false positive are not the same event.
Say which one hurts more and by roughly how much.

> False positive costs:
> False negative costs:

### 7. What happens when it fails?

Not *if*. What's the fallback path, who gets alerted, and does the system degrade
safely or confidently produce garbage?

> 

### 8. What does this cost at 100x volume?

Per-inference cost, latency budget, and what breaks first when traffic multiplies.

> 

### 9. Who is accountable for the output?

Especially where the output reaches a customer, a regulator, or a clinical decision.

> 

### 10. What would make you kill this?

Name the condition now, while you're still objective.

> 

---

## Post-mortem (fill in after)

- Which answer above turned out most wrong?
- What did the baseline actually score vs. the model?
- What did you not ask that you should have?

> 
