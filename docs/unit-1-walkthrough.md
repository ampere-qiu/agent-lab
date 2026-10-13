# Agent foundations and quick quizzes

Read this local lesson after [basic setup](prepare-your-computer.md). The explanations and instructions needed for this adaptation are provided here. Hugging Face is credited as source material and optional further reading; access to its lesson pages is not needed to proceed.

## 1. What is an agent?

An agent is a program that uses a model to choose actions toward a goal, executes those actions through software, and uses the results to decide what happens next.

For example, a model can generate a plausible time in Tokyo. An agent can instead select a timezone function, execute it, and use the returned value. The actual function call supplies information that text generation alone does not establish.

The **goal** is what you want to achieve. A **tool** is an available capability. An **action** is a particular use of that capability, such as calling the time function with `Asia/Tokyo`. Planning means choosing suitable steps; a simple task may need just one.

Not every program needs an agent. A fixed calculation with known inputs is often simpler as a direct function call. An agent is useful when different requests require different capabilities or several decisions.

## 2. Quick Quiz 1

Complete [Hugging Face Quick Quiz 1](https://huggingface.co/learn/agents-course/en/unit1/quiz1), then return here. We retain the original interactive activity rather than reproduce its questions. If temporarily unavailable, continue reading and retry later.

## 3. The model, provider, and local program

A large language model (LLM) generates text from the context supplied to it. Training gives it language patterns and broad knowledge, but a fluent answer can still be incorrect or out of date. It does not automatically know the current state of your computer or a website.

In this course, Qwen is the model, Groq serves it through an API, and your Python program sends requests. An API is a defined interface for programs to exchange requests and responses. Your Groq key authenticates those requests.

Models process **tokens**, units of encoded text that can represent parts of words or punctuation. Input tokens include instructions and conversation history; output tokens are generated text. These usage tokens differ from your API key, sometimes called an access token.

Adding earlier results to a request provides context but increases usage. The model has a finite context capacity. Sending a message does not train or update its weights.

## 4. Messages and roles

The API accepts a list of messages, each with a role and content:

```python
messages = [
    {"role": "system", "content": "Answer briefly and state when information is missing."},
    {"role": "user", "content": "What information would you need to tell me the local time?"},
]
```

A **system** message supplies instructions; a **user** message supplies the task. An **assistant** message records a model response and can be included in later requests. The service applies the model's chat formatting to distinguish these roles. Special tokens can mark role boundaries or the end of a sequence. You do not manually paste such markers into our message dictionaries.

In the dummy exercise you add an observation yourself. In the full agent, smolagents manages the history.

## 5. Tools and descriptions

A tool is executable code with a purpose, inputs, and output. It may use local data or contact an external service.

| Core tool | Input | Result source | Evidence to inspect |
| --- | --- | --- | --- |
| Timezone lookup | A timezone such as `Asia/Tokyo` | Computer clock and timezone rules | The function call and returned time |
| Web search | A search query | An external search service | Search execution and relevant returned sources |

The model uses descriptions to select a capability and construct inputs. A description does not implement the function. Defining the function does not register it with the agent, and naming it in generated text does not prove execution.

Search results need checking. Open a returned page, prefer primary sources, and inspect dates when relevant. A URL generated from model memory is not evidence of a search.

## 6. Quick Quiz 2

Complete [Hugging Face Quick Quiz 2](https://huggingface.co/learn/agents-course/en/unit1/quiz2), covering models, messages, and tools. These two quick quizzes are the quiz activities for this adaptation. The account-gated final quiz and certification flow are outside its scope.

## 7. The action–observation loop

1. Send the task, instructions, and available capabilities to the model.
2. Receive a proposed action.
3. Execute that action through the program.
4. Record its result or error as an observation.
5. Supply that observation to the model, which can propose another action or finish.

This connects reasoning about a task with acting on it, often discussed as ReAct. Displayed “Thought” text is a generated explanation, not proof of execution or a complete account of internal reasoning. Inspect actual calls and results.

Actions can be structured data naming a function and its inputs, or code. The dummy exercise describes an action in text; the full `CodeAgent` generates Python for the framework to execute. These formats are not interchangeable API settings.

An observation can be an error, such as an invalid timezone or blocked search. Preserve that distinction rather than presenting a guess as a verified result. A step limit bounds the loop but does not guarantee correctness.

## 8. Put the concepts into practice

[Build the dummy example in three stages](dummy-agent-local.md), then [download the starter](run-your-first-agent.md), [understand its components](understand-the-template.md), and [enable time and web search](first-agent-practical.md).

Finish by showing that both tools ran and explaining their results. A custom tool is optional. Image generation has been removed.

Source and optional further reading: [Hugging Face Agents Course Unit 1](https://huggingface.co/learn/agents-course/en/unit1/introduction). These local explanations are written for our Groq-based exercise, not copied verbatim from the source.
