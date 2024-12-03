#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install the required packages from requirements.txt
pip install -r requirements.txt
