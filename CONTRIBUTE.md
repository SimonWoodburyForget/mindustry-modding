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

You don't need to rebuild it unless you modify the script itself, to build and test cljsbuild auto is used:

```
lein cljsbuild auto app
```

App will output files into a `styles/main/js/main/out/` subdirectories, instead of into a single file, so it's output shouldn't be used directly, but this allows it to compile fast.

To compile a release version `release` is used, and is configured to run with advanced optimizations:

```
lein cljsbuild once release
```
