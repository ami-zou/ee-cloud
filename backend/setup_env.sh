#!/bin/bash

# Desired Python version
PYTHON_VERSION=3.11

# Find the correct python executable
if command -v python$PYTHON_VERSION &>/dev/null; then
    PYTHON_BIN=python$PYTHON_VERSION
elif command -v python3 &>/dev/null && [[ "$($PYTHON_BIN --version 2>&1)" == *"$PYTHON_VERSION"* ]]; then
    PYTHON_BIN=python3
else
    echo "Python $PYTHON_VERSION is not installed. Please install it (e.g., 'brew install python@$PYTHON_VERSION' on macOS)."
    exit 1
fi

# Create virtual environment
$PYTHON_BIN -m venv .venv

# Create a virtual environment named .venv
# python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required dependencies
pip install -r requirements.txt

# deactivate

# echo "✅ Environment setup complete."
# echo "Run the development server with:"
# echo "source .venv/bin/activate && uvicorn main:app --reload"

cat <<EOF

✅ Environment setup complete.

➡ To activate the environment:
   source .venv/bin/activate

➡ To start the development server:
   uvicorn main:app --reload

- (Combined) Run the development server with:
   source .venv/bin/activate && uvicorn main:app --reload

EOF