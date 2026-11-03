"""Small smolagents adapter for the maintained DDGS search client."""
from ddgs import DDGS
from smolagents.tools import Tool


class WebSearchTool(Tool):
    name = "web_search"
    description = (
        "Search the web through DuckDuckGo. Returns titles, URLs, and search snippets, "
        "not full page contents. Use this to find sources, then cite returned URLs."
    )
    inputs = {"query": {"type": "string", "description": "The search query."}}
    output_type = "string"

    def __init__(self, max_results: int = 3):
        super().__init__()
        self.max_results = max_results

    def forward(self, query: str) -> str:
        results = DDGS(timeout=15).text(
            query, max_results=self.max_results, backend="duckduckgo"
        )
        if not results:
            raise RuntimeError("No search results returned. Try a shorter query or retry later.")
        entries = [
            f"[{item['title']}]({item['href']})\n{item['body']}"
            for item in results[:self.max_results]
        ]
        return "## Search Results\n\n" + "\n\n".join(entries)
