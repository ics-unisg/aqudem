# Test and coverage
export PYTHONPATH=.
coverage run --source=aqudem --branch -m pytest
coverage report --fail-under=90 -m
# Lint
pylint aqudem
pylint --disable=protected-access,missing-function-docstring tests
# Type check
mypy aqudem tests --strict
