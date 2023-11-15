#!/bin/bash
python3 -m flake8 . --count --ignore=E221,E501,E227 --show-source --statistics
