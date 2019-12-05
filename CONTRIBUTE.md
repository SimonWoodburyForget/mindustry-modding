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

# Building `styles/main/js/main.js`

This script is generated with Clojure's ClojureScript compiler from:

```
helper/style.cljs
```

You don't need to rebuild it unless you modify the script itself, to build and test figwheel is used:

```
lein figwheel
```

Figwheel will start a server on port 3449, and will periodically inject JS/CSS into the runtime as you change and save it. Figwheel will output files into a `styles/main/js/main/out/` subdirectory, instead of into a single file, so it's output shouldn't be used directly.

To build a release version, `cljsbuild` is used, and is configured to run with advanced optimizations:

```
lein cljsbuild once release
```
