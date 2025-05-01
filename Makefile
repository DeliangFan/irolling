fmt:
	pylint * --ignore="Makefile,README.md,requirements.txt,LICENSE,TODO.md,AUTHORS,version.txt"
	flake8 --exclude .venv

all: fmt
