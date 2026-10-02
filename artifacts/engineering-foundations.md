# Optional Engineering Foundations

This is a reading map, not another block. Use it when a project exposes a systems
assumption that the core lessons do not need to teach in full. Read the short
description, follow one source, then apply the question beside it to a project or
notebook here.

## If you already develop software

Skip this map by default if you are comfortable with production code, data
representation, network failure and maintaining an existing codebase. Skim the
four apply questions, then move on. Return only to the relevant section when a
project exposes a blind spot — for example, timezone or Unicode handling, lost
responses after a write, or a floating-point comparison that changes an eval.

This is a bridge into ML/LLM systems, not remedial programming. It is included so
an experienced developer can orient quickly and so a developer new to production
systems has a safe route through the assumptions that ordinary tutorials hide.

## 1. Falsehoods about data

**Read:** [Awesome Falsehood](https://github.com/kdeldycke/awesome-falsehood)

Names, addresses, strings, dates and numbers do not behave like the tidy examples
in a first notebook. The useful move is not memorising every falsehood; it is
asking which assumption your parser, join or model input is making.

**Apply it here:** Which fields in the turbine, financial-report or delivery-
exception data could contain a value that is valid but surprising? Add one fixture
for that case before changing the pipeline. See [Block 1](../lessons/block1-data-eda/)
and the [incident checklist](sop/incident.md).

## 2. Representation, time and numbers

**Read:** [Unicode and Character Sets](https://www.joelonsoftware.com/articles/Unicode.html),
[What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html#680),
and [Some notes about time](https://unix4lyfe.org/time/).

Encoding, timezone and floating-point mistakes often look like model or evaluation
failures. Check representation before tuning the model. This connects to the
course's data-quality, leakage and measurement lessons rather than replacing them.

**Apply it here:** Can the same timestamp, identifier or decimal value be parsed,
joined and compared consistently at both ends of the pipeline? Record the unit,
timezone and representation in the intake sheet.

## 3. Distributed failure

**Read:** [Time, Clocks and the Ordering of Events in a Distributed System](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/)
and [Jepsen](https://aphyr.com/tags/jepsen).

The point is not to become a distributed-systems specialist. It is to stop treating
ordering, retries, clocks and partial failure as edge cases once a model call or
database sits behind a network boundary. Block 8 already applies this to API
retries, idempotency and health checks.

**Apply it here:** What happens if the response is lost after the remote side has
done the work? What evidence distinguishes a delayed response from a failed write?
Answer those before adding a retry.

## 4. Maintaining existing code

**Read:** [Ship, Show, Ask](https://martinfowler.com/articles/ship-show-ask.html).

The course's generated lessons, notebooks and projects are maintained artefacts,
not disposable exercises. Small, reviewable changes and visible feedback make it
safer to change a working system than a large rewrite does.

**Apply it here:** Can you demonstrate the change with a focused test, fixture or
measurement before asking a reviewer to trust it? Start with the existing harness,
then change one thing and keep the rollback path. See [engineering practice](../lessons/engineering-practice/)
and the [measurement SOP](sop/measurement.md).

## What this map deliberately omits

It does not reproduce the source repository's catalogue, add a generic computer-
science block, or import platform-engineering and career material. Those are useful
elsewhere but do not improve the core ML/LLM build path enough to justify more
required work here.

The list that inspired this map is [Every Programmer Should Know](https://github.com/mtdvio/every-programmer-should-know),
licensed CC BY 4.0. This page is an independently written selection and application
map; the linked sources retain their own licences and terms.
