#!/bin/sh
export FLASK_APP=./query_service/retrieve.py
flask --debug run -h 0.0.0.0 -p 5000