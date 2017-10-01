 watchmedo shell-command -W --patterns="*.py" --recursive \
     --command='clear && pytest -s --cov . --cov-report term-missing tests/'
