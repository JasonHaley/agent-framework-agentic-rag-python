 #!/bin/sh

azd env get-values > .env 

./scripts/load_python_env.sh

echo 'Running "load_index.py"'

additionalArgs=""
if [ $# -gt 0 ]; then
  additionalArgs="$@"
fi

./.venv/bin/python ./src/utils/index_loader.py './data/en-only-tickets.csv' $additionalArgs