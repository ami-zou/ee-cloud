#!/bin/bash

set -e  # Exit on any error
set -x  # Print commands as they run

# === Step 1: Install build dependencies for Python ===
sudo apt update
sudo apt install -y \
  make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git

# === Step 2: Install pyenv if not already installed ===
if [ ! -d "$HOME/.pyenv" ]; then
  curl https://pyenv.run | bash
fi

# === Step 3: Setup pyenv environment ===
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# === Step 4: Install Python 3.11 (change version if needed) ===
pyenv install -s 3.11.9
pyenv global 3.11.9

# === Step 5: Create virtual environment ===
python3 -m venv .venv
source .venv/bin/activate

# === Step 6: Upgrade pip and install requirements ===
pip install --upgrade pip
pip install -r requirements.txt

# === Step 7: Confirm success and instructions ===
cat <<EOF

✅ Vaquita environment is fully set up.

➡ To activate the environment:
   source .venv/bin/activate

➡ To run the development server:
   uvicorn main:app --reload

EOF