
texi:
	emacs index.org --batch -f org-texinfo-export-to-texinfo

html: clean texi
	makeinfo index.texi --html --force --no-split --css-include style.css

epub: build texi
	makeinfo index.texi --epub --force --css-include style.css

clean:
	rm index.texi -f
	rm index.html -f
	rm index -f
	rm index.epub -f

dist: html
	rm index.texi -f
