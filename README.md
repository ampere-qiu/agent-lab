# Agent Lab — bilingual local MkDocs course

The maintained course is in `docs/` (English) and `docs-ja/` (authored Japanese). `mkdocs.yml` and `mkdocs.ja.yml` define navigation and localized theme controls. The GitHub Actions workflow builds and publishes both languages when `main` changes. See [PUBLISHING.md](PUBLISHING.md).

## Preview on this Mac

From this directory, with documentation requirements installed in a Python virtual environment:

```bash
.venv/bin/python -m mkdocs build --strict
python -m http.server 8003 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:8003/ for English or http://127.0.0.1:8003/ja/ for Japanese. Control + C stops the server. This server is separate from the downloadable agent app on port 7860. Rebuild and refresh after Markdown edits.

On another computer, create a Python virtual environment, activate it, and install `requirements-docs.txt`. Then run `python -m mkdocs build --strict` and `python -m http.server 8003 --bind 127.0.0.1 --directory site`.

## Course mapping

The original source contains only HF Unit 1 material, not a nine-week app. It is now split into Week 1 (concepts, setup, and the dummy agent) and Week 2 (working template and tools). No later weeks or stored progress records existed to migrate. Completion remains evidence-based, with separate weekly checks; suggested durations are learning estimates.

Original lesson paths and English section IDs remain stable. `/week-1-learning-plan/` is now the Week 1 plan; `/course-route/` is the full route. `/ja/` and its lesson paths now serve the corresponding authored Japanese content, replacing translation-help pages and redirects.

## Language parity and validation

The header's EN / 日本語 switch opens the matching lesson and retains the section fragment. Both versions share explicit section IDs. Japanese prose covers instructions, exercises, code explanations, and troubleshooting. Runnable examples, identifiers, test prompts, and essential literal output are kept unchanged and explained in Japanese. External HF quizzes remain on HF and use its questions and feedback.

`hooks/bilingual.py` builds Japanese after English and shares downloads, scripts, and styles from the English tree. Material's Japanese locale translates built-in search, navigation, and copy controls. The custom 404 page is localized. There is no browser translation service or runtime translation dependency.

Run:

```bash
.venv/bin/python -m mkdocs build --strict
.venv/bin/python -m unittest discover -s tests -v
```

The tests check lesson/section parity, executable examples and prompts, resource parity, course sequence, generated links and anchors, language switches, search indexes, code protection, and localized error pages. Edit Markdown sources rather than generated `site/` files. Do not publish or copy to GitHub unless requested.
