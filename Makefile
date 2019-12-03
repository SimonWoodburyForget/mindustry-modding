clean:
	rm index.texi -f
	rm index.html -f
	rm index.tmp.org -f
	rm docs -rf

org:
	@echo "Making README.org..."
	python3.8 helper contents -i index.org -o README.org
	@echo "Making log section..."
	python3.8 helper build-index -i index.org -o index.tmp.org

index:
	rm index.html -f
	rm index.tmp.org -f
	mv index.tmp.html index.html
