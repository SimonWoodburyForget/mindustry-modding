# Building `index.html`

Currently there's three steps to build the `index.html`:

1. generate templates with jinja2;
2. activate [export-to-html-with-useful-anchors](https://github.com/alphapapa/unpackaged.el#export-to-html-with-useful-anchors)))) minor mode;
3. generate `index.html` with org-modes html export function.

Expected dependencies required to generate the `README.md` are the following:

- python3.8
- Jinja2
- Click

I use Emacs 26 to generate the `index.html` with:

- https://github.com/alphapapa/unpackaged.el#export-to-html-with-useful-anchors minor mode which gives the exported anchors better names without adding `:CUSTOM_ID:` to everything.

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
