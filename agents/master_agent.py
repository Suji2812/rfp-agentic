from agents.sales_agent import get_rfp_by_id
from agents.technical_agent import match_products, load_products
from agents.pricing_agent import estimate_pricing, load_pricing_table
from agents.report_agent import generate_pdf_report

def run_rfp_pipeline(rfp_id, top_n=3):
    rfp = get_rfp_by_id(rfp_id)
    if not rfp:
        raise ValueError("RFP not found")

    products_df = load_products()
    raw_recs = match_products(rfp.get("specs", {}), products_df, top_n=top_n)

    pricing_df = load_pricing_table()
    enriched = []
    for rec in raw_recs:
        sku = rec.get("sku")
        pricing = estimate_pricing(sku, rfp.get("quantity", 1), rfp.get("tests_required", []), pricing_df)
        rec["pricing"] = pricing
        enriched.append(rec)

    # Generate PDF bytes
    pdf_bytes = generate_pdf_report(rfp, enriched)
    return {
        "rfp": rfp,
        "recommendations": enriched,
        "pdf": pdf_bytes
    }
