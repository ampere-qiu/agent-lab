"""Bounded classroom research: short results and per-delegation attempt limits."""
import re
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from ddgs import DDGS
import requests
from smolagents.memory import TaskStep
from smolagents.tools import Tool


def clip(text, limit):
    text = str(text)
    suffix = "\n[Excerpt clipped; this is not the complete source.]"
    return text if len(text) <= limit else text[:limit-len(suffix)] + suffix


class ResearchBudget:
    """Count real attempts, including failed pages, within each fresh agent task."""
    def __init__(self, max_searches=1, max_pages=2):
        self.max_searches = max_searches
        self.max_pages = max_pages
        self.agent = None
        self.task = None
        self.counts = {"search": 0, "page": 0}
        self.seen = set()

    def bind(self, agent):
        self.agent = agent

    def allow(self, kind, key):
        if self.agent is not None:
            task = next((step for step in reversed(self.agent.memory.steps)
                         if isinstance(step, TaskStep)), None)
            if task is not self.task:
                self.task = task
                self.counts = {"search": 0, "page": 0}
                self.seen.clear()
        limit = self.max_searches if kind == "search" else self.max_pages
        if (kind, key) in self.seen:
            return "Already attempted in this task. Do not retry; return evidence or mark it missing."
        if self.counts[kind] >= limit:
            return f"Research limit reached: {limit} {kind} attempt(s). Return evidence or mark missing; stop searching."
        self.counts[kind] += 1
        self.seen.add((kind, key))
        return None


class WebSearchTool(Tool):
    name = "web_search"
    description = "Search for candidate sources. Returns at most 2 short snippets and URLs, not verified page evidence. Respect the task's research limit."
    inputs = {"query": {"type": "string", "description": "One focused search query."}}
    output_type = "string"

    def __init__(self, max_results=2, budget=None):
        super().__init__()
        self.max_results = min(max_results, 2)
        self.budget = budget or ResearchBudget()

    def forward(self, query: str) -> str:
        refusal = self.budget.allow("search", query.strip().casefold())
        if refusal:
            return refusal
        try:
            results = list(DDGS(timeout=12).text(
                query[:240], max_results=self.max_results, backend="duckduckgo"
            ))[:self.max_results]
            entries = []
            for item in results:
                url = str(item.get("href", ""))
                if len(url) > 350:
                    continue
                entries.append(f"[{str(item.get('title', 'Source'))[:90]}]({url})\n"
                               + str(item.get("body", ""))[:220])
            return clip("## Candidate search results\n\n" + "\n\n".join(entries), 1400) if entries else "No usable search results. Mark evidence missing; do not invent a source."
        except Exception:
            return "Search failed. This attempt counts toward the limit. Return available evidence and mark missing work."


class PageExcerptTool(Tool):
    name = "visit_webpage"
    description = "Read a short source excerpt (at most 1600 characters). Optional focus words select relevant paragraphs, e.g. Wayne Manor Batman or latitude longitude. A partial excerpt is not the whole page. Blocked pages count as attempts."
    inputs = {
        "url": {"type": "string", "description": "Source page URL."},
        "focus": {"type": "string", "nullable": True,
                  "description": "Optional words to locate the relevant passage."},
    }
    output_type = "string"

    def __init__(self, budget=None):
        super().__init__()
        self.budget = budget or ResearchBudget()

    def forward(self, url: str, focus: str = "") -> str:
        if urlsplit(url).scheme not in ("http", "https") or len(url) > 350:
            return "Use a normal HTTP(S) source URL of at most 350 characters."
        refusal = self.budget.allow("page", url)
        if refusal:
            return refusal
        try:
            response = requests.get(url, timeout=12)
            response.raise_for_status()
            soup = BeautifulSoup(response.text[:1_000_000], "html.parser")
            content = soup.find("article") or soup.find("main") or soup.body or soup
            for tag in content.find_all(["script", "style", "nav", "header", "footer", "aside", "form"]):
                tag.decompose()
            blocks = [" ".join(tag.get_text(" ", strip=True).split())
                      for tag in content.find_all(["h1", "h2", "h3", "p", "li", "tr"])]
            blocks = list(dict.fromkeys(block for block in blocks if block))
            if not blocks:
                blocks = [" ".join(content.get_text(" ", strip=True).split())]
            terms = set(re.findall(r"[a-z0-9]{3,}", (focus or "").lower()))
            if terms:
                ranked = sorted(enumerate(blocks), key=lambda pair: -sum(
                    term in pair[1].lower() for term in terms))
                matching = [(i, block) for i, block in ranked
                            if any(term in block.lower() for term in terms)][:3]
                if not matching:
                    return f"Source: {url}\nNo matching passage in the extracted text. This does not establish that the full page lacks the fact."
                blocks = [block for _, block in sorted(matching)]
            text = "\n".join(blocks)
            if not text:
                return f"Source: {url}\nNo readable text. Mark this observation incomplete."
            return clip(f"Source: {url}\nPartial page excerpt (check its scope):\n{text}", 1600)
        except requests.HTTPError as error:
            status = error.response.status_code if error.response is not None else "HTTP error"
            return f"Source: {url}\nPage blocked/unavailable ({status}). Attempt counted; do not retry this URL."
        except requests.RequestException:
            return f"Source: {url}\nPage request failed. Attempt counted; do not retry this URL."
