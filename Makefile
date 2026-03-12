PYTHON = python3
VENV_NAME = mazevenv
DEPENDECIES = requirement.txt
MAIN = mazegen/a_maze_ing.py
CONFIG_FILE = config.txt

$(VENV_NAME):
	${PYTHON} -m venv ${VENV_NAME}

install: $(VENV_NAME)
	${VENV_NAME}/bin/pip install -r ${DEPENDECIES}
run: install
	${VENV_NAME}/bin/python3 ${MAIN} ${CONFIG_FILE}
debug: install
	${VENV_NAME}/bin/python3 -m pdb ${MAIN} ${CONFIG_FILE}
lint: 
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
clean:
	rm -rf */__pycache__ .mypy_cache