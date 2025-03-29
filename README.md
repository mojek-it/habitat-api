# Habitat API

## Code Formatting with Black

This project uses [Black](https://github.com/psf/black) for code formatting to maintain consistent code style across the codebase.

### Running Black Before Commit

Black will automatically run before each commit thanks to the Git pre-commit hook that has been set up. This ensures that all code is properly formatted before being committed.

#### Installing the Pre-commit Hook on Windows

To install the pre-commit hook on Windows, simply run:

```
.\install-pre-commit-hook.bat
```

This will set up the hook to run Black automatically before each commit.

#### Using with GitKraken or Other Git GUI Clients

If you're using GitKraken or another Git GUI client, the pre-commit hook might not work automatically, and Docker might not be accessible. In this case, use this special script for GitKraken:

```
.\format-for-gitkraken.bat
```

This batch file will:
1. Install Black locally if needed (not using Docker)
2. Run Black to format your code
3. Stage all the formatted files
4. Let you know when it's done so you can commit in GitKraken

Simply run this batch file before committing in GitKraken, and your code will be properly formatted.

### Running Black Manually

You can also run Black manually using one of the following methods:

1. Using Make:
   ```
   make black
   ```

2. Using the provided script:
   - On Windows:
     ```
     format_code.bat
     ```
   - On Linux/macOS:
     ```
     ./format_code.sh
     ```

3. Directly with Docker Compose:
   ```
   docker compose exec web black . --exclude=migrations
   ```

### Black Configuration

Black is configured in the `pyproject.toml` file with the following settings:
- Line length: 88 characters
- Target Python version: 3.10
- Excludes migrations directories

## Development Setup

### Prerequisites

- Docker
- Docker Compose

### Getting Started

1. Clone the repository
2. Run `docker compose up`
3. Access the API at http://localhost:8000