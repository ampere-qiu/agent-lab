# Lesson editing workflow

- Week 03 now has an authored Japanese edition, requested after English review. Keep both editions aligned. Preserve HF figures unchanged and place a collapsed Japanese explanation directly beneath each figure in the Japanese lessons.
- Week 03 required scope ends after tools: introduction, CodeAgent, Python/structured actions, function/class tools, and completion. Retrieval/teams/vision belong on the Week 04 continuation page; keep their drafts outside docs and the minimal Week 03 ZIP. Preserve attributed HF code/figures, but show one classroom Groq setup without HF-vs-local comparisons or alternate provider snippets. Give complete named-file creation/save instructions. Show Windows Command Prompt/Mac Terminal environment activation once on the weekly setup page; later practicals use a short `Run: python filename.py` instruction. Put code explanations in collapsed panels directly under their code blocks, and give comparison activities explicit examples/questions with a collapsed answer. Week 03 is terminal-only: no Gradio UI or retrieval dependencies.
- Maintain authored English lessons in `docs/` and Japanese counterparts in `docs-ja/`. Do not use browser translation as the Japanese edition.
- Keep lesson filenames, explicit section IDs, runnable examples, and test prompts aligned across languages. Explain code and literal output in Japanese around the unchanged examples.
- Keep the EN / 日本語 switch linked to the matching lesson and section.
- Preserve the sequence: Week 1 concepts, setup, and dummy agent; Week 2 working template and tools; Week 03 smolagents.
- Shared styling, scripts, and downloads originate in `docs/`; `hooks/bilingual.py` copies them for the Japanese build.
- Run `python -m mkdocs build --strict` and `python -m unittest discover -s tests -v` before publishing.
- Do not commit generated `site/`, local environments, credentials, or caches.
- Push or publish only when the user requests it. Pushing `main` triggers the existing publishing workflow.
