PYTHON = python3
VENV_NAME = mazevenv
DEPENDECIES = requirement.txt
MAIN = a_maze_ing.py
CONFIG_FILE = config.txt
install:
	${PYTHON} -m venv ${VENV_NAME}
	${VENV_NAME}/bin/pip install -r ${DEPENDECIES}
run:
	${VENV_NAME}/bin/python3 ${MAIN} ${CONFIG_FILE}

clean:
	rm -rf __pycache__