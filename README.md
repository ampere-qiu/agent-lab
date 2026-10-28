# Agent Lab — bilingual local MkDocs course

The maintained course is in `docs/` (English) and `docs-ja/` (authored Japanese). `mkdocs.yml` and `mkdocs.ja.yml` define navigation and localized theme controls. The GitHub Actions workflow builds and publishes both language editions when `main` changes. See `PUBLISHING.md` in the publishing repository.

## Preview on this Mac

From this directory:

```bash
.venv/bin/python -m mkdocs build --strict
.venv/bin/python preview.py
```

Open http://127.0.0.1:8003/ for English or http://127.0.0.1:8003/ja/ for Japanese. Control + C stops the server. This server is separate from the downloadable agent app on port 7860. Rebuild and refresh after Markdown edits.

On another computer, create a Python virtual environment, activate it, and install `requirements-docs.txt`. Then run `python -m mkdocs build --strict` and `python preview.py`.

## Course mapping

The original source contains only HF Unit 1 material, not a nine-week app. It is split into Week 1 (concepts, setup, and the dummy agent) and Week 2 (working template and tools). No later weeks or stored progress records existed to migrate. Week 03 deepens the smolagents work through HF Unit 2.1 in English and authored Japanese. Its lessons continue the numbering from Week 2 as steps 08–13, including completion checks. Completion remains evidence-based, with separate weekly checks. Student pages do not prescribe study durations.

Week 03 is a terminal-only classroom course through function/class tools, with optional Agentic RAG retained in Week 3 and revisited next week. Its seven student pages use one Groq configuration and original attributed HF examples/figures. The weekly setup page gives Windows Command Prompt and Mac Terminal activation instructions; later practicals use short run commands. Each student-created program has a visible purpose statement before its code; code explanations and guided answers start collapsed. Japanese figure explanations sit below the unchanged HF originals. Step 10 includes a required ToolCallingAgent run for comparison with CodeAgent. Student-created `my_*.py` programs are copied from complete titled code blocks. The download contains seven support files from `week03-starter/`; rebuild it with `python scripts/package_week03.py`. The requirements keep the existing agent libraries and add pinned BM25/LangChain retrieval dependencies without a UI. Optional step 12 provides web retrieval, local direct checks, source-supported answers, an unsupported-query experiment, and a new-note exercise. `week-4-preview.md` is the continuation placeholder. Team and vision/browser material is reserved for Week 04; local authoring drafts remain outside the published site and ZIP. Keep provider/version adaptation notes in maintainer documentation, not student lesson comparisons. Run `python -m unittest discover -s week03-tests -v` in an environment with `week03-starter/week03-requirements.txt` installed; tests extract the real ZIP, create the exact student files from lesson blocks, and use mocked Groq/search calls. Live behavior and Windows execution remain unverified.

Original lesson paths and English section IDs remain stable. `/week-1-learning-plan/` is now the Week 1 plan; `/course-route/` is the full route. `/ja/` and its lesson paths now serve the corresponding authored Japanese content, replacing translation-help pages and redirects.

## Language parity and validation

The header's EN / 日本語 switch opens the matching lesson and retains the section fragment. Translated pages share explicit section IDs. Japanese prose covers instructions, exercises, code explanations, and troubleshooting. Runnable examples, identifiers, test prompts, and essential literal output are kept unchanged and explained in Japanese. External HF quizzes remain on HF and use its questions and feedback.

`hooks/bilingual.py` builds Japanese after English and shares downloads, scripts, styles, images, and licenses from the English tree. Material's Japanese locale translates built-in search, navigation, and copy controls. The custom 404 page is localized. There is no browser translation service or runtime translation dependency.

Run:

```bash
.venv/bin/python -m mkdocs build --strict
.venv/bin/python -m unittest discover -s tests -v
```

The tests check lesson/section parity, executable examples and prompts, resource parity, course sequence, generated links and anchors, language switches, search indexes, code protection, and localized error pages. Edit Markdown sources rather than generated `site/` files. Do not publish or copy to GitHub unless requested.
