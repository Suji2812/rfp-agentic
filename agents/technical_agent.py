import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.spec_match import compute_spec_match
import pandas as pd
from utils.spec_match import compute_spec_match
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PRODUCTS_PATH = os.path.join(DATA_DIR, "products.csv")

def load_products():
    path = os.path.abspath(PRODUCTS_PATH)
    df = pd.read_csv(path)
    # Normalize column names to match RFP spec keys expectations
    df.columns = [c.strip() for c in df.columns]
    return df

def match_products(rfp_specs: dict, products_df=None, top_n=3):
    """
    Returns top_n product recommendations with spec match % and details.
    products_df: pass DataFrame (if None, load default)
    """
    if products_df is None:
        products_df = load_products()

    results = []
    for _, row in products_df.iterrows():
        product = row.to_dict()
        # convert numeric fields if possible:
        for k, v in product.items():
            # try to coerce numeric-looking strings to numbers for better matching
            try:
                if isinstance(v, str) and v.replace('.', '', 1).isdigit():
                    product[k] = float(v) if '.' in v else int(v)
            except Exception:
                pass
        score, details = compute_spec_match(rfp_specs, product)
        results.append({
            "sku": product.get("sku"),
            "name": product.get("name"),
            "score": score,
            "details": details,
            "product_row": product
        })

    # sort descending by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]

