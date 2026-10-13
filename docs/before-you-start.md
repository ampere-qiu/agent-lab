# Before you start

This walkthrough explains setup from the beginning. The later practical expects you to recognize a Python function, its arguments, and its return value. For a refresher, read the [Python guide to defining functions](https://docs.python.org/3.11/tutorial/controlflow.html#defining-functions), including arguments and return values. You do not need previous experience building agents.

## What you need

- A Windows PC or Mac, a browser, and an internet connection.
- Permission to install Python and a code editor. On a managed computer, use its approved software portal; if installation is restricted, use a computer where you have installation permission.
- Your own Groq account for model calls. No HF token, final quiz, or certificate is needed for the practical.
- A plain-text/code editor. If you already have one, keep using it. You can install [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview) and open your exercise folder with File → Open Folder.

The local app still contacts remote services. Working installations can encounter model availability, permissions, or credit limits. An error at that stage is not necessarily a mistake in your code.

## Know which window to use

| Window | What goes there |
| --- | --- |
| Terminal on Mac / Command Prompt on Windows | Commands such as `python app.py` |
| Code editor | Changes to `app.py` and other project files |
| Browser | Account settings, this guide, quizzes, and the running agent's chat |

Never paste terminal commands into the agent chat. Never paste your token into the chat or a Python source file.

### Open a command window

**Mac:** press Command + Space, type `Terminal`, and press Return.

**Windows:** open Start, type `Command Prompt`, and open it. Use Command Prompt for this guide, not PowerShell.

Copy only the text inside a command block, or use its copy button. Do not copy the surrounding triple backticks, an example prompt, or output. Run one command at a time and wait until the prompt returns before the next command.

`(.venv)` is part of a prompt, not a command. `>>>` means you opened the Python interpreter; type `exit()` and press Enter/Return to get back to your normal command window.

## Find your downloaded project

During the dummy exercise, work in `agent-course/dummy-agent` and create `dummy_agent.py` there. Later, after downloading the first-agent starter, use this separate folder:

```text
agent-course/
└── First_agent_template/
    ├── app.py
    ├── Gradio_UI.py
    ├── prompts.yaml
    ├── requirements.txt
    ├── tools/
    └── .venv/              (created during setup; may be hidden)
```

Other files may also be present. Edit the project files, not files inside `.venv`.

**Mac:** in Finder, choose Go → Go to Folder, enter `~/agent-course/First_agent_template`, and press Return.

**Windows:** enter `%USERPROFILE%\agent-course\First_agent_template` in File Explorer's address bar and press Enter.

In your editor, use **File → Open Folder** (if available) to open that folder. Select a file from its file list. Double-clicking a `.py` file in the file manager may run it instead of opening it for editing.

## Edit a file without losing your place

1. Open the named file in your editor.
2. Use Find (Command + F on Mac or Control + F on Windows) to locate the exact text in the guide.
3. Replace only that line or block. Keep its leading spaces, commas, and surrounding parentheses.
4. Save with Command + S or Control + S. Keep the original extension: `app.py`, not `app.py.txt`.
5. Return to the terminal, stop the app with Control + C if it is running, and start it again.
6. Refresh the app's browser page.

Do not use a word processor to edit Python. Indentation is part of Python's structure; keep the spacing shown in code examples.

## If you get stuck

Stop at the first failing step rather than continuing with later commands. Note the step number and the command you ran. Copy the error from the terminal, excluding any credentials, then match the error to [troubleshooting](run-your-first-agent.md#troubleshooting). Check your current folder, active environment, and the exact command before retrying.

For a running app, the terminal stays occupied: this is expected. To run another command there, first stop the app with Control + C. On a Mac, this is the Control key, not Command.

**Next:** [Prepare your computer](prepare-your-computer.md).
