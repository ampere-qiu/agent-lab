# Download and run the first-agent template { #download-and-run-the-first-agent-template }

Begin Week 2 after finishing the [three dummy stages](dummy-agent-local.md) first. Then use this page to download the complete template, prepare its own environment, and start the app. CodeAgent will manage the model/action/observation loop that you assembled manually in the dummy exercise.

Your earlier [basic setup](prepare-your-computer.md) already provided Python 3.11 and your Groq key. This page continues from that setup. Your computer runs the app and tools; Groq provides the remote model, so you still need an internet connection.

Follow only the commands for your operating system. For help with terminals, folders, and editing, see [Before you start](before-you-start.md).

## 1. Have your Groq API key ready { #1-create-your-groq-account }

Use the same Groq API key you prepared during [basic setup](prepare-your-computer.md#4-create-your-groq-api-key). Have it ready to paste into the hidden terminal prompt when you start the app in Step 8. You do not need to create another account or key.

If you have not prepared your key yet, complete the linked setup step before continuing.

## 2. Use your existing Python installation { #2-install-python-311 }

Use Python 3.11 from basic setup. The new environment in Step 4 will check its version. If you have not installed it yet, complete [the Python setup step](prepare-your-computer.md#1-install-python-311) before continuing.

If your dummy exercise is still running, stop it with **Control + C**. If its virtual environment is active (the prompt shows `(.venv)`), run `deactivate` before switching to the template folder.

## 3. Download the agent template { #3-download-the-groq-starter }

<div class="template-download" markdown>

<p class="template-download__label">Complete agent template</p>

One ZIP containing `app.py`, the interface, tools, instructions, and library requirements. “Groq starter” and “agent template” refer to this same download. It includes no API key or virtual environment.

[Download agent template (.zip)](downloads/groq-agent-starter.zip){ .md-button .md-button--primary .template-download__button download="groq-agent-starter.zip" }

</div>

1. Click **Download agent template (.zip)** above.
2. Extract the ZIP: double-click it on Mac, or right-click and choose **Extract All** on Windows.
3. Locate the extracted folder containing `app.py`, `Gradio_UI.py`, `requirements.txt`, `prompts.yaml`, and `tools`. Its name is `First_agent_template`; it also includes `STUDENT_TASKS.md` with the tasks you will complete.
4. Move `First_agent_template` into the `agent-course` folder you created during basic setup. If a `First_agent_template` folder already exists, keep a backup before replacing it.
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

**Checkpoint:** Run `dir` on Windows or `ls` on Mac. Confirm `app.py` and `requirements.txt` are listed.

## 4. Create a virtual environment { #4-create-a-virtual-environment }

Create a new environment inside `First_agent_template` so its libraries stay separate from the dummy exercise. Run these commands once, after entering the folder in Step 3.

### Windows { #windows }

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
```

### Mac { #mac }

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

**Checkpoint:** The prompt starts with `(.venv)` and Python reports version 3.11.x. Keep using this terminal window.

## 5. Install the libraries { #5-install-the-libraries }

On either operating system:

```bash
python -m pip install -r requirements.txt
```

Wait for installation to finish and the prompt to return. Download progress bars are normal.

**Checkpoint:** There is no final `ERROR` message. You may see `Successfully installed` or `Requirement already satisfied`. Do not enter the next command while installation is still running.

Use the `requirements.txt` included in the Groq ZIP. It includes the `openai` client library, used here to connect to Groq through its compatible API; you do not need an OpenAI account.

## 6. Keep the supplied model settings { #6-create-your-groq-api-key }

The template already connects to Groq using these settings in `app.py`:

```python
model_id="qwen/qwen3.8-27b",
api_base="https://api.groq.com/openai/v1",
```

It also sets `reasoning_effort="none"` for code-agent responses. Leave these settings unchanged for the first run. Keep your API key out of the source code; the app will ask for it at startup.

## 7. Confirm local-only sharing { #7-confirm-local-only-sharing }

The Groq starter already uses `share=False` in `Gradio_UI.py` and binds the app to `127.0.0.1`. No edit is required.

If checking an older copy, find `demo.launch` in `Gradio_UI.py` and confirm it contains `share=False`. A public link would allow other people to send requests using the running app's Groq credentials.

## 8. Start the agent { #8-start-the-agent }

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

The key stays in memory while the app runs; it is not saved. If you separately configured `GROQ_API_KEY`, the app uses that value instead of prompting. Never print or share it.

Wait for output similar to:

```text
Running on local URL: http://127.0.0.1:7860
```

Open the exact address shown in your browser. Keep the terminal running.

The address goes in your browser's address bar, not the agent chat. If the terminal prints a different port, use that port. The command will not return to its normal prompt while the app is running; that is expected.

## 9. Test the connection to the LLM { #9-test-the-connection-to-the-llm }

Send:

> What is 12 multiplied by 8?

Look for a final answer containing **96**. You may also see generated Python code and a `python_interpreter` step.

**Checkpoint:** A model-generated answer confirms that your key, account access, endpoint, and model worked for this request. Opening the chat page alone only checks the interface. If the answer fails, use the troubleshooting table below.

The download includes working time and search implementations, but only `final_answer` is registered initially. You will test and register the two supplied tools in the [tools practical](first-agent-practical.md). Until then, the agent cannot use the supplied `web_search` tool. It may still answer from model knowledge or produce a URL; neither proves that it searched.

## 10. Check your usage limits { #10-understand-token-usage }

A single chat message can trigger several model requests. Check [Groq's usage limits](https://console.groq.com/docs/rate-limits) and avoid rapid repeated submissions. API keys authenticate requests; input and output tokens measure the text used. See the [template explanation](understand-the-template.md#the-model-connection) for the output budget and request settings.

## 11. Stop and restart { #11-stop-and-restart }

To stop the app, click the terminal and press **Control + C**.

To restart another day, open a new terminal and run:

### Windows { #windows_1 }

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
.venv\Scripts\activate.bat
python app.py
```

### Mac { #mac_1 }

```bash
cd ~/agent-course/First_agent_template
source .venv/bin/activate
python app.py
```

You do not need to reinstall libraries. Paste your Groq key again when prompted, then open the printed local URL.

## Troubleshooting { #troubleshooting }

### Model connection problems { #model-connection-problems }

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

### Common editing mistakes { #common-editing-mistakes }

| Message or symptom | What to check |
| --- | --- |
| `IndentationError` | Restore the leading spaces around your edit. Use the original file or backup as a reference. |
| `SyntaxError` | Check for a missing comma, quote, square bracket, or parenthesis in the edited lines. |
| `NameError` after adding a tool | Check the function name's spelling, that it is defined above the agent, and that the file was saved. |
| File appears to be `app.py.txt` | Save from a code editor as `app.py`; do not add `.txt`. |
| Changes have no effect | Save the file, stop and restart the app, then refresh its browser page. |
| Terminal shows `>>>` | Type `exit()` to return to the command prompt before running shell commands. |

**Completion check:** You can start the app, obtain an LLM response, explain where the model runs, and stop the app.

**Next:** [Understand smolagents and what the template does](understand-the-template.md), then [build your agent’s tools](first-agent-practical.md).
