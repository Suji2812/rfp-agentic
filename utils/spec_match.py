from difflib import SequenceMatcher
import numbers

def _text_similarity(a, b):
    if a is None or b is None:
        return 0.0
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()

def compute_spec_match(rfp_specs: dict, product_row: dict):
    """
    Returns a percent [0..100] match between rfp_specs and product attributes.
    Uses text similarity for strings, closeness for numbers.
    """
    if not rfp_specs:
        return 0.0

    scores = []
    details = {}
    for key, req_val in rfp_specs.items():
        prod_val = product_row.get(key)
        score = 0.0
        if prod_val is None:
            score = 0.0
        else:
            # numeric comparison
            if isinstance(req_val, numbers.Number) and isinstance(prod_val, numbers.Number):
                if req_val == 0 and prod_val == 0:
                    score = 1.0
                else:
                    # closeness normalized
                    denom = max(abs(req_val), abs(prod_val), 1)
                    closeness = 1 - (abs(req_val - prod_val) / denom)
                    score = max(0.0, closeness)
            else:
                # text similarity
                score = _text_similarity(req_val, prod_val)
        scores.append(score)
        details[key] = round(score, 3)

    average = sum(scores) / len(scores) if scores else 0.0
    return round(average * 100, 2), details
