# Put Agent Lab on GitHub Pages

These steps publish the guide and starter download. They do not host the running Python agent.

## 1. Create the repository

Sign in at https://github.com/new. Choose a repository name such as agent-lab, select Public, and create it. GitHub Pages is available for public repositories on GitHub Free. If using an existing repository, use a dedicated course repository and preserve its existing files.

## 2. Upload this folder's contents

Unzip the supplied package. Open the inner agent-lab folder in Finder. Press Command + Shift + . (period) to show hidden files.

On GitHub, choose "uploading an existing file" on an empty repository, or Add file → Upload files. Drag the CONTENTS of agent-lab into the upload area, including docs, .github, .gitignore, mkdocs.yml, requirements-docs.txt, README.md, and this publishing guide. Commit the upload to main.

Do not upload the ZIP as a single file. Do not add an extra enclosing agent-lab folder: mkdocs.yml must appear at the repository root.

Check that .github/workflows/publish.yml appears in GitHub. If the hidden folder was omitted, use Add file → Create new file, name it .github/workflows/publish.yml, paste the contents of the supplied workflow, and commit.

This curated package excludes local environments, backups, test runs, and key files. No Groq API key or GitHub Actions secret is needed for publishing.

## 3. Wait for the website build

Open the repository's Actions tab. The "Publish course website" workflow should run after the upload. Wait for a green check. It creates a gh-pages branch containing the generated website.

If Actions is disabled, enable Actions for this repository. If a run fails, open the failed step for its message. Check that main is the default/upload branch and that mkdocs.yml and requirements-docs.txt are at its root. Repository or organization policies may restrict workflow write access.

## 4. Turn on GitHub Pages

Open Settings → Pages. Under Build and deployment:

- Source: Deploy from a branch.
- Branch: gh-pages.
- Folder: / (root).
- Click Save.

Use these exact settings for the supplied workflow: GitHub Actions builds the site, and the generated gh-pages branch is the Pages publishing source. Do not select main/docs, which contains unbuilt Markdown.

If gh-pages is missing, wait for Step 3 to succeed and refresh Settings.

## 5. Share the website

After deployment, Settings → Pages displays the site address, normally:

    https://YOUR-GITHUB-USERNAME.github.io/agent-lab/

Replace agent-lab if you chose another repository name. Open the address, visit a lesson, and test the starter download. Students do not need a GitHub account to read this public site. The website stays available when your Mac is off.

## 6. Make future updates

Edit Markdown under docs/ on main and commit. The workflow republishes the site automatically. If you maintain local copies, keep this publishing copy and the original course source synchronized. Updates in one local folder do not automatically update the other.

## Official references

- https://squidfunk.github.io/mkdocs-material/publishing-your-site/
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

Prepared locally; deployment to a real GitHub repository has not yet been tested.
