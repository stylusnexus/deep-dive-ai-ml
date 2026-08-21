#!/usr/bin/env python3
"""Insert figure blocks into the vocabulary content at named anchors."""
import pathlib, sys

ARROW = ('<defs><marker id="a" markerWidth="9" markerHeight="7" refX="8" refY="3.5" '
         'orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-muted"/></marker>'
         '<marker id="aa" markerWidth="9" markerHeight="7" refX="8" refY="3.5" '
         'orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>')

FIGURES = {
"agent-loop-and-harness": ("""("figure", "The harness is the outer box. The model sits outside it and only ever returns text \\u2014 the loop is what turns that text into action.", '''<svg viewBox="0 0 640 300" role="img" aria-label="Diagram of an agent loop inside a harness">""" + ARROW + """
<rect x="12" y="12" width="400" height="276" rx="10" class="d-box"/>
<text x="28" y="38" class="d-accent">HARNESS</text>
<text x="28" y="56" class="d-label-sm">prompt assembly \\u00b7 tool registry \\u00b7 turn limit \\u00b7 persistence</text>
<rect x="40" y="76" width="150" height="42" rx="6" class="d-box-accent"/>
<text x="60" y="102" class="d-label">1. Build context</text>
<rect x="40" y="146" width="150" height="42" rx="6" class="d-box-accent"/>
<text x="60" y="172" class="d-label">2. Call model</text>
<rect x="40" y="216" width="150" height="42" rx="6" class="d-box-accent"/>
<text x="52" y="236" class="d-label">3. Tool requested?</text>
<text x="52" y="252" class="d-label-sm">run it, append result</text>
<path d="M115 118 L115 146" class="d-arrow-accent" marker-end="url(#aa)"/>
<path d="M115 188 L115 216" class="d-arrow-accent" marker-end="url(#aa)"/>
<path d="M205 237 L240 237 L240 97 L205 97" class="d-arrow-accent" marker-end="url(#aa)"/>
<text x="250" y="160" class="d-label-sm">loop until</text>
<text x="250" y="176" class="d-label-sm">no tool needed</text>
<rect x="470" y="146" width="150" height="60" rx="8" class="d-box"/>
<text x="500" y="172" class="d-label-b">MODEL</text>
<text x="486" y="192" class="d-label-sm">text in, text out</text>
<path d="M195 160 L470 160" class="d-arrow" marker-end="url(#a)"/>
<path d="M470 192 L195 192" class="d-arrow" marker-end="url(#a)"/>
<text x="300" y="152" class="d-label-sm">context</text>
<text x="300" y="212" class="d-label-sm">text (maybe a tool request)</text>
</svg>'''),""", '("callout", "insight", "Why this matters"'),

"tokens-context-and-kv-cache": ("""("figure", "Everything competes for the same window. As history grows, the room left for retrieved context and the answer shrinks \\u2014 and the whole bar is re-sent every turn.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Context window composition and cost growth">
<text x="12" y="20" class="d-label-b">One context window</text>
<rect x="12" y="32" width="616" height="38" rx="5" class="d-box"/>
<rect x="14" y="34" width="90" height="34" rx="4" class="d-fill-accent" opacity="0.75"/>
<text x="26" y="56" class="d-label-sm">system</text>
<rect x="106" y="34" width="230" height="34" rx="4" class="d-fill-yellow" opacity="0.65"/>
<text x="170" y="56" class="d-label-sm">conversation history</text>
<rect x="338" y="34" width="180" height="34" rx="4" class="d-fill-green" opacity="0.6"/>
<text x="372" y="56" class="d-label-sm">retrieved context</text>
<rect x="520" y="34" width="106" height="34" rx="4" class="d-fill-muted" opacity="0.5"/>
<text x="540" y="56" class="d-label-sm">answer</text>
<text x="12" y="108" class="d-label-b">Tokens sent per turn</text>
<line x1="12" y1="180" x2="628" y2="180" class="d-arrow"/>
<rect x="40" y="168" width="26" height="12" class="d-fill-accent" opacity="0.8"/>
<rect x="110" y="150" width="26" height="30" class="d-fill-accent" opacity="0.8"/>
<rect x="180" y="130" width="26" height="50" class="d-fill-accent" opacity="0.8"/>
<rect x="250" y="104" width="26" height="76" class="d-fill-accent" opacity="0.8"/>
<rect x="320" y="122" width="26" height="58" class="d-fill-red" opacity="0.35"/>
<text x="40" y="196" class="d-label-sm">t1</text>
<text x="110" y="196" class="d-label-sm">t5</text>
<text x="180" y="196" class="d-label-sm">t10</text>
<text x="250" y="196" class="d-label-sm">t20</text>
<text x="380" y="130" class="d-label-sm">the whole conversation is</text>
<text x="380" y="146" class="d-label-sm">re-sent every single turn</text>
</svg>'''),""", '("callout", "pitfall", "The mistake this causes"'),

"weights-gguf-quantization": ("""("figure", "Same 70B model at four precisions. Four-bit is the usual default because the quality loss is small and the size reduction is what makes the model runnable at all.", '''<svg viewBox="0 0 640 200" role="img" aria-label="Model size by quantization level">
<text x="12" y="20" class="d-label-b">A 70B model on disk</text>
<rect x="120" y="34" width="500" height="24" rx="4" class="d-fill-muted" opacity="0.55"/>
<text x="12" y="51" class="d-label">F16</text>
<text x="628" y="51" class="d-label-sm" text-anchor="end">~140 GB</text>
<rect x="120" y="70" width="250" height="24" rx="4" class="d-fill-accent" opacity="0.6"/>
<text x="12" y="87" class="d-label">Q8_0</text>
<text x="380" y="87" class="d-label-sm">~70 GB \\u00b7 near-lossless</text>
<rect x="120" y="106" width="156" height="24" rx="4" class="d-fill-green" opacity="0.75"/>
<text x="12" y="123" class="d-label">Q5_K_M</text>
<text x="286" y="123" class="d-label-sm">~44 GB</text>
<rect x="120" y="142" width="125" height="24" rx="4" class="d-fill-green" opacity="0.9"/>
<text x="12" y="159" class="d-label">Q4_K_M</text>
<text x="255" y="159" class="d-label-sm">~35 GB \\u00b7 the usual default</text>
<text x="12" y="190" class="d-label-sm">Q = quantized \\u00b7 4 = bits per weight \\u00b7 K = k-quant method \\u00b7 M = medium size within that family</text>
</svg>'''),""", '("h2", "GGUF is the container")'),

"serving-locally": ("""("figure", "Your code never talks to the model directly. Each layer down is closer to the metal \\u2014 and the OpenAI-shaped API at the top is what makes the local and hosted lanes interchangeable.", '''<svg viewBox="0 0 640 250" role="img" aria-label="Local serving stack">""" + ARROW + """
<rect x="160" y="12" width="320" height="40" rx="6" class="d-box-accent"/>
<text x="180" y="37" class="d-label-b">Your code</text>
<text x="330" y="37" class="d-label-sm">HTTP, OpenAI-shaped</text>
<path d="M320 52 L320 76" class="d-arrow-accent" marker-end="url(#aa)"/>
<rect x="160" y="76" width="320" height="40" rx="6" class="d-box"/>
<text x="180" y="101" class="d-label-b">Ollama</text>
<text x="290" y="101" class="d-label-sm">registry \\u00b7 memory \\u00b7 model switching</text>
<path d="M320 116 L320 140" class="d-arrow" marker-end="url(#a)"/>
<rect x="160" y="140" width="320" height="40" rx="6" class="d-box"/>
<text x="180" y="165" class="d-label-b">llama.cpp</text>
<text x="300" y="165" class="d-label-sm">the actual arithmetic</text>
<path d="M320 180 L320 204" class="d-arrow" marker-end="url(#a)"/>
<rect x="160" y="204" width="320" height="36" rx="6" class="d-box"/>
<text x="180" y="227" class="d-label-b">Metal / unified memory</text>
<text x="392" y="227" class="d-label-sm">128 GB, high bandwidth</text>
<text x="500" y="101" class="d-label-sm">swap this URL and</text>
<text x="500" y="117" class="d-label-sm">you're on a frontier</text>
<text x="500" y="133" class="d-label-sm">model instead</text>
<path d="M492 96 L484 96" class="d-arrow"/>
</svg>'''),""", '("h2", "Reading tokens per second")'),

"embeddings-and-retrieval": ("""("figure", "Meaning becomes geometry. Phrases sharing no words land close together; the negation pair lands close too, which is exactly the failure mode to watch for.", '''<svg viewBox="0 0 640 260" role="img" aria-label="Embedding space with clusters">
<rect x="12" y="12" width="616" height="236" rx="8" class="d-box"/>
<circle cx="140" cy="80" r="6" class="d-fill-accent"/>
<circle cx="176" cy="98" r="6" class="d-fill-accent"/>
<circle cx="150" cy="118" r="6" class="d-fill-accent"/>
<ellipse cx="156" cy="99" rx="60" ry="46" fill="none" stroke="var(--accent)" stroke-dasharray="4 4" opacity="0.6"/>
<text x="106" y="172" class="d-label-sm">"reset my password"</text>
<text x="106" y="188" class="d-label-sm">"locked out of my account"</text>
<text x="106" y="204" class="d-label-sm">"can't sign in"</text>
<circle cx="420" cy="70" r="6" class="d-fill-green"/>
<circle cx="458" cy="88" r="6" class="d-fill-green"/>
<ellipse cx="439" cy="79" rx="48" ry="34" fill="none" stroke="var(--green)" stroke-dasharray="4 4" opacity="0.6"/>
<text x="392" y="140" class="d-label-sm">"where is my order"</text>
<text x="392" y="156" class="d-label-sm">"track my delivery"</text>
<circle cx="300" cy="212" r="6" class="d-fill-red"/>
<circle cx="316" cy="216" r="6" class="d-fill-red"/>
<text x="336" y="212" class="d-label-sm">"I want a refund" /</text>
<text x="336" y="228" class="d-label-sm">"I don't want a refund" \\u2014 too close</text>
<text x="24" y="36" class="d-label-sm">similar meaning \\u2192 similar direction</text>
</svg>'''),""", '("h2", "How semantic routing works in Bullpen")'),

"tool-calls-and-mcp": ("""("figure", "The model never touches the tool. It emits a request; the harness executes and returns the result as more text. Everything the model 'does' passes through that gap \\u2014 which is also where injected instructions get their leverage.", '''<svg viewBox="0 0 640 190" role="img" aria-label="Tool call round trip">""" + ARROW + """
<rect x="12" y="60" width="140" height="54" rx="7" class="d-box"/>
<text x="52" y="84" class="d-label-b">MODEL</text>
<text x="30" y="102" class="d-label-sm">emits JSON only</text>
<rect x="250" y="60" width="140" height="54" rx="7" class="d-box-accent"/>
<text x="288" y="84" class="d-label-b">HARNESS</text>
<text x="272" y="102" class="d-label-sm">parses &amp; executes</text>
<rect x="488" y="60" width="140" height="54" rx="7" class="d-box"/>
<text x="536" y="84" class="d-label-b">TOOL</text>
<text x="506" y="102" class="d-label-sm">reads your files</text>
<path d="M152 78 L250 78" class="d-arrow-accent" marker-end="url(#aa)"/>
<text x="158" y="70" class="d-label-sm">{"name":"read_file"...}</text>
<path d="M390 78 L488 78" class="d-arrow" marker-end="url(#a)"/>
<text x="410" y="70" class="d-label-sm">actual call</text>
<path d="M488 100 L390 100" class="d-arrow" marker-end="url(#a)"/>
<text x="408" y="118" class="d-label-sm">result</text>
<path d="M250 100 L152 100" class="d-arrow" marker-end="url(#a)"/>
<text x="160" y="118" class="d-label-sm">appended as text</text>
<text x="12" y="164" class="d-label-sm">The model chooses which tool to call \\u2014 and that choice is influenced by every piece of text in its context,</text>
<text x="12" y="180" class="d-label-sm">including text that arrived from a document or a web page. That is indirect prompt injection.</text>
</svg>'''),""", '("h2", "Why tool descriptions are prompt engineering")'),

"routing-and-escalation": ("""("figure", "Observation replaces prediction. The verifier is load-bearing \\u2014 remove it and there is no signal to escalate on, which is why subjective tasks can't use this pattern.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Escalation flow">""" + ARROW + """
<rect x="12" y="76" width="120" height="48" rx="7" class="d-box"/>
<text x="46" y="105" class="d-label-b">Request</text>
<path d="M132 100 L176 100" class="d-arrow" marker-end="url(#a)"/>
<rect x="176" y="76" width="130" height="48" rx="7" class="d-box-good"/>
<text x="200" y="98" class="d-label-b">Local model</text>
<text x="208" y="115" class="d-label-sm">free, fast</text>
<path d="M306 100 L350 100" class="d-arrow" marker-end="url(#a)"/>
<polygon points="350,100 412,72 474,100 412,128" class="d-box-accent"/>
<text x="378" y="96" class="d-label-sm">verifier</text>
<text x="374" y="112" class="d-label-sm">passed?</text>
<path d="M474 100 L560 100" class="d-arrow" marker-end="url(#a)"/>
<text x="492" y="92" class="d-accent">yes</text>
<rect x="560" y="78" width="68" height="44" rx="7" class="d-box-good"/>
<text x="576" y="105" class="d-label">done</text>
<path d="M412 128 L412 168 L560 168" class="d-arrow" marker-end="url(#a)"/>
<text x="424" y="162" class="d-fill-red" font-size="12" font-weight="600">no</text>
<rect x="560" y="146" width="68" height="44" rx="7" class="d-box-warn"/>
<text x="572" y="166" class="d-label">escalate</text>
<text x="572" y="182" class="d-label-sm">paid</text>
<text x="12" y="36" class="d-label-sm">Compilation, tests, schema validation and malformed tool calls are all checkable \\u2014 those make good verifiers.</text>
<text x="12" y="52" class="d-label-sm">"Is this prose any good?" is not, so there is nothing to route on.</text>
</svg>'''),""", '("h2", "What escalation costs")'),

"eval-battery": ("""("figure", "Grade as far up this ladder as the task allows. Every step down costs you certainty, and the bottom rung can be circular.", '''<svg viewBox="0 0 640 200" role="img" aria-label="Grading methods ranked by trustworthiness">
<rect x="12" y="16" width="440" height="44" rx="6" class="d-box-good"/>
<text x="30" y="38" class="d-label-b">Deterministic</text>
<text x="30" y="54" class="d-label-sm">compiles \\u00b7 tests pass \\u00b7 schema validates</text>
<text x="470" y="44" class="d-fill-green" font-size="12" font-weight="600">most trustworthy</text>
<rect x="12" y="72" width="440" height="44" rx="6" class="d-box"/>
<text x="30" y="94" class="d-label-b">Reference match</text>
<text x="30" y="110" class="d-label-sm">compare to a known-good answer \\u00b7 brittle when many answers are valid</text>
<rect x="12" y="128" width="440" height="44" rx="6" class="d-box-warn"/>
<text x="30" y="150" class="d-label-b">Model-as-judge</text>
<text x="30" y="166" class="d-label-sm">flexible \\u00b7 inherits the judge's bias \\u00b7 circular if judge = model under test</text>
<text x="470" y="156" class="d-fill-red" font-size="12" font-weight="600">last resort</text>
<path d="M600 30 L600 160" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="4 4"/>
</svg>'''),""", '("callout", "pitfall", "The trap the harness is named for"'),
}

path = pathlib.Path("scripts/content/bullpen_vocabulary.py")
lines = path.read_text().split("\n")
inserted = 0
for slug, (fig, anchor) in FIGURES.items():
    slug_i = next(i for i, l in enumerate(lines) if f'"slug": "{slug}"' in l)
    try:
        anchor_i = next(i for i in range(slug_i, len(lines)) if anchor in lines[i])
    except StopIteration:
        print(f"  !! anchor not found for {slug}"); sys.exit(1)
    lines.insert(anchor_i, "    " + fig)
    inserted += 1
path.write_text("\n".join(lines))
print(f"inserted {inserted} figures")
