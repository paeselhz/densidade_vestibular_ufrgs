.PHONY: all
all: environment code_style run

.PHONY: environment
environment:
	python3 -m venv dv_ufrgs
	dv_ufrgs/bin/pip install -r requirements.txt

.PHONY: code_style
code_style:
	dv_ufrgs/bin/black --exclude '/(venv|env|build|dist|dv_ufrgs)/' .
	dv_ufrgs/bin/isort . --skip venv --skip env --skip dv_ufrgs

.PHONY: data_extraction
data_extraction:
	dv_ufrgs/bin/python data_extraction/main.py

.PHONY: run
run:
	shiny run shiny_app/app.py

.PHONY: build_shinylive
build_shinylive:
	shinylive export shiny_app docs
	python3 -m http.server --directory docs --bind localhost 8080

.PHONY: clean
clean:
	rm -rf dv_ufrgs
	find . -name '*.pyc' -delete

.PHONY: clear
clear: clean
	dv_ufrgs/bin/pip uninstall -y -r requirements.txt