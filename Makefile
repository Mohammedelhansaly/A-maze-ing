PYTHON = python3
VENV_NAME = mazevenev
DEPENDECIES = requirements.txt
MAIN = amazing.py
install :
	${PYTHON} venv ${VENV_NAME}
	source ${VENV_NAME}/bin/activate
	${VENV_NAME}/bin/pip install -r ${DEPENDECIES}
run: install
	${VENV_NAME}/bin/python3 ${MAIN}