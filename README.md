# Agent Lab — bilingual local MkDocs course

**Current Week 04 English teaching contract (2026-11-04):** RAG implementation stays in Week 3; Week 4 contains a five-question evidence review only. Students create each new agent in ordered, copyable construction blocks: specialist, manager/connection, image agent, then browser agent. Guidance becomes shorter as the constructor pattern repeats. Preserve explicit create/append/save steps, visible purpose and collapsed explanations/answers. The ZIP contains nine support files, English lessons and original HF figures; no RAG helper/dependencies or prebuilt exercise agents. Only adding another agent is an optional independent coding challenge. Historical revision notes below are superseded by this contract. Japanese Week 4 remains “To be released.”

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

Week 03 is a terminal-only classroom course through function/class tools, with optional Agentic RAG retained in Week 3 and revisited next week. Its seven student pages use one Groq configuration and original attributed HF examples/figures. The weekly setup page gives Windows Command Prompt and Mac Terminal activation instructions; later practicals use short run commands. Each student-created program has a visible purpose statement before its code; code explanations and guided answers start collapsed. Japanese figure explanations sit below the unchanged HF originals. Step 10 includes a required ToolCallingAgent run for comparison with CodeAgent. Student-created `my_*.py` programs are copied from complete titled code blocks. The download contains seven support files from `week03-starter/`; rebuild it with `python scripts/package_week03.py`. The requirements keep the existing agent libraries and add pinned BM25/LangChain retrieval dependencies without a UI. Optional step 12 provides web retrieval, local direct checks, source-supported answers, an unsupported-query experiment, and a new-note exercise. Week 04 reviews Week 3 RAG with a quiz and continues with staged Batman manager/web specialist construction, an optional third verifier, and guided image/browser agent construction. `week-4-preview.md` retains its URL as the Week 04 plan. Local authoring drafts remain outside the site. Keep provider/version adaptation notes in maintainer documentation, not student lesson comparisons. Run `python -m unittest discover -s week03-tests -v` in an environment with `week03-starter/week03-requirements.txt` installed; tests extract the real ZIP, create the exact student files from lesson blocks, and use mocked Groq/search calls. Live behavior and Windows execution remain unverified.

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

## Week 04 local update

Lessons in both languages continue as steps 14–17. Curated support lives in `week04-starter/`; rebuild the three self-contained lesson/support ZIPs with `python scripts/package_week04.py`. Students create the runnable files from lesson blocks. The original referenced conversation ZIPs could not be retrieved; reconstruction provenance is recorded in `week04-starter/NOTICE.md`.

The Batman task requires three filming locations and one supercar factory with claim and coordinate sources, cargo estimates, and a saved HTML table/map. A third verifier is optional. Vision uses original local venue assets; browser tools use Selenium and actual screenshot observations. Core packages remain pinned to smolagents 1.13.0. Run `python -m unittest discover -s week04-tests -v` in the agent test environment. Browser/remote model execution must be reported separately from offline tests. No publish or push was requested.

The current Week 04 Batman lesson builds the specialist and manager through complete ordered code blocks, then checks a bounded one-location handoff before the full task. Adding a third verifier is the optional independent challenge. Code explanations and question answers start collapsed. The three instructional HF figures from the audited multi-agent/vision source pages are preserved unchanged under `docs/images/huggingface-week04/`, with source URLs and hashes, Japanese explanation panels, and copies in both offline lesson editions. The HF video remains linked. The executable suite assembles the student programs from those blocks; the site suite verifies shared figure hashes, language parity and collapsed explanation panels.

## English-first review — 2026-11-04

The user requested English revisions before Japanese. Topic 14 now explicitly revisits Week 3 (links to Topic 13 completion and Topic 12 RAG), is required for Week 4, explains BM25, and gives a separate collapsed answer to each of its four Compare and challenge questions. Topic 14 is listed in `extra.translation_review_pending` so new English sections/links can be reviewed while existing Japanese anchors, runnable-code parity, page availability and generated links remain checked. Authored Japanese Markdown was not changed. Remove that entry when its Japanese revision is requested and aligned.

## Week 04 English editorial audit — 2026-11-04

All five English Week 04 pages were reviewed against Week 03's creation → purpose → code → collapsed explanation → run → expected observation → modification/answers pattern. Setup now explicitly distinguishes supplied files, student-created files/folders, and generated outputs; tells students how/where to create `evidence.md` and `evidence-files`; provides the note template; and explains terminal/folder/environment use. Each practical names its new file, exact save location, expected result and record location. Comparisons explain which existing file/input to edit and how to preserve generated outputs. Questions have individual or clearly scoped collapsed model answers. The optional verifier reference now follows the same Save As/edit-build_team workflow as its student instructions. Authored Japanese Markdown is unchanged; the five English pages are marked translation_review_pending until translation is requested. Tests validate each edition's syntax and actual links while allowing the explicitly requested English-only code/prose revisions.


## Week 04 staged-build revision — 2026-11-04

Removed the Week 4 RAG runner, retriever helper and LangChain/BM25 dependencies from the pack. Topic 14 links directly back to Week 3 and provides five short collapsed answers using earlier output or a labeled example. Batman is assembled in four blocks with explicit specialist and manager construction; vision and browser agents each use three blocks with less repeated guidance. Exercise tests assemble the blocks in the student order, validate partial-file syntax, inspect separate agent objects/registration before any model call, and exercise handoff/report/image/screenshot behavior with simulated remote/browser responses. Five required Python files remain. No new publication is authorized by this editing request.


## Week 04 Japanese local edition — 2026-11-04

The user requested Japanese after the English wording review. All five current Week 04 pages now have authored Japanese counterparts. Instructions, goals, Q&A, troubleshooting and figure explanations are Japanese; executable examples, file names, prompts and literal outputs remain identical to English. All section IDs match, including the smaller construction steps. The local header, menu and Japanese search now expose the full lessons; the previous unreleased/translation-review flags are cleared.

Both languages use the same three unchanged HF images and two English course diagrams. Japanese figure explanations start collapsed directly below each image. The shared figure viewer supports zoom, fit, original-file access, keyboard closing and focus restoration, with Japanese controls on Japanese pages. Ordinary image links remain usable without JavaScript and in the offline Markdown editions.

All three ZIP names now include both `lessons/en` and `lessons/ja`, with language-specific Week 3 links and identical helper files/figure bytes. The strict bilingual build, 11 site checks and 14 exercise checks pass. Local browser checks confirmed Japanese figure enlargement/reset/closing, explanation panels, section-preserving language switching and vision run instructions. No live model/browser-agent execution was added. Publishing checkout remains untouched; this Japanese edition has not been pushed or published.
