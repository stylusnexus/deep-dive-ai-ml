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
    ("related", ["convolutions-and-computer-vision", "embeddings-and-retrieval", "inside-an-llm", "building-a-rag-system"]),
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
{
  "slug": "convolutions-and-computer-vision",
  "title": "Convolutions, and What a CNN Assumes",
  "subtitle": "A grid is not a list, and building that in rather than learning it is the whole idea.",
  "body": [
    ("p", "A convolutional neural network (CNN) is the architecture that made computer vision work, and it is still the right answer for a large class of problems that this course&#39;s vision-language material does not serve. Its central idea is also the cleanest example in the whole program of an <strong>inductive bias</strong> &mdash; an assumption about the data built into the architecture rather than learned from examples &mdash; which is what makes it worth a lesson even if you never train one."),

    ("h2", "The problem with treating an image as a list of numbers"),
    ("p", "A fully-connected layer takes every input and connects it to every output. Feed it a modest 224 by 224 colour image and the input is about 150,000 numbers; connect that to a thousand units and that one layer holds roughly 150 million parameters. The next layer starts again from scratch."),
    ("p", "The parameter count is the smaller problem. The larger one is that the layer has been told nothing about the picture. Pixel (10, 10) and pixel (10, 11) are neighbours and it does not know; a cat in the top-left and the same cat in the bottom-right are unrelated inputs and it has to learn each position separately. Every fact about the grid has to be discovered from data that could just as well have been shuffled."),

    ("h2", "What a convolution does instead"),
    ("terms", [
      ("Convolution (kernel)", "A small window of weights",
       "Typically three by three or five by five. It is placed over a patch of the image, multiplied elementwise, and summed to one number. That number says how strongly this patch matches what the kernel is looking for."),
      ("Sliding it", "The same weights, everywhere",
       "The kernel moves across the whole image and the weights do not change as it moves. This is <strong>weight sharing</strong>, and it encodes the assumption that a feature worth detecting is worth detecting anywhere."),
      ("Locality", "Only neighbours are combined",
       "A unit sees a small patch rather than the whole image, which encodes the assumption that nearby pixels are related and distant ones mostly are not."),
      ("Stacking and pooling", "Where the reach comes from",
       "One layer sees three pixels; a layer above it sees three of those, and so on. The <em>receptive field</em> grows with depth, which is how a network of small windows ends up responding to whole objects."),
    ]),

    ("figure", "The same nine weights are applied at every position. A dense layer would need a separate weight for every pixel-to-unit pair.", '''<svg viewBox="0 0 540 168" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A three by three kernel slid across a grid, producing one output value per position.">
<g stroke="currentColor" stroke-width="1" fill="none" opacity="0.45">
<rect x="14" y="24" width="120" height="120"/>
<path d="M54 24 L54 144 M94 24 L94 144 M14 64 L134 64 M14 104 L134 104"/>
</g>
<rect x="14" y="24" width="80" height="80" class="d-box-accent" fill-opacity="0.25"/>
<text x="20" y="18" class="d-label-sm">image</text>
<text x="54" y="158" class="d-label-sm" text-anchor="middle">kernel here</text>
<path d="M140 64 L182 64" class="d-arrow"/>
<rect x="186" y="44" width="72" height="42" rx="5" class="d-box-accent"/>
<text x="222" y="62" class="d-label-sm" text-anchor="middle">9 weights</text>
<text x="222" y="78" class="d-label-sm" text-anchor="middle">multiply, sum</text>
<path d="M262 64 L304 64" class="d-arrow"/>
<rect x="308" y="48" width="34" height="34" rx="4" class="d-box-good"/>
<text x="325" y="70" class="d-label-sm" text-anchor="middle">1</text>
<text x="352" y="60" class="d-label-sm">one number per position,</text>
<text x="352" y="76" class="d-label-sm">using the SAME nine weights</text>
<text x="14" y="164" class="d-label-sm">dense layer on this image: about 150 million weights &#8212; one convolution: nine</text>
</svg>'''),

    ("know",
     "An inductive bias buys data efficiency and costs generality. That is the trade, and it is not free in either direction.",
     "Building locality and weight sharing into the architecture means the network does not have to learn them, so it reaches good performance on far less data than an unconstrained network would need. It also means the network cannot easily learn a relationship those assumptions forbid &mdash; something depending on absolute position, or on two distant regions jointly, is awkward for a CNN in a way it is not for an architecture with no such assumption.",
     "This is exactly why a vision transformer, which has almost no built-in assumption about the grid, needs substantially more data than a comparable CNN to reach the same accuracy &mdash; and why, given enough data, it overtakes. The CNN was handed a head start in the form of assumptions; past a certain data volume, learning the structure beats being told it."),

    ("h2", "Where this sits next to attention"),
    ("p", "The transformer lesson describes attention as letting every position look directly at every other. Read alongside this one, the two are opposite answers to the same question. A convolution says: nearby things are related, and a pattern means the same thing wherever it appears &mdash; here are those rules, do not learn them. Attention says: any position may matter to any other, work out which from the data."),
    ("p", "Neither is strictly better and the difference is a data budget. Architectures with strong assumptions win when data is scarce; architectures with weak assumptions win when it is plentiful, because an assumption is only a gift while it happens to be true. Modern vision models mostly sit between the two, and hybrid designs that keep some locality while adding attention are common for exactly this reason."),

    ("h2", "When a CNN is still the right tool"),
    ("p", "For most applied work involving an image today, the honest first move is the one the previous lesson describes: send it to a vision-language model and ask. That is a few lines, needs no labelled data and no training, and handles the enormous range of questions nobody anticipated."),
    ("ul", [
      "<strong>A narrow task, done constantly.</strong> Classifying one kind of defect on a production line, at high volume, where a per-image API cost and a network round trip are both unacceptable.",
      "<strong>You have the labels.</strong> Tens of thousands of examples of your specific task, which is the situation where a small purpose-built model beats a general one.",
      "<strong>The output is not language.</strong> A bounding box, a segmentation mask, a count &mdash; things a specialised head produces natively and a text model approximates.",
      "<strong>It has to run on the device.</strong> A few megabytes on a camera or a phone, with no connection.",
    ]),

    ("callout", "matters", "The deterministic-first argument applies here too",
     "<p>Before either option, ask whether the task needs learning at all. A great deal of practical image work &mdash; is this page blank, has the seal moved, is this barcode readable, are these two frames different &mdash; is answered by arithmetic on pixels with no model of any kind, faster and with a failure mode you can read. Classical computer vision did not stop working when deep learning arrived, and the ladder from Block 0 is the same ladder: rule, then classical method, then a small trained model, then a large general one.</p>"),
    ("related", ["when-the-input-is-not-text", "attention-and-transformers", "neural-networks-both-ways", "deterministic-first"]),
    ("quiz", [
      ("What does weight sharing in a convolution actually encode?",
       ["That the network should use fewer parameters to avoid overfitting",
        "The assumption that a feature worth detecting is worth detecting anywhere in the image, so the same weights apply at every position",
        "That nearby pixels have similar values and can be averaged"],
       1),
      ("Why does a vision transformer typically need more data than a CNN to reach the same accuracy?",
       ["Attention is less efficient per parameter, so it needs more examples to converge",
        "It has almost no built-in assumption about the grid, so relationships the CNN was handed must instead be learned from data",
        "Transformers cannot use weight sharing, so each position trains separately"],
       1),
      ("You need to classify one kind of defect, at high volume, on a device with no network. What does this lesson suggest?",
       ["A vision-language model, since it needs no labelled data",
        "A small purpose-built CNN — narrow task, your own labels, latency and offline constraints are exactly its case",
        "A hybrid architecture, since those outperform both"],
       1),
    ]),
  ],
},
{
  "slug": "recommendation-systems",
  "title": "Recommendation Systems, and the Loop They Sit In",
  "subtitle": "The one system in this course whose training data is its own past output.",
  "body": [
    ("p", "Recommenders are the most widely deployed machine learning systems in existence and the ones whose published accuracy numbers correspond least well to whether they work. Both facts have the same cause, and it is not the algorithm. A recommender is trained on data that a recommender produced, evaluated against behaviour it shaped, and judged on a metric that stops meaning what it meant the moment anyone optimises it."),

    ("h2", "The two families, and why every real system is both"),
    ("terms", [
      ("Collaborative filtering", "People like you liked this",
       "Uses only the interaction matrix &mdash; who engaged with what. It knows nothing about the items themselves, which is its strength: it finds affinities nobody could have described in advance."),
      ("Content-based recommendation", "This is like what you liked",
       "Uses features of the items &mdash; text, tags, an embedding. It can recommend something nobody has touched yet, which is precisely where collaborative filtering has nothing to say."),
      ("The hybrid", "Content for the cold, collaborative for the warm",
       "Almost every production system. Content-based handles new items and new users; collaborative takes over once there is enough interaction to be worth using."),
      ("The matrix", "Overwhelmingly empty",
       "A million users and a hundred thousand items is 100 billion cells, of which perhaps 0.01% are filled. Sparsity is not an inconvenience here, it is the defining property of the problem."),
    ]),

    ("h2", "What the data is actually telling you"),
    ("p", "Explicit feedback &mdash; a rating, a star, a thumbs down &mdash; is unambiguous and almost absent, because most people never rate anything. Implicit feedback &mdash; a click, a watch, a purchase &mdash; is abundant and means considerably less than it appears to."),

    ("know",
     "A click is not a like, and a non-click is not a dislike. Most of the empty cells mean &ldquo;never shown&rdquo;.",
     "Treating unobserved interactions as negative examples is the standard shortcut and it is wrong in a specific direction: the items a user did not interact with are overwhelmingly items they were never offered, and what they were offered was decided by the previous version of the recommender. The zeros in your matrix are a record of a past policy&#39;s choices, not of user preference &mdash; which makes this the Block 1 missing-data problem in its most consequential form. The data is missing not at random, and the mechanism generating the missingness is your own system.",
     "A user has never watched a documentary. Two explanations: they dislike documentaries, or the homepage has never shown them one because an early model decided they were a comedy viewer and every subsequent model trained on the resulting history. The matrix looks identical in both cases and the correct action is opposite."),

    ("h2", "Cold start, in three flavours"),
    ("ul", [
      "<strong>New user.</strong> No history, so collaborative filtering has nothing. Ask a few questions, use whatever context exists, or serve popular items and accept that the first session is weak.",
      "<strong>New item.</strong> Nobody has touched it, so it cannot be recommended, so nobody touches it. Content features are the only way out, and without them a catalogue addition is invisible indefinitely.",
      "<strong>New system.</strong> The one people forget. With no interaction history at all, the collaborative half cannot start, and the choices you make to bootstrap it become the data everything afterwards learns from.",
    ]),

    ("h2", "Popularity bias, and the loop that produces it"),
    ("p", "Popular items are recommended more, which gets them engaged with more, which makes them more popular. Nothing in the objective asks for this &mdash; it falls out of training on data the system generated. Left alone it narrows the catalogue in front of every user and concentrates engagement on a shrinking set of items, and the metrics improve throughout, because the metric is engagement and engagement is what is being concentrated."),

    ("figure", "The recommender chooses what is shown, what is shown determines what is engaged with, and engagement becomes the next training set. The loop closes with no adversary in it.", '''<svg viewBox="0 0 520 156" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A cycle: model recommends, user sees a narrowed slate, engagement is logged, and the log trains the next model.">
<rect x="16" y="20" width="108" height="38" rx="6" class="d-box"/><text x="70" y="44" class="d-label" text-anchor="middle">model</text>
<path d="M124 39 L172 39" class="d-arrow"/>
<rect x="176" y="20" width="128" height="38" rx="6" class="d-box"/><text x="240" y="38" class="d-label-sm" text-anchor="middle">what gets shown</text><text x="240" y="52" class="d-label-sm" text-anchor="middle">(a narrow slate)</text>
<path d="M304 39 L352 39" class="d-arrow"/>
<rect x="356" y="20" width="148" height="38" rx="6" class="d-box"/><text x="430" y="44" class="d-label-sm" text-anchor="middle">clicks on what was shown</text>
<path d="M430 58 L430 88" class="d-arrow"/>
<rect x="356" y="92" width="148" height="38" rx="6" class="d-box-bad"/><text x="430" y="116" class="d-label-sm" text-anchor="middle">becomes the training set</text>
<path d="M356 111 L128 111" class="d-arrow"/>
<rect x="16" y="92" width="108" height="38" rx="6" class="d-box-bad"/><text x="70" y="116" class="d-label-sm" text-anchor="middle">next model</text>
<text x="150" y="146" class="d-label-sm">nothing outside the loop ever enters it</text>
</svg>'''),

    ("h2", "Why the offline number does not predict the online one"),
    ("p", "This is the part that surprises people arriving from ordinary supervised learning. You hold out interactions, train, and measure error against them &mdash; and the resulting figure is a famously poor predictor of what happens when the system is deployed. Three reasons, each sufficient on its own."),

    ("terms", [
      ("You are ranking, not predicting", "The metric is the wrong shape",
       "Nobody sees a predicted rating. They see the top ten. Error averaged over all held-out interactions is dominated by items that will never be shown, so it can improve while the top of the list gets worse. Ranking metrics &mdash; precision at k, normalised discounted cumulative gain &mdash; at least measure the part anyone experiences."),
      ("The held-out data came from the old policy", "You cannot observe the counterfactual",
       "Your test set records what users did when shown the previous model&#39;s choices. A new model that would have recommended something better has no evidence for it in that data, because nobody was ever shown it. Offline evaluation systematically favours models that agree with the one already running."),
      ("Position and presentation dominate", "The slot is doing the work",
       "The top slot gets clicked far more than the fifth regardless of what is in it. Without correcting for it you measure position, and conclude that the model improved when the layout changed."),
    ]),

    ("callout", "pitfall", "The clearest Goodhart case in the whole course",
     "<p>Engagement is chosen as the objective because it correlates with value: people spend time on things they like. Optimise it hard and the correlation is what breaks first. What reliably increases engagement is not what people value most, it is what is hardest to stop doing &mdash; and a system with enough capacity finds that distinction long before anyone reviewing a dashboard does.</p><p>The measurement lesson&#39;s remedy applies directly and is unglamorous: pair the target with guardrails chosen in advance and permitted to veto. Catalogue coverage, repeat-visit rate at a week, explicit negative feedback, the share of engagement concentrated in the top one per cent of items. A recommender improving on engagement while every one of those degrades is not improving, and only the guardrails can say so.</p>"),

    ("h2", "What to do about the loop"),
    ("ul", [
      "<strong>Log what was shown, not only what was clicked.</strong> Without the slate, you cannot tell an item that was rejected from one that was never offered, and every analysis afterwards is guesswork.",
      "<strong>Reserve a fraction of traffic for exploration.</strong> A small share of randomised or deliberately diverse recommendations is the only source of evidence about items the current policy would never show. It costs measurable engagement and it is what keeps the training data from being purely self-generated.",
      "<strong>Measure coverage as a first-class metric.</strong> What share of the catalogue was recommended to anyone this week? A number that falls steadily is the loop closing, visible before the engagement number turns.",
      "<strong>Test online.</strong> The offline number is for filtering obviously bad candidates. The decision belongs to an experiment with real traffic, and the deployment lesson&#39;s interleaved comparison is unusually well suited here, since each user acts as their own control.",
    ]),
    ("related", ["loops-in-training", "drift", "why-measurement-decides", "embeddings-and-retrieval"]),
    ("quiz", [
      ("Why is treating unobserved user-item pairs as negative examples problematic?",
       ["It creates severe class imbalance that biases the loss",
        "Most unobserved pairs mean 'never shown' rather than 'not wanted', and what was shown was chosen by the previous model — so the zeros record a past policy, not preference",
        "It makes the matrix too sparse for factorisation to converge"],
       1),
      ("Why does offline evaluation systematically favour models similar to the one in production?",
       ["Because the held-out split is drawn from the same distribution as training",
        "Because the test data only records behaviour under the old policy's choices, so a better recommendation nobody was ever shown has no supporting evidence",
        "Because ranking metrics are biased towards popular items"],
       1),
      ("Catalogue coverage falls steadily while engagement rises. What is the most likely reading?",
       ["The model is getting better at identifying what users actually want",
        "The feedback loop is narrowing what gets shown — engagement is concentrating rather than improving, and coverage is the guardrail detecting it",
        "The catalogue has grown faster than the model has been retrained"],
       1),
    ]),
  ],
},
]
