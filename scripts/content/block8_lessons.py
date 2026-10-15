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
    ("related", ["after-it-ships", "where-the-money-goes", "when-the-provider-goes-down", "routing-and-escalation"]),
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
{
  "slug": "managed-cloud-surfaces",
  "title": "Managed Cloud Surfaces",
  "subtitle": "Calling a model through Amazon Bedrock, Google Vertex AI or Microsoft Foundry keeps the request in your hands and the capacity, the cache and the calendar in the provider's.",
  "body": [
    ("p", "The first lesson in this block treated a model API as a service you do not control. The big three clouds sell the same models behind a managed surface: Amazon Bedrock, Google Vertex AI and Microsoft Foundry. Each adds an account, a billing meter, a region choice and a set of policy features. The useful question is not which one is best. It is which parts of the behaviour you can still set, and which have moved into the provider."),
    ("callout", "warning", "Read this as shapes, not numbers",
     "Everything here was read from provider documentation on 2026-10-10 through a summarising fetch tool. No dollar price was obtainable from any of the three, so none appears. Default quota values, latency targets and several retention periods were not retrieved and are left out rather than guessed. Model names, multipliers and dates change; treat every figure as dated."),

    ("figure", "Control follows the request and the account. Capacity, cache internals and retirement dates follow the provider.", '''<svg viewBox="0 0 640 230" role="img" aria-label="What a team keeps and what the provider keeps on a managed model API"><rect x="14" y="14" width="296" height="196" rx="8" class="d-box"/><text x="162" y="38" class="d-label-b" text-anchor="middle">You keep</text><text x="30" y="66" class="d-label-sm">which model and version you call</text><text x="30" y="88" class="d-label-sm">prompt layout and max_tokens</text><text x="30" y="110" class="d-label-sm">region or profile you route through</text><text x="30" y="132" class="d-label-sm">retries and fallbacks</text><text x="30" y="154" class="d-label-sm">guardrail settings, log destinations</text><text x="30" y="176" class="d-label-sm">whether to buy reserved capacity</text><text x="30" y="198" class="d-label-sm">the regression suite for a model swap</text><rect x="330" y="14" width="296" height="196" rx="8" class="d-box d-fill-amber"/><text x="478" y="38" class="d-label-b" text-anchor="middle">The provider keeps</text><text x="346" y="66" class="d-label-sm">hardware and routing inside your scope</text><text x="346" y="88" class="d-label-sm">quota values and whether they rise</text><text x="346" y="110" class="d-label-sm">how the quota is counted</text><text x="346" y="132" class="d-label-sm">cache storage and eviction</text><text x="346" y="154" class="d-label-sm">the models behind safety filters</text><text x="346" y="176" class="d-label-sm">abuse-monitoring carve-outs</text><text x="346" y="198" class="d-label-sm">the retirement date of every model</text></svg>'''),

    ("h2", "Quota is counted differently from the bill"),
    ("p", "All three providers throttle with HTTP 429. Two document how the quota is counted, and in both the number that limits you is not the number you are billed for. Bedrock deducts the input tokens plus <code>max_tokens</code> when a request starts, then refunds the unused part when it finishes. Foundry's tokens-per-minute check likewise uses an estimate of the maximum tokens at the moment the request arrives, and its page says that is not the count used for billing."),
    ("p", "Bedrock also multiplies output tokens when it counts them against quota: its page lists 15x for one model family, 10x for several current ones, 5x for older Anthropic models and 1:1 for all others. Its worked example has 3,000 input tokens, 1,000 cache-write tokens, 1,000 output tokens and a <code>max_tokens</code> of 32,000. The initial deduction is 36,000 tokens and the final one is 9,000. With a <code>max_tokens</code> of 1,250 the same request starts at 5,250. A generous output cap can throttle you before the model has written anything."),
    ("know",
     "Set max_tokens to what the task needs, not to the largest value the API allows.",
     "On Bedrock and Foundry the quota check reserves your output cap at the start of the request. An oversized cap reserves capacity you will not use, so concurrent requests are rejected earlier than their real size would suggest, and the bill never shows the reason.",
     "A summariser that returns about 300 tokens is configured with a cap of 32,000. Each request reserves roughly 32,000 tokens of quota while it runs, so a handful of concurrent calls hit a 429 on a quota that would have carried dozens at a cap of 1,000."),
    ("callout", "pitfall", "A 429 is not always your quota",
     "Bedrock separates its 429 (account quota) from its 503 and 529 (capacity on the provider's side). Google says a pay-as-you-go 429 on Vertex AI does not mean you hit a fixed quota, because that traffic runs on shared capacity. Foundry documents temporary reductions of your effective limit when a shared pool is under pressure. Log the status and the response headers, because raising a quota will not fix a capacity error."),

    ("h2", "Reserved capacity buys throughput, and few pages promise latency"),
    ("terms", [
      ("Bedrock", "Model units, or a Reserved tier", "Provisioned Throughput is hourly capacity per model with no commitment, one month or six months. A newer Reserved service tier states a 99.5% uptime target and overflows to the Standard tier. Whether Provisioned Throughput itself carries a latency or availability guarantee is not stated on its page."),
      ("Vertex AI", "Generative AI Scale Units (GSUs)", "A fixed-term subscription of one week, one month, three months or one year. Fees cannot be cancelled and apply regardless of usage. By default overage is billed as pay-as-you-go, and a request header can force a 429 instead. SLA terms were not retrieved."),
      ("Foundry", "Provisioned Throughput Units (PTUs)", "Capacity held for your deployment whether or not you send requests, with a defined latency target per model. The numeric targets sit on a sizing page that was not retrieved. Holding PTU quota does not guarantee that capacity exists in the region."),
    ]),
    ("p", "Reservation changes who pays for idle time, not who owns the failure. Even with reserved capacity a deployment can reach full utilisation, so the retry or spillover path still has to exist."),

    ("h2", "Caching and batching: you shape the prompt, they own the cache"),
    ("p", "Prompt caching is best effort on all three, and the only lever you hold is putting the stable part of the prompt first. Foundry needs an identical prefix of at least 1,024 tokens. Bedrock publishes per-model minimums between 512 and 4,096 tokens, and says an identical prompt does not guarantee a hit, so you verify with the cache-read and cache-write token counts in the response. Cache writes can cost more than uncached input on newer models, so a prompt that never repeats can cost more with caching switched on."),
    ("p", "Batch is the cheapest option and has the weakest timing promise. Vertex AI and Foundry both describe a 24-hour target for their batch modes. Google says batch is excluded from the service-level objective. Foundry's own page both says it does not expire slow jobs and lists an <code>expired</code> status, so teach it as a target with no hard guarantee. Bedrock's batch turnaround time was not found."),

    ("h2", "Data: the defaults hold, with carve-outs you must read"),
    ("p", "Bedrock states that by default it does not store model inputs or outputs. The carve-outs are model-specific: for two named Anthropic models, traffic is retained for up to 30 days for automated abuse detection, and flagged traffic for a list of OpenAI models is retained for up to 30 days. A per-Region retention setting can refuse any model that requires retention."),
    ("p", "On Vertex AI, data at rest stays in the location you chose, but machine-learning processing is only guaranteed on regional and multi-region endpoints. The global endpoint may process in any Google Cloud location, and Google advises against it when you have processing-location requirements. The same endpoint can reduce 429 errors, so relieving throttling and keeping a residency promise pull in opposite directions. Foundry draws the same line by deployment type: Global may process in any Azure region, Data Zone inside the zone, and Standard or Regional inside the geography."),
    ("callout", "matters", "Logging creates a copy the provider did not keep",
     "Bedrock invocation logging is off by default and writes to your own storage. Vertex AI request-response logging is off by default and writes to BigQuery. Turning either on creates a copy of your prompts that the provider otherwise would not hold, and the retention policy of that copy is now yours. For Foundry, resource logs are not collected until you create a diagnostic setting. Whether those logs include prompt content was not confirmed."),

    ("h2", "Guardrails are provider-run filters you tune"),
    ("p", "Each provider offers content filtering, and none of it is a guarantee. Bedrock Guardrails evaluate input and output and can run on their own through an <code>ApplyGuardrail</code> call without invoking a model. AWS updates the models behind them automatically. If a guardrail blocks the output you still pay for the inference already generated. Foundry switches default filters on for its OpenAI models at a Medium threshold, and its classic page says that if the filter service is down or times out the request completes without filtering. Vertex AI's safety-filter default differs by model, and its own page lists both OFF and a medium threshold. Because the models behind these filters change without notice, a regression suite that includes refusals and edge cases is the control you own."),

    ("h2", "Retirement: the provider owns the calendar"),
    ("p", "Pinning a model version does not pin it forever. Foundry gives standard generally available (GA) models a retirement date 18 months out (12 months for some partner families) with at least 60 days' notice, and states that retirement dates are not extendable. A deployment set to <code>NoAutoUpgrade</code> stops working at retirement, and provisioned deployments are never upgraded automatically. Vertex AI commits that a retirement date may be extended but will not move earlier, and gives at least 45 days' notice for shorter-lived models. Bedrock moves a model from Active to Legacy to end of life; for models launched on or after 2026-09-07 the Legacy period is six months or 45 days, existing customers can lose access to a Legacy model after 15 days of inactivity, and at end of life nothing migrates automatically."),
    ("know",
     "Your regression suite must be re-runnable inside the shortest retirement notice you depend on.",
     "The provider sets the calendar and, on Foundry, says plainly that it cannot be extended. A swap you cannot evaluate within the notice window becomes a forced, unmeasured migration, and a rarely called fallback model can disappear before anyone notices.",
     "A fallback model called a few times a month is moved to Legacy on Bedrock. After 15 days without a call, access may lapse, well before the end-of-life date. The first sign is a failed request during a primary-model outage."),

    ("h2", "What was not retrieved"),
    ("ul", [
      "Every dollar price, from all three providers. The Foundry pricing page rendered placeholders and the Vertex AI page returned only its title.",
      "Default quota values, and numeric latency targets for reserved capacity.",
      "Bedrock batch turnaround, and any retention period for Azure abuse-monitoring data.",
      "The status of the older Azure AI Model Inference API, and Vertex AI's Priority and Flex pay-as-you-go semantics.",
      "Where the providers' own pages disagree, this lesson teaches the disagreement: Foundry names the retry header both <code>retry-after-ms</code> and <code>Retry-After</code>, and its pages list the Data Zone options as US or EU in one place and US, EU or APAC in another.",
    ]),
    ("links", [
      ("Bedrock: token counting and quota burndown", "https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html", "Source for the max_tokens deduction and the 36,000 and 9,000 example."),
      ("Bedrock: model lifecycle", "https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html", "Active, Legacy and end-of-life states and notice periods."),
      ("Bedrock: data retention", "https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html", "The per-Region retention setting."),
      ("Vertex AI: data residency", "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency", "Which endpoints guarantee a processing location."),
      ("Vertex AI: model versions and retirement", "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions", "Retirement dates and the commitment not to move them earlier."),
      ("Foundry: deployment types", "https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types", "Global, Data Zone, Standard, Provisioned and Batch, and where each processes data."),
      ("Foundry: model retirements", "https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements", "The 18-month and 12-month lifetimes and the 60-day notice."),
      ("Foundry: quota (classic portal page)", "https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/quota", "Source for the estimate-at-receipt token check. A classic-portal page dated 2026-05."),
    ]),
    ("related", ["calling-an-api-you-do-not-control", "serving-one-yourself", "after-it-ships", "latency-and-caching"]),
    ("quiz", [
      ("Why can an oversized max_tokens cause a 429 on Bedrock before the model has produced any output?", ["The quota check reserves input tokens plus max_tokens when the request starts", "Large caps disable prompt caching", "The provider bills the full cap in advance"], 0),
      ("A team picks the Vertex AI global endpoint to reduce 429 errors. What does it give up?", ["Access to Gemini models", "The guarantee of where machine-learning processing happens", "Prompt caching"], 1),
      ("What is the safest way to describe a provider's batch mode on Vertex AI or Foundry?", ["A 24-hour target with no hard real-time guarantee", "A guaranteed 24-hour turnaround", "Always faster than real-time inference"], 0),
      ("Why must a regression suite be re-runnable within the shortest retirement notice you depend on?", ["The provider sets the retirement date and may not extend it, so an unmeasured swap becomes forced", "Retired models are deleted from your account", "Notice periods are set by the customer"], 0),
    ]),
  ],
},
{
  "slug": "when-the-provider-goes-down",
  "title": "When the Provider Goes Down",
  "subtitle": "Failing over is a design with five rungs, a clock and a test, not a second API key in an environment variable.",
  "body": [
    ("p", "Every project in this course depends on a model someone else runs. The first lesson in this block covered one request: classify the status code, retry what is safe, back off with jitter. This lesson covers the other question, the one an interviewer actually asks: <em>what does your system do while the provider is not answering?</em> The honest answer has more parts than &ldquo;switch to another provider&rdquo;, and the first part is that &ldquo;down&rdquo; is rarely what happens."),

    ("h2", "Five ways a provider fails, and only one of them is an outage"),
    ("terms", [
      ("Hard down", "Connection refused, 5xx on every call", "The case everyone designs for, and the rarest. It is also the only one where switching immediately is obviously right."),
      ("Throttled", "429, or a quota you did not know you had", "The provider is up and is refusing you. Switching providers does not fix a quota problem; it moves the same traffic somewhere that has its own quota and its own bill."),
      ("Slow", "Answers arrive, after a timeout you set", "The most common failure and the hardest to see. Nothing errors. The p99 latency has doubled and every request waits for it."),
      ("Partial", "One model, one region or one feature fails", "The status page says operational. Your model in your region is the part that is not. The fix is usually another model or region at the same provider, not another provider."),
      ("Degraded", "It answers, and the answers got worse", "A silent model update, a changed safety filter, a structured-output mode that now truncates. No error code exists for this, so no failover trigger fires. Only your own evaluation notices."),
    ]),
    ("p", "A failover design is a table of these five against a response. If the plan only has a column for the first one, it is a plan for the failure that rarely occurs."),

    ("figure", "A request walks down the ladder only as far as it has to. Each rung changes something the caller may depend on, so each one needs to be chosen, evaluated and exercised before the day it is needed.", '''<svg viewBox="0 0 640 330" role="img" aria-label="The fallback ladder: primary model, same model in another region, another provider, smaller model, cached or retrieval-only answer, honest error"><defs><marker id="fo" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-muted"/></marker></defs>
<rect x="14" y="12" width="250" height="40" rx="7" class="d-box-good"/><text x="28" y="37" class="d-label-b">1 · Primary model</text>
<rect x="14" y="66" width="250" height="40" rx="7" class="d-box"/><text x="28" y="91" class="d-label-b">2 · Same model, other region</text>
<rect x="14" y="120" width="250" height="40" rx="7" class="d-box"/><text x="28" y="145" class="d-label-b">3 · Another provider, same tier</text>
<rect x="14" y="174" width="250" height="40" rx="7" class="d-box"/><text x="28" y="199" class="d-label-b">4 · Smaller or local model</text>
<rect x="14" y="228" width="250" height="40" rx="7" class="d-box-warn"/><text x="28" y="253" class="d-label-b">5 · Stored answer or passages only</text>
<rect x="14" y="282" width="250" height="40" rx="7" class="d-box-warn"/><text x="28" y="307" class="d-label-b">6 · A plain, honest error</text>
<path d="M139 52 L139 66" class="d-arrow" marker-end="url(#fo)"/><path d="M139 106 L139 120" class="d-arrow" marker-end="url(#fo)"/><path d="M139 160 L139 174" class="d-arrow" marker-end="url(#fo)"/><path d="M139 214 L139 228" class="d-arrow" marker-end="url(#fo)"/><path d="M139 268 L139 282" class="d-arrow" marker-end="url(#fo)"/>
<text x="290" y="36" class="d-label-sm">Behaviour you tuned the prompt against.</text>
<text x="290" y="90" class="d-label-sm">Same behaviour; check residency and quota.</text>
<text x="290" y="144" class="d-label-sm">Different behaviour, different tool-call and</text><text x="290" y="158" class="d-label-sm">JSON quirks, a different data agreement.</text>
<text x="290" y="198" class="d-label-sm">Lower quality; some tasks now fail outright.</text>
<text x="290" y="252" class="d-label-sm">No generation: reuse an earlier answer, or return</text><text x="290" y="266" class="d-label-sm">the retrieved passages with a notice.</text>
<text x="290" y="306" class="d-label-sm">Better than a confident wrong answer.</text>
</svg>'''),

    ("h2", "Decide on a clock, not on an error"),
    ("p", "Failing over on errors alone misses the slow case entirely, because a slow provider returns no error. The trigger that works is a deadline: every request gets a time budget, measured from the p99 you have observed, and a request that exceeds it moves down a rung. Set the deadline at the p99 you measured and about one healthy request in a hundred still moves down a rung; set it below the median and the fallback becomes your primary path. Set it far above and every user waits through the failure before anything happens."),
    ("p", "A circuit breaker is what stops that wait repeating. After a run of consecutive failures it stops sending to the failing rung for a cool-down, then lets one probe request through, and closes again only when the probe succeeds. Without it, a provider that hangs for thirty seconds costs <em>every</em> request thirty seconds before it falls back, which is the outage nobody wrote a monitor for."),
    ("know",
     "Fail over on a measured deadline, and trip a breaker so later requests skip the broken rung.",
     "An error code only exists for the failures that announce themselves. A slow or degraded provider announces nothing, and without a breaker each request pays the full timeout again before reaching the fallback.",
     "A provider starts taking 30 seconds to respond instead of 2. With a 30-second timeout and no breaker, every user waits 30 seconds and then gets the fallback anyway. With a 6-second deadline and a breaker that opens after five consecutive timeouts, the breaker only learns of each failure when a deadline expires. If requests arrive one at a time, the first five users wait 6 seconds each. If they arrive together, everyone who arrives in those first 6 seconds waits too. Once the breaker is open, requests go straight to the fallback, apart from one probe after each cool-down."),
    ("callout", "pitfall", "A 429 is not a reason to switch provider",
     "A throttle means you sent more than you may. Sending the same traffic to a second provider doubles the places you can be throttled and the places you are billed, and can push the second provider over its own limit at the worst moment. Back off, shed the lowest-value traffic, or queue it. Fail over for hard-down and slow; treat throttling as a capacity problem."),

    ("h2", "A fallback is a different system"),
    ("p", "The whole risk of failover sits in a single assumption: that the next rung behaves like the one above it. A different provider's model follows a different instruction style, formats tool calls differently, and fails differently on your structured-output schema. A prompt tuned for one is not tuned for the other. The first time the fallback runs should not be during an outage."),
    ("ul", [
      "<strong>Evaluate every rung on your own set.</strong> Run the same private eval set through each fallback and record the score and the non-completion rate, as in the one-set-many-models lesson. Decide in advance which tasks are allowed to degrade and which must refuse instead.",
      "<strong>Check the data agreement.</strong> A second provider may sit in another region, under other retention terms, or outside what your customers consented to. Failing over silently can be a compliance event.",
      "<strong>Keep it alive.</strong> A fallback called rarely can be retired by its provider before anyone notices. Send it a small share of real or shadow traffic so the credentials, quota and model name are known to work.",
      "<strong>Watch the cost.</strong> A larger fallback model can multiply the bill during exactly the hours when you are least watching it. Set a budget cap on the fallback path.",
    ]),
    ("know",
     "A fallback you have never run on real traffic is a guess about how your system behaves.",
     "Each rung differs from the one above it in tool-call format, output shape, quality, residency, quota and price. None of those differences shows up until a request is actually sent, and during an outage is the worst time to discover them.",
     "A team keeps a second provider configured and never calls it. When the primary degrades, the fallback returns a tool call in a different shape, the parser rejects it, and every request fails twice: once at the provider and once in the code written to handle that."),

    ("h2", "Switching providers is an interface problem first"),
    ("p", "Moving from one AI provider to another fails in the plumbing before it fails in the model. Request shapes differ, and so do the way a system prompt is passed, how tools are declared, what a tool call looks like when it comes back, how a stop reason is named and how usage is counted. Code that calls one provider's client directly in forty places cannot fall back to another without editing all forty."),
    ("terms", [
      ("One narrow interface", "Your code calls yours, not theirs", "Define a small function of your own, such as <code>complete(messages, tools, schema, deadline)</code>, and put each provider behind an adapter that translates in both directions. The fallback ladder then becomes a list of adapters, and nothing else in the system knows which one answered."),
      ("A gateway", "The same idea, run as a service", "A proxy that exposes one API and routes to several providers, with the retry, deadline and breaker logic in one place. It saves writing adapters and adds a service that is now itself a single point of failure, so it needs its own fallback path."),
      ("A prompt per provider", "Portability is tested, not assumed", "Keep the prompt, the tool definitions and the output schema as data you can vary per rung. Evaluate each pairing on your own set. A prompt that scores well on one model can score noticeably lower on another with identical wording."),
      ("A record of who answered", "Every response names its rung", "Log the provider, model and version on every request. Without it a quality drop during a failover is indistinguishable from a bug, and the cost report cannot attribute the spend."),
    ]),
    ("callout", "matters", "Failover is also a contract and a security question",
     "A second provider needs its own agreement, its own key held in your secret store, its own data-retention terms and its own entry in your list of subprocessors. The key has to be live and the quota non-zero before the day you need it. An unsigned or unfunded fallback is a diagram, not a fallback."),

    ("h2", "Streaming makes the choice earlier"),
    ("p", "Once the first token has reached the user you cannot switch models without showing them two answers. Decide before streaming begins: wait for the first token under a short deadline, and if it does not arrive, fall back then. A failure after streaming has started is a different case, and the honest handling is to end the response with a visible notice rather than splice in a second model's answer."),

    ("h2", "The rung people forget: do not generate"),
    ("p", "For a RAG system the cheapest, safest fallback is not another model. It is to skip generation and return what retrieval already found: the top passages, their sources and a notice that the summary is unavailable. The user still gets the evidence. An exact-match cache of earlier answers is the same idea, and it carries none of the false-match risk of a similarity cache. Both avoid asking a second model to do a job it was never evaluated for. Label the reply, though. A <code>200</code> that carries passages looks like success to any client that checks only the status code, so make the degraded case opt-in, keep the passages out of the field a client would display as the answer, and add a flag the caller has to read. Project 4 does exactly this."),

    ("h2", "What to measure"),
    ("ul", [
      "Time to detect: how long between the first failure and the breaker opening.",
      "The share of traffic served by each rung, per hour. A rung that should be rare and is not is the alert.",
      "Quality of each rung on the eval set, re-run on a schedule, because a fallback model changes under you too.",
      "A recovery drill: switch the primary off on purpose in a test environment and read the trace.",
    ]),
    ("related", ["calling-an-api-you-do-not-control", "managed-cloud-surfaces", "after-it-ships", "designing-the-whole-system"]),
    ("links", [
      ("Google SRE Book: Handling Overload", "https://sre.google/sre-book/handling-overload/", "Why retrying and failing over can make an overload worse, and what load shedding is for."),
      ("Google SRE Book: Addressing Cascading Failures", "https://sre.google/sre-book/addressing-cascading-failures/", "How one failing dependency becomes a system-wide failure, and the timeout and breaker patterns that stop it."),
      ("Martin Fowler: Circuit Breaker", "https://martinfowler.com/bliki/CircuitBreaker.html", "The closed, open and half-open states in two screens."),
    ]),
    ("quiz", [
      ("A provider's responses start taking 30 seconds and return no errors. What detects it?",
       ["A failover rule that triggers on 5xx status codes",
        "A per-request deadline plus a circuit breaker",
        "The provider's status page"], 1),
      ("You hit repeated 429s from your primary provider. What is the best first response?",
       ["Send the same traffic to a second provider immediately",
        "Back off or shed the lowest-value traffic, because a throttle is a capacity problem",
        "Raise the request timeout"], 1),
      ("Why must a fallback model be evaluated before the outage?",
       ["Because it differs in tool-call shape, quality and behaviour, and nothing shows that until it is run",
        "Because fallback models are always cheaper",
        "Because providers require it"], 0),
      ("For a RAG system with the model unavailable, which fallback needs the least new evaluation?",
       ["A second provider's model",
        "Returning the retrieved passages with a notice, with no generation",
        "A smaller local model"], 1),
    ]),
  ],
},
{
  "slug": "designing-the-whole-system",
  "title": "Designing the Whole System: The Interview Questions",
  "subtitle": "Nine questions that keep coming up, a drawing from query to answer, and where this course teaches each part.",
  "body": [
    ("p", "A system-design question for an AI role is rarely about a framework. The interviewer wants to hear how you think: what you ask first, what you draw, where you expect it to fail and how you would know. The same questions recur. This lesson answers each in the shape a good answer takes, and points to the lesson that holds the detail. Nothing here is new material; it is the map from the questions to the course."),

    ("h2", "Start with numbers, not boxes"),
    ("p", "Before drawing anything, ask five things, because every later choice depends on them: how many documents and how often they change; how many queries a second; the latency a user will tolerate; what a wrong answer costs; and who may see which document. An answer that begins with &ldquo;it depends on these five&rdquo; is already ahead of one that begins with a vector database."),

    ("figure", "One query, left to right: guard it, try the cheap exits, retrieve and rerank, generate under a deadline with a fallback, check the answer against its sources. The ingestion path on the bottom feeds the index, and everything writes traces to the evidence store.", '''<svg viewBox="0 0 640 330" role="img" aria-label="A production retrieval-augmented generation architecture from user query to final response, with ingestion and observability"><defs><marker id="ds" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-muted"/></marker></defs>
<rect x="8" y="14" width="86" height="46" rx="6" class="d-box"/><text x="51" y="34" class="d-label-b" text-anchor="middle">User</text><text x="51" y="50" class="d-label-sm" text-anchor="middle">query</text>
<rect x="108" y="14" width="96" height="46" rx="6" class="d-box"/><text x="156" y="34" class="d-label-b" text-anchor="middle">Gateway</text><text x="156" y="50" class="d-label-sm" text-anchor="middle">auth, limits</text>
<rect x="218" y="14" width="96" height="46" rx="6" class="d-box-accent"/><text x="266" y="34" class="d-label-b" text-anchor="middle">Cache</text><text x="266" y="50" class="d-label-sm" text-anchor="middle">exact, then similar</text>
<rect x="328" y="14" width="96" height="46" rx="6" class="d-box"/><text x="376" y="34" class="d-label-b" text-anchor="middle">Rewrite</text><text x="376" y="50" class="d-label-sm" text-anchor="middle">query, route</text>
<rect x="438" y="14" width="96" height="46" rx="6" class="d-box"/><text x="486" y="34" class="d-label-b" text-anchor="middle">Retrieve</text><text x="486" y="50" class="d-label-sm" text-anchor="middle">hybrid, filtered</text>
<rect x="548" y="14" width="84" height="46" rx="6" class="d-box"/><text x="590" y="34" class="d-label-b" text-anchor="middle">Rerank</text><text x="590" y="50" class="d-label-sm" text-anchor="middle">top few</text>
<path d="M94 37 L108 37" class="d-arrow" marker-end="url(#ds)"/><path d="M204 37 L218 37" class="d-arrow" marker-end="url(#ds)"/><path d="M314 37 L328 37" class="d-arrow" marker-end="url(#ds)"/><path d="M424 37 L438 37" class="d-arrow" marker-end="url(#ds)"/><path d="M534 37 L548 37" class="d-arrow" marker-end="url(#ds)"/>
<path d="M590 60 L590 96 L486 96 L486 110" class="d-arrow" marker-end="url(#ds)"/>
<rect x="408" y="110" width="156" height="46" rx="6" class="d-box"/><text x="486" y="130" class="d-label-b" text-anchor="middle">Assemble context</text><text x="486" y="146" class="d-label-sm" text-anchor="middle">budget, order, cite</text>
<path d="M408 133 L370 133" class="d-arrow" marker-end="url(#ds)"/>
<rect x="214" y="110" width="156" height="46" rx="6" class="d-box-good"/><text x="292" y="130" class="d-label-b" text-anchor="middle">Generate</text><text x="292" y="146" class="d-label-sm" text-anchor="middle">deadline, fallback ladder</text>
<path d="M214 133 L176 133" class="d-arrow" marker-end="url(#ds)"/>
<rect x="20" y="110" width="156" height="46" rx="6" class="d-box-warn"/><text x="98" y="130" class="d-label-b" text-anchor="middle">Check</text><text x="98" y="146" class="d-label-sm" text-anchor="middle">grounded? else refuse</text>
<path d="M98 156 L98 176" class="d-arrow" marker-end="url(#ds)"/><text x="108" y="172" class="d-label-sm">answer with sources</text>
<rect x="20" y="214" width="190" height="46" rx="6" class="d-box"/><text x="115" y="234" class="d-label-b" text-anchor="middle">Ingestion</text><text x="115" y="250" class="d-label-sm" text-anchor="middle">parse, chunk, embed, version</text>
<path d="M210 237 L286 237 L286 290" class="d-arrow" marker-end="url(#ds)"/>
<rect x="226" y="290" width="180" height="32" rx="6" class="d-box-accent"/><text x="316" y="310" class="d-label-b" text-anchor="middle">Index</text>
<rect x="430" y="214" width="196" height="108" rx="6" class="d-box"/><text x="528" y="238" class="d-label-b" text-anchor="middle">Evidence store</text><text x="528" y="258" class="d-label-sm" text-anchor="middle">traces, scores, costs,</text><text x="528" y="274" class="d-label-sm" text-anchor="middle">cache hits, fallback rung,</text><text x="528" y="290" class="d-label-sm" text-anchor="middle">grounding failures</text>
<text x="316" y="282" class="d-label-sm" text-anchor="middle">read by Retrieve at query time</text>
</svg>'''),

    ("h2", "The nine questions"),
    ("terms", [
      ("1 · Design a production-ready RAG system", "Draw the figure above, then defend each box", "State the five numbers first. Draw ingestion and query paths separately. Say what fails at each box, and name what you would measure. The build is in <em>building-a-rag-system</em>, the retrieval stages in <em>ranking-and-hybrid-retrieval</em> and <em>transforming-the-query</em>, and the serving side in <em>serving-one-yourself</em>."),
      ("2 · RAG or fine-tuning?", "RAG for knowledge, tuning for behaviour", "Facts that change, must be cited or must be access-controlled belong in retrieval. A consistent format, tone or narrow skill belongs in tuning, and usually only after prompting and retrieval have been measured. This course ran the experiment: a tuned adapter lost to a lookup table. See <em>when-fine-tuning-is-wrong</em>."),
      ("3 · Reduce latency without hurting quality", "Find which phase is slow before touching anything", "Time to first token is prefill and grows with what you send, so retrieve fewer, better chunks and keep the prompt prefix stable. Throughput is decode. Stream the answer, rerank a small shortlist, and measure quality on your eval set after every change. See <em>latency-and-caching</em>."),
      ("4 · What if the provider goes down?", "A ladder, a clock and a rehearsal", "Classify the failure, fail over on a deadline with a circuit breaker, walk down tested fallbacks and end at the retrieved passages or an honest error. See <em>when-the-provider-goes-down</em> and <em>managed-cloud-surfaces</em>."),
      ("5 · Evaluate an AI system", "Separate the numbers, on your own data", "Report index recall, retrieval quality, groundedness and correctness separately, on a private gold set, with a non-completion column and a check that a difference is bigger than noise. See <em>where-evaluation-lives</em>, <em>eval-data-you-can-trust</em>, <em>is-the-difference-real</em> and the Project 2 report."),
      ("6 · Where to add caching", "Cheapest and safest first", "An exact-match answer cache, then provider prompt caching with the stable prefix first, then a similarity cache only where a wrong match is cheap and tenants never share it. See <em>latency-and-caching</em>."),
      ("7 · Prevent hallucinations", "You cannot, so you make them detectable", "Ground the answer in retrieved text, require citations, check each claim against its source, refuse when retrieval found nothing, and measure groundedness. See <em>hallucination-and-grounding</em> and <em>measuring-retrieval</em>."),
      ("8 · What to monitor", "Is it up, and is it right?", "Latency percentiles, error and fallback rates, cost per request and cache hit rate, plus a scheduled quality measurement on a fixed set, because drift shows up there first. See <em>after-it-ships</em>, <em>drift</em> and <em>telemetry-and-instrumentation</em>."),
      ("9 · Scale to millions of documents", "Do the memory sum, then partition", "Compute bytes per vector times rows, compress and rerank, partition by tenant or source, shard only when needed, and plan the re-index for the day the embedding model changes. See <em>retrieval-at-scale</em> and <em>vector-search-algorithms</em>."),
    ]),
    ("h2", "The follow-ups an interviewer asks in the room"),
    ("p", "Five follow-ups are worth rehearsing, because they come up mid-discussion. Four are the list above in the first person. One is new, and it is the one people answer worst."),
    ("terms", [
      ("Where would I store documents?", "Three stores, because three things need keeping", "Keep the <strong>original files</strong> in immutable, versioned object storage, so you can re-parse them. Keep the <strong>chunks, their metadata and their embeddings</strong> in the index, with the embedding model's name and version on every row. Keep <strong>who may see what</strong> as metadata on the chunk, applied as a filter at query time. This course keeps the index in Postgres with pgvector because the filter and the vectors then share one planner. See <em>vector-search-algorithms</em>."),
      ("How would retrieval work?", "Rewrite, hybrid search, rerank, then cite", "Transform the query, run keyword and vector search together with the access filter, fuse by rank, rerank a short list and pass the top few chunks with their sources. See <em>transforming-the-query</em> and <em>ranking-and-hybrid-retrieval</em>."),
      ("How would I reduce latency?", "Same as question 3", "Find the slow phase, send fewer tokens, stream, rerank less, cache the safe things."),
      ("What happens if OpenAI goes down?", "Same as question 4, for any provider", "Deadline, breaker, tested fallbacks, retrieved passages as the last useful answer."),
      ("How would I evaluate after deployment?", "Questions 5 and 8 together", "A fixed gold set re-run on a schedule, plus live traces sampled and scored, because a deployed system drifts and the first sign is rarely an error."),
    ]),
    ("p", "One more request is worth practising: <em>draw the complete architecture from user query to final response</em>. It is the figure above. Practise it on a blank page: the order of the boxes matters less than saying aloud, for each one, what it protects against."),

    ("h2", "How to give the answer"),
    ("ul", [
      "Ask the five numbers before drawing. If the interviewer will not give them, state your assumptions aloud and carry on.",
      "Put the measurement next to every decision. &ldquo;I would add a reranker&rdquo; is a guess; &ldquo;I would add a reranker if recall at 20 is good and precision at 5 is not&rdquo; is a design.",
      "Name the failure of your own design before the interviewer finds it.",
      "Say what you would build first, and what you would leave out until a measurement asked for it.",
    ]),
    ("know",
     "A design answer is a diagram plus, for every box, what it protects against and how you would know it failed.",
     "Naming components shows you have read about them. Naming the failure each one prevents and the number that would reveal it shows you can operate one, which is what the question is testing.",
     "Asked where to add a cache, a weak answer names a product. A strong one says: exact-match first because it cannot return a wrong answer; prompt caching with the stable prefix first; a similarity cache only for low-stakes questions and never shared across tenants; and measures the hit rate and the wrong-hit rate for each."),
    ("callout", "matters", "Where the course is thinner",
     "The course teaches each part and its failure modes against runnable projects. It does not give you practice at saying them aloud under time pressure. Projects 2 and 4 are the best raw material: explain their trade-offs out loud, and time yourself drawing the figure above from memory."),
    ("related", ["when-the-provider-goes-down", "retrieval-at-scale", "after-it-ships", "managed-cloud-surfaces"]),
    ("quiz", [
      ("An interviewer says &ldquo;design a RAG system&rdquo;. What should you do first?",
       ["Name a vector database", "Ask for the corpus size, query rate, latency budget, cost of an error and access rules", "Start with the prompt"], 1),
      ("Which fact most clearly points to retrieval rather than fine-tuning?",
       ["The answers must follow a fixed JSON format", "The facts change weekly and must be cited", "The tone must match the brand"], 1),
      ("Which cache is safest to add first?",
       ["A similarity cache shared across customers", "An exact-match answer cache", "A cache of embeddings only"], 1),
      ("Why report index recall, retrieval quality, groundedness and correctness separately?",
       ["A single score hides which stage is failing", "It makes the report longer", "Providers require it"], 0),
    ]),
  ],
},
]
