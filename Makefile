
texi:
	emacs index.org --batch -f org-texinfo-export-to-texinfo

html: clean texi
	makeinfo index.texi --html --no-split --css-include style.css
	rm index.texi

html-doc: clean texi
	makeinfo index.texi --html --css-include style.css -o docs
	rm index.texi 

clean:
	rm index.texi -f
	rm index.html -f
	rm docs -fr

dist: html
	rm index.texi -f
