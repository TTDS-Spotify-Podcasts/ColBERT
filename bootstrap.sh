#!/bin/sh
export FLASK_APP=./query_service/index.py
flask --debug run -h 0.0.0.0