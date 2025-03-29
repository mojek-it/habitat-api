@echo off
echo Running Black code formatter for GitKraken users...

REM Check if Black is installed locally
pip show black > nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Black is not installed locally. Installing now...
  pip install black
  if %ERRORLEVEL% neq 0 (
    echo Failed to install Black. Please install it manually with: pip install black
    pause
    exit /b 1
  )
)

REM Run Black locally (not in Docker)
echo Running Black on your code...
black . --exclude=migrations

REM Check if Black made any changes
if %ERRORLEVEL% neq 0 (
  echo Black found issues that couldn't be automatically fixed. Please fix them and try again.
  pause
  exit /b 1
)

REM Add the reformatted files back to the staging area
for /f "tokens=*" %%a in ('git diff --name-only') do git add "%%a"

echo Code formatting complete!
echo You can now commit your changes in GitKraken.
pause