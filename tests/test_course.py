"""Regression checks for authored content and the generated bilingual course."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import ast
import json
import re
import unittest
from zipfile import ZipFile
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
CODE = re.compile(r'^```([^\n]*)\n(.*?)^```[ \t]*$', re.M | re.S)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.language_links = []
        self.code_attributes = []
        self.lang = None
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
            if 'data-course-language' in attrs:
                self.language_links.append(attrs)
        if tag == 'code':
            self.code_attributes.append(attrs)


class MainNavigation(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.href = None
        self.label = []
        self.links = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'nav' and (self.depth or attrs.get('aria-label') in ('Navigation', 'ナビゲーション')):
            self.depth += 1
        if self.depth and tag == 'a':
            self.href = attrs.get('href')
            self.label = []

    def handle_data(self, data):
        if self.depth and self.href is not None:
            self.label.append(data)

    def handle_endtag(self, tag):
        if tag == 'a' and self.depth and self.href is not None:
            self.links.append((self.href, ' '.join(''.join(self.label).split())))
            self.href = None
        if tag == 'nav' and self.depth:
            self.depth -= 1


def headings(text):
    masked = CODE.sub(lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), text)
    return re.findall(r'^#{1,6} .*?\{ #([^} ]+) \}$', masked, re.M)


def nav_paths(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [p for item in value for p in nav_paths(item)]
    return [p for item in value.values() for p in nav_paths(item)]


class CourseTests(unittest.TestCase):
    def setUp(self):
        self.pages = sorted((ROOT / 'docs').glob('*.md'))
        config = yaml.safe_load((ROOT / 'mkdocs.yml').read_text())
        self.english_only = set(config['extra'].get('english_only_pages', []))
        self.shared_pages = [p for p in self.pages if p.name not in self.english_only]

    def test_all_pages_are_authored_in_both_languages(self):
        self.assertEqual({p.name for p in self.shared_pages},
                         {p.name for p in (ROOT / 'docs-ja').glob('*.md')})
        self.assertEqual(len(self.shared_pages), 19)
        self.assertEqual({p.name for p in self.pages} - {p.name for p in self.shared_pages}, self.english_only)
        for en in self.shared_pages:
            with self.subTest(page=en.name):
                a = en.read_text()
                b = (ROOT / 'docs-ja' / en.name).read_text()
                self.assertTrue(re.search('[ぁ-んァ-ヶ一-龯]', b))
                self.assertNotIn('{{CODE:', b)
                self.assertEqual(headings(a), headings(b))
                self.assertTrue(headings(a))
                self.assertEqual(CODE.findall(a), CODE.findall(b))
                # Preserve all links and exercises, including literal test prompts.
                links = lambda s: Counter(link for link in re.findall(r'\]\(([^)]+)\)', s)
                                          if link.split('#')[0] not in self.english_only)
                self.assertEqual(links(a), links(b))
                prompts = lambda s: re.findall(r'^> .+$', s, re.M)
                self.assertEqual(prompts(a), prompts(b))

    def test_two_week_sequence_and_language_navigation_parity(self):
        en = yaml.safe_load((ROOT / 'mkdocs.yml').read_text())
        ja = yaml.safe_load((ROOT / 'mkdocs.ja.yml').read_text())
        self.assertEqual([p for p in nav_paths(en['nav']) if p not in self.english_only],
                         nav_paths(ja['nav']))
        self.assertEqual(set(nav_paths(ja['nav'])), {p.name for p in self.shared_pages})
        self.assertEqual(set(nav_paths(en['nav'])), {p.name for p in self.pages})
        self.assertIn('Week 1', next(iter(en['nav'][1])))
        self.assertIn('Week 2', next(iter(en['nav'][2])))
        self.assertNotIn('run-your-first-agent.md', nav_paths(en['nav'][1]))
        self.assertEqual(nav_paths(en['nav'][2])[1:4], [
            'run-your-first-agent.md', 'understand-the-template.md', 'first-agent-practical.md'])
        self.assertIn('week-1-completion', headings((ROOT / 'docs/week-1-learning-plan.md').read_text()))
        self.assertIn('finish-the-practical', headings((ROOT / 'docs/quizzes.md').read_text()))

    def test_dummy_python_is_syntactically_valid(self):
        for lang in ['docs', 'docs-ja']:
            blocks = CODE.findall((ROOT / lang / 'dummy-agent-local.md').read_text())
            ast.parse('\n'.join(body for kind, body in blocks if kind == 'python'))

    def test_every_generated_local_link_and_fragment(self):
        site = (ROOT / 'site').resolve()
        parsed = {}
        for en in self.pages:
            for lang in ([''] if en.name in self.english_only else ['', 'ja']):
                file = site / lang / ('' if en.stem == 'index' else en.stem) / 'index.html'
                parsed[file] = Page(file)
        for file, page in parsed.items():
            for href in page.links:
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                destination = (file.parent / unquote(url.path)).resolve() if url.path else file
                if destination.is_dir():
                    destination /= 'index.html'
                with self.subTest(page=str(file.relative_to(site)), href=href):
                    self.assertTrue(destination.is_relative_to(site))
                    self.assertTrue(destination.is_file())
                    if url.fragment and destination.suffix == '.html':
                        target = parsed.get(destination) or Page(destination)
                        self.assertIn(unquote(url.fragment), target.ids)

    def test_switches_return_to_same_lesson_and_code_is_protected(self):
        site = (ROOT / 'site').resolve()
        for en in self.pages:
            for lang, other in ([('', 'ja')] if en.name in self.english_only else [('', 'ja'), ('ja', '')]):
                suffix = '' if en.stem == 'index' else en.stem
                file = site / lang / suffix / 'index.html'
                page = Page(file)
                with self.subTest(page=str(file.relative_to(site))):
                    self.assertEqual(page.lang, lang or 'en')
                    if en.name in self.english_only:
                        self.assertEqual(page.language_links, [])
                        self.assertIn('data-course-language-pending', file.read_text())
                        self.assertIn('aria-disabled="true"', file.read_text())
                        self.assertFalse((site / 'ja' / suffix / 'index.html').exists())
                        self.assertTrue(set(headings(en.read_text())).issubset(page.ids))
                        continue
                    self.assertEqual(len(page.language_links), 1)
                    link = page.language_links[0]
                    self.assertEqual(link['hreflang'], other or 'en')
                    self.assertTrue(link.get('aria-label'))
                    self.assertEqual((file.parent / link['href']).resolve(),
                                     (site / other / suffix).resolve())
                    self.assertNotIn('target', link)
                    self.assertTrue(all(a.get('translate') == 'no' for a in page.code_attributes))
                    self.assertNotIn('translate.google.com', file.read_text())
                    self.assertNotIn('http-equiv="refresh"', file.read_text())
                    self.assertTrue(set(headings(en.read_text())).issubset(page.ids))

    def test_week03_bilingual_content_and_curated_download(self):
        self.assertEqual(self.english_only, set())
        pack = ROOT / 'docs/downloads/week03-smolagents.zip'
        expected = {p.name for p in (ROOT / 'week03-starter').iterdir() if p.suffix in ('.py', '.json', '.md', '.txt')}
        with ZipFile(pack) as archive:
            self.assertEqual({Path(n).name for n in archive.namelist()}, expected)
            for name in archive.namelist():
                self.assertTrue(name.startswith('week03-exercises/'))
                self.assertNotIn('..', Path(name).parts)
                self.assertEqual(archive.read(name), (ROOT / 'week03-starter' / Path(name).name).read_bytes())
                if name.endswith('.py'):
                    ast.parse(archive.read(name).decode())
            source = archive.read('week03-exercises/week03_tools.py').decode()
            self.assertIn('def catering_service_tool', source)
            self.assertIn('class SuperheroPartyThemeTool', source)
            self.assertNotIn('calculate_study_time', source)
            self.assertNotIn('NotImplementedError', source)
            self.assertEqual(len(archive.namelist()), 6)
            requirements = archive.read('week03-exercises/week03-requirements.txt').decode()
            self.assertIn('smolagents==1.13.0', requirements)
            self.assertIn('openai>=1.0,<3', requirements)
            self.assertIn('ddgs==9.16.0', requirements)
            self.assertNotIn('gradio', requirements.lower())
            self.assertNotIn('langchain', requirements.lower())
            self.assertFalse(any('retriev' in name or 'team' in name for name in archive.namelist()))
            self.assertEqual(archive.read('week03-exercises/week03-HF-LICENSE.txt'),
                             (ROOT / 'docs/licenses/huggingface-agents-course.txt').read_bytes())
        for name in [p.name for p in self.pages if p.name.startswith(('week-3-', 'week-4-'))]:
            source = (ROOT / 'docs' / name).read_text()
            self.assertTrue(headings(source))
            self.assertNotIn('{{CODE:', source)
        for name in [p.name for p in self.pages if p.name.startswith(('week-3-', 'week-4-'))]:
            for kind, body in CODE.findall((ROOT / 'docs' / name).read_text()):
                if kind.split()[0] == 'python':
                    ast.parse(body)

    def test_hf_images_are_real_and_match_built_assets(self):
        import hashlib
        folder = ROOT / 'docs/images/huggingface'
        records = json.loads((folder / 'sources.json').read_text())
        self.assertGreaterEqual(len(records), 9)
        for record in records:
            data = (folder / record['file']).read_bytes()
            self.assertTrue(record['source'].startswith('https://huggingface.co/datasets/'))
            self.assertTrue(data.startswith((b'\x89PNG', b'GIF8', b'\xff\xd8')))
            self.assertEqual(hashlib.sha256(data).hexdigest(), record['sha256'])
            for lang in ['', 'ja']:
                self.assertEqual(data, (ROOT / 'site' / lang / 'images/huggingface' / record['file']).read_bytes())

    def test_week03_menu_labels_and_destinations_are_consistent(self):
        for lang, config_name in [('', 'mkdocs.yml'), ('ja', 'mkdocs.ja.yml')]:
            config = yaml.safe_load((ROOT / config_name).read_text())
            entries = list(config['nav'][3].values())[0] + [config['nav'][4]]
            expected = [(label, (ROOT / 'site' / lang / Path(source).stem / 'index.html').resolve())
                        for entry in entries for label, source in entry.items()]
            self.assertEqual([label[:2] for label, _ in expected[1:6]],
                             ['08', '09', '10', '11', '12'])
            destinations = {target for _, target in expected}
            for label, file in expected:
                self.assertIn(label, re.sub('<[^>]+>', '', file.read_text()))
                links = []
                for href, text in MainNavigation(file).links:
                    url = urlsplit(href)
                    if url.scheme or url.netloc or url.fragment:
                        continue
                    target = (file.parent / unquote(url.path)).resolve()
                    if target.is_dir():
                        target /= 'index.html'
                    if target in destinations:
                        links.append((text, target))
                self.assertEqual(links, expected, file)
        for removed in ('week-3-retrieval', 'week-3-multi-agent', 'week-3-vision-browser'):
            self.assertFalse((ROOT / 'site' / removed).exists())

    def test_downloads_search_and_error_pages(self):
        for path in (ROOT / 'docs/downloads').iterdir():
            self.assertEqual(path.read_bytes(), (ROOT / 'site/downloads' / path.name).read_bytes())
            self.assertEqual(path.read_bytes(), (ROOT / 'site/ja/downloads' / path.name).read_bytes())
        for lang in ['', 'ja']:
            index = json.loads((ROOT / 'site' / lang / 'search/search_index.json').read_text())
            self.assertTrue(index['docs'])
            if lang == 'ja':
                self.assertTrue(any('エージェント' in d['text'] for d in index['docs']))
        self.assertIn('ページが見つかりません', (ROOT / 'site/ja/404.html').read_text())
        self.assertIn('Page not found', (ROOT / 'site/404.html').read_text())


if __name__ == '__main__':
    unittest.main()
