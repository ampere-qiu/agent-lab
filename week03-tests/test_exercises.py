"""Run the exact classroom files created from lesson code blocks.

The real minimal ZIP supplies support modules. Tests create the student's files
and execute real CodeAgent/SDK code with simulated Groq/search responses.
No UI, retrieval package, live API key, or external service is used.
"""
import contextlib
import importlib
import io
import json
from pathlib import Path
import re
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import httpx
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]


class ExerciseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        with ZipFile(ROOT / 'docs/downloads/week03-smolagents.zip') as archive:
            archive.extractall(cls.temporary.name)
        cls.folder = Path(cls.temporary.name) / 'week03-exercises'
        cls.student_files = {}
        for page in ('week-3-code-agent.md', 'week-3-action-formats.md', 'week-3-custom-tool.md'):
            content = (ROOT / 'docs' / page).read_text()
            for name, source in re.findall(r'```python title="(my_[^"]+\.py)"\n(.*?)```', content, re.S):
                (cls.folder / name).write_text(source)
                cls.student_files[name] = source
        sys.path.insert(0, str(cls.folder))
        cls.common = importlib.import_module('week03_common')
        cls.tools = importlib.import_module('week03_tools')
        cls.search = importlib.import_module('week03_search')

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(str(cls.folder))
        for name in list(sys.modules):
            if name.startswith('week03_'):
                del sys.modules[name]
        cls.temporary.cleanup()

    def model(self, actions, expected_observations=(), native=False):
        calls = []
        def handler(request):
            body = json.loads(request.content)
            calls.append(body)
            self.assertEqual(str(request.url), 'https://api.groq.com/openai/v1/chat/completions')
            self.assertEqual(body['model'], 'qwen/qwen3.8-27b')
            self.assertEqual(body['reasoning_effort'], 'none')
            self.assertEqual(body['max_tokens'], 512)
            index = len(calls)-1
            self.assertLess(index, len(actions), 'Unexpected extra model request')
            if index in dict(expected_observations):
                self.assertIn(dict(expected_observations)[index], json.dumps(body['messages']))
            if native:
                self.assertIn('web_search', [t['function']['name'] for t in body['tools']])
                name, arguments = actions[index]
                message = {'role': 'assistant', 'content': None, 'tool_calls': [{
                    'id': 'call_'+str(index), 'type': 'function',
                    'function': {'name': name, 'arguments': json.dumps(arguments)}}]}
                reason = 'tool_calls'
            else:
                self.assertNotIn('tools', body)
                message = {'role': 'assistant', 'content': f'Code:\n```py\n{actions[index]}\n```<end_code>'}
                reason = 'stop'
            return httpx.Response(200, json={
                'id': 'offline', 'object': 'chat.completion', 'created': 0,
                'model': body['model'], 'choices': [{'index': 0, 'finish_reason': reason,
                    'message': message}],
                'usage': {'prompt_tokens': 100, 'completion_tokens': 30, 'total_tokens': 130}})
        with patch.dict('os.environ', {'GROQ_API_KEY': 'offline-not-a-real-key'}):
            model = self.common.build_model()
        model.client.close()
        model.client = OpenAI(api_key='offline-not-a-real-key',base_url='https://api.groq.com/openai/v1',
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),max_retries=0)
        self.addCleanup(model.client.close)
        return model, calls

    def run_student_file(self, name, actions, expected=(), native=False):
        self.assertIn(name, self.student_files)
        model, calls = self.model(actions, expected, native)
        with patch.object(self.common, 'build_model', return_value=model), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as stopped:
                runpy.run_path(str(self.folder / name), run_name='__main__')
            self.assertEqual(stopped.exception.code, 0, output.getvalue())
        self.assertEqual(len(calls), len(actions))
        return output.getvalue(), calls

    def test_all_named_student_files_are_complete(self):
        self.assertEqual(set(self.student_files), {'my_playlist.py', 'my_menu.py', 'my_timing.py',
            'my_tool_calling.py', 'my_tool_check.py', 'my_catering.py', 'my_theme.py'})
        for name, source in self.student_files.items():
            compile(source, name, 'exec')
            self.assertNotIn('gradio', source)
            self.assertNotIn('langchain', source)
        with ZipFile(ROOT / 'docs/downloads/week03-smolagents.zip') as archive:
            self.assertEqual(len(archive.namelist()), 6)

    def test_direct_tool_check_needs_no_llm(self):
        with patch.object(self.common, 'build_model', side_effect=AssertionError('No LLM expected')), \
                patch.object(self.search, 'DDGS', side_effect=AssertionError('No search expected')), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            runpy.run_path(str(self.folder / 'my_tool_check.py'), run_name='__main__')
        self.assertIn('PASS: menu, catering, theme, and unknown-category checks.', output.getvalue())

    def test_menu_student_file(self):
        output, calls = self.run_student_file('my_menu.py', [
            'print(suggest_menu(occasion="formal"))',
            'final_answer("3-course dinner with wine and dessert.")',
        ], [(1, '3-course dinner with wine and dessert.')])
        self.assertIn('3-course dinner', output)

    def test_timing_student_file(self):
        output, calls = self.run_student_file('my_timing.py', [
            'import datetime\nstart = datetime.datetime.now()\nend = start + datetime.timedelta(minutes=30+60+45+45)\nprint((end-start).total_seconds()/60)',
            'final_answer("Preparation takes 180 minutes, or three hours.")',
        ], [(1, '180.0')])
        self.assertIn('180 minutes', output)

    def test_playlist_student_file(self):
        with patch.object(self.search, 'DDGS') as ddgs:
            ddgs.return_value.text.return_value = [{'title': 'Fixture playlist',
                'href': 'https://example.org/music', 'body': 'Fixture music recommendation.'}]
            output, calls = self.run_student_file('my_playlist.py', [
                'print(web_search(query="Batman party music"))',
                'final_answer("Fixture playlist: https://example.org/music")',
            ], [(1, 'Fixture music recommendation.')])
            self.assertEqual(ddgs.return_value.text.call_args.kwargs['backend'], 'duckduckgo')
        self.assertIn('https://example.org/music', output)

    def test_catering_student_file(self):
        output, calls = self.run_student_file('my_catering.py', [
            'print(catering_service_tool(query="catering"))',
            'final_answer("Gotham Catering Co.")',
        ], [(1, 'Gotham Catering Co.')])
        self.assertIn('Gotham Catering Co.', output)

    def test_theme_student_file_and_fallback(self):
        tool = self.tools.SuperheroPartyThemeTool()
        self.assertIn('not found', tool(category='unknown'))
        self.assertIn('Neo-Gotham Night', tool(category='FUTURISTIC GOTHAM'))
        output, calls = self.run_student_file('my_theme.py', [
            'print(superhero_party_theme_generator(category="villain masquerade"))',
            'final_answer("Gotham Rogues Ball: a mysterious masquerade.")',
        ], [(1, "Gotham Rogues' Ball")])
        self.assertIn('Gotham Rogues', output)

    def test_student_modifies_tool_and_direct_check(self):
        path = self.folder / 'week03_tools.py'
        checker = self.folder / 'my_tool_check.py'
        original, original_check = path.read_text(), checker.read_text()
        try:
            path.write_text(original.replace('"Gotham Catering Co.": 4.9,',
                '"Gotham Catering Co.": 4.9,\n        "Student Catering": 5.0,'))
            checker.write_text(original_check.replace('== "Gotham Catering Co."', '== "Student Catering"'))
            importlib.reload(self.tools)
            output, calls = self.run_student_file('my_catering.py', [
                'print(catering_service_tool(query="catering"))',
                'final_answer("Student Catering")',
            ], [(1, 'Student Catering')])
            self.assertIn('Student Catering', output)
            with contextlib.redirect_stdout(io.StringIO()) as direct:
                runpy.run_path(str(checker), run_name='__main__')
            self.assertIn('PASS:', direct.getvalue())
        finally:
            path.write_text(original)
            checker.write_text(original_check)
            importlib.reload(self.tools)

    def test_optional_structured_student_file(self):
        with patch.object(self.search, 'DDGS') as ddgs:
            ddgs.return_value.text.return_value = [{'title': 'Fixture',
                'href': 'https://example.org/native', 'body': 'Fixture native music'}]
            output, calls = self.run_student_file('my_tool_calling.py', [
                ('web_search', {'query': 'Batman party music'}),
                ('final_answer', {'answer': 'Fixture playlist: https://example.org/native'}),
            ], [(1, 'Fixture native music')], native=True)
        self.assertIn('https://example.org/native', output)


if __name__ == '__main__':
    unittest.main()
