# AquDeM Frontend
Interactive, visual evaluation of activity detection results.

## Usage
1. Install the required packages: `pip install -r requirements.txt`
2. Run the frontend: `streamlit run aqudem_app.py`

## Development
For development, in addition to the steps in usage, also run `pip install -r requirements_dev.txt`.
To execute some of the code quality checks that are done in the pipeline locally, run `./code-check.sh`.
This check contains the unit tests and linting.

For development purposes you might want to install the current aqudem package locally. To do so, run:
```bash
cd ../package
pip install .
cd ../frontend
```
