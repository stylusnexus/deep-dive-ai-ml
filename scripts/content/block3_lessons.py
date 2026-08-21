TITLE = "Block 3 · Retrieval and Agentic RAG"
TOPIC = "block3-retrieval"
ICON = "🔎"
DESCRIPTION = "Building a retrieval system that works, measuring the part everyone skips, and the loop that turns single-shot retrieval into something that can answer multi-hop questions."
TAGS = ["ai", "rag", "retrieval"]
COLOR = "rose"
CREATED = "2026-08-21"
ID_BASE = "1787600000"

LESSONS = [
{
  "slug": "building-a-rag-system",
  "title": "Building a Retrieval System That Works",
  "subtitle": "Five stages, and the two that decide whether the other three matter.",
  "body": [
    ("p", "Retrieval-augmented generation (RAG) is a short pipeline with a long tail of ways to get it wrong. The stages are simple; the judgement is in the two that people treat as configuration."),

    ("figure", "Five stages. Chunking and ranking are where quality is won or lost — the model at the end can only work with what reaches it, and most RAG failures happen before generation.", '''<svg viewBox="0 0 640 215" role="img" aria-label="The five stages of a retrieval pipeline"><defs><marker id="r1" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="12" y="30" width="112" height="52" rx="6" class="d-box"/>
<text x="26" y="52" class="d-label-b">1 · Ingest</text>
<text x="26" y="70" class="d-label-sm">parse, clean</text>
<path d="M124 56 L150 56" class="d-arrow-accent" marker-end="url(#r1)"/>
<rect x="150" y="30" width="112" height="52" rx="6" class="d-box-accent"/>
<text x="164" y="52" class="d-label-b">2 · Chunk</text>
<text x="164" y="70" class="d-label-sm">split by structure</text>
<path d="M262 56 L288 56" class="d-arrow-accent" marker-end="url(#r1)"/>
<rect x="288" y="30" width="112" height="52" rx="6" class="d-box"/>
<text x="302" y="52" class="d-label-b">3 · Embed</text>
<text x="302" y="70" class="d-label-sm">and index</text>
<path d="M400 56 L426 56" class="d-arrow-accent" marker-end="url(#r1)"/>
<rect x="426" y="30" width="112" height="52" rx="6" class="d-box-accent"/>
<text x="440" y="52" class="d-label-b">4 · Retrieve</text>
<text x="440" y="70" class="d-label-sm">and rank</text>
<path d="M538 56 L564 56" class="d-arrow-accent" marker-end="url(#r1)"/>
<rect x="546" y="30" width="82" height="52" rx="6" class="d-box"/>
<text x="560" y="52" class="d-label-b">5 · Gen</text>
<text x="560" y="70" class="d-label-sm">with cites</text>
<rect x="150" y="100" width="112" height="24" rx="4" class="d-fill-accent" opacity="0.25"/>
<rect x="426" y="100" width="112" height="24" rx="4" class="d-fill-accent" opacity="0.25"/>
<text x="150" y="146" class="d-accent">these two decide everything</text>
<text x="12" y="176" class="d-label-sm">A perfect model cannot answer from a chunk that was never retrieved, and cannot use a chunk that was</text>
<text x="12" y="194" class="d-label-sm">split mid-thought. Most "the model is bad at this" complaints are stage 2 or stage 4 problems.</text>
</svg>'''),

    ("h2", "Chunking is a modelling decision, not a parameter"),
    ("p", "The default advice — 512 tokens with 50 overlap — is a starting point that nobody should ship without looking at the output. The right question is not what size but <em>what is a self-contained thought in this corpus?</em>"),
    ("terms", [
      ("Split on structure first", "Headings, sections, functions", "A chunk that ends mid-sentence embeds badly and reads worse. Character counts are a fallback, not a strategy."),
      ("Too small", "Loses its referent", "A paragraph saying \"this threshold must not be exceeded\" is useless if the threshold was defined two chunks earlier."),
      ("Too large", "Averages several topics", "The embedding represents none of them well, and retrieving it burns context on material the question did not ask about."),
      ("Overlap a little", "10-15%", "So a passage spanning a boundary is not lost by both neighbours."),
      ("Keep the parent link", "Small to match, larger to read", "Retrieve the precise chunk, then optionally expand to its section for the model to read."),
    ]),

    ("know",
     "Print twenty random chunks and read them before tuning anything downstream.",
     "If you cannot tell what a chunk is about without its neighbours, neither can an embedding model. Every hour spent on embedding models or rerankers before doing this is spent on the wrong layer.",
     "A team spent two weeks comparing embedding models on a technical corpus with flat retrieval quality throughout. Their PDF parser was splitting on page boundaries, so roughly a third of chunks began mid-sentence and ended mid-table. No embedding model can rescue that, and ten minutes of reading would have found it."),

    ("h2", "What actually makes retrieval fail"),
    ("p", "In rough order of how often it is the real cause:"),
    ("ul", [
      "<strong>The chunk containing the answer was never retrieved.</strong> Nothing downstream can fix this, and it is by far the commonest failure.",
      "<strong>It was retrieved but ranked ninth.</strong> Attention is weakest mid-context, so a correct chunk buried in position nine is close to not retrieving it.",
      "<strong>The question needs two chunks that live far apart.</strong> Single-shot retrieval cannot combine them — this is the case the agentic lesson addresses.",
      "<strong>The corpus does not contain the answer.</strong> Worth establishing early, because everything else is wasted effort if so.",
      "<strong>The model ignored the context.</strong> Real, and much rarer than people assume. Check the first four before concluding this.",
    ]),
    ("callout", "matters", "Diagnose in that order, and cheaply", "For a failing question, look at what was retrieved before looking at the answer. If the right chunk is absent, it is a retrieval problem. If it is present but ranked low, it is a ranking problem. If it is present and first and the answer is still wrong, only then is it a generation problem. Three different fixes, and people reach for the third by default."),

    ("h2", "Retrieval: cheap, wide, then precise"),
    ("p", "The architecture that works, and the reasoning behind each step:"),
    ("terms", [
      ("Retrieve wide", "50 by keyword, 50 by vector", "Independent failure modes, so coverage is better than either alone. Cheap at this stage."),
      ("Fuse by rank", "Reciprocal rank fusion", "Two lines of code, no score normalisation, no tuning. Reliably beats either input list."),
      ("Rerank the shortlist", "Cross-encoder over ~100", "Scores query and document together rather than separately. Far more accurate, and only affordable because the set is small."),
      ("Send few", "Top 3 to 5", "Precision beats volume. Distractors actively degrade the answer rather than being politely ignored."),
    ]),

    ("h2", "Generation, and making the answer checkable"),
    ("ul", [
      "<strong>Require citations to the retrieved chunks.</strong> Not a bibliography — a mapping from claim to source span, so a human can verify one sentence without re-reading the corpus.",
      "<strong>Licence refusal explicitly.</strong> \"If the context does not contain the answer, say so\" costs one line and is the difference between a wrong answer and no answer.",
      "<strong>Define the empty-retrieval path.</strong> When nothing relevant came back, the model must not fall through to its parameters. This is where grounded systems quietly stop being grounded.",
      "<strong>Put the retrieved material at the start or the end.</strong> Never buried in the middle of a long prompt.",
    ]),

    ("know",
     "A grounded system stops being grounded the moment retrieval returns nothing and the model answers anyway.",
     "The grounding lives in the pipeline, not in the model. If your prompt does not explicitly handle the empty case, the model falls back to its parameters and produces a fluent, uncited, unverifiable answer that looks exactly like the grounded ones.",
     "A support assistant answers a question about a product discontinued before its training cutoff. Retrieval returned nothing, because the product is not in the knowledge base. The answer is confident, plausible, and drawn entirely from training data — indistinguishable in tone from the answers that were genuinely retrieved."),

    ("links", [
      ("Retrieval-Augmented Generation (Lewis et al., 2020)", "https://arxiv.org/abs/2005.11401",
       "The original paper — grounding as an architecture rather than a prompting trick."),
      ("pgvector", "https://github.com/pgvector/pgvector",
       "The Postgres extension this block uses. Read the indexing notes before loading real data."),
    ]),

    ("books", [
      ("Building Reliable AI Systems", "Rush Shahani",
       "Chapters 3 and 4 cover the same pipeline with production framing — data preparation, indexing, and the optimisations worth making."),
      ("Enterprise RAG", "Manning MEAP",
       "Chunking strategies and hybrid retrieval at scale, on your shelf."),
    ]),

    ("quiz", [
      ("A question fails. What do you look at first?",
       ["The generation prompt",
        "What was actually retrieved — absent, present-but-low-ranked and present-and-first are three different problems",
        "Whether the embedding model is strong enough"], 1),
      ("Why does chunk size matter beyond fitting the context window?",
       ["Larger chunks are slower to embed",
        "Too small loses the referent; too large averages several topics into a vector representing none of them well",
        "Embedding models have a fixed optimal input length"], 1),
      ("What happens to a grounded system when retrieval returns nothing?",
       ["It returns an empty response by default",
        "Unless the prompt handles the empty case, the model answers from its parameters — fluent, uncited and indistinguishable from a grounded answer",
        "The retrieval layer retries automatically"], 1),
    ]),
  ],
},
{
  "slug": "measuring-retrieval",
  "title": "Measuring Retrieval",
  "subtitle": "Three numbers, measured separately, because they fail independently and have different fixes.",
  "body": [
    ("p", "\"The RAG system is not very good\" is not a measurement. It could be retrieval missing the right chunk, ranking burying it, the index quietly losing candidates, or the model failing to use what it was given. Each has a different fix, and one aggregate score cannot distinguish them."),

    ("h2", "Measure three things, separately"),
    ("terms", [
      ("Index recall", "Is the index returning what exact search would?", "A property of your approximate index, measured against brute force. Nobody checks this."),
      ("Retrieval quality", "Is the right chunk in the top k?", "A property of embeddings, chunking and ranking. Measured against a labelled set."),
      ("Groundedness", "Is the answer supported by what was retrieved?", "A property of generation. Distinct from whether the answer is correct."),
    ]),
    ("p", "A system can have perfect index recall, poor retrieval quality and high groundedness — faithfully summarising the wrong document. Only measuring the three apart tells you that."),

    ("figure", "Each stage can fail independently, and the symptom is the same at the end. Measuring only the final answer tells you something is wrong, never what.", '''<svg viewBox="0 0 640 200" role="img" aria-label="Three independently measurable stages of a retrieval system"><defs><marker id="m3" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-muted"/></marker></defs>
<rect x="12" y="34" width="180" height="54" rx="6" class="d-box"/>
<text x="26" y="56" class="d-label-b">Index recall</text>
<text x="26" y="76" class="d-label-sm">vs exact search, on a sample</text>
<path d="M192 61 L226 61" class="d-arrow" marker-end="url(#m3)"/>
<rect x="226" y="34" width="180" height="54" rx="6" class="d-box"/>
<text x="240" y="56" class="d-label-b">Retrieval quality</text>
<text x="240" y="76" class="d-label-sm">recall@k, MRR, on labels</text>
<path d="M406 61 L440 61" class="d-arrow" marker-end="url(#m3)"/>
<rect x="440" y="34" width="188" height="54" rx="6" class="d-box"/>
<text x="454" y="56" class="d-label-b">Groundedness</text>
<text x="454" y="76" class="d-label-sm">supported by what came back</text>
<text x="12" y="122" class="d-fill-red" font-size="12" font-weight="600">Fails silently as:</text>
<text x="26" y="144" class="d-label-sm">candidates the index</text>
<text x="26" y="160" class="d-label-sm">never surfaced</text>
<text x="240" y="144" class="d-label-sm">right chunk exists,</text>
<text x="240" y="160" class="d-label-sm">ranked ninth</text>
<text x="454" y="144" class="d-label-sm">faithful summary of</text>
<text x="454" y="160" class="d-label-sm">the wrong passage</text>
<text x="12" y="190" class="d-label-sm">All three produce the same user complaint: "it gave me a wrong answer."</text>
</svg>'''),

    ("h2", "1 · Index recall, in about an hour"),
    ("p", "Take 200 real queries. Run each through exact brute-force search over the whole corpus and keep the true top-k. Run each through your index. Recall@k is the mean overlap."),
    ("p", "This is the number nobody computes, and it silently caps everything above it. An index at 90% recall is discarding one correct result in ten before ranking even begins, and the results it does return look entirely reasonable."),

    ("know",
     "An approximate index that loses candidates looks exactly like a system that never had them.",
     "Approximate nearest-neighbour search trades accuracy for speed by design. The results it returns are plausible, so nothing about the output signals that better ones were skipped — and every downstream metric inherits the loss without attributing it.",
     "RAG quality drops after a corpus grows from 50,000 to 400,000 chunks. Two weeks go into prompts, chunk sizes and a new embedding model. The index parameters were tuned at the original size; measured against exact search, recall had fallen from 0.97 to 0.71. One configuration change fixed it."),

    ("h2", "2 · Retrieval quality"),
    ("p", "This needs labels: questions paired with the chunks that genuinely answer them. Twenty to fifty is enough to be useful — the same twenty-item argument as everywhere else in this course."),
    ("terms", [
      ("Recall@k", "Is the right chunk in the top k?", "The headline. Measure at the k you actually send to the model, not at 100."),
      ("MRR", "Mean reciprocal rank", "How high it ranked, averaged. Rewards getting the answer to position one rather than position five."),
      ("Hit rate at k=1", "Did the best chunk come first?", "Blunt and honest. If this is low, a reranker is the highest-value addition."),
    ]),
    ("callout", "matters", "Build the label set from real questions, not invented ones", "Questions you write while looking at the corpus are subtly shaped by what you just read, and they retrieve better than real ones do. Take them from support tickets, search logs or actual users. Twenty real questions beat two hundred invented ones."),

    ("h2", "3 · Groundedness, and why it is not correctness"),
    ("p", "Two separate questions, and conflating them hides the more actionable one:"),
    ("terms", [
      ("Groundedness", "Is every claim supported by the retrieved text?", "A failure here is a generation problem. Fixable with prompting, citations, or a smaller context."),
      ("Correctness", "Is the answer actually right?", "A failure here with high groundedness means retrieval gave it the wrong material. Fixable upstream."),
    ]),
    ("p", "The combination is what tells you where to work. High groundedness with low correctness points squarely at retrieval. Low groundedness with high correctness means the model is answering from memory and happening to be right — which is worse than it sounds, because it will not always be."),

    ("know",
     "High groundedness and low correctness is a retrieval problem. Low groundedness and high correctness is a warning.",
     "The first means the model faithfully used what it was given, and it was given the wrong thing. The second means the model is answering from its parameters and getting away with it, which is not a property you can rely on.",
     "An assistant answers a policy question correctly, but the cited passage does not support the claim. Retrieval had failed and the model knew the answer anyway. The evaluation passes on correctness, the system is not actually grounded, and the first question outside the model's knowledge produces a confident fabrication with a citation attached."),

    ("h2", "Running the evaluation"),
    ("ul", [
      "<strong>Fix the set and leave it alone.</strong> Its value comes from not moving. Edit it between runs and it measures nothing.",
      "<strong>Score retrieval automatically.</strong> Recall@k and MRR need no judge — you have labels.",
      "<strong>Score groundedness with a judge, carefully.</strong> This is the case where a judge is genuinely the last resort, so use a different model family, compare pairwise where possible, and calibrate against thirty hand-labelled examples once.",
      "<strong>Re-run on every change.</strong> Chunk size, embedding model, index parameters, prompt, k — all of them are treatments.",
      "<strong>Record the manifest.</strong> Embedding model and version, index parameters, chunk strategy, k, prompt version. A score six weeks old is uninterpretable without it.",
    ]),

    ("links", [
      ("Precision-recall — scikit-learn", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html",
       "The metric mechanics, transferable directly to retrieval."),
      ("pgvector indexing", "https://github.com/pgvector/pgvector",
       "The index parameters whose effect on recall this lesson tells you to measure."),
    ]),

    ("quiz", [
      ("Your system faithfully summarises a passage that does not answer the question. Which measurement catches that?",
       ["Groundedness alone",
        "Groundedness and correctness measured separately — high groundedness with low correctness points at retrieval",
        "Index recall"], 1),
      ("Why measure index recall against exact search?",
       ["To benchmark query latency",
        "An approximate index discards correct candidates silently, and every downstream metric inherits the loss without attributing it",
        "To decide how many chunks to send the model"], 1),
      ("Where should the questions in your retrieval eval set come from?",
       ["Written while reading the corpus, for good coverage",
        "Real usage — tickets, logs, users. Questions written while looking at the corpus retrieve better than real ones do",
        "Generated by a model from the documents"], 1),
    ]),
  ],
},
{
  "slug": "agentic-rag",
  "title": "Agentic RAG: Retrieval as a Loop",
  "subtitle": "When one retrieval cannot answer the question — and the failure modes that arrive with the loop.",
  "body": [
    ("p", "Single-shot retrieval answers a question in one hop: embed, retrieve, generate. It works well and it has a hard limit. Some questions cannot be answered by any single retrieval, however good, because the answer does not exist in one place."),

    ("h2", "The questions single-shot cannot reach"),
    ("terms", [
      ("Multi-hop", "The answer needs two facts that live apart", "\"Which site has the turbine with the highest failure rate?\" needs per-turbine rates, then a site lookup. Neither chunk contains both."),
      ("Comparative", "Requires assembling several sources", "\"How does this year's policy differ from last year's?\" needs both policies retrieved and contrasted."),
      ("Under-specified", "The real question emerges from a first look", "\"Why did output drop?\" cannot be embedded usefully until you know which site and which period."),
      ("Aggregative", "Needs many chunks, not the top five", "\"How many incidents mentioned gearbox temperature?\" is a counting problem wearing a retrieval costume."),
    ]),
    ("callout", "matters", "The last one is a warning, not a use case", "Aggregative questions are usually the wrong shape for retrieval entirely. Counting, filtering and grouping are what a database does exactly and cheaply, and what a retrieval loop does approximately and expensively. If the question is really SQL, write SQL — the deterministic-first argument applies here as much as anywhere."),

    ("h2", "What the loop adds"),
    ("p", "Retrieve, reason about what came back, decide what is still missing, retrieve again. The model controls the query rather than receiving results of one it never saw."),

    ("figure", "The loop can reformulate, decompose and follow up. What it cannot do is know when to stop — that has to come from outside, exactly as with every other loop in this course.", '''<svg viewBox="0 0 640 220" role="img" aria-label="Single-shot retrieval compared with a retrieval loop"><defs><marker id="ar" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<text x="12" y="18" class="d-label-sm">SINGLE-SHOT</text>
<rect x="12" y="28" width="86" height="30" rx="5" class="d-box"/><text x="26" y="48" class="d-label-sm">question</text>
<path d="M98 43 L124 43" class="d-arrow-accent" marker-end="url(#ar)"/>
<rect x="124" y="28" width="86" height="30" rx="5" class="d-box"/><text x="138" y="48" class="d-label-sm">retrieve</text>
<path d="M210 43 L236 43" class="d-arrow-accent" marker-end="url(#ar)"/>
<rect x="236" y="28" width="86" height="30" rx="5" class="d-box-good"/><text x="252" y="48" class="d-label-sm">answer</text>
<text x="336" y="48" class="d-label-sm">one hop, cheap, predictable</text>
<line x1="12" y1="76" x2="628" y2="76" stroke="var(--border)"/>
<text x="12" y="100" class="d-label-sm">AGENTIC</text>
<rect x="12" y="110" width="86" height="30" rx="5" class="d-box"/><text x="26" y="130" class="d-label-sm">question</text>
<path d="M98 125 L124 125" class="d-arrow-accent" marker-end="url(#ar)"/>
<rect x="124" y="110" width="86" height="30" rx="5" class="d-box"/><text x="138" y="130" class="d-label-sm">retrieve</text>
<path d="M210 125 L236 125" class="d-arrow-accent" marker-end="url(#ar)"/>
<rect x="236" y="110" width="112" height="30" rx="5" class="d-box-accent"/><text x="248" y="130" class="d-label-sm">what is missing?</text>
<path d="M348 125 L374 125" class="d-arrow-accent" marker-end="url(#ar)"/>
<rect x="374" y="110" width="86" height="30" rx="5" class="d-box-good"/><text x="390" y="130" class="d-label-sm">answer</text>
<path d="M292 140 L292 166 L167 166 L167 142" class="d-arrow-accent" marker-end="url(#ar)"/>
<text x="188" y="182" class="d-label-sm">reformulate and retrieve again</text>
<text x="480" y="130" class="d-fill-red" font-size="11" font-weight="600">what stops it?</text>
<text x="12" y="208" class="d-label-sm">More capable, several times the cost and latency, and it needs a termination condition that is not the model's own opinion.</text>
</svg>'''),

    ("h2", "The failure modes the loop brings with it"),
    ("ul", [
      "<strong>Repetitive retrieval.</strong> The commonest and most expensive. The model reformulates slightly, gets near-identical results, and goes round again — burning turns and tokens without adding information.",
      "<strong>Weak contextualisation.</strong> Results arrive but are not integrated into the reasoning, so the next query is no better informed than the first.",
      "<strong>Context saturation.</strong> Every hop appends more retrieved text. By hop four the window holds a great deal of material, most of it already used, and attention thins across all of it.",
      "<strong>Drift.</strong> Each reformulation moves slightly away from the original question. By the fourth, the system is answering something adjacent.",
      "<strong>Cost you did not budget.</strong> Four hops is four retrievals and four generations, on a growing context. Several times the cost of single-shot, for a question that may not have needed it.",
    ]),

    ("know",
     "A retrieval loop with no de-duplication will re-retrieve what it already has.",
     "Slight query reformulations return substantially overlapping results. Without tracking what has already been seen, the loop mistakes repetition for progress, and its context fills with the same passages under different rankings.",
     "An agent asked a multi-hop question runs six retrievals. Passages two and three appear in five of the six result sets. The final context holds forty chunks of which fourteen are distinct, and the answer is no better than hop two would have produced at a sixth of the cost."),

    ("h2", "What makes it work"),
    ("terms", [
      ("De-duplicate against what you have", "Non-negotiable", "Track retrieved chunk ids and exclude them, or explicitly down-weight them, on subsequent hops."),
      ("Contextualise before reasoning", "Summarise what came back", "Turn raw chunks into a short statement of what is now known and what is still missing, then query on that."),
      ("Hard hop limit", "Three or four", "Plus a token budget. The gains flatten fast and the costs do not."),
      ("Decompose explicitly", "Where the structure is known", "\"Find the rate, then look up the site\" as two planned retrievals beats hoping a loop discovers the same decomposition."),
      ("Route by question shape", "Not everything needs the loop", "Most questions are single-hop. Detect the ones that are not, rather than paying loop cost on everything."),
    ]),

    ("know",
     "Route to the loop; do not make it the default.",
     "The overwhelming majority of real questions are answerable in one hop. Running every question through a multi-hop loop multiplies cost and latency across the whole workload to serve the minority that needed it, and adds failure modes to the majority that did not.",
     "A support assistant handles 2,000 questions a day. Roughly 60 genuinely need multiple hops. Making the loop the default multiplies the daily bill several times over and introduces drift and repetition into 1,940 questions that a single retrieval answered correctly."),

    ("h2", "The same rule as every other loop"),
    ("p", "This is the loops lesson arriving at a new surface. A retrieval loop improves things only when signal enters from outside it — a de-duplication check, a coverage test, an explicit \"do I now have what I need\" evaluated against something other than the model's confidence. Without that, extra hops mostly amplify the framing of the first query."),
    ("callout", "pitfall", "\"Do I have enough information?\" is the model marking its own work", "Asking the model whether it can answer yet is the same circularity as asking an agent whether it succeeded. It will frequently say yes when it has the shape of an answer rather than the substance. Prefer a checkable condition — required entities present, a citation for each part of the question, a hop budget — over the model's self-assessment."),

    ("links", [
      ("Agentic RAG: a survey (Singh et al., 2025)", "https://arxiv.org/abs/2501.09136",
       "The taxonomy of retrieval loops by agent count, control structure and autonomy."),
      ("Test-Time Strategies for Agentic RAG (2026)", "https://arxiv.org/abs/2603.12396",
       "The failure modes above measured, with de-duplication and contextualisation as the mitigations."),
      ("Effective context engineering for AI agents", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents",
       "Why hop four suffers — the attention budget, and what compaction does about it."),
    ]),

    ("quiz", [
      ("Which question genuinely needs a retrieval loop?",
       ["What is the maximum gearbox temperature?",
        "Which site has the turbine with the highest failure rate?",
        "How many incidents mention gearbox temperature?"], 1),
      ("What is the most common failure of a retrieval loop?",
       ["The model ignoring retrieved context",
        "Repetitive retrieval — slight reformulations returning near-identical results, mistaken for progress",
        "Exceeding the context window on the first hop"], 1),
      ("Why is 'ask the model whether it has enough information' a poor termination condition?",
       ["It costs an extra model call",
        "It is the model marking its own work — it will say yes when it has the shape of an answer rather than the substance",
        "Models cannot assess their own context"], 1),
      ("An aggregative question like 'how many incidents mention X' is best handled how?",
       ["A retrieval loop with a high hop limit",
        "Not by retrieval at all — counting and filtering is what a database does exactly and cheaply",
        "Single-shot retrieval with a very large k"], 1),
    ]),
  ],
},
]
