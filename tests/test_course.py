"""Regression checks for authored content and the generated bilingual course."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import ast
import json
import re
import unittest
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

    def test_all_pages_are_authored_in_both_languages(self):
        self.assertEqual({p.name for p in self.pages},
                         {p.name for p in (ROOT / 'docs-ja').glob('*.md')})
        self.assertEqual(len(self.pages), 12)
        for en in self.pages:
            with self.subTest(page=en.name):
                a = en.read_text()
                b = (ROOT / 'docs-ja' / en.name).read_text()
                self.assertTrue(re.search('[ぁ-んァ-ヶ一-龯]', b))
                self.assertNotIn('{{CODE:', b)
                self.assertEqual(headings(a), headings(b))
                self.assertTrue(headings(a))
                self.assertEqual(CODE.findall(a), CODE.findall(b))
                # Preserve all links and exercises, including literal test prompts.
                links = lambda s: Counter(re.findall(r'\]\(([^)]+)\)', s))
                self.assertEqual(links(a), links(b))
                prompts = lambda s: re.findall(r'^> .+$', s, re.M)
                self.assertEqual(prompts(a), prompts(b))

    def test_two_week_sequence_and_language_navigation_parity(self):
        en = yaml.safe_load((ROOT / 'mkdocs.yml').read_text())
        ja = yaml.safe_load((ROOT / 'mkdocs.ja.yml').read_text())
        self.assertEqual(nav_paths(en['nav']), nav_paths(ja['nav']))
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
            for lang in ['', 'ja']:
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
            for lang, other in [('', 'ja'), ('ja', '')]:
                suffix = '' if en.stem == 'index' else en.stem
                file = site / lang / suffix / 'index.html'
                page = Page(file)
                with self.subTest(page=str(file.relative_to(site))):
                    self.assertEqual(page.lang, lang or 'en')
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
