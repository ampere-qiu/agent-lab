"""Validate extracted downloads and exact lesson runners with real smolagents/SDK.

Remote model/search/page responses and Selenium driver are simulated. No paid API
calls, live web research, or actual driver execution is claimed by these tests.
"""
import ast
import contextlib
import importlib
import io
import json
import os
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
from PIL import Image
from smolagents.memory import ActionStep, TaskStep

ROOT = Path(__file__).resolve().parents[1]


class Driver:
    def __init__(self):
        self.current_url = 'about:blank'
        self.clicked = False
        self.closed = False
    def set_page_load_timeout(self, _): pass
    def get(self, url): self.current_url = url
    def find_element(self, *_): return self
    def click(self): self.clicked = True
    def get_screenshot_as_png(self):
        buf = io.BytesIO()
        Image.new('RGB', (40, 30), 'green' if self.clicked else 'red').save(buf, format='PNG')
        return buf.getvalue()
    def save_screenshot(self, name):
        Path(name).write_bytes(self.get_screenshot_as_png())
    def quit(self): self.closed = True


class Week04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        with ZipFile(ROOT / 'docs/downloads/week04-smolagents-part2.zip') as z:
            z.extractall(cls.tmp.name)
        cls.folder = Path(cls.tmp.name) / 'week04-exercises'
        cls.runners = {}
        cls.stages = {}
        for page in (cls.folder / 'lessons/en').glob('*.md'):
            for name, code in re.findall(r'```python title="(my_[^"]+\.py)"\n(.*?)```', page.read_text(), re.S):
                cls.stages.setdefault(name, []).append(code)
        for name, parts in cls.stages.items():
            # Follow the student's append/save instructions in document order.
            cls.runners[name] = '\n'.join(parts)
            (cls.folder / name).write_text(cls.runners[name])
        sys.path.insert(0, str(cls.folder))
        cls.common = importlib.import_module('week04_common')
        cls.tools = importlib.import_module('week04_tools')
        cls.search = importlib.import_module('week04_search')
        cls.browser = importlib.import_module('week04_browser')
        importlib.import_module('prepare_visuals').prepare()

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(str(cls.folder))
        for name in list(sys.modules):
            if name.startswith(('week04_', 'my_batman')) or name == 'prepare_visuals':
                del sys.modules[name]
        cls.tmp.cleanup()

    def model(self, actions):
        calls = []
        def respond(request):
            data = json.loads(request.content)
            calls.append(data)
            self.assertEqual(data['model'], 'qwen/qwen3.8-27b')
            self.assertEqual(data['reasoning_effort'], 'none')
            self.assertEqual(data['max_tokens'], 800)
            self.assertNotIn('tools', data)
            n = len(calls)-1
            self.assertLess(n, len(actions), 'Unexpected model call: possible tool/parse failure')
            return httpx.Response(200, json={
                'id':'offline', 'object':'chat.completion', 'created':0, 'model':data['model'],
                'choices':[{'index':0,'finish_reason':'stop','message':{
                    'role':'assistant','content':f'Code:\n```py\n{actions[n]}\n```<end_code>'}}],
                'usage':{'prompt_tokens':100,'completion_tokens':30,'total_tokens':130}})
        with patch.dict(os.environ, {'GROQ_API_KEY':'offline-not-a-real-key'}):
            model = self.common.build_model()
        model.client.close()
        model.client = OpenAI(api_key='offline-not-a-real-key',base_url='https://api.groq.com/openai/v1',
            http_client=httpx.Client(transport=httpx.MockTransport(respond)), max_retries=0)
        self.addCleanup(model.client.close)
        return model, calls

    def run_file(self, name, actions):
        model, calls = self.model(actions)
        with patch.object(self.common, 'build_model', return_value=model), contextlib.redirect_stdout(io.StringIO()) as out:
            runpy.run_path(str(self.folder / name), run_name='__main__')
        self.assertEqual(len(calls),len(actions),out.getvalue())
        return calls, out.getvalue()

    def fixtures(self):
        return [dict(location=f'Fixture {n}', kind='filming' if n<3 else 'factory',latitude=40+n,
                     longitude=-70+n,source_url=f'https://example.org/claim/{n}',
                     coordinate_source_url=f'https://example.org/coords/{n}',evidence='SIMULATED TEST DATA') for n in range(4)]

    def research_actions(self):
        rows = json.dumps(self.fixtures())
        return ['print(web_specialist(task="Find sourced candidates"))',
                'print(web_search(query="Batman filming"))',
                'print(visit_webpage(url="https://example.org/claim/0"))',
                f'final_answer({rows!r})']

    def test_downloads_runners_and_offline_links(self):
        self.assertEqual(set(self.runners), {'my_batman_tools.py','my_batman.py',
            'my_vision.py','my_browser_check.py','my_browser.py'})
        expected = {p.name for p in (ROOT / 'week04-starter').iterdir() if p.is_file()}
        for package in ['week04-smolagents-part2.zip','week4_batman_guided_student.zip','week4_vision_browser_student.zip']:
            with ZipFile(ROOT / 'docs/downloads' / package) as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(sum('/lessons/ja/week-4-' in name for name in z.namelist()), 5)
                self.assertIn('English and Japanese lessons', z.read('week04-exercises/README.md').decode())
                for lang in ['en', 'ja']:
                    for record in json.loads((ROOT/'docs/images/huggingface-week04/sources.json').read_text()):
                        name = f"week04-exercises/lessons/{lang}/images/huggingface-week04/{record['file']}"
                        self.assertEqual(z.read(name), (ROOT/'docs/images/huggingface-week04'/record['file']).read_bytes())
                self.assertEqual({Path(n).name for n in z.namelist() if '/lessons/' not in n}, expected)
                for name in z.namelist():
                    self.assertNotIn('..',Path(name).parts)
                    self.assertFalse(any(x in name for x in ('.env','__pycache__','.venv','outputs/')))
                    if name.endswith('.py'): ast.parse(z.read(name).decode())
                    if '/lessons/' not in name:
                        self.assertEqual(z.read(name),(ROOT/'week04-starter'/Path(name).name).read_bytes())
        for file in self.folder.rglob('*.md'):
            for href in re.findall(r'\]\(([^)]+)\)',file.read_text()):
                if '://' in href: continue
                local_path = href.split('#')[0]
                target = (file.parent/local_path).resolve() if local_path else file
                self.assertTrue(target.is_file(), (file,href))
        for name, code in self.runners.items(): ast.parse(code,filename=name)

    def test_setup_template_and_generated_file_origins(self):
        with ZipFile(ROOT/'docs/downloads/week04-smolagents-part2.zip') as archive:
            names = archive.namelist()
            self.assertNotIn('week04-exercises/evidence.md', names)
            self.assertFalse(any('/assets/' in n or '/outputs/' in n for n in names))
        setup = (self.folder/'lessons/en/week-4-preview.md').read_text()
        template = re.search(r'```markdown title="evidence.md — create this text file"\n(.*?)```', setup, re.S)[1]
        note = self.folder/'evidence.md'
        note.write_text(template)
        (self.folder/'evidence-files').mkdir(exist_ok=True)
        for topic in ['14', '15', '16', '17']:
            self.assertIn('## Topic '+topic, note.read_text())
        with tempfile.TemporaryDirectory() as fresh:
            visuals = importlib.import_module('prepare_visuals')
            with patch.object(visuals, 'ROOT', Path(fresh)), contextlib.redirect_stdout(io.StringIO()):
                visuals.prepare()
            with Image.open(Path(fresh)/'assets/venue.png') as image:
                self.assertEqual(image.size, (800,500))
            page = (Path(fresh)/'assets/venue.html').read_text()
            self.assertIn('The east exit is closed for maintenance.', page)
            self.assertIn('Show access details', page)

    def test_rag_review_has_no_new_implementation(self):
        lesson = (self.folder/'lessons/en/week-4-retrieval.md').read_text()
        self.assertIn('https://ampere-qiu.github.io/agent-lab/week-3-retrieval/', lesson)
        self.assertNotIn('```python', lesson)
        self.assertNotIn('my_rag_continuation.py', lesson)
        self.assertEqual(len(re.findall(r'\?\?\? success "Answer [1-5] ', lesson)), 5)
        self.assertIn('provided example', lesson)
        self.assertFalse((self.folder/'week04_retriever.py').exists())
        requirements = (self.folder/'requirements.txt').read_text()
        self.assertNotIn('langchain', requirements)
        self.assertNotIn('rank-bm25', requirements)

    def test_agent_construction_stages_before_any_task_call(self):
        for name, expected_stages in [('my_batman.py', 4), ('my_vision.py', 3), ('my_browser.py', 3)]:
            with self.subTest(file=name):
                parts = self.stages[name]
                self.assertEqual(len(parts), expected_stages)
                prefix = ''
                for part in parts:
                    prefix += '\n' + part
                    ast.parse(prefix, filename=name)
        model, calls = self.model([])
        scope = {'__file__':str(self.folder/'my_batman.py')}
        with patch.object(self.common, 'build_model', return_value=model), contextlib.redirect_stdout(io.StringIO()):
            for index, part in enumerate(self.stages['my_batman.py'][:-1]):
                exec(part, scope)
                if index == 0:
                    self.assertNotIn('specialist', scope)
                    self.assertNotIn('manager', scope)
                elif index == 1:
                    self.assertIn('web_search', scope['specialist'].tools)
                    self.assertIn('visit_webpage', scope['specialist'].tools)
                    self.assertNotIn('manager', scope)
                else:
                    self.assertIs(scope['manager'].managed_agents['web_specialist'], scope['specialist'])
                    self.assertIsNot(scope['manager'].memory, scope['specialist'].memory)
                    self.assertIn('save_report', scope['manager'].tools)
                    self.assertNotIn('web_search', scope['manager'].tools)
                self.assertEqual(calls, [], 'Construction must not execute a model task')

    def test_four_fresh_specialist_handoffs_and_report(self):
        rows = self.fixtures()
        actions = []
        for index, row in enumerate(rows):
            actions.extend([
                f'print(web_specialist(task="Research only Fixture {index}; return one sourced record"))',
                f'print(web_search(query="Fixture {index} claim and coordinates"))',
                f'print(visit_webpage(url="https://example.org/claim/{index}", focus="filming")); print(visit_webpage(url="https://example.org/coords/{index}", focus="coordinates"))',
                f'final_answer({json.dumps(row)!r})',
            ])
        actions.extend([
            f'print(cargo_time(latitude=40.0, longitude=-70.0)); print(save_report(rows_json={json.dumps(rows)!r}))',
            'final_answer("Report saved; all rows are simulated fixtures.")',
        ])
        path = self.folder/'my_batman.py'
        original = path.read_text()
        full = original.replace('max_pages=2', 'max_pages=3')
        full = full.replace('max_steps=4, compact=True', 'max_steps=5, compact=True')
        full = full.replace('max_steps=3, compact=True', 'max_steps=6, compact=True')
        full = full.replace('run_task(manager, ONE_LOCATION_TASK)', 'run_task(manager, TASK)')
        path.write_text(full)
        try:
            with patch.object(self.search, 'DDGS') as ddgs, patch.object(self.search.requests, 'get', side_effect=lambda url, **kwargs: self.response('<article><p>SIMULATED filming coordinates evidence '+url+'</p></article>')) as fetch:
                ddgs.return_value.text.return_value = [dict(title='Fixture', href='https://example.org/claim', body='SIMULATED SEARCH')]
                calls, out = self.run_file('my_batman.py', actions)
                self.assertEqual(ddgs.return_value.text.call_count, 4)
                self.assertEqual(fetch.call_count, 8)
        finally:
            path.write_text(original)
        for index in range(4):
            specialist_first = json.dumps(calls[index*4+1]['messages'])
            self.assertIn(f'Research only Fixture {index}', specialist_first)
            if index:
                self.assertNotIn(f'https://example.org/coords/{index-1}', specialist_first)
        self.assertIn('https://example.org/coords/3', json.dumps(calls[16]['messages']))
        # A regression bound on the actual serialized history, not a token estimate.
        self.assertLess(max(len(json.dumps(call['messages'])) for call in calls), 18000)
        report = (self.folder/'outputs/batman-report.html').read_text()
        self.assertIn('Fixture 3', report)
        self.assertEqual(report.count('<circle '), 4)

    def test_optional_third_agent_is_called(self):
        code = self.runners['my_batman.py']
        code = code.replace('manager = CodeAgent(', """verifier_budget = ResearchBudget(max_searches=1, max_pages=2)
verifier = CodeAgent(
    tools=[WebSearchTool(budget=verifier_budget), PageExcerptTool(budget=verifier_budget)], model=model,
    name="verifier", description="Independently checks sourced claims and coordinates with evidence and uncertainty.",
    **agent_options(max_steps=4, compact=True),
)
verifier_budget.bind(verifier)
manager = CodeAgent(""", 1)
        code = code.replace('managed_agents=[specialist]', 'managed_agents=[specialist, verifier]')
        code = code.replace('max_steps=3, compact=True', 'max_steps=4, compact=True')
        code = code.replace('run_task(manager, ONE_LOCATION_TASK)', 'TASK = "Research one candidate row, then ask verifier to independently check it. Return a sourced verdict without saving a report."\nrun_task(manager, ONE_LOCATION_TASK)')
        code = code.replace('run_task(manager, ONE_LOCATION_TASK)', 'run_task(manager, TASK)')
        (self.folder/'my_batman_verified.py').write_text(code)
        rows=json.dumps(self.fixtures())
        actions=self.research_actions()+['print(verifier(task="Independently check https://example.org/claim/0"))',
            'print(visit_webpage(url="https://example.org/claim/0"))',
            'final_answer("Independent simulated verdict: uncertain")','final_answer("Unverified report withheld")']
        with patch.object(self.search,'DDGS') as ddgs, patch.object(self.search.PageExcerptTool, 'forward', new=lambda self, url, focus='': 'SIMULATED PAGE EVIDENCE'):
            ddgs.return_value.text.return_value=[dict(title='Fixture',href='https://example.org/claim/0',body='SIMULATED SEARCH')]
            calls,out=self.run_file('my_batman_verified.py',actions)
        self.assertIn('Independent simulated verdict: uncertain',json.dumps(calls[-1]['messages']))
        self.assertIn('Unverified report withheld',out)

    def test_assembled_team_executes_small_handoff(self):
        code = self.runners['my_batman.py']
        self.assertNotIn('SPECIALIST_TOOLS = []', code)
        self.assertIn('Do NOT research coordinates', code)
        with patch.object(self.search.PageExcerptTool, 'forward', new=lambda self, url, focus='': 'SIMULATED filming claim from source'):
            calls, out = self.run_file('my_batman.py', [
                'print(web_specialist(task="Check only the Wollaton Hall filming claim"))',
                'print(visit_webpage(url="https://example.org/claim", focus="Wayne Manor Batman"))',
                'final_answer("SIMULATED supported filming claim https://example.org/claim; quote retained")',
                'final_answer("Source https://example.org/claim and quote retained; no coordinate research requested")'])
        self.assertIn('Wollaton Hall', json.dumps(calls[0]['messages']))
        self.assertIn('quote retained', json.dumps(calls[3]['messages']))
        self.assertIn('no coordinate research requested', out)

    def response(self, html, status=200):
        import requests
        result = requests.Response()
        result.status_code = status
        result._content = html.encode()
        result.encoding = 'utf-8'
        result.url = 'https://example.org/page'
        return result

    def test_deep_page_evidence_is_focused_and_bounded(self):
        html = '<html><body><nav>' + 'MENU ' * 10000 + '</nav><article>'
        html += '<p>Unrelated visitor information.</p>' * 500
        html += '<p>Wollaton Hall was Wayne Manor in The Dark Knight Rises.</p>'
        html += '<p>Other information.</p>' * 500 + '</article></body></html>'
        tool = self.search.PageExcerptTool()
        with patch.object(self.search.requests, 'get', return_value=self.response(html)) as fetch:
            excerpt = tool('https://example.org/page', focus='Wayne Manor Batman')
        self.assertLessEqual(len(excerpt), 1600)
        self.assertIn('Source: https://example.org/page', excerpt)
        self.assertIn('Wayne Manor in The Dark Knight Rises', excerpt)
        self.assertNotIn('MENU', excerpt)
        self.assertEqual(fetch.call_count, 1)
        long_html = '<article><p>Wayne Manor ' + 'supporting text ' * 5000 + '</p></article>'
        with patch.object(self.search.requests, 'get', return_value=self.response(long_html)):
            clipped = self.search.PageExcerptTool()('https://example.org/long', focus='Wayne Manor')
        self.assertLessEqual(len(clipped), 1600)
        self.assertIn('Excerpt clipped', clipped)

    def test_failed_attempts_count_and_fresh_delegation_resets_budget(self):
        from types import SimpleNamespace
        agent = SimpleNamespace(memory=SimpleNamespace(steps=[TaskStep(task='first place')]))
        budget = self.search.ResearchBudget(max_searches=1, max_pages=2)
        budget.bind(agent)
        page = self.search.PageExcerptTool(budget=budget)
        with patch.object(self.search.requests, 'get', side_effect=[self.response('',403), self.response('<p>Second source.</p>'), self.response('<p>Fresh task source.</p>')]) as fetch:
            self.assertIn('403', page('https://example.org/blocked'))
            self.assertIn('Already attempted', page('https://example.org/blocked'))
            self.assertIn('Second source', page('https://example.org/alternate'))
            self.assertIn('limit reached', page('https://example.org/third'))
            self.assertEqual(fetch.call_count, 2)
            agent.memory.steps = [TaskStep(task='next place')]
            self.assertIn('Fresh task source', page('https://example.org/blocked'))
            self.assertEqual(fetch.call_count, 3)
        search = self.search.WebSearchTool(budget=budget)
        with patch.object(self.search, 'DDGS') as ddgs:
            ddgs.return_value.text.return_value = [dict(title='Title'*100, href='https://example.org/source', body='SNIPPET '*1000)] * 5
            result = search('focused query')
            self.assertLessEqual(len(result), 1400)
            self.assertEqual(result.count('https://example.org/source'), 2)
            self.assertIn('limit reached', search('another query'))
            self.assertEqual(ddgs.return_value.text.call_count, 1)

    def test_large_printed_observation_is_bounded_before_next_model_call(self):
        calls, out = self.run_file('my_batman.py', [
            'print("NOISE" * 5000)',
            'final_answer("Incomplete simulated run; no research was performed.")',
        ])
        observation = [part['text'] for message in calls[1]['messages'] for part in message['content']
                       if part.get('type') == 'text' and 'Observation:' in part.get('text', '')]
        self.assertTrue(observation)
        self.assertTrue(all(len(text) < 2000 for text in observation))

    def test_initial_image_is_serialized_to_model(self):
        calls,_=self.run_file('my_vision.py',['final_answer("Visible room labels; exit availability unknown.")'])
        self.assertIn('data:image/',json.dumps(calls[0]['messages']))

    def test_browser_actions_and_screenshots_reach_next_model_call(self):
        driver=Driver()
        with patch('selenium.webdriver.Chrome', return_value=driver):
            calls,_=self.run_file('my_browser.py',['print(open_venue())','print(show_access_details())',
                'final_answer("Use the updated screenshot evidence; this test uses simulated pixels.")'])
        images=lambda call:[p['image_url']['url'] for m in call['messages'] for p in m['content'] if p.get('type')=='image_url']
        self.assertEqual(len(images(calls[0])),0)
        self.assertEqual(len(images(calls[1])),1)
        self.assertEqual(len(images(calls[2])),1)
        self.assertNotEqual(images(calls[1]),images(calls[2]))
        self.assertTrue(driver.clicked and driver.closed)
        with patch('selenium.webdriver.Chrome',return_value=Driver()),contextlib.redirect_stdout(io.StringIO()):
            browser=self.browser.BrowserSession()
            browser.tools[0]()
            browser.close()

    def test_direct_student_checks_need_no_model(self):
        driver = Driver()
        old = Path.cwd()
        try:
            os.chdir(self.folder)
            with patch('selenium.webdriver.Chrome', return_value=driver), patch.object(self.common, 'build_model', side_effect=AssertionError('No model expected')), contextlib.redirect_stdout(io.StringIO()):
                runpy.run_path(str(self.folder/'my_browser_check.py'), run_name='__main__')
            self.assertNotEqual((self.folder/'before.png').read_bytes(), (self.folder/'after.png').read_bytes())
            self.assertTrue(driver.closed)
            with patch.object(self.search, 'DDGS') as ddgs, patch.object(self.search.PageExcerptTool, 'forward', new=lambda self, url, focus='': 'SIMULATED PAGE'), contextlib.redirect_stdout(io.StringIO()) as out:
                ddgs.return_value.text.return_value = [dict(title='Fixture', href='https://example.org/', body='SIMULATED SEARCH')]
                runpy.run_path(str(self.folder/'my_batman_tools.py'), run_name='__main__')
            self.assertIn('1.0', out.getvalue())
            self.assertIn('SIMULATED PAGE', out.getvalue())
        finally:
            os.chdir(old)

    def test_calculator_validation_and_html_escaping(self):
        self.assertEqual(self.tools.cargo_time(40.7128,-74.0060),1.0)
        for lat,lon in [(91,0),(0,-181),(float('nan'),0)]:
            with self.assertRaises(ValueError):self.tools.cargo_time(lat,lon)
        rows=self.fixtures();rows[0]['location']='<script>alert(1)</script>'
        path=self.tools.save_report(json.dumps(rows))
        self.assertNotIn('<script>',Path(path).read_text())
        rows[0]['source_url']='javascript:alert(1)'
        with self.assertRaises(ValueError):self.tools.save_report(json.dumps(rows))


if __name__ == '__main__': unittest.main()
