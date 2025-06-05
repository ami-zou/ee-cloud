#!/bin/bash

# Create a virtual environment named .venv
python3 -m venv .venv

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