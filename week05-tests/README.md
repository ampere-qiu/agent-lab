# Week 5 verification

Use a Python 3.11 environment with `week05-starter/requirements.txt` installed.

```bash
python scripts/package_week05.py
python -m unittest discover -s week05-tests -v
python -m mkdocs build --strict
python -m unittest discover -s tests -v
```

The lesson suite extracts the actual ZIP and creates student programs from the titled
Markdown blocks. It tests the real workflow, tool and Chroma APIs. Routine tests use
MockEmbedding and simulated Groq replies, never a secret key or paid requests.

Regressions from the live student audit are covered explicitly:

- The second Bob request must actually contain the original user message; the fresh
  context must not. Checking for Bob anywhere in the output is insufficient.
- QueryEngineTool results must preserve verbatim source-node text and filenames
  separately from generated prose, for synchronous and asynchronous calls.
- Ingestion works under a hidden parent folder, reports missing data, refuses an
  incomplete saved index, and does not duplicate a successful ingestion on rerun.
- Diagram export writes HTML without calling the operating-system browser.
- Local diagnostics name the problem and protect credentials; raw API replies are
  not echoed as troubleshooting text.

The first live macOS/Python 3.11 student audit found faults missed by the mocked
suite. Its baseline logs and two audit-only adjustments are preserved separately in
`output/week05-student-audit-20261109` beside the repository. Fixes now live in the
English lessons and starter helpers. Live recheck results are kept separately so
those baseline failures are not overwritten.

Windows execution remains unverified. Week 5 now includes an authored Japanese edition with identical code/prompts and
matching sections. Existing Weeks 3/4 exercises and their ZIPs remain unchanged.

The ZIP also contains eight unchanged HF Unit 2.2 figures and their source/checksum
manifest. Packaging checks verify the original bytes and offline relative image links.

The copied .env provider prefix and inherited model settings are tested without
remote calls. Diagram checks reject external script/stylesheet tags, verify the
installed pyvis version/dependency, and still prevent OS browser launch. The helper
version command is checked against the setup, memory and drawing instructions.

Remaining-audit regressions cover HTTP 503 and truncated-row fallback using real
Parquet bytes, original-file checksum rejection, local-first embedding loading,
thinking-tag cleanup, exact query-line restoration and bounded search claims.
A live cached-embedding check with socket connections blocked is recorded in
the separate audit output, along with a real original-file fallback download.

Bilingual checks compare every fenced block, including indented optional
comparison/restoration lines, across both authored editions. They verify Japanese
figure-panel placement, offline lesson links, and unchanged figure checksums in
both built sites. The shared helpers mean the validated programs stay identical.
