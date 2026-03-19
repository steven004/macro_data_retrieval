#!/bin/bash

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Automatically setup the environment and dependencies if missing
if [ ! -d "venv" ]; then
    echo "First time setup: Creating environment and installing dependencies..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Pass any arguments provided (like --history-dir) directly to the python script
python3 main.py "$@"
