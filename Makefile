PYTHON = python3
MAIN = a_maze_ing.py
CONFIG_FILE = config.txt


install:
	poetry install
run: install
	poetry run python3 ${MAIN} ${CONFIG_FILE}
debug: install
	poetry run python3 -m pdb ${MAIN} ${CONFIG_FILE}
lint: 
	poetry run flake8 .
	poetry run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
clean:
	rm -rf */__pycache__ .mypy_cache