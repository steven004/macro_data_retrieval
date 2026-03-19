#!/bin/bash

# Ensure we are in the script's directory (This is crucial for cron jobs executing from ~/)
cd "$(dirname "$0")"

# Setup the environment if missing
if [ ! -d "venv" ]; then
    echo "First time setup: Creating environment and installing dependencies..."
    
    # Check if python3 is available in typical cron PATHs, forcefully append if missing
    if ! command -v python3 &> /dev/null; then
        export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
    fi
    
    python3 -m venv venv
    # Use the explicit path to pip inside the venv
    ./venv/bin/pip install -r requirements.txt
fi

# Run the main program using the virtual environment's embedded python binary.
# Using the explicit ./venv/bin/python completely bypasses any cron PATH or 'source' environment issues!
./venv/bin/python main.py "$@"
