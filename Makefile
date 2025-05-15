fmt:
	pylint * --ignore="Makefile,README.md,requirements.txt,LICENSE,TODO.md,AUTHORS,version.txt"
	flake8 --exclude .venv

unittest:
	python -m unittest discover irolling/tests

all: fmt unittest
