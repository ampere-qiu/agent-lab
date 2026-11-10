"""Run the exact student lesson blocks with real workflow/tool APIs and mocked Groq."""
import ast
import asyncio
from contextlib import redirect_stdout
import importlib.util
import hashlib
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
CODE = re.compile(r'^```python title="([^"\n]+)"\n(.*?)^```', re.M | re.S)


class Week05Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="week05-test-")
        cls.work = Path(cls.temp.name) / "week05-exercises"
        with ZipFile(ROOT / "docs/downloads/week05-llamaindex.zip") as archive:
            archive.extractall(Path(cls.temp.name))
        cls.examples = {}
        for page in sorted((ROOT / "docs").glob("week-5-*.md")):
            for name, code in CODE.findall(page.read_text()):
                ast.parse(code)
                if name in cls.examples:
                    raise AssertionError("Student filename repeated: " + name)
                cls.examples[name] = code
                (cls.work / name).write_text(code)
        sys.path.insert(0, str(cls.work))
        import week05_common, week05_rag
        cls.common = week05_common
        cls.rag = week05_rag

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(str(cls.work))
        # Chroma can retain a process-local client; do not reuse this path.
        cls.temp.cleanup()

    def script(self, name):
        output = subprocess.run([sys.executable, str(self.work / name)], cwd=self.work,
                                text=True, capture_output=True, timeout=30)
        self.assertEqual(output.returncode, 0, output.stdout + output.stderr)
        return output.stdout

    def load(self, name):
        modname = Path(name).stem
        spec = importlib.util.spec_from_file_location(modname, self.work / name)
        module = importlib.util.module_from_spec(spec)
        sys.modules[modname] = module
        spec.loader.exec_module(module)
        return module

    def test_exact_packaged_helpers_and_no_credentials(self):
        with ZipFile(ROOT / "docs/downloads/week05-llamaindex.zip") as archive:
            self.assertEqual(len(archive.namelist()), 36)
            for name in archive.namelist():
                self.assertTrue(name.startswith("week05-exercises/"))
                self.assertNotIn("..", Path(name).parts)
                self.assertNotIn(".env", Path(name).parts)
                self.assertNotIn(".venv", Path(name).parts)
            for path in (ROOT / "week05-starter").iterdir():
                if path.is_file():
                    self.assertEqual(archive.read("week05-exercises/" + path.name), path.read_bytes())
        with ZipFile(ROOT / "docs/downloads/week05-llamaindex.zip") as archive:
            for row in json.loads((ROOT / "docs/images/huggingface-week05/sources.json").read_text()):
                name = "images/huggingface-week05/" + row["file"]
                body = (ROOT / "docs" / name).read_bytes()
                self.assertEqual(hashlib.sha256(body).hexdigest(), row["sha256"])
                self.assertEqual(archive.read("week05-exercises/" + name), body)
            for page in (ROOT / "docs").glob("week-5-*.md"):
                packed = archive.read("week05-exercises/lessons/en/" + page.name).decode()
                for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', packed):
                    if target.startswith("../../images/"):
                        self.assertIn("week05-exercises/" + target.removeprefix("../../"), archive.namelist())
        self.assertEqual(len(self.examples), 18)

    def test_comparison_edits_target_real_lines_and_preserve_valid_programs(self):
        edits = [
            ("my_tools.py", "week-5-tools.md", '    print(weather.call("New York"))', '    print(weather.call("Tokyo"))'),
            ("my_retrieve.py", "week-5-components.md", 'hits = retriever.retrieve("Cincinnati art historian and museum professional")', 'hits = retriever.retrieve("What is this person\'s full legal name?")'),
            ("my_workflow_steps.py", "week-5-workflows.md", '        return ProcessingEvent(intermediate_result="Step 1 complete")', '        return ProcessingEvent(intermediate_result="Step 1 changed by the student")'),
            ("my_rag_agent.py", "week-5-agents.md", '    await show_agent(agent, "Find the persona interested in Cincinnati art. Use personas and quote its description.")', '    await show_agent(agent, "What is 2 times 2? Use multiply.")'),
        ]
        for name, page, old, new in edits:
            original = self.examples[name]
            self.assertEqual(original.count(old), 1)
            self.assertIn(old, (ROOT / "docs" / page).read_text())
            self.assertIn(new, (ROOT / "docs" / page).read_text())
            changed = original.replace(old, new)
            ast.parse(changed)
            self.assertEqual(changed.replace(new, old), original)

    def test_query_comparison_shows_the_exact_original_line(self):
        page = (ROOT / "docs/week-5-components.md").read_text()
        optional = page.split('??? info "Optional: ask about writing or travel"', 1)[1].split("## 5.", 1)[0]
        original = next(line.strip() for line in self.examples["my_query.py"].splitlines() if line.strip().startswith("question ="))
        self.assertIn(original, optional)
        self.assertIn("Two returned passages", optional)

    def test_course_order_and_authored_japanese_edition(self):
        import yaml
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text())
        nav = next(section for section in config["nav"] if "Week 05 · LlamaIndex" in section)
        expected = ["learning-plan", "introduction", "llamahub", "components", "tools",
                    "quiz-1", "agents", "workflows", "quiz-2", "completion"]
        filenames = ["week-5-" + name + ".md" for name in expected]
        self.assertEqual([next(iter(item.values())) for item in nav["Week 05 · LlamaIndex"]], filenames)
        self.assertEqual(config["extra"]["english_only_pages"], [])
        for name in filenames:
            self.assertTrue((ROOT / "docs-ja" / name).exists())

    def test_japanese_code_comparisons_figures_and_zip_match(self):
        def fences(text):
            lines = text.splitlines(keepends=True)
            result = []
            i = 0
            while i < len(lines):
                match = re.match(r"^([ \t]*)```[^\n]*\n?$", lines[i])
                if match:
                    indent = match[1]
                    block = [lines[i]]
                    i += 1
                    while i < len(lines):
                        block.append(lines[i])
                        i += 1
                        if block[-1].rstrip("\n") == indent + "```":
                            break
                    result.append("".join(block))
                else:
                    i += 1
            return result
        with ZipFile(ROOT / "docs/downloads/week05-llamaindex.zip") as archive:
            for page in (ROOT / "docs").glob("week-5-*.md"):
                en = page.read_text()
                ja = (ROOT / "docs-ja" / page.name).read_text()
                self.assertEqual(fences(en), fences(ja), page.name)
                self.assertEqual(CODE.findall(en), CODE.findall(ja), page.name)
                for match in re.finditer(r"^\[!\[[^\n]+\n", ja, re.M):
                    after = ja[match.end():].lstrip()
                    self.assertTrue(after.startswith('??? info "この図の説明を読む"'), page.name)
                for lang in ("en", "ja"):
                    packed = archive.read(f"week05-exercises/lessons/{lang}/{page.name}").decode()
                    for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', packed):
                        if target.startswith("../../images/"):
                            self.assertIn("week05-exercises/" + target.removeprefix("../../"), archive.namelist())
                        if target.startswith("week-5-"):
                            self.assertIn(f"week05-exercises/lessons/{lang}/" + target, archive.namelist())
            for row in json.loads((ROOT / "docs/images/huggingface-week05/sources.json").read_text()):
                for lang in ("", "ja/"):
                    asset = ROOT / "site" / lang / "images/huggingface-week05" / row["file"]
                    self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(), row["sha256"])

    def test_download_validates_rows_and_preserves_existing_work(self):
        module = self.load("prepare_personas.py")
        data = {"rows": [{"row_idx": i, "row": {"persona": f"Profile {i}"}, "truncated_cells": []} for i in range(10)]}
        with tempfile.TemporaryDirectory() as folder, patch.object(module, "ROOT", Path(folder)):
            with patch.object(module, "urlopen", return_value=io.BytesIO(json.dumps(data).encode())):
                module.main()
            self.assertEqual(len(list((Path(folder) / "data").glob("*.txt"))), 10)
            self.assertEqual((Path(folder) / "data/persona_0.txt").read_text(), "Profile 0")
            with self.assertRaises(SystemExit): module.main()
        with tempfile.TemporaryDirectory() as folder, patch.object(module, "ROOT", Path(folder)):
            bad = {"rows": []}
            with patch.object(module, "urlopen", side_effect=lambda *a, **kw: io.BytesIO(json.dumps(bad).encode())):
                with self.assertRaises(SystemExit): module.main()
            self.assertFalse((Path(folder) / "data").exists())

    def test_original_dataset_fallback_handles_503_and_truncated_rows(self):
        import pyarrow as arrow
        import pyarrow.parquet as parquet
        from urllib.error import HTTPError
        module = self.load("prepare_personas.py")
        sink = arrow.BufferOutputStream()
        expected = [f"Complete persona {i}: " + "full text " * 20 for i in range(12)]
        parquet.write_table(arrow.table({"persona": expected, "unused_embedding": list(range(12))}), sink)
        body = sink.getvalue().to_pybytes()
        truncated = {"rows": [{"row_idx": i, "row": {"persona": "cut text"}, "truncated_cells": ["persona"]} for i in range(10)]}
        for primary in [HTTPError("test", 503, "unavailable", {}, None), io.BytesIO(json.dumps(truncated).encode())]:
            with tempfile.TemporaryDirectory() as folder, patch.object(module, "ROOT", Path(folder)):
                with patch.object(module, "PARQUET_SHA256", hashlib.sha256(body).hexdigest()), patch.object(module, "urlopen", side_effect=[primary, io.BytesIO(body)]):
                    module.main()
                self.assertEqual((Path(folder) / "data/persona_9.txt").read_text(), expected[9])
                source = json.loads((Path(folder) / "dataset-source.json").read_text())
                self.assertEqual(source["revision"], module.REVISION)
        with tempfile.TemporaryDirectory() as folder, patch.object(module, "ROOT", Path(folder)):
            with patch.object(module, "urlopen", side_effect=[HTTPError("test", 503, "unavailable", {}, None), io.BytesIO(b"incomplete")]):
                with self.assertRaisesRegex(SystemExit, "checksum"):
                    module.main()
            self.assertFalse((Path(folder) / "data").exists())

    def test_final_answer_hides_thinking_tags_and_duplicate_prefix(self):
        clean = self.common.final_answer_text
        self.assertEqual(clean("The answer is 8.\n</think>\nThe answer is 8."), "The answer is 8.")
        self.assertEqual(clean("<think>private intermediate text</think>Final answer"), "Final answer")
        self.assertNotIn("private", clean("<think>private unfinished text"))
        self.assertEqual(clean("A normal answer"), "A normal answer")

    def test_embeddings_try_local_cache_before_any_download(self):
        with patch("llama_index.embeddings.huggingface.HuggingFaceEmbedding") as factory:
            self.rag.embedding_model()
            self.assertEqual(factory.call_count, 1)
            self.assertTrue(factory.call_args.kwargs["local_files_only"])
        with patch("llama_index.embeddings.huggingface.HuggingFaceEmbedding", side_effect=[OSError("missing cache"), object()]) as factory:
            self.rag.embedding_model()
            self.assertEqual([call.kwargs["local_files_only"] for call in factory.call_args_list], [True, False])

    def test_direct_tools_without_model(self):
        output = self.script("my_tools.py")
        self.assertIn("sunny (demo data)", output)
        self.assertIn("location", output)
        output = self.script("my_toolspec.py")
        self.assertIn("multiply", output)
        self.assertTrue(output.rstrip().endswith("4"))

    def test_actual_event_workflows_and_drawing(self):
        self.assertIn("Hello, world!", self.script("my_workflow.py"))
        self.assertIn("Finished processing: Step 1 complete", self.script("my_workflow_steps.py"))
        output = self.script("my_workflow_loop.py")
        self.assertEqual(output.count("Try again once"), 1)
        self.assertIn("Continue to step two", output)
        output = self.script("my_workflow_state.py")
        self.assertEqual(output.count("What is the capital of France?"), 2)
        self.script("my_workflow_draw.py")
        html = (self.work / "flow.html").read_text()
        self.assertIn("LoopEvent", html)
        self.assertIn("ProcessingEvent", html)

    def test_ingestion_is_persistent_and_does_not_duplicate(self):
        from llama_index.core.embeddings import MockEmbedding
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder) / ".hidden-course" / "week05-exercises"
            (work / "data").mkdir(parents=True)
            for i in range(10): (work / f"data/persona_{i}.txt").write_text(f"A classroom profile number {i}.")
            with patch.object(self.common, "ROOT", work), patch.object(self.rag, "ROOT", work):
                module = self.load("my_ingest.py")
                with patch.object(module, "embedding_model", return_value=MockEmbedding(embed_dim=8)):
                    asyncio.run(module.main())
                    collection, _ = self.rag.get_store()
                    count = collection.count()
                    self.assertEqual(count, 10)
                    asyncio.run(module.main())
                    self.assertEqual(collection.count(), count)
                with patch.object(self.rag, "embedding_model", return_value=MockEmbedding(embed_dim=8)):
                    index = self.rag.open_index()
                    hits = index.as_retriever(similarity_top_k=2).retrieve("a profile")
                    self.assertEqual(len(hits), 2)
                    self.assertTrue(all("file_name" in hit.node.metadata for hit in hits))

    def test_original_sources_are_distinct_from_generated_answer(self):
        from llama_index.core.base.response.schema import Response
        from llama_index.core.query_engine import CustomQueryEngine
        from llama_index.core.schema import NodeWithScore, TextNode

        original = "A local art historian interested in Cincinnati."
        class Engine(CustomQueryEngine):
            def custom_query(self, query_str):
                if query_str == "missing source":
                    return Response(response="An unsupported generated claim.", source_nodes=[])
                return Response(
                    response="A generated statement, not the original wording.",
                    source_nodes=[NodeWithScore(node=TextNode(
                        text=original, metadata={"file_name": "persona_0.txt"}))],
                )
        tool = self.rag.EvidenceQueryEngineTool.from_defaults(query_engine=Engine(), name="personas")
        for result in [tool.call("Cincinnati"), asyncio.run(tool.acall("Cincinnati"))]:
            self.assertIn("SOURCE: persona_0.txt\nEXCERPT:\n" + original, result.content)
            self.assertIn("GENERATED ANSWER (not an original quotation):", result.content)
            self.assertIn("not every profile", result.content)
            self.assertIn("No match was found in the retrieved passages", result.content)
            self.assertNotIn("generated statement", result.content.split("GENERATED ANSWER")[0])
            self.assertEqual(result.raw_output.source_nodes[0].node.get_content(), original)
        for result in [tool.call("missing source"), asyncio.run(tool.acall("missing source"))]:
            self.assertIn("Mark the evidence missing", result.content)
            self.assertNotIn("unsupported generated claim", result.content.split("GENERATED ANSWER")[0])

    def test_missing_data_and_partial_index_have_actionable_errors(self):
        from llama_index.core.embeddings import MockEmbedding
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            with patch.object(self.common, "ROOT", work), patch.object(self.rag, "ROOT", work):
                module = self.load("my_ingest.py")
                with self.assertRaisesRegex(FileNotFoundError, "prepare_personas.py"):
                    asyncio.run(module.main())
                (work / "data").mkdir()
                for i in range(10): (work / f"data/persona_{i}.txt").write_text(f"Profile {i}")
                collection, _ = self.rag.get_store()
                collection.add(ids=["partial"], documents=["incomplete"], embeddings=[[0.1] * 8])
                with patch.object(module, "embedding_model", return_value=MockEmbedding(embed_dim=8)):
                    with self.assertRaisesRegex(ValueError, "saved index is incomplete"):
                        asyncio.run(module.main())

    def test_diagnostics_are_actionable_and_do_not_echo_keys(self):
        async def missing():
            raise FileNotFoundError("Missing persona_0.txt. Run python prepare_personas.py.")
        with self.assertRaises(SystemExit) as caught: self.common.run(missing)
        self.assertIn("persona_0.txt", str(caught.exception))
        self.assertIn("prepare_personas.py", str(caught.exception))
        async def local():
            raise ValueError("Bad setting: unit-test-secret gsk_private_token")
        with patch.dict(os.environ, {"GROQ_API_KEY": "unit-test-secret"}):
            with self.assertRaises(SystemExit) as caught: self.common.run(local)
        self.assertNotIn("unit-test-secret", str(caught.exception))
        self.assertNotIn("gsk_private_token", str(caught.exception))
        class APIError(Exception): status_code = 401
        async def service(): raise APIError("A raw service response with private content")
        with self.assertRaises(SystemExit) as caught: self.common.run(service)
        self.assertIn("Check your Groq key", str(caught.exception))
        self.assertNotIn("private content", str(caught.exception))

    def test_diagram_export_does_not_launch_a_browser(self):
        workflow = self.load("my_workflow_loop.py").LoopWorkflow
        path = self.work / "export-only.html"
        previous = Path.cwd()
        try:
            os.chdir(self.work)
            with patch("webbrowser.open", side_effect=AssertionError("Do not launch a browser")):
                self.common.save_diagram(workflow, path)
        finally:
            os.chdir(previous)
        self.assertIn("LoopEvent", path.read_text())
        self.assertFalse((self.work / "lib").exists())
        self.assertIn('id="fit-diagram"', path.read_text())
        self.assertIn("network.fit", path.read_text())
        self.assertIn("70vh", path.read_text())
        class Resources(HTMLParser):
            def handle_starttag(parser, tag, attrs):
                attributes = dict(attrs)
                if tag == "script":
                    self.assertNotIn("src", attributes, "Diagram scripts must be embedded")
                if tag == "link" and attributes.get("rel") == "stylesheet":
                    self.fail("Diagram styles must be embedded")
        Resources().feed(path.read_text())
        from importlib.metadata import version, requires
        self.assertEqual(version("pyvis"), "0.3.2")
        self.assertTrue(any(dependency.startswith("pyvis") for dependency in requires("llama-index-utils-workflow")))

    def test_failed_embedding_download_has_recovery_guidance(self):
        with patch("llama_index.embeddings.huggingface.HuggingFaceEmbedding", side_effect=OSError("raw download error")):
            with self.assertRaises(SystemExit) as caught:
                self.rag.embedding_model()
        self.assertIn("rerun the same program", str(caught.exception))
        self.assertIn("No Groq tokens", str(caught.exception))
        self.assertNotIn("raw download error", str(caught.exception))

    def test_env_loading_and_no_automatic_retries(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(self.common, "ROOT", Path(folder)), patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit): self.common.get_llm()
            (Path(folder) / ".env").write_text("GROQ_API_KEY=unit-test-key\nGROQ_MODEL=qwen/qwen3.8-27b\n")
            llm = self.common.get_llm()
            self.assertEqual(llm.model, "qwen/qwen3.8-27b")
            self.assertEqual(llm.max_retries, 0)
            self.assertTrue(llm.metadata.is_function_calling_model)
            (Path(folder) / ".env").write_text("GROQ_API_KEY=unit-test-key\nGROQ_MODEL=groq/qwen/qwen3.8-27b\n")
            os.environ.pop("GROQ_MODEL")
            self.assertEqual(self.common.get_llm().model, "qwen/qwen3.8-27b")
            with patch.dict(os.environ, {"GROQ_MODEL": "groq/qwen/qwen3.8-27b"}):
                self.assertEqual(self.common.get_llm().model, "qwen/qwen3.8-27b")
        marker = "2026-11-10.2"
        self.assertEqual(self.common.STARTER_VERSION, marker)
        output = self.script("week05_common.py")
        self.assertEqual(output.strip(), "Week 5 starter version: " + marker)
        for page in ["week-5-learning-plan.md", "week-5-agents.md", "week-5-workflows.md"]:
            self.assertIn(marker, (ROOT / "docs" / page).read_text())

    def fake_groq(self):
        """Exercise real tool parsing/events while replacing remote model replies."""
        from llama_index.llms.groq import Groq
        from llama_index.core.base.llms.types import ChatMessage, ChatResponse, MessageRole
        from openai.types.chat import ChatCompletionMessageToolCall

        self.captured_requests = []

        def reply(messages, **kwargs):
            self.captured_requests.append([{"role": str(message.role), "content": message.content} for message in messages])
            tools = kwargs.get("tools") or []
            names = {tool["function"]["name"] for tool in tools}
            user = next((str(m.content) for m in reversed(messages) if m.role == MessageRole.USER), "")
            last = messages[-1]
            toolname = None
            inputs = None
            if "YES" in str(messages):
                text = "YES"
            elif "Bob" in user or "name again" in user:
                text = "Your name is Bob." if any("My name is Bob" in str(m.content) for m in messages) else "I do not know your name."
            elif last.role == MessageRole.TOOL and "handing off" not in str(last.content).lower() and "handoff" not in str(last.content).lower() and "is now handling" not in str(last.content).lower():
                text = str(last.content)
            elif "Cincinnati" in user:
                if "personas" in names:
                    toolname, inputs = "personas", {"input": "Cincinnati art historian"}
                elif "handoff" in names:
                    toolname, inputs = "handoff", {"to_agent": "info_lookup", "reason": "Persona research needs info_lookup."}
                text = "A Cincinnati art historian and museum professional."
            elif "add 5 and 3" in user:
                if "add" in names: toolname, inputs = "add", {"a": 5, "b": 3}
                else: toolname, inputs = "handoff", {"to_agent": "add_agent", "reason": "Addition needs add_agent."}
                text = "8"
            elif "multiply" in names:
                toolname, inputs, text = "multiply", {"a": 2, "b": 2}, "4"
            elif "YES" in str(messages) or "faithful" in str(messages).lower():
                text = "YES"
            else: text = "A Cincinnati art historian and museum professional."
            extra = {}
            if toolname:
                extra["tool_calls"] = [ChatCompletionMessageToolCall(
                    id="call_test", type="function", function={"name": toolname, "arguments": json.dumps(inputs)})]
                text = ""
            return ChatResponse(message=ChatMessage(role="assistant", content=text, additional_kwargs=extra), delta=text)

        async def chat(self, messages, **kwargs): return reply(messages, **kwargs)
        async def stream(self, messages, **kwargs):
            async def generator(): yield reply(messages, **kwargs)
            return generator()
        return Groq, chat, stream

    def mocked_run(self, filename, rag=False):
        from llama_index.core.tools import FunctionTool
        from llama_index.llms.groq import Groq
        def evidence(input: str) -> str:
            """Search profile evidence."""
            return "A Cincinnati art historian and museum professional."
        llm = Groq(model="qwen/qwen3.8-27b", api_key="unit-test-key", max_retries=0)
        cls, chat, stream = self.fake_groq()
        with patch.object(self.common, "get_llm", return_value=llm), patch.object(cls, "achat", chat), patch.object(cls, "astream_chat", stream), patch.object(cls, "_achat", chat):
            with patch.object(self.rag, "persona_tool", return_value=FunctionTool.from_defaults(evidence, name="personas")):
                module = self.load(filename)
                output = io.StringIO()
                with redirect_stdout(output): asyncio.run(module.main())
                return output.getvalue()

    def test_query_engine_tool_and_evaluator_with_mocked_groq(self):
        from llama_index.core.embeddings import MockEmbedding
        from llama_index.llms.groq import Groq
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            (work / "data").mkdir()
            for i in range(10):
                (work / f"data/persona_{i}.txt").write_text("A Cincinnati art historian and museum professional.")
            with patch.object(self.common, "ROOT", work), patch.object(self.rag, "ROOT", work):
                ingest = self.load("my_ingest.py")
                with patch.object(ingest, "embedding_model", return_value=MockEmbedding(embed_dim=8)):
                    asyncio.run(ingest.main())
                cls, chat, stream = self.fake_groq()
                llm = Groq(model="qwen/qwen3.8-27b", api_key="unit-test-key", max_retries=0)
                with patch.object(self.rag, "embedding_model", return_value=MockEmbedding(embed_dim=8)), patch.object(self.common, "get_llm", return_value=llm), patch.object(cls, "achat", chat), patch.object(cls, "astream_chat", stream), patch.object(cls, "_achat", chat):
                    for name in ["my_query.py", "my_query_tool.py", "my_evaluate.py", "my_llm.py"]:
                        module = self.load(name)
                        output = io.StringIO()
                        with redirect_stdout(output): asyncio.run(module.main())
                        self.assertTrue(output.getvalue().strip())
                        if name == "my_query.py": self.assertIn("SOURCE: persona_", output.getvalue())
                        if name == "my_evaluate.py": self.assertIn("PASS: True", output.getvalue())

    def test_real_agent_tool_call_and_context_memory_with_mocked_groq(self):
        output = self.mocked_run("my_agent.py")
        self.assertIn("TOOL: multiply", output)
        self.assertIn("RETURN: 4", output)
        output = self.mocked_run("my_memory.py")
        shared_answer = output.split("REQUEST: What was my name again?", 1)[1].split("NOW A FRESH CONTEXT:", 1)[0]
        fresh_answer = output.split("NOW A FRESH CONTEXT:", 1)[1]
        self.assertIn("ANSWER: Your name is Bob", shared_answer)
        self.assertIn("ANSWER: I do not know your name", fresh_answer)
        self.assertEqual(len(self.captured_requests), 3)
        self.assertTrue(any(message["content"] == "My name is Bob." for message in self.captured_requests[1]))
        self.assertFalse(any(message["content"] == "My name is Bob." for message in self.captured_requests[2]))

    def test_real_agent_handoff_and_shared_state_with_mocked_groq(self):
        output = self.mocked_run("my_rag_agent.py")
        self.assertIn("TOOL: personas", output)
        output = self.mocked_run("my_agent_team.py")
        self.assertIn("TOOL: handoff", output)
        self.assertIn("TOOL: personas", output)
        output = self.mocked_run("my_team_workflow.py")
        self.assertIn("TOOL: handoff", output)
        self.assertIn("TOOL: add", output)
        self.assertIn("ARITHMETIC CALLS: 1", output)


if __name__ == "__main__":
    unittest.main()
