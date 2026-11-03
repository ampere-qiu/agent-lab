"""Build English Week 4 ZIPs; unreleased Japanese lessons are excluded."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import re

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ["README.md", "NOTICE.md", "HF-LICENSE.txt", "requirements.txt", "week04_common.py",
           "week04_search.py", "week04_retriever.py", "week04_tools.py", "week04_browser.py", "prepare_visuals.py"]
PACKAGES = ["week04-smolagents-part2.zip", "week4_batman_guided_student.zip", "week4_vision_browser_student.zip"]


def package():
    for name in PACKAGES:
        with ZipFile(ROOT / "docs/downloads" / name, "w", ZIP_DEFLATED) as archive:
            for support in SUPPORT:
                archive.write(ROOT / "week04-starter" / support, "week04-exercises/" + support)
            for lang, folder in [("en", "docs")]:
                for lesson in sorted((ROOT / folder).glob("week-4-*.md")):
                    text = lesson.read_text(encoding="utf-8")
                    # Offline copies already contain the support files. Prior-week context
                    # is summarized in README; no website-only relative links remain.
                    text = re.sub(r'\]\(downloads/[^)]+\)', '](../../README.md#downloads)', text)
                    text = re.sub(r'\]\(week-3-[^)]+\)', '](../../README.md#week-03-context)', text)
                    archive.writestr(f"week04-exercises/lessons/{lang}/{lesson.name}", text)
                for asset in sorted((ROOT / "docs/images/huggingface-week04").iterdir()):
                    if asset.is_file():
                        archive.write(asset, f"week04-exercises/lessons/{lang}/images/huggingface-week04/{asset.name}")
    print("Packaged three self-contained Week 4 downloads with original HF figures.")


if __name__ == "__main__":
    package()
