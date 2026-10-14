"""Protect code during browser translation and preserve former Japanese URLs."""
from pathlib import Path
import html
import json
import re


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
