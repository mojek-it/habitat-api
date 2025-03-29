#!/bin/bash

# Run Black on the codebase
echo "Running Black code formatter..."
docker compose exec web black . --exclude=migrations

echo "Code formatting complete!"