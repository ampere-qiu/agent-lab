# 12 · Completion checks { #week-3-completion }

This week ends after function/class tools. Show your saved files and the actual terminal output. This site does not store progress or issue certificates.

## Files and practical evidence { #required-evidence }

All your new files should be inside `First_agent_template`, beside `app.py` and the supplied `week03_common.py`.

| File | What to show |
| --- | --- |
| `my_playlist.py` | A web-search call, returned snippets/URLs, and an answer using them. Record any service failure honestly. |
| `my_menu.py` | A `suggest_menu` call and the returned menu. |
| `my_tool_calling.py` | A structured `web_search` call, its returned results, and an answer using them; compare the action format with `my_playlist.py`. |
| `my_timing.py` | Generated `datetime` code, the PC's start time, 180-minute duration, and finish time. |
| `my_tool_check.py` | `PASS: menu, catering, theme, and unknown-category checks.` without a model call. |
| `my_catering.py` | A catering-tool call, its returned service name, and the final answer. |
| `my_theme.py` | A party-theme-tool call, its stored description, and the final answer. |
| Your change in `week03_tools.py` | A changed service/category reflected in direct-test and agent results. |

The direct test expects the supplied catering winner until you change its assertion to match your new service. Save edits before rerunning a program.

If you open a fresh terminal, use the [Windows or Mac activation steps](week-3-learning-plan.md#activate-environment) before running your file again. The result appears in that terminal, not in the Week 2 browser chat.

## Explain the ideas { #explain-concepts }

Explain each point in one or two sentences:

- Which part runs on Groq, and which parts run on your PC?
- What does CodeAgent coordinate?
- How are Python actions different from structured tool calls?
- What do the tool's name, description, inputs, and output type tell the model?
- How does a decorated function differ from a `Tool` class with `forward(...)`?
- Which party values are fictional Python data, and which results come from web search?
- How do you verify that a tool really ran?

Retrieval, knowledge bases, agent teams, and vision/browser work continue on the [Week 04 page](week-4-preview.md).

## Quiz and credits { #optional-hf }

[HF Quick Quiz 1](https://huggingface.co/learn/agents-course/en/unit2/smolagents/quiz1) is optional. The later quizzes include topics beyond this week's class.

Lesson concepts and examples are adapted from the [Hugging Face Agents Course, Unit 2.1](https://huggingface.co/learn/agents-course/en/unit2/smolagents/introduction).

**Review:** [Week 03 plan](week-3-learning-plan.md) · **Next:** [Week 04 · Coming next](week-4-preview.md).
