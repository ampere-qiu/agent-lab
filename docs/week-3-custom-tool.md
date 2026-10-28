# 11 · Tools: functions and classes { #week-3-custom-tool }

**Objective:** understand two ways to define a tool, run the supplied catering and theme tools, and make one change of your own.

**Before starting:** finish [Week 03 setup](week-3-learning-plan.md#exercise-files). Use your `First_agent_template` folder, existing `.venv`, and Groq key. You will create `my_tool_check.py`, `my_catering.py`, and `my_theme.py` directly beside `app.py`.

## What a model needs to know { #your-task }

A tool has a name, description, input names and types, and an output type. These tell the model when and how to use it. The Python implementation does the actual work.

[![Animation showing a model request, tool execution, and returned observation](images/huggingface/Agent_ManimCE.gif)](images/huggingface/Agent_ManimCE.gif)

*Image credit: [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/tools). Select it to enlarge.*

## A. Read the supplied catering function { #implement }

[![Alfred choosing a catering service](images/huggingface/alfred-catering.jpg)](images/huggingface/alfred-catering.jpg)

*Image credit: [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit2/smolagents/tools). Select it to enlarge.*

In your editor, open **`week03_tools.py`**, which is already supplied in the download. Find `catering_service_tool`. **This block shows code already in that file: read it there; do not create a second copy.**

```python
@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.

    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }

    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)

    return best_service
```

??? info "Explain catering_service_tool"

    **This supplied function chooses a name from fixed Python data.**

    | Code | What it means |
    | --- | --- |
    | `@tool` | Turn the function into a smolagents tool with a description the model can read. The decorator is imported near the top of the supplied file. |
    | `def catering_service_tool(query: str) -> str:` | Name the function and describe its input and output as strings. `query` is accepted but is not used to filter the data in this example. |
    | The docstring and `Args:` | Explain the tool's purpose and input to the model. They do not run a search. |
    | `services = {...}` | Store fictional service names and ratings in a dictionary on your PC. |
    | `max(services, key=services.get)` | Compare the ratings and select the service name with the largest rating. `services.get` tells `max` to compare each name's rating. |
    | `return best_service` | Return that name to whoever called the function. With the supplied data, it is `Gotham Catering Co.`. |

    **No LLM is needed inside this function.** Calling it directly runs ordinary Python on your PC. An agent can also call it: the model chooses the action, Python returns the name, and the result becomes an observation.

## B. Create a direct tool-check file { #direct-tests }

**Goal:** call the Python tools directly before involving the model. This test does not need a Groq key or internet access.

1. Open **`First_agent_template`** in your code editor.
2. Choose **File → New Text File**, then **File → Save As**. Save it as **`my_tool_check.py`** directly beside `app.py` and `week03_common.py`.
3. Paste the **whole code block below** into the file.
4. Save with **Ctrl + S** on Windows or **Command + S** on Mac. Use the exact `.py` filename, without `.txt`.

**What this file does — `my_tool_check.py`:** Checks the menu, catering, and theme tools by calling them directly with known inputs, including an unknown theme category. It prints PASS only when every returned value satisfies its assertion; otherwise Python stops at the failed check. It uses no LLM and does not need a Groq key.

```python title="my_tool_check.py"
from week03_tools import suggest_menu, catering_service_tool, SuperheroPartyThemeTool

assert suggest_menu(occasion="formal") == "3-course dinner with wine and dessert."
assert catering_service_tool(query="catering") == "Gotham Catering Co."

theme_tool = SuperheroPartyThemeTool()
assert "Gotham Rogues' Ball" in theme_tool(category="villain masquerade")
assert "not found" in theme_tool(category="unknown")

print("PASS: menu, catering, theme, and unknown-category checks.")
```

??? info "Explain my_tool_check.py"

    **This file checks the tools directly, without creating an agent or contacting Groq.**

    | Code | What it means |
    | --- | --- |
    | `from week03_tools import ...` | Load the two supplied functions and the theme-tool class. |
    | `assert suggest_menu(...) == ...` | Call the menu function with `formal` and check that its returned text exactly matches the expected menu. |
    | `assert catering_service_tool(...) == ...` | Call the catering function and check that it returns the expected winning name. |
    | `theme_tool = SuperheroPartyThemeTool()` | Create one theme-tool instance so the next lines can call it. |
    | `assert "Gotham Rogues' Ball" in theme_tool(...)` | Call the instance with `villain masquerade` and check that its result contains the expected theme name. |
    | `assert "not found" in theme_tool(category="unknown")` | Check that an unsupported category gives the fallback message. |
    | `print("PASS: ...")` | Print success only after all the assertions pass. |

    An **assertion** is a check that must be true. If it is false, Python stops with `AssertionError` before printing `PASS`. `==` checks an exact match; `in` checks whether the expected words occur inside the returned text. These checks test the Python tools, not the model's answers.

**Run:** `python my_tool_check.py`.

Expected output:

```text
PASS: menu, catering, theme, and unknown-category checks.
```

If an assertion fails, check that `week03_tools.py` still contains the supplied example data. Fix the local tool first; an LLM answer cannot fix a wrong function.

## C. Create the catering agent { #register }

1. Open **`First_agent_template`** in your code editor.
2. Choose **File → New Text File**, then **File → Save As**. Save it as **`my_catering.py`** directly beside `app.py` and `week03_common.py`.
3. Paste the **whole code block below** into the file.
4. Save with **Ctrl + S** on Windows or **Command + S** on Mac. Use the exact `.py` filename, without `.txt`.

**What this file does — `my_catering.py`:** Runs an agent that answers a request for the highest-rated catering service using the supplied catering function. Groq chooses the tool call; Python compares the fixed fictional ratings and returns the winning name. The tool result and final answer appear in the terminal.

```python title="my_catering.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_tools import catering_service_tool

model = build_model()
agent = CodeAgent(
    tools=[catering_service_tool],
    model=model,
    **agent_options(),
)

task = "Can you give me the name of the highest-rated catering service in Gotham City?"
raise SystemExit(run_task(agent, task))
```

??? info "Explain my_catering.py"

    **This file lets the model use the catering function you just checked.**

    | Code | What it means |
    | --- | --- |
    | `from smolagents import CodeAgent` | Load the class that coordinates model requests, Python actions, and observations. |
    | `from week03_common import ...` | Load the supplied Groq connection, classroom settings, and task runner. |
    | `from week03_tools import catering_service_tool` | Load the supplied decorated function. Its implementation stays in `week03_tools.py`. |
    | `model = build_model()` | Prepare the Groq connection using your key. The task has not run yet. |
    | `agent = CodeAgent(...)` | Create the local agent and give it a model and a tool. |
    | `tools=[catering_service_tool]` | Make the function available to the agent. There are no parentheses here because this line registers the function for later use. |
    | `model=model` | Give the agent the model connection prepared above. |
    | `**agent_options()` | Pass the supplied Python-action instructions, four-step limit, and terminal logging settings into CodeAgent. |
    | `task = "Can you ..."` | Store the question that the model will interpret. |
    | `raise SystemExit(run_task(agent, task))` | Start the agent loop, print the result, and finish with the helper's success/error status. |

    **Follow the work:** the model on Groq proposes a call such as `catering_service_tool(query="catering")`. CodeAgent executes the function on your PC. It returns `Gotham Catering Co.` from the fixed ratings, and the model uses this observation in its answer. Check the trace for the actual call and result.

**Run:** `python my_catering.py`.

Enter your Groq key at the hidden prompt if asked. Find the actual `catering_service_tool(...)` call, its returned `Gotham Catering Co.`, and a final answer using that result.

## D. Read the supplied Tool class { #class-tool }

In the same **`week03_tools.py`**, find `SuperheroPartyThemeTool`. The class is already supplied. Read its fields and `forward(...)` method; keep this code in that file.

```python
class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""

    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }

    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }

        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")
```

??? info "Explain SuperheroPartyThemeTool"

    **A class groups the tool's description and its working Python code together.**

    | Code | What it means |
    | --- | --- |
    | `class SuperheroPartyThemeTool(Tool):` | Define a tool class using smolagents' `Tool` as its base. `Tool` is imported in the supplied file. |
    | `name` | Set the name the model uses to request this tool: `superhero_party_theme_generator`. |
    | `description` | Tell the model when this tool is useful. |
    | `inputs` | Describe the accepted input: a string named `category`, with example categories. |
    | `output_type = "string"` | Tell the framework that the result is text. |
    | `def forward(self, category: str):` | Define the work to do when the tool is called. `self` refers to the tool instance; the caller supplies `category`. |
    | `themes = {...}` | Store three fictional categories and their theme descriptions. |
    | `category.lower()` | Convert the input to lowercase so it matches the dictionary's lowercase keys. |
    | `themes.get(..., "Themed party idea not found. ...")` | Look up the category and return its description. If the key is missing, return the supplied fallback message. |

    For `villain masquerade`, Python returns the stored **Gotham Rogues' Ball** description. **This tool does not generate new ideas with another LLM**; it looks up fixed text on your PC.

    With a function tool, `@tool` uses the function's name, docstring, and type hints to describe the interface. With this class, you write the interface fields explicitly and put the work in `forward(...)`.

## E. Create the party-theme agent { #run-agent }

1. Open **`First_agent_template`** in your code editor.
2. Choose **File → New Text File**, then **File → Save As**. Save it as **`my_theme.py`** directly beside `app.py` and `week03_common.py`.
3. Paste the **whole code block below** into the file.
4. Save with **Ctrl + S** on Windows or **Command + S** on Mac. Use the exact `.py` filename, without `.txt`.

**What this file does — `my_theme.py`:** Runs an agent that answers a party-theme request using an instance of SuperheroPartyThemeTool. Groq chooses a category, and the Python tool retrieves its stored description, such as the villain-masquerade idea. The terminal shows the call, returned description, and final answer.

```python title="my_theme.py"
from smolagents import CodeAgent
from week03_common import build_model, agent_options, run_task
from week03_tools import SuperheroPartyThemeTool

model = build_model()
party_theme_tool = SuperheroPartyThemeTool()
agent = CodeAgent(
    tools=[party_theme_tool],
    model=model,
    **agent_options(),
)

task = "What would be a good superhero party idea for a 'villain masquerade' theme?"
raise SystemExit(run_task(agent, task))
```

??? info "Explain my_theme.py"

    **This file creates an instance of the supplied theme-tool class and gives it to an agent.**

    | Code | What it means |
    | --- | --- |
    | `from smolagents import CodeAgent` | Load the class that manages the model/action/observation loop. |
    | `from week03_common import ...` | Load the Groq connection, classroom settings, and task runner. |
    | `from week03_tools import SuperheroPartyThemeTool` | Load the supplied tool class. |
    | `model = build_model()` | Prepare the connection to Groq using your key. |
    | `party_theme_tool = SuperheroPartyThemeTool()` | Create a tool instance. The parentheses create it; they do not request a theme yet. |
    | `agent = CodeAgent(...)` | Create the agent that will handle the question. |
    | `tools=[party_theme_tool]` | Register that instance as an available tool. Its declared tool name is `superhero_party_theme_generator`. |
    | `model=model` | Give the agent the Groq model connection. |
    | `**agent_options()` | Supply the Python-action instructions, step limit, and terminal logs. |
    | `task = "What would ..."` | Store the user's request for a villain-masquerade party idea. |
    | `raise SystemExit(run_task(agent, task))` | Run the task, print the result, and finish with the returned status. |

    **Follow the work:** Groq's model chooses the tool and the `villain masquerade` input. CodeAgent runs `superhero_party_theme_generator(category="villain masquerade")` on your PC, which uses the instance's `forward(...)` method. The stored description becomes an observation for the model's final answer.

**Run:** `python my_theme.py`.

Find `superhero_party_theme_generator(category="villain masquerade")` in the trace. The returned description should begin `Gotham Rogues' Ball`. Compare the final answer with that observation.

## F. Make one change and run it again { #challenge }

1. In **`week03_tools.py`**, add a fictional service with a rating higher than 4.9 inside the `services` dictionary. Keep the same `"name": rating,` structure.
2. Save the file. Predict which name the tool will now return.
3. In the same activated terminal, run **`python my_catering.py`** again. Read the actual tool result and final answer.
4. The old assertion in **`my_tool_check.py`** still expects `Gotham Catering Co.`. Update that one expected name to your new winner, save, and run **`python my_tool_check.py`** again.

You can also add a lowercase category to the theme dictionary and request that category by editing the `task` sentence in **`my_theme.py`**. Save both files before rerunning the command. You are changing Python data and the question, not training the model.

**Checkpoint:** show the passing direct checks, a catering call, a theme call, and an agent result that reflects your own change.

## Other tool capabilities { #default-toolbox }

Tools can also get user input, read a webpage, or return a final answer. Each capability must be made available to the agent. A web-search tool returns snippets; that is different from controlling a browser.

## Further reading { #integrations }

Tools can be shared or connected to other systems. Those topics are outside this week's practical. You can preview [12 · Building Agentic RAG Systems (optional)](week-3-retrieval.md), or go straight to [13 · Completion checks](week-3-completion.md). RAG will be revisited next week; see [Coming in Week 04](week-4-preview.md).

## Credits { #sources }

Adapted from [Hugging Face Agents Course — Tools](https://huggingface.co/learn/agents-course/en/unit2/smolagents/tools), under the [Apache 2.0 license](licenses/huggingface-agents-course.txt).

**Next:** [13 · Completion checks](week-3-completion.md), or try [12 · Building Agentic RAG Systems (optional)](week-3-retrieval.md).
