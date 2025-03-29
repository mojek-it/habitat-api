@echo off
echo Installing Black pre-commit hook for Windows...

REM Make sure Git knows this is a batch file even without the .bat extension
echo @echo off > .git\hooks\pre-commit.tmp
type .git\hooks\pre-commit >> .git\hooks\pre-commit.tmp
move /y .git\hooks\pre-commit.tmp .git\hooks\pre-commit

REM Set the core.fileMode to false to avoid executable bit issues on Windows
git config core.fileMode false

echo Pre-commit hook installed successfully!
echo Now Black will automatically run before each commit.