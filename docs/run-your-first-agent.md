# Download and run the first-agent template

<div class="template-download" markdown>

<p class="template-download__label">Step 04 · Starter files</p>

**Download the complete agent template**

One ZIP with all the Python files, tools, instructions, and library requirements. Use this after the three dummy exercises.

[Download agent template (.zip)](downloads/groq-agent-starter.zip){ .md-button .md-button--primary .template-download__button download="groq-agent-starter.zip" }

**Next:** Extract the ZIP, then [follow Step 3 below](#3-download-the-groq-starter). No API key is included; you will enter your own Groq key when starting the app.

</div>

> **Why local setup?** The original tutorial's Space duplication step was blocked in our setup: CPU Basic was disabled, ZeroGPU asked for PRO, and custom hardware was paid. An API token does not unlock hosting. This guide uses a local app and Groq for model calls, with local lessons, time and search activities, and two original quick quizzes. See the [course introduction](index.md).

**When to use this page:** Finish the [three dummy stages](dummy-agent-local.md) first. You will now receive the full template and let CodeAgent manage the model/action/observation loop. Reuse your existing Groq key; create a separate virtual environment for this template. If Python and your account are ready, begin at Step 3. Reuse the same Groq key at Step 6; you do not need to create another key. Before switching from the dummy exercise, run `deactivate`, then create and activate the template’s separate environment as shown below.

Follow this guide on Windows or Mac to run our Groq adaptation of the Hugging Face Agents Course starter app.

If this is your first Python project, read [Before you start](before-you-start.md). Follow only your operating system's commands; steps labelled for either system apply to everyone.

Your computer runs the app and its tools. A remote large language model (LLM) generates responses, so an internet connection is required. You are running an existing model, not training one.

You do not need a Hugging Face token for this version's chat. Groq provides the model API. Local lessons supply the instructions, and only the two HF quick quizzes remain in the course route. The final quiz and certification are excluded. Image generation has been removed.

## 1. Create your Groq account

1. Open [Groq Console](https://console.groq.com).
2. Sign up or sign in with your own account and complete any verification requested.
3. Stay on the **Free** plan for this exercise. A paid upgrade is not a setup requirement.
4. Key creation is explained in Step 6 below.

Free access has request and token limits. A multi-step agent can make several calls for one message. Check your account's Limits page; creating extra keys does not increase an organization's quota. See [Groq's current limits](https://console.groq.com/docs/rate-limits).

## 2. Install Python 3.11

Python runs the app. Install it only if Python 3.11 is not already available. The ZIP route does not require Git.

### Windows

Open **Command Prompt**, then run each command separately:

```bat
winget install --exact --id Python.Python.3.11
```

Accept the installer prompts, close and reopen Command Prompt, then check:

```bat
py -3.11 --version
```

If `winget` is unavailable, open the [Python 3.11.9 release page](https://www.python.org/downloads/release/python-3119/), scroll to **Files**, and download the **Windows installer (64-bit)** for an x64 PC. Run it, enable **Add python.exe to PATH** and the Python launcher, finish installation, then reopen Command Prompt and retry `py -3.11 --version`. Use **Command Prompt**, not PowerShell, for this guide's Windows commands.

### Mac

Open **Terminal**. If Homebrew is installed, run:

```bash
brew install python@3.11
```

If Homebrew is missing, follow [its installation instructions](https://brew.sh), including the final setup instructions, then retry.

Check the installations:

```bash
python3.11 --version
```

**Checkpoint:** You see Python 3.11.x. On Mac, `python3` may still point to an older version; this is fine. Use `python3.11` below.

## 3. Download the Groq starter

[Download agent template (.zip)](downloads/groq-agent-starter.zip){ .md-button .md-button--primary .template-download__button download="groq-agent-starter.zip" }

1. Click **Download agent template (.zip)** above. If you already downloaded it from the top of this page, use that same ZIP.
2. Extract the ZIP: double-click it on Mac, or right-click and choose **Extract All** on Windows.
3. Locate the extracted folder containing `app.py`, `Gradio_UI.py`, `requirements.txt`, `prompts.yaml`, and `tools`. Its name is `First_agent_template`; it also includes `STUDENT_TASKS.md` with the tasks you will complete.
4. Create an `agent-course` folder inside your home/user folder and move `First_agent_template` into it. If a folder of that name already exists, keep a backup before replacing it.
5. Open a terminal and enter the project folder:

**Windows — Command Prompt**

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
```

**Mac — Terminal**

```bash
cd ~/agent-course/First_agent_template
```

Do not work inside an unopened ZIP. If extraction created two nested folders with the same name, use the inner folder containing `app.py`.

**Checkpoint:** Run `dir` on Windows or `ls` on Mac. Confirm `app.py` and `requirements.txt` are listed. This ZIP contains code only, not a virtual environment or anyone's API key.

## 4. Create a virtual environment

This keeps the project's libraries separate from other Python projects.

### Windows

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
```

### Mac

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

**Checkpoint:** The prompt starts with `(.venv)` and Python reports version 3.11.x. Keep using this terminal window.

## 5. Install the libraries

On either operating system:

```bash
python -m pip install -r requirements.txt
```

Wait for installation to finish and the prompt to return. Download progress bars are normal.

**Checkpoint:** There is no final `ERROR` message. You may see `Successfully installed` or `Requirement already satisfied`. Do not enter the next command while installation is still running.

Use the `requirements.txt` included in the Groq ZIP. It includes the `openai` client library, used here to connect to Groq through its compatible API; you do not need an OpenAI account.

## 6. Create your Groq API key

### A. Open the key page

1. In your browser, sign in to [Groq Console](https://console.groq.com).
2. Open **API Keys** in the console navigation, or use the [direct API Keys link](https://console.groq.com/keys).
3. Click **Create API Key**.
4. Enter a descriptive name such as `agents-course` in the name field. If an expiration choice is offered, choose one that covers your course sessions.
5. Confirm creation using the dialog's create/submit button.
6. Copy the generated secret key and keep it in a password manager so you can retrieve it at startup. Do not share it with classmates or paste it into this guide, source code, or chat.

The name `agents-course` is only a label. The generated secret value is the actual key. The console's labels may vary; Groq's [official quickstart](https://console.groq.com/docs/quickstart) also links to key creation.

**Checkpoint:** You have your own Groq key ready. Creating a key does not choose a model or prove that a model request will succeed.

### B. Understand how the app uses it

The starter asks for your key when you run `python app.py` in Step 8. Do not run a Hugging Face login or `whoami` command: those check a different service and do not validate Groq access.

The key is hidden while you paste and is held in memory for that running app. It is not saved by the app. Unless you separately configured `GROQ_API_KEY`, you will paste it again each time you restart.

### C. Model selection is already configured

The supplied `app.py` selects:

```python
model_id="qwen/qwen3.8-27b",
api_base="https://api.groq.com/openai/v1",
```

These lines select the model and Groq endpoint. The app also sets `reasoning_effort="none"` so this model returns its code-agent response without a reasoning preamble. Keep them unchanged for the first test. Do not replace the key prompt with a literal key in the code.

### D. Verification happens with a real response

This version does not print a username after key creation. In Step 9, a successful answer from the model verifies that the key, account access, endpoint, and model worked for that request. Opening the chat page alone is not that verification.

If a key is exposed or lost, manage/revoke it on the [Groq API Keys page](https://console.groq.com/keys), create a replacement if needed, and restart the app with the new key.

## 7. Confirm local-only sharing

The Groq starter already uses `share=False` in `Gradio_UI.py` and binds the app to `127.0.0.1`. No edit is required.

If checking an older copy, find `demo.launch` in `Gradio_UI.py` and confirm it contains `share=False`. A public link would allow other people to send requests using the running app's Groq credentials.

## 8. Start the agent

```bash
python app.py
```

Terminal first asks:

```text
Paste your Groq API key (hidden):
```

Paste your key and press Enter/Return. Nothing appears while pasting; that is normal. The app then prints:

```text
Using Groq: qwen/qwen3.8-27b
```

This names the configured model; it does not yet mean the key was accepted by Groq. If no key prompt appears, the app found `GROQ_API_KEY` in its environment. Never print that variable to share it.

The local `app.py` configures the model and starts the agent interface.

Wait for output similar to:

```text
Running on local URL: http://127.0.0.1:7860
```

Open the exact address shown in your browser. Keep the terminal running.

The address goes in your browser's address bar, not the agent chat. If the terminal prints a different port, use that port. The command will not return to its normal prompt while the app is running; that is expected.

## 9. Test the connection to the LLM

Send:

> What is 12 multiplied by 8?

Look for a final answer containing **96**. You may also see generated Python code and a `python_interpreter` step.

The request flows from your browser to the local app, then to a remote LLM. Your app executes the generated code and displays the result. The configured model is `qwen/qwen3.8-27b`, served by Groq; availability may change.

Opening the page confirms the interface works. Receiving a model-generated answer also tests the remote model connection. The starter app has limited tools; do not assume it can search the web.

## 10. Understand token usage

| Term | Meaning |
| --- | --- |
| Access token / API key | Your reusable authentication credential. |
| Input tokens | Pieces of text sent to the model, including instructions and conversation context. |
| Output tokens | Pieces of text generated by the model. |

The app reuses your key while it is running. After stopping and restarting, it asks again unless `GROQ_API_KEY` is configured. Input/output token counts describe model usage, not credentials.

## 11. Stop and restart

To stop the app, click the terminal and press **Control + C**.

To restart another day, open a new terminal and run:

### Windows

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
.venv\Scripts\activate.bat
python app.py
```

### Mac

```bash
cd ~/agent-course/First_agent_template
source .venv/bin/activate
python app.py
```

You do not need to reinstall libraries. Paste your Groq key again when prompted, then open the printed local URL.

## Troubleshooting

### Model connection problems

| Problem | Next step |
| --- | --- |
| Python is the wrong version | Activate the Python 3.11 environment from Step 4. |
| `app.py` or `requirements.txt` cannot be found | Enter the extracted `First_agent_template` folder. |
| `ModuleNotFoundError: openai` | Activate `.venv` and rerun Step 5. |
| No Groq key entered | Restart and paste your key into the hidden prompt. |
| 400 / `tool_use_failed` / “Tool choice is none” | Use the current starter's `app.py` and `prompts.yaml`, stop the old process, and restart. It now selects Qwen rather than GPT-OSS and explicitly requests Python text. If it repeats, check [Groq’s tool-call behavior](https://console.groq.com/docs/tool-use/local-tool-calling) and the model ID against the current download. Do not enable native tools blindly: this exercise expects Python text. |
| 401 / invalid API key | Use the full Groq key, not its label or an HF token. Check it has not expired or been revoked. |
| 403 / access denied | Check your Groq account/project's model access and any organization restrictions. |
| 429 / Request too large | Read the limit named in the terminal. For output tokens, lower `max_tokens` in `app.py` (the current starter uses 512), save, and restart. For input tokens, restart to clear chat history or shorten the prompt. Waiting alone does not fix an oversized request. |
| 429 / rate limit (usage exhausted) | Follow the retry interval. Free-tier limits apply to both requests and tokens. Avoid rapid repeated messages. |
| 404 / model unavailable | Compare `model_id` with [Groq’s supported models](https://console.groq.com/docs/models) and check your console’s model permissions. Model IDs must match exactly. |
| HF router 402 / no credits | You are still running the old HF model connection. Stop that app and use the Groq starter; buying HF credits is not required for this version. |
| Old `NoneType` token-count crash | Confirm you are using the updated `Gradio_UI.py` from the starter ZIP. |
| Page opens but chat fails | Read the model error in the terminal; the page alone does not test API access. |
| Connection error or timeout | Check internet access and Groq service availability, then retry once. The current starter uses a 30-second timeout per attempt and at most two automatic retries; do not repeatedly submit messages while it is waiting. |
| Browser cannot connect | Keep the app running and use its printed local URL. |
| Port already in use | Stop the older app process before launching again. |

For help, share your operating system, command, and final error lines. Exclude credentials.

### Common editing mistakes

| Message or symptom | What to check |
| --- | --- |
| `IndentationError` | Restore the leading spaces around your edit. Use the original file or backup as a reference. |
| `SyntaxError` | Check for a missing comma, quote, square bracket, or parenthesis in the edited lines. |
| `NameError` after adding a tool | Check the function name's spelling, that it is defined above the agent, and that the file was saved. |
| File appears to be `app.py.txt` | Save from a code editor as `app.py`; do not add `.txt`. |
| Changes have no effect | Save the file, stop and restart the app, then refresh its browser page. |
| Terminal shows `>>>` | Type `exit()` to return to the command prompt before running shell commands. |

**Completion check:** You can start the app, obtain an LLM response, explain where the model runs, and stop the app.

## Validation status

On 12 October 2026, a separate Mac test folder with new Python 3.11 environments passed dependency installation, all three dummy stages against Groq, browser chat, timezone lookup, and individual live web search after the search adapter was updated. A later combined run completed a final answer, but search returned no results, so it did not pass the search-evidence checkpoint. The starter now requests 512 output tokens per completion and allows two automatic retries after an account rejected the former 2,096-token budget. These are tested settings, not a guarantee for every account. Windows installation, account creation, and installing Python on a machine without Python remain untested. Search is intermittent and model usage limits still apply. Use the checkpoints to validate your own installation. Some dependencies remain unpinned.

**Next:** [Understand smolagents and what the template does](understand-the-template.md), then [build your agent’s tools](first-agent-practical.md).
