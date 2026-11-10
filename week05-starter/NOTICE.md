# Week 5 source and adaptation notes

This English/Japanese classroom adaptation follows Hugging Face Agents Course Unit 2.2:
https://huggingface.co/learn/agents-course/en/unit2/llama-index/introduction

Examples are adapted from the Apache-2.0 licensed course notebooks:
https://huggingface.co/agents-course/notebooks/tree/main/unit2/llama-index
See HF-LICENSE.txt. The example order, persona search, demo weather, arithmetic,
Bob memory, event workflows and shared counter follow those sources.

Local adaptations: Python 3.11 scripts with asyncio entry points; existing classroom
Groq account; explicit .env loading; small bounded tasks; deterministic loop;
local ToolSpec instead of connecting a personal Gmail account; workflow drawing saved to HTML. Local helper code and guided explanations are classroom additions.

The dataset is downloaded separately from dvilasuero/finepersonas-v0.1-tiny:
https://huggingface.co/datasets/dvilasuero/finepersonas-v0.1-tiny
No dataset records or model weights are redistributed in this starter. The downloader
preserves the first ten persona texts; they describe profiles, not verified people.
The embedding model is downloaded from BAAI/bge-small-en-v1.5 on first use:
https://huggingface.co/BAAI/bge-small-en-v1.5

Audit corrections: explicitly carry conversation memory between context runs;
preserve original source nodes beside generated query-engine answers; load the ten
intended persona paths explicitly; name missing/partial-data errors; provide local
model-cache placement and download progress; save diagrams without browser launch.
The lesson sequence and credited HF examples are retained.

Original HF Unit 2.2 figures are included unchanged in images/huggingface-week05.
The adjacent sources.json records the original lesson, immutable image URL,
upstream revision and SHA-256 for each file. Explanations below the figures are
classroom additions; labels in the original figures are explained where needed.

Starter 2026-11-10.2 accepts the older leading groq/ provider prefix, pins pyvis
explicitly, and removes unused Bootstrap CDN tags from the plain workflow graph
so the saved diagram can be viewed offline. Setup and recovery guidance are updated.

Starter 2026-11-10.2 reads the original dataset Parquet as a fallback when the
rows service cannot return complete text. The dataset revision, file checksum
and actual source are recorded in the downloader/provenance. No dataset content
is bundled. A complete embedding cache is used with local_files_only=True.
Terminal-only output cleanup omits model thinking markup; original workflow
responses and conversation memory are not rewritten. Diagram fitting and
bounded missing-match guidance are classroom additions.

The authored Japanese lessons use matching section IDs and identical program,
command and comparison blocks. Japanese explanations accompany unchanged English
figures and literal output. Both lesson editions share these support files.
