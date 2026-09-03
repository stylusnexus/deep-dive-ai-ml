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
  "slug": "transforming-the-query",
  "title": "Transforming the Query",
  "subtitle": "Every technique so far improves what you search. This one changes what you search for.",
  "body": [
    ("p", "The pipeline lesson tuned the index side: chunk well, retrieve wide, fuse, rerank, send few. All of it takes the user's question exactly as typed and works on everything downstream of it. That is a choice, and it is worth noticing, because the question is often the weakest part of the request."),

    ("h2", "The asymmetry underneath all of this"),
    ("p", "You embed a question and match it against documents that are <em>answers</em>. Those are different kinds of text. A question is short, interrogative, and phrased in the words of someone who does not yet know; the passage that answers it is declarative, longer, and phrased in the words of someone who does. Similarity search assumes the two live near each other in the vector space, and they often do not."),

    ("terms", [
      ("Hypothetical document embedding", "Retrieve with a fake answer, not the question",
       "Ask the model to write the answer it would expect, then embed that draft and search with it. The draft is discarded — only its vector is used. You are matching answer against answer instead of question against answer, which is the shape the space is better at."),
      ("Query rewriting", "Make a dependent question standalone",
       "A follow-up carries meaning from the turn before it and none of that meaning is in the embedding. Rewriting resolves the reference before retrieval happens."),
      ("Query expansion", "Several phrasings instead of one",
       "Generate a handful of alternative wordings, retrieve for each, and fuse the ranked lists — the same reciprocal rank fusion the pipeline lesson already uses for combining keyword and vector results, applied to combining queries instead."),
      ("Decomposition", "Covered already, in the agentic lesson",
       "Splitting a question into planned sub-questions is the same family, and this course teaches it as part of the loop rather than here."),
    ]),

    ("know",
     "A follow-up question carries almost none of its meaning in its own words.",
     "This course has measured it. Running &ldquo;What is the failure rate at Clyde?&rdquo; against the follow-up &ldquo;And at Whitelee?&rdquo; through the same encoder the retrieval notebooks use gives a cosine similarity of 0.149 — near the floor, barely above two unrelated sentences. The second question is perfectly clear to a human reading the transcript and nearly meaningless to an embedding, because everything that makes it a question about failure rates is in the previous turn.",
     "Retrieval on a conversational interface fails on follow-ups long before it fails on hard questions, and it fails silently: the search runs, returns something, and nobody sees that the query never contained the subject. Rewriting is not an optimisation here, it is the difference between working and not."),

    ("figure", "Three transformations, all of them a model call before retrieval. The question is rewritten, replaced by a drafted answer, or fanned out into several phrasings — and only then does the index get used.", '''<svg viewBox="0 0 640 232" role="img" aria-label="Query transformation before retrieval"><defs><marker id="qt" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="12" y="94" width="104" height="44" rx="6" class="d-box"/><text x="24" y="112" class="d-label-b">question</text><text x="24" y="130" class="d-label-sm">as typed</text>
<path d="M116 116 L164 116" class="d-arrow-accent" marker-end="url(#qt)"/>
<rect x="164" y="20" width="196" height="42" rx="6" class="d-box-accent"/><text x="176" y="38" class="d-label-b">rewrite</text><text x="176" y="55" class="d-label-sm">resolve what the turn assumed</text>
<rect x="164" y="94" width="196" height="42" rx="6" class="d-box-accent"/><text x="176" y="112" class="d-label-b">draft an answer</text><text x="176" y="129" class="d-label-sm">embed that instead of the question</text>
<rect x="164" y="168" width="196" height="42" rx="6" class="d-box-accent"/><text x="176" y="186" class="d-label-b">expand</text><text x="176" y="203" class="d-label-sm">several phrasings, fuse the results</text>
<path d="M360 41 L432 108" class="d-arrow-accent" marker-end="url(#qt)"/>
<path d="M360 115 L432 115" class="d-arrow-accent" marker-end="url(#qt)"/>
<path d="M360 189 L432 124" class="d-arrow-accent" marker-end="url(#qt)"/>
<rect x="432" y="94" width="196" height="44" rx="6" class="d-box"/><text x="444" y="112" class="d-label-b">retrieval, unchanged</text><text x="444" y="130" class="d-label-sm">chunk, search, fuse, rerank</text>
<text x="164" y="228" class="d-label-sm">Each box is a model call, paid before the index is touched.</text>
</svg>'''),

    ("h2", "What it costs, in the place you just learned to look"),
    ("p", "Every one of these is a model call that happens <em>before</em> retrieval. The measurement lesson showed retrieval running in milliseconds against a read measured in seconds, and a transformation moves a piece of that expensive second category in front of the cheap first one. It is still usually worth it — a generated draft is short, and short generations are quick — but it is the one change in this block that makes the cheap stage meaningfully less cheap, and it should be timed rather than assumed."),

    ("callout", "pitfall", "A drafted answer can be confidently wrong and still steer retrieval",
     "<p>The draft in a hypothetical-document approach is never shown to anyone, which makes it easy to forget it can be nonsense. A model that drafts a plausible wrong answer produces a vector pointing at the wrong region of the corpus, and retrieval then faithfully returns documents supporting the wrong thing. The failure is invisible: recall looks fine against the drafted answer and terrible against the actual question.</p>"),

    ("callout", "matters", "Do not transform a query that was already good",
     "<p>These techniques repair a mismatch between how questions and answers are phrased. Where users type keyword-shaped queries, or where the corpus is itself full of questions — a support knowledge base of FAQ entries, say — the mismatch is small and the transformation adds latency, cost and a new failure mode for very little. Measure the block's existing three numbers before and after; if they do not move, do not keep it.</p>"),

    ("h2", "Where this sits in the block"),
    ("p", "Chunking decides what can be found. Retrieval and reranking decide what is found. Transformation decides what is looked for, and it is the only stage that touches the request rather than the corpus — which is why it is the first thing to reach for on a conversational interface and among the last on a search box."),

    ("quiz", [
      ("Why can embedding a hypothetical answer retrieve better than embedding the question?",
       ["Generated text is cleaner than user input",
        "The corpus contains answers, so matching an answer-shaped vector against answer-shaped passages is closer to what the space is good at than matching a question against them",
        "It gives the retriever more tokens to work with"],
       1),
      ("A conversational follow-up like \"And at Whitelee?\" retrieves badly. Why?",
       ["It is too short for the encoder to represent",
        "Its meaning lives in the previous turn, so the embedding contains almost none of what the question is actually about — measured at 0.149 similarity to the question it follows",
        "Site names are poorly represented in general-purpose embeddings"],
       1),
      ("What does a query transformation cost that the rest of this block does not?",
       ["A larger index and more storage",
        "A model call before retrieval, which moves expensive generation work in front of the stage that was previously milliseconds",
        "A second reranking pass over the results"],
       1),
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

    ("h2", "The fourth number, which this lesson used to omit"),
    ("p", "Everything above measures whether retrieval found the right thing. None of it measures how long the request took, and the two are not distributed the way people assume. Break a retrieval request into stages and the shape is stark: embedding the query is a few milliseconds, approximate nearest-neighbour search over a few million vectors is tens of milliseconds, and reranking a shortlist with a cross-encoder is around a hundred. Then the model reads what came back, and on a long context that step alone runs into <em>seconds</em>."),

    ("p", "Retrieval is a small fraction of the clock. Tuning it for speed is optimising the part that was already cheap, while the expensive stage sits immediately downstream and is fed by exactly how much you chose to retrieve."),

    ("terms", [
      ("Retrieval time", "Milliseconds",
       "Embedding, search and reranking together. Worth measuring, and rarely worth optimising first."),
      ("Read time (prefill)", "Often seconds",
       "The model processing everything retrieval handed it, before a single output token appears. This is what the user experiences as the delay."),
      ("The lever", "Send fewer chunks, not find them faster",
       "Read time grows with how much you send. Attention's own cost grows with the <em>square</em> of the context, but that term does not dominate until the context approaches the model's hidden dimension — at retrieval-sized contexts the read is close to linear in tokens. Either way, precision beats volume on the clock for the same reason it beats volume on the answer."),
    ]),

    ("know",
     "&ldquo;Prefill is quadratic&rdquo; is true about attention and misleading about the read.",
     "Attention does compare every token against every other, so its cost carries a squared term. But attention is only part of prefill: the projections and the feed-forward layers cost roughly tokens times the hidden dimension squared, which is linear in context. The squared term does not overtake the linear one until the context is on the order of the model's hidden dimension — thousands of tokens — so at retrieval-sized contexts the read grows roughly in proportion to what you send.",
     "Project 2 measures this on its own corpus by sweeping how many chunks it retrieves. Going from 288 to 1,073 words of context — 3.7 times the context — multiplied the read by 3.6. Quadratic scaling would have predicted about fourteen. The lever is still sending less, but the reason is proportion rather than explosion."),

    ("callout", "insight", "One value of k cannot separate reading from writing",
     "<p>A single measurement of read time bundles two things: prefill, which grows with the context you sent, and decode, which grows with the answer the model writes. Neither is visible on its own. Project 2 separates them by sweeping how many chunks it retrieves — the answers stay roughly the same length while the context grows, so the <em>slope</em> of read time against context is prefill and the intercept is the decode floor.</p><p>On its corpus that floor is around three and a half seconds before a single retrieved word is read. If you are optimising context size against a read time dominated by an unchanging decode cost, you are tuning the smaller half and the numbers will barely move.</p>"),

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

    ("h2", "The other answer to the same question"),
    ("p", "The loop is one way to reach a fact that lives in two places. The other is to stop searching for the relationship each time and store it: extract the entities and the connections between them from the corpus ahead of time, and the multi-hop question becomes a traversal instead of a search. This is what people mean by a knowledge graph, and by <strong>GraphRAG</strong> when it is wired into retrieval."),

    ("p", "Take the question above. Under retrieval it is two searches and a model holding the intermediate result in its head. Under a graph, <em>turbine</em> and <em>site</em> are nodes, <em>installed at</em> is an edge, the failure rate is a property, and the answer is a query that walks from one to the other &mdash; no iteration, no intermediate context, and the same answer every time."),

    ("figure", "The same multi-hop question, two ways: iterate at query time, or extract the relationships once and traverse them.", '''<svg viewBox="0 0 520 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Agentic retrieval loops at query time; a knowledge graph extracts relationships at build time and traverses them.">
<text x="8" y="16" class="d-label-sm">agentic loop &#8212; pays at query time</text>
<rect x="8" y="24" width="74" height="30" rx="5" class="d-box"/><text x="45" y="43" class="d-label" text-anchor="middle">search</text>
<path d="M82 39 L106 39" class="d-arrow"/>
<rect x="110" y="24" width="74" height="30" rx="5" class="d-box"/><text x="147" y="43" class="d-label" text-anchor="middle">reason</text>
<path d="M184 39 L208 39" class="d-arrow"/>
<rect x="212" y="24" width="74" height="30" rx="5" class="d-box"/><text x="249" y="43" class="d-label" text-anchor="middle">search</text>
<path d="M286 39 L310 39" class="d-arrow"/>
<rect x="314" y="24" width="86" height="30" rx="5" class="d-box-good"/><text x="357" y="43" class="d-label" text-anchor="middle">answer</text>
<text x="408" y="43" class="d-label-sm">turns, tokens,</text>
<text x="408" y="55" class="d-label-sm">latency each ask</text>
<text x="8" y="88" class="d-label-sm">knowledge graph &#8212; pays once, at build time</text>
<rect x="8" y="96" width="112" height="30" rx="5" class="d-box"/><text x="64" y="115" class="d-label" text-anchor="middle">extract entities</text>
<path d="M120 111 L144 111" class="d-arrow"/>
<circle cx="168" cy="111" r="13" class="d-box"/><text x="168" y="115" class="d-label-sm" text-anchor="middle">trb</text>
<path d="M181 111 L211 111" class="d-arrow"/>
<circle cx="228" cy="111" r="13" class="d-box"/><text x="228" y="115" class="d-label-sm" text-anchor="middle">site</text>
<text x="176" y="100" class="d-label-sm">installed at</text>
<path d="M243 111 L300 111" class="d-arrow"/>
<rect x="304" y="96" width="96" height="30" rx="5" class="d-box-good"/><text x="352" y="115" class="d-label" text-anchor="middle">traverse</text>
<text x="408" y="115" class="d-label-sm">one query,</text>
<text x="408" y="127" class="d-label-sm">same answer twice</text>
</svg>'''),

    ("terms", [
      ("Where it genuinely wins", "Questions about relationships, not passages",
       "Anything phrased as which, how many, who else, what connects &mdash; where the answer is a join across entities rather than a passage that contains it. Also anything you need to be repeatable, because a traversal is deterministic and a loop is not."),
      ("What it costs", "An extraction pipeline, and its upkeep",
       "Something has to read the corpus and decide what the entities and relationships are. That is usually a model, run over everything, once per corpus and again whenever the corpus changes."),
      ("The failure that matters", "Extraction errors become structure",
       "A retrieval mistake affects one answer. A wrong edge in the graph is reused by every question that walks through it, and it is invisible at query time because the traversal is working perfectly on bad data."),
      ("How it is usually deployed", "Alongside vectors, not instead of them",
       "The graph answers the structural part and the vector index still finds the prose. Most working systems are hybrids, in the same way that Block 3&#39;s ranking lesson ends up combining keyword and vector search rather than choosing."),
    ]),

    ("know",
     "A knowledge graph moves the work from query time to build time. That is the entire trade.",
     "The loop is cheap to build and expensive per question &mdash; every ask pays the turns, the tokens and the latency again, and gets a slightly different path each time. The graph is expensive to build and cheap per question, and gives the same answer twice. Neither is more advanced than the other; they bill differently, and which one is right depends on whether your questions are numerous and repetitive or few and varied.",
     "A corpus of ten thousand maintenance reports, queried a hundred times a day with questions about which sites and which components. Extracting a graph once costs a few hours of model time and makes every one of those hundred queries a fast, repeatable traversal. The same corpus queried twice a week with open-ended questions does not repay the pipeline, and the loop is the right answer."),

    ("callout", "pitfall", "The same discipline this lesson already applies to the loop",
     "<p>Everything the lesson says about not making the loop the default applies here with more force, because a graph costs more up front. The majority of questions are single-hop and a well-built vector index answers them. Build the graph when you can point at a class of question you are actually asked, repeatedly, that needs relationships &mdash; not because the architecture is appealing.</p><p>And be suspicious of a graph built entirely by a model with nobody checking the edges. Extraction quality is the whole system: a graph with plausible wrong relationships is a machine for producing confident wrong answers, and it will be more convincing than a bad retrieval because it arrives with structure attached.</p>"),

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
{
  "slug": "preloading-instead-of-retrieving",
  "title": "Preloading Instead of Retrieving",
  "subtitle": "If the corpus does not change between queries, nothing forces you to wait for a question before reading it.",
  "body": [
    ("p", "Every system in this block waits for a query, then retrieves, then reads what it retrieved. The previous lesson showed that the reading is where the time goes. This lesson asks a question that follows directly and that the rest of the block never raises: if the documents are the same for every user who asks, why is the model reading them at request time at all?"),

    ("h2", "The spectrum"),
    ("p", "This is not one technique. It is a range, and each step down it moves more work before the query arrives and keeps a different artefact afterwards. A real system usually sits at several points at once — a preloaded cache for stable documentation, ordinary retrieval for anything that changed this morning."),

    ("terms", [
      ("Retrieval only", "Nothing precomputed",
       "Every query pays a full read of whatever came back. The whole block up to this point. Its limit is that the read is paid again for every question."),
      ("Prefix cache", "Whatever an earlier request happened to leave",
       "Free and automatic, and the previous lesson showed why it barely helps here: retrieval produces a shared set, not a shared prefix. Its limit is order sensitivity."),
      ("Naive preload", "One read of the whole corpus, stored",
       "Read the corpus once before any query, keep the resulting cache, and every question skips straight to answering. Its limit is the context ceiling — the corpus has to fit."),
      ("Modular preload", "One read per passage, assembled on demand",
       "Each passage read separately so it can be dropped into any position. Buys the order-independence the prefix cache cannot offer, and costs either recomputation at request time or a change to the model."),
      ("Compressed preload", "The stored cache, shrunk",
       "Smaller artefact, and it carries a requirement most compression methods fail: it has to be done before any query exists, so it cannot be guided by what was asked."),
      ("Trained preload", "A cache produced by a training run",
       "Not a copy of anything — a small set of trained vectors taught to behave as though the corpus were present. Its limit is that the corpus must be stable enough to justify the run."),
    ]),

    ("figure", "Each step trades more work done before the question for less work done after it, and keeps a different artefact. It is a spectrum rather than a ranking, and one system can sit at several points at once.", '''<svg viewBox="0 0 640 220" role="img" aria-label="The preload spectrum"><defs><marker id="pl" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<text x="14" y="20" class="d-label-b">More work before the query</text>
<path d="M14 30 L620 30" class="d-arrow-accent" marker-end="url(#pl)"/>
<rect x="14" y="44" width="96" height="52" rx="6" class="d-box"/><text x="24" y="66" class="d-label-sm">retrieval</text><text x="24" y="84" class="d-label-sm">only</text>
<rect x="118" y="44" width="96" height="52" rx="6" class="d-box"/><text x="128" y="66" class="d-label-sm">prefix</text><text x="128" y="84" class="d-label-sm">cache</text>
<rect x="222" y="44" width="96" height="52" rx="6" class="d-box-accent"/><text x="232" y="66" class="d-label-sm">naive</text><text x="232" y="84" class="d-label-sm">preload</text>
<rect x="326" y="44" width="96" height="52" rx="6" class="d-box"/><text x="336" y="66" class="d-label-sm">modular</text><text x="336" y="84" class="d-label-sm">preload</text>
<rect x="430" y="44" width="96" height="52" rx="6" class="d-box"/><text x="440" y="66" class="d-label-sm">compressed</text><text x="440" y="84" class="d-label-sm">preload</text>
<rect x="534" y="44" width="92" height="52" rx="6" class="d-box"/><text x="544" y="66" class="d-label-sm">trained</text><text x="544" y="84" class="d-label-sm">preload</text>
<text x="14" y="126" class="d-label-sm">stores: vector index</text>
<text x="222" y="126" class="d-label-sm">stores: raw corpus cache</text>
<text x="430" y="126" class="d-label-sm">stores: a trained artefact</text>
<text x="14" y="164" class="d-label-b">Less work after it</text>
<path d="M620 174 L14 174" class="d-arrow-accent" marker-end="url(#pl)"/>
<text x="14" y="204" class="d-label-sm">The corpus must be stable across queries for any of this. Anything that changes per request is still fetched.</text>
</svg>'''),

    ("know",
     "Preloading and retrieval are not competitors. They apply to different parts of the same system.",
     "Everything on this spectrum assumes the knowledge is the same for every query. A product manual, a legal contract, a policy document and a codebase all qualify. A customer's current balance does not, and no amount of offline work will make it. The question is never which approach wins — it is which parts of your corpus are stable enough to read in advance.",
     "A support system might serve a trained cache for its product documentation, which changes quarterly, and ordinary retrieval for ticket history, which changes continuously. Both in the same request."),

    ("h2", "Why the obvious repair does not work"),
    ("p", "Modular preloading sounds like it should be easy: read each passage on its own, store its cache, and glue the pieces together in whatever order retrieval returns them. It fails, and for three separate reasons that are worth knowing because they explain the shape of every real fix."),

    ("terms", [
      ("Positions restart", "Every block thinks it begins the sequence",
       "Position is encoded into the keys by rotation, and an attention score depends on the distance between a query and a key. A key computed at position zero, replayed at position five hundred, measures the wrong distance and produces a wrong score. It has to be re-rotated to where it now sits."),
      ("Cross-attention is missing", "No block ever saw the others",
       "A passage read alone never attended to the passages before it, so the relationships between them were never computed and are not in the stored cache."),
      ("Several attention sinks", "Each block anchors its own first token",
       "Models place disproportionate attention on the first token of a sequence. Glue three blocks together and the model gets three starts instead of one."),
    ]),

    ("callout", "pitfall", "Precomputing blocks and hoping is measurably worse",
     "<p>This is not theoretical caution. When researchers re-implemented the training-free version of this idea and tested it on retrieval, its accuracy landed at or below their weakest baselines. Something has to give: either you recompute a slice of tokens at request time, or you change the model so the blocks are genuinely independent by design. There is no free version.</p>"),

    ("callout", "matters", "The trade is ownership, not just accuracy",
     "<p>Recomputing a slice at request time works with any model you can download. Training the model to treat blocks as independent removes that cost permanently — and hands you a model variant to maintain, which every base-model upgrade obliges you to produce again. That is an architecture decision with a long tail, and it belongs in a decision record rather than in someone's head.</p>"),

    ("h2", "Where this leaves the block"),
    ("p", "The honest summary is that retrieval earns its place when the corpus moves and the read is short, and stops being obviously right when the corpus is fixed and the read is long. Most of this block taught you to retrieve well. This lesson is the boundary of that advice, and the measurement from the previous lesson — how much of your request is the read — is what tells you which side of it you are on."),

    ("quiz", [
      ("What has to be true before any preloading approach is worth considering?",
       ["The corpus fits in the context window",
        "The knowledge is stable across queries — anything changing per request still has to be fetched at request time",
        "The model supports a long enough context"],
       1),
      ("Why can you not simply read each passage separately and concatenate the stored caches?",
       ["The caches are too large to hold in memory together",
        "Positions are encoded into the keys so they are wrong when replayed elsewhere, no passage ever attended to the others, and each block brings its own attention sink",
        "Passages must be read in the order they were retrieved"],
       1),
      ("What is the real cost of training a model to treat retrieved blocks as independent?",
       ["The training run itself, which is paid once",
        "A model variant you now maintain, which every base-model upgrade obliges you to produce again",
        "Reduced accuracy compared with recomputation"],
       1),
    ]),
  ],
},
]
