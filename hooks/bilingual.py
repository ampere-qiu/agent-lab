"""Build two native-language sites with matching lesson URLs, without new plugins."""
from pathlib import Path
import shutil
import posixpath
import re
import subprocess
import sys


def on_pre_build(config):
    # Defaults also keep the language menu usable on the generated 404 page.
    japanese = config.theme['language'] == 'ja'
    config.extra['alternate'] = [
        {'name': 'English', 'lang': 'en', 'link': '../' if japanese else '.',
         'href': '../' if japanese else './'},
        {'name': '日本語', 'lang': 'ja', 'link': '.' if japanese else 'ja/',
         'href': './' if japanese else 'ja/'},
    ]
    if config.theme['language'] == 'ja':
        root = Path(config.config_file_path).parent
        # Shared downloads and styling always come from the English source.
        for folder in ('downloads', 'stylesheets', 'javascripts'):
            shutil.copytree(root / 'docs' / folder, Path(config.docs_dir) / folder,
                            dirs_exist_ok=True)


def on_page_context(context, page, config, nav):
    root = Path(config.config_file_path).parent
    japanese = config.theme['language'] == 'ja'
    source = page.file.src_uri
    counterpart = root / ('docs' if japanese else 'docs-ja') / source
    translated = counterpart.is_file()
    target = page.url if translated else ''
    config.extra['alternate'] = [
        {'name': 'English', 'lang': 'en',
         'link': '../' + target if japanese else page.url},
        {'name': '日本語' if translated or japanese else '日本語（準備中）',
         'lang': 'ja', 'link': page.url if japanese else 'ja/' + target},
    ]
    current_dir = posixpath.dirname(('ja/' if japanese else '') + page.file.dest_uri)
    for alternative in config.extra['alternate']:
        destination = ('ja/' if alternative['lang'] == 'ja' else '') + (
            page.url if alternative['lang'] == config.theme['language'] or translated else '')
        alternative['href'] = posixpath.relpath(destination or '.', current_dir or '.') + '/'
    return context


def on_post_page(output, page, config):
    # Hreflang metadata and the header share the same resolved links.
    links = {a['lang']: a['href'] for a in config.extra['alternate']}
    return re.sub(r'<link rel="alternate" href="[^"]*" hreflang="(en|ja)">',
                  lambda m: f'<link rel="alternate" href="{links[m[1]]}" hreflang="{m[1]}">',
                  output)


def on_post_build(config):
    if config.theme['language'] != 'ja':
        root = Path(config.config_file_path).parent
        subprocess.run([sys.executable, '-m', 'mkdocs', 'build', '--strict',
                        '-f', str(root / 'mkdocs.ja.yml'),
                        '-d', str(Path(config.site_dir) / 'ja')], check=True)
