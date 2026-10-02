TITLE = "Block 8 · Deployment and APIs"
TOPIC = "block8-deployment"
ICON = "🚢"
DESCRIPTION = "Calling an interface you do not control, serving one other people do not control, and what changes the moment either has a caller who is not you."
TAGS = ["ai", "deployment", "apis"]
COLOR = "cyan"
CREATED = "2026-09-02"
ID_BASE = "1788100000"

LESSONS = [
{
  "slug": "calling-an-api-you-do-not-control",
  "title": "Calling an API You Do Not Control",
  "subtitle": "It will fail, it will be slow, and it will occasionally charge you twice for the same work.",
  "body": [
    ("p", "Every project in this course has called a model over HTTP and every one of them has done it naively, because the endpoint was on the same machine. That is a fair simplification for learning and a poor one for anything else. A remote interface fails in ways a local one does not, and the failures are boring rather than dramatic, which is why they get skipped."),

    ("h2", "Read the status code before deciding what to do"),
    ("p", "The single most useful habit is to stop treating errors as one category. What the caller should do next is almost entirely determined by which failure it was, and code that catches everything and retries treats a malformed request as a transient outage."),

    ("terms", [
      ("400 and 422 — you sent something wrong",
       "Never retry",
       "The request is malformed or fails validation. Retrying sends the same wrong thing again, and does so as fast as the loop allows. These belong in a log with the payload, not in a retry."),
      ("401 and 403 — you are not allowed",
       "Never retry",
       "A credential problem does not resolve itself. Retrying a 401 in a loop is how a key gets rate-limited or revoked."),
      ("429 — slow down",
       "Retry, but only when told",
       "The response usually carries a Retry-After header. Honour it. Backing off on your own schedule while ignoring the one you were handed is how a client makes an overload worse."),
      ("500 and 502 to 504 — their problem",
       "Retry with backoff",
       "Genuinely transient much of the time. This is the category exponential backoff exists for, and the only one where blind retrying is defensible."),
      ("Timeouts — you do not know",
       "The dangerous one",
       "You have no idea whether the work happened. The request may have completed and the response been lost, which is why this is the case that needs idempotency rather than a retry policy."),
    ]),

    ("know",
     "A timeout is not a failure. It is an absence of information.",
     "Every other error tells you something definite. A timeout tells you only that you stopped waiting, and the operation on the other side may have succeeded, failed, or still be running. Retrying is therefore a decision to possibly do the thing twice — which is free for a read, expensive for a paid generation, and unacceptable for anything that sends, charges or writes.",
     "A model call that times out at thirty seconds and is retried has plausibly been billed twice for one answer. The same pattern on an endpoint that emails a customer has sent two emails, and no amount of logging on your side will tell you which happened."),

    ("h2", "Hyrum's law, and why your output format is now a contract"),
    ("p", "<strong>Hyrum&#39;s law</strong>: with a sufficient number of users, every observable behaviour of your system will be depended on by somebody, regardless of what you promised. Not the documented interface &mdash; the <em>observable</em> one. Field ordering, whitespace, how long a list usually is, the fact that an optional field is always present in practice."),
    ("p", "This is sharper for a model-backed service than for an ordinary API, because a model emits far more observable behaviour than you specified. Nobody documented that the summary is usually three sentences, or that the reason field starts with a capital, or that refusals begin with a particular phrase &mdash; and downstream someone is splitting on it. Change the model version and those unwritten behaviours all move at once, which is why a model upgrade breaks consumers that the schema said were safe."),

    ("know",
     "Version the model as part of the interface, because your users are consuming behaviour you never promised.",
     "A pinned schema constrains the shape and says nothing about the distribution of what fills it. Two model versions can both satisfy the schema perfectly while differing in length, tone, refusal phrasing and how often an optional field appears &mdash; and each of those is something a consumer may have come to rely on. Treating the model version as an implementation detail is what makes an upgrade look like an outage nobody changed anything to cause.",
     "A service returns a category and a free-text justification. The schema never changes. A model upgrade shortens the justification from around forty words to around twelve, and a downstream dashboard that truncated at thirty starts showing complete sentences where it used to show ellipses &mdash; which a customer had been using to spot cases needing review."),

    ("h2", "Idempotency is the answer to the timeout"),
    ("p", "An idempotent operation produces the same result whether it runs once or five times. Most interfaces are not naturally idempotent, so the mechanism is a key: the caller generates a unique identifier per logical operation and sends it with every attempt, and the server recognises a repeat and returns the original result rather than doing the work again. The important half is that the key belongs to the <em>operation</em>, not to the attempt — a new key per retry defeats the entire mechanism."),

    ("figure", "The client cannot tell these apart, and the difference decides whether retrying is free or charges twice. An idempotency key makes the distinction irrelevant, which is the only reliable fix.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Two timeouts that look identical to the caller"><defs><marker id="api" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="14" y="26" width="120" height="36" rx="6" class="d-box"/><text x="26" y="49" class="d-label-sm">your request</text>
<path d="M134 44 L214 44" class="d-arrow-accent" marker-end="url(#api)"/>
<rect x="214" y="20" width="220" height="48" rx="6" class="d-box-accent"/><text x="226" y="40" class="d-label-b">work completed</text><text x="226" y="58" class="d-label-sm">response lost on the way back</text>
<rect x="14" y="112" width="120" height="36" rx="6" class="d-box"/><text x="26" y="135" class="d-label-sm">your request</text>
<path d="M134 130 L214 130" class="d-arrow-accent" marker-end="url(#api)"/>
<rect x="214" y="106" width="220" height="48" rx="6" class="d-box"/><text x="226" y="126" class="d-label-b">never arrived</text><text x="226" y="144" class="d-label-sm">nothing happened at all</text>
<path d="M434 44 L500 82" class="d-arrow-accent" marker-end="url(#api)"/>
<path d="M434 130 L500 96" class="d-arrow-accent" marker-end="url(#api)"/>
<rect x="500" y="66" width="126" height="44" rx="6" class="d-box"/><text x="512" y="86" class="d-label-b">timeout</text><text x="512" y="103" class="d-label-sm">identical to you</text>
<text x="14" y="188" class="d-label-sm">Retry the first and you pay twice. Retry the second and you get the answer. You cannot tell which you have.</text>
</svg>'''),

    ("h2", "Backoff, and the part everyone omits"),
    ("ul", [
      "<strong>Exponential</strong> — double the wait each attempt, so a struggling service is not hammered by every client at once.",
      "<strong>Jittered</strong> — the omitted part. Without randomisation every client that failed together retries together, and the retry storm is a second outage arriving on a schedule.",
      "<strong>Capped, and bounded in total</strong> — a maximum interval and a maximum number of attempts, because a caller retrying for an hour has turned a fast failure into a slow one.",
      "<strong>Budgeted</strong> — with a paid model behind the call, the retry policy is also a spending policy. Three attempts at a large prompt is three times the bill for one answer.",
    ]),

    ("callout", "pitfall", "Streaming changes what a failure looks like",
     "<p>A streamed response can fail after you have already shown the user half an answer. There is no clean status code for that — the connection simply stops. Decide in advance whether a truncated stream is discarded, retried from the start, or kept with a marker, and make sure the answer is not \"whatever the client library happens to do\", because that is usually to leave the partial text on screen looking complete.</p>"),
    ("related", ["after-it-ships", "where-the-money-goes", "serving-one-yourself", "routing-and-escalation"]),
    ("quiz", [
      ("Which failure category most needs idempotency rather than a retry policy?",
       ["429, because the rate limit may persist across retries",
        "A timeout, because you do not know whether the work happened — retrying is a decision to possibly do it twice",
        "500, because the server state may be inconsistent"],
       1),
      ("Why must an idempotency key belong to the operation rather than the attempt?",
       ["Keys are rate-limited per request",
        "A fresh key on each retry looks like a new operation to the server, which defeats the entire mechanism",
        "The server caches keys for a fixed window"],
       1),
      ("What does jitter add to exponential backoff?",
       ["A longer average wait, reducing load further",
        "Randomisation, so clients that failed together do not all retry together and create a second outage",
        "Protection against clock skew between client and server"],
       1),
    ]),
  ],
},
{
  "slug": "serving-one-yourself",
  "title": "Serving One Yourself",
  "subtitle": "The concerns that appear the moment the caller is not you — worked against Project 4.",
  "body": [
    ("p", "Project 4 exists to make this lesson concrete. It is Project 2's retrieval behind an interface, and almost none of the code it added is retrieval. That difference is the subject: a notebook may assume one caller, a trusted question, unlimited time and a failure only you see, and a service may assume none of those."),

    ("terms", [
      ("Authentication", "Because it is reachable",
       "A public endpoint is called by whoever finds it, and things get found. Return the same response for a missing key and a wrong one, so the endpoint does not confirm which keys exist."),
      ("Rate limiting, per caller", "Because a model call is not free",
       "The limit exists for the bill rather than the processor. Per key rather than globally, or one enthusiastic caller denies service to everyone else while staying inside a global limit."),
      ("Validation with bounds", "Because inputs are attacker-controlled",
       "Question length and retrieved-chunk count are capped in Project 4 specifically because context is cost. An unbounded parameter that multiplies tokens is a way for a caller to spend your money."),
      ("A health check that means something", "Because uptime is not readiness",
       "Report whether the dependencies are reachable, and return 503 when they are not. A check that returns 200 whatever the state of the thing it fronts answers the question &ldquo;is something listening&rdquo;, which nobody was asking."),
      ("A version in the path", "Because the contract will change",
       "Project 4 serves /v1/ask. The cost is nothing today and it is the difference between shipping a change and breaking every caller."),
      ("Generic error responses", "Because exceptions leak",
       "A stack trace or exception message returned to a caller is the cheapest way to disclose a path, a hostname or a library version. Log the detail, return the category."),
    ]),

    ("know",
     "Refuse to start misconfigured rather than starting with an unsafe default.",
     "Project 4 raises on startup when its key list is empty, and the reason is that the alternative is worse in a specific way: a default open configuration works perfectly in development, ships unchanged, and fails only when someone finds it. A service that will not boot is discovered by the person deploying it, in the minute they deploy it, which is the cheapest possible moment.",
     "The same logic covers a default admin key, a default allow-all origin, and a debug flag defaulting to on. If the safe value cannot be a default, absence should be an error rather than a fallback."),

    ("figure", "Everything outside the dashed box exists because the caller is not you. Project 4 is roughly forty lines of retrieval and two hundred of this.", '''<svg viewBox="0 0 640 208" role="img" aria-label="What a service adds around the same logic"><rect x="14" y="14" width="612" height="150" rx="8" class="d-box"/>
<rect x="216" y="70" width="200" height="46" rx="6" class="d-box-accent" stroke-dasharray="5 4"/><text x="230" y="90" class="d-label-b">the actual work</text><text x="230" y="108" class="d-label-sm">retrieve, then answer</text>
<text x="30" y="42" class="d-label-sm">auth</text><text x="30" y="62" class="d-label-sm">rate limit</text><text x="30" y="82" class="d-label-sm">validation</text><text x="30" y="102" class="d-label-sm">bounded params</text>
<text x="470" y="42" class="d-label-sm">versioned path</text><text x="470" y="62" class="d-label-sm">health check</text><text x="470" y="82" class="d-label-sm">generic errors</text><text x="470" y="102" class="d-label-sm">startup refusal</text>
<text x="216" y="146" class="d-label-sm">load once at start, not per request</text>
<text x="14" y="186" class="d-label-sm">A notebook is the dashed box. A service is the whole rectangle, and the rectangle is where the incidents are.</text>
</svg>'''),

    ("callout", "matters", "Load the model once, at start",
     "<p>A handler that loads an encoder or opens a connection per request pays that cost on every call and times out on the first one. Project 4 does it in a startup hook, which also gives the health check something true to report: the service is ready because loading finished, not because a process exists.</p>"),
    ("related", ["the-image-is-the-unit", "serving-locally", "calling-an-api-you-do-not-control", "latency-and-caching"]),
    ("quiz", [
      ("Why should a wrong API key and a missing one produce identical responses?",
       ["It simplifies the error-handling code",
        "Different responses confirm which keys exist, which turns the endpoint into an oracle for guessing them",
        "Clients cannot distinguish them anyway"],
       1),
      ("What is wrong with a health check that always returns 200?",
       ["It cannot express partial degradation",
        "It answers whether something is listening rather than whether the service can do its job, so a broken dependency looks healthy",
        "Load balancers require a body in the response"],
       1),
    ]),
  ],
},
{
  "slug": "the-image-is-the-unit",
  "title": "The Image Is the Unit",
  "subtitle": "What goes inside, what stays configuration, and why the size is a design decision rather than an outcome.",
  "body": [
    ("p", "A container is not a packaging step at the end. What you choose to put inside it decides what &ldquo;the system&rdquo; means — whether it is the code plus a hope about the environment, or something that behaves the same wherever it runs."),

    ("h2", "Inside or configured"),
    ("terms", [
      ("Code and dependencies", "Inside, pinned",
       "Pinned versions, and dependencies installed in a layer before the code is copied, so a code change does not reinstall them. Unpinned dependencies mean the image built today and the image built next week are different systems with the same tag."),
      ("Data the system is defined by", "Inside, usually",
       "Project 4 bakes its corpus in, because it is generated by a seeded script and versioned with the code. The image is then the whole system rather than the code plus an assumption about what is mounted."),
      ("Anything environment-specific", "Configured",
       "Endpoints, limits, feature flags. Project 4 learned this the hard way: it resolved its corpus path relative to the repository, which was correct outside the container and wrong inside it."),
      ("Secrets", "Configured, never inside",
       "A key in an image is in every layer, every registry copy and every developer's cache, and removing it in a later layer does not remove it from the earlier one."),
    ]),

    ("know",
     "Image size is a design decision, and the deployment project is where it stops being free.",
     "Project 4 retrieves by keyword rather than by embedding, and the reason is the image: the embedding pipeline needs a deep-learning framework and turns roughly two hundred megabytes into several gigabytes. That is slower to build, slower to pull, more expensive to store, and larger to attack. It is a defensible trade in either direction — the point is that it is a trade, decided deliberately, with a cost written down.",
     "The cost here is real and named in the project's README: answers are worse than Project 2's where the question's wording differs from the corpus. A deployment that quietly performs worse than the notebook it came from, with nobody having decided that, is the failure this avoids."),

    ("figure", "The left column travels with the artefact and is the same everywhere it runs. The right column differs per environment, which is exactly why it must not be baked in.", '''<svg viewBox="0 0 640 180" role="img" aria-label="What belongs inside an image and what stays configuration"><rect x="14" y="18" width="290" height="132" rx="8" class="d-box-accent"/>
<text x="28" y="42" class="d-label-b">inside the image</text>
<text x="28" y="66" class="d-label-sm">code · pinned dependencies</text>
<text x="28" y="86" class="d-label-sm">data the system is defined by</text>
<text x="28" y="106" class="d-label-sm">the non-root user</text>
<text x="28" y="132" class="d-label-sm">identical wherever it runs</text>
<rect x="336" y="18" width="290" height="132" rx="8" class="d-box"/>
<text x="350" y="42" class="d-label-b">configured at run</text>
<text x="350" y="66" class="d-label-sm">endpoints · paths · limits</text>
<text x="350" y="86" class="d-label-sm">secrets, always</text>
<text x="350" y="106" class="d-label-sm">anything environment-specific</text>
<text x="350" y="132" class="d-label-sm">differs per deployment</text>
</svg>'''),

    ("h2", "Two habits that cost nothing"),
    ("ul", [
      "<strong>Run as a non-root user.</strong> A container running as root has isolated your filesystem from you and not from whatever reaches the process. One line in the Dockerfile.",
      "<strong>Give it a real healthcheck instruction.</strong> The orchestrator can only restart what it can tell is broken, and the default is to assume a running process is a working one.",
    ]),

    ("callout", "pitfall", "The same image, or you have tested nothing",
     "<p>The value of building an image is that the artefact you tested is the artefact that runs. Rebuilding from source at deploy time, or applying a different configuration path in production, throws that away and returns you to hoping the environments match. Promote the image; change only the configuration.</p>"),
    ("related", ["serving-one-yourself", "sandboxing-and-what-actually-works", "version-control-basics", "after-it-ships"]),
    ("quiz", [
      ("Why does Project 4 bake its corpus into the image rather than mounting it?",
       ["Mounted volumes are slower to read",
        "The corpus is generated by a seeded script and versioned with the code, so including it makes the image the whole system rather than the code plus an assumption",
        "The container has no persistent storage"],
       1),
      ("Why is deleting a secret in a later Dockerfile layer ineffective?",
       ["Layer deletion is not supported by the image format",
        "The earlier layer still contains it, and that layer exists in every registry copy and local cache of the image",
        "Environment variables persist across layers"],
       1),
    ]),
  ],
},
{
  "slug": "after-it-ships",
  "title": "After It Ships",
  "subtitle": "What to watch, what to wake someone for, and the difference between the service being up and the service being right.",
  "body": [
    ("p", "A deployed system generates a new class of question that no amount of pre-deployment testing answers, because the traffic is real and the failures are the ones nobody imagined. This lesson is about what to watch, and it inherits its discipline from Block 5: a dashboard nobody has decided how to read is decoration."),

    ("h2", "Two different questions, often confused"),
    ("terms", [
      ("Is it up?", "Cheap, and nearly always answered",
       "Process alive, requests returning, latency within bounds. Every monitoring setup covers this because it is easy, and it is the question that matters least."),
      ("Is it right?", "Expensive, and usually not answered",
       "Are the answers still grounded, still correct, still refusing when they should? A system can be perfectly available and quietly wrong for weeks, and nothing in the first question detects it."),
    ]),

    ("know",
     "Availability monitoring cannot see a model that has started answering badly.",
     "Every request returns 200 in a reasonable time. Latency is flat, the error rate is zero, and the answers have drifted — because the corpus changed, or the model was updated, or the traffic moved to questions the retrieval was never good at. Traditional monitoring is blind to this by construction, because nothing about it is an error. The only thing that catches it is running your eval set against production on a schedule and watching the number rather than the uptime.",
     "This is Block 5's battery, pointed at the deployed instance instead of at a branch. The same fixed cases, the same criteria, run nightly. When the score moves and no deploy explains it, something upstream changed."),

    ("figure", "The left column is what monitoring gives you by default and the right column is what decides whether the system is doing its job. Almost every setup has the left and not the right.", '''<svg viewBox="0 0 640 190" role="img" aria-label="Availability signals against correctness signals"><rect x="14" y="20" width="290" height="130" rx="8" class="d-box"/>
<text x="28" y="44" class="d-label-b">is it up — cheap, always built</text>
<text x="28" y="70" class="d-label-sm">request rate · error rate</text>
<text x="28" y="90" class="d-label-sm">latency percentiles</text>
<text x="28" y="110" class="d-label-sm">saturation · restarts</text>
<text x="28" y="134" class="d-label-sm">all green while answers rot</text>
<rect x="336" y="20" width="290" height="130" rx="8" class="d-box-accent"/>
<text x="350" y="44" class="d-label-b">is it right — the one that lapses</text>
<text x="350" y="70" class="d-label-sm">eval battery, run on a schedule</text>
<text x="350" y="90" class="d-label-sm">refusal rate · groundedness</text>
<text x="350" y="110" class="d-label-sm">cost per request · truncations</text>
<text x="350" y="134" class="d-label-sm">moves before anyone complains</text>
<text x="14" y="178" class="d-label-sm">A page for the left. A dashboard read weekly for the right. Confusing the two produces alarms nobody trusts.</text>
</svg>'''),

    ("h2", "Four ways to put a change in front of traffic"),
    ("p", "Everything above assumes the new version is already serving. How it got there is a separate decision, and the options differ in what they risk and what they can measure. The evaluation block argued that a held-out set is not the same as production; these are the ways to get production evidence without betting production on it."),

    ("terms", [
      ("Shadow deployment", "Runs on real traffic, serves nothing",
       "The new version receives a copy of every live request and its output is logged and discarded. Zero user risk, real inputs, and it is the only one of these that can be run for as long as you like before anyone is affected."),
      ("Canary release", "A small slice of real users",
       "Route a few per cent of traffic to the new version, watch the metrics, widen if they hold. Real risk, bounded by the slice, and the first option here that can measure anything about user behaviour."),
      ("Interleaved comparison", "Both versions in one response",
       "For ranked output, mix results from both models into a single list and see which side earns the clicks. Far more sensitive than splitting users, because each user acts as their own comparison &mdash; the pairing argument from the evaluation block, applied to deployment."),
      ("Blue-green deployment", "Two full environments, one switch",
       "Stand the new version up alongside the old, cut traffic across, and keep the old one warm to cut back to. This is a rollback strategy rather than an evaluation one: it makes reverting fast, and tells you nothing before the switch."),
    ]),

    ("know",
     "Shadow deployment is the one people skip, and it is the only way to see how a change behaves on the inputs you never imagined.",
     "A held-out set contains the cases you thought to collect. Production contains the malformed requests, the enormous documents, the encoding no one anticipated and the traffic pattern at three in the morning. Running the new version against all of it while serving none of it separates &ldquo;does it work&rdquo; from &ldquo;does it work here&rdquo;, at no risk, before a single user is exposed. What it cannot tell you is whether people <em>prefer</em> the output, which is what the canary and the interleaved comparison are for.",
     "A retrieval change passes the eval set at 94 per cent. Shadowed against a week of live traffic it errors on 0.3 per cent of requests &mdash; all of them documents above a size the eval set never contained. Nobody saw an error, because nobody was served the shadow output, and the fix shipped before the canary started."),

    ("callout", "pitfall", "A shadow that writes is not a shadow",
     "<p>The guarantee only holds if the shadowed path has no effects. If the new version calls a tool that sends, charges, records or deletes, it is running in production regardless of whether anyone reads its answer &mdash; and the same is true of anything that mutates a shared cache or index. Run shadows with write access removed rather than with writes merely unused, which is the least-privilege argument from the security block arriving in a place people do not expect it.</p><p>Watch the cost too. A shadow doubles inference volume for as long as it runs, and on a paid model that is a real bill for output nobody reads.</p>"),

    ("h2", "What deserves waking someone"),
    ("p", "Alert on the things that are both urgent and actionable, and put everything else on a dashboard somebody reads on a schedule. A page that fires for a condition nobody can act on at three in the morning trains people to ignore pages, which costs more than the alert ever saved."),

    ("ul", [
      "<strong>Page:</strong> the service is down, the dependency is unreachable, the error rate has stepped, spend has crossed a ceiling.",
      "<strong>Dashboard, read weekly:</strong> eval score, refusal rate, groundedness, cost per request, latency distribution, the mix of question types.",
      "<strong>Neither:</strong> anything with no decision attached to it. Collect it if it is cheap, but a metric nobody would act on is not monitoring.",
    ]),

    ("callout", "matters", "Drift has its own lesson, and this is where it lands",
     "<p>Block 0 covers why a deployed model degrades — the world moves, the traffic changes, the inputs stop resembling what you tested. What this block adds is that you will not notice unless something is measuring correctness on a schedule. Drift is not detected by the system getting worse; it is detected by a number you chose to keep watching.</p>"),
    ("related", ["drift", "telemetry-and-instrumentation", "where-evaluation-lives", "calling-an-api-you-do-not-control"]),
    ("quiz", [
      ("Why can a system be perfectly available and still be failing?",
       ["Availability metrics are typically sampled too coarsely",
        "Answering badly is not an error — every request returns 200 in good time, so availability monitoring is blind to it by construction",
        "Latency and correctness are inversely correlated"],
       1),
      ("What separates something that should page from something that belongs on a dashboard?",
       ["How severe the consequence is",
        "Whether it is both urgent and actionable — paging for something nobody can act on now trains people to ignore pages",
        "Whether it can be measured automatically"],
       1),
    ]),
  ],
},
{
  "slug": "the-artefact-is-code-data-and-config",
  "title": "The Artefact Is Code, Data and Configuration",
  "subtitle": "A model file is not a deployment; behaviour only becomes reproducible when its inputs and assumptions travel with it.",
  "body": [
    ("p", "A commit identifies the program, not the behaviour. The same training code against a changed dataset, a different base model or a new preprocessing rule can produce a different system while every source file looks unchanged. Treat the deployable unit as a small bundle: code, model weights, data identity and configuration."),

    ("figure", "A rollback is only real when every input that shaped behaviour can be named and retrieved.", '''<svg viewBox="0 0 640 190" role="img" aria-label="A model release made from code, data, weights and configuration"><rect x="18" y="26" width="136" height="52" rx="7" class="d-box"/><text x="86" y="48" class="d-label-b" text-anchor="middle">code</text><text x="86" y="66" class="d-label-sm" text-anchor="middle">commit</text><rect x="176" y="26" width="136" height="52" rx="7" class="d-box"/><text x="244" y="48" class="d-label-b" text-anchor="middle">data</text><text x="244" y="66" class="d-label-sm" text-anchor="middle">manifest + hash</text><rect x="334" y="26" width="136" height="52" rx="7" class="d-box"/><text x="402" y="48" class="d-label-b" text-anchor="middle">weights</text><text x="402" y="66" class="d-label-sm" text-anchor="middle">immutable URI</text><rect x="492" y="26" width="130" height="52" rx="7" class="d-box"/><text x="557" y="48" class="d-label-b" text-anchor="middle">config</text><text x="557" y="66" class="d-label-sm" text-anchor="middle">schema + limits</text><path d="M86 86 L557 86" class="d-arrow-accent"/><rect x="154" y="112" width="332" height="48" rx="7" class="d-box-accent"/><text x="320" y="134" class="d-label-b" text-anchor="middle">reproducible release</text><text x="320" y="151" class="d-label-sm" text-anchor="middle">promote, compare, or roll back as one unit</text></svg>'''),

    ("h2", "Make the identity cheap to record"),
    ("p", "A dataset version does not need a heavyweight platform for a small project. Start with a manifest containing file paths, row counts, schema, generation seed, source revision and a content hash. Store that manifest beside the run record. The point is not the brand of registry; it is being able to answer which exact bytes trained the weights."),
    ("know",
     "If you cannot name the data that produced a model, you cannot reproduce or safely roll it back.",
     "A model artefact without its dataset identity is like a binary without its compiler inputs: you may be able to run it, but you cannot explain why it behaves differently or rebuild it when the file is lost. A manifest and hash turn an informal promise into a checkable identity.",
     "The maintenance model improves from 0.71 to 0.76 after a retrain. The run record points to commit abc123 and dataset hash 9f2e. When the score later falls, the team can fetch that exact pair, rerun it, and determine whether the change came from code, data or the serving environment."),

    ("h2", "Three tests, three different questions"),
    ("terms", [
      ("Training-system test", "Did the pipeline execute the intended work?", "Checks loading, splitting, preprocessing, checkpoint writing and artefact metadata. It should fail quickly without requiring a full expensive run."),
      ("Validation test", "Does the candidate meet the measured bar?", "Runs the frozen evaluation set and compares the candidate with the incumbent using the metric and slices chosen before the run."),
      ("Functionality test", "Does the service still behave on known cases?", "Uses a few named fixtures to catch schema, refusal, routing and preprocessing regressions that an aggregate score can hide."),
    ]),
    ("p", "These tests are complementary. A pipeline can finish successfully while training on the wrong split; a model can clear the aggregate score while losing a critical slice; an API can answer the right cases offline while failing to load its corpus in the container. The test suite should make each failure legible rather than calling all of them 'the model failed'."),
    ("callout", "pitfall", "A green test suite that never reached the model is not evidence",
     "Keep one readiness check that proves the real dependency path: the artefact loads, the data identity matches the run record, and one prediction travels through the same entry point production uses. Mock the expensive call where appropriate, but do not let every test mock away the thing it claims to protect."),
    ("h2", "Measure the serving boundary"),
    ("p", "The prediction function and the HTTP service have different failure modes. Measure both: correctness belongs to the prediction path; throughput, queueing, p95 latency, memory and error handling belong to the service. Run a small local load sweep and record the concurrency, payload, model revision and machine state with the results. A single fast request is not a capacity estimate."),
    ("links", [
      ("Production-Level Deep Learning", "https://github.com/alirezadir/Production-Level-Deep-Learning", "Source for the production-system framing; this lesson is independently written and measured here."),
      ("Full Stack Deep Learning", "https://fullstackdeeplearning.com/", "Upstream source credited by the repository for the code-plus-data and production lifecycle ideas."),
    ]),
    ("related", ["the-image-is-the-unit", "after-it-ships", "where-evaluation-lives", "the-artifact-and-when-to-retrain"]),
    ("quiz", [
      ("What must accompany a model weight file for a reproducible release?", ["Only the latest source commit", "The code, data identity and configuration that shaped its behaviour", "A larger validation set"], 1),
      ("Which test catches a container that starts but cannot load its corpus?", ["A functionality or readiness test through the deployed entry point", "A training-system test on a different machine", "A larger aggregate evaluation set"], 0),
      ("Why is one successful request not a capacity estimate?", ["It says nothing about queueing, concurrency or tail latency", "The response may be cached", "Single requests are never valid"], 0),
    ]),
  ],
},
]
