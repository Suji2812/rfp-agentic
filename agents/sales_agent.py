import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RFPS_PATH = os.path.join(DATA_DIR, "rfps.json")

def _load_rfps():
    path = os.path.abspath(RFPS_PATH)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_rfp_list():
    """Return list of RFPs (metadata)."""
    return _load_rfps()

def get_rfp_by_id(rfp_id):
    rfps = _load_rfps()
    for r in rfps:
        if r.get("id") == rfp_id:
            return r
    return None
