<div class="course-hero" markdown>

<p class="eyebrow">Agent Lab / Week 01</p>

# Build your first AI agent

Understand the model. Connect the tools. Watch your agent take action.

A local course adapted from Hugging Face’s Agents Course and starter template.

[Start the setup](prepare-your-computer.md){ .md-button .md-button--primary }
[Continue to the lessons](unit-1-walkthrough.md){ .md-button }

<p class="course-meta">Windows & Mac · Local app, remote LLM · Local lessons · Two quick quizzes</p>

</div>

## About this adaptation

This lesson borrows and adapts the starter template from the [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction). Because API access, model availability, and hosting requirements affected the original setup, this version runs locally and uses **Groq** for model calls. It still uses Hugging Face's **smolagents** Python library.

**Image generation has been removed.** The core practical uses two tools: **timezone lookup** and **web search**. Creating your own tool is an optional extension.

The learning material and executable instructions are provided on this local site. External HF lesson pages are optional references. We retain only the two quick quizzes; the account-gated final quiz and certification are not part of this adaptation.

During our original setup, free Space duplication was unavailable and HF inference later returned a no-credit error. A local interface does not make remote inference unlimited. Use your own Groq key and check [current usage limits](https://console.groq.com/docs/rate-limits).

## Course route

New to terminals or editing Python? Read [Before you start](before-you-start.md) first. It explains which window to use, how to locate files, and how to save edits.

1. [Prepare Python, the dummy exercise folder, and your Groq key](prepare-your-computer.md).
2. [Read the local lessons and complete the two quick quizzes](unit-1-walkthrough.md).
3. [Build the dummy exercise in three stages](dummy-agent-local.md).
4. [Download and run the full template](run-your-first-agent.md), then [understand its components](understand-the-template.md).
5. [Build and test your agent’s tools](first-agent-practical.md).
6. [Review your practical completion checks](quizzes.md#finish-the-practical).

**The full template comes after the dummy exercise.** Students first see how a model call, a function, and an observation fit together; then CodeAgent automates that loop.

[Get the agent template →](run-your-first-agent.md){ .md-button .md-button--primary }

The quick-quiz links open the original activities. All other steps can be followed using this local guide.

## Environment changes

| Original instruction | Local equivalent |
| --- | --- |
| Duplicate a Space | Download the adapted Groq starter ZIP |
| Add an HF_TOKEN Space secret | Enter your Groq key at startup |
| Edit files in the Space | Edit the downloaded files |
| Wait for the Space to rebuild | Save, stop, and restart the local app |
| Open the hosted app | Open the printed local address |
| Publish/share a Space | Demonstrate the local app; hosting is optional |

The sequence still moves from concepts to a manual dummy loop and then a framework-based agent. The template retains attribution to its source; provider choice, hosting, tool scope, and assessment access are adapted.

## Version note

The Groq starter uses `OpenAIServerModel`, `smolagents==1.13.0`, and `qwen/qwen3.8-27b` through Groq. The current online tutorial uses a different model connection. Use the supplied local starter for executable edits. Complete the response and tool checkpoints on your machine; changing provider/model can change behavior.

## Model compatibility update

The earlier GPT-OSS configuration returned “Tool choice is none, but model called a tool” during a live test. The course's CodeAgent expects Python code in text; a native API function call is a different format. Groq documents this possible [tool-choice rejection](https://console.groq.com/docs/tool-use/local-tool-calling). The updated starter uses [Qwen 3.8 27B](https://console.groq.com/docs/model/qwen/qwen3.8-27b) with reasoning disabled and explicit code-format instructions. It is currently a preview model with [free-plan limits](https://console.groq.com/docs/rate-limits); availability and behavior must be checked before class.
