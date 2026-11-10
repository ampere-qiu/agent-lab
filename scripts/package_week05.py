"""Package the matching Week 5 English/Japanese lessons and support files."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import re

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/downloads/week05-llamaindex.zip"


def package():
    entries = []
    for source in sorted((ROOT / "week05-starter").iterdir()):
        if source.is_file() and source.suffix in (".py", ".txt", ".md"):
            entries.append((source.name, source.read_bytes()))
    for source in sorted((ROOT / "docs/images/huggingface-week05").iterdir()):
        if source.is_file():
            entries.append(("images/huggingface-week05/" + source.name, source.read_bytes()))
    for lang, folder in [("en", "docs"), ("ja", "docs-ja")]:
        for source in sorted((ROOT / folder).glob("week-5-*.md")):
            text = source.read_text(encoding="utf-8")
            text = text.replace("](images/huggingface-week05/", "](../../images/huggingface-week05/")
            text = re.sub(r'\]\(downloads/[^)]+\)', '](../../README.md)', text)
            prefix = "ja/" if lang == "ja" else ""
            text = re.sub(r'\]\((week-[1-4][^#)]+\.md)(#[^)]*)?\)',
                          lambda m: f"](https://ampere-qiu.github.io/agent-lab/{prefix}{Path(m[1]).stem}/{m[2] or ''})", text)
            entries.append((f"lessons/{lang}/{source.name}", text.encode("utf-8")))
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for name, body in entries:
            info = ZipInfo("week05-exercises/" + name, date_time=(2026, 11, 9, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, body)
    print("Packaged:", OUTPUT.name, f"({len(entries)} files)")


if __name__ == "__main__":
    package()
