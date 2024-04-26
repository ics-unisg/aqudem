# Test and coverage
export PYTHONPATH=.
pytest
# Lint
pylint aqudem_app.py
pylint --disable=missing-function-docstring tests
