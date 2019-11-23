clean:
	rm index.texi -f
	rm index.html -f
	rm index.tmp.org -f
	rm docs -rf

dist:
	@echo "Making README.org..."
	python3.8 helper contents -i index.org -o README.org
	@echo "Making log section..."
	python3.8 helper build-index -i index.org -o index.tmp.org
	@echo "Making texi file..."
	emacs index.tmp.org --batch -f org-texinfo-export-to-texinfo
	@echo "Mmaking html file..."
	makeinfo index.tmp.texi --html --no-split --css-include style.css
