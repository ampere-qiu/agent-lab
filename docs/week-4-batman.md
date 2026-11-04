# 15 · Multi-agent systems { #week-4-batman }

*Reference: [Hugging Face Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems). Follow the arrows: a request goes down and evidence must come back up.*

**Objective:** understand agent roles and delegation, then build the Batman research team.

Start with **Part A: how agents work together**, then build the Batman team in **Part B**. Adding a third agent is optional.

## Part A · Understand multi-agent systems { #multi-agent-concepts }

[![HF original manager, code tool, and web-agent architecture](images/huggingface-week04/multi-agent-architecture.png)](images/huggingface-week04/multi-agent-architecture.png){ .course-figure-link }

*Figure from Hugging Face, unchanged. [Open the full-size figure](images/huggingface-week04/multi-agent-architecture.png).*

### 1. What makes a system multi-agent? { #why-teams }

An **agent** has a model-driven decision loop, instructions, tools and its own execution history. A **multi-agent system** connects two or more of these agents so they can divide work and exchange results. A **role** describes a responsibility; a **handoff** is the request and information passed between agents.

A single CodeAgent can search, read pages, calculate, and write a report. That makes it a useful baseline: there is only one execution history to inspect. However, a long research task puts search snippets, page text, calculation output, and reporting decisions into that same history. An agent may spend attention on details irrelevant to its current job, repeat searches, or lose the sources needed for a later step.

A manager/specialist design gives research its own model–action–observation loop. The manager sends a goal; the specialist decides which queries and pages to use; the specialist returns a compact report. The manager continues using that report. This is different from a function tool, which runs the specified Python operation and returns its result without making its own sequence of model decisions.

Both agents can share one model connection and key while maintaining different histories and available tools. Two agents do not automatically mean parallel execution: in this exercise the manager waits for the specialist's return. The handoff can reduce irrelevant detail in the manager's context, but it can also discard important evidence. Extra model calls and coordination can make a team slower or more expensive. You must evaluate the trace rather than assume that a team is better.

[![Course diagram showing separate manager and specialist decision loops, request and evidence arrows, and tools outside the agent count](images/week04/multi-agent-concept.svg)](images/week04/multi-agent-concept.svg){ .course-figure-link }

*Course diagram: **2 agents** with separate loops. Tools are not additional agents. [Enlarge the diagram](images/week04/multi-agent-concept.svg).*

### Check the concept before the example { #concept-check }

**1. A manager delegates to one researcher and calls a calculator. How many agents are there?**

??? success "Concept answer 1 — count the loops"

    **Two agents:** manager and researcher. The calculator is a tool that runs a defined operation; it is not a third model-driven loop.

**2. If both agents share one model connection, are they the same agent?**

??? success "Concept answer 2 — connection versus agent"

    No. They remain separate agent objects with their own histories, instructions and available tools. A different model is not required for each role.

**3. Does a manager/specialist diagram mean the agents run in parallel or that the answer is verified?**

??? success "Concept answer 3 — inspect execution"

    No. In this exercise the manager waits for the specialist. Check the trace for actual delegation and inspect the returned sources; an extra agent or a diagram does not guarantee correctness.

## Part B · Main exercise: Batman research team { #batman-exercise }

**Your task:** build a web specialist and a manager that work together to research locations, check sources and create a report.

Alfred needs a shortlist of places where a replacement Batmobile might be found. Your team must research **three Batman filming locations and one supercar factory**, preserve the evidence for their roles and coordinates, calculate a classroom cargo-flight estimate to fictional Gotham, and produce a sourced table and colored coordinate map.

First, check the research tools. Then create the specialist and manager, connect them, and test one filming claim before researching all four locations. Answer each check as you go and keep your results in `evidence.md`.

**Before starting:** complete [Week 4 setup](week-4-preview.md#exercise-files) and [create `evidence.md` and `evidence-files`](week-4-preview.md#evidence-file). Use the **Topic 15** section of that note for your answers and results.

| File | Where it comes from / what you do |
| --- | --- |
| `week04_common.py`, `week04_search.py`, `week04_tools.py` | Supplied in the ZIP. Open the existing files when asked; do not recreate them. |
| `my_batman_tools.py`, `my_batman.py` | Create these in `week04-exercises` by following steps 3 and 4. |
| `my_batman_verified.py` | Not supplied. Create a copy of your working team only for the optional extension. |
| `evidence.md` | Created by you in setup; save your answers and terminal excerpts here. |
| `outputs/batman-report.html` | Generated when the report tool succeeds. Do not create an empty HTML file. |

Use the same activated `week04-exercises` terminal throughout. The research and model traces appear there; only the generated report is opened in a browser.

### See the required team and the optional extension { #team-roles }

[![Course diagram comparing the required two-agent Batman team with the optional three-agent team, showing each role, tools and the verifier connection](images/week04/batman-agent-roles.svg)](images/week04/batman-agent-roles.svg){ .course-figure-link }

*Course diagram: **required = manager + web specialist (2 agents)**. **Optional = add a verifier (3 agents total)**. [Enlarge the diagram](images/week04/batman-agent-roles.svg).*

The web specialist researches. The manager coordinates, calculates and saves. In the optional challenge, add a verifier that independently checks one researched record and returns a verdict. Both specialists report to the manager; the verifier is a separate agent, not a second name for the researcher. The search/page tools, calculator and report writer do not increase the agent count.

**Think before coding:** suppose the specialist returns only “Wollaton Hall is a good candidate.” What can the manager verify? What information would you need to draw the map and check the source?

??? success "Reasoning check"

    The statement lacks a supporting page, coordinates and their source, the filming/factory category, and uncertainty. A persuasive summary is not a usable research record. The manager cannot reconstruct missing evidence reliably from the specialist's confidence.

### 2. Understand each agent’s role { #plan }

The table shows what each agent will do. Before writing the code, explain the two roles in your own words under Topic 15 in `evidence.md`.

| Part | What you will give it |
| --- | --- |
| Web specialist | `WebSearchTool(budget=budget)` and `PageExcerptTool(budget=budget)`; the name `web_specialist` and a description of its research role. |
| Manager | `cargo_time` and `save_report`; access to the specialist through `managed_agents=[specialist]`. |
| Handoff | A supported location/role, coordinates when established, a claim source URL, a coordinate source URL and evidence/uncertainty. |
| Small test | The complete `ONE_LOCATION_TASK` checks one building and asks for a sourced return, without saving a report. |
| Full task | The complete `TASK` asks for three distinct filming sites and one supercar factory, calculations and a saved table/map. |

The fields for a supported report row are `location`, `kind` (`filming` or `factory`), `latitude`, `longitude`, `source_url`, `coordinate_source_url` and `evidence`. A filming source may not establish the coordinate. Missing evidence should be reported, not invented; unsupported coordinates must not become fabricated calculator inputs.

```text
Given task → manager → web_specialist(task="a research goal")
                           ↓ web_search → visit_webpage
                     sourced report → manager
                           ↓ cargo_time → save_report (full task only)
                     outputs/batman-report.html
```

**1. Why does the specialist have search/page tools while the manager has the calculator/report tools?**

??? success "Answer 1 — each agent’s role"

    The specialist gathers evidence in its own loop. The manager requests that research, uses the returned coordinates for calculations and saves the report. This separation makes delegation visible; the manager has no direct search tool to bypass it.

**2. Why should the specialist include source URLs and any uncertainty in its reply?**

??? success "Answer 2 — usable evidence"

    You and the manager need to check what supports each claim and coordinate. A conclusion without its evidence cannot reliably support the calculation or audit. Missing fields should remain explicitly missing until resolved.

### 3. Check tools and explain the estimate { #tool-check }

**Goal:** test the supplied tools without an LLM before asking a team to use them.

1. In your editor, open **`week04-exercises`**, where `requirements.txt` and `week04_common.py` are visible.
2. Choose **File → New Text File → Save As** and save **`my_batman_tools.py`** directly beside those files. **It is not supplied in the ZIP; create it now.**
3. Paste the complete code below, then save with **Ctrl + S** (Windows) or **Command + S** (Mac).
4. Check the name ends in `.py`, not `.py.txt`. Keep this file out of `.venv`, `lessons` and `assets`.

Start with the query and URL in the code below. Read what each call returns. If the page is unavailable, record the error and check the source in your browser.

**What this file does — `my_batman_tools.py`:** Searches public web data, fetches one page, and checks a fixed coordinate through the supplied calculator. It uses no LLM. Inspect the terminal output and source page.

```python title="my_batman_tools.py"
from week04_search import WebSearchTool, PageExcerptTool
from week04_tools import cargo_time

print("Same-coordinate classroom estimate:", cargo_time(40.7128, -74.0060))
print(WebSearchTool()("Batman Wollaton Hall filming official"))
print(PageExcerptTool()("https://wollatonhall.org.uk/hall-and-museum/history/", focus="Wayne Manor Batman"))
```

??? info "Explain the code"

    | Code | What it means |
    | --- | --- |
    | `from ... import ...` | Load the supplied bounded search/page classes and calculator. |
    | `cargo_time(40.7128, -74.0060)` | Call the calculator directly with Gotham's own coordinate. No model is involved. |
    | `WebSearchTool()("...")` | Create a tool instance, then call it with the query. It contacts the search service and returns snippets/URLs. |
    | `PageExcerptTool()("...", focus="...")` | Fetch a focused, partial source excerpt of at most 1,600 characters. It does not control Chrome. |

    Search results help you find sources. Open a source in your browser to check whether the excerpt supports the claim. Keep the output cap: an excerpt is only part of a page, so note any information it does not establish.

**Run:** `python my_batman_tools.py`. **What to check:** the same-coordinate estimate is `1.0`; search returns actual URLs; the page call returns text or an explicit failure. In the existing `evidence.md`, save one snippet URL and the page passage that supports or fails to support the claim. A blocked page is a failed observation; try another credible source and record the failure.

Open the supplied `week04_tools.py` and find `cargo_time`. Read the function before continuing; you will import it into your program. The formula is `round(distance_km * 1.1 / 750 + 1, 2)`: great-circle distance from fictional Gotham `(40.7128, -74.0060)`, a 10% distance allowance, 750 km/h, and a fixed hour. It is a **cargo-plane classroom estimate**, not a shipping schedule. The function accepts destination latitude and longitude and returns hours; it does not search for coordinates or check that a location appeared in a film.

**Your calculation checkpoint:** why does the same coordinate return `1.0`, not zero? If the assumed speed falls, does the travel estimate rise or fall? Explain which parts are assumptions and which must come from sources.

??? success "Check the estimate"

    The fixed hour remains even when distance is zero. Lower speed increases the distance/speed term. Source-backed coordinates are research inputs; speed, route allowance and fixed overhead are teaching assumptions. Correct arithmetic does not validate a location claim.

### 4. Build the agents one at a time { #build-team }

**Goal:** create the web specialist and manager, then connect them so the manager can delegate research.

1. In your editor, open **`week04-exercises`**, where `requirements.txt` and `week04_common.py` are visible.
2. Choose **File → New Text File → Save As** and save **`my_batman.py`** directly beside them. This file is not included in the ZIP.
3. Add blocks **4A → 4B → 4C → 4D** in that order to this **same file**. Each block goes at the bottom, after the previous one; do not replace earlier blocks or repeat the imports. Keep all lines at the indentation shown.
4. Save after each stage with **Ctrl + S** or **Command + S**. The filename must end in `.py`, not `.py.txt`. Do not run until you finish 4D; the earlier stages construct objects but do not yet assign a task.
5. If you have an older `my_batman.py`, preserve its evidence first, then clear that file once and rebuild it in these stages. Do not append the new version to an old complete program.

**What this file does — `my_batman.py`:** uses Groq and live web tools to run the two agents you create. The manager asks the web specialist for evidence, then uses local calculation/report tools. The small task prints a handoff in the terminal; the later full task can generate `outputs/batman-report.html`.

#### 4A. Start the file: imports and model { #4a-start-the-file-imports-and-model }

Paste this as the first block. No agents are created by these imports.

```python title="my_batman.py"
from smolagents import CodeAgent
from week04_common import build_model, agent_options, run_task
from week04_search import WebSearchTool, PageExcerptTool, ResearchBudget
from week04_tools import cargo_time, save_report

model = build_model(max_tokens=800)
```

??? info "Explain 4A — shared connection"

    `CodeAgent` is the class you will use twice. The remaining imports load supplied connection, search, calculation and report helpers. `build_model(max_tokens=800)` prepares one Groq model connection with a smaller output allowance and asks for the key when the completed file runs. It does not itself search or create an agent. Sharing the connection does not merge the agents' histories.

**Check A:** how many agents have you created so far?

??? success "Build answer A"

    **Zero.** Importing a class and preparing a model connection are not `CodeAgent(...)` calls.

#### 4B. Create the web specialist { #4b-create-the-web-specialist }

Append this block below `model = build_model(max_tokens=800)`. This is the **first agent you create**. Before continuing, point to its name, role description, model and tools in your file.

```python title="my_batman.py"

budget = ResearchBudget(max_searches=1, max_pages=2)
specialist = CodeAgent(
    tools=[WebSearchTool(budget=budget), PageExcerptTool(budget=budget)],
    model=model,
    name="web_specialist",
    description="Researches ONE named place per call. Visit sources and return a concise claim, URL and quote. Seek coordinates only when explicitly requested. Respect tool limits; stop after sufficient evidence or mark gaps. Return at most 500 characters.",
    **agent_options(max_steps=4, compact=True),
)
budget.bind(specialist)
```

??? info "Explain 4B — construct a specialist"

    | Setting | Why you add it |
    | --- | --- |
    | `specialist = CodeAgent(...)` | Create a distinct agent object and keep it in the variable `specialist`. |
    | `budget = ResearchBudget(max_searches=1, max_pages=2)` | Allow one search and two page attempts per specialist task. Failed/blocked pages count; retrying the same URL is refused. |
    | `tools=[WebSearchTool(budget=budget), PageExcerptTool(budget=budget)]` | Give both tools the same attempt counter. Search returns at most two snippets; page reading returns a focused excerpt of at most 1,600 characters. |
    | `model=model` | Give it the connection from 4A. |
    | `name="web_specialist"` | Give the manager a callable agent name. The Python variable name and callable name serve different purposes. |
    | `description=...` | Tell the manager when to delegate and what evidence should return. |
    | `**agent_options(max_steps=4, compact=True)` | Limit the specialist to four action steps and each printed observation to 1,800 characters. |
    | `budget.bind(specialist)` | Tie the counters to this agent’s task. A new delegation resets them with the new task history; extra calls within that task cannot bypass them. |

**Check B:** could this specialist save the final report using `save_report` as a registered tool?

??? success "Build answer B"

    **No.** Its registered custom tools are search and page reading. You will give the report tool to the manager.

#### 4C. Create the manager and connect the team { #4c-create-the-manager-and-connect-the-team }

Append the next block. This is the **second agent you create**. Locate the line that connects the already-created specialist; a shared model alone would not connect the two agents.

```python title="my_batman.py"

manager = CodeAgent(
    tools=[cargo_time, save_report],
    model=model,
    managed_agents=[specialist],
    **agent_options(max_steps=3, compact=True),
)
manager.visualize()
```

??? info "Explain 4C — manager and connection"

    `manager = CodeAgent(...)` creates another object with its own execution history. `cargo_time` and `save_report` are supplied function tools: register their names without calling them here. `managed_agents=[specialist]` gives this manager access to the first agent. `visualize()` prints the configured tree; it does not demonstrate an actual delegation. The manager waits for the specialist to return; this example does not run both agents in parallel.

**Check C:** draw the tree from your code before running it. Which agent can search, which can save, and what line would break delegation if removed?

??? success "Build answer C"

    Manager → `cargo_time`, `save_report`, and web specialist → `web_search`, `visit_webpage`. The framework may also show `final_answer`. Removing `managed_agents=[specialist]` removes the manager's delegation connection.

#### 4D. Add the tasks only after both agents exist { #4d-add-the-tasks-only-after-both-agents-exist }

Append this last block at the bottom of the same file. Start with `ONE_LOCATION_TASK`, which checks one filming claim. `TASK` contains the four-location research request for step 6.

```python title="my_batman.py"

TASK = """Alfred needs three Batman filming locations and one supercar factory.
Use at most FOUR separate web_specialist calls, ONE named candidate per call:
Wollaton Hall, Knebworth House, Mentmore Towers, and Lamborghini Sant'Agata Bolognese.
Use ONE delegation per manager action step; do not combine delegations in a loop.
These are candidates to VERIFY, not facts to assume. For each, request a supported
filming/factory claim, coordinates, source_url, coordinate_source_url and a short
evidence quote. Ask the specialist to use focused page excerpts, at most one search
and three page attempts, and return one compact record under 500 characters.
Preserve each record before the next delegation. Do not request all four places
in one specialist call. Do not repeat a failed delegation or invent missing data.
If four supported rows are unavailable, report the gaps without saving a complete report.
Otherwise calculate all four cargo estimates and call save_report in ONE Python
action using the compact rows; do not print the whole JSON again. Then finish with
the report path, sources and assumptions. Keep responses and printed output short.
"""

ONE_LOCATION_TASK = """Delegate ONCE to web_specialist: check ONLY whether
Wollaton Hall was used as Wayne Manor in a Batman film. First read
https://wollatonhall.org.uk/hall-and-museum/history/ with focus="Wayne Manor Batman".
If blocked or insufficient, use at most one search and one alternate page.
Stop as soon as a relevant page supports the claim. Do NOT research coordinates,
transport, opening times or other places. Return the claim, source URL, one short
quote and uncertainty in at most 500 characters. If unsupported, mark it missing.
The manager should preserve that evidence and finish. No calculation or report.
"""

run_task(manager, ONE_LOCATION_TASK)
```

??? info "Explain 4D — construction versus execution"

    Triple-quoted text stores each task as one multi-line string. Defining `TASK` does not run it. `run_task(manager, ONE_LOCATION_TASK)` starts the manager's model/action/observation loop using the smaller request. The manager may then call the separately created specialist. That specialist has its own loop and must return its evidence.

**Check D:** which line starts model reasoning, and does the tree prove the specialist has been called?

??? success "Build answer D"

    `run_task(manager, ONE_LOCATION_TASK)` starts the task loop. The tree proves only configuration; the trace must show an actual `web_specialist(task=...)` call.

**Before running:** your file should now have one import/model section, one specialist constructor, one manager constructor, the two tasks and one `run_task` call. Explain the two constructors and the connecting line to a partner or in `evidence.md`; then save and continue below.

### 5. Test one filming claim { #small-handoff }

**For the first run, check only the filming claim.** Leave coordinate research for step 6. Check the returned quote against its source.

| Enforced limit | First run |
| --- | --- |
| Manager action steps | 3 |
| Specialist action steps | 4 per delegation |
| Search attempts | 1 per delegation, at most 2 short results |
| Page attempts | 2 per delegation, including failures; no repeat URL |
| Page excerpt / printed observation | At most 1,600 / 1,800 characters |
| Model output allowance | 800 tokens per response; this is not an input-token limit |

These are limits, not a required step count. A failed task may make one extra framework final-answer request at its step limit. A page refusal or exhausted research budget should lead to a short incomplete answer, not more retries.

After saving steps 4A–4D, check that the last line is **`run_task(manager, ONE_LOCATION_TASK)`**.

**Run:** `python my_batman.py`. Enter your Groq key if prompted. The code first prints the tree, then the manager should delegate the supplied Wollaton Hall task to the specialist.

**What to check:** copy a short actual trace excerpt into **Topic 15 → One-location handoff** in your existing `evidence.md`:

| Stage | Find this in your own run |
| --- | --- |
| Manager action | An executed `web_specialist(task=...)` request. |
| Specialist action | Its page-reading call and any permitted search fallback. A successful first source needs no search. |
| Observation | A returned page passage or an explicit retrieval failure. |
| Specialist return | The filming claim, source URL, short quote and uncertainty. Coordinates are not requested in this test. |
| Manager response | Whether it preserves the source and limitation. |

**1. Is this the same as the manager calling `web_search` directly?**

??? success "Answer 1 — two loops"

    No. The manager calls `web_specialist`, which has its own loop and may make several tool calls before returning. `web_search` is a function-like tool action inside that specialist's loop.

**2. Should this small test create `outputs/batman-report.html`?**

??? success "Answer 2 — small-test output"

    No. The supplied one-location task explicitly requests no calculation or report. Its result is in the terminal. The report is generated only in the full-task step below; do not create an empty HTML file yourself.

**3. What if the manager never delegates, a page fails, or the run reaches its limit?**

??? success "Answer 3 — an incomplete run"

    Record the actual failure and mark this run incomplete. A final answer alone is insufficient. Check the four build stages, both agent constructors, the managed-agent connection and the direct tools. Keep the limits; record the failure rather than repeatedly retrying. Use the [research-limit guidance](#research-limits) to decide what to check next.

### 6. Research four locations and inspect the report { #full-run }

The full task covers **three filming sites and one factory**, but uses **one place per specialist delegation**. Each call starts a fresh specialist history, so whole pages from the earlier location do not accumulate there. The manager retains only the compact returned records.

In the **existing `my_batman.py`**, make these changes, then save:

1. Change `ResearchBudget(max_searches=1, max_pages=2)` to **`ResearchBudget(max_searches=1, max_pages=3)`**. This allows a claim page, a coordinate page and at most one alternate.
2. In the specialist constructor, change `agent_options(max_steps=4, compact=True)` to **`agent_options(max_steps=5, compact=True)`**.
3. In the manager constructor, change `agent_options(max_steps=3, compact=True)` to **`agent_options(max_steps=6, compact=True)`**.
4. Change the final call from `run_task(manager, ONE_LOCATION_TASK)` to **`run_task(manager, TASK)`**.

Keep the excerpt, print and model-output caps. Do not raise limits to force a complete report. The task requests at most four short delegations, then combined calculation/report writing and a final answer. If a claim or coordinate cannot be supported within the budget, an honest gap is the expected result.

**What to inspect:** each `web_specialist(task=...)` should name only one place, in a separate manager action step. Its step counter starts again for that task. The manager should keep each source-backed record and should not ask a new specialist run to rediscover an earlier result. Printing all four handoffs in one action could clip the last record, so keep each delegation in a separate step.

**Run:** `python my_batman.py`. Check the terminal trace. If `save_report` succeeded, it creates **`outputs/batman-report.html`** inside `week04-exercises`. In File Explorer/Finder, open `week04-exercises` → `outputs` and double-click `batman-report.html` to view it in your browser. If the file is missing, look for the `save_report` call and any error in the terminal.

Copy the generated HTML in your file manager into the **existing `evidence-files` folder**, keeping its name **`batman-report.html`**. This is a copy of an output, not a new program. Paste the actual sources/trace into `evidence.md`. The report writer recalculates hours and writes a table and coordinate plot. It checks basic input shape/URLs, not whether a webpage supports the claim. Check every source and coordinate even if the report file was created successfully.

[![HF original Batman research example output map](images/huggingface-week04/batman-output-map.png)](images/huggingface-week04/batman-output-map.png){ .course-figure-link }

[Open the full-size original](images/huggingface-week04/batman-output-map.png)

*Original example output, unchanged: [Hugging Face Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems). Use it to discuss marker position, color, labels and evidence; it is not an answer key for your research.*

**How final checks differ from another agent:** smolagents can run Python `final_answer_checks` before accepting an answer. A check can reject missing output or inconsistent data, but that callback is not automatically a third agent. Here, you check the sources and map yourself. In the optional challenge, you add another agent to check a researched record. Compare the evidence each type of check can examine.

Your classroom output uses a lightweight longitude/latitude coordinate plot without a geographic basemap. Check the printed legend: purple means under five estimated hours; red means five or more. A neat visual can still hide wrong coordinates, overlapping locations or unsupported film associations.

**Check your map:** choose one marker, locate the corresponding row, check both source URLs, and recompute its time. Would a longitude-sign error move it to the other side of the map? Does the color agree with the estimate? Note one limitation of this simplified map and one limitation of the flight assumption.

??? success "Map answer 1 — location and longitude sign"

    Check the marker's name against the row and both source pages. Changing the sign of longitude reflects its horizontal position across the zero-longitude line; for a western location it can place the marker far to the east. A plausible-looking marker does not verify the source coordinate.

??? success "Map answer 2 — time and color"

    Recompute `round(distance_km * 1.1 / 750 + 1, 2)` with a source-backed destination. Under the printed legend, values below five hours are purple and values of five or more are red. An unrelated color or unsupported coordinate needs correction.

??? success "Map answer 3 — limits and final checks"

    The coordinate plot has no geographic basemap and can overlap markers; the flight estimate ignores real routing, schedules and handling constraints. A Python final-answer check can test a file or data rule. A verifier agent has its own model/tool loop and must show which sources it checked. Neither proves that a claim is correct without suitable evidence.

### 7. Check and explain the team you built { #audit }

**Check your results:** use your report and terminal output to answer the questions below in `evidence.md`.

**1. Does every row have a supported role and coordinate?** Open both source links for each of the three filming sites and one factory. Write one supported example and any gap you find.

??? success "Answer 1 — check the evidence"

    A claim source must support the film/factory role; a coordinate source must establish the location used in the calculation. A working URL or plausible number alone is not enough. Record gaps honestly; do not label an unsupported four-row report complete.

**2. Where do the model decisions end and the supplied Python tool's work begin?**

??? success "Answer 2 — model and tool responsibilities"

    Groq produces the actions and report reasoning. Local Python runs search/page requests and the supplied calculator/report writer. `cargo_time` calculates from input coordinates; it does not discover or verify them. `save_report` renders the given rows; it does not prove that a cited page supports a claim.

**3. Would one agent always be worse than this team?**

??? success "Answer 3 — team trade-off"

    No. One agent may be simpler for a small task. A team separates responsibilities and histories, but adds calls, coordination and possible handoff losses. Judge actual supported results, not the number of agents.

**Checkpoint:** keep the two required Python files, the one-location trace, the full-run trace, checked source links, one recalculated estimate and your understanding answers in the existing evidence note. Keep the generated report and its archive copy if the full task succeeded. If a run failed, keep the error message and note which checks remain incomplete.

### If the service refuses a request { #research-limits }

- **Page 403:** the website blocked the request. It counts as an attempt; use one permitted alternate or mark the source unavailable. Do not retry the blocked URL.
- **Research limit reached:** return the evidence collected and identify missing fields. A refusal does not prove a fact is false.
- **Groq 413 / request too large:** stop that run. Check that your helper files match the latest download and that you are using `ONE_LOCATION_TASK`; start a fresh small run after correcting it. Waiting alone does not shrink a large history.
- **Groq 429:** stop and respect the service’s retry interval before a fresh run. Calls share the account’s token/request limits; these local caps reduce usage but do not guarantee capacity.

See [Groq’s rate-limit explanation](https://console.groq.com/docs/rate-limits). A local character cap is not an exact token count. Do not paste a whole page into the task or increase the step limits to work around a service refusal.

### 8. Optional challenge: add a verifier agent { #optional-verifier }

Add a third agent that independently checks one result from your Batman research. Complete the two-agent exercise first, then save a copy for this challenge:

1. Open your working, saved **`my_batman.py`** in the editor.
2. Choose **File → Save As** and save a copy as **`my_batman_verified.py`** directly in `week04-exercises`. Keep `my_batman.py` as the two-agent version.
3. Confirm that both filenames appear in the editor's file list, and that you are now editing **`my_batman_verified.py`**. This file is not supplied in the ZIP.
4. In the copied file, **you** create the verifier **after** the `specialist = CodeAgent(...)` block and **before** `manager = CodeAgent(...)`. Register both with the manager; keep the same model connection. Keep the changes in this copied file.
5. Replace the copied file's `TASK` with your own **one-row research and verification request**, using one entry from the existing report as a candidate to recheck. Request both delegations and a sourced verdict, **without saving another report**. Keep each specialist at four steps, with its own one-search/two-page budget. Give the copied manager four steps. Confirm its last call uses your new `TASK`, then save. Use the hints below if you get stuck.

**What this file does — `my_batman_verified.py`:** your copied and edited Groq program adds an independent checking loop for one candidate row. It uses live research tools and prints both handoffs/verdicts in the terminal. Compare with your existing report; this bounded optional test does not overwrite it. Checking all four rows would require separate fresh one-row runs, rather than packing eight delegations into the six-step required full task.

Before adding the verifier, decide:

1. Give it a distinct name, a description and a narrow checking responsibility. Decide which tools it needs and why it must read the cited pages independently.
2. Define a verdict format with `pass`, `fail` or `uncertain` for each row, plus the checked URL, supported/disputed claim, and correction or missing evidence. State what makes a verdict credible.
3. Decide when the manager should call the verifier and what the manager should do with each verdict. Who can author the report? Who can block an unsupported row?
4. Add a new `CodeAgent` object. Register it **alongside** the web specialist in the manager's `managed_agents` list. Update the manager task so the one sourced record reaches the verifier before the manager accepts it.
5. Inspect the tree: it should have a manager and two different specialists. Then inspect execution: both specialist calls must actually occur.

**Challenge test:** in this same optional file, first copy your normal final call into `evidence.md`. Temporarily replace its final call with `run_task(manager, "YOUR FALSE-CLAIM TEST REQUEST")`—no new test file is needed. In your request, supply one deliberately wrong label, such as “Wollaton Hall is a supercar factory,” and the [official hall history source](https://wollatonhall.org.uk/hall-and-museum/history/). Ask for a verdict without saving a report. Predict the result, then inspect whether the verifier reads the page and rejects or marks the claim uncertain. Label the claim as an intentional test error in your evidence; do not submit it as a research result.

**Optional run:** save and run `python my_batman_verified.py` for the false-claim test, then restore `run_task(manager, TASK)`, save and rerun your one-row research/verification task. Keep both results under **Topic 15 → Optional verifier** in your existing `evidence.md`. Compare with the existing two-agent report: did the new agent catch the injected error? Did it supply a checked source or merely repeat the researcher's wording? Record added model calls and any remaining uncertainty.

??? tip "Hint 1 — create a different agent"

    Give the verifier its own `name`, `description` and `CodeAgent` object. Assigning the existing specialist to a second variable does not create a new loop.

??? tip "Hint 2 — connect the new agent"

    Use `managed_agents=[specialist, verifier]` on the copied manager. Give the verifier its own `ResearchBudget(max_searches=1, max_pages=2)`, bounded search/page tools and at most four steps. Bind that budget to the verifier; do not share its counters with the researcher or give it the report-writing tool. Check one row per delegation and keep verdicts short.

??? tip "Hint 3 — request verification"

    Registration is not execution. Update the manager task to hand over the sourced row and request a verdict. Specify what happens after `fail` or `uncertain`; this bounded extension does not save a new report.

??? success "Verifier answer 1 — name, scope and tools"

    A suitable role is an independent claim/coordinate checker, with its own name and page-reading/search tools. It should inspect the cited source rather than trust the researcher's confidence.

??? success "Verifier answer 2 — a useful verdict"

    Return pass/fail/uncertain for each claim, checked URL, the evidence, and a correction or missing field. A verdict without an inspected source is only another assertion.

??? success "Verifier answer 3 — when to accept a row"

    Call the verifier after research and before accepting the row. Return an evidence-backed verdict or honest uncertainty; do not start repair loops after the budget is exhausted. This test leaves the existing report unchanged. In a later reporting workflow, only the manager would write a verified report.

??? success "Verifier answer 4 — expected configuration and execution"

    The tree contains the manager plus two distinct specialists. The trace must then show the manager calling both specialists; the tree alone does not prove either call happened.

??? success "Verifier answer 5 — false-claim test"

    A hall's filming/history page does not establish that it is a supercar factory. After reading the source, a verifier should reject that factory claim or mark it unsupported/uncertain. Record the actual result if it misses the error. Then restore your normal one-row task and compare the verdicts; an extra agent does not guarantee a useful correction.

??? success "What counts as the extension?"

    A third object in a diagram is insufficient. Show the new design, the actual second delegation, a page observation, and a verdict linked to evidence. An independent checker may still be wrong; you still need to check its sources.

### Code-reading recap { #reference }

You created the specialist in **4B** and the manager in **4C**. In your file, find where each agent is created and where `managed_agents=[specialist]` connects them. Step 6 gives the exact small-to-full changes while keeping short excerpts and fresh specialist tasks. Keep the two-agent file so you can compare it with the optional verifier version.

**Credit:** scenario, hierarchy, estimate and unchanged figures adapted from [HF Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems), Apache-2.0. The research runs through Groq, and the report uses a simplified coordinate plot.

**Next:** [16 · Vision & Browser Agents](week-4-vision-browser.md). Keep your explanations, handoff results and source/map checks for the [completion review](week-4-completion.md).
