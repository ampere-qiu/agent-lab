# Week 04 — smolagents Part 2 (English release)

The Japanese Week 4 edition is **To be released** and is not included in this download. Published Japanese Weeks 1–3 remain available on the course website.

## Start here

Open `lessons/en/week-4-preview.md` and follow the setup in order. Continue with `week-4-retrieval.md`, `week-4-batman.md`, `week-4-vision-browser.md`, and `week-4-completion.md` in the same folder.

## Supplied, student-created and generated files

The ZIP supplies the package list, Groq/retrieval/search/report/browser helpers, asset generator, English lessons, unchanged credited HF figures and license. Do not recreate the helper files.

Create `evidence.md` and the `evidence-files` folder using the setup lesson's template and steps. Create each required `my_*.py` directly in the extracted `week04-exercises` root beside `requirements.txt`, using the complete code shown in its lesson. Do not save them inside `.venv` or `lessons`.

The supplied `prepare_visuals.py` generates `assets/venue.png` and `assets/venue.html` without an LLM. Later programs generate screenshots and reports; do not create empty stand-ins. The setup page lists every file's origin and save location.

## Required practicals and optional challenge

All required code is given: paste the complete program, read its collapsed explanation, run the specified steps and explain the observed results. The supplied small/full Batman task switch and RAG/vision/browser data changes are exact guided edits. Only adding a third agent is an optional independent coding challenge. The English lesson gives hints for that extension rather than a completed solution.

The first Batman run prints one-location research. The given final-call change runs the full task and can create `outputs/batman-report.html`. Preserve actual outputs in `evidence-files` before comparisons; see the lessons for copy/rename instructions.

## Environment

Use Python 3.11 and a separate `.venv`; install `requirements.txt` using the Windows/Mac steps in the setup lesson. Chrome is needed for the browser part. Selenium Manager may obtain a compatible driver on first use.

Groq model calls send prompts, retrieved passages and images to a remote model. Enter the key with hidden input; never put credentials in scripts or evidence. The direct retrieval/browser checks can work without a model call. Completion requires the actual observations specified in each lesson.

## Downloads

You have extracted a complete English Week 4 pack. The three download names contain the same files; no second ZIP is needed. Start with `lessons/en/week-4-preview.md`.

## Week 03 context

Understand CodeAgent's model → Python action → tool observation loop and function/class tools. Week 03 made Agentic RAG optional; Week 04 makes its continuation required and supplies the five source-labeled party notes, so prior RAG files are not needed.

## Credits

Adapted from Hugging Face Agents Course Unit 2.1, Apache-2.0 (see `HF-LICENSE.txt`):

- https://huggingface.co/learn/agents-course/en/unit2/smolagents/retrieval_agents
- https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems
- https://huggingface.co/learn/agents-course/en/unit2/smolagents/vision_agents

Original HF instructional figures are preserved unchanged with URLs/hashes in `lessons/en/images/huggingface-week04/sources.json`. The venue assets and bounded classroom tools are original adaptations. Batman/Wayne Manor are fictional teaching references; no DC artwork is bundled. See `NOTICE.md`.
