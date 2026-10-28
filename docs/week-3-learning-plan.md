# Week 03 · Plan and download { #week-3-learning-plan }

This week you will use **smolagents and your Groq key** to run small Python agents from the terminal. Alfred is planning a party: your programs will search for music, choose a menu, calculate preparation time, use catering/theme tools, and retrieve information from a local knowledge base.

The class covers introduction, CodeAgent, action formats, tools, and Agentic RAG. [Agent teams and vision/browser topics continue in Week 04](week-4-preview.md).

## Learning objectives { #learning-objectives }

By the end, you can create and run a small agent program, identify its action and observation, explain Python versus structured tool calls, change the data used by a Python tool, and check a RAG answer against retrieved passages and their sources.

## What you need { #what-you-need }

Use your existing **`First_agent_template`** folder, **Python 3.11 `.venv`**, code editor, and **Groq API key** from Week 2. You need internet for Groq calls and web searches.

**The agent programs run only in the terminal.** They print their results there. There is no Gradio interface or browser chat to start for Week 03. The course website is where you read the instructions.

## Your route this week { #learning-sequence }

| Lesson | Activity |
| --- | --- |
| [08 · Introduction to smolagents](week-3-framework.md) | Read how the model, framework, and tools work together. |
| [09 · Run a CodeAgent](week-3-code-agent.md) | Create and run playlist, menu, and preparation-time programs. |
| [10 · Python or structured tool calls?](week-3-action-formats.md) | Compare two action formats, then run ToolCallingAgent and inspect its trace. |
| [11 · Tools: functions and classes](week-3-custom-tool.md) | Create a direct test and two agent programs; change a tool's data. |
| [12 · Building Agentic RAG Systems](week-3-retrieval.md) | Search the web and local notes; verify sources and add a note. |
| [13 · Completion checks](week-3-completion.md) | Show your files and execution results. |

## 1. Download and place the support files { #exercise-files }

**What is provided?** A small ZIP with **seven support files**: the Groq connection, ready-made Python tools, a local knowledge-base retriever, a package list, instructions, and the source license. You will write the small agent programs yourself by copying the code from the lessons.

[Download Week 03 support files (.zip)](downloads/week03-smolagents.zip){ .md-button .md-button--primary download="week03-smolagents.zip" }

| Inside the ZIP | What it provides |
| --- | --- |
| `week03_common.py` | Groq connection, agent settings, and result/error printing. |
| `week03_tools.py` | Ready-made menu, catering, and party-theme tools. |
| `week03_search.py` | The web-search tool. |
| `week03_retriever.py` | Five party notes and the local BM25 retrieval tool. |
| `week03-requirements.txt` | The Python packages needed this week. |
| `week03_README.md` | Setup and run instructions. |
| `week03-HF-LICENSE.txt` | The Hugging Face source license. |

1. If the Week 2 chat app is running, stop it with **Control + C** in its terminal.
2. Click the download button. The ZIP is usually saved in **Downloads**.
3. **Windows:** right-click the ZIP → **Extract All** → **Extract**. **Mac:** double-click the ZIP in Finder.
4. Open the extracted **`week03-exercises`** folder. Copy its **seven files**.
5. Paste those files directly into the **existing `First_agent_template` folder**, beside `app.py`. Copy the files themselves, not the enclosing `week03-exercises` folder. If you already edited older `week03...` files, keep a backup of those edits before replacing same-name files.

Open the correct destination in your file manager:

- **Windows — File Explorer:** paste `%USERPROFILE%\agent-course\First_agent_template` into its address bar and press Enter.
- **Mac — Finder:** choose **Go → Go to Folder**, enter `~/agent-course/First_agent_template`, and press Return.

These paths use the default Week 2 location. If you saved the project elsewhere, use that existing folder; do not create an empty replacement folder.

After copying, the seven files should be beside your existing `app.py` and `.venv` folder. The ZIP provides the helpers and tools; the lessons show you how to create the `my_...py` programs that use them.

## 2. Open the project in your editor { #open-project }

Open your code editor. In VS Code, choose **File → Open Folder** and select **`First_agent_template`**. The file list should show `app.py`, `week03_common.py`, `week03_tools.py`, and `week03_search.py` together.

When a lesson says **create a file**, choose **File → New Text File**, paste the given complete Python code, then use **File → Save As** to save the exact filename in this folder. Save beside `app.py`, not inside `.venv` or `tools`.

Use **Ctrl + S** on Windows or **Command + S** on Mac after each edit. A filename such as `my_playlist.py.txt` is wrong: use `my_playlist.py`.

## 3. Open a terminal and activate the environment { #activate-environment }

**Windows:** open Start, type **Command Prompt**, and open it. Use this separate Command Prompt window for the Windows commands, not PowerShell.

```bat
cd /d "%USERPROFILE%\agent-course\First_agent_template"
.venv\Scripts\activate.bat
python --version
dir
```

**Mac:** open **Terminal**, then run:

```bash
cd ~/agent-course/First_agent_template
source .venv/bin/activate
python --version
ls
```

Run one line at a time. Confirm **`(.venv)`** appears, Python is **3.11.x**, and the file listing includes the supplied `week03...` files. The current folder must be `First_agent_template`.

Repeat the `cd` and activation commands whenever you open a new terminal. Keep this terminal open for the practicals. Later lessons simply say **Run: `python filename.py`**; use this activated terminal in `First_agent_template` on either system.

## 4. Check the terminal packages { #packages }

In the same activated terminal, on **either Windows or Mac**, run:

```bash
python -m pip install -r week03-requirements.txt
```

This list keeps `smolagents==1.13.0`, `openai>=1.0,<3`, and `ddgs==9.16.0`, and adds `langchain-community==0.4.2`, `langchain-text-splitters==1.1.3`, and `rank-bm25==0.2.2` for step 12. It does not request a Gradio UI, a GPU, an embedding model, or browser automation. Existing packages may show `Requirement already satisfied`; the retrieval packages and their dependencies may need downloading.

Then check the supplied menu tool without contacting Groq:

```bash
python -c "from week03_tools import suggest_menu; print(suggest_menu(occasion='formal'))"
```

Expected output:

```text
3-course dinner with wine and dessert.
```

This confirms that the folder, imports, and supplied Python tool work. It does not call the LLM.

## Files you will create { #files }

| Step | File to create in First_agent_template | What it does |
| --- | --- | --- |
| 09 | `my_playlist.py` | Search for party music with CodeAgent. |
| 09 | `my_menu.py` | Choose a stored menu through an agent. |
| 09 | `my_timing.py` | Calculate a preparation finish time with Python. |
| 10 | `my_tool_calling.py` | Run the music search using structured tool calls. |
| 11 | `my_tool_check.py` | Test menu, catering, and theme tools without an LLM. |
| 11 | `my_catering.py` | Use an agent to select the highest-rated fictional service. |
| 11 | `my_theme.py` | Use a class-based tool to retrieve a party theme. |
| 12 | `my_rag_search.py` | Build a party plan using web-search results. |
| 12 | `my_retrieval_check.py` | Test local retrieval and its limits without an LLM. |
| 12 | `my_rag.py` | Answer from local notes with returned source labels. |

Every practical gives the complete code, the filename, a short run command, and what to look for in the terminal. The environment setup above applies to all of them. The short blocks marked **read only** show supplied functions or generated output; they are not extra programs to create.

## If something does not run { #local-adaptation }

| Message or symptom | What to check |
| --- | --- |
| Folder does not exist | Find the actual `First_agent_template` folder in your file manager and use its location. |
| `.venv` activation file is missing | You may be in the wrong folder. Use the existing Week 2 project and environment. |
| `can't open file` | Save the named `.py` file beside `app.py`; check its spelling and that it is not `.py.txt`. |
| `No module named week03_common` | Copy the ZIP's files beside your new program, not into a nested folder. |
| `No module named smolagents`, `openai`, or `ddgs` | Activate `.venv` and run the requirements command above. |
| A retrieval module such as `langchain_community` or `rank_bm25` is missing | Use the updated requirements file and run its install command in the same `.venv`. |
| Groq key prompt looks empty while typing | Input is hidden. Enter the key and press Enter. |
| Groq request or search fails | Show the actual error to your teacher; see [Week 2 troubleshooting](run-your-first-agent.md#troubleshooting). |

## Credits { #sources }

Lessons, party examples, and credited figures are adapted from the [Hugging Face Agents Course, Unit 2.1](https://huggingface.co/learn/agents-course/en/unit2/smolagents/introduction). The [Apache 2.0 license](licenses/huggingface-agents-course.txt) is included with the download.

**Next:** [08 · Introduction to smolagents](week-3-framework.md).
