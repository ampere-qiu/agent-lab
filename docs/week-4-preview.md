# Week 04 · smolagents Part 2 { #week-4-preview }

**Objective:** revisit retrieval, build a required manager/web-specialist team, and use image and browser observations. Topics 14, 15, 16 and the completion review are required. Adding the third verifier in Topic 15 is optional and is the only independent coding challenge. Required work follows Week 3: create a file from the complete given code, read its explanation, run the supplied steps and check your understanding.

**Before starting:** complete [Week 03](week-3-learning-plan.md). Keep that work in `First_agent_template`; Week 4 uses a **separate `week04-exercises` folder**. The course website is where you read. Your code editor is where you create files. Your activated terminal is where you run Python. The exercises do not add a chat box to this website.

## Learning route { #planned-topics }

| Topic | What you will do | Required? |
| --- | --- | --- |
| [14 · Agentic RAG continuation](week-4-retrieval.md) | Revisit Week 3 retrieval, run local/agent retrieval and compare four questions with their collapsed answers. | Yes; RAG was optional only in Week 3. |
| [15 · Batman multi-agent guided exercise](week-4-batman.md) | Read the supplied roles, copy the complete program, run the given small/full tasks and explain the handoffs and sourced report. | Yes; the third verifier is optional. |
| [16 · Vision & Browser Agents](week-4-vision-browser.md) | Create three programs, inspect an image, operate a local page and compare screenshots after a change. | Yes. |
| [17 · Completion checks](week-4-completion.md) | Review your saved programs, actual evidence and explanation answers. | Yes. |

## 1. Download and locate the supplied files { #exercise-files }

[Download all Week 04 lessons and support files](downloads/week04-smolagents-part2.zip){ .md-button .md-button--primary }

The [Batman download](downloads/week4_batman_guided_student.zip) and [Vision & Browser download](downloads/week4_vision_browser_student.zip) contain the same complete pack. **Download and extract only one ZIP.**

1. Save the ZIP, usually in **Downloads**.
2. **Windows:** right-click → **Extract All** → **Extract**. **Mac:** double-click it in Finder.
3. Open the extracted folder named **`week04-exercises`**. If extraction created an outer folder, open the inner `week04-exercises` folder. You are in the right place when `requirements.txt` and `week04_common.py` appear together.
4. Move this whole folder into your existing **`agent-course`** folder, beside `First_agent_template`. The default location is `%USERPROFILE%\agent-course\week04-exercises` on Windows or `~/agent-course/week04-exercises` on Mac. If your course folder is elsewhere, use that location in the commands below.

**Already supplied in the ZIP — open these existing files; do not create replacements:**

| Supplied item | Purpose |
| --- | --- |
| `README.md`, `NOTICE.md`, `HF-LICENSE.txt` | Instructions, source/adaptation notes and the HF license. |
| `requirements.txt` | Package installation list. |
| `week04_common.py` | Groq connection, agent settings and terminal result printing. |
| `week04_retriever.py` | Five party notes and their BM25 retrieval tool. |
| `week04_search.py` | Web-search tool. |
| `week04_tools.py` | Cargo estimate and HTML report writer. |
| `week04_browser.py` | Local browser tools and screenshot callback. |
| `prepare_visuals.py` | A supplied program that generates the practice image/page. |
| `lessons/en` | Released English lessons and original credited HF figures. The Japanese Week 4 edition is to be released. |

**Not supplied:** `evidence.md`, `evidence-files`, any `my_*.py` program, `.venv`, `assets`, or `outputs`. The steps below and later lessons explicitly tell you when to create or generate them.

## 2. Open the editor and prepare the environment { #activate-environment }

In VS Code, choose **File → Open Folder** and select **`week04-exercises`**. You should see `requirements.txt` and `week04_common.py` in its file list. Leave the supplied Python files in place. You will create the separate `my_*.py` programs beside them.

You need Python 3.11, your existing Groq key, internet for installation/model/search requests, and Chrome for Topic 16. Run the following commands one line at a time. Use the actual extracted folder path if you did not use the default location.

**Windows — Command Prompt** (not PowerShell):

```bat
cd /d "%USERPROFILE%\agent-course\week04-exercises"
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
dir
python -m pip install -r requirements.txt
python prepare_visuals.py
```

**Mac — Terminal:**

```bash
cd ~/agent-course/week04-exercises
python3.11 -m venv .venv
source .venv/bin/activate
python --version
ls
python -m pip install -r requirements.txt
python prepare_visuals.py
```

**What the supplied `prepare_visuals.py` does:** without an LLM or network, it draws an original fictional venue plan and writes a local practice page. It **creates** `assets/venue.png` and `assets/venue.html`. You do not create those files by hand. Expected terminal output:

```text
Created assets/venue.png and assets/venue.html (no LLM).
```

**Check before continuing:** the terminal shows `(.venv)`, Python is 3.11.x, installation completed, and your file manager shows both files inside the new `assets` folder. Open `assets/venue.png` to confirm that the drawing exists. If installation failed, fix that error before running later programs.

Keep this terminal open. Later **Run: `python filename.py`** instructions use this activated terminal in `week04-exercises`. In a fresh terminal, repeat the `cd` and activation lines above; you do not need to recreate `.venv`. **Do not rerun `prepare_visuals.py` after editing the practice page unless you want to reset it**—it replaces both generated assets.

Selenium may obtain a compatible Chrome driver on the first browser run. For driver/network problems, use Topic 16's troubleshooting section with your instructor. Groq runs ask for the key with hidden input; do not save it in your scripts or notes. Task text, retrieved passages and images used by the agent are sent to Groq.

## 3. Create your evidence file now { #evidence-file }

**`evidence.md` is a student-created Markdown text file. It is not in the ZIP.** It stores your predictions, answers and short excerpts of actual results. Markdown is plain text; use the same code editor, without installing another application. You do not run this file with Python.

1. In your editor, choose **File → New Text File**.
2. Paste the starter headings below.
3. Choose **File → Save As** and save it as **`evidence.md`** directly inside `week04-exercises`, beside `requirements.txt`.
4. Save with **Ctrl + S** or **Command + S**. Confirm the filename is `evidence.md`, not `evidence.md.txt`.
5. In the editor's file list or your file manager, choose **New Folder** and create **`evidence-files`** inside `week04-exercises`. This is also student-created; it will hold copies of generated reports/screenshots that you want to preserve.

```markdown title="evidence.md — create this text file"
# Week 4 evidence

## Topic 14 — RAG
- Baseline: query, actual tool call, passage/source and final answer:
- Challenge answers 1–4:
- Policy-query run: actual result and missing evidence:

## Topic 15 — Batman team
- Explain the supplied roles and source/coordinate contract:
- Explain the supplied specialist description, task and tool/agent wiring:
- One-location handoff: request, actions, observations, returned evidence:
- Full report: sources checked and one recalculated estimate:
- Code-reading answers, checked sources and limitations:
- Optional verifier: design, false-claim test and verdict (or not attempted):

## Topic 16 — Vision and browser
- My image predictions, supported facts and uncertainty:
- Initial image run and step-free-route comparison:
- Direct browser check: before.png versus after.png:
- Agent browser run: actions, screenshot names and supported answer:
- Edited-page run: exact change, prediction, archived results and comparison:

## Topic 17 — Review
- Status for each required checkpoint: complete or incomplete, with reason:
- Answers 1–5:
```

For each later activity, reopen this **existing** file, add your own results under the matching heading, and save it. Copy a short terminal excerpt by selecting/copying it and pasting into the note; do not replace your actual result with a model answer from a collapsed panel. Write “incomplete” with the observed error when a run fails. Model answers explain what evidence should mean; they do not certify your execution.

## 4. Know which files you will create { #student-files }

| Topic | Student-created file | When to create it |
| --- | --- | --- |
| Setup | `evidence.md` and `evidence-files` folder | Now, using the steps above. |
| 14 | `my_rag_continuation.py` | Topic 14's file-creation steps. |
| 15 | `my_batman_tools.py` | Before the direct tool check. |
| 15 | `my_batman.py` | Copy the complete two-agent program supplied in Topic 15. |
| 15, optional | `my_batman_verified.py` | Make a copy of your working team when attempting the verifier extension. |
| 16 | `my_vision.py` | Before the initial-image run. |
| 16 | `my_browser_check.py` | Before the direct browser check. |
| 16 | `my_browser.py` | Before the browser-agent run. |

**Generated outputs — do not create empty stand-ins:** `.venv` comes from environment setup; `assets/venue.png` and `assets/venue.html` come from `prepare_visuals.py`; `before.png` and `after.png` come from `my_browser_check.py`; `outputs/batman-report.html` comes from the report tool; and `outputs/browser-*.png` comes from the browser callback. Output files may not exist until the corresponding step succeeds. A rerun can replace a same-name output; each lesson explains what to copy before comparing runs.

## Before the first agent run { #for-now }

Confirm the supplied helpers, generated assets, your new `evidence.md` and `evidence-files` folder, and activated terminal are ready. The `my_*.py` files are still absent at this point; create them one at a time in their lessons. Read `README.md` as a supplied reference, not as a file you need to write.

For a model error: 401 means check the key; 403/404 means check model access; 429 means stop and wait for available capacity. Do not repeatedly restart the whole team. A printed final answer after a step limit is not completion evidence; inspect the actual tool trace.

**Start:** [14 · Agentic RAG continuation](week-4-retrieval.md).
