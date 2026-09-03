TITLE = "Block 9 · Electives"
TOPIC = "block9-electives"
ICON = "🧭"
DESCRIPTION = "Three directions the spine does not cover: what happens when the input is not text, how to ask the database properly, and where the money actually goes."
TAGS = ["ai", "electives", "cost"]
COLOR = "amber"
CREATED = "2026-09-02"
ID_BASE = "1788200000"

LESSONS = [
{
  "slug": "when-the-input-is-not-text",
  "title": "When the Input Is Not Text",
  "subtitle": "Images and documents enter the same context window, cost tokens, and break the assumptions the rest of this course made about both.",
  "body": [
    ("p", "Everything so far assumed text in and text out. A multimodal model takes an image and the interesting part is not that it can — it is that the image becomes tokens in the same window everything else lives in, and every cost, limit and failure mode this course has taught applies to it unchanged."),

    ("h2", "An image is a number of tokens"),
    ("p", "The model does not see pixels. An encoder turns the image into a sequence of vectors occupying positions in the context, exactly like words. That single fact carries most of the practical consequences, because it means an image is priced, budgeted and truncated like text."),

    ("terms", [
      ("Resolution is a token count", "The dial nobody realises they are turning",
       "Larger images become more tokens, usually by tiling — the image is cut into patches and each contributes. Sending a screenshot at full resolution when a downscaled one would do is the same mistake as retrieving twenty chunks when four would do, and it is less visible because nobody thinks of an image as a length."),
      ("Documents are often images", "The expensive surprise",
       "A scanned PDF is pictures of pages. Processing it multimodally costs image tokens per page, where extracting the text first costs a fraction. Which is correct depends on whether the layout carries meaning."),
      ("Position still applies", "So caching still applies",
       "Images sit in the prefix like anything else. An image early in a stable prompt caches; an image that changes per request invalidates everything after it, which is the rule from the caching lesson with a different payload."),
      ("Detail settings", "A quality-cost dial, chosen once and forgotten",
       "Providers expose a low or high detail mode that changes how finely the image is tiled. It is a real quality-cost trade and it is usually left at the default by people who would agonise over a chunk size."),
    ]),

    ("know",
     "Everything this course taught about context cost applies to images, and people apply almost none of it.",
     "Teams that carefully count tokens, cap retrieved chunks and worry about prompt caching will attach a full-resolution screenshot to every request without measuring what it costs. The habits do not transfer, because an image does not look like a length — but the context window does not care what the tokens were made of, and neither does the bill.",
     "Measure it once. Send the same request with and without the image, read the input token count, and you have the price of that image in the units everything else in this course is denominated in."),

    ("figure", "The encoder is the only new component. Everything downstream is the pipeline this course already built, which is why its rules still apply.", '''<svg viewBox="0 0 640 176" role="img" aria-label="How an image enters the same context as text"><defs><marker id="mm" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="14" y="20" width="120" height="40" rx="6" class="d-box-accent"/><text x="26" y="45" class="d-label-sm">image</text>
<path d="M134 40 L192 40" class="d-arrow-accent" marker-end="url(#mm)"/>
<rect x="192" y="20" width="150" height="40" rx="6" class="d-box-accent"/><text x="204" y="38" class="d-label-b">encoder, tiled</text><text x="204" y="54" class="d-label-sm">resolution sets the count</text>
<rect x="14" y="86" width="120" height="40" rx="6" class="d-box"/><text x="26" y="111" class="d-label-sm">text</text>
<path d="M134 106 L192 106" class="d-arrow-accent" marker-end="url(#mm)"/>
<rect x="192" y="86" width="150" height="40" rx="6" class="d-box"/><text x="204" y="111" class="d-label-sm">tokenizer</text>
<path d="M342 50 L408 66" class="d-arrow-accent" marker-end="url(#mm)"/>
<path d="M342 100 L408 82" class="d-arrow-accent" marker-end="url(#mm)"/>
<rect x="408" y="52" width="218" height="44" rx="6" class="d-box"/><text x="420" y="72" class="d-label-b">one context window</text><text x="420" y="89" class="d-label-sm">priced, budgeted, truncated alike</text>
<text x="14" y="160" class="d-label-sm">Prefix caching, context cost and the prefill curve all apply unchanged — the tokens simply came from a picture.</text>
</svg>'''),

    ("callout", "pitfall", "Extraction is often the better tool, and it is less interesting",
     "<p>Before sending a document to a multimodal model, ask whether the layout carries meaning. A form, a chart, a diagram or a signed page needs to be seen. A text report does not, and extracting its text costs a fraction of processing pictures of its pages. The multimodal route is more impressive and frequently the wrong answer, which is the same shape as the fine-tuning argument in Block 7.</p>"),

    ("related", ["embeddings-and-retrieval", "attention-and-transformers", "inside-an-llm", "building-a-rag-system"]),
    ("quiz", [
      ("Why does image resolution matter beyond visual quality?",
       ["Larger images take longer to upload",
        "Resolution determines how many tokens the image becomes, so it is a context-cost dial like retrieved chunk count",
        "Encoders reject images above a size limit"],
       1),
      ("When is extracting a document's text preferable to sending it to a multimodal model?",
       ["Whenever the document is longer than a page",
        "When the layout carries no meaning — extraction costs a fraction of processing pictures of pages",
        "When the model has no vision capability"],
       1),
    ]),
  ],
},
{
  "slug": "asking-the-database-properly",
  "title": "Asking the Database Properly",
  "subtitle": "The intake sheet keeps asking whether a query would do. This is what that query looks like.",
  "body": [
    ("p", "Every project intake in this course opens with the same question: could a rule, a lookup or a SQL query solve this? It is asked so insistently because the answer is so often yes, and it deserves more than a rhetorical role. This lesson is the small amount of SQL that answers most of the analytical questions this course's projects raise."),

    ("h2", "The four that cover most questions"),
    ("terms", [
      ("Aggregate with GROUP BY", "How much, per what",
       "Almost every reporting question is this. Failure rate per site, spend per model, requests per key. If a question can be phrased as &ldquo;X per Y&rdquo;, it is a group-by and needs nothing cleverer."),
      ("Window functions", "Comparisons within a group",
       "Rank within a category, a running total, this row against the group average. The thing SQL does that a group-by cannot, because it keeps every row while adding the aggregate alongside it — the query behind &ldquo;which turbine is worst at its own site&rdquo;."),
      ("Joins, and their cardinality", "Where the wrong numbers come from",
       "The mistake is rarely writing the join and usually not knowing whether it multiplies rows. A one-to-many join silently inflates every sum downstream of it, and the result looks plausible."),
      ("Filtering before and after aggregation", "WHERE against HAVING",
       "WHERE removes rows before grouping; HAVING removes groups after. Confusing them produces answers that are wrong rather than errors that are visible."),
    ]),

    ("know",
     "A join that multiplies rows produces a wrong total, not an error.",
     "If each turbine has many readings, joining turbines to readings and summing a turbine-level column counts that column once per reading. The query runs, the number looks reasonable, and nothing in the output says it is several times too large. This is the single most common way a confident analysis is wrong, and it is invisible unless you check the row count before and after every join.",
     "Count the rows before the join and after it. If the number grew, every aggregate downstream needs looking at — and if you did not expect it to grow, stop and find out why before reading any of the results."),

    ("callout", "matters", "This is the baseline the intake sheet means",
     "<p>Question two on the intake sheet asks for the dumb baseline. On a great many problems the dumb baseline is a query, and it is genuinely difficult to beat: it is exact rather than approximate, it costs nothing per run, it explains itself, and it does not need evaluating. A model that cannot beat a group-by has told you something valuable and cheap.</p>"),

    ("figure", "Aggregation collapses rows; a window function keeps them and adds the comparison alongside. Most reporting questions are the first, and most interesting ones are the second.", '''<svg viewBox="0 0 640 176" role="img" aria-label="Group-by against window functions"><rect x="14" y="20" width="280" height="126" rx="8" class="d-box"/>
<text x="28" y="44" class="d-label-b">GROUP BY — rows collapse</text>
<text x="28" y="70" class="d-label-sm">4 turbines at a site</text>
<text x="28" y="90" class="d-label-sm">becomes 1 row: the site average</text>
<text x="28" y="118" class="d-label-sm">answers "how much, per what"</text>
<rect x="346" y="20" width="280" height="126" rx="8" class="d-box-accent"/>
<text x="360" y="44" class="d-label-b">window — rows survive</text>
<text x="360" y="70" class="d-label-sm">4 turbines stay 4 rows</text>
<text x="360" y="90" class="d-label-sm">each gains its site average beside it</text>
<text x="360" y="118" class="d-label-sm">answers "which one is worst at its site"</text>
</svg>'''),

    ("related", ["deterministic-first", "tabular-data-and-dtypes", "structured-output-json", "agentic-rag"]),
    ("quiz", [
      ("What makes a one-to-many join dangerous?",
       ["It is slower than other join types",
        "It multiplies rows, so any sum downstream is inflated — and the query succeeds with a plausible-looking wrong number",
        "It can return null values in unexpected columns"],
       1),
      ("What can a window function do that GROUP BY cannot?",
       ["Aggregate across multiple tables at once",
        "Keep every row while adding the group's aggregate alongside it, which is what comparing a row to its own group requires",
        "Filter rows after aggregation"],
       1),
    ]),
  ],
},
{
  "slug": "where-the-money-goes",
  "title": "Where the Money Goes",
  "subtitle": "Block 0 taught routing, which is architecture. This is the measurement — attributing spend, and the four places it hides.",
  "body": [
    ("p", "The vocabulary block taught cheap-first architecture: route simple work to a small model and escalate when it fails. That is the design decision. This lesson is the part that comes after — knowing what you actually spent and on what, which is a measurement problem and is almost never solved by looking at the invoice."),

    ("h2", "An invoice is not an attribution"),
    ("p", "A monthly total tells you the size of the problem and nothing about its shape. The question worth answering is which requests, which features and which users produced it, and that requires recording cost per request at the point the request happens, because it cannot be reconstructed afterwards."),

    ("terms", [
      ("Per request, at the time",
       "Input tokens, output tokens, cached tokens, model, feature",
       "Logged as part of the trace from Block 4. Everything below is a group-by over this, and none of it is possible without it."),
      ("Cached against uncached",
       "The number that says whether caching works",
       "Cache reads cost roughly a tenth of normal input. If that ratio is not visible per request, a cache that silently stopped working looks exactly like one that never existed, except on the total."),
      ("Cost per successful outcome",
       "Not cost per call",
       "A cheap model that needs three attempts and an escalation is not cheap. Attribute the whole chain to the outcome, or a routing strategy that is losing money will look like one that is saving it."),
      ("The long tail",
       "Where it usually is",
       "Spend is rarely uniform. A small number of users, features or question types typically dominate, and a median tells you nothing about them. Look at the distribution and specifically at the top percentile."),
    ]),

    ("know",
     "The expensive request is usually the one that failed and was retried.",
     "Cost dashboards are built around successful calls because those are the ones that produce something to attribute. The retries, the truncated generations, the escalations and the runs that hit a turn cap are all paid for in full and produce nothing, and they are frequently a large fraction of spend. Any measurement that counts only what worked will understate the bill and — worse — will hide the fact that the overspend is a reliability problem rather than a pricing one.",
     "This connects to the non-completion column from Block 5. There, classifying failures separately protected the capability numbers. Here it protects the cost numbers, and it is the same discipline applied to a different aggregate."),

    ("figure", "Dashboards are built from the left-hand column because it is what succeeds. The right-hand column is paid for identically and produces nothing, and it is frequently the larger share.", '''<svg viewBox="0 0 640 182" role="img" aria-label="Where spend hides"><rect x="14" y="20" width="250" height="120" rx="8" class="d-box"/>
<text x="28" y="44" class="d-label-b">what dashboards count</text>
<text x="28" y="70" class="d-label-sm">successful calls</text>
<text x="28" y="90" class="d-label-sm">tokens in and out</text>
<text x="28" y="112" class="d-label-sm">attributable, tidy</text>
<rect x="300" y="20" width="326" height="120" rx="8" class="d-box-accent"/>
<text x="314" y="44" class="d-label-b">what they miss, and you still pay for</text>
<text x="314" y="68" class="d-label-sm">retries · timeouts billed twice</text>
<text x="314" y="88" class="d-label-sm">history re-sent, growing with the square</text>
<text x="314" y="108" class="d-label-sm">a cache that silently stopped working</text>
<text x="314" y="128" class="d-label-sm">reasoning tokens behind a short answer</text>
<text x="14" y="170" class="d-label-sm">Counting only what worked understates the bill and hides that the overspend is a reliability problem.</text>
</svg>'''),

    ("h2", "The four places it hides"),
    ("ul", [
      "<strong>Retries and timeouts</strong> — paid in full, produce nothing, and Block 8 showed a timed-out call may have been billed twice.",
      "<strong>Context growth</strong> — history re-sent every turn means cost grows with the square of a conversation's length. The single biggest driver of surprise bills.",
      "<strong>Broken caching</strong> — fails open and silently. A timestamp near the front of a prompt takes the hit rate to zero and nothing errors.",
      "<strong>Reasoning tokens</strong> — billed as output and invisible in the answer. A model that thinks for eight hundred tokens before writing forty has charged for eight hundred and forty.",
    ]),

    ("callout", "matters", "Set a ceiling that stops something, not one that emails you",
     "<p>A budget alert is a notification that money has already been spent. The control that works is a hard cap in the path — a per-key spend limit, a token budget per request, a turn cap on a loop — because the failure mode being guarded against is a runaway loop at three in the morning, and that is precisely when nobody is reading alerts.</p>"),

    ("related", ["latency-and-caching", "routing-and-escalation", "loop-tradeoffs", "calling-an-api-you-do-not-control"]),
    ("quiz", [
      ("Why is cost per call a misleading metric?",
       ["It ignores infrastructure costs beyond the model",
        "A cheap model needing three attempts and an escalation is not cheap — the whole chain must be attributed to the outcome, or a losing strategy looks like a winning one",
        "Providers price calls differently by time of day"],
       1),
      ("Why does a broken prompt cache go unnoticed?",
       ["Cache metrics are usually sampled rather than complete",
        "It fails open — the requests still succeed and the answers are still correct, so the only symptom is the bill",
        "Providers do not expose cache hit rates"],
       1),
      ("What kind of spending control actually prevents a runaway loop?",
       ["A budget alert configured on the provider dashboard",
        "A hard cap in the request path — a per-key limit or a token budget — because an alert is a notification that the money is already gone",
        "A daily review of the cost dashboard"],
       1),
    ]),
  ],
},
]
