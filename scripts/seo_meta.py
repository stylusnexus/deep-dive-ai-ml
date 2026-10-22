"""Search and AI-answer metadata shared by every generated page.

One place for the site URL and the <head> tags, so the landing page, the
lessons and the sitemap cannot disagree about a canonical address.
"""
import html, json, re

SITE = "https://stylusnexus.github.io/deep-dive-ai-ml/"
NAME = "Building and Measuring LLM Systems"
ORG = {"@type": "Organization", "name": "Stylus Nexus", "url": "https://github.com/stylusnexus"}
OG_IMAGE = "og.png"          # 1200x630, built by the landing-page work

E = html.escape


def plain(text, limit=158):
    """Strip tags and trim to a meta-description length at a word boundary."""
    t = re.sub(r"<[^>]+>", "", text)
    t = html.unescape(re.sub(r"\s+", " ", t)).strip()
    if len(t) <= limit:
        return t
    cut = t[:limit].rsplit(" ", 1)[0].rstrip(",;:- ")
    return cut + "…"


def describe(subtitle, set_title, floor=110, limit=158):
    """Meta description for a lesson: its subtitle, padded with course context when too short to be useful."""
    d = plain(subtitle, limit)
    if len(d) >= floor:
        return d
    d = d if d.endswith((".", "?", "!", "…")) else d + "."
    for tail in (f" A lesson in {set_title} from a free applied LLM course.",
                 f" A lesson in {set_title} from a free LLM course.",
                 f" A lesson in {set_title}.",
                 f" Part of {set_title}."):
        if len(d + tail) <= limit:
            return d + tail
    return d


def course_jsonld(description):
    return {"@context": "https://schema.org", "@type": "Course", "name": NAME,
            "description": description, "url": SITE, "inLanguage": "en",
            "isAccessibleForFree": True, "provider": ORG,
            "educationalLevel": "Intermediate", "teaches": [
                "LLM evaluation", "retrieval-augmented generation", "agentic AI",
                "LLM security", "model quantization and fine-tuning", "classical machine learning"]}


def lesson_jsonld(title, description, path, set_title):
    return {"@context": "https://schema.org", "@type": "LearningResource",
            "name": title, "description": description, "url": SITE + path,
            "inLanguage": "en", "isAccessibleForFree": True,
            "learningResourceType": "lesson", "publisher": ORG,
            "isPartOf": {"@type": "Course", "name": NAME, "url": SITE},
            "about": set_title}


def head_meta(title, description, path, jsonld=None, og_type="article"):
    """Return the <meta>/<link>/JSON-LD block for a page at `path` (relative to the site root)."""
    url = SITE + path
    d = E(description, quote=True)
    t = E(title, quote=True)
    tags = [
        f'<meta name="description" content="{d}">',
        f'<link rel="canonical" href="{url}">',
        '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="{E(NAME, quote=True)}">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{SITE}{OG_IMAGE}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
        f'<meta name="twitter:image" content="{SITE}{OG_IMAGE}">',
    ]
    if jsonld:
        # "</" inside a script block would end it early; json.dumps can emit it from text.
        body = json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/")
        tags.append(f'<script type="application/ld+json">{body}</script>')
    return "\n".join(tags)
