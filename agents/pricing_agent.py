import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PRICING_PATH = os.path.join(DATA_DIR, "pricing.csv")

def load_pricing_table():
    path = os.path.abspath(PRICING_PATH)
    return pd.read_csv(path)

def estimate_pricing(sku: str, quantity: int, tests_required: list, pricing_df=None):
    """
    Simple pricing estimate:
      material_cost = unit_price * quantity
      total_test_cost = test_cost (per product) -- in real life tests might be per batch
    """
    if pricing_df is None:
        pricing_df = load_pricing_table()

    row = pricing_df[pricing_df["sku"] == sku]
    if row.empty:
        return {"unit_price": None, "test_cost": 0, "material_cost": None, "total_cost": None}

    unit_price = float(row.iloc[0]["unit_price"])
    test_cost = float(row.iloc[0].get("test_cost", 0))
    material_cost = unit_price * max(int(quantity), 1)
    # naive: apply test cost once per SKU (demo purposes)
    total_cost = material_cost + test_cost
    return {
        "sku": sku,
        "unit_price": unit_price,
        "test_cost": test_cost,
        "material_cost": material_cost,
        "total_cost": total_cost
    }
