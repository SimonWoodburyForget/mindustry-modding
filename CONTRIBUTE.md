# Building `index.html`

Currently a four step process is used to generate the `index.html`:

1. copy `index.org` to `index.tmp.org`
2. generate templates with jinja2 *(for change log)*
3. generate `index.tmp.org` with Org Mode
4. copy `index.tmp.thml` to `index.html`

Expected dependencies required to generate the `index.html` are the following:

- emacs26
- python3.8
  - humanize
  - PyGitHub
  - PyYAML
  - Jinja2
  - Click

Running Org-Mode's html export alone is sufficient for testing. Add a `mindustry-modding` symlink in the root of the project, pointing back to the root of the project, if you want to test/render the style locally, or change the links within the `HTML_HEAD` in the org file.
