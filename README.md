# Envelope Engine — Team Spark

**Follow the Money: Innovation Challenge · PayU × CSITM, IIM Bangalore**

Physics-of-the-merchant prototype for "The Bakery That Takes Bets": capacity
envelopes derived from a merchant's declared profile, 6-dimension breach
scoring, network constellation, decision router (T0–T4), delta settlement
waterfall and a merchant appeal portal. **Rules only — no ML in the hot path.**

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Browser opens at `http://localhost:8501`.

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit app — all 7 screens |
| `merchants.py` | Merchant A/B data (deck-exact numbers) + envelope logic |
| `build_workbook.py` | Regenerates `TeamSpark_Envelope_Model.xlsx` (defense model) |
| `requirements.txt` | Pinned dependencies |
| `TeamSpark_Envelope_Model.xlsx` | 6-tab model workbook (binary — upload to repo separately, see below) |

## Screens

1. Merchant Onboarding — live envelope derivation (staff × txn/hr × hours)
2. Transaction Simulator — inject a Diwali spike vs a betting day
3. Physics Score — 6 envelope dimensions, breach flags, 0–100 gauge
4. Constellation — 7 merchants + 4 hubs, confidence 0.41 → 0.97
5. Decision Router — interactive 2×2 → T0–T4 with reason codes
6. Delta Settlement Waterfall — Panel A (98.6% held) vs Panel B (₹0 held)
7. Merchant Appeal Portal — evidence upload → ≤72 h SLA, HMIR counter

Team Spark · Yash Tholambia
