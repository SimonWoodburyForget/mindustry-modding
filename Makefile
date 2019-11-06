clean:
	rm index.texi -f
	rm index.html -f
	rm docs -rf

texi:
	emacs index.org --batch -f org-texinfo-export-to-texinfo

html: texi
	rm index.html -f
	makeinfo index.texi --html --no-split --css-include style.css

html-doc: texi
	rm docs -rf
	makeinfo index.texi --html --css-include style.css -o docs

dist: html
	rm index.texi -f
