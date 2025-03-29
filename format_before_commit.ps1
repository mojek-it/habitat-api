# PowerShell script to format code with Black before committing
Write-Host "Running Black code formatter before commit..."

# Run the make black command
& make black

# Check if Black made any changes
if ($LASTEXITCODE -ne 0) {
  Write-Host "Black found issues that couldn't be automatically fixed. Please fix them and try again."
  exit 1
}

# Add the reformatted files back to the staging area
$changedFiles = & git diff --name-only --cached
foreach ($file in $changedFiles) {
  & git add $file
}

Write-Host "Code formatting complete!"