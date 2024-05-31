#!/bin/bash

# Define the source and destination directories
CONFIG_SRC_DIR="$(pwd)/.config/jupyter"
CONFIG_DEST_DIR="$HOME/.jupyter"

# Ensure the destination directory exists
mkdir -p "$CONFIG_DEST_DIR"

# Copy configuration files from the repository to the Jupyter config directory
cp -r "$CONFIG_SRC_DIR"/* "$CONFIG_DEST_DIR/"

# Display a message confirming the copy
echo "Jupyter configuration files have been copied to $CONFIG_DEST_DIR"

# Optionally, activate the virtual environment (if applicable)
if [ -d "venv" ]; then
  source venv/bin/activate
  echo "Virtual environment activated."
fi
