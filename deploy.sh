#!/bin/bash

rm -rf dist
python setup.py bdist_wheel sdist --formats gztar && python -m twine upload dist/*
