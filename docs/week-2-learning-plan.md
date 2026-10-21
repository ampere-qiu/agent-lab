# Week 2 — working template and tools { #week-2-working-template-and-tools }

Start after the [Week 1 completion checks](week-1-learning-plan.md#week-1-completion). Suggested time: **3–4 hours**, plus an optional custom-tool extension of 30–60 minutes. Keep your dummy script, Python installation, and Groq key.

## Learning objectives { #learning-objectives }

By the end of Week 2, you can run the chat template end to end, explain how CodeAgent manages the loop, register and test tools, and verify an answer against execution evidence and a returned source.

## Learning sequence { #learning-sequence }

1. [Download and run the template](run-your-first-agent.md) in its own folder and virtual environment (about 45–60 minutes). Verify the answer to `12 * 8`; opening the page alone does not verify the model connection.
2. [Understand the template](understand-the-template.md) with `app.py` open beside the lesson (about 30–45 minutes). Compare its automated loop with your Week 1 dummy script.
3. [Build and test tools](first-agent-practical.md) (about 90–120 minutes): test timezone lookup directly, register it, and inspect an agent call; then repeat for web search and verify a returned source.
4. Demonstrate both tools and review [completion checks](quizzes.md#finish-the-practical) (about 15 minutes).
5. Optional: implement, describe, test, and register a custom tool using the [worked example](first-agent-practical.md#6-optional-create-your-own-tool).

## Week 2 completion { #week-2-completion }

Show a successful chat response, direct tests and agent traces for time and search, and a supported source link. Explain where the model runs, which code runs locally, and how errors differ from successful observations. Demonstrate stopping and restarting the app.

Search and Groq limits are independent. If a live checkpoint is unavailable, mark it incomplete and retry later; a link recalled by the model does not substitute for search execution. Image generation, hosting a Space, the account-gated final quiz, and certification are not required.

**Review:** [Course route](course-route.md) · [Completion checks](quizzes.md#finish-the-practical).
