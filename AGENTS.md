# Lesson editing workflow

- Week 03 now has an authored Japanese edition, requested after English review. Keep both editions aligned. Preserve HF figures unchanged and place a collapsed Japanese explanation directly beneath each figure in the Japanese lessons.
- Week 03 includes introduction, CodeAgent, Python/structured actions, function/class tools, Agentic RAG (step 12), and completion (step 13). The user moved RAG into Week 03 after tools. Keep teams/vision for Week 04. Use HF's five party documents, BM25 tool, and splitter, with source labels in returned observations. The small ZIP now has seven support files including week03_retriever.py; students create the runnable scripts from lesson blocks. Preserve attributed HF code/figures, but show one classroom Groq setup without HF-vs-local comparisons or alternate provider snippets. Give complete named-file creation/save instructions. Show Windows Command Prompt/Mac Terminal environment activation once on the weekly setup page; later practicals use a short `Run: python filename.py` instruction. Put code explanations in collapsed panels directly under their code blocks, and give comparison activities explicit examples/questions with a collapsed answer. Week 03 is terminal-only: no Gradio UI; include the pinned BM25/LangChain retrieval dependencies needed for step 12.
- Maintain authored English lessons in `docs/` and Japanese counterparts in `docs-ja/`. Do not use browser translation as the Japanese edition.
- Keep lesson filenames, explicit section IDs, runnable examples, and test prompts aligned across languages. Explain code and literal output in Japanese around the unchanged examples.
- Keep the EN / 日本語 switch linked to the matching lesson and section.
- Preserve the sequence: Week 1 concepts, setup, and dummy agent; Week 2 working template and tools; Week 03 smolagents.
- Shared styling, scripts, and downloads originate in `docs/`; `hooks/bilingual.py` copies them for the Japanese build.
- Run `python -m mkdocs build --strict` and `python -m unittest discover -s tests -v` before publishing.
- Do not commit generated `site/`, local environments, credentials, or caches.
- Push or publish only when the user requests it. Pushing `main` triggers the existing publishing workflow.

- Do not include estimated study durations for weeks, lessons, or activities. Preserve time values that are actual exercise data or code behavior. For every student-created Python file from Week 03 onward, show a visible plain-language purpose before the code: what it does, its inputs/data, and where to see the result; clarify whether it uses an LLM. Keep the detailed code explanation collapsed below the code. Apply these changes in both languages.
