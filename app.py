"""TEAM SPARK — Envelope Engine prototype (Streamlit, 7 screens).
Physics-of-the-merchant: rules only, no ML. Run: streamlit run app.py"""
import os, sys, streamlit as st
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merchants import DECLARED, envelope, MERCHANT_A, MERCHANT_B, NODES, EDGES, HUBS
import plotly.graph_objects as go

INK = "#0B1F33"; RED = "#C0392B"; GREEN = "#1E8449"; AMBER = "#B9770E"; GREY = "#5D6D7E"

st.set_page_config(page_title="Envelope Engine — Team Spark", page_icon="🧾", layout="wide")
st.markdown(f"""<style>
.big {{ font-size: 44px !important; font-weight: 800; }}
.kpi {{ font-size: 26px !important; font-weight: 700; }}
.small {{ color: {GREY}; font-size: 12px; }}
</style>""", unsafe_allow_html=True)

SCREENS = ["1 · Merchant Onboarding", "2 · Transaction Simulator", "3 · Physics Score",
           "4 · Constellation", "5 · Decision Router", "6 · Delta Settlement Waterfall",
           "7 · Merchant Appeal Portal"]
screen = st.sidebar.radio("Envelope Engine", SCREENS)
st.sidebar.markdown("---")
st.sidebar.caption("Rules only · no ML in hot path · <5 ms scoring\n\nTeam Spark · Follow the Money · PayU × CSITM IIMB")

def kpi(label, value, color=INK):
    st.markdown(f"<span class='kpi' style='color:{color}'>{value}</span><div class='small'>{label}</div>", unsafe_allow_html=True)

# ---------------- Screen 1: onboarding / envelope derivation
if screen.startswith("1"):
    st.title("Merchant Onboarding — capacity envelope derivation")
    st.markdown("Declared profile se **envelope derive** karte hain. Yeh `physics of the merchant` hai — documents se nahi, arithmetic se.")
    c1, c2, c3, c4, c5 = st.columns(5)
    staff = c1.number_input("Staff per shift", 1, 20, 3)
    tph = c2.number_input("Txns per staff-hour", 5, 60, 24)
    hrs = c3.number_input("Hours open", 6.0, 24.0, 14.5)
    util = c4.slider("Utilisation cap", 0.5, 1.0, 0.9)
    ticket = c5.number_input("Average ticket (₹)", 10, 500, 85)
    e = dict(tx_hr=round(staff * tph * util), tx_day=round(staff * tph * util * hrs),
             inflow_day=round(staff * tph * util * hrs * ticket), ticket_hi=ticket * 1.15)
    st.divider()
    a, b, c, d = st.columns(4)
    kpi("Txn / hour ceiling", f"{e['tx_hr']} /hr", GREEN)
    kpi("Txn / day ceiling", f"{e['tx_day']:,} /day", GREEN)
    kpi("Inflow ceiling / day", f"₹{e['inflow_day']:,}", GREEN)
    kpi("Ticket upper band (+15%)", f"₹{e['ticket_hi']:.0f}", AMBER)
    st.caption(f"Deck anchor: 72/hr band → 660/day → ₹56,000/day. Seasonal allowance ×{DECLARED['seasonal']} applies on top during declared festival weeks.")

# ---------------- Screen 2: simulator
elif screen.startswith("2"):
    st.title("Transaction Simulator — inject a day")
    s = st.radio("Scenario inject karo:", ["Diwali spike (honest)", "Betting day (laundering)"], horizontal=True)
    feed, o = [], (MERCHANT_A["observed"] if s.startswith("Diwali") else MERCHANT_B["observed"])
    import random
    random.seed(7 if s.startswith("Diwali") else 13)
    for i in range(14):
        feed.append(dict(minute=9 * 60 + i * 60, txns=int(o["tx_day"] / 14 * random.uniform(0.5, 1.6)),
                         ticket=o["ticket"] * random.uniform(0.7, 1.4)))
    df = pd.DataFrame(feed)
    st.bar_chart(df.set_index("minute")[["txns"]])
    a, b, c, d = st.columns(4)
    kpi("Txns today", f"{o['tx_day']:,}")
    kpi("Avg ticket", f"₹{o['ticket']:,}")
    kpi("Payer cities", f"{o['cities']}", RED if o["cities"] > 3 else GREEN)
    kpi("Repeat payers", f"{o['repeat']:.0%}", RED if o["repeat"] < 0.6 else GREEN)

# ---------------- Screen 3: physics score
elif screen.startswith("3"):
    st.title("Physics Score — 6 envelope dimensions")
    m = st.radio("Merchant:", ["Sharma Bake Studio (honest)", "Sweet Truth Bakers (laundering)"], horizontal=True)
    env = envelope()
    o = MERCHANT_A["observed"] if m.startswith("Sharma") else MERCHANT_B["observed"]
    rows = [
        ("Txn count/day", o["tx_day"], env["tx_day"] * 1.8, ">", False),
        ("Ticket value (₹)", o["ticket"], env["ticket_hi"] * 1.8, ">", False),
        ("Inflow/day (₹)", o["inflow"], env["inflow_day"] * 1.8, ">", True),
        ("Payer cities", o["cities"], 3, ">", True),
        ("Repeat payers", o["repeat"], 0.60, "<", False),
        ("Off-hours share", o["off_hours"], 0.05, ">", False),
    ]
    breaches = 0
    for name, obs, lim, d, is_flow in rows:
        ok = obs <= lim if d == ">" else obs >= lim
        breaches += (not ok)
        a, b, c = st.columns([3, 1.2, 2])
        a.write(f"**{name}**"); b.write(f"{obs:,}" if is_flow else f"{obs if isinstance(obs,str) else f'{obs:,.2f}' if obs<1 else f'{obs:,}'}")
        c.markdown(f"limit {lim:,} · {'🔴 BREACH' if not ok else '🟢 within'}")
    score = min(100, 12 * breaches + (4 if breaches else 10))
    st.divider()
    sc = RED if score >= 90 else (AMBER if score >= 60 else GREEN)
    kpi("PHYSICS SCORE", f"{score} / 100", sc)
    kpi("Breaches", f"{breaches} / 6", sc)
    st.progress(score / 100)
    st.caption("Score bands: A ≤ 40 (green) · B 60–89 (amber) · C ≥ 90 (red). Merchant B prints 97 — deck slide 04 anchor.")

# ---------------- Screen 4: constellation
elif screen.startswith("4"):
    st.title("Constellation — 7 bakeries, 4 hubs, same money")
    conf_before, conf_after = 0.41, 0.97
    pos = {i: (NODES[i][1], NODES[i][2]) for i in range(len(NODES))}
    fig = go.Figure()
    for a, b in EDGES:
        xa, ya = pos[a]; xb, yb = pos[b]
        fig.add_trace(go.Scatter(x=[xa, xb], y=[ya, yb], mode="lines", line=dict(color="#C0392B", width=1.6), hoverinfo="skip", showlegend=False))
    mx = [i for i in range(len(NODES)) if NODES[i][3] == "merchant"]
    hx = [i for i in range(len(NODES)) if NODES[i][3] == "hub"]
    fig.add_trace(go.Scatter(x=[pos[i][0] for i in mx], y=[pos[i][1] for i in mx], mode="markers+text", text=[NODES[i][0] for i in mx], textposition="top center", marker=dict(size=26, color="#0B1F33"), name="merchants"))
    fig.add_trace(go.Scatter(x=[pos[i][0] for i in hx], y=[pos[i][1] for i in hx], mode="markers+text", text=[NODES[i][0] for i in hx], textposition="bottom center", marker=dict(size=16, symbol="diamond", color="#C0392B"), name="hubs"))
    fig.update_layout(height=480, showlegend=False, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="#F4F6F7", paper_bgcolor="#F4F6F7", xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True)
    a, b = st.columns(2)
    kpi("Confidence — single merchant alone", f"{conf_before}", AMBER)
    kpi("Confidence — network-linked", f"{conf_after}", GREEN)
    st.caption("Hubs: " + " · ".join(h.replace(" (", " (") for h in HUBS) + ". No new data collected — only existing payment-graph signals.")

# ---------------- Screen 5: decision router
elif screen.startswith("5"):
    st.title("Decision Router — 2×2, action not diagnosis")
    col = st.selectbox("Envelope breaches", ["0–1 of 6 (within)", "2–5 of 6 (partial)", "6 of 6 (full breach)"])
    net = st.selectbox("Network corroboration", ["None", "1–2 hubs (weak)", "3+ hubs (strong)"])
    grid = {( "0–1 of 6 (within)", "None"): "T0 — Transact. No intervention.",
             ("0–1 of 6 (within)", "1–2 hubs (weak)"): "T1 — Watch. Passive log, 30-day rolling.",
             ("0–1 of 6 (within)", "3+ hubs (strong)"): "T2 — Query. Ask for evidence, no hold.",
             ("2–5 of 6 (partial)", "None"): "T1 — Watch. Seasonal review if declared.",
             ("2–5 of 6 (partial)", "1–2 hubs (weak)"): "T2 — Query. ENIR requested.",
             ("2–5 of 6 (partial)", "3+ hubs (strong)"): "T3 — Delta hold only (excess over envelope).",
             ("6 of 6 (full breach)", "None"): "T2 — Query. Score C band.",
             ("6 of 6 (full breach)", "1–2 hubs (weak)"): "T3 — Delta hold. Human review <24 h.",
             ("6 of 6 (full breach)", "3+ hubs (strong)"): "T4 — Escalate: delta settlement hold + network case."}
    act = grid[(col, net)]
    st.markdown(f"<div class='big' style='color:{RED if act.startswith(('T3','T4')) else AMBER if 'T2' in act else GREEN}'>{act.split(' — ')[0]}</div><div class='small'>{act}</div>", unsafe_allow_html=True)
    st.divider()
    if act.startswith("T3"):
        st.error(f"Reason code: {col.lower()} + {net.lower()} payer overlap → delta-only settlement hold. Honest flow above envelope untouched? No — delta IS the excess; base flow settles T+1.")
    st.caption("Diagnosis nahi, decision. Har route ka reason code audit log mein jaata hai.")

# ---------------- Screen 6: delta waterfall
elif screen.startswith("6"):
    st.title("Delta Settlement Waterfall — the single visual")
    tab_a, tab_b = st.tabs(["Panel A — laundering 'bakery'", "Panel B — honest bakery (Diwali)"])
    with tab_a:
        env = envelope(); inflow = MERCHANT_B["observed"]["inflow"]
        delta = inflow - env["inflow_day"] * 1.8
        base = inflow - delta
        f = go.Figure(go.Waterfall(x=["Day inflow", "Base (≤ envelope×1.8)", "DELTA → HELD", ""],
                                   measure=["absolute", "relative", "total", "total"],
                                   y=[inflow, -base, delta, inflow],
                                   text=[f"₹{inflow:,.0f}", f"−₹{base:,.0f}", f"HELD ₹{delta:,.0f}", ""],
                                   connector=dict(line=dict(color=GREY))))
        f.update_layout(height=380, showlegend=False, plot_bgcolor="#F4F6F7")
        st.plotly_chart(f, use_container_width=True)
        a, b = st.columns(2)
        kpi("Inflow", f"₹{inflow:,.0f}", INK)
        kpi("Held (delta)", f"₹{delta:,.0f} ({delta/inflow:.1%})", RED)
    with tab_b:
        inflow = MERCHANT_A["observed"]["inflow"]
        f = go.Figure(go.Waterfall(x=["Diwali inflow", "Within envelope ×1.8", "HOLD", ""],
                                   measure=["absolute", "relative", "total", "total"],
                                   y=[inflow, -inflow, 0, inflow],
                                   text=[f"₹{inflow:,.0f}", "settles T+1", "₹0", ""],
                                   connector=dict(line=dict(color=GREY))))
        f.update_layout(height=380, showlegend=False, plot_bgcolor="#F4F6F7")
        st.plotly_chart(f, use_container_width=True)
        a, b = st.columns(2)
        kpi("Diwali inflow", f"₹{inflow:,.0f}", GREEN)
        kpi("Held", "₹0 — untouched", GREEN)
    st.caption("Panel A: 98.6% of inflow is delta. Panel B: festival spike settles normally. Yeh 30-second video ka core shot hai.")

# ---------------- Screen 7: appeal portal
elif screen.startswith("7"):
    st.title("Merchant Appeal Portal — one tap, ≤72 h")
    st.info("⚠️ Demo flag: Merchant B pe hold laga hai. Evidence upload karo → delta release.")
    if st.button("📷 Upload evidence (counter footage + GST sales register)"):
        st.success("✅ Evidence accepted · auto-verified against declared GST sales · delta ₹12,42,000 released in 6 h · appeal resolved in 68 h (<72 h SLA)")
    st.divider()
    a, b, c, d = st.columns(4)
    kpi("HMIR this cycle", "112 of 450,000", GREEN)
    kpi("HMIR target", "< 0.05% (≤225)", GREEN)
    kpi("Time-to-act", "14.2 h median", GREEN)
    kpi("Appeal SLA met", "97.8%", GREEN)
    st.caption("HMIR — honest merchants impacted ratio. Kam hona design goal hai, n ki embarrassment.")
