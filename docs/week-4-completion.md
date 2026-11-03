# 17 · Week 04 completion checks { #week-4-completion }

**Objective:** explain what you built and show actual results from required Topics 14–16. This review creates no new Python program.

**Before starting:** open your **existing `week04-exercises` folder** and the **`evidence.md` file you created in [Week 4 setup](week-4-preview.md#evidence-file)**. If you skipped creating the note, follow that linked step now; it was never a supplied download file. You will fill its existing **Topic 17** heading, not create a second evidence file.

## Required evidence { #required }

Use the table to locate each item and check its result. A file's presence alone does not prove the required action ran.

| Topic | Student-created files | Generated result / evidence to review |
| --- | --- | --- |
| [14 · RAG](week-4-retrieval.md) | `my_rag_continuation.py` | Terminal direct/agent retrieval, source-supported dish claim, unsupported-policy run and answers 1–4 in `evidence.md`. This runner does not save a separate report. |
| [15 · Batman](week-4-batman.md) | `my_batman_tools.py`, `my_batman.py` | Your explanation of the supplied code, actual one-location delegation, full four-entry research/source/coordinate audit, one recalculation and understanding answers in `evidence.md`. The report tool generates `outputs/batman-report.html`; preserve a copy as `evidence-files/batman-report.html` using the lesson's copy step. No independent role/task design or code improvement is required. |
| [16 · Vision & Browser](week-4-vision-browser.md) | `my_vision.py`, `my_browser_check.py`, `my_browser.py` | Image predictions and changed-question answers in `evidence.md`; generated direct `before.png` and `after.png`; generated agent screenshots copied into student-created `evidence-files/browser-baseline` and `evidence-files/browser-revised` folders. Record the saved HTML edit and observed answer change. |
| Optional Topic 15 verifier | `my_batman_verified.py`, only if attempted | Your additional-agent design, both delegations, independent page observation, sourced verdict and intentional false-claim test in `evidence.md`. Mark “not attempted” if you skipped this optional extension. |

`week04_common.py`, `week04_retriever.py`, `week04_search.py`, `week04_tools.py`, `week04_browser.py` and `prepare_visuals.py` are **supplied helpers**. You do not need to create replacements. `assets/venue.png` and `assets/venue.html` are **generated during setup**; the Topic 16 edit changes that existing HTML file. `evidence-files` and its archive subfolders are **created by you** to preserve generated results.

For each required row, write **complete** or **incomplete** under Topic 17 in the existing `evidence.md`, followed by the actual supporting action/observation or the error. Save the note with **Ctrl + S** or **Command + S**. Missing outputs should lead you back to the relevant creation/run step; do not create blank output files or substitute example answers.

The **RAG continuation, two-agent Batman team and guided vision/browser work are required in Week 4**. All required code is given in full; explain it and show what actually ran. A third verifier is optional and is the only independent coding challenge. A correct diagram or direct tool test is preparation; a required agent checkpoint also needs successful model/tool execution evidence. Do not share keys in your notes or terminal excerpts.

## Explain the system { #explain }

Write your own answers 1–5 under **Topic 17** in your existing `evidence.md`, then expand the answers to compare. Use one short example from your actual run wherever possible.

**1. Why is delegating to an agent different from calling a function tool?**

??? success "Answer 1 — another execution loop"

    A function tool executes its specified Python operation and returns a value/error. A specialist agent has its own model/action/observation loop and may choose several searches/page reads before returning a report. Show the manager's specialist call and one specialist tool action from your run.

**2. What must survive the specialist-to-manager handoff?**

??? success "Answer 2 — evidence contract"

    The location and role, coordinates, claim source URL, coordinate source URL, supporting evidence and uncertainty must remain available. Without them, the manager cannot reliably calculate or audit the report. In your trace, identify the returned fields rather than assuming they survived.

**3. Why does successful retrieval not establish every requested fact?**

??? success "Answer 3 — returned passages versus support"

    Retrieval ranks candidate passages; they may be irrelevant or lack the requested fact. Our top-five search can return all five notes despite no allergy policy being present. The answer should state that the supplied notes do not establish the policy, not invent one or claim no real policy exists.

**4. How does `images=[image]` differ from a screenshot callback?**

??? success "Answer 4 — initial input versus new observation"

    `images=[image]` supplies pixels at the start of the task. The callback captures the browser after an action and attaches fresh pixels to an action-step observation for a later model call. A saved PNG alone is not evidence that the model received it. Match one changed screenshot to the next answer in your run.

**5. What could make a larger team less useful than a single agent?**

??? success "Answer 5 — coordination costs and errors"

    Extra calls, latency, lost sources, unclear responsibility and repeated unsupported assertions can outweigh specialization. A verifier is useful only when its checks add evidence or catch a problem. More agents and agreement do not guarantee correctness.

**Final checkpoint:** keep the supplied helpers, your six required `my_*.py` programs created from the given code, existing evidence note, generated assets/results and archived comparisons together in `week04-exercises`. The optional seventh runner is needed only if you attempted the verifier. Be ready to open a named file, point to an actual action/observation and explain one limitation. There is no new submission script, publishing, certification or account-gated quiz for this review.

Return to the [Week 04 plan](week-4-preview.md), [Batman exercise](week-4-batman.md), or [Vision & Browser exercise](week-4-vision-browser.md).
