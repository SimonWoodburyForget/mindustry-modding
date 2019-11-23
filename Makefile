clean:
	rm index.texi -f
	rm index.html -f
	rm index.tmp.org -f
	rm docs -rf

dist:
	python3.8 helper contents -i index.org -o README.org
	python3.8 helper build-index -i index.org -o index.tmp.org
	emacs index.tmp.org --batch -f org-texinfo-export-to-texinfo
	makeinfo index.tmp.texi --html --no-split --css-include style.css



