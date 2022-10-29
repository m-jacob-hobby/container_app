#!/bin/sh
export FLASK_APP=./load_manager/main.py
export FLASK_DEBUG=1
export FLASK_ENV=development
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0