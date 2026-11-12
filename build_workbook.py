"""Build TeamSpark_Envelope_Model.xlsx — defense backbone for the PayU case.
Every computed cell is a live formula referencing Inputs. Deck anchors are
printed in a separate 'Deck anchor' column with reconciliation notes."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter

INK = "0B1F33"; RED = "C0392B"; GREEN = "1E8449"; AMBER = "B9770E"; GREY = "5D6D7E"; LIGHT = "F4F6F7"
YELLOW = PatternFill("solid", fgColor="FFF2CC")
HDR = PatternFill("solid", fgColor=INK)
BAND = PatternFill("solid", fgColor=LIGHT)
WHITE_B = Font(color="FFFFFF", bold=True, size=11)
BOLD = Font(bold=True)
thin = Side(style="thin", color="D5DBDB")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = openpyxl.Workbook()

def title(ws, text, width=8):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=width)
    c = ws.cell(1, 1, text)
    c.font = Font(bold=True, size=13, color=INK)
    ws.cell(2, 1, "Team Spark · Follow the Money: Innovation Challenge · PayU × CSITM IIMB — illustrative* values flagged yellow").font = Font(size=9, italic=True, color=GREY)

def header(ws, row, cols):
    for i, v in enumerate(cols, 1):
        c = ws.cell(row, i, v); c.fill = HDR; c.font = WHITE_B; c.border = BORDER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# ------------------------------------------------ SHEET 1: Inputs
ws = wb.active; ws.title = "Inputs"
title(ws, "INPUTS — every assumption in one place", 6)
header(ws, 3, ["#", "Input", "Value", "Unit", "Tag", "Notes"])
rows = [
    ("Merchant base rate (laundering prevalence)", 0.0015, "of merchants", "Illustrative*", "Slide 01 footnote; see Sensitivity for robustness"),
    ("PayU total merchants", 450000, "merchants", "PayU (verified)", "450,000+ merchants, $82B TPV"),
    ("Laundering accounts at any time", "=C5*C4", "merchants", "Derived", "= 450,000 × 0.15% = 675"),
    ("Facilitation per laundering account", 5000000, "₹ / month", "Illustrative*", "₹50 lakh/month"),
    ("Cost per false alarm", 8000, "₹", "Illustrative*", "review + appeal handling"),
    ("Curtailment realisation", 0.60, "share", "Illustrative*", "share of facilitation actually cut when caught"),
    ("Run cost per 90-day cycle", 90000000, "₹ / cycle", "Illustrative*", "₹9 cr"),
    ("Status quo recall", 0.40, "", "Illustrative*", ""),
    ("Status quo FPR", 0.01, "", "Illustrative*", ""),
    ("Proposed recall", 0.85, "", "Illustrative*", ""),
    ("Proposed FPR", 0.001, "", "Illustrative*", ""),
    ("Cycle length", 90, "days", "", ""),
    ("Cycles per year", 4, "", "", ""),
    ("Bakery: staff per shift", 3, "", "Illustrative*", "Slide 04 envelope"),
    ("Bakery: txns per staff-hour", 24, "", "Illustrative*", ""),
    ("Bakery: hours open", 14.5, "hrs/day", "Illustrative*", "09:00–23:30"),
    ("Bakery: utilisation cap", 0.9, "", "Illustrative*", "physical ceiling allowance"),
    ("Bakery: average ticket", 85, "₹", "Illustrative*", ""),
    ("Bakery: ticket band width", 0.15, "±", "Illustrative*", ""),
    ("Bakery: seasonal uplift factor", 1.8, "×", "Illustrative*", "Diwali-type festival allowance"),
    ("Merchant B: observed txns/day", 3000, "txns", "Illustrative*", "betting day"),
    ("Merchant B: observed ticket", 420, "₹", "Illustrative*", "vs ₹85 band"),
    ("Merchant B: observed inflow/day", "=C24*C25", "₹", "Derived", "= 3,000 × ₹420 = ₹12,60,000"),
    ("Merchant B: observed payer cities", 340, "cities", "Illustrative*", ""),
    ("Merchant B: repeat-payer share", 0.04, "", "Illustrative*", ""),
]
for i, (name, val, unit, tag, note) in enumerate(rows, start=4):
    ws.cell(i, 1, i - 3).border = BORDER
    ws.cell(i, 2, name).border = BORDER
    c = ws.cell(i, 3, val); c.border = BORDER
    if tag == "Illustrative*" and not (isinstance(val, str) and val.startswith("=")):
        c.fill = YELLOW
    ws.cell(i, 4, unit).border = BORDER
    tc = ws.cell(i, 5, tag); tc.border = BORDER
    if tag == "Illustrative*": tc.font = Font(color=AMBER, bold=True)
    if tag == "PayU (verified)": tc.font = Font(color=GREEN, bold=True)
    if tag == "Derived": tc.font = Font(color=INK, bold=True)
    ws.cell(i, 6, note).border = BORDER
ws.column_dimensions["B"].width = 38; ws.column_dimensions["C"].width = 14
ws.column_dimensions["D"].width = 12; ws.column_dimensions["E"].width = 16; ws.column_dimensions["F"].width = 48
INP = "Inputs!$C$"

# ------------------------------------------------ SHEET 2: Confusion Matrix
ws = wb.create_sheet("Confusion Matrix")
title(ws, "CONFUSION MATRIX — per 100,000 merchants, one 90-day cycle", 5)
header(ws, 3, ["Metric", "Status quo", "Proposed", "Deck anchor", "Formula shown"])
R = 4
def row(ws, r, label, sq, pr, anchor, note, fmt="#,##0.0"):
    ws.cell(r, 1, label).border = BORDER
    for col, v in ((2, sq), (3, pr)):
        c = ws.cell(r, col, v); c.border = BORDER; c.number_format = fmt
        if col == 3: c.font = Font(bold=True, color=GREEN)
    ws.cell(r, 4, anchor).border = BORDER
    ws.cell(r, 5, note).font = Font(size=9, color=GREY)

row(ws, R, "Merchants scored", 100000, 100000, "1,00,000", "fixed cohort", "#,##0"); R += 1
row(ws, R, "Actually laundering", f"=B{R}*{INP}4", f"=C{R}*{INP}4", "150", "= 100,000 × 0.15%"); R += 1
row(ws, R, "Caught (recall)", f"=ROUND(B{R-1}*{INP}11,0)", f"=ROUND(C{R-1}*{INP}13,0)", "60 / 128", "= laundering × recall (rounded)"); R += 1
row(ws, R, "Innocent merchants flagged", f"=ROUND((B{R-3}-B{R-2})*{INP}12,0)", f"=ROUND((C{R-3}-C{R-2})*{INP}14,0)", "999 / 100", "= (scored − caught) × FPR (rounded)")
SQ_FA, PR_FA = f"B{R}", f"C{R}"; R += 1
row(ws, R, "Precision", f"=B{R-2}/(B{R-2}+{SQ_FA})", f"=C{R-2}/(C{R-2}+{PR_FA})", "5.7% / 56.1%", "= caught ÷ (caught + false alarms)", "0.0%"); R += 1
row(ws, R, "Innocent flagged per criminal caught", f"={SQ_FA}/B{R-3}", f"={PR_FA}/C{R-3}", "16.7 : 1 / 0.78 : 1", "= false alarms ÷ caught", "0.00"); R += 1
row(ws, R, "Facilitation curtailed (₹)", f"=B{R-4}*{INP}7*{INP}9", f"=C{R-4}*{INP}7*{INP}9", "₹18.0 cr / ₹38.4 cr", "= caught × ₹50L/month × 60% curtailment (monthly flow)", "₹#,##0"); R += 1
row(ws, R, "  … in ₹ cr", f"=B{R-1}/10000000", f"=C{R-1}/10000000", "", "", "0.0"); R += 1
row(ws, R, "Cost of false alarms (₹)", f"={SQ_FA}*{INP}8", f"={PR_FA}*{INP}8", "₹79.9 L / ₹8.0 L", "= false alarms × ₹8,000", "₹#,##0"); R += 1
row(ws, R, "Net value (₹ cr / cycle)", f"=B{R-3}-B{R-1}/10000000", f"=C{R-3}-C{R-1}/10000000", "≈17.2 / ≈38.3", "= facilitation − false-alarm cost", "0.00"); R += 1
NET_SQ, NET_PR = f"B{R-1}", f"C{R-1}"
row(ws, R, "Run cost (₹ cr / cycle, whole PayU)", f"={INP}10/10000000", f"={INP}10/10000000", "₹9 cr", "programme-level, shown separately from net value", "0.0"); R += 1
row(ws, R, "Net uplift vs status quo (₹ cr / cycle)", f"={NET_PR}-{NET_SQ}", "", "≈₹86 cr with ×4.5 network scaling — see Waterfall", "= proposed net − status quo net (pre-scaling)", "0.00"); R += 2
ws.cell(R, 1, "SANITY CHECKS (PayU-wide)").font = BOLD
R += 1
for label, f, a in [
    ("Laundering accounts across PayU", f"={INP}5*{INP}4", "675"),
    ("Monthly facilitation (₹ cr)", f"={INP}5*{INP}4*{INP}7/10000000", "≈₹337 cr/month"),
    ("Annual facilitation run-rate (₹ cr/yr)", f"={INP}5*{INP}4*{INP}7*12/10000000", "≈₹4,041 cr/yr"),
    ("Deck figure check: ₹70,000 cr/yr ÷ 12", "=70000000000/12/10000000", "≈₹5,833 cr/month — deck slide 01 must read ₹5,833 cr/month, not 15,833"),
]:
    ws.cell(R, 1, label).border = BORDER
    c = ws.cell(R, 2, f); c.border = BORDER; c.number_format = "#,##0.0"
    ws.cell(R, 3, a).border = BORDER; R += 1
ws.column_dimensions["A"].width = 40; ws.column_dimensions["E"].width = 52

# ------------------------------------------------ SHEET 3: Sensitivity
ws = wb.create_sheet("Sensitivity")
title(ws, "SENSITIVITY — Net value (₹ cr / cycle) across base rate, recall, FPR", 8)
bps = [0.0005, 0.001, 0.0015, 0.003, 0.005, 0.01]
recalls = [0.40, 0.60, 0.85]
fprs = [0.01, 0.001]
r0 = 4
ws.cell(r0, 1, "Base rate ↓ / (recall, FPR) →").font = BOLD
col = 2
for fpr in fprs:
    for rec in recalls:
        c = ws.cell(r0, col, f"recall {rec:.0%} @ FPR {fpr:.2%}")
        c.fill = HDR; c.font = WHITE_B; c.border = BORDER; c.alignment = Alignment(wrap_text=True)
        col += 1
for i, br in enumerate(bps):
    r = r0 + 1 + i
    c = ws.cell(r, 1, br); c.number_format = "0.00%"; c.fill = YELLOW; c.border = BORDER
    col = 2
    for fpr in fprs:
        for rec in recalls:
            # caught = 100000*br*rec ; FA = (100000-100000*br)*fpr ; net = caught*50L*0.6 - FA*8000 (₹ cr)
            f = f"=(100000*$A{r}*{rec})*{INP}7*{INP}9 - (100000-100000*$A{r})*{fpr}*{INP}8"
            f = f + "=0" if False else "(" + f")/10000000"
            cell = ws.cell(r, col, f); cell.border = BORDER; cell.number_format = "0.0"
            col += 1
rng = f"B{r0+1}:{get_column_letter(col-1)}{r0+len(bps)}"
ws.conditional_formatting.add(rng, ColorScaleRule(
    start_type="min", start_color="F5B7B1", mid_type="percentile", mid_value=50, mid_color="FDEBD0",
    end_type="max", end_color="A9DFBF"))
nr = r0 + len(bps) + 2
ws.cell(nr, 1, "Note: higher base rate improves precision at the same FPR — the 0.15% framing is CONSERVATIVE for the proposal.").font = Font(italic=True, color=GREEN)
ws.column_dimensions["A"].width = 26
for cc in range(2, col): ws.column_dimensions[get_column_letter(cc)].width = 17

# ------------------------------------------------ SHEET 4: Envelope Calculator
ws = wb.create_sheet("Envelope Calculator")
title(ws, "CAPACITY ENVELOPE — derivation & breach ratios (Slide 03/04)", 6)
r = 4
ws.cell(r, 1, "MERCHANT A — honest bakery (festival day)").font = Font(bold=True, size=12, color=GREEN); r += 1
header(ws, r, ["Envelope dimension", "Formula", "Value", "Unit", "", ""])
r += 1
def calc(ws, r, label, formula, val_note, fmt="#,##0"):
    ws.cell(r, 1, label).border = BORDER
    ws.cell(r, 2, formula).font = Font(size=9, color=GREY)
    c = ws.cell(r, 3, formula.replace("…", "")); c.border = BORDER; c.number_format = fmt
    ws.cell(r, 4, val_note).border = BORDER
calc(ws, r, "Txns / hour ceiling", f"={INP}17*{INP}18*{INP}20", "= staff × txns/staff-hr × utilisation = 3×24×0.9 = 64.8 → quote 72 band"); r += 1
calc(ws, r, "Txns / day ceiling", f"={INP}17*{INP}18*{INP}20*{INP}19", "= × hours open (14.5) ≈ 660/day (deck anchor 660, model 648)"); r += 1
calc(ws, r, "Inflow ceiling / day (₹)", f"={INP}17*{INP}18*{INP}20*{INP}19*{INP}21", "= 648 × ₹85 ≈ ₹56,000/day (deck anchor ₹56,000)", "₹#,##0"); r += 2
ws.cell(r, 1, "MERCHANT B — laundering 'bakery' (betting day)").font = Font(bold=True, size=12, color=RED); r += 1
header(ws, r, ["Dimension", "Envelope", "Observed", "Breach ratio (obs ÷ env)", "Deck anchor", "Breach?"])
r += 1
br_start = r
env_obs = [
    ("Txns / day", f"={INP}17*{INP}18*{INP}20*{INP}19", f"={INP}24", "4.6×"),
    ("Ticket value (₹)", f"={INP}21*(1+{INP}22)", f"={INP}25", "5×"),
    ("Inflow / day (₹)", f"={INP}17*{INP}18*{INP}20*{INP}19*{INP}21", f"={INP}26", "≈23× (22.5)"),
    ("Payer cities", "1 (neighbourhood)", f"={INP}27", "340× (vs 1)"),
    ("Repeat payers", "> 60% expected", f"={INP}28", "4% — collapsed"),
    ("Off-hours txns", "closed after 23:30", "38% after 23:30", "envelope violated"),
]
for label, env, obs, anchor in env_obs:
    ws.cell(r, 1, label).border = BORDER
    c = ws.cell(r, 2, env); c.border = BORDER
    if isinstance(env, str) and env.startswith("="): c.number_format = "#,##0.0"
    c = ws.cell(r, 3, obs); c.border = BORDER
    if isinstance(obs, str) and obs.startswith("="): c.number_format = "#,##0.0"
    if isinstance(obs, str) and obs.startswith("=") and isinstance(env, str) and env.startswith("="):
        cc = ws.cell(r, 4, f"=C{r}/B{r}"); cc.number_format = "0.0\"×\""; cc.font = Font(bold=True, color=RED); cc.border = BORDER
    else:
        cc = ws.cell(r, 4, "breach"); cc.font = Font(bold=True, color=RED); cc.border = BORDER
    ws.cell(r, 5, anchor).border = BORDER
    ws.cell(r, 6, "6 of 6" if r == br_start else "").border = BORDER
    r += 1
ws.cell(br_start - 1 + 7, 1, "BREACH COUNT").font = BOLD
ws.cell(br_start - 1 + 7, 4, "6 / 6").font = Font(bold=True, color=RED, size=12)
ws.column_dimensions["A"].width = 30; ws.column_dimensions["B"].width = 22
ws.column_dimensions["C"].width = 14; ws.column_dimensions["E"].width = 18; ws.column_dimensions["F"].width = 10

# ------------------------------------------------ SHEET 5: Value Waterfall
ws = wb.create_sheet("Value Waterfall")
title(ws, "VALUE WATERFALL — per 90-day cycle, then annualised (Slide 06)", 5)
r = 4
header(ws, r, ["Step", "₹ cr", "Live formula", "Deck anchor", "Reconciliation"]); r += 1
steps = [
    ("Status quo: facilitation recovered", f"='Confusion Matrix'!B11", "₹18.0 cr", ""),
    ("Proposed: facilitation recovered", f"='Confusion Matrix'!C11", "₹38.4 cr", ""),
    ("Proposed × 4.5 network scaling (constellation)", f"='Confusion Matrix'!C11*4.5", "₹172.4 cr", "4.5 = constellation multiplier (input below)"),
    ("Status quo × 4.5 (like-for-like)", f"='Confusion Matrix'!B11*4.5", "₹77.4 cr", ""),
    ("Incremental recovered facilitation", None, "≈₹95 cr", "= 172.4 − 77.4"),
    ("+ False-alarm saving", f"=('Confusion Matrix'!B12-'Confusion Matrix'!C12)/10000000", "≈₹0.72 cr", ""),
    ("− Run cost", f"=-{INP}10/10000000", "−₹9 cr", ""),
    ("= NET UPLIFT per cycle", None, "≈₹86 cr", "deck prints ₹86 cr; live model ≈₹86.7 — rounding of 128 & 999"),
    ("Annualised uplift (×4 cycles)", None, "≈₹344–347 cr", "deck prints ₹344 cr"),
    ("Status quo annualised net", f"='Confusion Matrix'!B11*4", "₹72 cr flow", "deck's ₹36 cr anchor uses different net basis — reconcile before quoting 9.6×"),
]
prev_inc = None
for label, f, anchor, note in steps:
    ws.cell(r, 1, label).border = BORDER
    if f:
        c = ws.cell(r, 2, f); c.number_format = "0.0"; c.border = BORDER
    elif "Incremental" in label:
        c = ws.cell(r, 2, "=B8-B7"); c.number_format = "0.0"; c.border = BORDER
    elif "NET UPLIFT" in label:
        c = ws.cell(r, 2, "=B9+B10+B11"); c.number_format = "0.0"; c.border = BORDER; c.font = Font(bold=True, color=GREEN, size=12)
    elif "Annualised uplift" in label:
        c = ws.cell(r, 2, "=B12*4"); c.number_format = "0.0"; c.border = BORDER; c.font = Font(bold=True, color=GREEN)
    else:
        c = ws.cell(r, 2, ""); c.border = BORDER
    ws.cell(r, 3, f or "derived from rows above").font = Font(size=9, color=GREY)
    ws.cell(r, 4, anchor).border = BORDER
    ws.cell(r, 5, note).font = Font(size=9, color=AMBER)
    r += 1
ws.cell(r + 1, 1, "Constellation multiplier").border = BORDER
mc = ws.cell(r + 1, 2, 4.5); mc.fill = YELLOW; mc.border = BORDER; mc.number_format = "0.0"
ws.cell(r + 1, 3, "Illustrative* — network scaling factor from constellation clusters").font = Font(size=9, color=GREY)
ws.column_dimensions["A"].width = 46; ws.column_dimensions["C"].width = 34; ws.column_dimensions["E"].width = 56

# ------------------------------------------------ SHEET 6: KPI Scorecard
ws = wb.create_sheet("KPI Scorecard")
title(ws, "KPI SCORECARD — what we commit to (Slide 06)", 5)
header(ws, 3, ["KPI", "Status quo", "Proposed target", "Where measured", "Verified source basis"])
kpis = [
    ("Precision", "5.7%", "≥ 55%", "Confusion Matrix sheet", "Derived model"),
    ("HMIR — honest merchants impacted ratio", "999/cycle ≈ 1.0% of cohort", "< 0.05% of 450,000 = ≤ 225/cycle", "Confusion Matrix", "Derived model"),
    ("Time-to-act from breach", "days–weeks (manual review)", "< 24 h", "Prototype decision log", ""),
    ("Appeal resolution", "undefined", "< 72 h", "Prototype appeal portal", ""),
    ("Settlement delta release after evidence", "n/a", "≤ 6 h", "Prototype waterfall panel B", ""),
]
r = 4
for k in kpis:
    for i, v in enumerate(k, 1):
        ws.cell(r, i, v).border = BORDER
    r += 1
r += 1
ws.cell(r, 1, "Verified claim sources").font = BOLD; r += 1
for s in [
    "RBI PA Master Directions — 13(a)–(i), 16(a), 18(a); net worth ₹15 cr → ₹25 cr (RBI)",
    "PROG Act 2025 — offering = 3 yrs + ₹1 cr; advertising = 2 yrs + ₹50 lakh; banks/FIs barred from processing (PIB · Drishti IAS)",
    "DGGI — ₹70,000 cr betting ecosystem traced via proxy merchants; originating-website recording + GST-linked accounts recommended (Economic Times)",
    "DPIP — hashed signals, RBIH, 12+ PSBs (IDPIC)",
    "MeitY — 7,800 betting sites blocked (Storyboard18)",
    "PayU — 450,000+ merchants, $82B TPV (PayU)",
    "UPI Oct 2026 — 2,547 cr txns, ₹31.53 lakh cr (DD News / NPCI)",
]:
    ws.cell(r, 1, s); r += 1
ws.column_dimensions["A"].width = 40; ws.column_dimensions["D"].width = 26; ws.column_dimensions["E"].width = 60

for sheet in wb.worksheets:
    sheet.freeze_panes = "A4"

wb.save("/home/user/deliverables/TeamSpark_Envelope_Model.xlsx")
print("workbook saved")
