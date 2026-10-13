# Prepare your computer

Start here before the lessons and Dummy Agent exercise. You only need Python and a Groq key at this stage. You will download the full agent template **after** the three dummy stages.

## 1. Install Python 3.11

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

## 2. Create a folder for the dummy exercise

Open your terminal and run the commands for your operating system, one at a time.

### Windows — Command Prompt

```bat
mkdir "%USERPROFILE%\agent-course\dummy-agent"
cd /d "%USERPROFILE%\agent-course\dummy-agent"
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python --version
```

### Mac — Terminal

```bash
mkdir -p ~/agent-course/dummy-agent
cd ~/agent-course/dummy-agent
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

If the folder already exists, enter it instead of creating it again. A virtual environment only needs creating once.

**Checkpoint:** Your terminal shows `(.venv)` and Python 3.11.x. Keep this window open.

## 3. Install the model client

On either system:

```bash
python -m pip install "openai>=1.0,<3"
```

Wait for the normal terminal prompt to return without a final error. The library connects to Groq's compatible API; you do not need an OpenAI account.

## 4. Create your Groq API key

Sign up or sign in to Groq Console using your own account. The free plan has usage limits; see [Groq's limits](https://console.groq.com/docs/rate-limits).

### A. Open the key page

1. In your browser, sign in to [Groq Console](https://console.groq.com).
2. Open **API Keys** in the console navigation, or use the [direct API Keys link](https://console.groq.com/keys).
3. Click **Create API Key**.
4. Enter a descriptive name such as `agents-course` in the name field. If an expiration choice is offered, choose one that covers your course sessions.
5. Confirm creation using the dialog's create/submit button.
6. Copy the generated secret key and keep it in a password manager so you can retrieve it at startup. Do not share it with classmates or paste it into this guide, source code, or chat.

The name `agents-course` is only a label. The generated secret value is the actual key. The console's labels may vary; Groq's [official quickstart](https://console.groq.com/docs/quickstart) also links to key creation.

**Checkpoint:** You have your own Groq key ready. Creating a key does not choose a model or prove that a model request will succeed.

The dummy script will ask you to paste this key into a hidden terminal prompt. The full agent will use the same key later. Do not put it in your Python files.

## 5. Continue to the lessons

Follow the [lessons and quick quizzes](unit-1-walkthrough.md), then the [three dummy stages](dummy-agent-local.md). At this point you do **not** need `app.py`, Gradio, or the full agent ZIP.

## Restart the dummy exercise another day

On Windows:

```bat
cd /d "%USERPROFILE%\agent-course\dummy-agent"
.venv\Scripts\activate.bat
```

On Mac:

```bash
cd ~/agent-course/dummy-agent
source .venv/bin/activate
```

Run `python dummy_agent.py` after you have created that file during the exercise. Paste your key when prompted. Output appears in the terminal, not a browser chat.
