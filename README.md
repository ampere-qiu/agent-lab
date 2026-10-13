# Agent Lab

A local-computer adaptation of Hugging Face Agents Course Unit 1, with MkDocs lessons and a downloadable Groq agent starter.

Students read the website, download the starter, and run the Python app on their own computers using their own Groq key. GitHub Pages hosts the lessons and download; it does not run the agent or require a Groq secret.

## Publish

Follow [PUBLISHING.md](PUBLISHING.md). The included workflow rebuilds the website when main changes.

## Edit and preview

Install requirements-docs.txt in a Python 3.11 virtual environment, then run:

    python -m mkdocs serve

Edit lesson files under docs/. The student download is docs/downloads/groq-agent-starter.zip. Update the download as well if changing its code.

## Attribution and scope

Adapted from the [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction) and [First_agent_template](https://huggingface.co/spaces/agents-course/First_agent_template). Source notices are retained. This adaptation changes hosting and inference setup, removes image generation, and focuses on time and web search. Only the original two quick quizzes are retained.

The starter uses smolagents, Gradio, and Groq-hosted inference. External search is intermittent; students must verify returned evidence. The Mac path was tested; Windows installation remains untested.
