# AquDeM Frontend
Interactive, visual evaluation of activity detection results.

## Usage
1. Install the required packages: `pip install -r requirements.txt`
2. Install aqudem:
```bash
cd ../package
pip install .
cd ../frontend
```
3. Run the frontend: `streamlit run aqudem_app.py`

## Development
For development, in addition to the steps in usage, also run `pip install -r requirements-dev.txt`.
To execute some of the code quality checks that are done in the pipeline locally, run `./code-check.sh`