
build: clean
	emacs index.org --batch -f org-texinfo-export-to-texinfo
	makeinfo index.texi --html --force --no-split --css-include style.css

clean:
	rm index.texi -f
	rm index.html -f

dist: build
	rm index.texi -f
