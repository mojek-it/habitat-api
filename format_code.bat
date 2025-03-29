@echo off
echo Running Black code formatter...
docker compose exec web black . --exclude=migrations
echo Code formatting complete!