from smolagents import CodeAgent, OpenAIServerModel, tool
from getpass import getpass
from pathlib import Path
import os
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool
from tools.web_search import WebSearchTool

from Gradio_UI import GradioUI

# OPTIONAL EXTENSION: Replace this placeholder with a tool of your choice.
# Decide the parameters and return type; update the docstring to match.
# Leave it unregistered until you have implemented and tested it.
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A placeholder for your own tool; implement before registering it.

    Args:
        arg1: Replace with a description of your first input.
        arg2: Replace with a description of your second input.
    """
    raise NotImplementedError("Implement your custom tool before adding it to the agent.")


# A worked example: inspect it, then register it in STUDENT TASK 1 below.
@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


def main():
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        api_key = getpass("Paste your Groq API key (hidden): ").strip()
    if not api_key:
        raise SystemExit("No Groq key entered. Run python app.py again and enter your key.")

    model = OpenAIServerModel(
        model_id="qwen/qwen3.8-27b",
        api_base="https://api.groq.com/openai/v1",
        api_key=api_key,
        client_kwargs={"timeout": 30, "max_retries": 2},
        max_tokens=512,  # Small output budget for introductory exercises.
        temperature=0.5,
        reasoning_effort="none",  # Return the code-agent response without a reasoning preamble.
    )

    with Path(__file__).with_name("prompts.yaml").open(encoding="utf-8") as stream:
        prompt_templates = yaml.safe_load(stream)

    final_answer = FinalAnswerTool()
    agent = CodeAgent(
        model=model,
        # STUDENT TASK 1: Register the existing timezone function and test it.
        # STUDENT TASK 2: Add an instance of WebSearchTool and inspect its results.
        # OPTIONAL EXTENSION: Register your implemented custom tool and verify its output.
        tools=[final_answer],  # Keep final_answer; add completed tools here.
        max_steps=6,
        verbosity_level=1,
        grammar=None,
        planning_interval=None,
        name=None,
        description=None,
        prompt_templates=prompt_templates,
    )
    print("Using Groq: qwen/qwen3.8-27b")
    GradioUI(agent).launch(server_name="127.0.0.1")


if __name__ == "__main__":
    main()
