# 15 · Batman: build and investigate an agent team { #week-4-batman }

**Required guided practical: copy the complete code, run it, and explain the manager/web-specialist loop. Optional independent challenge: add a third verifier agent.**

Alfred needs a shortlist of places where a replacement Batmobile might be found. Your team must research **three Batman filming locations and one supercar factory**, preserve the evidence for their roles and coordinates, calculate a classroom cargo-flight estimate to fictional Gotham, and produce a sourced table and colored coordinate map.

The learning goal is to **understand the supplied code and trace the information crossing the agent boundary**. As in Week 3, the required programs below are complete: paste them into the named files, read the collapsed code explanations, run the given steps, and answer the checks. You do not invent role descriptions, tool wiring, task text or a required code improvement. The only independent coding challenge is the optional third agent at the end.

**Before starting:** complete [Week 4 setup](week-4-preview.md#exercise-files) and [create `evidence.md` and `evidence-files`](week-4-preview.md#evidence-file). If you have not done that setup, stop here and create them now. Throughout this lesson, reopen that **existing** note under Topic 15; do not look for a supplied `evidence.md`.

| File | Where it comes from / what you do |
| --- | --- |
| `week04_common.py`, `week04_search.py`, `week04_tools.py` | Supplied in the ZIP. Open the existing files when asked; do not recreate them. |
| `my_batman_tools.py`, `my_batman.py` | Not supplied as files. Create each below by copying the complete given code directly into `week04-exercises`. |
| `my_batman_verified.py` | Not supplied. Create a copy of your working team only for the optional extension. |
| `evidence.md` | Created by you in setup; save your answers and terminal excerpts here. |
| `outputs/batman-report.html` | Generated when the report tool succeeds. Do not create an empty HTML file. |

Use the same activated `week04-exercises` terminal throughout. The research and model traces appear there; only the generated report is opened in a browser.

## 1. Understand what a team changes { #why-teams }

A single CodeAgent can search, read pages, calculate, and write a report. That makes it a useful baseline: there is only one execution history to inspect. However, a long research task puts search snippets, page text, calculation output, and reporting decisions into that same history. An agent may spend attention on details irrelevant to its current job, repeat searches, or lose the sources needed for a later step.

A manager/specialist design gives research its own model–action–observation loop. The manager sends a goal; the specialist decides which queries and pages to use; the specialist returns a compact report. The manager continues using that report. This is different from a function tool, which runs the specified Python operation and returns its result without making its own sequence of model decisions.

Both agents can share one model connection and key while maintaining different histories and available tools. Two agents do not automatically mean parallel execution: in this exercise the manager waits for the specialist's return. The handoff can reduce irrelevant detail in the manager's context, but it can also discard important evidence. Extra model calls and coordination can make a team slower or more expensive. You must evaluate the trace rather than assume that a team is better.

![HF original manager, code tool, and web-agent architecture](images/huggingface-week04/multi-agent-architecture.png)

[Open the full-size original](images/huggingface-week04/multi-agent-architecture.png)

*Original figure, unchanged: [Hugging Face Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems). Follow the arrows: a request goes down and evidence must come back up.*

**Think before coding:** suppose the specialist returns only “Wollaton Hall is a good candidate.” What can the manager verify? What is missing for a map or a source audit?

??? success "Reasoning check"

    The statement lacks a supporting page, coordinates and their source, the filming/factory category, and uncertainty. A persuasive summary is not a usable research record. The manager cannot reconstruct missing evidence reliably from the specialist's confidence.

## 2. Read the supplied roles and return contract { #plan }

The code below already assigns the responsibilities. **Read this table; you do not need to design or fill in a configuration.** In the existing `evidence.md`, explain each role in your own words under Topic 15.

| Part | What the provided program gives it |
| --- | --- |
| Web specialist | `WebSearchTool()` and `VisitWebpageTool()`; a supplied name and description requiring source-backed research and uncertainty. |
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

??? success "Answer 1 — supplied responsibilities"

    The specialist gathers evidence in its own loop. The manager requests that research, uses the returned coordinates for calculations and saves the report. This separation makes delegation visible; the manager has no direct search tool to bypass it.

**2. Why must source URLs and uncertainty survive the handoff?**

??? success "Answer 2 — usable evidence"

    The manager and student need to check what supports each claim and coordinate. A conclusion without its evidence cannot reliably support the calculation or audit. Missing fields should remain explicitly missing until resolved.

## 3. Check tools and explain the estimate { #tool-check }

**Goal:** test the supplied tools without an LLM before asking a team to use them.

1. In your editor, open **`week04-exercises`**, where `requirements.txt` and `week04_common.py` are visible.
2. Choose **File → New Text File → Save As** and save **`my_batman_tools.py`** directly beside those files. **It is not supplied in the ZIP; create it now.**
3. Paste the complete code below, then save with **Ctrl + S** (Windows) or **Command + S** (Mac).
4. Check the name ends in `.py`, not `.py.txt`. Keep this file out of `.venv`, `lessons` and `assets`.

Use the supplied query and URL for this required check. Read what each call returns; you are not asked to write another query or tool. If the site is unavailable, record the actual failure and ask the instructor for an alternate source before continuing.

**What this file does — `my_batman_tools.py`:** Searches public web data, fetches one page, and checks a fixed coordinate through the supplied calculator. It uses no LLM. Inspect the terminal output and source page.

```python title="my_batman_tools.py"
from week04_search import WebSearchTool
from smolagents import VisitWebpageTool
from week04_tools import cargo_time

print("Same-coordinate classroom estimate:", cargo_time(40.7128, -74.0060))
print(WebSearchTool()("Batman Wollaton Hall filming official"))
print(VisitWebpageTool()("https://wollatonhall.org.uk/hall-and-museum/history/")[:2000])
```

??? info "Explain the code"

    | Code | What it means |
    | --- | --- |
    | `from ... import ...` | Load the supplied search class, smolagents page-reader class and supplied calculator. |
    | `cargo_time(40.7128, -74.0060)` | Call the calculator directly with Gotham's own coordinate. No model is involved. |
    | `WebSearchTool()("...")` | Create a tool instance, then call it with the query. It contacts the search service and returns snippets/URLs. |
    | `VisitWebpageTool()("...")` | Fetch text from the specified page; it does not control Chrome. |
    | `[:2000]` | Print only the first 2,000 characters of the fetched text. Missing text may simply be farther down the page. |

    Search discovers candidate sources; a fetched passage supports a specific claim. For this exercise open the returned URL yourself as well. If the relevant passage is beyond the printed slice, read it on the page or increase the slice and rerun. Do not interpret a truncated printout as the whole source.

**Run:** `python my_batman_tools.py`. **What to check:** the same-coordinate estimate is `1.0`; search returns actual URLs; the page call returns text or an explicit failure. In the existing `evidence.md`, save one snippet URL and the page passage that supports or fails to support the claim. A blocked page is a failed observation; try another credible source and record the failure.

Open the **supplied, existing** `week04_tools.py` beside your new runner and find `cargo_time`. Read this function in place; you do not create or paste another calculator. The formula is `round(distance_km * 1.1 / 750 + 1, 2)`: great-circle distance from fictional Gotham `(40.7128, -74.0060)`, a 10% distance allowance, 750 km/h, and a fixed hour. It is a **cargo-plane classroom estimate**, not a shipping schedule. The function accepts destination latitude and longitude and returns hours; it does not search for coordinates or check that a location appeared in a film.

**Your calculation checkpoint:** why does the same coordinate return `1.0`, not zero? If the assumed speed falls, does the travel estimate rise or fall? Explain which parts are assumptions and which must come from sources.

??? success "Check the estimate"

    The fixed hour remains even when distance is zero. Lower speed increases the distance/speed term. Source-backed coordinates are research inputs; speed, route allowance and fixed overhead are teaching assumptions. Correct arithmetic does not validate a location claim.

## 4. Create the complete two-agent program { #build-team }

**Goal:** understand how the supplied program creates and connects two agents. All required values and connections are already written.

1. In your editor, open **`week04-exercises`**, where `requirements.txt` and `week04_common.py` are visible.
2. Choose **File → New Text File → Save As** and save **`my_batman.py`** directly beside those files. **The file is not in the ZIP; you create it by copying the code below.**
3. Paste the **entire code block**, from the imports through the final `run_task` line. There are no blanks to fill.
4. Save with **Ctrl + S** (Windows) or **Command + S** (Mac). The filename must be `my_batman.py`, not `.py.txt`; keep it out of `.venv`, `lessons` and `assets`.
5. If you already made the earlier scaffold, first save any results you want in `evidence.md`, then **replace its contents** with this complete version. Do not append a second program below it.

**What this file does — `my_batman.py`:** uses Groq and live web tools to run a manager and a web specialist. The first run uses the provided one-location task and prints a sourced handoff in the terminal. The same file also contains the provided full task; a later exact one-line edit runs it and can generate `outputs/batman-report.html`.

```python title="my_batman.py"
from smolagents import CodeAgent, VisitWebpageTool
from week04_common import build_model, agent_options, run_task
from week04_search import WebSearchTool
from week04_tools import cargo_time, save_report

TASK = """Alfred needs a Batmobile replacement research shortlist.
First delegate research to web_specialist. Find three Batman filming locations
and one supercar factory. Visit sources to support each filming/factory claim
and coordinates. Return location, kind (filming or factory), latitude, longitude,
source_url, coordinate_source_url, evidence and uncertainty. Never invent sources
or coordinates. Mark unavailable evidence and stop short of a complete report
if four verified entries cannot be obtained.
Then use cargo_time for each verified entry and save_report with a JSON list
of these rows. Final answer: report path, source URLs, assumptions and gaps.
"""


ONE_LOCATION_TASK = """Delegate to web_specialist: check whether Wollaton Hall
was used as Wayne Manor in a Batman film. Search and visit an appropriate source.
Return the supported claim and source URL. State whether a coordinate source was
found; mark it missing if not established. Preserve the source and uncertainty in
your final answer. Do not calculate a transfer time or save a report in this test.
"""


def build_team(model):
    specialist = CodeAgent(
        tools=[WebSearchTool(), VisitWebpageTool()], model=model,
        name="web_specialist",
        description="Researches filming locations and factories; visits sources and returns evidence, coordinates, source URLs and uncertainties.",
        **agent_options(max_steps=12),
    )
    manager = CodeAgent(
        tools=[cargo_time, save_report], model=model,
        managed_agents=[specialist], **agent_options(max_steps=8),
    )
    return manager, specialist


if __name__ == "__main__":
    manager, specialist = build_team(build_model())
    manager.visualize()
    run_task(manager, ONE_LOCATION_TASK)
```

??? info "Explain my_batman.py"

    | Code | What it means |
    | --- | --- |
    | `from smolagents import ...` | Load the agent class and ready-made page-reader class. |
    | `from week04_... import ...` | Load the supplied helpers and tools from existing files in the same folder. You do not rewrite those modules. |
    | `TASK = """..."""` | Store the full research request. Triple quotes keep several lines together as one string. Defining it does not run the task. |
    | `ONE_LOCATION_TASK = """..."""` | Store the smaller supplied request for inspecting one handoff first. |
    | `build_team(model)` | Build the two agents using the same model connection and return both objects. |
    | `tools=[WebSearchTool(), VisitWebpageTool()]` | Create the two class-tool instances for the specialist. The parentheses create objects; the web requests occur when those tools are called. |
    | `name="web_specialist"` and `description=...` | Give the specialist a callable name and explain its role to the manager. These values are already supplied. |
    | `tools=[cargo_time, save_report]` | Register the supplied function tools on the manager without calling them during setup. |
    | `managed_agents=[specialist]` | Register a separate agent the manager may delegate to. This is the connection, not proof the manager used it. |
    | `**agent_options(max_steps=...)` | Insert the supplied Python-action instructions, logging and limit for each agent's loop. A step limit is a boundary, not a promise of completion. |
    | `return manager, specialist` | Return both objects so the main program can use or inspect them. |
    | `if __name__ == "__main__":` | Run the main block when you execute this saved file. |
    | `build_team(build_model())` | Prepare the Groq connection, ask for the key if needed, then create the agents. |
    | `manager.visualize()` | Print the configured agent/tool tree. This does not itself call the model or research a location. |
    | `run_task(manager, ONE_LOCATION_TASK)` | Run the first, smaller supplied task and print the actual trace/result. |

    Each agent has its own model/action/observation history. The manager waits for the specialist's returned report, then continues. Sharing a model/key does not merge those histories or make this example parallel.

**Code-reading check:** which tools should appear under each agent in the printed tree? What does `managed_agents=[specialist]` add?

??? success "Answer — configuration before execution"

    Expect `web_search` and `visit_webpage` under the specialist, and `cargo_time` and `save_report` under the manager. The framework may also show its built-in `final_answer`. The managed-agent registration lets the manager call the specialist, which can run its own loop. The tree checks configuration; the next step checks execution.

## 5. Run the supplied one-location handoff { #small-handoff }

Leave the last line exactly as supplied: **`run_task(manager, ONE_LOCATION_TASK)`**. You do not write a test prompt.

**Run:** `python my_batman.py`. Enter your Groq key if prompted. The code first prints the tree, then the manager should delegate the supplied Wollaton Hall task to the specialist.

**What to check:** copy a short actual trace excerpt into **Topic 15 → One-location handoff** in your existing `evidence.md`:

| Stage | Find this in your own run |
| --- | --- |
| Manager action | An executed `web_specialist(task=...)` request. |
| Specialist action | Its actual search and page-reading call. |
| Observation | A returned page passage or an explicit retrieval failure. |
| Specialist return | The claim, source URL and any missing coordinate evidence. |
| Manager response | Whether it preserves the source and limitation. |

**1. Is this the same as the manager calling `web_search` directly?**

??? success "Answer 1 — two loops"

    No. The manager calls `web_specialist`, which has its own loop and may make several tool calls before returning. `web_search` is a function-like tool action inside that specialist's loop.

**2. Should this small test create `outputs/batman-report.html`?**

??? success "Answer 2 — small-test output"

    No. The supplied one-location task explicitly requests no calculation or report. Its result is in the terminal. The report is generated only in the full-task step below; do not create an empty HTML file yourself.

**3. What if the manager never delegates, a page fails, or the run reaches its limit?**

??? success "Answer 3 — an incomplete run"

    Record the actual failure and mark this run incomplete. A final answer alone is insufficient. Check that you copied the complete given file and that the direct tools worked, then ask the instructor before repeating a failing model/network run. You are not required to invent new agent instructions to fix it.

## 6. Run the supplied full task and inspect the report { #full-run }

The complete four-entry request is already stored in `TASK`. Make this **one exact guided edit** in the existing `my_batman.py`:

- Find the last line: `run_task(manager, ONE_LOCATION_TASK)`.
- Replace it with: **`run_task(manager, TASK)`**.
- Save the same file. Do not change the role description, tool lists or task strings. No new Python file is needed.

The given full task requests research → source/coordinate handoff → calculation → saved report. The specialist gathers evidence; the manager calculates and saves. You can follow this sequence in the trace rather than designing a plan yourself.

**Run:** `python my_batman.py`. Check the terminal trace. If `save_report` succeeded, it creates **`outputs/batman-report.html`** beside your runner's folder. In File Explorer/Finder, open `week04-exercises` → `outputs` and double-click `batman-report.html` to view it in your browser. **Do not create this HTML file manually.** If it is absent, find the missing/failed report call in the trace rather than making an empty stand-in.

Copy the generated HTML in your file manager into the **existing `evidence-files` folder**, keeping its name **`batman-report.html`**. This is a copy of an output, not a new program. Paste the actual sources/trace into `evidence.md`. You are not required to make a revised agent or produce a second report. The report writer recalculates hours and writes a table and coordinate plot. It checks basic input shape/URLs, not whether a webpage supports the claim. Its output file can exist even when research is weak; file existence is not the completion criterion.

![HF original Batman research example output map](images/huggingface-week04/batman-output-map.png)

[Open the full-size original](images/huggingface-week04/batman-output-map.png)

*Original example output, unchanged: [Hugging Face Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems). Use it to discuss marker position, color, labels and evidence; it is not an answer key for your research.*

**How final checks differ from another agent:** smolagents can run Python `final_answer_checks` before accepting an answer. A check can reject missing output or inconsistent data, but that callback is not automatically a third agent. Our required exercise uses a manual source/map audit; the optional extension adds a separately instructed agent with its own research loop. Explain what evidence either form of checking actually examines.

Your classroom output uses a lightweight longitude/latitude coordinate plot without a geographic basemap. Check the printed legend: purple means under five estimated hours; red means five or more. A neat visual can still hide wrong coordinates, overlapping locations or unsupported film associations.

**Your map audit:** choose one marker, locate the corresponding row, check both source URLs, and recompute its time. Would a longitude-sign error move it to the other side of the map? Does the color agree with the estimate? Note one limitation of this simplified map and one limitation of the flight assumption.

??? success "Map answer 1 — location and longitude sign"

    Check the marker's name against the row and both source pages. Changing the sign of longitude reflects its horizontal position across the zero-longitude line; for a western location it can place the marker far to the east. A plausible-looking marker does not verify the source coordinate.

??? success "Map answer 2 — time and color"

    Recompute `round(distance_km * 1.1 / 750 + 1, 2)` with a source-backed destination. Under the printed legend, values below five hours are purple and values of five or more are red. An unrelated color or unsupported coordinate needs correction.

??? success "Map answer 3 — limits and final checks"

    The coordinate plot has no geographic basemap and can overlap markers; the flight estimate ignores real routing, schedules and handling constraints. A Python final-answer check can test a file or data rule. A verifier agent has its own model/tool loop and must show which sources it checked. Neither proves that a claim is correct without suitable evidence.

## 7. Check and explain the supplied program { #audit }

**Required understanding checks:** use the actual output in your existing `evidence.md`. You do not have to replace a candidate, invent a task or improve the code independently.

**1. Does every row have a supported role and coordinate?** Open both source links for each of the three filming sites and one factory. Write one supported example and any gap you find.

??? success "Answer 1 — evidence audit"

    A claim source must support the film/factory role; a coordinate source must establish the location used in the calculation. A working URL or plausible number alone is not enough. Record gaps honestly; do not label an unsupported four-row report complete.

**2. Where do the model decisions end and the supplied Python tool's work begin?**

??? success "Answer 2 — model and tool responsibilities"

    Groq produces the actions and report reasoning. Local Python runs search/page requests and the supplied calculator/report writer. `cargo_time` calculates from input coordinates; it does not discover or verify them. `save_report` renders the given rows; it does not prove that a cited page supports a claim.

**3. Would one agent always be worse than this team?**

??? success "Answer 3 — team trade-off"

    No. One agent may be simpler for a small task. A team separates responsibilities and histories, but adds calls, coordination and possible handoff losses. Judge actual supported results, not the number of agents.

**Checkpoint:** keep the two required Python files, the one-location trace, the full-run trace, checked source links, one recalculated estimate and your understanding answers in the existing evidence note. Keep the generated report and its archive copy if the full task succeeded. Failures should be marked incomplete and discussed with the instructor; independent redesign is not required.

## 8. Optional challenge: design and add a new verifier agent { #optional-verifier }

**Yes: in this extension you add a new agent yourself.** First complete the manager/web-specialist exercise. Then create the optional file as follows:

1. Open your working, saved **`my_batman.py`** in the editor.
2. Choose **File → Save As** and save a copy as **`my_batman_verified.py`** directly in `week04-exercises`. Keep `my_batman.py` as the two-agent version.
3. Confirm that both filenames appear in the editor's file list, and that you are now editing **`my_batman_verified.py`**. This file is not supplied in the ZIP.
4. In the copied `build_team` function, **you** create the verifier **after** `specialist` and **before** `manager`. Register both with the manager. Keep `return manager, specialist` and the existing main block; you do not need another runner file.
5. Update the copied file's `TASK` to request checking before saving, confirm its last call uses `TASK`, then save the changes. This is the only independent coding challenge in Week 4; the required two-agent work above is already complete.

**What this file does — `my_batman_verified.py`:** your copied and edited Groq program adds an independent checking loop to the same research task. It uses live research tools and prints both handoffs/verdicts in the terminal. The manager alone calls `save_report`; preserve its generated output in `evidence-files` if you want to compare it.

Write a verifier design before coding:

1. Give it a distinct name, a description and a narrow checking responsibility. Decide which tools it needs and why it must read the cited pages independently.
2. Define a verdict format with `pass`, `fail` or `uncertain` for each row, plus the checked URL, supported/disputed claim, and correction or missing evidence. State what makes a verdict credible.
3. Decide when the manager should call the verifier and what the manager should do with each verdict. Who can author the report? Who can block an unsupported row?
4. Add a new `CodeAgent` object. Register it **alongside** the web specialist in the manager's `managed_agents` list. Update the manager task so the sourced rows reach the verifier before saving.
5. Inspect the tree: it should have a manager and two different specialists. Then inspect execution: both specialist calls must actually occur.

**Challenge test:** in this same optional file, first copy your normal final call into `evidence.md`. Temporarily replace its final call with `run_task(manager, "YOUR FALSE-CLAIM TEST REQUEST")`—no new test file is needed. In your request, supply one deliberately wrong label, such as “Wollaton Hall is a supercar factory,” and the [official hall history source](https://wollatonhall.org.uk/hall-and-museum/history/). Ask for a verdict without saving a report. Predict the result, then inspect whether the verifier reads the page and rejects or marks the claim uncertain. Label the claim as an intentional test error in your evidence; do not submit it as a research result.

**Optional run:** save and run `python my_batman_verified.py` for the false-claim test, then restore `run_task(manager, TASK)`, save and rerun for the full verified task. Keep both results under **Topic 15 → Optional verifier** in your existing `evidence.md`. Compare with the two-agent run: did the new agent catch the injected error? Did it supply a checked source or merely repeat the researcher's wording? Record added model calls and one case where the verdict remained uncertain.

??? tip "Hint 1 — create a different agent"

    Give the verifier its own `name`, `description` and `CodeAgent` object. Assigning the existing specialist to a second variable does not create a new loop.

??? tip "Hint 2 — connect the new agent"

    Use `managed_agents=[specialist, verifier]` on the copied manager. Give the verifier the search/page tools it needs, not the report-writing tool.

??? tip "Hint 3 — request verification"

    Registration is not execution. Update the manager task to hand over sourced rows before saving and specify what happens after `fail` or `uncertain`.

??? success "Verifier answer 1 — name, scope and tools"

    A suitable role is an independent claim/coordinate checker, with its own name and page-reading/search tools. It should inspect the cited source rather than trust the researcher's confidence.

??? success "Verifier answer 2 — a useful verdict"

    Return pass/fail/uncertain for each claim, checked URL, the evidence, and a correction or missing field. A verdict without an inspected source is only another assertion.

??? success "Verifier answer 3 — when to save"

    Call the verifier after research and before reporting. The manager can request repairs for failed claims, retain honest uncertainty, and withhold unsupported rows from a complete report. The verifier reports; the manager writes the file.

??? success "Verifier answer 4 — expected configuration and execution"

    The tree contains the manager plus two distinct specialists. The trace must then show the manager calling both specialists; the tree alone does not prove either call happened.

??? success "Verifier answer 5 — false-claim test"

    A hall's filming/history page does not establish that it is a supercar factory. After reading the source, a verifier should reject that factory claim or mark it unsupported/uncertain. Record the actual result if it misses the error. Then restore the normal task and compare the full run; an extra agent does not guarantee a useful correction.

??? success "What counts as the extension?"

    A third object in a diagram is insufficient. Show the new design, the actual second delegation, a page observation, and a verdict linked to evidence. An independent checker may still be wrong; your manual audit remains necessary.

## Code-reading recap { #reference }

The required `my_batman.py` is the complete visible program in step 4; there is no separate hidden required solution to assemble. You create that file by pasting the whole block and use the exact final-call change in step 6. The optional third-agent file is made only if you choose the independent extension.

**Credit:** scenario, hierarchy, estimate and unchanged figures adapted from [HF Multi-Agent Systems](https://huggingface.co/learn/agents-course/en/unit2/smolagents/multi_agent_systems), Apache-2.0. This class uses one Groq setup, complete required programs, code explanations and guided observation checks. The local output uses a simplified coordinate plot.

**Next:** [16 · Vision & Browser Agents](week-4-vision-browser.md). Bring the supplied-code explanations, actual handoffs and source/map audit to [completion review](week-4-completion.md).
