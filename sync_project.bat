:: For use in Windows
@echo off

:: Get the path of the current directory
SET PROJECT_DIR=%~dp0

:: Remove trailing backslash
SET PROJECT_DIR=%PROJECT_DIR:~0,-1%

:: Define destination directory on the remote server
SET DESTINATION=lmaloney@sso.local:/home/lmaloney/SkySprinkler

:: Run rsync with .gitignore (using Git Bash or similar)
"C:\Program Files\Git\bin\bash.exe" -c "rsync -avz --filter=':- .gitignore' '%PROJECT_DIR%' '%DESTINATION%'"
