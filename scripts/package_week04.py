"""Build bilingual Week 4 ZIPs with shared helpers and original figures."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import re

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ["README.md", "NOTICE.md", "HF-LICENSE.txt", "requirements.txt", "week04_common.py",
           "week04_search.py", "week04_tools.py", "week04_browser.py", "prepare_visuals.py"]
PACKAGES = ["week04-smolagents-part2.zip", "week4_batman_guided_student.zip", "week4_vision_browser_student.zip"]


def package():
    for name in PACKAGES:
        with ZipFile(ROOT / "docs/downloads" / name, "w", ZIP_DEFLATED) as archive:
            for support in SUPPORT:
                archive.write(ROOT / "week04-starter" / support, "week04-exercises/" + support)
            for lang, folder in [("en", "docs"), ("ja", "docs-ja")]:
                for lesson in sorted((ROOT / folder).glob("week-4-*.md")):
                    text = lesson.read_text(encoding="utf-8")
                    # Offline copies already contain the support files. Prior-week practice links
                    # target the published Week 3 lessons; no website-only relative links remain.
                    text = re.sub(r'\]\(downloads/[^)]+\)', '](../../README.md#downloads)', text)
                    text = re.sub(
                        r'\]\((week-3-[^#)]+\.md)(#[^)]*)?\)',
                        lambda match: f"](https://ampere-qiu.github.io/agent-lab/{'ja/' if lang == 'ja' else ''}{Path(match[1]).stem}/{match[2] or ''})",
                        text,
                    )
                    archive.writestr(f"week04-exercises/lessons/{lang}/{lesson.name}", text)
                for image_folder in ["huggingface-week04", "week04"]:
                    for asset in sorted((ROOT / "docs/images" / image_folder).iterdir()):
                        if asset.is_file():
                            archive.write(asset, f"week04-exercises/lessons/{lang}/images/{image_folder}/{asset.name}")
    print("Packaged three self-contained Week 4 downloads with original HF figures.")


if __name__ == "__main__":
    package()
