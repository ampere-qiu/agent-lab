# Week 04 · smolagents Part 2 { #week-4-preview }

**Objective:** review retrieval, build a team of agents, and use images and screenshots as evidence.

**Before starting:** complete [Week 03](week-3-learning-plan.md). Keep that work in `First_agent_template`; Week 4 uses a **separate `week04-exercises` folder**. Read the lessons here, write your Python files in your code editor, and run them in your terminal.

## Learning route { #planned-topics }

| Topic | Objective |
| --- | --- |
| [14 · Week 3 RAG understanding check](week-4-retrieval.md) | Check retrieval evidence; return to Week 3 for RAG coding. |
| [15 · Multi-agent systems & Batman exercise](week-4-batman.md) | Create and connect a manager and web specialist. |
| [16 · Vision & Browser Agents](week-4-vision-browser.md) | Build agents that use images and fresh screenshots. |
| [17 · Completion checks](week-4-completion.md) | Explain your code and verify its results. |

**Note:** all topics are required. Adding an extra agent in Topic 15 is optional.

## 1. Download and locate the supplied files { #exercise-files }

[Download all Week 04 lessons and support files](downloads/week04-smolagents-part2.zip){ .md-button .md-button--primary }

The [Batman download](downloads/week4_batman_guided_student.zip) and [Vision & Browser download](downloads/week4_vision_browser_student.zip) contain the same complete pack. **Download and extract only one ZIP.**

1. Save the ZIP, usually in **Downloads**.
2. **Windows:** right-click → **Extract All** → **Extract**. **Mac:** double-click it in Finder.
3. Open the extracted folder named **`week04-exercises`**. If extraction created an outer folder, open the inner `week04-exercises` folder. You are in the right place when `requirements.txt` and `week04_common.py` appear together.
4. Move this whole folder into your existing **`agent-course`** folder, beside `First_agent_template`. The default location is `%USERPROFILE%\agent-course\week04-exercises` on Windows or `~/agent-course/week04-exercises` on Mac. If your course folder is elsewhere, use that location in the commands below.

**Already started Week 4?** Save a copy of your work before extracting the latest ZIP into a fresh folder. Use the helper files from that download together with the code in these lessons.

**Already supplied in the ZIP — open these existing files; do not create replacements:**

| Supplied item | Purpose |
| --- | --- |
| `README.md`, `NOTICE.md`, `HF-LICENSE.txt` | Instructions, source/adaptation notes and the HF license. |
| `requirements.txt` | Package installation list. |
| `week04_common.py` | Connects to Groq and prints agent results in the terminal. |
| `week04_search.py` | Searches the web and reads short page excerpts within the research limits. |
| `week04_tools.py` | Cargo estimate and HTML report writer. |
| `week04_browser.py` | Local browser tools and screenshot callback. |
| `prepare_visuals.py` | A supplied program that generates the practice image/page. |
| `lessons/en`, `lessons/ja` | English and Japanese lessons with the original credited HF figures. |

**Files you will add:** create `evidence.md`, the `evidence-files` folder and your `my_*.py` programs as you reach their instructions. Setup creates `.venv` and `assets`; later runs create `outputs`.

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

Selenium may obtain a compatible Chrome driver on the first browser run. For driver or network errors, start with [Topic 16’s troubleshooting table](week-4-vision-browser.md#credit). The supplied helper asks for the key with hidden input; the local `.env` option and its loading step are explained below. Do not save keys in scripts or evidence notes. Task text, retrieved passages and images used by the agent are sent to Groq.

### Local settings: create `.env`

In your editor, create **`.env`** beside `week04_common.py` inside **`week04-exercises`**. Save it as `.env`, not `.env.txt`. Paste these two lines and replace only the key placeholder with your own key:

```dotenv
GROQ_API_KEY=your_own_groq_api_key
GROQ_MODEL=qwen/qwen3.8-27b
```

Keep this file on your computer. Never upload it to GitHub, add it to evidence, or show it in screenshots. The model ID is listed in [Groq’s supported models](https://console.groq.com/docs/models) (checked 2026-11-04); it is a preview model, so check that page and your account access if it changes. Use the plain ID here, without an extra `groq/` prefix.

**Creating `.env` alone does not load it into Python.** Step 4A of the Batman lesson calls `load_dotenv(Path(__file__).with_name(".env"), override=False)` before reading the settings. Existing terminal environment values take priority; remove an old terminal value or open a fresh terminal if it selects the wrong model/key. Do not print the key to check it.

The supplied `week04_common.py` does not read `.env`: it checks the terminal environment, then asks for the key with hidden input, and uses a fixed model ID. Leave that helper unchanged. The Batman code below replaces only its model construction in your own `my_batman.py`, keeps hidden input as a fallback when the key is absent, and reads `GROQ_MODEL`. For Topic 16, the unchanged examples still use the supplied helper and its hidden-key prompt/fixed model; a `.env` file alone does not change them.

**Install the additions after the ZIP requirements**, in the activated terminal above:

```bash
python -m pip install "smolagents[litellm]==1.13.0" "ddgs==9.16.0" "python-dotenv>=1.0,<2"
python -m pip check
```

This adds support for the current search wrapper, `.env` loading and LiteLLM integration while keeping the course’s smolagents version. Do not use the older `duckduckgo_search` import or `DuckDuckGoSearchTool` in your new Batman file. If you cloned the GitHub repository instead of using the ZIP, run `python -m pip install -r requirements.txt` **from the repository root**; that root list includes the Week 4 starter list and these additions. The ZIP’s `requirements.txt` is a different file and stays unchanged. Continue reading these online pages for the updated steps; the lessons inside the unchanged ZIP are older.

## 3. Create your evidence file now { #evidence-file }

**Create a text file named `evidence.md` to keep your predictions, answers and short excerpts from your results.** Markdown is plain text, so you can use your code editor. The file is not included in the ZIP and is not a Python program.

1. In your editor, choose **File → New Text File**.
2. Paste the starter headings below.
3. Choose **File → Save As** and save it as **`evidence.md`** directly inside `week04-exercises`, beside `requirements.txt`.
4. Save with **Ctrl + S** or **Command + S**. Confirm the filename is `evidence.md`, not `evidence.md.txt`.
5. In the editor's file list or your file manager, choose **New Folder** and create **`evidence-files`** inside `week04-exercises`. Use this folder to keep copies of reports and screenshots for comparison.

```markdown title="evidence.md — create this text file"
# Week 4 evidence

## Topic 14 — Week 3 RAG review
- Evidence used: Week 3 run or provided example:
- Answers 1–5:

## Topic 15 — Batman team
- What each agent does and what evidence it returns:
- Build checks A–D: agent count, tools and managed-agent connection:
- One-location handoff: request, actions, observations, returned evidence:
- Full report: sources checked and one recalculated estimate:
- Code-reading answers, checked sources and limitations:
- Optional verifier: design, false-claim test and verdict (or not attempted):

## Topic 16 — Vision and browser
- My image predictions, supported facts and uncertainty:
- How each agent receives its image or screenshot:
- Initial image run and step-free-route comparison:
- Direct browser check: before.png versus after.png:
- Agent browser run: actions, screenshot names and supported answer:
- Edited-page run: exact change, prediction, archived results and comparison:

## Topic 17 — Review
- Status for each required checkpoint: complete or incomplete, with reason:
- Answers 1–5:
```

As you work, add your answers and results under the matching heading. Copy short excerpts from the terminal and note any errors. Try the questions before opening their answers, then use the answers to check your reasoning.

## 4. Know which files you will create { #student-files }

| Topic | File to create | When to create it |
| --- | --- | --- |
| Setup | `evidence.md` and `evidence-files` folder | Now, using the steps above. |
| 14 | No new Python file | Use Week 3 output or the provided example for the quiz. |
| 15 | `my_batman_tools.py` | Before the direct tool check. |
| 15 | `my_batman.py` | Follow steps 4A–4D to create the two agents and their tasks. |
| 15, optional | `my_batman_verified.py` | Make a copy of your working team when attempting the verifier extension. |
| 16 | `my_vision.py` | Follow B1–B3 to load the image, create the agent and add its task. |
| 16 | `my_browser_check.py` | Before the direct browser check. |
| 16 | `my_browser.py` | Follow D1–D3 to create and run the browser agent. |

**Files Python creates:** `.venv` comes from environment setup; `assets/venue.png` and `assets/venue.html` come from `prepare_visuals.py`; `before.png` and `after.png` come from `my_browser_check.py`; `outputs/batman-report.html` comes from the report tool; and `outputs/browser-*.png` comes from the browser callback. Output files may not exist until the corresponding step succeeds. A rerun can replace a same-name output; each lesson explains what to copy before comparing runs.

## Before the first agent run { #for-now }

Confirm the supplied helpers, generated assets, your new `evidence.md` and `evidence-files` folder, and activated terminal are ready. The `my_*.py` files are still absent at this point; create them one at a time in their lessons. You can also find a summary of the setup in the supplied `README.md`.

For a model error: 401 means check the key; 403/404 means check model access; 429 means check your account limits and use the bounded waiting guidance in Topic 15. Waiting does not add credits or guarantee success. Do not repeatedly restart the whole team. A printed final answer after a step limit is not completion evidence; inspect the actual tool trace.

**Start:** [14 · Check your Week 3 RAG understanding](week-4-retrieval.md).
