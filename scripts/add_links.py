#!/usr/bin/env python3
"""Insert a verified further-reading block before the quiz in each lesson."""
import pathlib, sys

L = {
"agent-loop-and-harness": [
 ("Building effective agents", "https://www.anthropic.com/engineering/building-effective-agents",
  "Anthropic's engineering write-up on when a loop is warranted and when a fixed workflow is better."),
 ("Bullpen: docs/agent-runtime-design.md", "https://github.com/stylusnexus/Bullpen",
  "Your own loop, written down. Read it alongside this lesson."),
],
"tokens-context-and-kv-cache": [
 ("Lost in the Middle (Liu et al., 2023)", "https://arxiv.org/abs/2307.03172",
  "The paper behind the U-shaped attention finding. Short and worth reading properly."),
 ("Prompt caching", "https://docs.claude.com/en/docs/build-with-claude/prompt-caching",
  "The KV cache sold as a feature — note the rules about what invalidates a cached prefix."),
],
"weights-gguf-quantization": [
 ("GGUF on the Hugging Face Hub", "https://huggingface.co/docs/hub/gguf",
  "Format reference, and the quantization table naming every Q-variant."),
 ("llama.cpp", "https://github.com/ggml-org/llama.cpp",
  "The engine. The README's quantization section is the primary source for the trade-offs here."),
],
"serving-locally": [
 ("Ollama", "https://ollama.com", "Model registry and the local OpenAI-compatible server."),
 ("vLLM documentation", "https://docs.vllm.ai",
  "What you move to when one developer becomes many concurrent users — the contrast is instructive."),
],
"embeddings-and-retrieval": [
 ("Sentence Transformers", "https://sbert.net",
  "The practical library for embeddings, with clear docs on model choice and similarity."),
 ("pgvector", "https://github.com/pgvector/pgvector",
  "The Postgres extension Block 3 uses. Read the indexing notes before loading real data."),
],
"tool-calls-and-mcp": [
 ("Model Context Protocol", "https://modelcontextprotocol.io",
  "The specification. The Tools / Resources / Prompts split is clearer here than anywhere else."),
 ("Tool use overview", "https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview",
  "How a tool call is actually shaped on the wire, with the schema conventions."),
],
"routing-and-escalation": [
 ("RouteLLM (Ong et al., 2024)", "https://arxiv.org/abs/2406.18665",
  "The predict-which-model approach Bullpen deliberately inverts. Useful for arguing with."),
 ("Bullpen: docs/routing-strategy.md", "https://github.com/stylusnexus/Bullpen",
  "Your own strategy doc — the escalation criteria in prose."),
],
"eval-battery": [
 ("honest-bench", "https://github.com/stylusnexus/honest-bench",
  "Your eval harness (private repo). The premise — replay closed PRs so the outcome is known in advance — is the lesson."),
 ("Google ML Crash Course: overfitting", "https://developers.google.com/machine-learning/crash-course/overfitting/overfitting",
  "Short, visual treatment of held-out evaluation if you want a second angle."),
],
"overfitting-and-underfitting": [
 ("Cross-validation (scikit-learn)", "https://scikit-learn.org/stable/modules/cross_validation.html",
  "The canonical reference, with the diagrams. You'll use this directly in Block 2."),
 ("Google ML Crash Course: overfitting", "https://developers.google.com/machine-learning/crash-course/overfitting/overfitting",
  "Generalisation, regularisation and early stopping, worked through interactively."),
],
"agents-autonomy-and-danger": [
 ("OWASP Top 10 for LLM Applications", "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
  "The reference list of agent and LLM attack classes. Block 6 works through it."),
 ("Simon Willison on prompt injection", "https://simonwillison.net/tags/prompt-injection/",
  "The clearest running commentary on why this isn't solved by better prompting."),
 ("agent-armor", "https://github.com/stylusnexus/agent-armor",
  "Your own defence framework — the trap taxonomy maps onto this lesson's danger surface."),
],
"feedback-rlhf-and-humans": [
 ("InstructGPT (Ouyang et al., 2022)", "https://arxiv.org/abs/2203.02155",
  "The RLHF pipeline paper. Figure 2 is the diagram in this lesson, done properly."),
 ("Direct Preference Optimization (Rafailov et al., 2023)", "https://arxiv.org/abs/2305.18290",
  "Why the reward model and RL stage can be collapsed into one step."),
 ("Constitutional AI (Bai et al., 2022)", "https://arxiv.org/abs/2212.08073",
  "Self-critique against written principles, and how Claude is trained."),
 ("TRL documentation", "https://huggingface.co/docs/trl",
  "The library you'll actually run DPO with in Block 7."),
],
"context-engineering": [
 ("Lost in the Middle (Liu et al., 2023)", "https://arxiv.org/abs/2307.03172",
  "The evidence for the U-shaped curve. Read it once; it changes how you order retrieved material."),
 ("Prompt caching", "https://docs.claude.com/en/docs/build-with-claude/prompt-caching",
  "The mechanical reason stable content goes at the front."),
],
"structured-output-json": [
 ("Structured outputs (OpenAI)", "https://platform.openai.com/docs/guides/structured-outputs",
  "Rung 3 of the ladder, documented — schema-constrained generation and its limits."),
 ("GBNF grammars in llama.cpp", "https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md",
  "Rung 4. Constrained decoding, where invalid output is made unrepresentable."),
 ("Pydantic", "https://docs.pydantic.dev",
  "Validation that checks values, not just shape. The repair loop hangs off its error messages."),
],
}

path = pathlib.Path("scripts/content/bullpen_vocabulary.py")
lines = path.read_text().split("\n")
n = 0
for slug, links in L.items():
    try:
        si = next(i for i, l in enumerate(lines) if f'"slug": "{slug}"' in l)
        qi = next(i for i in range(si, len(lines)) if lines[i].lstrip().startswith('("quiz",'))
    except StopIteration:
        print(f"  !! anchor missing for {slug}"); sys.exit(1)
    block = '    ("links", [\n' + "".join(
        f'      ({t!r}, {u!r},\n       {note!r}),\n' for t, u, note in links) + "    ]),"
    lines.insert(qi, block); n += 1
path.write_text("\n".join(lines))
print(f"added further-reading to {n} lessons")
