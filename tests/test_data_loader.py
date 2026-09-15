import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "logindata.json"
with DATA_PATH.open() as f:
    test_data = json.load(f)
VALID_USER = test_data["data"][0]
PROBLEM_USER = test_data["data"][7]
