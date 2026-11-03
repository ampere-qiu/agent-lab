# Agent Lab — local AI agent course

English and Japanese course materials adapt Hugging Face Agents Course for local Python execution and Groq model calls. Weeks 1–2 cover foundations and a working template; Week 03 covers smolagents, action formats, tools and optional RAG.

## Week 04 release

Week 04 is available in **English only**. Japanese Week 04 pages are marked **To be released**. Published Japanese Weeks 1–3 remain available.

- Topic 14: required RAG continuation, BM25 explanation and guided evidence comparison.
- Topic 15: required Batman manager/web-specialist practical using complete provided code; adding a third agent is the only optional independent coding challenge.
- Topic 16: guided image and browser-observation programs with supplied assets/tools and exact comparison steps.
- Topic 17: file/output review and individual collapsed explanation answers.

Required programs have explicit file creation/save instructions, a visible purpose, complete code, collapsed code explanations, run commands and observation checks. The setup creates the student's `evidence.md` note and distinguishes supplied, student-created and generated files.

## Build and preview

Use Python 3.11. Create/activate a documentation environment and install `requirements-docs.txt`, then run:

```bash
python -m mkdocs build --strict
python -m unittest discover -s tests -v
python preview.py
```

English preview: http://127.0.0.1:8003/ . Japanese: http://127.0.0.1:8003/ja/ . Edit `docs/` sources, not generated `site/` files.

The bilingual build hook preserves corresponding URLs. For Week 04 it suppresses unreleased Japanese lesson bodies, shows release notices, and disables the English page's Japanese switch with “To be released”. Public Japanese Week 04 Markdown is placeholder text. `extra.unreleased_translations` controls this boundary.

## Student downloads and exercise validation

Rebuild curated downloads with:

```bash
python scripts/package_week03.py
python scripts/package_week04.py
```

Week 04 ZIPs contain English lessons, credited original HF figures, and an explicit support-file allowlist. They exclude Japanese drafts, local environments, credentials, generated student outputs and test data. Students create the required runner files from the complete lesson blocks.

For executable validation, use a separate Python 3.11 environment with `week04-starter/requirements.txt` installed:

```bash
python -m unittest discover -s week03-tests -v
python -m unittest discover -s week04-tests -v
```

The tests extract the actual downloads and run real framework/tool code with simulated remote/browser responses. They do not establish live model availability, successful live research or Selenium driver behavior.

## Publishing and attribution

Pushes to `main` trigger the existing GitHub Pages workflow. See `PUBLISHING.md`. Do not commit generated `site/`, environments, caches or secrets.

Original Hugging Face material retains its Apache-2.0 license. Figure source URLs and hashes are included alongside the images; classroom adaptations are credited in the lessons and student notices.
