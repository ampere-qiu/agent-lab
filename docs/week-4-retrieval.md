# 14 · Check your Week 3 RAG understanding { #week-4-retrieval }

**Quick recap:** RAG retrieves relevant passages so the model can answer from evidence. Agentic RAG lets the agent choose when and what to retrieve. Check the source; say when evidence is missing.

**Objective:** check whether an answer is supported by retrieved text.

!!! note "Return to Week 3 for the practical"

    If you have not done the RAG practical, return to [12 · Building Agentic RAG Systems](week-3-retrieval.md) and follow its existing setup, file-creation and run instructions in **`First_agent_template`**. If you already did it, review your saved code and trace. [13 · Week 3 completion checks](week-3-completion.md#optional-rag) lists the earlier files. Do not recreate them in `week04-exercises` or install RAG packages in the Week 4 environment.

Answer the questions using your Week 3 results or the provided example below. Label your notes **“Week 3 run”** or **“provided example”** so you can tell which evidence you used. You do not need a new Python program for this review.

**Where to write:** open the existing `evidence.md` you created in [Week 4 setup](week-4-preview.md#evidence-file), under **Topic 14 — Week 3 RAG review**. Write your answers in that file.

## What is BM25? { #bm25 }

**BM25 ranks documents using keyword matches.** It considers how often query words occur, how distinctive they are across the collection, and document length; repeated matches have diminishing benefit. It retrieves candidate passages; it does not generate an answer or verify a claim.

In the Week 3 example BM25 searches five local party notes, without an LLM, embeddings or a vector database. The model separately chooses a query and writes an answer from the returned observations. The tool requests up to five results from five short notes, so it can return notes even when none contains the requested fact. A high rank is not proof that an answer exists, and keyword matching does not automatically resolve synonyms.

Reference: [BM25 scoring and normalization](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity#bm25-similarity-default). No formula is required for this review.

## Read the evidence { #retrieve-first }

**Read this example; do not paste it into a Python file or run it.** It shows the main steps of the Week 3 retrieval loop. Your own tool output may contain several notes.

```text
Task: Suggest a superhero dish and cite its source.
Agent action: party_planning_retriever(query="superhero catering")
Tool observation:
  For catering, serve dishes named after superheroes, like
  'The Hulk's Green Smoothie' and 'Iron Man's Power Steak.'
  Source: Catering Ideas
Final answer: Try The Hulk's Green Smoothie [Catering Ideas].

Second query: caterer allergy policy
Observation: the five party notes contain no allergy policy.
```

## Compare and check understanding { #compare }

Try each question before opening its answer. Quote the action, passage and source from either your Week 3 results or the provided example.

**1. Underline the passage and source label supporting the suggested dish. What does that passage establish?**

??? success "Answer 1 — passage and source"

    Mark **“The Hulk's Green Smoothie”** in the catering passage and **`Source: Catering Ideas`**. They support the dish suggestion, not ingredients or allergy handling. In your note, use bold text or quote the exact words.

**2. Which line demonstrates agent retrieval? How does it differ from a direct Python tool check?**

??? success "Answer 2 — an executed retrieval action"

    The agent action `party_planning_retriever(query="superhero catering")`, followed by its returned passage, demonstrates retrieval in the loop. A direct tool test alone does not show the model chose a retrieval action. Matching the final claim to the passage shows available support; it cannot prove the model used no prior knowledge.

**3. For the second query, do the notes contain an allergy policy? Why might BM25 still return results?**

??? success "Answer 3 — missing evidence"

    **No.** Ranking the top five notes does not require any note to contain a policy. Say **“The supplied notes do not provide the caterer's allergy policy.”** This does not establish that the caterer has no policy.

**4. Rewrite this unsupported answer: “The caterer guarantees a nut-free menu and checks every guest's allergies.” What should happen next?**

??? success "Answer 4 — a supported limitation"

    **“The notes do not establish the allergy policy; obtain the caterer's authoritative policy before answering.”** A detailed guarantee would invent evidence. More confident wording cannot repair a missing source.

**5. Put these in order: final answer, retrieval observation, model chooses a query, tool searches the notes. Which part runs without an LLM?**

??? success "Answer 5 — the loop"

    Model chooses a query → tool searches the notes → retrieval observation → final answer. BM25's local search does not use an LLM; query selection and answer generation do.

**Checkpoint:** save answers 1–5 in `evidence.md` and name the evidence you used. For more coding practice, return to [Week 3’s RAG practical](week-3-retrieval.md). Next, you will build a team of agents.

**Credit:** review adapted from [HF Retrieval Agents](https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents), Apache-2.0. See Week 3 for the RAG practical.

**Next:** [15 · Build the Batman agent team](week-4-batman.md).
