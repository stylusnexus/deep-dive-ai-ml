TITLE = "Closing · The Future of Work"
TOPIC = "closing-future-of-work"
ICON = "🔭"
DESCRIPTION = "The only chapter here that argues rather than instructs. What the labour evidence actually shows in 2026, and a thesis about which capability becomes scarce — offered as an argument, with its counter-argument attached."
TAGS = ["ai", "work", "essay"]
COLOR = "slate"
CREATED = "2026-09-02"
ID_BASE = "1788300000"

LESSONS = [
{
  "slug": "what-the-evidence-shows",
  "title": "What the Evidence Actually Shows",
  "subtitle": "Before anyone's thesis, including mine: the measured numbers, and how much weight they hold.",
  "body": [
    ("p", "This closing chapter is different in kind from everything before it. The rest of this course teaches things that can be checked, and it has been unusually strict about that — numbers come from runs, claims get verified before they are written down, and several lessons exist because a check failed. A chapter about the future of work cannot meet that standard, because the future has not happened. What it can do is separate the part that is measured from the part that is argued, and label them."),

    ("p", "This lesson is the measured part. The next is the argument."),

    ("h2", "The aggregate has not moved. The composition has."),
    ("p", "The single most important thing in the current evidence is that these two statements are both true, and most commentary picks one and ignores the other."),

    ("terms", [
      ("No aggregate employment effect", "National studies, Denmark and the United States",
       "Two national-level studies find no discernible relationship between AI exposure or adoption and changes in overall employment. If your expectation was mass displacement visible in the headline numbers, it has not arrived."),
      ("A sharp compositional effect", "Concentrated on the junior end",
       "Firms adopting generative AI reduce junior employment by around 9% relative to non-adopters, with senior employment unaffected. In highly exposed occupations a 16% relative decline in early-career employment has been documented, again with no corresponding effect on senior roles."),
      ("Visible in graduate outcomes", "Unemployment for new graduates at 5.6% in early 2026",
       "Up 1.6 percentage points on three years earlier. Somewhat over a quarter of employers report that AI has reduced the need for tasks entry-level workers used to do."),
      ("Slowed hiring rather than firing", "The United Kingdom pattern",
       "Firms with high AI exposure have slowed new hiring, particularly for junior positions. That is a different mechanism from redundancy and it is much harder to see, because nothing happens — a role simply is not opened."),
    ]),

    ("know",
     "A stable total with a shifting composition is the finding, and it is more interesting than either half.",
     "&ldquo;AI is destroying jobs&rdquo; is not supported by the aggregate data. &ldquo;Nothing is happening&rdquo; is not supported by the junior-versus-senior split. The evidence describes a labour market of roughly constant size whose entry point is narrowing, and that is a structurally different situation from a shrinking one — with different consequences, on a different timescale, for different people.",
     "This is the same reading discipline the evaluation block teaches. An aggregate that has not moved does not mean nothing changed; it means nothing changed <em>on average</em>, and the average is the statistic least able to show you a redistribution."),

    ("figure", "The two halves of the finding. Read the left bar alone and nothing is happening; read the right one alone and the sky is falling. The evidence says both, and they are not in conflict.", '''<svg viewBox="0 0 640 210" role="img" aria-label="Stable aggregate employment against a shifting composition"><rect x="14" y="24" width="290" height="150" rx="8" class="d-box"/>
<text x="28" y="48" class="d-label-b">aggregate employment</text>
<rect x="28" y="66" width="240" height="30" rx="4" class="d-box"/><text x="40" y="86" class="d-label-sm">before</text>
<rect x="28" y="104" width="240" height="30" rx="4" class="d-box"/><text x="40" y="124" class="d-label-sm">after — no discernible change</text>
<text x="28" y="158" class="d-label-sm">two national studies, no relationship</text>
<rect x="336" y="24" width="290" height="150" rx="8" class="d-box-accent"/>
<text x="350" y="48" class="d-label-b">who holds the jobs</text>
<rect x="350" y="66" width="240" height="30" rx="4" class="d-box"/><text x="362" y="86" class="d-label-sm">senior — unaffected</text>
<rect x="350" y="104" width="150" height="30" rx="4" class="d-box-accent"/><text x="362" y="124" class="d-label-sm">junior — down 9-16%</text>
<text x="350" y="158" class="d-label-sm">relative to non-adopting firms</text>
<text x="14" y="198" class="d-label-sm">A constant total with a narrowing entry point is not a smaller labour market. It is a different one.</text>
</svg>'''),

    ("h2", "Productivity: real, modest, and very unevenly distributed"),
    ("terms", [
      ("The headline figure", "Around 0.6% in 2025, with roughly 1.8% expected in 2026",
       "Real and positive, and a long way from the transformation implied by the surrounding discourse. Treat a forecast as a forecast."),
      ("Concentrated by sector", "Over 2% in high-skill services and finance",
       "Against roughly 0.4% in low-skill services, manufacturing and construction. Where the work is already language and analysis, the gains are several times larger."),
      ("Largest for the least experienced", "Up to 36% in field experiments",
       "Gains were greatest for the lowest-skilled workers and minimal for the most experienced. The technology compresses the distribution rather than lifting it uniformly."),
      ("And negative past the frontier", "19 percentage points less accurate",
       "On tasks outside the model's capability, people using AI were substantially <em>less</em> likely to be accurate than people without it. The tool does not fail quietly at its boundary; it fails confidently, and takes the user with it."),
    ]),

    ("callout", "pitfall", "Firms report more gain than their own revenue shows",
     "<p>A consistent finding is that firms report larger productivity gains from AI than their contemporaneous revenue and employment changes imply. The generous reading is a timing lag — output and quality improvements arriving later than the adoption. The ungenerous reading is that self-reported gains from a technology everyone is invested in believing in are exactly the measurement this course would tell you not to trust. Both readings are live, and the data does not yet separate them.</p>"),

    ("h2", "How much weight this evidence holds"),
    ("p", "Not as much as its precision suggests, and the statistics lesson in the evaluation block is the reason. Many of these figures are single studies of an early deployment, measuring an unstable target during a period of rapid change. A relative decline of 9% and one of 16% are not necessarily in conflict — they are different populations, methods and windows. Treat them as a direction with wide error bars rather than as constants."),

    ("callout", "matters", "Adoption is concentrated where the advantages already were",
     "<p>Adoption is heaviest among large, already-productive firms, and the complementary assets turn out to matter enormously — skilled staff, organisational process, data infrastructure. This is the least surprising and most consequential finding in the set: a technology that multiplies existing capability widens the gap between organisations that had it and those that did not, and the same logic applies to individuals.</p>"),

    ("quiz", [
      ("What do national-level studies find about AI's effect on overall employment?",
       ["A measurable decline concentrated in the last two years",
        "No discernible relationship — the aggregate has not moved, while the composition has shifted sharply against junior roles",
        "An increase, driven by new AI-related job categories"],
       1),
      ("What happened to accuracy on tasks outside the model's capability?",
       ["It was unchanged, since users ignored unhelpful output",
        "People using AI were about 19 percentage points less likely to be accurate than people without it",
        "It improved slightly, as the model surfaced relevant considerations"],
       1),
      ("Why should the firm-reported productivity gains be treated cautiously?",
       ["Firms have no way to measure productivity accurately",
        "They exceed what those firms' own revenue and employment changes imply, and self-reported gains from a technology everyone is invested in believing in are a weak measurement",
        "The surveys used inconsistent definitions of productivity"],
       1),
    ]),
  ],
},
{
  "slug": "the-apprenticeship-problem",
  "title": "The Apprenticeship Problem",
  "subtitle": "An argument, not a finding: the scarce thing becomes knowing where the boundary is, and we are automating the work that used to teach it.",
  "body": [
    ("p", "Everything below is argument. It is consistent with the evidence in the previous lesson and it is not established by it, and where I think it is weak I have said so at the end rather than left it out. Read it as a position to disagree with, which is what a closing chapter should be."),

    ("h2", "The starting point: a video, and an executive who changed her mind"),
    ("p", "This chapter began with a talk by Clara Shih, formerly of Salesforce and Meta, on how AI could radically change white-collar work. Her account of the turn is specific: she watched AI agents match and in places beat her strongest people across a set of tasks, and describes feeling radicalised in the moment of seeing it work. She left to build a nonprofit aimed at helping young people find work before entry-level roles disappear, on the reasoning that the only way for people to keep pace with AI is to give them AI."),

    ("p", "I think the observation is right and the remedy is incomplete, and the gap between those two is where this chapter lives."),

    ("h2", "The shape of the change"),
    ("p", "Put the two strongest findings from the previous lesson next to each other. Within the model's competence, the largest gains go to the <em>least</em> experienced — up to 36% in field experiments, minimal for the most experienced. Outside its competence, people using it were about 19 percentage points less accurate than people without it."),

    ("p", "Read together those say something sharper than either alone. The technology compresses the skill distribution inside its frontier and steepens the penalty outside it. If that holds, the capability that becomes scarce is not the ability to produce the work — that is what got compressed — but the ability to tell which side of the boundary you are standing on."),

    ("know",
     "The scarce skill is knowing where the model stops being reliable, and it is the hardest thing to teach without experience.",
     "Recognising that an answer is confidently wrong requires knowing what a right answer looks like in that domain, and that recognition is built by having been wrong and corrected, repeatedly, on work that mattered enough for someone to check. It is not transferable by instruction. This entire course is an attempt to transfer some of it and the honest assessment is that lessons can only get a reader to the point where their own mistakes start teaching them faster.",
     "It is also exactly the judgement the evidence says is not being compressed — the experienced gained least from the tool, because what they were bringing was not production."),

    ("h2", "Why the junior end is not just the cheap end"),
    ("p", "Junior work has always been two things at once, and organisations bought it for the first and got the second thrown in. It is output, produced more slowly and less well than a senior would. It is also the apprenticeship — the mechanism by which someone acquires the judgement that makes them senior, through doing work slightly beyond them and having it corrected."),

    ("p", "Automating that work removes the first function and, incidentally, the second. Nobody decides to stop training people; the training was a by-product of an economic arrangement, and the arrangement changed. Meanwhile the demand for senior judgement rises, because somebody has to review output that arrives faster than before and carries no reasoning with it — which is the problem the engineering-practice block calls code nobody decided."),

    ("figure", "The loop on the left is how judgement was produced. The one on the right removes the step in the middle. Both ends still need seniors, and only one of them makes any.", '''<svg viewBox="0 0 640 220" role="img" aria-label="The apprenticeship loop, before and after"><defs><marker id="ap" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" class="d-fill-accent"/></marker></defs>
<text x="14" y="20" class="d-label-b">how judgement was made</text>
<rect x="14" y="30" width="122" height="38" rx="6" class="d-box"/><text x="26" y="54" class="d-label-sm">junior does it</text>
<path d="M136 49 L166 49" class="d-arrow-accent" marker-end="url(#ap)"/>
<rect x="166" y="30" width="122" height="38" rx="6" class="d-box"/><text x="178" y="54" class="d-label-sm">senior corrects</text>
<path d="M227 68 L227 96" class="d-arrow-accent" marker-end="url(#ap)"/>
<rect x="120" y="96" width="168" height="38" rx="6" class="d-box-accent"/><text x="132" y="120" class="d-label-sm">junior becomes senior</text>
<path d="M120 115 L60 115 L60 72" class="d-arrow-accent" marker-end="url(#ap)"/>
<text x="346" y="20" class="d-label-b">how it is made now</text>
<rect x="346" y="30" width="122" height="38" rx="6" class="d-box"/><text x="358" y="54" class="d-label-sm">model does it</text>
<path d="M468 49 L498 49" class="d-arrow-accent" marker-end="url(#ap)"/>
<rect x="498" y="30" width="128" height="38" rx="6" class="d-box"/><text x="510" y="54" class="d-label-sm">senior reviews</text>
<rect x="452" y="96" width="174" height="38" rx="6" class="d-box"/><text x="464" y="120" class="d-label-sm">no junior in the loop</text>
<text x="346" y="164" class="d-label-sm">demand for senior review rises;</text>
<text x="346" y="182" class="d-label-sm">the supply of new seniors does not.</text>
<text x="14" y="164" class="d-label-sm">The apprenticeship was never</text>
<text x="14" y="182" class="d-label-sm">a policy. It was a by-product.</text>
</svg>'''),

    ("h2", "Why giving people the tools is necessary and not sufficient"),
    ("p", "Shih's remedy — put AI in the hands of the people being displaced — is clearly right as far as it goes, and the evidence supports it: the largest measured gains went to the least experienced. Someone entering work without these tools is at a straightforward disadvantage."),

    ("p", "But what the junior loses is not access. It is the corrected-mistake loop. A person handed a capable tool and no one to tell them when its output is wrong learns to produce faster, not to judge better — and the 19-point accuracy penalty says that is precisely the failure mode past the frontier. Tools raise the floor of output. They do not by themselves build the thing that was being built accidentally, and I have not seen a convincing account of what replaces it."),

    ("callout", "insight", "The most valuable thing an organisation can do is probably unfashionable",
     "<p>If this argument holds, the highest-leverage move available to an employer is to keep hiring juniors and deliberately spend senior time correcting them, while accepting that the same output could be produced faster another way. That is a cost with no visible return in the quarter it is paid, which is precisely why it will not happen by default and why the shortfall shows up years later as an absence nobody can attribute.</p>"),

    ("h2", "The case against everything I have just said"),
    ("p", "This argument has been made before, repeatedly, and it was wrong. Compilers were going to end programming and produced more programmers. Spreadsheets were going to end accounting; the accounting profession grew. Computer-aided design did not empty drawing offices. In each case the apprenticeship did not vanish, it reformed around the new tool, and the people predicting otherwise were reasoning exactly as I have — from the tasks being automated to the skills that would no longer be learned."),

    ("terms", [
      ("The historical prior is against me", "And it is a strong prior",
       "Every previous automation of a professional task produced a new layer of work above it, and the entry point moved rather than closing. There is no reason to be confident this is the exception, and considerable reason for humility about it."),
      ("The evidence is thin and early", "Single studies, unstable target",
       "A 9% relative decline in one dataset and 16% in another are a direction, not a law, measured during a period of rapid change. This course's own statistics lesson says what to do with a handful of studies at small effect sizes, and it does not say build a worldview on them."),
      ("The mechanism may be right and the magnitude wrong", "The most likely outcome",
       "It is entirely possible that the apprenticeship is genuinely disrupted, reforms within a decade around reviewing and directing rather than producing, and the disruption is a rough transition rather than a structural break. That would make this chapter partly right in a way that is not very useful."),
    ]),

    ("h2", "What follows for someone who has read this far"),
    ("p", "This course has an implicit answer to the question and it is worth making explicit, because it shaped what was taught. Almost nothing here was about producing output faster. It was about knowing what to measure, noticing when a measurement is lying, telling a real difference from a wobble, checking whether the model was needed at all, and recognising the failures that arrive looking like successes."),

    ("p", "That was a bet: that the durable skill is judgement about systems rather than fluency at producing them, and that judgement is built by being wrong on purpose in cheap places. Every fixture that failed before the work, every baseline written down before the run, every measurement that turned out to be measuring the instrument — those were rehearsals for being wrong somewhere expensive. If the argument in this chapter is right, that is the correct bet. If the historical prior is right, it is still not a bad one."),

    ("callout", "matters", "Be wrong on purpose, in cheap places, on a schedule",
     "<p>If the corrected-mistake loop is no longer supplied by the job, it has to be arranged deliberately. Build the thing before reading how. Predict the number before running the eval. Write down what you expect and check. This course is full of moments where a check disagreed with a confident expectation, and every one of those was worth more than a lesson that went smoothly — which is the whole argument in miniature.</p>"),

    ("quiz", [
      ("What does the chapter argue becomes the scarce capability?",
       ["The ability to produce work quickly with AI assistance",
        "Knowing where the model stops being reliable — since capability is compressed inside its frontier and penalised outside it",
        "Familiarity with the widest range of available tools"],
       1),
      ("Why is junior work described as two things at once?",
       ["It is both technical and administrative",
        "It is output, and it is also the apprenticeship — the mechanism by which judgement is built, which organisations got as a by-product rather than bought deliberately",
        "It serves both the individual's career and the team's capacity"],
       1),
      ("What is the strongest argument against this chapter's thesis?",
       ["Productivity gains from AI are smaller than reported",
        "Every previous automation of professional work produced this same prediction, and each time the apprenticeship reformed around the tool rather than disappearing",
        "Junior employment declines are concentrated in a few sectors"],
       1),
    ]),
  ],
},
]
