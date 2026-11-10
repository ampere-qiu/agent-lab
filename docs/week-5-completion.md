# Week 05 · Conclusion and completion { #week-5-completion }

**Goal:** show how your documents, tools, agents and workflows connect, using actual output from your computer. Open your existing `week05-exercises` folder and `evidence.md`.

## What you built { #review }

You followed HF Unit 2.2: found integrations; assembled a document query engine; exposed functions and retrieval as tools; ran agents with memory and handoffs; and connected event-driven steps with shared state. The important boundary is visible: retrieval supplies text, tools perform operations, models make decisions or compose answers, and workflow events connect steps.

## Required evidence { #evidence }

| Topic | Files to open | What to show |
| --- | --- | --- |
| Integration | `my_llm.py` | One successful greeting or an honestly recorded connection failure. |
| Components | `my_ingest.py`, `my_retrieve.py`, `my_query.py` | Ten loaded documents, persistent vectors, actual retrieved passage and an answer checked against it. |
| Tools | `my_tools.py`, `my_query_tool.py`, `my_toolspec.py` | A direct function result, query-tool result, tool names/descriptions and explanation of utility-tool patterns. |
| Agents | `my_agent.py`, `my_memory.py`, `my_rag_agent.py`, `my_agent_team.py` | Actual arithmetic call, Bob context comparison, persona tool selection, original EXCERPT/SOURCE checks, and a handoff followed by research. |
| Workflows | `my_workflow.py`, `my_workflow_steps.py`, `my_workflow_loop.py`, `my_workflow_draw.py`, `my_workflow_state.py`, `my_team_workflow.py` | Hello result, event payload, bounded loop, `flow.html`, stored query and the team’s arithmetic counter. |
| Understanding | `evidence.md` | Your Quiz 1/2 answers and one limitation of each model-based result. |

`my_evaluate.py` is an optional extra model-based faithfulness check. External Gmail, MCP-server and Phoenix integrations are reading extensions, not required account connections. Keep their purpose clear in your notes.

Restore the original lines after comparison activities and check each lesson’s file checklist. For each row write **complete** or **incomplete**, with a short observed result or the failure still to resolve. A final answer without the requested tool trace does not satisfy a tool-use check. A quotation that comes from GENERATED ANSWER instead of the original EXCERPT does not satisfy the evidence check. A shared-context answer that forgets Bob does not satisfy the memory check. A supported incomplete result is better evidence than an invented success.

## Explain it without running it again { #explain }

1. Which operations use the local embedding model, and which use Groq?
2. How did you know which source passage supported the answer?
3. What changed when the agent could choose a query tool instead of you calling it directly?
4. What connects workflow steps, and where did the shared state live?
5. Why are the arithmetic-call counter, the model-request count and the number of agents different quantities?

Point to the relevant code and one saved observation for each answer. Keep keys out of your evidence. Preserve the generated database, your files and your notes together; the website does not save your progress or certify your result.

## Where this leads { #next }

HF’s [Unit 2.2 conclusion](https://huggingface.co/learn/agents-course/en/unit2/llama-index/conclusion) leads to its LangGraph module. The next week’s local teaching plan has not yet been published here.

Return to the [Week 5 route](week-5-learning-plan.md#route) to revisit any incomplete topic.
