# Lesson editing workflow

- Maintain authored English lessons in `docs/` and Japanese counterparts in `docs-ja/`. Do not use browser translation as the Japanese edition.
- Keep lesson filenames, explicit section IDs, runnable examples, and test prompts aligned across languages. Explain code and literal output in Japanese around the unchanged examples.
- Keep the EN / 日本語 switch linked to the matching lesson and section.
- Preserve the two-week sequence: Week 1 concepts, setup, and dummy agent; Week 2 working template and tools.
- Shared styling, scripts, and downloads originate in `docs/`; `hooks/bilingual.py` copies them for the Japanese build.
- Run `python -m mkdocs build --strict` and `python -m unittest discover -s tests -v` before publishing.
- Do not commit generated `site/`, local environments, credentials, or caches.
- Push or publish only when the user requests it. Pushing `main` triggers the existing publishing workflow.
