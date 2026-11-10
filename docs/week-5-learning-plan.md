# Week 05 · LlamaIndex { #week-5-plan }

**Goal:** build an assistant that searches your documents, uses tools, and passes work through clear steps.

Complete [Week 4](week-4-completion.md) first. This week follows **HF Unit 2.2 in the same order**. Keep your earlier work. Use a new **`week05-exercises`** folder, Python 3.11, your editor and terminal. No notebook or GPU is required. English and Japanese use the same code and exercises.

## Follow this route { #route }

| Order | Lesson | What you will do |
| --- | --- | --- |
| Setup | This page | Install a separate environment and download ten persona descriptions. |
| 18 | [Introduction](week-5-introduction.md) | Distinguish components, tools, agents and workflows. |
| 19 | [LlamaHub](week-5-llamahub.md) | Match an integration package to its Python import; test the model connection. |
| 20 | [Components](week-5-components.md) | Load, split, embed, store, retrieve and query the persona data; inspect evidence. |
| 21 | [Tools](week-5-tools.md) | Make a function tool, a query-engine tool and a local tool collection. |
| Check | [Quiz 1](week-5-quiz-1.md) | Explain components and tools before creating an agent. |
| 22 | [Agents](week-5-agents.md) | Use arithmetic tools, remember Bob, search personas and hand off a task. |
| 23 | [Workflows](week-5-workflows.md) | Connect events and steps, make a bounded loop, draw the flow and share state. |
| Check | [Quiz 2](week-5-quiz-2.md) | Explain agent decisions, events, memory and shared state. |
| Review | [Conclusion and completion](week-5-completion.md) | Show your working files and explain the results. |

The persona search, demo weather, arithmetic, Bob memory and workflow examples follow the [HF unit](https://huggingface.co/learn/agents-course/en/unit2/llama-index/introduction). You will run them as saved Python programs. We keep the classroom Groq connection; no new model-provider account is needed.

## 1. Download and open the new folder { #download }

[Download the Week 5 English/Japanese starter](downloads/week05-llamaindex.zip){ .md-button .md-button--primary }

1. Save the ZIP. On Windows, right-click it and choose **Extract All**. On Mac, double-click it in Finder.
2. Open the extracted folder and find the folder containing `requirements.txt` and `week05_common.py`. On Mac, this is usually the extracted `week05-exercises` folder itself. Windows may add an extra outer folder. Move the folder containing those files into **`agent-course`**, beside your earlier exercise folders. Name it **`week05-exercises`**.
3. Open **`week05-exercises`** with **VS Code → File → Open Folder**. You should see `requirements.txt`, `prepare_personas.py`, `week05_common.py` and `week05_rag.py` together.
4. Keep these supplied helpers. The `my_*.py` files are **not** in the ZIP: you will create them from the lessons, beside the helpers. Read the online lessons or the Markdown copies in `lessons/en` and `lessons/ja`.

| Supplied file | Purpose |
| --- | --- |
| `requirements.txt` | Tested Week 5 packages, separate from smolagents. |
| `prepare_personas.py` | Downloads ten public persona descriptions without an LLM. |
| `week05_common.py` | Loads local settings, connects to Groq and prints tool-call results. |
| `week05_rag.py` | Reopens the local index for later lessons, avoiding repeated setup code. |
| `README.md`, `NOTICE.md`, `HF-LICENSE.txt` | Setup summary, sources and license. |
| `lessons/en`, `lessons/ja` | Matching English and Japanese lesson sequences. |
| `images/huggingface-week05` | Original HF figures used by the lesson copies. Click a figure to open it at full size. |

## 2. Create and activate a separate environment { #environment }

Use **64-bit Python 3.11** on a supported Windows or Mac system. Check that your computer has room for the packages and model files before installing. In the Mac walkthrough, the environment alone used about 1.6 GB; usage varies by computer. Installation includes local embedding libraries and can download large packages. Internet is required for installation, the persona download, the first embedding-model download and Groq requests. Later retrieval and plain workflows run locally. Keep the terminal open after activation.

### Choose the terminal and check Python { #choose-the-terminal-and-check-python }

**Windows in VS Code:** open **Terminal → New Terminal**. If its prompt begins with `PS`, it is PowerShell. Click the arrow beside the terminal’s **+** button and choose **Command Prompt**. For future terminals, use **Ctrl + Shift + P → Terminal: Select Default Profile → Command Prompt**, then open a new terminal. The commands below use Command Prompt. See [VS Code terminal profiles](https://code.visualstudio.com/docs/terminal/profiles).

Check Python before creating the environment:

- **Windows Command Prompt:** run `py -3.11 --version`.
- **Mac Terminal:** run `python3.11 --version`.

Continue when the result is `Python 3.11.x`. If the command is missing or cannot find 3.11, open the instructions below first.

??? help "Python 3.11 is missing"

    **Windows 10/11:** install the **Python install manager** from [python.org](https://www.python.org/downloads/windows/). Close and reopen VS Code so its terminal sees the installation. In a new Command Prompt, run these lines:

    ```bat
    pymanager install 3.11
    py -3.11 --version
    ```

    `pymanager` avoids a conflict with an older `py` launcher. If either command is still missing, follow [Python’s Windows troubleshooting](https://docs.python.org/3/using/windows.html#troubleshooting), or ask your instructor for help with the command and error shown.

    **Mac:** if Homebrew is installed, run:

    ```bash
    brew install python@3.11
    python3.11 --version
    ```

    If `brew` is missing, install it using the instructions at [brew.sh](https://brew.sh/), including the installer’s **Next steps** for your terminal, then run the two lines above. [Homebrew’s Python 3.11 page](https://formulae.brew.sh/formula/python@3.11) lists supported systems. For a managed or unsupported computer, ask your instructor before continuing.

### Install the Week 5 packages { #install-the-week-5-packages }

**Windows — Command Prompt**, one line at a time:

```bat
cd /d "%USERPROFILE%\agent-course\week05-exercises"
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
python -m pip install -r requirements.txt
python -m pip check
python week05_common.py
python prepare_personas.py
```

**Mac — Terminal**, one line at a time:

```bash
cd ~/agent-course/week05-exercises
python3.11 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements.txt
python -m pip check
python week05_common.py
python prepare_personas.py
```

Use your actual folder path if it differs. Check for `(.venv)`, Python `3.11.x`, `No broken requirements found.`, **`Week 5 starter version: 2026-11-10.2`**, and **`Saved 10 persona files in data/ (no LLM, no Groq tokens).`** The version check prints only the helper version; it makes no model request. The download also creates `dataset-source.json`. Open `data/persona_0.txt`; it should describe a Cincinnati art historian. These are profile descriptions, not identified real people. Some source descriptions may be incomplete; do not repair them by guessing.

`prepare_personas.py` obtains the first ten records from the same [HF persona dataset](https://huggingface.co/datasets/dvilasuero/finepersonas-v0.1-tiny) used in HF’s notebook. If the rows service fails or truncates text, it downloads the original dataset file (about 35 MB), verifies it, and reads the same ten complete descriptions. Only those texts are saved; no HF token is needed. It will not overwrite a non-empty `data` folder. Wait for the saved-file message. If downloading stops, follow its printed diagnosis before continuing. First embedding use downloads `BAAI/bge-small-en-v1.5` into `.cache/huggingface` inside this folder. Later runs load the complete cache locally without checking HF. It runs on your CPU and does not use Groq tokens.

In a new terminal, repeat only the folder-change and activation lines. Do not recreate the environment every lesson.

## 3. Create your local settings { #settings }

**Reusing Week 4’s key:** copy only the `GROQ_API_KEY` value into this new file. If you copied the whole `.env`, replace its `GROQ_MODEL` line with the exact line below. Week 4 used a provider prefix such as `groq/`; this week uses the plain Groq model ID. Keep your Week 4 file as it is.

In the editor, create **`.env`** directly in `week05-exercises`, beside `week05_common.py`. Save it as `.env`, not `.env.txt`. Paste this and replace the key placeholder:

```dotenv
GROQ_API_KEY=your_own_groq_api_key
GROQ_MODEL=qwen/qwen3.8-27b
```

The helper explicitly calls `load_dotenv` before reading the settings. Creating the file alone does not make Python read it. Existing terminal environment values take priority. If you previously set `GROQ_MODEL` in this terminal, clear it with `set GROQ_MODEL=` in Windows Command Prompt or `unset GROQ_MODEL` on Mac, then rerun. Keep the key on your computer; do not include `.env` in GitHub, screenshots or your evidence.

The model is listed on [Groq’s model page](https://console.groq.com/docs/models), checked 2026-11-09. It is a preview model; check current availability and your permissions if a run fails. Use the plain model ID shown above. The current helper also removes a leading `groq/` from a copied value, but it cannot update an old model name for you. The programs send prompts and retrieved persona passages to Groq. Use the public sample data for these exercises.

Run model programs one at a time. Each agent run has a six-iteration cap and no automatic API retries. A query tool can make several model requests. If Groq returns **429**, stop and check account limits, credits and the retry interval. Waiting can reset a short rate window; it does not add credits or guarantee success.

## 4. Start an evidence note { #evidence }

Create **`evidence.md`** in the same folder. Paste these headings, then save. Add short actual output and your own explanations after each lesson. This note is not a Python program.

```markdown title="evidence.md"
# Week 5 evidence
## 18 — Components, tools, agents, workflows
## 19 — Integration and model connection
## 20 — Ingestion, retrieval, answer, sources, evaluation
## 21 — Function tool, query tool, ToolSpec and utility tools
## Quiz 1
## 22 — Tool calls, Bob memory, RAG and handoff
## 23 — Events, loop, flow diagram and shared counter
## Quiz 2
## Completion — complete/incomplete and limitations
```

For every later file: **File → New Text File → Save As**, save the exact `.py` name beside the helpers, paste the blocks in order and save with **Ctrl + S** or **Command + S**. Do not put your programs inside `.venv` or `lessons`.

**Work on one program at a time.** Do not create all the files in advance. Each lesson ends with a short file/result checklist. Keep earlier programs because later examples import them. There are 17 required small programs and one optional evaluator across the whole week; you do not need to understand or build them all at setup.

**Setup checkpoint:** your folder should contain the supplied helpers, `.venv`, `.env`, `evidence.md`, `dataset-source.json`, and `data/persona_0.txt` through `data/persona_9.txt`. No `my_*.py` file is required yet. The first one is created in the LlamaHub lesson.

**Start:** [18 · Introduction to LlamaIndex](week-5-introduction.md).

## Help when needed { #help }

If a command stops, open the matching help below before continuing.

### Read the first-run messages { #first-run-messages }

??? help "Installation and model-loading messages"

    | Message or stage | What to do |
    | --- | --- |
    | Many `Collecting`, `Downloading`, or `Installing` lines | Let installation finish. Wait until your command prompt returns before entering the next command. |
    | `No broken requirements found.` | The package check passed. Continue to the data download. |
    | `Downloading ten public persona records...` | Wait for `Saved 10 persona files...` before running ingestion. A fallback message means the original file is being tried; wait for the saved-file message. |
    | `No complete model cache...` or `Loading weights` | The first complete model download needs internet. Later, `Loaded the cached CPU embedding model locally` means HF was not contacted. Wait for the lesson’s completion output. |
    | A warning suggesting `HF_TOKEN` during a model download | This public model needs no token. Once the cache is complete, the helper loads it locally. |
    | pip says `huggingface-hub ... does not provide the extra 'inference'` | The embedding adapter requests an old optional extra that the installed Hub package no longer declares. This warning alone did not prevent our local embedding checks. Wait for installation to finish, then check `No broken requirements found.` and the lesson’s actual output. Keep the pinned packages. |
    | PyTorch says redirects are unsupported on macOS | This library message alone did not prevent the tested scripts from completing. Check the expected result below it. |
    | `Run incomplete`, a traceback, or a nonzero exit | Read the error and use the troubleshooting table below. Do not mark the activity complete. |


### If a step stops { #troubleshooting }

??? help "Find the error and its next action"

    | What you see | Next action |
    | --- | --- |
    | `python: can't open file` | Check that the terminal is in `week05-exercises`, that you saved the named file beside the helpers, and that its name is not `.py.txt`. |
    | Wrong or missing starter version | Replace only `week05_common.py` with the copy from the current Week 5 ZIP. Keep your `.env`, data and student programs. Rerun `python week05_common.py`. |
    | `ModuleNotFoundError` | Activate this week’s `.venv` using the instructions above, then rerun `python -m pip install -r requirements.txt`. Do not install into Week 4. |
    | Dataset download stops | HTTP 503 means a server failure: try later. For a connection timeout, check the network and retry. A checksum failure means the original file was incomplete or changed. No persona files are written on these failures; keep the message for your instructor. |
    | Missing `persona_*.txt` | Run `python prepare_personas.py`. If `data` is incomplete and the downloader refuses to overwrite it, preserve it by renaming it `data-backup`, then rerun the download. |
    | The embedding model cannot finish loading | Check internet access and free disk space, then rerun the same program. The public download can resume; a failed download does not mean the model is private. If it keeps failing, close the programs, rename `.cache/huggingface` to `.cache/huggingface-backup`, and retry when the connection is stable. Keep your `data` and source files. This download does not use Groq tokens. |
    | The index is missing or incomplete | Finish the ten-file download, then run `python my_ingest.py`. If a partial database exists, close its programs, rename `alfred_chroma_db` as a backup, and run ingestion again. |
    | Local `NameError`, `TypeError` or `ValueError` | Use the file name and line number printed by the helper. Compare that part with the matching lesson block; check names, quotes and indentation. |
    | Groq 401 | Check the key in your local `.env`; do not print it or send it in evidence. |
    | Groq 403/404 | Check the Week 5 model ID and your account’s model permissions. If you copied Week 4 settings, replace the model line using step 3. |
    | Groq 413 | Keep the small dataset and short task; waiting does not shrink an oversized request. |
    | Groq 429 | Stop and follow the model-limit guidance in [step 3](#settings). |
    | `flow.html` is blank | Follow the [drawing check in lesson 23](week-5-workflows.md#draw). The current helper embeds the graph libraries; internet is not required to view the saved diagram. |

    Fix the current checkpoint before continuing to a program that depends on it. If you need help, record the filename, command and error category without including `.env` or your key.
