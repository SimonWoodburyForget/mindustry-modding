# Building `index.html`

Currently a four step process is used to generate the `index.html`:

1. copy `index.org` to `index.tmp.org`
2. generate templates with jinja2 *(for change log and `README.md` content table)*
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

Running Org-Mode's html export alone is sufficient for testing.
