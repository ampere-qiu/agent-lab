# Week 1 — concepts, setup, and a dummy agent { #week-1-concepts-setup-and-a-dummy-agent }

This week builds your mental model before you use an agent framework. Suggested time: **3–4 hours**, including reading, setup, and practice; installation and API availability can add time.

## Learning objectives { #learning-objectives }

By the end of Week 1, you can explain the difference between a model, provider, program, and tool; prepare a local Python environment; and trace a request → proposed action → function call → observation → final response.

## Learning sequence { #learning-sequence }

1. Read [Before you start](before-you-start.md) if terminals or Python editing are new to you.
2. Read [agent foundations](unit-1-walkthrough.md) and complete the two original HF quick quizzes (about 60–90 minutes). External HF lessons are optional references; unavailable playgrounds do not block local practice.
3. [Prepare your computer](prepare-your-computer.md): Python 3.11, the dummy folder, its virtual environment, the model client, and your own Groq key (about 45–60 minutes).
4. [Build and run the dummy agent in three stages](dummy-agent-local.md): a model request, an inspected proposed action, and a Python function observation (about 60–90 minutes).

Do not download or configure the full chat template this week. The dummy example uses fixed demonstration weather data; the two real tools arrive in Week 2.

## Week 1 completion { #week-1-completion }

- Explain why a model naming a tool does not mean the tool ran.
- Show Python 3.11 and an active `.venv` in the dummy folder.
- Run `python dummy_agent.py` and show all three stages, including the actual function result before the final answer.
- Explain the stop marker, the manual confirmation, and why the weather result is demo data.
- Attempt both quick quizzes; note any external activity that was unavailable. The site does not store quiz scores.

Keep `dummy_agent.py` for comparison next week. If a provider request fails, use [troubleshooting](run-your-first-agent.md#troubleshooting) and return to the failed checkpoint; reading alone does not verify a live request.

**Next:** [Week 2 — working template and tools](week-2-learning-plan.md). For both weeks, see the [course route](course-route.md).
