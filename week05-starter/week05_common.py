"""Local settings and a short, visible tool trace for the Week 5 lessons."""
# Week 5 starter version: 2026-11-10.2
import asyncio
import os
from pathlib import Path
import re
import traceback

from dotenv import load_dotenv

STARTER_VERSION = "2026-11-10.2"
ROOT = Path(__file__).resolve().parent


def get_llm():
    from llama_index.llms.groq import Groq

    load_dotenv(ROOT / ".env", override=False)
    key = os.getenv("GROQ_API_KEY", "").strip()
    model = os.getenv("GROQ_MODEL", "").strip().removeprefix("groq/")
    if not key or not model:
        raise SystemExit("Create .env beside week05_common.py with GROQ_API_KEY and GROQ_MODEL.")
    return Groq(
        model=model, api_key=key, temperature=0, max_tokens=600,
        timeout=45, max_retries=0,
        additional_kwargs={"reasoning_effort": "none"},
    )


async def show_agent(agent, prompt, ctx=None):
    from llama_index.core.agent.workflow import ToolCallResult

    print("REQUEST:", prompt)
    # The workflow runtime can omit memory while restoring a completed Context.
    # Carry the existing object explicitly so previous messages reach the model.
    memory = await ctx.store.get("memory", default=None) if ctx is not None else None
    handler = agent.run(user_msg=prompt, ctx=ctx, memory=memory, max_iterations=6)
    async for event in handler.stream_events():
        if isinstance(event, ToolCallResult):
            print("TOOL:", event.tool_name, event.tool_kwargs)
            result = str(event.tool_output)
            print("RETURN:", result[:2600])
            if len(result) > 2600:
                print("[Terminal output clipped; inspect the original source file.]")
    response = await handler
    print("ANSWER:", final_answer_text(response))
    return response


def final_answer_text(response):
    """Display final text without model thinking tags or their duplicated prefix."""
    text = str(response)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S | re.I)
    if re.search(r"</think>", text, flags=re.I):
        text = re.split(r"</think>", text, flags=re.I)[-1]
    text = re.split(r"<think>", text, flags=re.I)[0].strip()
    return text or "No final answer was returned. Record this run as incomplete."


def save_diagram(workflow, filename):
    """Export HF's workflow drawing without launching the operating-system browser."""
    from llama_index.utils.workflow import draw_all_possible_flows
    from pyvis.network import Network
    from unittest.mock import patch

    def export_only(network, name, notebook=False):
        network.cdn_resources = "in_line"
        network.height = "70vh"
        network.width = "100%"
        result = network.write_html(name, notebook=notebook, open_browser=False)
        # Pyvis embeds the graph library but still adds Bootstrap CDN tags.
        # This plain graph has no Bootstrap controls; remove those unused tags.
        path = Path(name)
        html = path.read_text(encoding="utf-8")
        html = re.sub(
            r'<link\b[^>]*href="https://cdn\.jsdelivr\.net/npm/bootstrap@[^"]+"[^>]*>',
            "", html, flags=re.I | re.S,
        )
        html = re.sub(
            r'<script\b[^>]*src="https://cdn\.jsdelivr\.net/npm/bootstrap@[^"]+"[^>]*>\s*</script>',
            "", html, flags=re.I | re.S,
        )
        # Fit once after stabilization and provide an accessible manual reset.
        controls = """
<div style="clear:both;padding:12px;font-family:sans-serif">
  <button type="button" id="fit-diagram">Fit diagram</button>
  <span>Drag empty space to pan. Scroll or pinch to zoom. Use Fit diagram to see every node.</span>
</div>
<script>
(function () {
  function fitDiagram() { network.fit({animation: false}); }
  network.once('stabilized', fitDiagram);
  window.addEventListener('load', fitDiagram);
  window.addEventListener('resize', fitDiagram);
  document.getElementById('fit-diagram').addEventListener('click', fitDiagram);
  fitDiagram();
})();
</script>
"""
        html = html.replace("</body>", controls + "</body>")
        path.write_text(html, encoding="utf-8")
        return result

    with patch.object(Network, "show", export_only):
        draw_all_possible_flows(workflow, filename=str(filename))


def local_error_message(error):
    message = str(error)
    key = os.getenv("GROQ_API_KEY", "")
    if key:
        message = message.replace(key, "[key hidden]")
    return re.sub(r"gsk_[A-Za-z0-9_-]+", "[key hidden]", message)[:700]


def run(main):
    try:
        asyncio.run(main())
    except Exception as error:
        # Print a diagnosis, not raw service responses or credentials.
        status = getattr(error, "status_code", None)
        cause = error.__cause__ or error.__context__
        local_error = error
        for _ in range(5):
            if cause is None or status is not None:
                break
            local_error = cause
            status = getattr(cause, "status_code", None)
            cause = cause.__cause__ or cause.__context__
        advice = {
            401: "Check your Groq key locally.",
            403: "Check model permission in your Groq account.",
            404: "Check GROQ_MODEL against Groq's current model list.",
            413: "Input too large. Keep the small dataset and short task.",
            429: "Stop and check Groq limits/credits and Retry-After. Waiting does not add credits or guarantee success.",
        }.get(status)
        if advice is None:
            if isinstance(local_error, ModuleNotFoundError):
                advice = local_error_message(local_error) + " Activate .venv and run python -m pip install -r requirements.txt."
            elif isinstance(local_error, (FileNotFoundError, NotADirectoryError, ValueError, NameError, TypeError)):
                advice = local_error_message(local_error) + " Check the named file/data and the lesson's matching code block."
            elif isinstance(local_error, (TimeoutError, ConnectionError)):
                advice = "Connection or workflow timed out. Check internet access and the last completed step."
            else:
                advice = "Check the last printed step and the setup troubleshooting table. Do not repeatedly restart."
            frames = traceback.extract_tb(local_error.__traceback__)
            student_frames = [frame for frame in frames if Path(frame.filename).name.startswith("my_")]
            if student_frames:
                frame = student_frames[-1]
                advice = f"{Path(frame.filename).name}:{frame.lineno}: " + advice
        raise SystemExit(f"Run incomplete ({status or type(error).__name__}). {advice}") from None


if __name__ == "__main__":
    print(f"Week 5 starter version: {STARTER_VERSION}")
