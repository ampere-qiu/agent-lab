# Week 2 — working template and tools { #week-2-working-template-and-tools }

Start after the [Week 1 completion checks](week-1-learning-plan.md#week-1-completion). Suggested time: **3–4 hours**, plus an optional custom-tool extension of 30–60 minutes. Keep your dummy script, Python installation, and Groq key.

## Learning objectives { #learning-objectives }

By the end of Week 2, you can run the chat template end to end, explain how CodeAgent manages the loop, register and test tools, and verify an answer against execution evidence and a returned source.

## What is supplied, and what do you do? { #what-is-supplied }

The download already contains the chat interface, model connection, and implementations of the time and search tools. **Your required task is to test and register those supplied tools, then demonstrate that the agent actually used them.** You do not need to write their function bodies.

“Register” means adding a tool to the `tools=[...]` list in `CodeAgent(...)`, so the agent can use it. A file or import by itself does not register a tool.

| Tool | Supplied in the download | Available to the agent at first startup? | Your task |
| --- | --- | --- | --- |
| `final_answer` | Implemented in `tools/final_answer.py` | Yes | Keep it registered; it returns the final result |
| `get_current_time_in_timezone` | Implemented in `app.py` | No | Test, register, and check its execution |
| `WebSearchTool` (agent name: `web_search`) | Implemented in `tools/web_search.py` and imported in `app.py` | No | Test, register, and verify a returned source |
| `my_custom_tool` | Unfinished placeholder in `app.py` | No | Optional: write your own implementation, then test and register it |
| `get_weather` | Not included in this template | No | No Week 2 task; it belongs to the Week 1 dummy exercise |

The untouched template can respond to a simple question and calculate `12 * 8`. Its supplied web-search tool is unavailable until you register it. A plausible URL or the words “I searched” are not evidence that a search ran.

## Learning sequence { #learning-sequence }

1. [Download and run the template](run-your-first-agent.md) in its own folder and virtual environment (about 45–60 minutes). Verify the answer to `12 * 8`; opening the page alone does not verify the model connection.
2. [Understand the template](understand-the-template.md) with `app.py` open beside the lesson (about 30–45 minutes). Compare its automated loop with your Week 1 dummy script.
3. [Enable and test the supplied tools](first-agent-practical.md) (about 90–120 minutes): test timezone lookup directly, register it, and inspect an agent call; then repeat for web search and verify a returned source.
4. Demonstrate both tools and review [completion checks](quizzes.md#finish-the-practical) (about 15 minutes).
5. Optional: implement, describe, test, and register a custom tool using the [worked example](first-agent-practical.md#6-optional-create-your-own-tool).

## Week 2 completion { #week-2-completion }

Show a successful chat response, direct tests and agent traces for time and search, and a supported source link. Explain where the model runs, which code runs locally, and how errors differ from successful observations. Demonstrate stopping and restarting the app.

Search and Groq limits are independent. If a live checkpoint is unavailable, mark it incomplete and retry later; a link recalled by the model does not substitute for search execution. Image generation, hosting a Space, the account-gated final quiz, and certification are not required.

**Review:** [Course route](course-route.md) · [Completion checks](quizzes.md#finish-the-practical).

**Next:** [Week 03 — smolagents](week-3-learning-plan.md).
