#!/bin/bash
set -x

cd /project

python -m venv /tmp/venv
source /tmp/venv/bin/activate

touch requirements_dev.txt
pip install -r requirements_dev.txt -e .[dev]
pip freeze --exclude-editable > requirements_dev.txt

pipdeptree

# ensure non-zero length requirements.txt
echo "# runtime dependencies" >> requirements.txt

pytest tests
