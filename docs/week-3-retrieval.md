# 12 · Building Agentic RAG Systems { #week-3-retrieval }

**Objective:** give an agent a searchable collection of notes, follow what it retrieves, and check that its answer is supported by those notes. **Activities:** read, run a web-search agent, test a local retriever without an LLM, run a local RAG agent, and add your own note.

Finish [11 · Tools: functions and classes](week-3-custom-tool.md) first. All new files go directly in **`First_agent_template`**, beside `app.py`. Use the same activated environment and Groq key. Run the saved files in the terminal.

## What is new after the tools lesson? { #retrieval-concept }

Your menu and theme tools select a fixed response from Python data. Now you will give the agent a **retrieval tool**: a tool that searches a collection of text and returns useful passages.

**RAG** means **Retrieval-Augmented Generation**: find relevant material, give it to the model, and use it to answer. **Agentic RAG** lets the model choose a search query, read the results, and request another search when needed.

**Question → model chooses a search → Python retrieves text → observation → model answers or searches again.**

| Part | Job | Runs where? |
| --- | --- | --- |
| Model | Choose the query and write an answer using returned text. | Groq |
| Retrieval tool | Search the supplied notes and return their text and source labels. | Your PC |
| CodeAgent | Execute the requested action and coordinate the loop. | Your PC |

The notes stay in a local Python file, but retrieved passages are sent to Groq as observations during an agent run. The direct test below does not contact Groq. Retrieval does not train the model or automatically save a permanent memory.

## Prepare the retrieval files { #setup }

The current [Week 03 download](week-3-learning-plan.md#exercise-files) contains **seven support files**, including **`week03_retriever.py`**. If you downloaded an earlier six-file ZIP, download the current one and copy **`week03_retriever.py`** and **`week03-requirements.txt`** beside `app.py`. Keep your edited `week03_tools.py` and your `my_...py` programs.

In your existing activated terminal, run this once if you have not installed the updated requirements:

```bash
python -m pip install -r week03-requirements.txt
```

This adds `langchain-community`, `langchain-text-splitters`, and `rank-bm25` for the retrieval tool. It keeps `smolagents==1.13.0` and your Groq connection. You do not need another API key, an embedding model, or a vector database. If a retrieval import is missing, check that you installed this updated list in the same `.venv` used to run the files. An import deprecation warning is different from a failed test: check the actual result.

## A. Retrieve information from the web { #web-retrieval }

First, use the search tool you already know. The task asks for **decorations, entertainment, and catering** for a luxury superhero party. The model can search for these topics and combine the results into a plan.

Create **`my_rag_search.py`** in your code editor, paste the complete code, and save it beside `app.py`.

**What this file does — `my_rag_search.py`:** Runs a web-search agent to gather ideas for decorations, entertainment, and catering, then turn retrieved information into a party plan. Groq chooses the searches and writes the plan; the Python tool retrieves snippets and URLs. Inspect the terminal output to see which sources support the suggestions.

```python title="my_rag_search.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_search import WebSearchTool

model = build_model()
search_tool = WebSearchTool()
agent = CodeAgent(
    tools=[search_tool],
    model=model,
    **agent_options(),
)

task = "Search for luxury superhero-themed party ideas, including decorations, entertainment, and catering."
task += " Use web_search and print its results. Cite only URLs returned by the tool."
raise SystemExit(run_task(agent, task))
```

??? info "Explain my_rag_search.py"

    | Code | What it does |
    | --- | --- |
    | The imports | Load CodeAgent, the supplied Groq helpers, and the search-tool class. |
    | `model = build_model()` | Prepare the Groq connection; ask for your key if needed. |
    | `search_tool = WebSearchTool()` | Create a search-tool instance. This does not search yet. |
    | `tools=[search_tool]` | Make that instance available to CodeAgent. |
    | `model=model` and `**agent_options()` | Use your Groq connection and the classroom Python-action settings. |
    | `task = ...` | Ask for party ideas across three topics. |
    | `task += ...` | Append instructions to show retrieved results and use their URLs. `+=` adds text to the existing string. |
    | `raise SystemExit(run_task(agent, task))` | Run the task, print the result, and exit with its success/error status. |

    The model chooses the queries. Python on your PC calls the search service. Returned snippets become observations for the model. This is the familiar web-search pattern, now used to gather material for a broader answer.

**Run:** `python my_rag_search.py`.

**Activity:** find a search call, a returned snippet and URL, and a part of the final plan supported by that result. Did the actual run search once or more than once?

??? success "Show answer"

    Find model-generated Python calling `web_search(...)`, then the actual returned data. Choose one URL from that output and check whether the answer uses information from its snippet. A URL appearing only in model-written text is not evidence of retrieval.

    **A guided answer:** “The model chose the search terms. The search tool returned a snippet and URL. The agent used that information to suggest part of the plan.” Add your actual query, source, and supported suggestion.

    Count the real calls in your trace. The task allows multiple searches, but one run may use only one; do not report extra searches that did not happen. If the service failed, record the error rather than a successful source. Suggested party ideas are not proof that a real vendor offers that service.

## B. Read the local knowledge-base tool { #hf-retrieval-code }

Open the supplied **`week03_retriever.py`**. This is the complete code already in that file; **read it there rather than creating another copy**. Its five short notes are fictional party-planning material, with source labels.

```python
"""HF PartyPlanningRetrieverTool and five example documents (Apache-2.0).
Source: https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents
Changes: accurate BM25 description and returned source metadata.
"""
from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from smolagents import Tool


class PartyPlanningRetrieverTool(Tool):
    name = "party_planning_retriever"
    description = "Uses BM25 keyword search to retrieve relevant party planning ideas for Alfred’s superhero-themed party at Wayne Manor."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be a query related to party planning or superhero themes.",
        }
    }
    output_type = "string"

    def __init__(self, docs, **kwargs):
        super().__init__(**kwargs)
        self.retriever = BM25Retriever.from_documents(
            docs, k=5  # Retrieve the top 5 documents
        )

    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"

        docs = self.retriever.invoke(
            query,
        )
        return "\nRetrieved ideas:\n" + "".join(
            [
                f"\n\n===== Idea {str(i)} =====\n" + doc.page_content
                + f"\nSource: {doc.metadata['source']}"
                for i, doc in enumerate(docs)
            ]
        )

# Simulate a knowledge base about party planning
party_ideas = [
    {"text": "A superhero-themed masquerade ball with luxury decor, including gold accents and velvet curtains.", "source": "Party Ideas 1"},
    {"text": "Hire a professional DJ who can play themed music for superheroes like Batman and Wonder Woman.", "source": "Entertainment Ideas"},
    {"text": "For catering, serve dishes named after superheroes, like 'The Hulk's Green Smoothie' and 'Iron Man's Power Steak.'", "source": "Catering Ideas"},
    {"text": "Decorate with iconic superhero logos and projections of Gotham and other superhero cities around the venue.", "source": "Decoration Ideas"},
    {"text": "Interactive experiences with VR where guests can engage in superhero simulations or compete in themed games.", "source": "Entertainment Ideas"}
]

source_docs = [
    Document(page_content=doc["text"], metadata={"source": doc["source"]})
    for doc in party_ideas
]

# Split the documents into smaller chunks for more efficient search
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
    strip_whitespace=True,
    separators=["\n\n", "\n", ".", " ", ""],
)
docs_processed = text_splitter.split_documents(source_docs)

# Create the retriever tool
party_planning_retriever = PartyPlanningRetrieverTool(docs_processed)
```

??? info "Explain week03_retriever.py"

    Read the file in this order:

    | Part | Meaning |
    | --- | --- |
    | `party_ideas` | Five notes: luxury decor, a DJ, superhero food, projected logos, and VR activities. Each has `text` and a `source` label. |
    | `Document(...)` | Wrap each note's text and retain its source in `metadata`. |
    | `RecursiveCharacterTextSplitter(...)` | Prepare chunks with a maximum target of 500 characters and 50 characters of overlap when splitting is needed. These short notes remain five chunks. `add_start_index` records each chunk's starting position. |
    | `PartyPlanningRetrieverTool(Tool)` | Define a tool class, as in step 11. Its name, description, `inputs`, and `output_type` describe the interface to the model. |
    | `__init__(self, docs, **kwargs)` | Set up an instance using the supplied documents. `super().__init__(**kwargs)` initializes the base Tool. |
    | `BM25Retriever.from_documents(docs, k=5)` | Build a local word-based index and request up to five ranked results per query. |
    | `forward(self, query)` | Check that the query is a string, call the retriever, and return its results as text. The tool itself does not call an LLM. |
    | `enumerate(docs)` | Number the results in their current order, starting at zero. `Idea 0` is a result position, not a permanent document ID. |
    | `Source: ...` | Include the saved source label alongside each returned passage so the answer can be checked. |
    | `party_planning_retriever = ...` | Create the tool instance from the processed documents. Importing this module prepares it locally. |

    **BM25 uses matching words to rank text.** It is not an embedding model. Spelling, capitalization, punctuation, and synonyms can affect matching with this simple default tokenizer.

    **Important limitation:** `k=5` asks for five results, and there are five original notes. All five can therefore be returned, including weak or irrelevant matches. This tool has no score threshold or automatic “nothing found” response. The first result is ranked highest; that does not make every returned passage relevant.

The `Source:` values are labels for these supplied notes, not web addresses. Two entertainment notes share the same label; use the label **and the passage text** to identify which one supports a claim.

## C. Test retrieval without an LLM { #direct-tests }

Create **`my_retrieval_check.py`** beside `app.py`, paste the complete code, and save it.

**What this file does — `my_retrieval_check.py`:** Tests the local knowledge-base tool without creating an agent. It checks that the velvet query ranks the expected note first, that source labels are preserved, and that an absent query word can still return documents. It prints retrieved notes and PASS when the checks succeed; no LLM or Groq key is used.

```python title="my_retrieval_check.py"
from week03_retriever import party_ideas, docs_processed, party_planning_retriever

matches = party_planning_retriever.retriever.invoke("velvet")
assert "velvet curtains" in matches[0].page_content
assert matches[0].metadata["source"] == "Party Ideas 1"
assert len(docs_processed) == len(party_ideas)

result = party_planning_retriever(query="velvet")
assert "Source: Party Ideas 1" in result
print(result)

unrelated = party_planning_retriever.retriever.invoke("zyxwvu")
assert len(unrelated) == min(5, len(docs_processed))
assert all("zyxwvu" not in doc.page_content.lower() for doc in unrelated)

print("PASS: retrieval ranks a matching note, preserves sources, and exposes the no-match limitation.")
```

??? info "Explain my_retrieval_check.py"

    | Code | Meaning |
    | --- | --- |
    | The import | Load the notes, processed chunks, and prepared tool instance. |
    | `.retriever.invoke("velvet")` | Search directly and return Document objects so you can inspect their text and metadata. |
    | The first two `assert` lines | Check that the first match contains `velvet curtains` and has the expected source. |
    | `len(docs_processed) == len(party_ideas)` | Check that these short notes each remain one chunk. |
    | `party_planning_retriever(query="velvet")` | Call the tool interface used by the agent; its result is formatted text with source labels. |
    | The `zyxwvu` checks | Demonstrate that the retriever returns ranked items even though none contains the query word. `min(5, ...)` allows the check to work after you add a sixth short note. |
    | `all(...)` | Require every returned document to satisfy the condition. |
    | The final `print` | Report success only if all assertions passed. |

    No agent or Groq model is created here. This checks local Python retrieval without an API key or a network request. If an assertion fails, fix the local data or retrieval setup before asking the model to use it.

**Run:** `python my_retrieval_check.py`.

Read the returned notes. The first result should contain `velvet curtains` and `Source: Party Ideas 1`, followed eventually by:

```text
PASS: retrieval ranks a matching note, preserves sources, and exposes the no-match limitation.
```

**Activity:** why does the test pass even though `zyxwvu` appears in none of the notes? Does “five documents returned” mean “five useful documents”?

??? success "Show answer"

    The `velvet` query checks that a matching note ranks first and its source survives. The `zyxwvu` query checks a different behavior: BM25 still returns up to five ranked documents when the query has no matching words. This tool does not filter out zero-score results.

    **A guided answer:** “Returned documents are candidates, not proof of relevance. The local test exposes the limitation; the agent must still check whether their text supports the requested answer.” The test passes because it expects this behavior, not because the unknown word was found.

## D. Let CodeAgent use the notes { #agent-retrieval }

Create **`my_rag.py`** beside `app.py`, paste the complete code, and save it.

**What this file does — `my_rag.py`:** Runs an agent that answers party-planning questions from the local notes in week03_retriever.py. Python retrieves passages and source labels, then the model on Groq uses that text to answer. The terminal shows the retrieval and final answer so you can check the evidence, try an unsupported question, and verify a note you add.

```python title="my_rag.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_retriever import party_planning_retriever

model = build_model()
agent = CodeAgent(
    tools=[party_planning_retriever],
    model=model,
    **agent_options(),
)

task = "Find ideas for a luxury superhero-themed party, including entertainment, catering, and decoration options."
task += " Use party_planning_retriever and print its results."
task += " Answer briefly from the returned notes and cite their Source labels."
task += " If the notes do not support an answer, say so."
raise SystemExit(run_task(agent, task))
```

??? info "Explain my_rag.py"

    | Code | Meaning |
    | --- | --- |
    | `from week03_retriever import party_planning_retriever` | Load the tool instance and its local index. This is the retriever you just tested. |
    | `build_model()` | Prepare the same Groq connection used earlier. |
    | `tools=[party_planning_retriever]` | Register the existing instance; do not add parentheses to call it during setup. |
    | `CodeAgent(...)` | Coordinate Python actions, tool results, and model requests. |
    | `task = ...` | Ask for entertainment, catering, and decoration ideas. |
    | The three `task += ...` lines | Ask the agent to retrieve and print notes, use returned sources, and admit missing evidence. These are instructions; inspect the trace to verify them. |
    | `run_task(...)` | Start the model/action/observation loop and print the final result. |

    **Follow one run:** the model proposes `party_planning_retriever(query=...)`; local Python retrieves passages; their text and labels become the observation; the model uses that observation to write an answer. Unlike the direct test, this agent run needs Groq and internet access.

**Run:** `python my_rag.py`.

**Activity:** choose one suggestion in the answer. Find the actual retrieval call, the passage that supports it, and its returned `Source:` label. Write down all three.

??? success "Show answer"

    A source-supported example would be a DJ suggestion based on the returned passage beginning `Hire a professional DJ`, with `Source: Entertainment Ideas`. A luxury-decor suggestion could be supported by the gold accents and velvet-curtains passage with `Source: Party Ideas 1`.

    **A guided answer:** “The agent called the retriever with [my actual query]. It returned [the passage I observed], labelled [its Source]. The final answer used that passage to suggest [the supported idea].” Fill this in from your own run; these examples do not prove your agent called the tool.

    Check the passage as well as its label. A source name alone cannot support extra details absent from the text, such as a price, a confirmed booking, or a real vendor's availability.

## E. Ask a focused question and an unsupported question { #query-experiments }

In **`my_rag.py`**, replace only the first `task = ...` sentence with `task = "Find the idea mentioning velvet curtains."`. Keep the three appended instructions. Save and run **`python my_rag.py`** again.

Then replace that sentence with `task = "Do these notes contain the word zyxwvu?"`, save, and run the same file again. Keep the execution records from both runs.

**Activity:** what evidence supports the first answer? What should the second answer say even if the retriever returns notes?

??? success "Show answer"

    **Focused query:** look for the actual returned passage containing `velvet curtains`, labelled `Party Ideas 1`. That text supports the first answer.

    **Unsupported query:** none of the supplied notes contains `zyxwvu`. The retriever can still return five items; the answer should state that the word was not found in the returned notes. Returning text does not mean it answers the question.

    The model chooses its own search wording, so inspect the real query. If the final answer invents a matching passage, it fails this check even though the Python tool ran successfully.

## F. Add your own knowledge { #challenge }

1. Open **`week03_retriever.py`** and find `party_ideas`.
2. Add a sixth dictionary entry before the closing `]`, keeping the same `"text"` and `"source"` fields. For example, use `"text": "Create a planetarium ceiling for the party."` and `"source": "Student Decoration Idea"`. Keep a comma between entries.
3. Save. In **`my_rag.py`**, set the first task sentence to `task = "Find the planetarium decoration idea."`. Keep the appended instructions, save, and run **`python my_rag.py`**.
4. Find the new passage and its source in the tool output and answer. Run **`python my_retrieval_check.py`** again; the original velvet note should still rank first for its query.

**Activity:** did you train the model? Why might one of six notes be absent from a retrieval result?

??? success "Show answer"

    You changed the **knowledge base**, not the model's weights. Restarting the program loads your edited notes and rebuilds the local index. Searching for `planetarium` should now bring the new note near the top; verify the actual output and source.

    With six short notes and `k=5`, each retrieval returns at most five, so at least one note is left out. The direct check still uses the original `velvet` query; it does not replace checking your new note and the agent's answer.

## How a larger system could improve retrieval { #limitations-and-next-steps }

| Strategy | In simple words |
| --- | --- |
| Query reformulation | Rewrite a question into better search terms. |
| Query decomposition | Split a multi-part question into smaller searches. |
| Query expansion | Search several alternative wordings. |
| Reranking | Score the first results again with another method, such as a cross-encoder. |
| Multi-step retrieval | Let the first results inform the next search. |
| Source integration | Combine material from different sources, such as notes and the web. |
| Result validation | Check whether the returned text is relevant and supports the answer. |

These are design options, not features automatically added by BM25. The two programs above register one retrieval tool each; they do not demonstrate automatic choice between web search and local notes in a single agent. Execution history can help within a run, but persistent memory requires additional design.

**Activity:** the question asks about catering and entertainment. What could the agent do if one broad query gives poor results?

??? success "Show answer"

    It could split the question into two searches, such as `catering` and `entertainment`, inspect both observations, and combine supported passages. That is query decomposition and potentially multi-step retrieval. Using alternative words is query reformulation or expansion. Check the trace before claiming your small example actually did any of these.

**Checkpoint:** show the passing direct test, an actual retrieval call, a source-supported answer, the unsupported-query result, and your added note. Explain what the model chooses and what local Python executes.

## Credits and next step { #sources }

Adapted from [Hugging Face Agents Course — Building Agentic RAG Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents), under the [Apache 2.0 license](licenses/huggingface-agents-course.txt). The party notes, retriever class, and splitter settings come from that lesson. The returned text includes the notes' source labels.

The [original notebook](https://huggingface.co/agents-course/notebooks/blob/main/unit2/smolagents/retrieval_agents.ipynb) and [larger agentic RAG recipe](https://huggingface.co/learn/cookbook/agent_rag) are further references. [HF Quick Quiz 2](https://huggingface.co/learn/agents-course/en/unit2/smolagents/quiz2) is optional.

**Next:** [13 · Completion checks](week-3-completion.md).
