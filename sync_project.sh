#!/bin/bash
# For use in Linux
# Determine the project directory based on the script's location
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define destination directory on the remote server
DESTINATION="lmaloney@sso.local:/home/lmaloney/SkySprinkler"

# Run rsync with .gitignore
rsync -avz --filter=':- .gitignore' "$PROJECT_DIR" "$DESTINATION"
