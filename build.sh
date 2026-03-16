#!/bin/bash

# Upgrade pip first
python3 -m pip install --upgrade pip

# Install dependencies from requirements.txt
python3 -m pip install --no-cache-dir -r requirements.txt
