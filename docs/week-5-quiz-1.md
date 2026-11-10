# Week 5 · Quiz 1 { #week-5-quiz-1 }

**Goal:** explain components and tools before you use them in an agent. Write your answers under **Quiz 1** in `evidence.md`, then open the explanations. These are classroom self-checks following the topics of [HF Quiz 1](https://huggingface.co/learn/agents-course/en/unit2/llama-index/quiz1); they do not submit a score to HF.

## 1. Query engine { #query-engine }

How does a query engine differ from the retriever you ran?

??? success "Answer 1"

    The retriever returns candidate passages and scores. A query engine also uses a model to compose an answer from retrieved information. Both need their outputs checked.

## 2. Function tool { #function-tool }

What does `FunctionTool` add to a Python function? Does calling it directly require an LLM?

??? success "Answer 2"

    It exposes the function through a tool interface with a name, description and input schema. A direct call runs the function without an LLM deciding to use it.

## 3. Tool collection { #tool-spec }

Your `ClassroomToolSpec` returns two tools. How many agents did it create?

??? success "Answer 3"

    Zero. It groups capabilities into a list. An agent is created separately and can be given that list.

## 4. Clear interface { #interface }

Why is “search ten persona descriptions for interests and expertise” a better description than “a useful tool”? Which parts of a function help form its schema?

??? success "Answer 4"

    The specific description helps a model decide when the tool is appropriate and what information it can supply. The function’s name, parameter names, type annotations and docstring describe its inputs and purpose. Metadata can be inferred, but should be inspected and clarified.

**Ready to continue:** locate one actual source passage and explain which tool could retrieve it. If you cannot, revisit [components](week-5-components.md#retrieve) and [tools](week-5-tools.md#query-tool).

**Next:** [22 · Agents](week-5-agents.md).
