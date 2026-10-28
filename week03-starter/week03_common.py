"""Shared Week 3 setup. Reuses the Week 2 environment and Groq settings."""
from copy import deepcopy
from getpass import getpass
import os

from smolagents import CodeAgent, OpenAIServerModel
from smolagents.agents import EMPTY_PROMPT_TEMPLATES

MODEL_ID = "qwen/qwen3.8-27b"
SYSTEM_PROMPT = """You complete short course exercises using Python actions.
Return only a short action description followed by Code: and a fenced Python block.
End each block with <end_code>, for example:
Code:
```py
print(2 + 2)
```<end_code>
The Python runs on the user's PC. Never use native API tool calls or JSON actions.
Use print(...) to inspect tool results, then final_answer(...) to finish.
Call the requested tool; do not calculate its result yourself or invent observations.
Menu, catering and themes are fictional demonstration data.
Only the web_search tool retrieves live web results. Cite URLs returned by it.
Only these tools are registered:
{% for tool in tools.values() %}
{{ tool.name }}: {{ tool.description }}
Inputs: {{ tool.inputs }}. Output type: {{ tool.output_type }}.
{% endfor %}

Allowed imports: {{ authorized_imports }}.
"""


def build_model():
    """Ask for the same Groq key used in Week 2; do not save it."""
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        key = getpass("Paste your Groq API key (hidden): ").strip()
    if not key:
        raise SystemExit("No Groq key entered. Run the command again and enter your key.")
    return OpenAIServerModel(
        model_id=MODEL_ID,
        api_base="https://api.groq.com/openai/v1",
        api_key=key,
        client_kwargs={"timeout": 30, "max_retries": 2},
        max_tokens=512,
        temperature=0.5,
        reasoning_effort="none",
    )


def agent_options(action_format="python"):
    """Supply the classroom action format and step limit."""
    prompts = deepcopy(EMPTY_PROMPT_TEMPLATES)
    prompts["system_prompt"] = SYSTEM_PROMPT if action_format == "python" else """\
Complete the task using the registered native tools. Make a structured tool call,
not a Python code block. Inspect observations before answering. Use final_answer
to finish. Never invent search results or claim a failed tool succeeded.
Available tools:
{% for tool in tools.values() %}
{{ tool.name }}: {{ tool.description }}
{% endfor %}
"""
    prompts["final_answer"] = {
        "pre_messages": "The step limit was reached. Use only the observed results.",
        "post_messages": "Answer the task briefly; say if execution was incomplete: {{task}}",
    }
    return {"prompt_templates": prompts, "max_steps": 4, "verbosity_level": 1}



def run_task(agent, task):
    """Print an actionable error without exposing raw request data or credentials."""
    from smolagents.utils import AgentError
    try:
        result = agent.run(task)
        print("\nFINAL RESULT:")
        print(result)
        return 0
    except AgentError as error:
        cause = error.__cause__
        status = getattr(cause, "status_code", None)
        if status == 401:
            detail = "Groq rejected the key. Restart and enter a valid Groq key."
        elif status == 429:
            detail = ("Groq rejected this request because of a usage or size limit. "
                      "Pause before retrying; for Request too large, shorten the task/history "
                      "or reduce max_tokens. See the Week 2 troubleshooting guide.")
        elif status in (403, 404):
            detail = "Check your Groq model permissions and whether the configured model is available."
        else:
            detail = ("Check internet access and the model settings. CodeAgent expects Python "
                      "actions; the separate ToolCallingAgent runner expects native tool calls. "
                      "See the Week 2 troubleshooting guide.")
        print(f"\nMODEL REQUEST FAILED: {detail}")
        print("This run does not complete the live checkpoint. Do not share API keys.")
        return 1
