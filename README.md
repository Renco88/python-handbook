# Python Handbook

A professional, static, beginner-friendly Python learning book.

## What is included
- 18 structured chapters from Python fundamentals to professional projects
- Beginner-friendly explanations
- Runnable code examples
- Practice challenges and common mistakes
- One Jupyter/Colab notebook per chapter
- Responsive UI
- Copy-code buttons
- Reading progress indicator
- No npm, no build step, no backend

## GitHub Pages deployment
1. Upload this folder to a repository named `python-handbook`.
2. Push to GitHub.
3. In GitHub: Settings → Pages.
4. Select **Deploy from a branch**.
5. Select `main` and `/ (root)`.
6. Save.

The expected Colab links use:
`https://colab.research.google.com/github/renco88/python-handbook/blob/main/notebooks/...`

If the repository name or GitHub username changes, update the Colab links in the chapter HTML files.

## Local preview
Open `index.html` directly, or run:
`python -m http.server 8000`
Then visit `http://localhost:8000`.

## Git
Correct commit syntax:
`git add .`
`git commit -m "Build complete Python handbook"`
`git push`
