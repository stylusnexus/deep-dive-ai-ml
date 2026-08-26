TITLE = "Block 4 · Agentic AI"
TOPIC = "block4-agentic"
ICON = "🤖"
DESCRIPTION = "Building the agent loop by hand before reaching for a framework, then what a graph runtime buys, then multi-agent systems and the approval gates that actually halt."
TAGS = ["ai", "agents", "langgraph"]
COLOR = "amber"
CREATED = "2026-08-21"
ID_BASE = "1787700000"

LESSONS = [
{
  "slug": "the-loop-by-hand",
  "title": "The Agent Loop, By Hand",
  "subtitle": "Forty lines. Build it once and every framework afterwards is legible.",
  "body": [
    ("p", "The vocabulary lesson said an agent is a while-loop that runs until something says stop. This lesson writes it. The point is not that you should ship this — it is that after writing it, LangGraph and every other framework stop being magic and become a set of decisions you can evaluate."),

    ("h2", "The whole thing"),
    ("code", """def run(question, tools, max_turns=8, max_spend=0.50):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    spend = 0.0

    for turn in range(max_turns):
        reply, cost = call_model(messages, tools)
        spend += cost
        messages.append(reply)

        if not reply.get("tool_calls"):
            return {"answer": reply["content"], "reason": "completed",
                    "turns": turn + 1, "spend": spend}

        for call in reply["tool_calls"]:
            result = execute(call, tools)              # the harness runs it, not the model
            messages.append({"role": "tool",
                             "tool_call_id": call["id"],
                             "content": truncate(result, 4000)})

        if spend > max_spend:
            return {"answer": None, "reason": "spend_cap", "turns": turn + 1, "spend": spend}

    return {"answer": None, "reason": "turn_cap", "turns": max_turns, "spend": spend}"""),

    ("h2", "Five decisions hiding in that code"),
    ("terms", [
      ("The termination set", "Three exits, each named", "Completed, spend cap, turn cap. The caller can distinguish them, which the operating lesson insisted on. A loop with one exit tells you nothing about why it stopped."),
      ("Truncating tool results", "4000 characters", "Tool results are context. A raw file dump swamps the window and is re-sent every subsequent turn. This one line is most of your context budget."),
      ("The harness executes", "Not the model", "The model emits a request; <code>execute</code> runs it. Everything you allow that function to do is what the agent can do — which is where the security lesson lives."),
      ("Messages accumulate", "And are re-sent whole", "Turn eight sends eight turns of history. Cost grows with the square of the conversation, which is why the caps are not optional."),
      ("No self-assessment", "Deliberately", "The loop never asks the model whether it is finished. It exits when the model stops requesting tools — an observable event, not an opinion."),
    ]),

    ("know",
     "Terminate on an observable event, never on the model's opinion that it is done.",
     "The loop above exits when no tool call is present in the reply — a fact about the response, checkable by the harness. Asking the model whether it has finished hands the stopping decision to the component least able to judge, and it will say yes when it has the shape of an answer.",
     "An agent asked to fix a failing test replies 'I have resolved the issue' while its last edit broke the build. Exiting on that sentence ships a broken tree. Exiting on 'no tool call requested, then run the tests' produces a verdict the harness can check."),

    ("h2", "What the model actually receives"),
    ("p", "Worth seeing once, because the mental model of \"the agent has tools\" hides what is really happening. Every turn, the harness sends the entire conversation plus a list of tool definitions, and receives text back. That is the whole interface."),

    ("figure", "The model never touches a tool. It emits a request; the harness executes and appends the result as another message. Everything the agent can do is defined by what execute() permits.", '''<svg viewBox="0 0 640 225" role="img" aria-label="One turn of an agent loop"><defs><marker id="l4" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="12" y="26" width="170" height="70" rx="7" class="d-box-accent"/>
<text x="28" y="48" class="d-label-b">HARNESS sends</text>
<text x="28" y="68" class="d-label-sm">whole message history</text>
<text x="28" y="84" class="d-label-sm">+ tool definitions</text>
<path d="M182 61 L232 61" class="d-arrow-accent" marker-end="url(#l4)"/>
<rect x="232" y="26" width="150" height="70" rx="7" class="d-box"/>
<text x="248" y="48" class="d-label-b">MODEL</text>
<text x="248" y="68" class="d-label-sm">returns text, which</text>
<text x="248" y="84" class="d-label-sm">may contain a request</text>
<path d="M382 61 L432 61" class="d-arrow-accent" marker-end="url(#l4)"/>
<rect x="432" y="26" width="196" height="70" rx="7" class="d-box-warn"/>
<text x="448" y="48" class="d-label-b">execute()</text>
<text x="448" y="68" class="d-label-sm">the only thing that acts</text>
<text x="448" y="84" class="d-fill-red" font-size="11" font-weight="600">your entire blast radius</text>
<path d="M530 96 L530 126 L97 126 L97 100" class="d-arrow-accent" marker-end="url(#l4)"/>
<text x="236" y="144" class="d-label-sm">result appended as a message, and the loop goes again</text>
<rect x="12" y="158" width="616" height="54" rx="7" class="d-box"/>
<text x="28" y="180" class="d-label-b">Three ways out, each named</text>
<text x="28" y="200" class="d-label-sm">no tool requested (completed) · spend cap · turn cap — and the caller can tell which</text>
</svg>'''),

    ("h2", "Tool definitions are the interface"),
    ("p", "The model chooses from names and descriptions. Everything from the tool-calls lesson applies, and two things matter more than the rest:"),
    ("ul", [
      "<strong>Write descriptions for someone who has never seen your system.</strong> This is the highest-leverage text in the whole agent, and it is usually written last and fastest.",
      "<strong>Errors should name the fix.</strong> Returning \"invalid request\" burns a turn. Returning \"start_date must be ISO 8601, received 03/04/2026\" gets corrected on the next one, which is a real difference in a loop with eight turns.",
      "<strong>Enforce preconditions in the tool, not the prompt.</strong> The compliance test from the practice set: can the model tell when it has complied? A refusal it can act on beats an instruction it cannot finish.",
      "<strong>Shape the return value for a model, not for a log.</strong> Raw API responses are a context-budget disaster and the model has to parse them out of your JSON.",
    ]),

    ("h2", "State that survives the loop"),
    ("p", "The messages list is working memory and it is volatile — compacted, truncated, eventually gone. Anything the agent must not forget belongs somewhere else."),
    ("terms", [
      ("Message history", "Volatile", "Grows, gets compacted, and loses things silently."),
      ("Explicit state object", "Durable", "A dictionary the loop threads through: the plan, what has been tried, what is known. Cheap and it survives compaction."),
      ("External notes", "Most durable", "A file the agent writes and re-reads. Survives a restart, which the other two do not."),
    ]),
    ("callout", "matters", "Add the state object before you think you need it", "A loop that carries only messages works fine for four turns and degrades from there — the plan formed at turn two gets summarised at turn twelve into something slightly different. Threading an explicit state dictionary costs almost nothing at the start and is intrusive to retrofit, because every node then has to be rewritten to accept it."),

    ("h2", "What you will want next, and that is the argument for a framework"),
    ("p", "Run this loop for a while and a predictable list of wants appears: resuming after a crash without replaying everything, pausing for human approval mid-run, branching to different handling by task type, running two independent tool calls at once, and inspecting what happened on turn six of a run that finished yesterday."),
    ("p", "Each is a few days of careful work. All of them together is a graph runtime, which is what the next lesson is about — and having felt the want is what lets you judge whether the framework's answer is a good one."),

    ("links", [
      ("Building effective agents — Anthropic", "https://www.anthropic.com/engineering/building-effective-agents",
       "The argument for the simplest loop that works, and when a fixed workflow beats an agent entirely."),
      ("Tool use overview", "https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview",
       "The wire format for tool definitions and tool results."),
    ]),

    ("quiz", [
      ("Why does the loop exit on 'no tool call requested' rather than asking the model whether it is done?",
       ["It saves a model call",
        "Absence of a tool call is an observable fact the harness can check; the model's opinion of its own success is not",
        "The model cannot reliably produce a stop token"], 1),
      ("What defines the blast radius of an agent?",
       ["The model's capabilities",
        "Whatever execute() is permitted to do — the model only ever emits a request",
        "The number of turns allowed"], 1),
      ("Why truncate tool results?",
       ["To fit within the model's maximum response length",
        "Tool results are context, re-sent every subsequent turn — one large dump swamps the budget for the rest of the run",
        "To speed up the tool itself"], 1),
      ("When should you add an explicit state object rather than relying on message history?",
       ["When the loop exceeds twenty turns",
        "At the start — it is cheap then and intrusive to retrofit, because every node must be rewritten to accept it",
        "Only if you need to resume after a crash"], 1),
    ]),
  ],
},
{
  "slug": "what-a-graph-buys",
  "title": "What a Graph Runtime Buys",
  "subtitle": "The five things you wanted after writing the loop by hand — and what they cost.",
  "body": [
    ("p", "LangGraph models an agent as a state graph: nodes that transform state, edges that decide what runs next. That framing sounds like ceremony until you match it against the list of wants from the previous lesson, at which point each piece is answering a specific problem you already had."),

    ("h2", "The model in one paragraph"),
    ("terms", [
      ("State", "A typed dictionary threaded through everything", "The explicit state object the last lesson told you to add early, made structural. Every node receives it and returns updates to it."),
      ("Nodes", "Functions that transform state", "Call the model, run a tool, summarise, validate. Ordinary functions — no framework magic inside them."),
      ("Edges", "What runs next", "Fixed, or conditional on the state. A conditional edge back to an earlier node is the loop."),
      ("Checkpointer", "Persists state after every node", "This is the one that changes what is possible, and it is covered below."),
    ]),
    ("code", """from langgraph.graph import StateGraph, END

def call_model(state):  ...      # returns {"messages": [...]}
def run_tools(state):   ...      # returns {"messages": [...]}

g = StateGraph(AgentState)
g.add_node("model", call_model)
g.add_node("tools", run_tools)
g.set_entry_point("model")
g.add_conditional_edges("model", needs_tool, {"tools": "tools", "done": END})
g.add_edge("tools", "model")     # the loop
agent = g.compile(checkpointer=saver)"""),
    ("p", "That is the same loop as the previous lesson, with the control flow lifted out of a <code>for</code> statement and made data. Which is what makes the rest possible."),

("figure", "The same loop, with control flow lifted out of a for-statement and made data. That is what lets something else — a checkpointer, a human, a debugger — get between the steps.", '''<svg viewBox="0 0 640 215" role="img" aria-label="An agent as a state graph"><defs><marker id="g4" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<rect x="12" y="30" width="88" height="34" rx="5" class="d-box"/><text x="30" y="52" class="d-label-sm">START</text>
<path d="M100 47 L134 47" class="d-arrow-accent" marker-end="url(#g4)"/>
<rect x="134" y="30" width="112" height="34" rx="5" class="d-box-accent"/><text x="158" y="52" class="d-label-sm">model node</text>
<path d="M246 47 L280 47" class="d-arrow-accent" marker-end="url(#g4)"/>
<polygon points="280,47 340,24 400,47 340,70" class="d-box"/>
<text x="304" y="51" class="d-label-sm">tool call?</text>
<path d="M400 47 L440 47" class="d-arrow-accent" marker-end="url(#g4)"/>
<rect x="440" y="30" width="112" height="34" rx="5" class="d-box"/><text x="466" y="52" class="d-label-sm">tools node</text>
<path d="M496 64 L496 92 L190 92 L190 66" class="d-arrow-accent" marker-end="url(#g4)"/>
<text x="266" y="108" class="d-label-sm">conditional edge back: this is the loop</text>
<path d="M340 70 L340 128" class="d-arrow-accent" marker-end="url(#g4)"/>
<rect x="300" y="128" width="80" height="30" rx="5" class="d-box-good"/><text x="326" y="148" class="d-label-sm">END</text>
<rect x="12" y="168" width="616" height="40" rx="6" class="d-box-warn"/>
<text x="28" y="192" class="d-label-sm">Checkpointer saves state after every node — which is what makes pausing, resuming and inspecting possible.</text>
</svg>'''),

        ("h2", "The five things it buys"),
    ("terms", [
      ("Resumption", "State is saved after every node", "A crash on turn nine resumes at turn nine rather than replaying eight turns of model calls. On a long run this is the difference between an annoyance and a lost afternoon."),
      ("Interrupts", "Pause before a node, resume later", "The approval gate that actually halts. Covered properly in the next lesson, and it is the strongest single argument for the framework."),
      ("Branching", "Conditional edges", "Route by task type without a growing thicket of if-statements inside one function."),
      ("Parallelism", "Independent nodes run together", "Two retrievals that do not depend on each other take one node's worth of wall clock rather than two."),
      ("Inspectability", "The state history is a record", "What the state was at every step of a run that finished yesterday. This is the trajectory log from the operating lesson, produced by construction rather than by discipline."),
    ]),

    ("know",
     "Checkpointing is the feature; everything else is convenience.",
     "Branching, parallelism and typed state are all things you could write yourself in an afternoon. Persisting state after every node — so a run can be interrupted, inspected, resumed on another machine, or paused for a human — is genuinely hard to retrofit, and it is what makes approval gates and long-running agents possible at all.",
     "A three-hour agent run crashes at hour two on a transient API error. Without checkpointing you re-run from the start and pay for every model call again. With it you resume from the last completed node. The same mechanism is what lets the run stop and wait for a human overnight."),

    ("h2", "What it costs"),
    ("ul", [
      "<strong>Indirection.</strong> A stack trace now runs through framework code. When something misbehaves you are debugging your logic and its runtime at once.",
      "<strong>A version surface.</strong> The API has moved repeatedly and will again. That is a maintenance cost you have signed up for.",
      "<strong>Conceptual overhead for simple cases.</strong> A two-node graph is more code and more concepts than a <code>while</code> loop, and no better.",
      "<strong>Easy over-modelling.</strong> Graphs invite nodes. A twelve-node graph where three would do is harder to reason about than the loop it replaced.",
    ]),
    ("callout", "matters", "Take the framework when you need the checkpointer", "If your agent runs for seconds, never pauses, and does one thing, the hand-written loop is better — fewer dependencies, a stack trace you own, and nothing to keep up with. Reach for the graph when you need to pause, resume, branch meaningfully, or inspect a finished run. That is a decision about requirements, not about sophistication."),

    ("h2", "The state design decision"),
    ("p", "The one thing worth getting right up front, because it is expensive to change later: what goes in the state, and how updates combine."),
    ("code", """from typing import Annotated, TypedDict
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list, add]     # nodes append; updates are concatenated
    plan: str                          # nodes replace; last write wins
    findings: Annotated[list, add]     # append
    turn: int                          # replace
    approved: bool"""),
    ("p", "The annotation decides how two updates to the same key combine. <code>add</code> concatenates, which is what you want for anything accumulating. No annotation means replacement, which is what you want for a current value. Getting this wrong produces a bug that looks like the agent forgetting things — because it is."),

    ("h2", "Where it fits with everything else"),
    ("p", "The graph does not change what an agent is. The loop is the same loop, the model still only emits text, and <code>execute</code> is still the entire blast radius. What changes is that the control flow is now data rather than code, which is what lets something else — a checkpointer, a human, a debugger — get between the steps."),
    ("callout", "pitfall", "The framework does not supply judgement", "Nothing here decides your termination conditions, your tool permissions, your approval gates or your budget caps. A graph with no turn limit spins exactly as a <code>while True</code> does. Every discipline from the operating and danger lessons still applies, and the framework will happily let you skip all of it."),

    ("links", [
      ("LangGraph documentation", "https://langchain-ai.github.io/langgraph/",
       "State, nodes, edges and the checkpointer, with the concepts in the order this lesson uses them."),
      ("Building effective agents — Anthropic", "https://www.anthropic.com/engineering/building-effective-agents",
       "Worth re-reading here: the argument that most tasks need a workflow rather than an agent applies to graphs too."),
    ]),

    ("quiz", [
      ("Which LangGraph feature is genuinely hard to write yourself?",
       ["Conditional branching between nodes",
        "Checkpointing state after every node — it is what makes resumption, interrupts and inspection possible",
        "Typed state dictionaries"], 1),
      ("Your agent runs for two seconds, never pauses, and does one thing. What should you use?",
       ["A graph, for consistency with future agents",
        "The hand-written loop — fewer dependencies, a stack trace you own, nothing to keep up with",
        "A graph, because frameworks are more reliable than custom code"], 1),
      ("What does an Annotated[list, add] state field do that a plain list does not?",
       ["Validates the list contents",
        "Concatenates updates from nodes rather than replacing — which is what you want for anything accumulating",
        "Persists it to the checkpointer"], 1),
      ("What does adopting a graph runtime change about the agent's blast radius?",
       ["It sandboxes tool execution automatically",
        "Nothing — the tool executor is still the entire blast radius, and the framework supplies no judgement about limits",
        "It adds approval gates by default"], 1),
    ]),
  ],
},
{
  "slug": "multi-agent-and-approval",
  "title": "Multi-Agent Systems and Gates That Actually Halt",
  "subtitle": "When to split an agent, what it costs, and why most approval gates do not stop what matters.",
  "body": [
    ("p", "Two topics that belong together, because the same mechanism underlies both: a multi-agent system is a graph where control passes between specialised nodes, and an approval gate is a graph that stops and waits. Both depend on the state being persistable, which is the previous lesson's point arriving in practice."),

    ("h2", "When splitting is justified"),
    ("p", "The vocabulary lesson gave the answer that survives scrutiny: <strong>context isolation</strong>, not specialisation. A sub-agent explores in a clean window and returns a distilled summary, so the expensive search never touches the main context. Specialisation alone is usually an org chart being imitated rather than a constraint being solved."),
    ("terms", [
      ("Sub-agent as a tool", "Called, returns, disappears", "The simplest useful form and the one to reach for first. The parent does not manage it; it calls it like any other tool."),
      ("Orchestrator and workers", "One plans, several execute", "Works when subtasks are genuinely independent. Fails when they need each other's intermediate results, at which point you have built a slow, expensive single agent."),
      ("Planner, generator, evaluator", "Roles that conflict, separated", "The evaluator has a different context from the generator, so it is not marking its own work. This is the judging lesson's independence requirement expressed as architecture."),
    ]),

    ("know",
     "Every handoff is a place where context is lost and error compounds.",
     "State that was implicit in one agent's context must become explicit to cross a boundary, and whatever you forget to pass simply does not exist on the other side. Five agents is not five times the debugging difficulty — it is worse, because the failures are now in the seams.",
     "An orchestrator delegates research to three workers and synthesis to a fourth. The synthesiser produces a confident summary missing the caveat one worker found, because the worker's summary dropped it as a detail. Nothing errored. Every agent did its job. The finding was lost in a handoff."),

    ("h2", "The cost nobody budgets"),
    ("p", "Parallel agents multiply token spend, and each carries its own growing context. A fan-out of five is more than five times one agent's cost, because coordination and summarisation are extra turns on top. Measure it before scaling out — the pattern that reads as efficient on an architecture diagram is frequently the most expensive component in the system."),

    ("h2", "Approval gates, and why most of them do not work"),
    ("p", "The operating lesson made the distinction; here is what it means in code. Most approval implementations gate <em>admission</em> — they check a flag before starting new work. An agent already mid-trajectory with a write-capable tool sails straight through."),

    ("figure", "Admission control stops new runs. It does nothing about the run already in flight, which is the one holding a write-capable tool. Only a checked interrupt between nodes halts that.", '''<svg viewBox="0 0 640 215" role="img" aria-label="Admission control versus a real interrupt"><defs><marker id="a4" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-muted"/></marker></defs>
<text x="12" y="18" class="d-fill-red" font-size="12" font-weight="600">ADMISSION CONTROL — stops the wrong thing</text>
<rect x="12" y="28" width="96" height="30" rx="5" class="d-box"/><text x="26" y="48" class="d-label-sm">new request</text>
<path d="M108 43 L138 43" class="d-arrow" marker-end="url(#a4)"/>
<polygon points="138,43 176,25 214,43 176,61" class="d-box-warn"/>
<text x="152" y="47" class="d-label-sm">flag?</text>
<path d="M214 43 L246 43" class="d-arrow" marker-end="url(#a4)"/>
<rect x="246" y="28" width="90" height="30" rx="5" class="d-box-good"/><text x="264" y="48" class="d-label-sm">blocked</text>
<rect x="392" y="28" width="236" height="30" rx="5" class="d-box-warn"/>
<text x="406" y="48" class="d-label-sm">run already in flight: finishes its writes</text>
<line x1="12" y1="80" x2="628" y2="80" stroke="var(--border)"/>
<text x="12" y="104" class="d-fill-green" font-size="12" font-weight="600">INTERRUPT — stops the run that matters</text>
<rect x="12" y="116" width="80" height="30" rx="5" class="d-box"/><text x="26" y="136" class="d-label-sm">node A</text>
<path d="M92 131 L120 131" class="d-arrow" marker-end="url(#a4)"/>
<rect x="120" y="116" width="120" height="30" rx="5" class="d-box-accent"/>
<text x="132" y="136" class="d-label-sm">checkpoint saved</text>
<path d="M240 131 L268 131" class="d-arrow" marker-end="url(#a4)"/>
<polygon points="268,131 316,110 364,131 316,152" class="d-box-good"/>
<text x="288" y="135" class="d-label-sm">approved?</text>
<path d="M364 131 L396 131" class="d-arrow" marker-end="url(#a4)"/>
<rect x="396" y="116" width="110" height="30" rx="5" class="d-box"/><text x="412" y="136" class="d-label-sm">write tool</text>
<path d="M316 152 L316 178" class="d-arrow" marker-end="url(#a4)"/>
<text x="330" y="182" class="d-label-sm">no: halt here, state persisted, resume when a human says so</text>
</svg>'''),

    ("know",
     "An approval gate that only checks before starting is not a stop button.",
     "Halting new work and halting work in progress are different mechanisms. The run you actually need to stop is the one already holding a write-capable tool, and it will finish unless something is checked between its steps.",
     "A flag is flipped to halt an agent that is mis-tagging customer records. New runs are refused immediately. The three runs already in flight keep going for another four minutes and write two hundred more records, because nothing between their steps was checking anything."),

    ("h2", "What an interrupt requires"),
    ("terms", [
      ("A checkpoint before the gated node", "So state survives the pause", "Without persistence the pause is just a crash."),
      ("A durable pending record", "Not an in-memory queue", "The approval may arrive tomorrow, after a deploy."),
      ("Identity on the decision", "Who approved, when, what exactly", "This is the audit trail. \"Approved\" without those three is not one."),
      ("A timeout with a default", "Usually deny", "Approvals get forgotten. Decide now what happens after 24 hours, or the system decides by hanging."),
      ("Enough context to decide", "The diff, not the summary", "An approver shown 'the agent wants to update 3 records' cannot approve meaningfully. Show which records and what changes."),
    ]),
    ("callout", "pitfall", "The gate that trains people to click yes", "An approval that fires on everything gets approved reflexively within a week, and you have added latency while removing nothing. Gate the irreversible and the outward-facing — sending, publishing, deleting, paying, merging — and let the rest through. A gate that is always right to approve is not a control, it is a delay."),

    ("h2", "What to log, since you now have several actors"),
    ("p", "Everything the operating lesson asked for, plus the seams: which agent produced which message, what crossed each handoff, and what was dropped in each summarisation. That last one is not usually recorded and it is where the failures live."),

    ("h2", "The honest default"),
    ("p", "Use the fewest agents that do the job. Start with one, add a sub-agent when a specific context is being polluted by a specific exploration, and gate only what cannot be undone. Every addition beyond that should be answering a constraint you have observed rather than a diagram you find appealing."),

    ("links", [
      ("How we built our multi-agent research system — Anthropic", "https://www.anthropic.com/engineering/multi-agent-research-system",
       "Production experience with orchestrator-worker, including where it did not pay off."),
      ("LangGraph human-in-the-loop", "https://langchain-ai.github.io/langgraph/",
       "Interrupts, checkpointing and resuming — the mechanism this lesson describes."),
      ("Effective harnesses for long-running agents", "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents",
       "Planner, generator and evaluator over multi-hour sessions, and what the architecture costs."),
    ]),

    ("quiz", [
      ("What is the argument for multi-agent that survives scrutiny?",
       ["Specialised agents perform better at specialised tasks",
        "Context isolation — a sub-agent explores in a clean window and returns a summary, so the search never touches the main context",
        "Parallel agents are faster"], 1),
      ("You flip a flag to halt a misbehaving agent. What keeps happening?",
       ["Nothing — the flag stops all activity",
        "Runs already in flight finish their writes, unless something between their steps is checking",
        "Only queued runs continue"], 1),
      ("What does an approval request need beyond 'the agent wants to do X'?",
       ["A confidence score from the model",
        "The specific change — the diff, not the summary — or the approver cannot decide meaningfully",
        "An estimate of how long the approval will take"], 1),
      ("What should be logged in a multi-agent system that is not logged in a single-agent one?",
       ["Each agent's token usage",
        "What crossed each handoff and what each summarisation dropped — the seams are where the failures live",
        "The order in which agents were invoked"], 1),
    ]),
  ],
},
{
  "slug": "telemetry-and-instrumentation",
  "title": "Telemetry: Making the Run Legible",
  "subtitle": "You cannot reproduce an agent run. The trace is the only evidence it happened the way you think.",
  "body": [
    ("p", "Every other lesson in this course assumes you can find out what happened. That assumption is doing a great deal of work, and it is false by default. An agent run cannot be reproduced — sampling varies, retrieval varies, external state moves, and the model behind a version alias may not be the one you called yesterday."),
    ("p", "So the trace is not a debugging convenience. It is the <strong>only artefact</strong> that survives, and gaps in it are outages of your ability to know anything."),

    ("h2", "The vocabulary, because it is standard and worth using"),
    ("terms", [
      ("Trace", "One end-to-end run", "Everything that happened in service of a single request, tied together by one identifier."),
      ("Span", "One unit of work inside it", "A model call, a retrieval, a tool execution. Spans nest — a tool span sits inside the turn span that requested it."),
      ("Attributes", "Structured facts on a span", "Model name, token counts, latency, the tool's arguments. Queryable, unlike a log line."),
      ("Events", "Timestamped things within a span", "A retry, a cache miss, a guard firing."),
      ("Baggage", "Context carried across boundaries", "The trace id following a request into a sub-agent, so the whole tree stays connected."),
    ]),
    ("p", "This is OpenTelemetry's model, and it is worth adopting even if you never export to a vendor, because it forces the question <em>what is a unit of work here?</em> — which is the question that makes a trace readable."),

    ("h2", "What to record on every agent run"),
    ("figure", "A trace is a tree. The value is in the leaves — arguments, results, token counts — and in the fact that the whole tree shares one identifier, so a complaint about one answer resolves to one tree.", '''<svg viewBox="0 0 640 235" role="img" aria-label="The span tree of one agent run">
<rect x="12" y="16" width="616" height="26" rx="4" class="d-box-accent"/>
<text x="26" y="34" class="d-label-sm">trace: request 8f3a — 12.4s, 4 turns, 18,400 tokens, terminated: completed</text>
<rect x="40" y="50" width="560" height="24" rx="4" class="d-box"/>
<text x="54" y="67" class="d-label-sm">span: turn 1 — model call, 1,900 tok, 2.1s</text>
<rect x="68" y="80" width="510" height="24" rx="4" class="d-box"/>
<text x="82" y="97" class="d-label-sm">span: tool retrieve_policy — args {topic: inspection}, 4 chunks, 0.3s</text>
<rect x="40" y="112" width="560" height="24" rx="4" class="d-box"/>
<text x="54" y="129" class="d-label-sm">span: turn 2 — model call, 4,100 tok, 3.8s</text>
<rect x="68" y="142" width="510" height="24" rx="4" class="d-box-warn"/>
<text x="82" y="159" class="d-label-sm">span: tool update_record — DENIED by approval gate, awaiting human</text>
<rect x="40" y="174" width="560" height="24" rx="4" class="d-box-good"/>
<text x="54" y="191" class="d-label-sm">span: turn 3 — model call, 6,200 tok, 4.4s → no tool requested, completed</text>
<text x="12" y="222" class="d-label-sm">One identifier ties it together, so "the answer on Tuesday was wrong" resolves to exactly this tree.</text>
</svg>'''),

    ("terms", [
      ("The manifest", "Once per trace", "Model and version, prompt version, tool set, every budget, verification state, config hash. Without it a trace from six weeks ago cannot be interpreted."),
      ("Every model call", "Request and response", "Including the reasoning where the provider exposes it. A harness that records only final answers cannot tell you why a run went wrong."),
      ("Every tool call", "Arguments and result", "Truncated for storage, but present. This is where an injected instruction would be visible, and nowhere else."),
      ("Termination reason", "Named, not inferred", "Completed, turn cap, spend cap, timeout, error, denied. The operating lesson's requirement, and the single most useful field."),
      ("Cost and latency", "Per span and per trace", "Both drift upward silently as prompts and tool sets grow."),
    ]),

    ("know",
     "You cannot reproduce an agent run, so the trace is not a convenience — it is the evidence.",
     "Sampling, retrieval order, external state and a floating model alias all move between runs. Re-running a failure gives you a different failure. Whatever was not recorded did not happen as far as any later investigation is concerned.",
     "A customer reports a wrong answer from three weeks ago. Re-running the same question now produces a correct one, because the corpus has since been updated. Without the trace there is nothing to investigate — you cannot tell whether the system was broken, the corpus was wrong, or the model changed underneath you."),

    ("h2", "Logs, metrics and traces are three different things"),
    ("terms", [
      ("Logs", "What happened, in prose", "Good for the unexpected. Terrible for answering \"how often\" or \"how slow\"."),
      ("Metrics", "Aggregates over time", "Good for \"is it getting worse\". Useless for \"why did this one fail\"."),
      ("Traces", "One run in full", "Good for \"what happened to this request\". Expensive to keep for everything."),
    ]),
    ("callout", "matters", "Sample traces, keep all failures", "Full traces on every run gets expensive fast on a system with any volume. The usual compromise is a low sample rate for successes and one hundred percent for anything that errored, hit a cap, was denied at a gate, or was overridden by a human. Those are the runs you will want, and they are a small fraction of the total."),

    ("h2", "Instrumenting an agent specifically"),
    ("p", "General application tracing misses the things that matter here. Add these deliberately:"),
    ("ul", [
      "<strong>The prompt, versioned.</strong> Not \"a prompt was used\" — which one, by hash or version. Prompts change more often than code and are rarely in the trace.",
      "<strong>The retrieved chunk ids.</strong> Not the text, the identifiers. When an answer is wrong, the first question is what was retrieved, and this makes it a lookup rather than an investigation.",
      "<strong>Guard and gate firings.</strong> Every budget, nudge, clamp and approval, whether it fired or not. This is the confounds lesson made operational — a limit that ends a run and does not appear in the trace is indistinguishable from the model failing.",
      "<strong>What each summarisation dropped.</strong> In a multi-agent or compacting system, the seams are where findings vanish, and nothing records them by default.",
      "<strong>Human interventions.</strong> Overridden, corrected, abandoned, approved. The most honest quality signal you have, and it only exists if you record it.",
    ]),

    ("know",
     "Instrument every guard, including the ones that did not fire.",
     "A guard that silently terminates a run is indistinguishable from a model that gave up. Recording only the firings is not enough either — you need to know the effective value of every limit, after all the code that can modify it has run, or a null result is ambiguous between the treatment failing and the treatment never happening.",
     "Nine runs are attributed to model capability. They were ended by six different mechanisms — a read budget, a phase clamp, a decomposition reassignment, a wall clock, a routing bug, and a config default that disabled verification. None appeared in the output. A run manifest naming every effective limit would have resolved it on run one."),

    ("h2", "Making it useful, not just present"),
    ("ul", [
      "<strong>One identifier, end to end.</strong> Propagate it into sub-agents and tool calls, or you have several disconnected trees and no way to relate them.",
      "<strong>Structured attributes, not prose.</strong> <code>tokens_in=1900</code> is queryable; \"used about 1900 tokens\" is not.",
      "<strong>Redact at the boundary.</strong> Traces contain user input and tool arguments, which means they contain personal data. Decide what is scrubbed before you turn recording on, not after.",
      "<strong>Read three traces a week.</strong> Whole ones, chosen at random. Aggregates hide the failures worth finding, and nothing substitutes for reading what actually happened.",
    ]),
    ("callout", "pitfall", "Telemetry you never read is a storage bill", "The failure mode here is not under-instrumentation, it is instrumenting thoroughly and then only ever looking at the dashboard. The dashboard shows you the shape of what you already thought to measure. The individual traces are where you find the thing you did not."),

    ("links", [
      ("OpenTelemetry — traces", "https://opentelemetry.io/docs/concepts/signals/traces/",
       "Traces, spans and attributes, and why the model is worth adopting even without a vendor."),
      ("Effective harnesses for long-running agents", "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents",
       "The operational surface a long-running agent creates, and what has to be visible in it."),
    ]),

    ("books", [
      ("LLMOps", "on your shelf",
       "The monitoring and observability chapters cover exporting this to a platform, and the cost trade-offs of sampling."),
    ]),

    ("quiz", [
      ("Why is a trace the only evidence an agent run happened as you think?",
       ["Because logs are usually deleted after 30 days",
        "Because agent runs cannot be reproduced — sampling, retrieval and external state all move, so re-running gives a different failure",
        "Because model providers do not retain request history"], 1),
      ("Why record guards that did not fire, not just the ones that did?",
       ["To measure how often each guard is close to firing",
        "Because a null result is otherwise ambiguous between the treatment failing and the treatment never having engaged",
        "Because unfired guards indicate dead configuration"], 1),
      ("What is the usual sampling compromise for traces?",
       ["Sample uniformly at a rate the budget allows",
        "A low rate for successes, and everything for runs that errored, hit a cap, were denied or were overridden",
        "Full traces for the first month, then metrics only"], 1),
      ("What does a dashboard fail to show you?",
       ["Aggregate trends over time",
        "The failures you did not think to measure — those are found by reading individual traces",
        "Latency percentiles"], 1),
    ]),
  ],
},
{
  "slug": "loop-tradeoffs",
  "title": "Four Levers, and What Each Costs",
  "subtitle": "Prefix caching, read accumulation, per-edit verification and reasoning effort — every one trades tokens against reliability.",
  "body": [
    ("p", "The loop works. Now you have four dials, and turning any of them costs something. They are worth taking together because they share a shape: <strong>each trades tokens and latency against reliability</strong>, and the right setting depends entirely on where your failures actually are — which you only know from the trace."),

    ("figure", "Four levers on the same axis. Nothing here is free, and the correct position for each is a property of your failure distribution rather than a best practice.", '''<svg viewBox="0 0 640 230" role="img" aria-label="Four loop levers and their tradeoffs">
<text x="12" y="18" class="d-accent">LEVER</text><text x="250" y="18" class="d-fill-green" font-size="12" font-weight="600">BUYS</text><text x="452" y="18" class="d-fill-red" font-size="12" font-weight="600">COSTS</text>
<line x1="12" y1="26" x2="628" y2="26" stroke="var(--border)"/>
<rect x="12" y="36" width="220" height="40" rx="4" class="d-box"/>
<text x="26" y="52" class="d-label-b">Prefix caching</text>
<text x="26" y="68" class="d-label-sm">reuse the processed prefix</text>
<text x="250" y="60" class="d-label-sm">most of prefill, free</text>
<text x="452" y="52" class="d-label-sm">rigid prompt order,</text>
<text x="452" y="68" class="d-label-sm">silent invalidation</text>
<rect x="12" y="84" width="220" height="40" rx="4" class="d-box"/>
<text x="26" y="100" class="d-label-b">Read accumulation</text>
<text x="26" y="116" class="d-label-sm">keep every tool result</text>
<text x="250" y="108" class="d-label-sm">full fidelity, revisitable</text>
<text x="452" y="100" class="d-label-sm">quadratic cost,</text>
<text x="452" y="116" class="d-label-sm">attention diluted</text>
<rect x="12" y="132" width="220" height="40" rx="4" class="d-box"/>
<text x="26" y="148" class="d-label-b">Per-edit verification</text>
<text x="26" y="164" class="d-label-sm">check after every change</text>
<text x="250" y="148" class="d-label-sm">fast failure, precise</text>
<text x="250" y="164" class="d-label-sm">attribution</text>
<text x="452" y="148" class="d-label-sm">latency per edit,</text>
<text x="452" y="164" class="d-label-sm">blocks valid interim states</text>
<rect x="12" y="180" width="220" height="40" rx="4" class="d-box"/>
<text x="26" y="196" class="d-label-b">Reasoning effort</text>
<text x="26" y="212" class="d-label-sm">let it think first</text>
<text x="250" y="204" class="d-label-sm">accuracy on multi-step</text>
<text x="452" y="196" class="d-label-sm">tokens billed unseen,</text>
<text x="452" y="212" class="d-label-sm">nothing on recall tasks</text>
</svg>'''),

    ("h2", "1 · Prefix caching"),
    ("p", "The provider keeps the processed keys and values for an unchanged prefix instead of recomputing them. On a hit you pay for new tokens only, which on a multi-turn loop is most of the work eliminated."),
    ("terms", [
      ("What it buys", "Prefill, mostly gone", "On a long system prompt plus a tool set plus a growing transcript, this is the single largest latency and cost lever available in an agent loop."),
      ("What it costs — ordering", "The prompt becomes rigid", "Stable content must come first and stay byte-identical. Adding a timestamp, reordering tools, or interpolating a session id near the front sets your hit rate to zero."),
      ("What it costs — pricing", "Writes cost more than reads save, once", "Caching a prefix used twice is roughly break-even. Used fifty times it is a large win. Below a few reuses it is a small loss."),
      ("What it costs — silence", "Nothing errors on a miss", "Hit rate is a metric you have to look at. A cache that stopped working looks exactly like a system that never had one, except on the bill."),
    ]),
    ("callout", "matters", "Instrument the hit rate or you do not have caching", "The failure mode is not a broken cache, it is a cache that quietly stopped matching after someone added a line to the system prompt. Record cached-token counts per call and alert on the ratio. Without that number you are hoping, and hoping is expensive at three times the cost per turn."),

    ("h2", "2 · Read accumulation, and the growing context"),
    ("p", "An agent reads a file, then another, then searches, then reads again. By default every one of those results stays in the transcript and is re-sent on every subsequent turn. That is the default because it is simple and because the model can revisit anything — and it is also why turn twenty costs twenty times turn one."),
    ("terms", [
      ("Keep everything", "Maximum fidelity", "The model can go back to any detail. Simple to implement. Cost grows with the square of the run, and attention thins across material that is mostly already used."),
      ("Truncate on ingest", "Cheapest intervention", "Cap each tool result. One line of code, and it caps the worst case — a 3,000-line file read at turn four otherwise dominates the window for the rest of the run."),
      ("Summarise as you go", "Middle ground", "Replace a read with a short statement of what was learned. Preserves the finding, drops the bulk. Lossy in a way the agent cannot see, which is the compaction problem."),
      ("Drop after use", "Most aggressive", "Once an edit is made from a read, the read itself is rarely needed verbatim. Clearing old tool results is the safest form of compaction and the most under-used."),
    ]),

    ("know",
     "A single large read early in a run taxes every turn after it.",
     "Tool results are context, and context is re-sent whole on every turn. A file read at turn four is paid for again at turns five through twenty, at growing prefill cost, while crowding out the material the model actually needs now.",
     "An agent reads a 3,000-line file at turn four of a twenty-turn run. That one read is re-sent sixteen more times. It is not the read that costs, it is the sixteen re-sends — and truncating the result to the relevant 200 lines would have removed almost all of it."),

    ("h2", "3 · Per-edit verification"),
    ("p", "Run the check after every change, rather than once at the end. The granularity question, and it has a sharper tradeoff than it first appears."),
    ("terms", [
      ("Verify at the end", "Cheapest", "One check per run. When it fails you know the run failed and not which of nine edits caused it."),
      ("Verify per edit", "Precise attribution", "The failing edit is named immediately, and the agent gets feedback while the context that produced it is still present. This is the strongest form of verifier-guided looping."),
      ("Verify per logical unit", "The usual compromise", "After a coherent group of edits rather than each one. Keeps most of the attribution and pays a fraction of the cost."),
    ]),
    ("callout", "pitfall", "Per-edit verification blocks legitimate intermediate states", "A refactor that renames a function across four files does not compile after the first edit, and per-edit checking will report a failure that is not one. The agent then tries to fix a break that its own next edit was about to resolve, and can spin. Where changes are genuinely atomic across files, verify per unit rather than per edit — and make sure the agent can tell the difference."),

    ("know",
     "Verification granularity decides whether feedback names the cause or only the symptom.",
     "A check at the end tells you the run failed. A check after each change tells you which change did it, while the reasoning that produced it is still in context and can be corrected. The cost is real, and so is the difference between debuggable and not.",
     "Nine edits, one broken build, one check at the end. The agent sees a failure with no attribution, guesses, and reverts the wrong edit — because from inside the loop every one of the nine is equally suspect. Per-unit checking would have named the third."),

    ("h2", "4 · Reasoning effort"),
    ("p", "Covered in its own lesson, so only the tradeoff here. Extra reasoning tokens buy accuracy on genuinely multi-step problems and buy nothing on recall, extraction, classification or formatting. They are billed whether or not you see them, so cost tracks problem difficulty rather than visible output length."),
    ("callout", "insight", "This is a routing decision, not a setting", "The mistake is picking one reasoning level for the whole system. Most turns in an agent loop are mechanical — read this, call that, format the result — and pay for reasoning they cannot use. Route by turn shape: high effort where the model must plan or diagnose, low or none where it is executing a decision already made."),

    ("h2", "Setting them, in order"),
    ("p", "There is a sequence that avoids wasted work, and it starts where it always starts:"),
    ("terms", [
      ("First, read the trace", "Where do runs actually fail?", "Turn cap, wrong tool, broken edit, or cost? Each points at a different lever, and tuning the wrong one measures flat."),
      ("Then truncate reads", "Cheapest real win", "One line, no downside worth the name, and it caps the worst case immediately."),
      ("Then order the prompt for caching", "Free once, then permanent", "Stable content first, variable last, and instrument the hit rate."),
      ("Then set verification granularity", "Match it to your change shape", "Per edit for independent changes, per unit where changes are atomic across files."),
      ("Last, tune reasoning effort", "By turn type, not globally", "And only after the above, because a cheaper loop makes higher effort affordable where it helps."),
    ]),
    ("callout", "matters", "Change one lever at a time and re-run the whole battery", "These interact. Truncating reads improves cache hit rates by stabilising the prompt. Per-edit verification adds turns, which makes read accumulation worse. Adjust two at once and the result tells you something moved, not what — which is the measurement checklist arriving in a place people forget to apply it."),

    ("links", [
      ("Prompt caching", "https://docs.claude.com/en/docs/build-with-claude/prompt-caching",
       "The mechanics, the pricing asymmetry between writes and reads, and exactly what invalidates a prefix."),
      ("Effective context engineering for AI agents", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents",
       "Compaction and tool-result clearing, which is lever two done properly."),
      ("Building effective agents — Anthropic", "https://www.anthropic.com/engineering/building-effective-agents",
       "The case for the simplest loop that works, before any of these are worth tuning."),
    ]),

    ("quiz", [
      ("Your cache hit rate silently dropped to zero last week. What most likely happened?",
       ["The provider expired the cache",
        "Something variable was added near the front of the prompt, and the prefix stopped matching",
        "The conversation grew past the cache size limit"], 1),
      ("An agent reads a 3,000-line file at turn four of a twenty-turn run. What is the real cost?",
       ["The one large prefill on turn four",
        "The sixteen re-sends afterwards, at growing prefill cost, crowding out what the model needs now",
        "The time taken to read the file from disk"], 1),
      ("A refactor renames a function across four files. Why can per-edit verification hurt?",
       ["Verification is too slow to run four times",
        "The code does not compile after the first edit, so the check reports a failure the next edit was about to resolve",
        "The agent cannot see verification results mid-run"], 1),
      ("Which lever should you tune last?",
       ["Prefix caching, because pricing changes often",
        "Reasoning effort — a cheaper loop first makes higher effort affordable where it actually helps",
        "Read truncation, since it risks losing information"], 1),
    ]),
  ],
},
]
