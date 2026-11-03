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
from smolagents.memory import ActionStep

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
        for page in (cls.folder / 'lessons/en').glob('*.md'):
            for name, code in re.findall(r'```python title="(my_[^"]+\.py)"\n(.*?)```', page.read_text(), re.S):
                cls.runners[name] = code
                (cls.folder / name).write_text(code)
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
            self.assertEqual(data['max_tokens'], 1200)
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
        self.assertEqual(set(self.runners), {'my_rag_continuation.py','my_batman_tools.py','my_batman.py',
            'my_vision.py','my_browser_check.py','my_browser.py'})
        expected = {p.name for p in (ROOT / 'week04-starter').iterdir() if p.is_file()}
        for package in ['week04-smolagents-part2.zip','week4_batman_guided_student.zip','week4_vision_browser_student.zip']:
            with ZipFile(ROOT / 'docs/downloads' / package) as z:
                self.assertIsNone(z.testzip())
                self.assertFalse(any('/lessons/ja/' in name for name in z.namelist()))
                self.assertIn('English release', z.read('week04-exercises/README.md').decode())
                for lang in ['en']:
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
                self.assertTrue((file.parent/href.split('#')[0]).resolve().is_file(), (file,href))
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

    def test_policy_experiment_from_student_edit_instructions(self):
        path = self.folder/'my_rag_continuation.py'
        original = path.read_text()
        old_task = "Use party_planning_retriever for superhero catering. Suggest one dish and cite its source label. Then say whether these notes establish the caterer's allergy policy. Do not invent a policy."
        new_task = 'Use party_planning_retriever to search for caterer allergy policy. State whether the returned notes establish a policy. Cite any supporting source; if none does, say the policy is not provided.'
        revised = original.replace(old_task, new_task).replace('party_planning_retriever("superhero catering")', 'party_planning_retriever("caterer allergy policy")')
        self.assertNotEqual(revised, original)
        lesson = (self.folder/'lessons/en/week-4-retrieval.md').read_text()
        given_version = re.search(r'```python title="my_rag_continuation.py — policy-query version"\n(.*?)```', lesson, re.S)[1]
        self.assertEqual(revised.strip(), given_version.strip())
        try:
            path.write_text(revised)
            calls, out = self.run_file('my_rag_continuation.py',[
                'print(party_planning_retriever(query="caterer allergy policy"))',
                'final_answer("The supplied notes do not provide the caterer allergy policy.")'])
            self.assertIn(new_task, json.dumps(calls[0]['messages']))
            self.assertIn('Catering Ideas', json.dumps(calls[1]['messages']))
            self.assertIn('do not provide', out)
        finally:
            path.write_text(original)

    def test_rag_actual_retrieval_reaches_model(self):
        calls, out = self.run_file('my_rag_continuation.py',[
            'print(party_planning_retriever(query="superhero catering"))',
            'final_answer("Hulk smoothie [Catering Ideas]. Allergy policy is not in these notes.")'])
        self.assertIn('DIRECT RETRIEVAL',out)
        self.assertIn('Catering Ideas',json.dumps(calls[1]['messages']))
        self.assertIn('Allergy policy is not',out)

    def test_two_agent_handoff_and_report(self):
        rows=json.dumps(self.fixtures())
        actions=self.research_actions()+['print(cargo_time(latitude=40.0, longitude=-70.0))',
            f'print(save_report(rows_json={rows!r}))','final_answer("Report saved; all rows are simulated fixtures.")']
        with patch.object(self.search,'DDGS') as ddgs, patch('smolagents.default_tools.VisitWebpageTool.forward',new=lambda self, url: 'SIMULATED PAGE EVIDENCE'):
            ddgs.return_value.text.return_value=[dict(title='Fixture',href='https://example.org/claim/0',body='SIMULATED SEARCH')]
            path = self.folder/'my_batman.py'
            original = path.read_text()
            path.write_text(original.replace('run_task(manager, ONE_LOCATION_TASK)', 'run_task(manager, TASK)'))
            try:
                calls,out=self.run_file('my_batman.py',actions)
            finally:
                path.write_text(original)
        self.assertIn('web_specialist',json.dumps(calls[0]['messages']))
        self.assertIn('SIMULATED PAGE EVIDENCE',json.dumps(calls[3]['messages']))
        self.assertIn('https://example.org/coords/3',json.dumps(calls[4]['messages']))
        report=(self.folder/'outputs/batman-report.html').read_text()
        self.assertIn('Fixture 3',report)
        self.assertEqual(report.count('<circle '),4)

    def test_optional_third_agent_is_called(self):
        code = self.runners['my_batman.py']
        code = code.replace('    manager = CodeAgent(', """    verifier = CodeAgent(
        tools=[WebSearchTool(), VisitWebpageTool()], model=model,
        name="verifier", description="Independently checks sourced claims and coordinates with evidence and uncertainty.",
        **agent_options(max_steps=12),
    )
    manager = CodeAgent(""", 1)
        code = code.replace('managed_agents=[specialist]', 'managed_agents=[specialist, verifier]')
        code = code.replace('def build_team(model):', 'TASK += " Ask verifier to independently check the sourced rows before saving."\n\ndef build_team(model):')
        code = code.replace('run_task(manager, ONE_LOCATION_TASK)', 'run_task(manager, TASK)')
        (self.folder/'my_batman_verified.py').write_text(code)
        rows=json.dumps(self.fixtures())
        actions=self.research_actions()+['print(verifier(task="Independently check https://example.org/claim/0"))',
            'print(visit_webpage(url="https://example.org/claim/0"))',
            'final_answer("Independent simulated verdict: uncertain")','final_answer("Unverified report withheld")']
        with patch.object(self.search,'DDGS') as ddgs, patch('smolagents.default_tools.VisitWebpageTool.forward',new=lambda self, url: 'SIMULATED PAGE EVIDENCE'):
            ddgs.return_value.text.return_value=[dict(title='Fixture',href='https://example.org/claim/0',body='SIMULATED SEARCH')]
            calls,out=self.run_file('my_batman_verified.py',actions)
        self.assertIn('Independent simulated verdict: uncertain',json.dumps(calls[-1]['messages']))
        self.assertIn('Unverified report withheld',out)

    def test_complete_given_program_executes_small_handoff(self):
        code = self.runners['my_batman.py']
        self.assertNotIn('SPECIALIST_TOOLS = []', code)
        self.assertNotIn('YOUR ', code)
        calls, out = self.run_file('my_batman.py', [
            'print(web_specialist(task="Check one location"))',
            'final_answer("SIMULATED supported claim https://example.org/claim; coordinate source missing")',
            'final_answer("Source https://example.org/claim retained; coordinates not established")'])
        self.assertIn('Wollaton Hall', json.dumps(calls[0]['messages']))
        self.assertIn('coordinate source missing', json.dumps(calls[2]['messages']))
        self.assertIn('coordinates not established', out)

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
            with patch.object(self.search, 'DDGS') as ddgs, patch('smolagents.default_tools.VisitWebpageTool.forward', new=lambda self, url: 'SIMULATED PAGE'), contextlib.redirect_stdout(io.StringIO()) as out:
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
