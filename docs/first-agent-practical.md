# Build the first agent: local walkthrough { #build-the-first-agent-local-walkthrough }

Continue with the `First_agent_template` you already downloaded, set up, and ran in [Get the agent template](run-your-first-agent.md). You should have received a model response and read [Understand the template](understand-the-template.md).

Now extend that working app with **timezone lookup** and **web search**. Use your existing project folder, its `.venv`, and your Groq key throughout this practical.

This practical adapts the [Hugging Face starter tutorial](https://huggingface.co/learn/agents-course/en/unit1/tutorial) for our local app.

## 1. Prepare your existing app for editing { #1-open-the-adapted-starter }

In the terminal running your app, press **Control + C** to stop it. Leave the template's virtual environment active. Open your existing `First_agent_template` folder in a code editor and save a copy of `app.py` as `app.before-tools.py` for comparison.

After each edit, save the file, run `python app.py` in that same terminal, enter your Groq key when prompted, and refresh the chat page. Stop the app before making the next change. If returning in a new terminal, use the [restart commands](run-your-first-agent.md#11-stop-and-restart) to reactivate this project's environment.

## Files used in this practical { #files-used-in-this-practical }

The small test scripts are **new files you create during this lesson**. They are not in the original starter ZIP. Use the exact name `check_time.py` (with an underscore), not `checktime.py`.

| File | What to do |
| --- | --- |
| `app.py` | Edit the existing agent program to register tools |
| `check_time.py` | Create beside `app.py` in Step 3B to test the time function directly |
| `check_search.py` | Create beside `app.py` in Step 4B to test search directly |
| `tools/web_search.py` | Already supplied; keep it inside the `tools` folder |

Your folder will look like this after creating the two test files:

```text
First_agent_template/
├── app.py
├── check_time.py
├── check_search.py
├── Gradio_UI.py
├── prompts.yaml
├── requirements.txt
├── tools/
│   ├── final_answer.py
│   └── web_search.py
└── .venv/
```

Keep the test scripts here, not inside `tools/` or `.venv/`. Put each test's code in its own file, not in `app.py`. Save Python files without an extra `.txt` extension.

!!! note "If you already have the completed app.py"

    The completed reference has both tools registered. Keep its existing tools list. Run the direct tests in **3B** and **4B**, then the chat tests in **3D** and **4D**. You can skip the registration edits in **3C** and **4C**. The optional custom tool is still unfinished.

## What you will add { #what-you-will-add }

| Already in your template | Your work now |
| --- | --- |
| Working timezone function, not registered | Test it directly, register it, and inspect a real agent call |
| Search tool, not registered | Test it directly, add an instance, and verify returned sources |
| Custom-tool placeholder, not registered | Optional: implement, test, and register your own tool |

## 2. Find the tool registration { #2-walk-through-apppy }

Open `app.py` and find `CodeAgent(...)` inside `main()`. Its initial registration is:

```python
tools=[final_answer],
```

Keep `final_answer` in this list. You will add the existing timezone function and a search-tool instance in the next steps. The `STUDENT TASK` comments mark these edit points. Keep the working model connection and interface settings as they are.

For the optional custom tool later, follow [Step 6: create and connect a new tool](#6-optional-create-your-own-tool).

### How does the agent know which tools it can use? { #how-does-the-agent-know-which-tools-it-can-use }

`tools=[...]` is the connection between your Python tools and the agent. `CodeAgent` includes each registered tool's **name, description, input descriptions, and types** in the instructions sent to the model. The model receives this information together with your chat request and chooses a suitable action.

For example, a request for Tokyo's current time fits the description of `get_current_time_in_timezone`. A request to find an official website fits `web_search`. The model generates Python using those names; the local executor runs it. See [what CodeAgent handles automatically](understand-the-template.md#what-codeagent-handles-automatically).

| Part | Where to edit | Purpose |
| --- | --- | --- |
| Function implementation | The function body in `app.py`, above `main()` | Does the actual work |
| Function description | The docstring directly below `def` | Tells the model when to use the tool |
| Input descriptions | The docstring's `Args:` section | Helps the model supply suitable arguments |
| Tool registration | `tools=[...]` inside `CodeAgent(...)` in `main()` | Makes the tool available to this agent |

The timezone function is already defined in `app.py`; it needs registration, not another implementation file. `check_time.py` only tests it. Search is defined separately in `tools/web_search.py`: its class has a `description` field, and the import in `app.py` makes the class available to your program. Registering `WebSearchTool(max_results=3)` makes an instance available to the agent.

### How does it decide when to call a tool? { #how-does-it-decide-when-to-call-a-tool }

There is no fixed rule such as “if the user says time, call this function.” The model uses the request and tool descriptions to choose. For a first test, ask explicitly: **“Use get_current_time_in_timezone with Asia/Tokyo.”** Then inspect the code and execution output. Registration makes a tool available; it does not guarantee the model chooses it or supplies the correct inputs.

`prompts.yaml` contains general instructions and examples. Some examples mention `search` or `wiki`, but examples do not register tools. A generated `search(...)` call is not a successful search; our registered search tool is named `web_search`. Use the tools list and the actual execution logs to check what happened.

## 3. Enable the time-zone tool { #3-enable-the-time-zone-tool }

**Goal:** make the agent obtain a time from an actual function call and distinguish that result from a model guess.

### A. Read the function { #a-read-the-function }

Find `get_current_time_in_timezone` in `app.py`. Its input is a timezone identifier such as `Asia/Tokyo`. Its output is a string containing the date and time.

| Code in the function | What it does |
| --- | --- |
| `@tool` | Wraps the function with metadata the agent can use |
| `timezone: str` | Describes the input as a string |
| `pytz.timezone(timezone)` | Looks up the timezone rules for that identifier |
| `datetime.datetime.now(tz)` | Reads the current time in that timezone using your computer's clock |
| `.strftime(...)` | Formats the result as readable text |
| `return ...` | Supplies the result to the caller |
| `except Exception ...` | Returns an error message if the input or operation fails |

Timezone names identify regions, not fixed offsets. Some regions change offset during daylight saving time. Use `Asia/Tokyo` for your first test. The function cannot correct an inaccurate computer clock.

### B. Test it without the agent { #b-test-it-without-the-agent }

With the app stopped and the template's virtual environment still active:

1. In your code editor, choose **New File**.
2. Paste the following code into the new file.
3. Save it as **`check_time.py`** inside your existing `First_agent_template` folder, next to `app.py`.


```python
from app import get_current_time_in_timezone

print(get_current_time_in_timezone(timezone="Asia/Tokyo"))
print(get_current_time_in_timezone(timezone="Not/A_Real_Zone"))
```

In the terminal, make sure you are in `First_agent_template` with `(.venv)` active, then run:

```bash
python check_time.py
```

The first line should report Tokyo's date and time. The second should start with `Error fetching time`. The second test checks how invalid input is handled; it is not a successful time lookup. Neither call uses Groq or needs a key. Importing `app` defines the tools without launching the chat.

**Checkpoint:** compare the valid result with a clock set to Tokyo. The invalid-timezone error on the second line is intentional. If the valid Tokyo call fails, fix it before testing through the agent.

If Python says it cannot open `check_time.py`, confirm that you saved it beside `app.py` and that the terminal is in that folder. `dir` on Windows or `ls` on Mac should list both files. If an `ImportError` names the time function, check that you kept the function in `app.py` and saved the file.

### C. Register it with the agent { #c-register-it-with-the-agent }

If `get_current_time_in_timezone` is already in your `tools` list, leave it there and go to Step D. Otherwise, in the original starter's `app.py`, find `tools=[final_answer]` inside `CodeAgent(...)` and replace that argument only with:

```python
tools=[final_answer, get_current_time_in_timezone],
```

Keep the leading indentation and trailing comma. There should be only one `tools=` argument. Do not write `get_current_time_in_timezone()` here: you are registering the capability, not calling it during startup.

Save, run `python app.py`, enter your Groq key, and refresh the local chat page.

### D. Ask for a real tool call { #d-ask-for-a-real-tool-call }

Send in the chat:

> Use get_current_time_in_timezone with Asia/Tokyo. Report the returned time and say where it came from.

Click **Used tool python_interpreter**, then **Execution Logs** inside it to reveal the returned value. You can also inspect the terminal. A possible action is:

```python
result = get_current_time_in_timezone(timezone="Asia/Tokyo")
print(result)
```

This is illustrative output to recognize, not another block to paste into `app.py`. The model may use different variable names or call `final_answer` within the same block.

**Checkpoint:** find the function call, the returned date/time, and a final answer consistent with it. A statement such as “It is 10:00 in Tokyo” without execution evidence is not enough.

If the direct test works but the agent reports an undefined function, check the registration, spelling, saved file, and restart. If it ignores the function, repeat the explicit tool request in a freshly restarted app.

## 4. Explore the search tool { #4-explore-the-search-tool }

**Goal:** let the agent retrieve search results, use them in an answer, and distinguish source evidence from unsupported claims.

### A. Understand what this tool returns { #a-understand-what-this-tool-returns }

`WebSearchTool` is a small adapter supplied in our template’s `tools/web_search.py`. It connects smolagents to the maintained `ddgs` Python package, with **DuckDuckGo explicitly selected as the search service**. The agent sees the name **`web_search`**. Its input is one text argument, `query`. Its output contains result titles, links, and short snippets.

The Python tool contacts a search service. Groq generates the agent's actions and answer; it does not perform this search itself. This starter's search integration requires no separate search API key, but the service can still fail or limit requests.

**Search is not full-page reading.** This tool returns search-result snippets; it does not fetch and read the full contents of each linked page. When the agent summarizes results, it may only have seen those snippets. You will open a source yourself to verify it. Automatically reading pages would require another tool and is outside the two-tool core practical.

### B. Test search directly before using the LLM { #b-test-search-directly-before-using-the-llm }

Stop the app with **Control + C** if it is running; leave the template's `.venv` active.

1. In your code editor, choose **New File**.
2. Paste the following code into it.
3. Save it as **`check_search.py`** inside `First_agent_template`, next to `app.py` and `check_time.py`.


```python
from tools.web_search import WebSearchTool

search_tool = WebSearchTool(max_results=3)
print("Agent-facing name:", search_tool.name)
print(search_tool(query="Python official documentation tutorial"))
```

Run from the `First_agent_template` folder in your activated terminal:

```bash
python check_search.py
```

This uses the search service directly, without a Groq request or key. It lets you check search connectivity independently of the LLM.

`max_results=3` requests up to three results. We use a small number to keep the result readable and reduce how much search text is sent to the model later. It does not limit the number of search calls an agent can make.

Expect the name `web_search`, followed by a `Search Results` heading and entries containing a title, URL, and snippet. Exact results and order vary. A shortened **illustration**, not a live result, is:

```text
Agent-facing name: web_search
## Search Results

[The Python Tutorial](https://docs.python.org/3/tutorial/)
A short search-result description would appear here.
```

**Checkpoint:** at least one relevant result is returned and its link opens. If Python cannot open `check_search.py`, check the file's name, saved location, and current terminal folder as in Step 3B. For a search-service error, use the troubleshooting table below before changing the model or API key.

### C. Register the search instance { #c-register-the-search-instance }

If your `tools` list already contains `WebSearchTool(max_results=3)`, keep it and go to Step D. Otherwise, the starter already imports `WebSearchTool` from `tools.web_search` near the top of `app.py`. The import alone does not register it. Find your existing `tools=` argument and replace it with:

```python
tools=[
    final_answer,
    get_current_time_in_timezone,
    WebSearchTool(max_results=3),
],
```

Indent this block to match the other arguments inside `CodeAgent(...)`. Keep the surrounding constructor and all its other arguments.

| Expression | Meaning |
| --- | --- |
| `WebSearchTool` | The class imported into your app |
| `WebSearchTool(max_results=3)` | A configured instance that can be registered |
| `web_search(query="...")` | The name and call the agent uses in generated Python |

Do not rename the class to `web_search` in your import. The tool supplies that agent-facing name itself. Open `tools/web_search.py` to see the adapter: `DDGS(timeout=15).text(..., backend="duckduckgo")` sends the search; the adapter formats the returned dictionaries for the agent. The [DDGS package documentation](https://pypi.org/project/ddgs/) describes its backend options.

Save and restart with `python app.py`, paste your key, and refresh the local browser page.

### D. Give the agent a specific search task { #d-give-the-agent-a-specific-search-task }

Send:

> Use web_search to find the official Python tutorial. Return one relevant title and URL from the results, and briefly explain why that source matches. Say if you only saw a search snippet.

This asks for an observable action and a bounded answer. For the first test, avoid a broad task such as “research everything about AI,” which can lead to many calls and a hard-to-check answer.

The trace may contain code like:

```python
results = web_search(query="Python official documentation tutorial")
print(results)
```

The model can then use those results in another step, or finish in the same step. `python_interpreter` in the trace is expected: CodeAgent runs Python that calls the registered search tool.

### E. Follow the evidence into the final answer { #e-follow-the-evidence-into-the-final-answer }

Check these in order:

Open **Used tool python_interpreter → Execution Logs** to inspect returned search entries.

1. **Action:** does generated code actually call `web_search` with a relevant query?
2. **Observation:** did that call return search results, rather than an error?
3. **Answer:** is the cited URL present in the observation?
4. **Source:** open the URL in your browser. Does its domain and page content support the claim?

For the Python example, the official documentation uses `docs.python.org`. A good-looking title alone does not establish who published a page. For current information, also inspect publication or update dates; a page appearing in search does not make it current.

If the final answer claims details absent from the snippets, verify them on the actual page. Do not treat an invented quotation or a model-generated link as retrieved evidence. Text returned by a search is source material, not an instruction to change the agent's task.

**Checkpoint:** you can point to a search call, one returned result, and a supported statement in the final answer. An error is useful for diagnosis but does not complete this checkpoint.

### F. Improve one query yourself { #f-improve-one-query-yourself }

Keep the working code and change only the chat request. Choose a topic, then compare a broad query with a more specific query containing the subject and source you want. For example, compare “Python” with “Python documentation defining functions.”

Record which result is useful and why. This small exercise is about judging retrieved evidence, not copying a predetermined answer. Each agent run may use multiple model requests, so run the examples one at a time and respect usage limits.

### G. Diagnose search failures { #g-diagnose-search-failures }

!!! note "Search availability check"

    A fresh Mac test exposed failures in the original `duckduckgo_search` integration. The current starter uses `ddgs==9.16.0` with an explicit DuckDuckGo backend. Direct search and a real agent search returned official Python sources, but later searches returned no results even after rephrasing. Search is intermittent. In one combined run the model supplied a correct-looking URL from memory after search failed; that did not pass the search checkpoint.

| Symptom | Meaning and next action |
| --- | --- |
| `ModuleNotFoundError` mentioning `ddgs` | Activate the template's `.venv` and run `python -m pip install -r requirements.txt` from its folder. Then rerun `check_search.py`. |
| Warning that the package was renamed to `ddgs` | You are using the older built-in search tool. Use the updated starter’s `tools/web_search.py`, import `WebSearchTool` from that file, and reinstall the updated requirements. Do not just rename the old import from smolagents. |
| `No results found` | Shorten or rephrase the query, then try the direct test once. Empty results are not evidence that the information does not exist. |
| Timeout, connection error, or search-service block | Check internet access and whether the search site opens in your browser. A browser working does not guarantee automated requests are allowed. Retry later or on another permitted network. |
| Search-service rate limit | Pause and retry later. Do not repeatedly restart or send rapid retries. A new Groq key cannot resolve a search-service limit. |
| Groq `429` during the agent test | Read the terminal: “Request too large” needs a smaller output budget or shorter input; other exhausted limits need the indicated reset. See the setup troubleshooting table. A successful direct search does not prove Groq has remaining capacity. |
| `web_search` undefined in generated code | Check that a search-tool instance is in `tools`, save, and restart the app. |
| Direct search works, but the agent does not call it | Use the explicit prompt in Step D, verify registration, and retry with fresh agent memory by restarting the app. |
| Search returns results, but the answer gives another URL | Compare the answer with the observation and request a URL actually present in the results. |

If external search remains unavailable, continue reading the trace explanation and return to the live checkpoint later. Label the search test incomplete; do not replace it with invented results.

## 5. Verify the two core tools { #5-verify-the-two-core-tools }

Time and search are a useful first pair: time provides an easily checked local result, while search introduces an external service and source evaluation. Neither requires adding another API key in this starter. Search can still be blocked or rate-limited independently of Groq.

Test each separately before combining them. For a combined test, ask:

> Get the current time in Asia/Tokyo using the time tool, then search for the official Python documentation. Give me a source link actually returned by web_search. If search fails, say that it failed; do not substitute a link from memory.

Inspect the trace for **both** calls and their successful outputs. Compare the time with a trusted clock and open the returned documentation link. The link must occur in the search observation, even if you already know it is correct. If the agent skips a tool, ask explicitly for it and inspect the next run. Do not count a fabricated time or a link supplied from memory as successful execution. This prompt makes the requirement clearer but does not replace checking the evidence yourself.

`final_answer` remains in the tools list as the framework's completion mechanism; it is separate from the two capabilities you are learning to enable.

Image generation has been removed from this adaptation. There is no image tool to register or image-service setup to complete.

## 6. Optional: create your own tool { #6-optional-create-your-own-tool }

You choose the purpose of your tool. The example below uses a tiny **invented Mordor-style glossary** to show where the code and descriptions go. These demo words are not authentic translations, and this is not a general translator. You can use another topic for your own tool.

The process is **write → describe → test directly → register → ask the agent → inspect execution**. A description tells the model what your function does; you must still implement that behavior.

### A. Write the function and its description { #a-scaffold-if-python-functions-are-new }

Stop the app with **Control + C**. In `app.py`, find the optional `@tool` / `my_custom_tool` placeholder **above `main()`**. Replace that entire decorated function, including its old docstring and `raise NotImplementedError(...)`, with this example. Keep the existing timezone function and the rest of the app.

```python
@tool  # Make the function's name, description, and inputs available to smolagents.
def translate_to_mordor(text: str) -> str:
    """Translate one supported English word using an invented Mordor-style demo glossary.

    Args:
        text: One English word to translate: hello, friend, or goodbye.
    """
    glossary = {"hello": "mor", "friend": "dur", "goodbye": "nak"}  # Invented demo words.
    word = text.strip().lower()  # Ignore surrounding spaces and capital letters.
    if word not in glossary:
        return "Unsupported word. Choose hello, friend, or goodbye."
    return glossary[word]  # Return the dictionary result; no model or online translator is called.
```

| Code | Meaning |
| --- | --- |
| `translate_to_mordor` | Name the agent will use to call the tool |
| `text: str` | The input is a string |
| `-> str` | The result is a string |
| First sentence inside triple quotes | Tool description: what it does and when it is useful |
| `Args:` / `text:` | Description of the input the model should supply |
| `glossary`, lookup, and `return` | Actual Python implementation |

**Where do you change the description?** Edit the docstring under `def`, not the chat message or `prompts.yaml`. Describe the real capability and its limits. This function supports only three words, so its description says so.

### B. Test the function before the agent calls it { #check-the-function-before-the-agent-calls-it }

In your editor, create a new file named **`check_my_tool.py`** beside `app.py`, paste the following, and save it. Keep the app stopped and the template's `.venv` active.

```python
from app import translate_to_mordor  # Import the new function; do not launch the chat.

print(translate_to_mordor(text="Hello"))  # Normal input; capital letters are accepted.
print(translate_to_mordor(text="unknown"))  # Unsupported input checks the function's limit.
```

In the terminal, from `First_agent_template`, run:

```bash
python check_my_tool.py
```

Expected output:

```text
mor
Unsupported word. Choose hello, friend, or goodbye.
```

This is a direct Python test. It does not use Groq or require a key. If you choose a different tool, change the import and inputs to match your function, and write down expected results before running it. Fix direct-test failures before testing through the agent.

### C. Connect the tool to CodeAgent { #c-connect-the-tool-to-codeagent }

Inside `main()`, find `CodeAgent(...)`. Add your function's name to its **existing** tools list, keeping the time, search, and final-answer tools:

```python
tools=[
    final_answer,
    get_current_time_in_timezone,
    WebSearchTool(max_results=3),
    translate_to_mordor,  # ADDED: allow the agent to call the new function.
],
```

Register a decorated function by name: `translate_to_mordor`, without parentheses. Writing `translate_to_mordor(...)` here would call it during startup instead of registering it. `WebSearchTool(max_results=3)` uses parentheses because it creates a tool-class instance. Keep only one `tools=` argument inside `CodeAgent(...)`.

You do not need another `.py` file for the tool itself when its definition is in `app.py`. `check_my_tool.py` is only the test script.

### D. Restart and ask for a tool call { #d-restart-and-ask-for-a-tool-call }

Save `app.py`, run `python app.py`, enter your Groq key when prompted, and refresh the chat page. Send:

> Use translate_to_mordor to translate the word Hello using the demo glossary. Report the returned value.

`CodeAgent` supplies the model with your registered tool's name and docstring. The model can generate an action such as:

```python
translated = translate_to_mordor(text="Hello")
print(translated)
final_answer(translated)
```

This is an example of generated action code to recognize in the trace; do not paste it into your function definition. The local executor runs the call. If another step is needed, CodeAgent supplies the result or error to the model, which can continue toward an answer. You do not write that action loop yourself as you did in the dummy exercise.

### E. Check that the new tool actually ran { #e-check-that-the-new-tool-actually-ran }

Open **Used tool python_interpreter → Execution Logs**. Find the `translate_to_mordor` call, the returned `mor`, and a final answer consistent with that result. The model saying “I translated it” without an executed call is insufficient.

Then ask for an unsupported word. The answer should report the function's limit instead of inventing a translation. If the function works directly but the agent test fails, check the saved file, registration, exact function name, docstring, generated arguments, and restart. Tool choice is made by the model, so inspect the trace even when you explicitly name the tool.

### If you later put the tool in a separate file { #if-you-later-put-the-tool-in-a-separate-file }

For your first tool, keeping it above `main()` in `app.py` is simplest. If you choose to organize it as `tools/mordor.py`, move the complete decorated function there and add this import at the top of that file:

```python
from smolagents import tool
```

Then import the function near the top of `app.py`:

```python
from tools.mordor import translate_to_mordor
```

Keep its registration in `CodeAgent`'s tools list. Remove the duplicate definition from `app.py`, and update the direct test to import from `tools.mordor`. **Importing loads the tool into your program; registering exposes it to the agent.** The folder name `tools/` alone does not connect anything.

For the interface details, see the [smolagents 1.13.0 tools guide](https://huggingface.co/docs/smolagents/v1.13.0/en/tutorials/tools). For Python parameters, returns, and docstrings, see [Python's function guide](https://docs.python.org/3.11/tutorial/controlflow.html#defining-functions).

## 7. Inspect instructions and settings { #7-inspect-instructions-and-settings }

A prompt is text sent as part of a model request. The system instructions in `prompts.yaml` describe available tools and the expected response structure. They guide generation; they do not execute functions or train the model. The template placeholders are filled with information such as tool descriptions when the agent builds its instructions.

Open `prompts.yaml` and locate the instructions. Compare one formatting instruction with a response in your trace. See the [template explanation](understand-the-template.md#instructions-and-agent-construction) for how those instructions reach the model. If experimenting, back up the file and preserve its YAML indentation and template placeholders.

In `app.py`, locate the model identifier and `max_steps`. Keep working settings for the first run. `max_steps` limits the action loop, while `max_tokens` limits the output allowance of an individual completion. Neither grants extra API credits or guarantees a correct answer. Experiments with other models remain possible, subject to access and library compatibility.

## 8. Demonstrate the result { #8-demonstrate-the-result }

Demonstrate timezone lookup and web search, showing each call, observation, and final answer. If you completed the optional custom tool, demonstrate that too. Use errors to revise your implementation or description and retry.

Demonstrate the local app. Publishing a Space is the environment-specific exception and is not required. A temporary public link, if deliberately enabled, uses the app owner's credentials and is not permanent hosting.

## 9. Complete the local practical { #9-complete-the-local-practical }

Review the [completion checks](quizzes.md#finish-the-practical). The two quick quizzes appear in the foundations lesson; there is no final-quiz or certificate requirement.
