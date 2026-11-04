# Week 04 — smolagents Part 2

This download contains English and Japanese lessons with identical code and figures.

日本語で始める場合は、[第04週の学習計画](lessons/ja/week-4-preview.md)を開いてください。環境準備から各ファイルの作成・実行まで、順に説明しています。図をクリックすると元の画像を開けます。図の下の説明パネルは開閉できます。

## Start here

Open [the English Week 4 plan](lessons/en/week-4-preview.md) for setup. Then continue with Topics 14–17 in the same folder: the RAG review, multi-agent systems and Batman exercise, vision/browser agents, and completion checks.

## Your files

The download includes connection and tool helpers, `requirements.txt`, `prepare_visuals.py`, the lessons, diagrams and source credits. Leave those helper files in place.

Create `evidence.md` and an `evidence-files` folder using the setup instructions. As you reach each exercise, create these five Python files directly inside `week04-exercises`, beside `requirements.txt`:

- `my_batman_tools.py` — check the research and calculation tools.
- `my_batman.py` — create the web specialist and manager, then test their handoff.
- `my_vision.py` — ask an agent to inspect the venue plan.
- `my_browser_check.py` — check that Chrome can open the page, click and save screenshots.
- `my_browser.py` — let an agent choose browser actions and read the screenshots.

Add each lesson’s code blocks to its named file in order and save before running. The lessons tell you when to run, which command to use and where to find the result. Keep your answers and short terminal excerpts in `evidence.md`.

`prepare_visuals.py` creates `assets/venue.png` and `assets/venue.html`. Later programs create reports and screenshots. Copy results into `evidence-files` before a comparison run replaces them.

## Week 03 context

For RAG coding, return to [Week 3 — Building Agentic RAG Systems](https://ampere-qiu.github.io/agent-lab/week-3-retrieval/) in your `First_agent_template` folder. Topic 14 checks your understanding using earlier results or its provided example; you do not need another RAG program for Week 4.

If you already started Week 4, save a copy of your work and extract the latest pack to a fresh folder. Use that download’s helper files with the code in the current lessons.

## Batman research limits

The first task checks one filming claim. It allows 3 manager steps, 4 specialist steps, one search and two page attempts per delegation. Page excerpts are limited to 1,600 characters, printed observations to 1,800 characters, and model output to 800 tokens.

For the full task, follow Topic 15’s changes to research one place per delegation, with 3 page attempts, 5 specialist steps and 6 manager steps. A blocked page counts as an attempt. Keep any missing evidence in your notes instead of increasing the limits to force an answer. Groq’s shared limits may still require you to stop and wait.

## Optional challenge

Copy your working Batman team to `my_batman_verified.py` and add a verifier agent. Have it check one researched record, then test whether it catches an intentionally false claim. Topic 15 includes hints to help you get started.

## Environment

Use Python 3.11 and the Week 4 `.venv`. Follow the setup’s Windows or Mac commands to install `requirements.txt`. You also need Chrome for the browser work and internet for model and search requests. Selenium may download a compatible Chrome driver on the first run.

Enter your Groq key when prompted. Task text, page observations and image inputs are sent to Groq. Keep the key out of scripts and notes. The direct tool and browser checks do not call a model.

## Downloads

The three Week 4 download names contain the same files. Extract only one and choose `lessons/en/week-4-preview.md` or `lessons/ja/week-4-preview.md`.

## Credits

Adapted from Hugging Face Agents Course Unit 2.1 under Apache-2.0. See `HF-LICENSE.txt` and `NOTICE.md`.

- [Retrieval Agents](https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents)
- [Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems)
- [Vision and Browser Agents](https://huggingface.co/learn/agents-course/en/unit2/smolagents/vision_agents)

Original HF figures retain source URLs and hashes in `lessons/en/images/huggingface-week04/sources.json`. The download also includes two course diagrams and the fictional venue assets.
