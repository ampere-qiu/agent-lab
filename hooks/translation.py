"""Protect code during browser translation and preserve former Japanese URLs."""
from pathlib import Path
import html
import json
import re
from urllib.parse import urlencode, urljoin


def translate_link(public_url):
    return 'https://translate.google.com/translate?' + urlencode({
        'sl': 'en', 'tl': 'ja', 'hl': 'ja', 'u': public_url,
    })


def on_config(config):
    config.extra['translation_home_url'] = translate_link(config.extra['translation_base_url'])
    return config


def on_page_context(context, page, config, nav):
    # Use the published counterpart even in a localhost preview. Google cannot
    # fetch a site running only on the student's computer.
    context['course_translation_url'] = translate_link(
        urljoin(config.extra['translation_base_url'], page.url))
    return context


def on_post_page(output, page, config):
    return re.sub(r'<code(?=[\s>])', '<code translate="no"', output)


def on_post_build(config):
    # The old /ja/ home remains a Japanese help page. Old lesson links lead to
    # the corresponding maintained English page, which browsers can translate.
    site = Path(config.site_dir)
    for source in Path(config.docs_dir).glob('*.md'):
        if source.name == 'index.md':
            continue
        target = '../../' + source.stem + '/'
        destination = site / 'ja' / source.stem / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Agent Lab — lesson moved</title>'
            f'<meta http-equiv="refresh" content="0; url={html.escape(target)}">'
            '</head><body><p>This lesson is available in English with browser translation. '
            f'<a href="{html.escape(target)}">Open lesson</a></p>'
            f'<script>location.replace({json.dumps(target)} + location.search + location.hash);</script>'
            '</body></html>', encoding='utf-8')
