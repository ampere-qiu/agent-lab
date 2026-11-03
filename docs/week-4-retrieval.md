# 14 · Agentic RAG continuation { #week-4-retrieval }

!!! note "Required in Week 4"

    We revisit the Agentic RAG work from Week 3. Start with [13 · Week 3 completion checks](week-3-completion.md), then review [12 · Building Agentic RAG Systems](week-3-retrieval.md). RAG was optional in Week 3; **this review and continuation are required in Week 4**.

**Goal:** distinguish a retrieved passage from a model claim. If you completed the earlier RAG exercise, bring its output for comparison. If you skipped it, review the retrieval loop in the linked lesson, then complete the exercise below. Prepare the [Week 04 files](week-4-preview.md#exercise-files); this download supplies the retrieval notes and support code you need.

**Before starting:** finish [Week 4 setup](week-4-preview.md#exercise-files), including [creating `evidence.md`](week-4-preview.md#evidence-file). Work in `week04-exercises`, not the Week 3 folder.

| File | Status in this lesson |
| --- | --- |
| `week04_common.py`, `week04_retriever.py` | Already supplied. The five notes are inside the retriever file; no separate note-data file is missing. |
| `my_rag_continuation.py` | Not supplied; create it below. |
| `evidence.md` | You created it during Week 4 setup. Open and update that existing file. |

## What is BM25? { #bm25 }

**BM25 is a keyword-based method for ranking documents against a search query.** It helps the retriever decide which notes to return first. It does not write an answer or check whether a claim is true.

It considers:

- **Matching words:** which query terms occur in a document.
- **How distinctive they are:** words that occur in fewer documents usually carry more weight.
- **How often they occur:** repeated matches can help, but their benefit levels off.
- **Document length:** longer documents are adjusted so they do not gain an advantage simply by containing more words.

In this exercise, BM25 runs locally over the five supplied party notes. It uses no LLM, embeddings, or vector database. The Groq model separately chooses a query, receives the returned passages as observations, and generates an answer.

**Example:** a note naming superhero dishes can support a dish suggestion. It cannot establish an allergy policy that is absent from the notes, even if the retriever ranks it highly. Word matching also does not automatically understand synonyms.

Our tool requests the top **five** results from a collection of **five** short notes. It can therefore return all five even when the query has little or no useful evidence. **Returned results are candidates to inspect, not proof that an answer exists.**

**Technical reference:** [BM25 scoring and normalization](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity#bm25-similarity-default). You do not need its formula to complete this exercise.

## Retrieve first, then generate { #retrieve-first }

1. In your code editor, open the **`week04-exercises`** folder that contains `requirements.txt` and `week04_common.py`.
2. Choose **File → New Text File**, then **File → Save As**. Save it as **`my_rag_continuation.py`** directly in that folder. **This file is not included in the ZIP; you create it now.**
3. Paste the complete code below into that file.
4. Save with **Ctrl + S** on Windows or **Command + S** on Mac. The filename must end in `.py`, not `.py.txt`. Do not save inside `.venv`, `lessons`, or `assets`.

**What this file does — `my_rag_continuation.py`:** Searches the supplied five party notes locally, then asks a Groq agent to retrieve and answer with source labels. The first terminal section uses no LLM; the second uses an LLM. Inspect both outputs.

```python title="my_rag_continuation.py"
from smolagents import CodeAgent
from week04_common import build_model, agent_options, run_task
from week04_retriever import party_planning_retriever

if __name__ == "__main__":
    print("DIRECT RETRIEVAL — NO LLM")
    print(party_planning_retriever("superhero catering"))
    agent = CodeAgent(tools=[party_planning_retriever], model=build_model(), **agent_options())
    run_task(agent, "Use party_planning_retriever for superhero catering. Suggest one dish and cite its source label. Then say whether these notes establish the caterer's allergy policy. Do not invent a policy.")
```

??? info "Explain my_rag_continuation.py"

    | Code | What it means |
    | --- | --- |
    | The imports | Load CodeAgent, the supplied Groq/settings helpers and the supplied retrieval-tool object. You do not copy its implementation into this file. |
    | `if __name__ == "__main__":` | Run these steps when you run this file as a program. |
    | The first `print` | Label the direct check so you can distinguish it from the agent trace. |
    | `party_planning_retriever("superhero catering")` | Search the supplied notes directly on your PC, without a model call. |
    | `CodeAgent(tools=[party_planning_retriever], ...)` | Register that same tool so the model can request retrieval during its own loop. |
    | `build_model()` | Prepare the Groq connection and ask for your hidden key if needed. |
    | `**agent_options()` | Insert the classroom action format, step limit and terminal logging settings. |
    | `run_task(agent, "...")` | Give the task to the model, run its actions and print the final result. |

    The direct tool result is not the agent's action. Check the later trace separately. BM25 may return documents even when the answer is absent; the model must inspect their contents.

**Run:** `python my_rag_continuation.py`. Enter your Groq key if prompted. Read the terminal, not a browser chat.

**What to check:** first find `DIRECT RETRIEVAL — NO LLM` and its returned notes. Then find the agent's separate retrieval call, its observation and final answer. Under Topic 14 in your existing `evidence.md`, paste one passage/source and the actual agent call. You do not create another output file for this program; its results are printed in the terminal.

## Compare and understand { #compare }

These are guided code-reading and result checks, not independent coding challenges. Try each question before expanding its answer. Record answers 1–4 under **Topic 14** in your existing `evidence.md`; select/copy a short terminal excerpt where requested. To “underline,” mark the passage with `**...**` in your note or identify its exact sentence and source label. The answers describe what to look for; keep what happened in **your** run.

**1. Underline the returned passage and its source label that support the suggested dish.**

??? success "Answer 1 — supporting passage and source"

    If the model suggests **The Hulk's Green Smoothie** or **Iron Man's Power Steak**, underline that dish name in the returned catering passage and **`Source: Catering Ideas`**. That passage supports the dish idea; it says nothing about ingredients or allergy policy. If your model suggests another dish, check whether the notes actually name it; do not invent supporting evidence.

**2. Find the actual retrieval call in the agent trace. Did the model use the passage or answer from memory?**

??? success "Answer 2 — retrieval evidence"

    Look for an executed **`party_planning_retriever(query=...)`** call, followed by the returned passage/source label and a final answer consistent with that observation. The earlier **`DIRECT RETRIEVAL — NO LLM`** output is a direct Python call, not evidence that the agent retrieved anything. If the agent never called the tool, it has not demonstrated Agentic RAG. A trace shows the retrieved evidence available to the model; it does not prove that the model used no prior knowledge.

**3. Change the query to `caterer allergy policy`. Run again. Do the returned notes contain a policy?**

First paste the baseline query/task and result into the existing `evidence.md`. Then open the **existing `my_rag_continuation.py`** and **replace its entire contents** with the complete policy-query version below. The title is a version label: save the file with the same name `my_rag_continuation.py`, not a new longer name. Do not append this program to the original.

**What this version does — `my_rag_continuation.py`:** runs a direct local search and a Groq agent search for the supplied allergy-policy question. The data still comes from the same five notes, and results appear in the terminal. You do not write another prompt yourself.

```python title="my_rag_continuation.py — policy-query version"
from smolagents import CodeAgent
from week04_common import build_model, agent_options, run_task
from week04_retriever import party_planning_retriever

if __name__ == "__main__":
    print("DIRECT RETRIEVAL — NO LLM")
    print(party_planning_retriever("caterer allergy policy"))
    agent = CodeAgent(tools=[party_planning_retriever], model=build_model(), **agent_options())
    run_task(agent, "Use party_planning_retriever to search for caterer allergy policy. State whether the returned notes establish a policy. Cite any supporting source; if none does, say the policy is not provided.")
```

??? info "Explain the policy-query version"

    The imports and agent wiring are unchanged. The direct query and the supplied agent task both now ask about allergy policy. BM25 can still return party notes; the model must say when those notes lack the requested policy. Replacing only the direct-call query would not change the agent's task, which is why the complete replacement is given here.

Save and run **`python my_rag_continuation.py`** again. Record the actual result under Topic 14 in the existing note.

??? success "Answer 3 — unsupported query"

    **No.** The five notes contain party ideas, including dishes, but no caterer's allergy policy. BM25 can still return notes because this tool returns the top five without an evidence threshold. A suitable answer is: **“The supplied notes do not provide the caterer's allergy policy.”** This does not mean that the caterer has no policy; it means this collection does not establish one.

**4. Explain why a cautious answer is better supported than a detailed invented policy.**

??? success "Answer 4 — a supported limitation"

    “The notes do not provide this policy” accurately describes the available evidence. A detailed policy would add unsupported claims, such as ingredients, allergen handling, or guarantees. The next step is to obtain an authoritative policy from the caterer, then answer from that source. More detail does not make an unsupported answer more reliable.

**Checkpoint:** save `my_rag_continuation.py` and `evidence.md`. Show one successful direct retrieval, one executed agent retrieval, a source-supported claim, and an unsupported-policy result. Restore the original query/task if you want to repeat the baseline later; do not delete the comparison from your note.

**Credit:** adapted from [HF Retrieval Agents](https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents); original five-document BM25 example, Apache-2.0. The supplied `HF-LICENSE.txt` retains the license.

**Next:** [15 · Batman multi-agent exercise](week-4-batman.md).
