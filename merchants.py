"""Merchant data for the Envelope Engine prototype — numbers mirror Team Spark's deck."""
import random

DECLARED = dict(staff=3, txn_per_staff_hr=24, hours_open=14.5, utilisation=0.9,
                ticket=85, band=0.15, seasonal=1.8)

def envelope(declared=DECLARED):
    tx_hr = declared["staff"] * declared["txn_per_staff_hr"] * declared["utilisation"]
    tx_day = tx_hr * declared["hours_open"]
    inflow_day = tx_day * declared["ticket"]
    return dict(tx_hr=round(tx_hr), tx_day=round(tx_day),
                inflow_day=round(inflow_day), ticket_hi=declared["ticket"] * (1 + declared["band"]))

MERCHANT_A = dict(
    name="Sharma Bake Studio", city="Indore", kind="Honest bakery — festival day (Diwali)",
    observed=dict(tx_day=1180, ticket=110, inflow=130000, cities=2, repeat=0.71,
                  off_hours=0.02, delta_out=0.05, night=0.02),
    score=22, route="T1 — Watch (seasonal uplift within allowance)",
    breaches=[],  # computed
)

MERCHANT_B = dict(
    name="Sweet Truth Bakers", city="6 registered cities", kind="Laundering 'bakery' — betting day",
    observed=dict(tx_day=3000, ticket=420, inflow=1260000, cities=340, repeat=0.04,
                  off_hours=0.38, delta_out=0.986, night=0.38),
    score=97, route="T4 — Escalate: delta settlement hold + network case",
    breaches=[],
)

HUBS = ["Agent UPI handle (12 evenings)", "Same-IFSC beneficiary a/c ×3",
        "Device/IP cluster", "Payer-overlap ring (61%)"]

NODES = [
    # (label, x, y, kind)
    ("Sweet Truth Bakers", 0.0, 0.0, "merchant"),
    ("Crumb & Co", -1.6, 0.9, "merchant"),
    ("Dough Diaries", -1.4, -1.1, "merchant"),
    ("Oven Story 2", 1.5, 1.2, "merchant"),
    ("Bake Junction", 1.8, -0.6, "merchant"),
    ("Flour Power", 0.2, 1.7, "merchant"),
    ("The Cake Line", -0.3, -1.8, "merchant"),
    (HUBS[0], 0.4, 0.6, "hub"),
    (HUBS[1], -0.9, -0.4, "hub"),
    (HUBS[2], 1.0, 0.3, "hub"),
    (HUBS[3], -0.5, 0.5, "hub"),
]
EDGES = [(0, 7), (1, 7), (2, 8), (0, 8), (3, 9), (4, 9), (5, 10), (6, 8),
         (1, 10), (3, 7), (4, 7), (0, 9)]

def txn_feed(m, scenario):
    """Deterministic-ish feed summary for the simulator screen."""
    env = envelope()
    if scenario == "Diwali spike (honest)":
        o = MERCHANT_A["observed"]
    else:
        o = MERCHANT_B["observed"]
    breaches = []
    checks = [
        ("Txn count/day", o["tx_day"], env["tx_day"] * (1.8 if scenario.startswith("Diwali") else 1.0)),
        ("Ticket value (₹)", o["ticket"], env["ticket_hi"] * (1.8 if scenario.startswith("Diwali") else 1.0)),
        ("Inflow/day (₹)", o["inflow"], env["inflow_day"] * 1.8),
        ("Payer cities", o["cities"], 3),
        ("Repeat payers", o["repeat"], 0.60),
        ("Off-hours share", o["off_hours"], 0.05),
    ]
    for name, obs, lim in checks:
        breached = obs > lim if name not in ("Repeat payers",) else obs < lim
        breaches.append((name, obs, lim, breached))
    n = sum(1 for b in breaches if b[3])
    score = min(100, 12 * n + (4 if n else 10))
    return env, o, breaches, n, score
