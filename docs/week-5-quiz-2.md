# Week 5 · Quiz 2 { #week-5-quiz-2 }

**Goal:** explain how agent decisions, events and state work together. Answer under **Quiz 2** in `evidence.md` before opening the explanations. These classroom checks follow the topics of [HF Quiz 2](https://huggingface.co/learn/agents-course/en/unit2/llama-index/quiz2); they do not submit a score.

## 1. AgentWorkflow { #agent-workflow }

What does `AgentWorkflow` organize? Does constructing it prove that its agents handed off a task?

??? success "Answer 1"

    It organizes one or more agents and their tools, including permitted handoffs. Construction shows configuration. An actual tool/handoff trace shows execution.

## 2. Shared state { #context }

Which object held the stored query and the team’s arithmetic counter? How is it different from `ProcessingEvent`?

??? success "Answer 2"

    `Context` held shared state. `ProcessingEvent` carried a typed payload between matching steps and determined routing. Both can carry information, but their roles in the workflow differ.

## 3. Conversation memory { #memory }

Why did both Bob messages use the same `ctx`? Would a new context automatically know his name?

??? success "Answer 3"

    Passing the same context retains the earlier interaction. A new context has no evidence of that earlier name. Guessing the name is not remembering it.

## 4. Agentic RAG { #agentic-rag }

How does an agent with arithmetic and persona tools differ from calling the persona query engine directly?

??? success "Answer 4"

    The direct query follows a fixed retrieval-and-answer operation. The agent can choose between available tools and formulate their inputs. You must inspect which tool it actually chose and whether the returned evidence supports the final answer.

**Extra check:** `ARITHMETIC CALLS: 1` appears in your output. Does that mean there was only one Groq request?

??? success "Counter answer"

    No. The counter counts only executions of the arithmetic functions. Handoffs and decisions can require other model requests. It is not a request or token meter.

**Next:** [Conclusion and completion](week-5-completion.md).
