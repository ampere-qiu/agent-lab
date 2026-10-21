# Understand smolagents and the template { #understand-smolagents-and-the-template }

Read this after your first successful response and before adding tools. Keep `app.py` open beside the guide. By the end, you should be able to explain which component generates text, which executes an action, and where to add your own capability.

## 1. What is smolagents? { #1-what-is-smolagents }

**smolagents is a Python library for building agents, developed by Hugging Face.** A library is reusable code you import into your program. Here, it provides the machinery for asking a model what to do, executing an action, recording the result, and continuing toward an answer. Its `CodeAgent` represents actions as Python code. See the [smolagents introduction for version 1.13.0](https://huggingface.co/docs/smolagents/v1.13.0/en/index), which matches this starter.

In the dummy exercise, you assembled messages, called the LLM, ran a weather function, and returned its result. The template lets a framework manage that sequence. You still choose the model, provide tools, and check the outcome.

We continue using Hugging Face's **library** and course material while using **Groq's API** for model requests. Installing smolagents does not require hosting a Space or buying Hugging Face inference credits for this configuration.

## 2. Which component does what? { #2-which-component-does-what }

An *agent* in this project is the complete arrangement of model, instructions, available actions, and execution loop.

| Component | Job in this template | Runs where? |
| --- | --- | --- |
| Qwen model | Generates the next response, including proposed Python actions | Remotely, through Groq |
| Groq API | Receives authenticated requests and returns model output | Groq's service |
| `OpenAIServerModel` | Adapts smolagents messages to the compatible API | Your Python process |
| `CodeAgent` | Coordinates model requests, Python execution, and observations | Your Python process |
| A registered tool | Performs a capability you make available, such as looking up a time | Called locally; some tools contact another service |
| Gradio | Provides the browser chat interface | A local web server plus your browser |

The word “OpenAI” in `OpenAIServerModel` names an API-compatible connection class. In this template its address points to Groq, and its key is a Groq key. You do not need an OpenAI account.

The time tool reads your computer's clock and applies a timezone. The search tool sends a request to an external search service. Both are Python capabilities; their sources of information differ.

## 3. From a message to an answer { #3-from-a-message-to-an-answer }

The arrows below show the two-way flow. The same local agent makes each model request.

```text
Browser chat
    ↓ user message
Gradio → CodeAgent on your computer
              ↓ instructions + task + earlier observations
         Groq → Qwen model
              ↓ model response containing Python code
         Local Python execution
              ↓ result or error recorded as an observation
         CodeAgent → another model request if needed
              ↓ final_answer(...) completes the task
Browser displays the result
```

For example, after you register the timezone tool, an action could contain:

```python
current_time = get_current_time_in_timezone("Asia/Tokyo")
print(current_time)
```

The **model generates that code**. The **local executor runs it**. Its output becomes an **observation** that can be included in the next request. The model might then generate `final_answer(...)` to finish. It can also call a tool and finish within one code block, so every task does not have the same number of steps.

This explains why one chat message can consume multiple API requests. It also explains why a model saying “I checked the time” is insufficient evidence: look for the executed call and its result.

### What CodeAgent handles automatically { #what-codeagent-handles-automatically }

Yes: **CodeAgent manages the action–observation loop for you.** The model chooses proposed actions; the framework runs the generated Python locally and records the result.

| Responsibility | Who handles it? |
| --- | --- |
| Write the tool's function and describe its inputs | You |
| Register the function in `tools=[...]` | You |
| Supply registered tool names and descriptions in the model's instructions | CodeAgent |
| Choose whether to use a tool and generate Python arguments | The model |
| Execute the Python, call the tool, and record output or errors | CodeAgent's local executor |
| Include observations in later requests when another step is needed | CodeAgent |
| Generate code calling `final_answer(...)` | The model |
| Finish the run and return the final result | CodeAgent |

For a request such as “Use the time tool for Asia/Tokyo,” CodeAgent supplies the task and the registered tools to the model, executes the proposed call, and continues if needed. The run can end with a final answer, reach its step limit, or stop because of an error. Registration and automatic execution do not guarantee correct choices or correct answers.

The dummy exercise asked you to inspect an action and call a hard-coded function yourself. Here, CodeAgent handles that execution loop. A simple Python calculation such as `12 * 8` uses the built-in executor; a real search needs a registered search tool. Neither a generated “Thought” nor a function name appearing in text proves execution.

Follow [how tools are connected and selected](first-agent-practical.md#how-does-the-agent-know-which-tools-it-can-use) and [the new-tool example](first-agent-practical.md#6-optional-create-your-own-tool) in the practical to see where each part is edited.

## 4. What does the downloaded template provide? { #4-what-does-the-downloaded-template-provide }

The template is a starting program with the connection and interface already assembled. It can answer a simple question immediately. The student version deliberately leaves the two core tools (time and web search) unregistered. The unfinished custom tool is an optional extension. Image generation has been removed.

| File | Purpose | What you do with it |
| --- | --- | --- |
| `app.py` | Defines tools, configures Groq, creates the agent, and launches the interface | Main file for your practical edits |
| `Gradio_UI.py` | Passes chat messages to the agent and displays steps, answers, and errors | Read to trace the interface; no edits needed for the tasks |
| `prompts.yaml` | Stores text templates for instructions and response formatting | Inspect after the basic tool tasks |
| `tools/web_search.py` | Adapts the DDGS client to a smolagents tool, using the DuckDuckGo backend | Register its `WebSearchTool` class in the practical |
| `tools/final_answer.py` | Defines the final-answer tool used by this starter | Keep it available |
| `requirements.txt` | Lists Python packages and version constraints | Install with the supplied setup command |
| `STUDENT_TASKS.md` | Lists the tool activities and completion checks | Use alongside the practical |
| `.venv/` | Holds your locally installed Python environment | Created during setup; not part of the downloadable code |

The template contains neither the model's weights nor your API key. Downloading it does not download an LLM onto your laptop.

## 5. Read app.py in execution order { #5-read-apppy-in-execution-order }

### Imports and function definitions { #imports-and-function-definitions }

`from smolagents import ...` makes library components available to this program. Defining `get_current_time_in_timezone` creates a callable tool, but does not fetch the time at startup. Similarly, importing `WebSearchTool` does not perform a web search.

The custom placeholder raises `NotImplementedError` if called. This is intentional: implement it before registering it. The initial app runs because it does not expose that placeholder to the agent.

### main() and the startup guard { #main-and-the-startup-guard }

At the bottom of the file:

```python
if __name__ == "__main__":
    main()
```

Running `python app.py` triggers `main()`. Importing `app` from a tool-test script defines its functions without launching the chat. That lets you test your own tool independently.

### The key prompt { #the-key-prompt }

`main()` checks the `GROQ_API_KEY` environment variable first. If it is empty, `getpass(...)` asks for a key without displaying it. The key authorizes API requests. It is different from the input and output *tokens* that measure text usage.

The app does not save a key entered at the prompt. You enter it again after restarting unless you configured the environment variable separately.

### The model connection { #the-model-connection }

These are the working starter's settings, shown for explanation rather than as a replacement block:

```python
model = OpenAIServerModel(
    model_id="qwen/qwen3.8-27b",
    api_base="https://api.groq.com/openai/v1",
    api_key=api_key,
    client_kwargs={"timeout": 30, "max_retries": 2},
    max_tokens=512,
    temperature=0.5,
    reasoning_effort="none",
)
```

| Setting | Meaning |
| --- | --- |
| `model_id` | Exact identifier of the model requested from the service |
| `api_base` | Address to which the client sends requests |
| `api_key` | Credential supplied at startup |
| `max_tokens` | Maximum output per completion. We start with 512 tokens for short exercises; this must fit your account allowance and is not a daily usage budget. |
| `client_kwargs` | Each network attempt has a 30-second timeout; up to two automatic retries handle temporary failures and short rate-limit waits. Longer limits can still stop the run. |
| `temperature` | Sampling setting affecting variation; it does not measure accuracy |
| `reasoning_effort` | A model-specific option configured here to disable the model's separate reasoning mode |

Keep these settings for the initial practical. Changing the model may change supported options and response format. It does not automatically give you a larger usage allowance.

### Instructions and agent construction { #instructions-and-agent-construction }

The program reads `prompts.yaml` next to `app.py`, then constructs `CodeAgent`. The important arguments are:

```python
model=model,
tools=[final_answer],
max_steps=6,
prompt_templates=prompt_templates,
```

`model` selects the connection. `tools` supplies the explicit capabilities available to the agent. `max_steps` limits its action-loop iterations for a task; it is not a guarantee of success or an exact cap on total API calls. `prompt_templates` supplies instructions for those interactions. The versioned [agent reference](https://huggingface.co/docs/smolagents/v1.13.0/en/reference/agents) documents these parameters and the distinction between Python-code agents and JSON tool-calling agents.

The starter also supplies several optional settings as `None`, including planning and managed-agent metadata. You do not need to change them to complete the tools exercise. `verbosity_level=1` controls logging detail.

### Launching the interface { #launching-the-interface }

`GradioUI(agent).launch(server_name="127.0.0.1")` starts the local interface. Starting this server does not itself request an answer from the LLM. Sending a chat message triggers `agent.run(...)` in `Gradio_UI.py`.

The URL is local, but model requests still travel over the internet. Stopping the Python process stops the app. Refreshing a browser page does not reload changed Python files; restart the program after code edits.

## 6. How does a function become a tool? { #6-how-does-a-function-become-a-tool }

A useful function must exist, describe its inputs and purpose, and be registered with the agent.

```python
@tool
def get_current_time_in_timezone(timezone: str) -> str:
```

`@tool` is a Python decorator: it wraps the function with information smolagents can use. The type hints describe the expected argument and return types. The docstring describes the capability and its arguments. These descriptions help the model select a function and construct inputs; they do not implement its behavior. The [versioned tools guide](https://huggingface.co/docs/smolagents/v1.13.0/en/tutorials/tools) explains this interface.

Registering the existing function means adding its name to `tools`. Use the name without calling it: calling it yourself would produce a result immediately instead of registering the capability. `WebSearchTool()` is different syntax because it creates an instance of a supplied tool class.

For the optional custom-tool extension, you must still write the function body and verify its return value. Accurate documentation cannot repair an incorrect calculation. A sensible test order is **direct function call → registration → agent request → trace inspection**. See [the optional new-tool walkthrough](first-agent-practical.md#6-optional-create-your-own-tool) for a complete example with a description, a test file, registration, and a chat request.

## 7. Why final_answer is already included { #7-why-final_answer-is-already-included }

In the template, `final_answer = FinalAnswerTool()` creates the object registered under that name. Generated Python such as `final_answer(96)` signals completion and supplies the result to display. This function does not make an additional LLM request on its own.

That is why a greeting can show a `python_interpreter` step even when it needs no search or external lookup: this CodeAgent may execute a small Python block that calls `final_answer`.

The initial agent can use its Python executor for simple calculations even though its explicit tools list contains only the final-answer tool. Registering search or your timezone function adds those specific capabilities.

## 8. Read the trace and understand the limits { #8-read-the-trace-and-understand-the-limits }

| What you see | What it tells you |
| --- | --- |
| Model commentary or “Thought” | Generated explanation; not proof of an action or a complete account of internal reasoning |
| Code | The action proposed by the model |
| `python_interpreter` | The framework executing generated Python |
| Observation / execution output | Information returned by execution, including possible errors |
| Final answer | The reported result; still check it against the observations |
| Input/output token counts | Text usage for model requests, not the API key |

The UI preserves the agent's history between messages in the running app. Later requests can therefore contain previous steps as context, increasing usage. Restart the app when you want an independent experiment with fresh agent memory. This conversation history is not model training.

An error before a model response suggests a connection, access, request-format, or usage-limit issue. An error while executing code suggests a problem with generated arguments, tool code, registration, or execution permissions. Follow the [troubleshooting table](run-your-first-agent.md#troubleshooting) for the corresponding layer.

## 9. Before you start editing { #9-before-you-start-editing }

Use these as reading checks, not an additional graded quiz:

- Locate the line that chooses the remote model and the line that chooses local tools.
- Explain why importing a search class does not enable searching.
- Trace one answer from the chat input through an action to the displayed result.
- Identify the optional custom-tool placeholder and the two core capabilities you need to register.

**Next:** [Build and test your agent's tools](first-agent-practical.md). The core tasks are time and web search; implementing a custom tool is optional.
