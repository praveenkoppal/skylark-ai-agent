#!/bin/bash
set -e

# Install dependencies using uv pip
uv pip install -r requirements.txt

# Verify installation
python -m pip list | grep fastapi
