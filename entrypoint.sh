#!/bin/sh
#gunicorn --chdir app main:app -w 2 --threads 2 -b 0.0.0.0:8000
gunicorn --chdir app --bind 0.0.0.0:5002 main:app