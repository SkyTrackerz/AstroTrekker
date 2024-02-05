:: For use in Windows
@echo off

:: Get the current Windows directory and convert it to WSL path format
:: This replaces 'C:\' with '/mnt/c/' and changes backslashes to forward slashes
SET CUR_DIR=%CD:C:\=/mnt/c/%
SET CUR_DIR=%CUR_DIR:\=/%

:: Run the Linux script using WSL in the current directory
wsl cd "%CUR_DIR%" && bash ./sync_project.sh
