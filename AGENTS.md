# Lesson editing workflow

- Maintain the lessons in English. Japanese reading uses Google Translate's website view or the user's browser translation feature; do not create separate Japanese lesson versions.
- Keep the 日本語 button linked to the matching published lesson in Google Translate, and retain browser-translation instructions at /ja/.
- Preserve code blocks, commands, identifiers, filenames, and test prompts. Code must be marked `translate="no"` in the generated site.
- Write and validate lesson changes in English for Ampere's review.
- Build with `.venv/bin/python -m mkdocs build --strict` from this directory.
- Keep previous Japanese lesson URLs working through the redirects in `hooks/translation.py`.
- Do not copy changes to GitHub or publish without a request to do so.
