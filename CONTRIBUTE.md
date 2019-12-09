# Modifying `index.org`

The `.org` file at the root of the project is the meat of everything. It starts with some metadata *(`#+WORD: ..` and `:PREAMBEL: ... :END:`)* which you can easily skip over.

Sections are split-up with `* Headline`. It's important for `*` to be prefixed with a newline and no white spaces, and it shouldn't be confused with ` *` which is actually just an unnamed list element.

Sections themselves may be referenced with `[[Section Name][Description text]]`

Tables are much like Markdown tables, except that you may see some metadata flags in them to assist org-mode in knowing how to align things or whether to cutoff overflow text:

```org
| column1 | column2    |
|---------|------------|
|         | <8>        |
| value   | long val=> |
```

You can `*bold*` `/italic/` and `~inline code~` text or use code blocks:

```org
#+BEGIN_SRC js
// block code
const x = "This is JavaScript";
print(x);
#+END_SRC
```

`js` should be used for JavaScript, as it colors the output text itself,  `yaml` mode is what is currently used for `hjson`, because it usually lines up nicely, and `json` can be used for `json` itself, although `yaml` would just work. `fundamental` for anything that not uncolored.

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
