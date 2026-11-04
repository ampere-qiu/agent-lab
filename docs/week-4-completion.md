# 17 · Week 04 completion checks { #week-4-completion }

**Objective:** explain how your agents work and check their answers against their evidence.

**Before starting:** open your **existing `week04-exercises` folder** and the **`evidence.md` file you created in [Week 4 setup](week-4-preview.md#evidence-file)**. If the note is missing, create it using the linked setup instructions. Add this review under its **Topic 17** heading.

## Required evidence { #required }

Open the files and results below. Check what happened in each run and note anything that remains incomplete.

| Topic | Your files | Results to check |
| --- | --- | --- |
| [14 · Week 3 RAG review](week-4-retrieval.md) | No new Python file | Answers 1–5 in `evidence.md`, labeled “Week 3 run” or “provided example.” Use the Week 3 lesson and folder for any RAG coding. |
| [15 · Batman](week-4-batman.md) | `my_batman_tools.py`, `my_batman.py` | Your answers to checks A–D, the one-location handoff, the four-location results, checked source links and one recalculated flight estimate in `evidence.md`. The report tool generates `outputs/batman-report.html`; preserve a copy as `evidence-files/batman-report.html` as described in Topic 15. |
| [16 · Vision & Browser](week-4-vision-browser.md) | `my_vision.py`, `my_browser_check.py`, `my_browser.py` | Your image predictions, answers and comparison of the two agents in `evidence.md`; the direct-check screenshots `before.png` and `after.png`; browser-agent screenshots saved in `evidence-files/browser-baseline` and `evidence-files/browser-revised` folders. Record the saved HTML edit and observed answer change. |
| Optional Topic 15 verifier | `my_batman_verified.py`, only if attempted | Your additional-agent design, both delegations, independent page observation, sourced verdict and intentional false-claim test in `evidence.md`. Mark “not attempted” if you skipped this optional extension. |

`week04_common.py`, `week04_search.py`, `week04_tools.py`, `week04_browser.py` and `prepare_visuals.py` are **supplied helpers**. You do not need to create replacements. `assets/venue.png` and `assets/venue.html` are **generated during setup**; the Topic 16 edit changes that existing HTML file. `evidence-files` and its archive subfolders are **created by you** to preserve generated results.

For each topic, write **complete** or **incomplete** under Topic 17 in `evidence.md`. Include a short result that supports your choice, or the error you need to resolve. Save with **Ctrl + S** or **Command + S**. If an output is missing, return to that lesson’s run instructions.

**Complete Topics 14–16 before this review.** The third verifier agent is optional. For each agent, keep a trace showing its action, the returned observation and its final answer. Remove API keys from any notes or terminal excerpts you share.

## Explain the system { #explain }

Write your own answers 1–5 under **Topic 17** in your existing `evidence.md`, then expand the answers to compare. Use one short example from your actual run wherever possible.

**1. Why is delegating to an agent different from calling a function tool?**

??? success "Answer 1 — another execution loop"

    A function tool executes its specified Python operation and returns a value/error. A specialist agent has its own model/action/observation loop and may choose several searches/page reads before returning a report. Show the manager's specialist call and one specialist tool action from your run.

**2. What information must the specialist return to the manager?**

??? success "Answer 2 — information to return"

    The location and role, coordinates, claim source URL, coordinate source URL, supporting evidence and uncertainty must remain available. Without them, the manager cannot calculate the estimate or check the report. In your trace, identify the returned fields rather than assuming they survived.

**3. Why does successful retrieval not establish every requested fact?**

??? success "Answer 3 — returned passages versus support"

    Retrieval ranks candidate passages; they may be irrelevant or lack the requested fact. The Week 3 top-five search can return all five notes despite no allergy policy being present. The answer should state that the supplied notes do not establish the policy, not invent one or claim no real policy exists.

**4. How does `images=[image]` differ from a screenshot callback?**

??? success "Answer 4 — initial input versus new observation"

    `images=[image]` supplies pixels at the start of the task. The callback captures the browser after an action and attaches fresh pixels to an action-step observation for a later model call. A saved PNG alone is not evidence that the model received it. Match one changed screenshot to the next answer in your run.

**5. What could make a larger team less useful than a single agent?**

??? success "Answer 5 — coordination costs and errors"

    Extra calls, latency, lost sources, unclear responsibility and repeated unsupported assertions can outweigh specialization. A verifier is useful only when its checks add evidence or catch a problem. More agents and agreement do not guarantee correctness.

**Final checkpoint:** keep the supplied helpers, your five `my_*.py` programs, existing evidence note, generated assets/results and archived comparisons together in `week04-exercises`. Include `my_batman_verified.py` if you attempted the optional challenge. Be ready to open a named file, point to an actual action/observation and explain one limitation.

Return to the [Week 04 plan](week-4-preview.md), [Batman exercise](week-4-batman.md), or [Vision & Browser exercise](week-4-vision-browser.md).
