# Dummy agent: build the loop in three stages

This local exercise adapts the manual-loop idea from the [HF Dummy Agent lesson](https://huggingface.co/learn/agents-course/en/unit1/dummy-agent-library). All code needed is below. The original page is optional reading; Groq replaces its model connection.

You will send a request, inspect a proposed action, execute a function yourself, and send its result back. This is a teaching example, not a general-purpose autonomous agent. The full template comes later.

## Prepare the file

Complete [basic setup](prepare-your-computer.md) and activate the environment in `agent-course/dummy-agent`. In your editor, create `dummy_agent.py` in that folder. Add the blocks below in order, saving after each stage. Run:

```bash
python dummy_agent.py
```

Output appears in the terminal, not a browser chat. Each rerun repeats the requests already in your file and uses your Groq allowance. If you reach a limit, follow the provider's retry interval rather than repeatedly rerunning.

## Step 1. Make a simple LLM call

Put this in the new file:

```python
from getpass import getpass
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=getpass("Paste your Groq API key (hidden): ").strip(),
)
MODEL = "qwen/qwen3.8-27b"

reply = client.chat.completions.create(
    model=MODEL,
    reasoning_effort="none",
    messages=[{"role": "user", "content": "Name the capital city of France."}],
    max_tokens=150,
)
print("STEP 1 — model response:")
print(reply.choices[0].message.content)
```

Save and run it. Paste your key into the hidden terminal prompt and press Enter/Return.

**What happens:** `messages` supplies the user request. The client sends it to Groq. `choices[0].message.content` reads the first returned answer. No weather function has run and no agent framework is involved.

**Checkpoint:** You receive an answer identifying Paris. This tests the model connection. A traceback is a connection or request problem; use [troubleshooting](run-your-first-agent.md#troubleshooting) before continuing.

## Step 2. Inspect a proposed action

Append this block below Step 1:

```python
SYSTEM_PROMPT = """You are demonstrating a text-based action loop.
The available capability is get_weather(location: str).
Describe an action as plain text, not a native API function call.
Use these labels in order:
Action: get_weather(location="city name")
Observation: the result supplied by the Python program
Final Answer: a brief answer using that result
Do not claim that an observation came from a real function unless supplied.
"""
weather_messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Use get_weather to check the weather in London."},
]

proposal = client.chat.completions.create(
    model=MODEL,
    reasoning_effort="none",
    messages=weather_messages,
    max_tokens=250,
)
print("STEP 2A — without a stop marker:")
print(proposal.choices[0].message.content)

stopped_reply = client.chat.completions.create(
    model=MODEL,
    reasoning_effort="none",
    messages=weather_messages,
    max_tokens=250,
    stop=["Observation:"],
)
proposed_action = stopped_reply.choices[0].message.content or ""
print("STEP 2B — stop before the observation:")
print(proposed_action)
```

Save and rerun. You will enter the key again. Compare the two outputs.

**What happens:** the system message describes a capability, but it does not execute it. Without a stop marker, the model might invent a result, state that a result is missing, or simply stop. Do not expect identical wording on every run. The `stop` parameter stops generation if the model reaches the specified marker, reserving that point for feedback from your program.

**Checkpoint:** Inspect Step 2B for a proposed `get_weather` action with London as the input. It should not contain a claimed function result. If it names a different action or city, fix the prompt before proceeding. A stop marker alone does not guarantee the model follows every instruction.

## Step 3. Execute the function and return its observation

Append this block below Step 2:

```python
def get_weather(location: str) -> str:
    """Return fixed demonstration data, not a live weather forecast."""
    return f"Demo weather for {location}: sunny, 18 degrees Celsius."

# Read Step 2B first. This teaching script handles only the London example.
confirmation = input("Does Step 2B request get_weather for London? Type yes: ")
if confirmation.strip().lower() != "yes":
    raise SystemExit("Check the proposed action and prompt before running the function.")

observation = get_weather("London")
print("STEP 3 — actual Python function result:")
print(observation)

follow_up = weather_messages + [
    {"role": "assistant", "content": proposed_action},
    {
        "role": "user",
        "content": (
            "Observation from the Python function: " + observation
            + "\nNow give a final answer. Clearly label this as demo data."
        ),
    },
]
final_reply = client.chat.completions.create(
    model=MODEL,
    reasoning_effort="none",
    messages=follow_up,
    max_tokens=250,
)
print("STEP 3 — model answer using the observation:")
print(final_reply.choices[0].message.content)
```

**What happens:** you verify the proposed action, Python calls the function, and its return value is added to the next model request. The function returns fixed demonstration data so you can trace where the answer came from. No weather API is contacted.

The confirmation is deliberate: this small script does not parse arbitrary model actions or automatically choose functions. Do not paste the generated text into `eval` or `exec`. In the next practical, CodeAgent supplies the execution loop.

**Checkpoint:** The terminal prints the function result before the final model answer. The answer should reflect the supplied sunny/18-degree demonstration data and identify it as demo data. If it contradicts the observation, inspect the final request and prompt rather than treating the answer as verified.

## What you have learned

| Part | Your evidence |
| --- | --- |
| Model request | The first answer came from Groq |
| Proposed action | The model named a function and input |
| Execution | Your Python script actually called `get_weather` |
| Observation | The returned string entered the next request |
| Final response | The model used the supplied result |

This weather function is only a dummy example. The full agent's core tools will be **real timezone lookup and web search**.

**Next:** [Download and run the agent template](run-your-first-agent.md), then [understand how smolagents manages the loop](understand-the-template.md).
