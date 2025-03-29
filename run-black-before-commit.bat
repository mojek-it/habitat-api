@echo off
echo Running Black code formatter before commit...

REM Run Black using make
make black

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