"""Package only the curated Week 03 exercise files, excluding local state."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    'week03_README.md', 'week03_common.py', 'week03_tools.py',
    'week03_search.py', 'week03-requirements.txt', 'week03-HF-LICENSE.txt',
]


def package():
    destination = ROOT / 'docs/downloads/week03-smolagents.zip'
    with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
        for name in FILES:
            archive.write(ROOT / 'week03-starter' / name, f'week03-exercises/{name}')
    print(f'Packaged {len(FILES)} exercise files.')


if __name__ == '__main__':
    package()
