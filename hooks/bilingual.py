"""Build authored English/Japanese lessons and preserve corresponding URLs."""
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import sys


def on_pre_build(config):
    root = Path(config.config_file_path).parent
    japanese = config.theme['language'] == 'ja'
    # Default for the 404 page; lesson contexts resolve their own relative links.
    config.extra['course_language'] = 'ja' if japanese else 'en'
    config.extra['course_alternate'] = '../' if japanese else 'ja/'
    if japanese:
        for folder in ('downloads', 'stylesheets', 'javascripts', 'images', 'licenses'):
            shutil.copytree(root / 'docs' / folder, Path(config.docs_dir) / folder,
                            dirs_exist_ok=True)


def on_page_context(context, page, config, nav):
    japanese = config.theme['language'] == 'ja'
    prefix = 'ja/' if japanese else ''
    current_dir = posixpath.dirname(prefix + page.file.dest_uri)
    target = ('' if japanese else 'ja/') + page.url
    root = Path(config.config_file_path).parent
    counterpart = root / ('docs' if japanese else 'docs-ja') / page.file.src_uri
    context['course_translation_available'] = counterpart.is_file() and (japanese or page.file.src_uri not in config.extra.get('unreleased_translations', []))
    context['course_alternate'] = posixpath.relpath(target or '.', current_dir or '.') + '/'
    context['course_language'] = 'ja' if japanese else 'en'
    return context


def pending_translation_markdown(source_path):
    """Public placeholder; never expose the unpublished Japanese lesson body."""
    anchor = Path(source_path).stem
    return (
        f"# Japanese edition — To be released {{ #{anchor} }}\n\n"
        "**Week 04 Japanese edition: To be released.**\n\n"
        "第04週の日本語版は準備中です。現在は英語版のみ公開しています。\n\n"
        "Use the **EN** language switch above to read the released English lesson.\n"
    )


def on_page_markdown(markdown, page, config, files):
    if (config.theme['language'] == 'ja'
            and page.file.src_uri in config.extra.get('unreleased_translations', [])):
        return pending_translation_markdown(page.file.src_uri)
    return markdown


def on_post_page(output, page, config):
    return re.sub(r'<code(?=[\s>])', '<code translate="no"', output)


def on_post_build(config):
    if config.theme['language'] != 'ja':
        root = Path(config.config_file_path).parent
        subprocess.run([sys.executable, '-m', 'mkdocs', 'build', '--strict',
                        '-f', str(root / 'mkdocs.ja.yml'),
                        '-d', str(Path(config.site_dir) / 'ja')], check=True)
