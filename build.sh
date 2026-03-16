#!/bin/bash

# Remove old virtual environment
rm -rf .venv

# Recreate venv
python -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install specific numpy first, then pandas
pip install numpy==1.23.5
pip install pandas==1.3.5

# Install remaining requirements
pip install fastapi==0.110.0 uvicorn==0.29.0 gmn-python-api==0.0.13 beautifulsoup4 future
