import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinCalc Suite",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Nunito:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3rem 4rem 3rem;
    max-width: 1280px;
}

/* ── Back button ── */
.stButton > button {
    background: rgba(255,255,255,0.07) !important;
    color: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 1.1rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.13) !important;
    color: #ffffff !important;
}

/* ── Home page hero ── */
.home-hero {
    text-align: center;
    padding: 3.5rem 2rem 2.5rem 2rem;
    margin-bottom: 2.5rem;
}
.home-badge {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    color: #90cdf4;
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.home-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 0.8rem;
}
.home-title span {
    background: linear-gradient(90deg, #63b3ed, #9f7aea, #f687b3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.home-sub {
    color: rgba(255,255,255,0.45);
    font-size: 1rem;
    font-weight: 400;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
    text-align: center;
}

/* ── Calculator cards (home) ── */
.calc-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 2rem;
}
.calc-card {
    border-radius: 22px;
    padding: 2rem 1.8rem;
    border: 1px solid rgba(255,255,255,0.08);
    cursor: pointer;
    transition: transform 0.2s, border-color 0.2s;
    position: relative;
    overflow: hidden;
    text-decoration: none;
}
.calc-card:hover { transform: translateY(-4px); border-color: rgba(255,255,255,0.2); }
.calc-card.blue   { background: linear-gradient(145deg, #1a2a5e, #1e3a7e); }
.calc-card.green  { background: linear-gradient(145deg, #1a3a2e, #1a5a42); }
.calc-card.amber  { background: linear-gradient(145deg, #3a2a0e, #5a420e); }
.calc-card.pink   { background: linear-gradient(145deg, #3a1a3a, #5a2a5a); }
.calc-card.teal   { background: linear-gradient(145deg, #0e2a3a, #0e3a5a); }
.calc-card.red    { background: linear-gradient(145deg, #3a1a1a, #5a2a2a); }
.calc-card::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -30px;
    width: 120px; height: 120px;
    border-radius: 50%;
    background: rgba(255,255,255,0.03);
}
.calc-icon { font-size: 2.2rem; margin-bottom: 1rem; display: block; }
.calc-name {
    font-size: 1.15rem; font-weight: 700; color: #ffffff;
    margin-bottom: 0.4rem;
}
.calc-desc { font-size: 0.82rem; color: rgba(255,255,255,0.45); line-height: 1.5; }
.calc-arrow {
    position: absolute; top: 1.5rem; right: 1.5rem;
    font-size: 1rem; color: rgba(255,255,255,0.25);
}
.coming-soon {
    position: absolute; top: 1rem; right: 1rem;
    background: rgba(255,200,100,0.15);
    color: #f6c90e;
    border: 1px solid rgba(246,201,14,0.3);
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Page hero (inner pages) ── */
.hero-wrap {
    background: linear-gradient(120deg, #1a1a4e 0%, #2d2d6e 50%, #1a3a5c 100%);
    border-radius: 24px;
    padding: 2.2rem 2.5rem 1.8rem 2.5rem;
    margin-bottom: 1.8rem;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}
.hero-wrap.bond {
    background: linear-gradient(120deg, #1a3a1e 0%, #1e5a2a 50%, #1a3a10 100%);
}
.hero-wrap::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 220px; height: 220px; border-radius: 50%;
    background: rgba(99,179,237,0.06);
}
.hero-tag {
    display: inline-block;
    background: rgba(99,179,237,0.15); color: #90cdf4;
    border: 1px solid rgba(99,179,237,0.3); border-radius: 20px;
    padding: 4px 14px; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.7rem;
}
.hero-tag.bond { background: rgba(104,211,145,0.15); color: #68d391; border-color: rgba(104,211,145,0.3); }
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem; font-weight: 800; color: #ffffff;
    line-height: 1.1; margin-bottom: 0.4rem;
}
.hero-title span { background: linear-gradient(90deg, #63b3ed, #9f7aea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-title span.green { background: linear-gradient(90deg, #68d391, #38a169); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-sub { color: rgba(255,255,255,0.45); font-size: 0.9rem; margin: 0; }

/* ── Input section ── */
.input-section {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.6rem;
}
.input-section-title {
    font-size: 0.7rem; font-weight: 700;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 1rem;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 0.78rem !important; font-weight: 600 !important;
    color: rgba(255,255,255,0.55) !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
    font-family: 'Nunito', sans-serif !important;
}
input[type="number"] {
    background: #ffffff !important;
    border: 1.5px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important; color: #1a1a2e !important;
    font-size: 1.1rem !important; font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
}
input[type="number"]:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.2) !important;
}
div[data-baseweb="input"] { background: #ffffff !important; border-radius: 12px !important; }
div[data-baseweb="input"] input { color: #1a1a2e !important; background: #ffffff !important; font-weight: 700 !important; }
[data-testid="stNumberInput"] input { color: #1a1a2e !important; background: #ffffff !important; }

/* ── KPI Cards ── */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px; margin-bottom: 1.6rem;
}
.cards-grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px; margin-bottom: 1.6rem;
}
.kpi-card {
    border-radius: 18px; padding: 1.3rem 1.4rem;
    position: relative; overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06); min-width: 0; word-break: break-word;
}
.kpi-card.blue   { background: linear-gradient(135deg, #1a3a6e 0%, #1e4d8c 100%); }
.kpi-card.green  { background: linear-gradient(135deg, #1a4a3a 0%, #1e6b52 100%); }
.kpi-card.red    { background: linear-gradient(135deg, #5a1a1a 0%, #7a2a2a 100%); }
.kpi-card.purple { background: linear-gradient(135deg, #2d1a5a 0%, #4a2d8c 100%); }
.kpi-card.amber  { background: linear-gradient(135deg, #3a2a0a 0%, #5a440e 100%); }
.kpi-card.teal   { background: linear-gradient(135deg, #0a2a3a 0%, #0e3a5a 100%); }
.kpi-card::after {
    content: ''; position: absolute; top: -20px; right: -20px;
    width: 80px; height: 80px; border-radius: 50%;
    background: rgba(255,255,255,0.03);
}
.kpi-icon  { font-size: 1.3rem; margin-bottom: 0.5rem; display: block; }
.kpi-label {
    font-size: 0.68rem; font-weight: 600; color: rgba(255,255,255,0.45);
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.kpi-value {
    font-size: 1.35rem; font-weight: 700; color: #ffffff;
    font-family: 'Nunito', sans-serif; line-height: 1.3; overflow-wrap: anywhere;
}
.kpi-card.blue   .kpi-value { color: #90cdf4; }
.kpi-card.green  .kpi-value { color: #68d391; }
.kpi-card.red    .kpi-value { color: #fc8181; }
.kpi-card.purple .kpi-value { color: #b794f4; }
.kpi-card.amber  .kpi-value { color: #f6ad55; }
.kpi-card.teal   .kpi-value { color: #76e4f7; }

/* ── Section / chart card ── */
.sec-title {
    font-size: 0.7rem; font-weight: 700;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase; letter-spacing: 0.12em; margin: 0 0 0.9rem 0;
}
.chart-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 1.3rem 1.5rem 0.5rem 1.5rem;
}
.table-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 1.3rem 1.5rem 1rem 1.5rem; margin-bottom: 1.4rem;
}
.tip-bar {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #63b3ed; border-radius: 0 10px 10px 0;
    padding: 0.8rem 1rem; margin-top: 1rem;
    font-size: 0.85rem; color: rgba(255,255,255,0.6);
}
.tip-bar.green { border-left-color: #68d391; }
.tip-bar b { color: #90cdf4; }
.tip-bar.green b { color: #68d391; }

/* Download button */
.stDownloadButton button {
    background: linear-gradient(90deg, #3182ce, #553c9a) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 0.5rem 1.4rem !important; font-size: 0.88rem !important;
}
.stDownloadButton button:hover { opacity: 0.85 !important; }

/* Footer */
.footer {
    text-align: center; color: rgba(255,255,255,0.2);
    font-size: 0.76rem; padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.07); margin-top: 1rem;
}

/* Mobile */
@media (max-width: 768px) {
    .calc-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 12px !important; }
    .cards-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 10px !important; }
    .cards-grid-3 { grid-template-columns: repeat(2, 1fr) !important; gap: 10px !important; }
    .block-container { padding: 1rem 0.8rem 3rem 0.8rem !important; }
    .hero-wrap { padding: 1.5rem 1.2rem 1.2rem 1.2rem !important; }
    .hero-title { font-size: 1.9rem !important; }
    .home-title { font-size: 2.4rem !important; }
    .input-section { padding: 1.1rem 0.9rem !important; }
    .kpi-value { font-size: 1rem !important; }
    .kpi-label { font-size: 0.6rem !important; white-space: normal !important; }
    .kpi-card { padding: 0.9rem 0.9rem !important; border-radius: 14px !important; }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fmt_inr(value: float) -> str:
    s = f"{abs(value):,.2f}"
    parts = s.split(".")
    integer = parts[0].replace(",", "")
    if len(integer) > 3:
        last3 = integer[-3:]
        rest = integer[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        integer = ",".join(groups) + "," + last3
    return f"₹{integer}.{parts[1]}"


def fmt_cell(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return "—"
    return f"{val:,.2f}"


CHART_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255,255,255,0.07)"
FONT_COLOR = "rgba(255,255,255,0.5)"
FONT_FAM   = "Nunito"


# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <style>
    .hcard {
        border-radius: 22px;
        padding: 1.8rem 1.8rem 1.4rem 1.8rem;
        border: 1px solid rgba(255,255,255,0.09);
        position: relative; overflow: hidden; margin-bottom: 10px;
    }
    .hcard.blue   { background: linear-gradient(145deg, #1a2a5e, #1e3a7e); }
    .hcard.green  { background: linear-gradient(145deg, #1a3a2e, #1a5a42); }
    .hcard.amber  { background: linear-gradient(145deg, #3a2a0e, #4a3a10); }
    .hcard.pink   { background: linear-gradient(145deg, #3a1a3a, #5a2a5a); }
    .hcard.teal   { background: linear-gradient(145deg, #0e2a3a, #0e3a5a); }
    .hcard.red    { background: linear-gradient(145deg, #3a1a1a, #5a2a2a); }
    .hcard::after {
        content: ""; position: absolute; bottom: -30px; right: -30px;
        width: 110px; height: 110px; border-radius: 50%;
        background: rgba(255,255,255,0.03);
    }
    .hcard-icon { font-size: 2rem; margin-bottom: 0.6rem; display: block; }
    .hcard-name { font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem; }
    .hcard-desc { font-size: 0.8rem; color: rgba(255,255,255,0.45); line-height: 1.55; margin-bottom: 0; }
    .hcard-cs {
        display: inline-block; margin-top: 0.8rem;
        background: rgba(255,200,100,0.15); color: #f6c90e;
        border: 1px solid rgba(246,201,14,0.3); border-radius: 12px;
        padding: 3px 12px; font-size: 0.65rem; font-weight: 700;
        letter-spacing: 0.08em; text-transform: uppercase;
    }
    /* Open button styling */
    .open-btn div[data-testid="stButton"] > button {
        background: rgba(255,255,255,0.13) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.28) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 0.38rem 1.1rem !important;
        width: auto !important;
        margin-top: 2px !important;
    }
    .open-btn div[data-testid="stButton"] > button:hover {
        background: rgba(255,255,255,0.24) !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="home-hero">
        <div class="home-badge">💹 Financial Tools</div>
        <div class="home-title">Your <span>Finance</span><br>Calculator Suite</div>
        <p class="home-sub">All your financial calculators in one place. Simple inputs, instant results, beautiful breakdowns.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""<div class="hcard blue">
          <span class="hcard-icon">💸</span>
          <div class="hcard-name">EMI Calculator</div>
          <div class="hcard-desc">Calculate monthly installments, total interest & full amortization schedule for any loan.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="open-btn">', unsafe_allow_html=True)
        if st.button("Open EMI Calculator →", key="btn_emi"):
            st.session_state.page = "emi"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="hcard green">
          <span class="hcard-icon">📈</span>
          <div class="hcard-name">Bond Valuation</div>
          <div class="hcard-desc">Find the fair value of a bond using face value, coupon rate, market rate & tenure.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="open-btn">', unsafe_allow_html=True)
        if st.button("Open Bond Valuation →", key="btn_bond"):
            st.session_state.page = "bond"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div class="hcard amber">
          <span class="hcard-icon">📊</span>
          <div class="hcard-name">SIP Calculator</div>
          <div class="hcard-desc">Estimate returns on your monthly SIP investments with compounding growth.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="open-btn">', unsafe_allow_html=True)
        if st.button("Open SIP Calculator →", key="btn_sip"):
            st.session_state.page = "sip"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin:0.6rem 0'></div>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3, gap="medium")
    with col4:
        st.markdown("""<div class="hcard pink">
          <span class="hcard-icon">🏦</span>
          <div class="hcard-name">FD Calculator</div>
          <div class="hcard-desc">Calculate maturity amount and interest earned on fixed deposits.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="open-btn">', unsafe_allow_html=True)
        if st.button("Open FD Calculator →", key="btn_fd"):
            st.session_state.page = "fd"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col5:
        st.markdown("""<div class="hcard teal">
          <span class="hcard-icon">📉</span>
          <div class="hcard-name">NPV / IRR</div>
          <div class="hcard-desc">Evaluate investment viability with Net Present Value and Internal Rate of Return.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="open-btn">', unsafe_allow_html=True)
        if st.button("Open NPV / IRR →", key="btn_npv"):
            st.session_state.page = "npv"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col6:
        st.markdown("""<div class="hcard red">
          <span class="hcard-icon">🧾</span>
          <div class="hcard-name">GST Calculator</div>
          <div class="hcard-desc">Quickly compute GST inclusive or exclusive amounts across all tax slabs.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="open-btn">', unsafe_allow_html=True)
        if st.button("Open GST Calculator →", key="btn_gst"):
            st.session_state.page = "gst"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer" style="margin-top:2rem;">
      <b>FinCalc Suite</b> &nbsp;·&nbsp; Results are indicative only. Consult your financial advisor for exact figures.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# EMI CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
def calculate_emi(principal, annual_rate, years):
    n = years * 12
    r = annual_rate / 12 / 100
    emi = principal / n if r == 0 else principal * r * (1 + r)**n / ((1 + r)**n - 1)
    return emi, n, r


def build_emi_schedule(principal, emi, r, n):
    rows = [{"Period": 0, "EMI": None, "Interest": None,
             "Principal Amount Paid": None, "Remaining Amount": principal}]
    balance = principal
    for i in range(1, n + 1):
        interest = balance * r
        princ_paid = emi - interest
        balance = max(0.0, balance - princ_paid)
        rows.append({"Period": i, "EMI": emi, "Interest": interest,
                     "Principal Amount Paid": princ_paid, "Remaining Amount": balance})
    return pd.DataFrame(rows)


def page_emi():
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-tag">🏦 Loan Planner</div>
      <div class="hero-title">Know Your <span>EMI</span></div>
      <p class="hero-sub">Enter loan details · Instant breakdown · Full amortization schedule · Downloadable report</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<p class="input-section-title">⚙️  Loan Parameters</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        principal = st.number_input("💰  Loan Amount (₹)", min_value=1,
                                     max_value=10_000_000_000, value=1_000_000, step=1000, format="%d")
    with col2:
        annual_rate = st.number_input("📈  Annual Interest Rate (%)", min_value=0.1,
                                       max_value=50.0, value=8.0, step=0.1, format="%.1f")
    with col3:
        years = st.number_input("📅  Loan Tenure (Years)", min_value=1,
                                 max_value=30, value=5, step=1, format="%d")
    st.markdown('</div>', unsafe_allow_html=True)

    emi, n, r = calculate_emi(principal, annual_rate, years)
    total_payable = emi * n
    total_interest = total_payable - principal
    interest_pct = total_interest / total_payable * 100
    df = build_emi_schedule(principal, emi, r, n)

    st.markdown(f"""
    <div class="cards-grid">
      <div class="kpi-card blue"><span class="kpi-icon">💸</span>
        <div class="kpi-label">Monthly EMI</div><div class="kpi-value">{fmt_inr(emi)}</div></div>
      <div class="kpi-card green"><span class="kpi-icon">🏦</span>
        <div class="kpi-label">Principal Amount</div><div class="kpi-value">{fmt_inr(principal)}</div></div>
      <div class="kpi-card red"><span class="kpi-icon">📊</span>
        <div class="kpi-label">Total Interest</div><div class="kpi-value">{fmt_inr(total_interest)}</div></div>
      <div class="kpi-card purple"><span class="kpi-icon">🧾</span>
        <div class="kpi-label">Total Payable</div><div class="kpi-value">{fmt_inr(total_payable)}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="tip-bar">
      💡 You pay <b>{interest_pct:.1f}%</b> as interest — that's <b>{fmt_inr(total_interest)}</b> over
      <b>{years} year{"s" if years > 1 else ""}</b>. Consider prepayments to reduce this significantly.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin:1.4rem 0'></div>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns([1, 1.7], gap="large")

    with chart_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">🥧  Principal vs Interest</p>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=["Principal", "Interest"],
            values=[round(principal, 2), round(total_interest, 2)],
            hole=0.65,
            marker=dict(colors=["#3182ce", "#e53e3e"],
                        line=dict(color="rgba(0,0,0,0.3)", width=3)),
            textinfo="label+percent",
            texttemplate="%{label}<br>%{percent:.2%}",
            textfont=dict(family=FONT_FAM, size=12, color="white"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent:.2%}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text=f"<b>{fmt_inr(total_payable)}</b><br>Total",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False,
            font=dict(size=12, family=FONT_FAM, color="white"), align="center",
        )
        fig_pie.update_layout(showlegend=True,
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05,
                        font=dict(family=FONT_FAM, size=12, color=FONT_COLOR)),
            margin=dict(t=5, b=10, l=10, r=10), height=295,
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">📉  Yearly Balance Reduction</p>', unsafe_allow_html=True)
        yearly = df[(df["Period"] % 12 == 0) & (df["Period"] > 0)].copy()
        yearly["Paid Off"] = principal - yearly["Remaining Amount"]
        yearly["Year"] = (yearly["Period"] / 12).astype(int)
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Outstanding", x=yearly["Year"],
            y=yearly["Remaining Amount"].round(2), marker_color="#3182ce", marker_line_width=0,
            hovertemplate="<b>Year %{x}</b><br>Outstanding: ₹%{y:,.2f}<extra></extra>"))
        fig_bar.add_trace(go.Bar(name="Paid Off", x=yearly["Year"],
            y=yearly["Paid Off"].round(2), marker_color="#68d391", marker_line_width=0,
            hovertemplate="<b>Year %{x}</b><br>Paid Off: ₹%{y:,.2f}<extra></extra>"))
        fig_bar.update_layout(barmode="stack",
            xaxis=dict(title="Year", tickmode="linear", dtick=1, showgrid=False,
                       tickfont=dict(family=FONT_FAM, size=11, color=FONT_COLOR),
                       title_font=dict(family=FONT_FAM, color=FONT_COLOR)),
            yaxis=dict(title="Amount (₹)", tickformat=",.0f",
                       tickfont=dict(family=FONT_FAM, size=11, color=FONT_COLOR),
                       title_font=dict(family=FONT_FAM, color=FONT_COLOR),
                       gridcolor=GRID_COLOR, gridwidth=0.5),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08,
                        font=dict(family=FONT_FAM, size=12, color=FONT_COLOR)),
            margin=dict(t=20, b=40, l=60, r=10), height=295,
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, bargap=0.2)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin:1.2rem 0'></div>", unsafe_allow_html=True)

    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📋  Amortization Schedule</p>', unsafe_allow_html=True)
    display_df = df.copy()
    for col in ["EMI", "Interest", "Principal Amount Paid", "Remaining Amount"]:
        display_df[col] = display_df[col].apply(fmt_cell)
    display_df["Period"] = display_df["Period"].astype(int)
    display_df = display_df.set_index("Period")
    st.dataframe(display_df, use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

    export_df = df.copy()
    for col in ["EMI", "Interest", "Principal Amount Paid"]:
        export_df[col] = export_df[col].apply(lambda x: round(x, 2) if x is not None else "")
    export_df["Remaining Amount"] = export_df["Remaining Amount"].apply(lambda x: round(x, 2))
    dl_col, _ = st.columns([1, 3])
    with dl_col:
        st.download_button("⬇  Download Schedule (CSV)", export_df.to_csv(index=False),
            file_name=f"EMI_{int(principal)}_{annual_rate}pct_{years}yr.csv", mime="text/csv")

    st.markdown("""
    <div class="footer">
      <b>Know Your EMI</b> &nbsp;·&nbsp; Results are indicative only. Consult your bank for exact figures.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# BOND VALUATION
# ══════════════════════════════════════════════════════════════════════════════
def calculate_bond(face_value, coupon_rate, years, payments_per_year, market_rate):
    coupon_payment = face_value * (coupon_rate / 100) / payments_per_year
    total_periods = years * payments_per_year
    period_rate = (market_rate / 100) / payments_per_year

    # PV of coupons + PV of face value
    if period_rate == 0:
        pv_coupons = coupon_payment * total_periods
    else:
        pv_coupons = coupon_payment * (1 - (1 + period_rate) ** -total_periods) / period_rate
    pv_face = face_value / (1 + period_rate) ** total_periods
    bond_value = pv_coupons + pv_face

    total_coupon_paid = coupon_payment * total_periods
    total_payment = total_coupon_paid + face_value

    schedule = []
    for i in range(1, total_periods + 1):
        payout = coupon_payment + (face_value if i == total_periods else 0)
        schedule.append({"Period": i, "Coupon Payment": coupon_payment,
                         "Principal": face_value if i == total_periods else 0,
                         "Total Payout": payout})
    return bond_value, coupon_payment, total_coupon_paid, total_payment, pd.DataFrame(schedule)


def page_bond():
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("""
    <div class="hero-wrap bond">
      <div class="hero-tag bond">📈 Fixed Income</div>
      <div class="hero-title">Bond <span class="green">Valuation</span></div>
      <p class="hero-sub">Enter bond details · Get fair value · View payout schedule · Analyze premium or discount</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<p class="input-section-title">⚙️  Bond Parameters</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        face_value = st.number_input("💵  Face Value (₹)", min_value=1,
                                      max_value=10_000_000_000, value=50_000, step=1000, format="%d")
    with col2:
        coupon_rate = st.number_input("🎟️  Coupon Rate (%)", min_value=0.01,
                                       max_value=50.0, value=9.1, step=0.01, format="%.2f")
    with col3:
        years = st.number_input("📅  Time Period (Years)", min_value=1,
                                 max_value=50, value=6, step=1, format="%d")

    col4, col5 = st.columns(2, gap="large")
    with col4:
        payments_per_year = st.number_input("🔁  Payments Per Year", min_value=1,
                                             max_value=12, value=2, step=1, format="%d")
    with col5:
        market_rate = st.number_input("📉  Market Interest Rate (%)", min_value=0.01,
                                       max_value=50.0, value=6.0, step=0.01, format="%.2f")
    st.markdown('</div>', unsafe_allow_html=True)

    bond_value, coupon_payment, total_coupon_paid, total_payment, schedule_df = \
        calculate_bond(face_value, coupon_rate, years, payments_per_year, market_rate)

    # Premium or discount
    diff = bond_value - face_value
    if diff > 0:
        status = f"Trading at a <b style='color:#68d391'>PREMIUM</b> of {fmt_inr(diff)}"
        tip_class = "tip-bar green"
    elif diff < 0:
        status = f"Trading at a <b style='color:#fc8181'>DISCOUNT</b> of {fmt_inr(abs(diff))}"
        tip_class = "tip-bar"
    else:
        status = "Trading at <b>PAR</b> — bond value equals face value"
        tip_class = "tip-bar"

    st.markdown(f"""
    <div class="cards-grid-3">
      <div class="kpi-card green"><span class="kpi-icon">💎</span>
        <div class="kpi-label">Bond Valuation</div><div class="kpi-value">{fmt_inr(bond_value)}</div></div>
      <div class="kpi-card blue"><span class="kpi-icon">🎟️</span>
        <div class="kpi-label">Per Period Coupon</div><div class="kpi-value">{fmt_inr(coupon_payment)}</div></div>
      <div class="kpi-card amber"><span class="kpi-icon">💰</span>
        <div class="kpi-label">Total Coupon Paid</div><div class="kpi-value">{fmt_inr(total_coupon_paid)}</div></div>
      <div class="kpi-card purple"><span class="kpi-icon">🧾</span>
        <div class="kpi-label">Total Payout (incl. FV)</div><div class="kpi-value">{fmt_inr(total_payment)}</div></div>
      <div class="kpi-card teal"><span class="kpi-icon">📅</span>
        <div class="kpi-label">Total Periods</div><div class="kpi-value">{years * payments_per_year}</div></div>
      <div class="kpi-card red"><span class="kpi-icon">📊</span>
        <div class="kpi-label">Face Value</div><div class="kpi-value">{fmt_inr(face_value)}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="{tip_class}">💡 {status} compared to face value of {fmt_inr(face_value)}.</div>',
                unsafe_allow_html=True)

    st.markdown("<div style='margin:1.4rem 0'></div>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns([1, 1.6], gap="large")

    with chart_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">🥧  Value Breakdown</p>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=["Face Value (Principal)", "Total Coupons"],
            values=[round(face_value, 2), round(total_coupon_paid, 2)],
            hole=0.65,
            marker=dict(colors=["#3182ce", "#38a169"],
                        line=dict(color="rgba(0,0,0,0.3)", width=3)),
            textinfo="label+percent",
            texttemplate="%{label}<br>%{percent:.2%}",
            textfont=dict(family=FONT_FAM, size=11, color="white"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent:.2%}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text=f"<b>{fmt_inr(total_payment)}</b><br>Total Out",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False,
            font=dict(size=11, family=FONT_FAM, color="white"), align="center",
        )
        fig_pie.update_layout(showlegend=True,
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05,
                        font=dict(family=FONT_FAM, size=11, color=FONT_COLOR)),
            margin=dict(t=5, b=10, l=10, r=10), height=295,
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">📊  Payout Per Period</p>', unsafe_allow_html=True)
        colors = ["#e53e3e" if row["Period"] == len(schedule_df) else "#38a169"
                  for _, row in schedule_df.iterrows()]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="Coupon", x=schedule_df["Period"],
            y=schedule_df["Coupon Payment"].round(2),
            marker_color="#38a169", marker_line_width=0,
            hovertemplate="Period %{x}<br>Coupon: ₹%{y:,.2f}<extra></extra>"))
        fig_bar.add_trace(go.Bar(
            name="Principal (last)", x=schedule_df["Period"],
            y=schedule_df["Principal"].round(2),
            marker_color="#3182ce", marker_line_width=0,
            hovertemplate="Period %{x}<br>Principal: ₹%{y:,.2f}<extra></extra>"))
        fig_bar.update_layout(barmode="stack",
            xaxis=dict(title="Period", tickmode="linear", dtick=1, showgrid=False,
                       tickfont=dict(family=FONT_FAM, size=11, color=FONT_COLOR),
                       title_font=dict(family=FONT_FAM, color=FONT_COLOR)),
            yaxis=dict(title="Amount (₹)", tickformat=",.0f",
                       tickfont=dict(family=FONT_FAM, size=11, color=FONT_COLOR),
                       title_font=dict(family=FONT_FAM, color=FONT_COLOR),
                       gridcolor=GRID_COLOR, gridwidth=0.5),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08,
                        font=dict(family=FONT_FAM, size=12, color=FONT_COLOR)),
            margin=dict(t=20, b=40, l=60, r=10), height=295,
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, bargap=0.25)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin:1.2rem 0'></div>", unsafe_allow_html=True)

    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📋  Payout Schedule</p>', unsafe_allow_html=True)
    disp = schedule_df.copy()
    for col in ["Coupon Payment", "Principal", "Total Payout"]:
        disp[col] = disp[col].apply(lambda x: f"{x:,.2f}")
    disp = disp.set_index("Period")
    st.dataframe(disp, use_container_width=True, height=380)
    st.markdown('</div>', unsafe_allow_html=True)

    dl_col, _ = st.columns([1, 3])
    with dl_col:
        export = schedule_df.copy()
        export["Coupon Payment"] = export["Coupon Payment"].round(2)
        export["Principal"] = export["Principal"].round(2)
        export["Total Payout"] = export["Total Payout"].round(2)
        st.download_button("⬇  Download Schedule (CSV)", export.to_csv(index=False),
            file_name=f"Bond_{int(face_value)}_{coupon_rate}pct_{years}yr.csv", mime="text/csv")

    st.markdown("""
    <div class="footer">
      <b>Bond Valuation</b> &nbsp;·&nbsp; Results are indicative only. Consult your financial advisor for exact figures.
    </div>""", unsafe_allow_html=True)




# ══════════════════════════════════════════════════════════════════════════════
# SIP CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
def page_sip():
    if st.button("← Back to Home", key="back_sip"):
        st.session_state.page = "home"; st.rerun()

    st.markdown("""
    <div class="hero-wrap" style="background:linear-gradient(120deg,#2d1a5e,#4a2d8c,#1a1a4e);">
      <div class="hero-tag" style="background:rgba(183,148,244,0.15);color:#b794f4;border-color:rgba(183,148,244,0.3);">📊 Wealth Builder</div>
      <div class="hero-title">SIP <span style="background:linear-gradient(90deg,#b794f4,#9f7aea);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Calculator</span></div>
      <p class="hero-sub">Systematic Investment Plan · Estimate your wealth growth with monthly investments</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<p class="input-section-title">⚙️  SIP Parameters</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        monthly = st.number_input("💰  Monthly Investment (₹)", min_value=100, max_value=10_000_000, value=10_000, step=500, format="%d")
    with col2:
        rate = st.number_input("📈  Expected Annual Return (%)", min_value=0.1, max_value=50.0, value=12.0, step=0.1, format="%.1f")
    with col3:
        years = st.number_input("📅  Investment Period (Years)", min_value=1, max_value=40, value=10, step=1, format="%d")
    st.markdown('</div>', unsafe_allow_html=True)

    n = years * 12
    r = rate / 12 / 100
    if r == 0:
        fv = monthly * n
    else:
        fv = monthly * ((((1 + r) ** n) - 1) / r) * (1 + r)
    total_invested = monthly * n
    total_returns  = fv - total_invested

    st.markdown(f"""
    <div class="cards-grid">
      <div class="kpi-card purple"><span class="kpi-icon">💎</span>
        <div class="kpi-label">Maturity Value</div><div class="kpi-value">{fmt_inr(fv)}</div></div>
      <div class="kpi-card blue"><span class="kpi-icon">💳</span>
        <div class="kpi-label">Total Invested</div><div class="kpi-value">{fmt_inr(total_invested)}</div></div>
      <div class="kpi-card green"><span class="kpi-icon">📈</span>
        <div class="kpi-label">Total Returns</div><div class="kpi-value">{fmt_inr(total_returns)}</div></div>
      <div class="kpi-card amber"><span class="kpi-icon">🔥</span>
        <div class="kpi-label">Return Multiplier</div><div class="kpi-value">{fv/total_invested:.2f}x</div></div>
    </div>""", unsafe_allow_html=True)

    gain_pct = total_returns / total_invested * 100
    st.markdown(f"""<div class="tip-bar" style="border-left-color:#b794f4;">
      💡 Your money grows by <b style="color:#b794f4">{gain_pct:.1f}%</b> — investing <b style="color:#b794f4">{fmt_inr(total_invested)}</b>
      gives you <b style="color:#b794f4">{fmt_inr(fv)}</b> in {years} year{"s" if years>1 else ""} thanks to compounding.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:1.4rem 0'></div>", unsafe_allow_html=True)

    # Build yearly schedule
    rows = []
    balance = 0
    cum_invested = 0
    for yr in range(1, years + 1):
        for m in range(12):
            balance = (balance + monthly) * (1 + r)
            cum_invested += monthly
        rows.append({"Year": yr, "Amount Invested (₹)": round(cum_invested, 2),
                     "Returns Earned (₹)": round(balance - cum_invested, 2),
                     "Total Value (₹)": round(balance, 2)})
    sip_df = pd.DataFrame(rows)

    chart_col1, chart_col2 = st.columns([1, 1.7], gap="large")
    with chart_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">🥧  Invested vs Returns</p>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=["Invested", "Returns"],
            values=[round(total_invested,2), round(total_returns,2)],
            hole=0.65,
            marker=dict(colors=["#553c9a","#b794f4"], line=dict(color="rgba(0,0,0,0.3)",width=3)),
            textinfo="label+percent", texttemplate="%{label}<br>%{percent:.2%}",
            textfont=dict(family=FONT_FAM, size=12, color="white"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent:.2%}<extra></extra>"))
        fig.add_annotation(text=f"<b>{fmt_inr(fv)}</b><br>Maturity",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False,
            font=dict(size=11, family=FONT_FAM, color="white"), align="center")
        fig.update_layout(showlegend=True,
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05, font=dict(family=FONT_FAM, size=12, color=FONT_COLOR)),
            margin=dict(t=5,b=10,l=10,r=10), height=295, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">📈  Wealth Growth Over Years</p>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Invested", x=sip_df["Year"], y=sip_df["Amount Invested (₹)"],
            marker_color="#553c9a", marker_line_width=0,
            hovertemplate="Year %{x}<br>Invested: ₹%{y:,.2f}<extra></extra>"))
        fig2.add_trace(go.Bar(name="Returns", x=sip_df["Year"], y=sip_df["Returns Earned (₹)"],
            marker_color="#b794f4", marker_line_width=0,
            hovertemplate="Year %{x}<br>Returns: ₹%{y:,.2f}<extra></extra>"))
        fig2.update_layout(barmode="stack",
            xaxis=dict(title="Year", tickmode="linear", dtick=1, showgrid=False,
                tickfont=dict(family=FONT_FAM,size=11,color=FONT_COLOR), title_font=dict(family=FONT_FAM,color=FONT_COLOR)),
            yaxis=dict(title="Amount (₹)", tickformat=",.0f",
                tickfont=dict(family=FONT_FAM,size=11,color=FONT_COLOR), title_font=dict(family=FONT_FAM,color=FONT_COLOR),
                gridcolor=GRID_COLOR, gridwidth=0.5),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08, font=dict(family=FONT_FAM,size=12,color=FONT_COLOR)),
            margin=dict(t=20,b=40,l=60,r=10), height=295,
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, bargap=0.2)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin:1.2rem 0'></div>", unsafe_allow_html=True)
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📋  Yearly Growth Schedule</p>', unsafe_allow_html=True)
    disp = sip_df.copy()
    for c in ["Amount Invested (₹)","Returns Earned (₹)","Total Value (₹)"]:
        disp[c] = disp[c].apply(lambda x: f"{x:,.2f}")
    disp = disp.set_index("Year")
    st.dataframe(disp, use_container_width=True, height=380)
    st.markdown('</div>', unsafe_allow_html=True)

    dl_col, _ = st.columns([1, 3])
    with dl_col:
        st.download_button("⬇  Download Schedule (CSV)", sip_df.to_csv(index=False),
            file_name=f"SIP_{monthly}pm_{rate}pct_{years}yr.csv", mime="text/csv")

    st.markdown('<div class="footer"><b>SIP Calculator</b> &nbsp;·&nbsp; Results are indicative only. Consult your financial advisor.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FD CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
def page_fd():
    if st.button("← Back to Home", key="back_fd"):
        st.session_state.page = "home"; st.rerun()

    st.markdown("""
    <div class="hero-wrap" style="background:linear-gradient(120deg,#1a3a5e,#0e4a6e,#0a2a4e);">
      <div class="hero-tag" style="background:rgba(118,228,247,0.15);color:#76e4f7;border-color:rgba(118,228,247,0.3);">🏦 Fixed Income</div>
      <div class="hero-title">FD <span style="background:linear-gradient(90deg,#76e4f7,#3182ce);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Calculator</span></div>
      <p class="hero-sub">Fixed Deposit · Compute maturity amount and total interest with compounding options</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<p class="input-section-title">⚙️  FD Parameters</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        principal = st.number_input("💰  Principal Amount (₹)", min_value=1000, max_value=10_000_000_000, value=100_000, step=1000, format="%d")
    with col2:
        rate = st.number_input("📈  Annual Interest Rate (%)", min_value=0.1, max_value=20.0, value=7.5, step=0.1, format="%.1f")
    with col3:
        years = st.number_input("📅  Tenure (Years)", min_value=0, max_value=30, value=3, step=1, format="%d")
    with col4:
        months_extra = st.number_input("📅  + Extra Months", min_value=0, max_value=11, value=0, step=1, format="%d")
    
    compound_opts = {"Monthly (12/yr)": 12, "Quarterly (4/yr)": 4, "Half-Yearly (2/yr)": 2, "Yearly (1/yr)": 1}
    compound_label = st.selectbox("🔁  Compounding Frequency", list(compound_opts.keys()), index=1)
    n_per_yr = compound_opts[compound_label]
    st.markdown('</div>', unsafe_allow_html=True)

    total_months = years * 12 + months_extra
    t = total_months / 12
    maturity = principal * (1 + (rate / 100) / n_per_yr) ** (n_per_yr * t)
    interest_earned = maturity - principal

    st.markdown(f"""
    <div class="cards-grid">
      <div class="kpi-card teal"><span class="kpi-icon">💎</span>
        <div class="kpi-label">Maturity Amount</div><div class="kpi-value">{fmt_inr(maturity)}</div></div>
      <div class="kpi-card blue"><span class="kpi-icon">🏦</span>
        <div class="kpi-label">Principal</div><div class="kpi-value">{fmt_inr(principal)}</div></div>
      <div class="kpi-card green"><span class="kpi-icon">📈</span>
        <div class="kpi-label">Interest Earned</div><div class="kpi-value">{fmt_inr(interest_earned)}</div></div>
      <div class="kpi-card amber"><span class="kpi-icon">⏳</span>
        <div class="kpi-label">Effective Yield</div><div class="kpi-value">{((maturity/principal)**(1/t)-1)*100:.2f}%</div></div>
    </div>""", unsafe_allow_html=True)

    gain_pct = interest_earned / principal * 100
    st.markdown(f"""<div class="tip-bar" style="border-left-color:#76e4f7;">
      💡 Your <b style="color:#76e4f7">{fmt_inr(principal)}</b> grows to <b style="color:#76e4f7">{fmt_inr(maturity)}</b>
      — earning <b style="color:#76e4f7">{gain_pct:.2f}%</b> total interest over {years} yr {months_extra} mo at {compound_label}.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:1.4rem 0'></div>", unsafe_allow_html=True)

    # Yearly schedule
    rows = []
    for yr in range(1, int(t) + 2):
        t_yr = min(yr, t)
        val = principal * (1 + (rate/100)/n_per_yr) ** (n_per_yr * t_yr)
        rows.append({"Year": yr if yr <= int(t) else f"{yr} (partial)",
                     "Principal (₹)": round(principal, 2),
                     "Interest Earned (₹)": round(val - principal, 2),
                     "Total Value (₹)": round(val, 2)})
        if t_yr == t: break
    fd_df = pd.DataFrame(rows)

    chart_col1, chart_col2 = st.columns([1, 1.7], gap="large")
    with chart_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">🥧  Principal vs Interest</p>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=["Principal","Interest Earned"],
            values=[round(principal,2), round(interest_earned,2)],
            hole=0.65,
            marker=dict(colors=["#0e3a5a","#76e4f7"], line=dict(color="rgba(0,0,0,0.3)",width=3)),
            textinfo="label+percent", texttemplate="%{label}<br>%{percent:.2%}",
            textfont=dict(family=FONT_FAM, size=12, color="white"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent:.2%}<extra></extra>"))
        fig.add_annotation(text=f"<b>{fmt_inr(maturity)}</b><br>Maturity",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False,
            font=dict(size=11, family=FONT_FAM, color="white"), align="center")
        fig.update_layout(showlegend=True,
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05, font=dict(family=FONT_FAM,size=12,color=FONT_COLOR)),
            margin=dict(t=5,b=10,l=10,r=10), height=295, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">📈  Growth Over Tenure</p>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Principal", x=fd_df["Year"].astype(str), y=fd_df["Principal (₹)"],
            marker_color="#0e3a5a", marker_line_width=0))
        fig2.add_trace(go.Bar(name="Interest", x=fd_df["Year"].astype(str), y=fd_df["Interest Earned (₹)"],
            marker_color="#76e4f7", marker_line_width=0))
        fig2.update_layout(barmode="stack",
            xaxis=dict(title="Year", showgrid=False,
                tickfont=dict(family=FONT_FAM,size=11,color=FONT_COLOR), title_font=dict(family=FONT_FAM,color=FONT_COLOR)),
            yaxis=dict(title="Amount (₹)", tickformat=",.0f",
                tickfont=dict(family=FONT_FAM,size=11,color=FONT_COLOR), title_font=dict(family=FONT_FAM,color=FONT_COLOR),
                gridcolor=GRID_COLOR, gridwidth=0.5),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08, font=dict(family=FONT_FAM,size=12,color=FONT_COLOR)),
            margin=dict(t=20,b=40,l=60,r=10), height=295,
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, bargap=0.25)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin:1.2rem 0'></div>", unsafe_allow_html=True)
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📋  Year-wise Breakup</p>', unsafe_allow_html=True)
    disp = fd_df.copy()
    for c in ["Principal (₹)","Interest Earned (₹)","Total Value (₹)"]:
        disp[c] = disp[c].apply(lambda x: f"{x:,.2f}")
    st.dataframe(disp.set_index("Year"), use_container_width=True, height=360)
    st.markdown('</div>', unsafe_allow_html=True)

    dl_col, _ = st.columns([1,3])
    with dl_col:
        st.download_button("⬇  Download Schedule (CSV)", fd_df.to_csv(index=False),
            file_name=f"FD_{int(principal)}_{rate}pct_{years}yr.csv", mime="text/csv")

    st.markdown('<div class="footer"><b>FD Calculator</b> &nbsp;·&nbsp; Results are indicative only. Consult your bank for exact figures.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# NPV / IRR CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
def page_npv():
    if st.button("← Back to Home", key="back_npv"):
        st.session_state.page = "home"; st.rerun()

    st.markdown("""
    <div class="hero-wrap" style="background:linear-gradient(120deg,#1a3a2a,#1e5a3a,#0a2a1a);">
      <div class="hero-tag" style="background:rgba(104,211,145,0.15);color:#68d391;border-color:rgba(104,211,145,0.3);">📉 Investment Analysis</div>
      <div class="hero-title">NPV / <span style="background:linear-gradient(90deg,#68d391,#38a169);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">IRR</span></div>
      <p class="hero-sub">Net Present Value & Internal Rate of Return · Evaluate investment profitability</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<p class="input-section-title">⚙️  Investment Parameters</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        initial = st.number_input("💰  Initial Investment (₹) — enter as positive", min_value=0, max_value=10_000_000_000, value=500_000, step=10_000, format="%d")
        discount = st.number_input("📉  Discount Rate / Required Return (%)", min_value=0.1, max_value=100.0, value=10.0, step=0.1, format="%.1f")
    with col2:
        n_periods = st.number_input("📅  Number of Periods (Years)", min_value=1, max_value=30, value=5, step=1, format="%d")
        st.markdown('<p style="font-size:0.75rem;color:rgba(255,255,255,0.4);margin-top:0.3rem;">Enter expected cash inflow for each year below</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Cash flow inputs
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<p class="input-section-title">💵  Expected Cash Inflows (₹) Per Year</p>', unsafe_allow_html=True)
    cash_flows = []
    cols_per_row = 5
    for row_start in range(0, int(n_periods), cols_per_row):
        row_cols = st.columns(min(cols_per_row, int(n_periods) - row_start), gap="medium")
        for i, c in enumerate(row_cols):
            yr = row_start + i + 1
            val = c.number_input(f"Year {yr} (₹)", min_value=0, max_value=10_000_000_000,
                                  value=150_000, step=10_000, format="%d", key=f"cf_{yr}")
            cash_flows.append(float(val))
    st.markdown('</div>', unsafe_allow_html=True)

    # NPV calculation
    r = discount / 100
    npv = -initial + sum(cf / (1 + r) ** (i + 1) for i, cf in enumerate(cash_flows))

    # IRR via bisection
    def calc_npv_at_rate(rate, initial, flows):
        return -initial + sum(cf / (1 + rate) ** (i+1) for i, cf in enumerate(flows))

    irr = None
    try:
        lo, hi = -0.9999, 10.0
        for _ in range(1000):
            mid = (lo + hi) / 2
            if abs(hi - lo) < 1e-8: break
            if calc_npv_at_rate(mid, initial, cash_flows) > 0:
                lo = mid
            else:
                hi = mid
        irr_val = (lo + hi) / 2
        if -0.9999 < irr_val < 10.0:
            irr = irr_val * 100
    except:
        irr = None

    total_inflow = sum(cash_flows)
    roi = (total_inflow - initial) / initial * 100 if initial > 0 else 0

    npv_color = "#68d391" if npv >= 0 else "#fc8181"
    npv_card  = "green"   if npv >= 0 else "red"
    decision  = "✅ ACCEPT — Investment adds value" if npv >= 0 else "❌ REJECT — Investment destroys value"
    irr_str   = f"{irr:.2f}%" if irr is not None else "N/A"

    st.markdown(f"""
    <div class="cards-grid">
      <div class="kpi-card {npv_card}"><span class="kpi-icon">{"📈" if npv>=0 else "📉"}</span>
        <div class="kpi-label">Net Present Value</div><div class="kpi-value" style="color:{npv_color}">{fmt_inr(npv)}</div></div>
      <div class="kpi-card teal"><span class="kpi-icon">🎯</span>
        <div class="kpi-label">IRR</div><div class="kpi-value">{irr_str}</div></div>
      <div class="kpi-card blue"><span class="kpi-icon">💵</span>
        <div class="kpi-label">Total Inflow</div><div class="kpi-value">{fmt_inr(total_inflow)}</div></div>
      <div class="kpi-card amber"><span class="kpi-icon">📊</span>
        <div class="kpi-label">Simple ROI</div><div class="kpi-value">{roi:.2f}%</div></div>
    </div>""", unsafe_allow_html=True)

    tip_color = "#68d391" if npv >= 0 else "#fc8181"
    irr_msg = f" IRR of <b style='color:{tip_color}'>{irr_str}</b> {'exceeds' if irr is not None and irr > discount else 'is below'} your required return of <b style='color:{tip_color}'>{discount}%</b>." if irr else ""
    st.markdown(f"""<div class="tip-bar" style="border-left-color:{tip_color};">
      💡 <b style="color:{tip_color}">{decision}</b>.{irr_msg}
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:1.4rem 0'></div>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns([1, 1.7], gap="large")
    with chart_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">🥧  Investment vs Returns</p>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=["Initial Investment", "Total Cash Inflows"],
            values=[round(initial,2), round(total_inflow,2)],
            hole=0.65,
            marker=dict(colors=["#1a3a2a","#68d391"], line=dict(color="rgba(0,0,0,0.3)",width=3)),
            textinfo="label+percent", texttemplate="%{label}<br>%{percent:.2%}",
            textfont=dict(family=FONT_FAM, size=11, color="white"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent:.2%}<extra></extra>"))
        fig.add_annotation(text=f"<b>ROI<br>{roi:.1f}%</b>",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False,
            font=dict(size=13, family=FONT_FAM, color="white"), align="center")
        fig.update_layout(showlegend=True,
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05, font=dict(family=FONT_FAM,size=11,color=FONT_COLOR)),
            margin=dict(t=5,b=10,l=10,r=10), height=295, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">📊  Cash Flow & Cumulative NPV</p>', unsafe_allow_html=True)
        years_list = list(range(1, int(n_periods)+1))
        cum_npv = []
        running = -initial
        for i, cf in enumerate(cash_flows):
            running += cf / (1 + r) ** (i+1)
            cum_npv.append(round(running, 2))
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Cash Inflow", x=years_list, y=[round(c,2) for c in cash_flows],
            marker_color="#68d391", marker_line_width=0,
            hovertemplate="Year %{x}<br>Inflow: ₹%{y:,.2f}<extra></extra>"))
        fig2.add_trace(go.Scatter(name="Cumulative NPV", x=years_list, y=cum_npv,
            mode="lines+markers", line=dict(color="#f6ad55", width=2.5),
            marker=dict(size=7, color="#f6ad55"),
            hovertemplate="Year %{x}<br>Cum NPV: ₹%{y:,.2f}<extra></extra>"))
        fig2.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)", line_width=1)
        fig2.update_layout(
            xaxis=dict(title="Year", tickmode="linear", dtick=1, showgrid=False,
                tickfont=dict(family=FONT_FAM,size=11,color=FONT_COLOR), title_font=dict(family=FONT_FAM,color=FONT_COLOR)),
            yaxis=dict(title="Amount (₹)", tickformat=",.0f",
                tickfont=dict(family=FONT_FAM,size=11,color=FONT_COLOR), title_font=dict(family=FONT_FAM,color=FONT_COLOR),
                gridcolor=GRID_COLOR, gridwidth=0.5),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08, font=dict(family=FONT_FAM,size=12,color=FONT_COLOR)),
            margin=dict(t=20,b=40,l=60,r=10), height=295,
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin:1.2rem 0'></div>", unsafe_allow_html=True)
    npv_table = []
    running2 = -initial
    for i, cf in enumerate(cash_flows):
        pv = cf / (1+r)**(i+1)
        running2 += pv
        npv_table.append({"Year": i+1, "Cash Inflow (₹)": round(cf,2),
            "Present Value (₹)": round(pv,2), "Cumulative NPV (₹)": round(running2,2)})
    npv_df = pd.DataFrame(npv_table)

    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📋  Discounted Cash Flow Table</p>', unsafe_allow_html=True)
    disp = npv_df.copy()
    for c in ["Cash Inflow (₹)","Present Value (₹)","Cumulative NPV (₹)"]:
        disp[c] = disp[c].apply(lambda x: f"{x:,.2f}")
    st.dataframe(disp.set_index("Year"), use_container_width=True, height=360)
    st.markdown('</div>', unsafe_allow_html=True)

    dl_col, _ = st.columns([1,3])
    with dl_col:
        st.download_button("⬇  Download Analysis (CSV)", npv_df.to_csv(index=False),
            file_name=f"NPV_IRR_{int(initial)}invested.csv", mime="text/csv")

    st.markdown('<div class="footer"><b>NPV / IRR Calculator</b> &nbsp;·&nbsp; Results are indicative only. Consult your financial advisor.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GST CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
def page_gst():
    if st.button("← Back to Home", key="back_gst"):
        st.session_state.page = "home"; st.rerun()

    st.markdown("""
    <div class="hero-wrap" style="background:linear-gradient(120deg,#5a1a1a,#7a2a2a,#4a1010);">
      <div class="hero-tag" style="background:rgba(252,129,129,0.15);color:#fc8181;border-color:rgba(252,129,129,0.3);">🧾 Tax Tool</div>
      <div class="hero-title">GST <span style="background:linear-gradient(90deg,#fc8181,#e53e3e);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Calculator</span></div>
      <p class="hero-sub">Goods & Services Tax · Compute GST inclusive or exclusive across all Indian tax slabs</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<p class="input-section-title">⚙️  GST Parameters</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        amount = st.number_input("💰  Amount (₹)", min_value=1, max_value=10_000_000_000, value=10_000, step=100, format="%d")
    with col2:
        gst_rate = st.selectbox("📊  GST Rate", ["3%","5%","12%","18%","28%"], index=3)
        gst_pct  = float(gst_rate.replace("%",""))
    with col3:
        calc_type = st.selectbox("🔁  Calculation Type", ["Exclusive (Add GST to amount)", "Inclusive (Extract GST from amount)"])
    st.markdown('</div>', unsafe_allow_html=True)

    if "Exclusive" in calc_type:
        base_amount  = amount
        gst_amount   = base_amount * gst_pct / 100
        total_amount = base_amount + gst_amount
    else:
        total_amount = amount
        base_amount  = total_amount / (1 + gst_pct / 100)
        gst_amount   = total_amount - base_amount

    cgst = gst_amount / 2
    sgst = gst_amount / 2

    st.markdown(f"""
    <div class="cards-grid">
      <div class="kpi-card blue"><span class="kpi-icon">💰</span>
        <div class="kpi-label">{"Original" if "Exclusive" in calc_type else "Pre-GST"} Amount</div>
        <div class="kpi-value">{fmt_inr(base_amount)}</div></div>
      <div class="kpi-card red"><span class="kpi-icon">🧾</span>
        <div class="kpi-label">GST Amount ({gst_rate})</div>
        <div class="kpi-value">{fmt_inr(gst_amount)}</div></div>
      <div class="kpi-card green"><span class="kpi-icon">✅</span>
        <div class="kpi-label">{"Total with GST" if "Exclusive" in calc_type else "Total (GST incl.)"}</div>
        <div class="kpi-value">{fmt_inr(total_amount)}</div></div>
      <div class="kpi-card purple"><span class="kpi-icon">⚖️</span>
        <div class="kpi-label">CGST / SGST Each</div>
        <div class="kpi-value">{fmt_inr(cgst)}</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="tip-bar" style="border-left-color:#fc8181;">
      💡 GST Breakup — CGST: <b style="color:#fc8181">{fmt_inr(cgst)}</b> ({gst_pct/2:.1f}%)
      + SGST: <b style="color:#fc8181">{fmt_inr(sgst)}</b> ({gst_pct/2:.1f}%)
      = Total GST: <b style="color:#fc8181">{fmt_inr(gst_amount)}</b>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:1.4rem 0'></div>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns([1, 1.7], gap="large")
    with chart_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">🥧  Amount Breakup</p>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=["Base Amount","CGST","SGST"],
            values=[round(base_amount,2), round(cgst,2), round(sgst,2)],
            hole=0.65,
            marker=dict(colors=["#3182ce","#e53e3e","#fc8181"], line=dict(color="rgba(0,0,0,0.3)",width=3)),
            textinfo="label+percent", texttemplate="%{label}<br>%{percent:.2%}",
            textfont=dict(family=FONT_FAM, size=12, color="white"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent:.2%}<extra></extra>"))
        fig.add_annotation(text=f"<b>{gst_rate}<br>GST</b>",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False,
            font=dict(size=15, family=FONT_FAM, color="white"), align="center")
        fig.update_layout(showlegend=True,
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05, font=dict(family=FONT_FAM,size=12,color=FONT_COLOR)),
            margin=dict(t=5,b=10,l=10,r=10), height=295, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">📊  GST Across All Slabs (on same base)</p>', unsafe_allow_html=True)
        slabs = [3, 5, 12, 18, 28]
        gst_vals = [round(base_amount * s/100, 2) for s in slabs]
        total_vals = [round(base_amount + g, 2) for g in gst_vals]
        bar_colors = ["#68d391" if s == gst_pct else "#3182ce" for s in slabs]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Base Amount", x=[f"{s}%" for s in slabs],
            y=[round(base_amount,2)]*5, marker_color="#1a3a6e", marker_line_width=0))
        fig2.add_trace(go.Bar(name="GST", x=[f"{s}%" for s in slabs],
            y=gst_vals, marker_color=bar_colors, marker_line_width=0,
            hovertemplate="Slab %{x}<br>GST: ₹%{y:,.2f}<extra></extra>"))
        fig2.update_layout(barmode="stack",
            xaxis=dict(title="GST Slab", showgrid=False,
                tickfont=dict(family=FONT_FAM,size=12,color=FONT_COLOR), title_font=dict(family=FONT_FAM,color=FONT_COLOR)),
            yaxis=dict(title="Amount (₹)", tickformat=",.0f",
                tickfont=dict(family=FONT_FAM,size=11,color=FONT_COLOR), title_font=dict(family=FONT_FAM,color=FONT_COLOR),
                gridcolor=GRID_COLOR, gridwidth=0.5),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08, font=dict(family=FONT_FAM,size=12,color=FONT_COLOR)),
            margin=dict(t=20,b=40,l=60,r=10), height=295,
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG, bargap=0.3)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin:1.2rem 0'></div>", unsafe_allow_html=True)

    # All slabs comparison table
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📋  GST Comparison Across All Slabs</p>', unsafe_allow_html=True)
    slab_rows = []
    for s in slabs:
        g = base_amount * s / 100
        slab_rows.append({"GST Slab": f"{s}%", "Base Amount (₹)": f"{base_amount:,.2f}",
            "CGST (₹)": f"{g/2:,.2f}", "SGST (₹)": f"{g/2:,.2f}",
            "Total GST (₹)": f"{g:,.2f}", "Total Amount (₹)": f"{base_amount+g:,.2f}"})
    slab_df = pd.DataFrame(slab_rows).set_index("GST Slab")
    st.dataframe(slab_df, use_container_width=True, height=260)
    st.markdown('</div>', unsafe_allow_html=True)

    dl_col, _ = st.columns([1,3])
    with dl_col:
        export_rows = [{"GST Slab": r["GST Slab"], "Base Amount": base_amount,
            "CGST": base_amount*float(r["GST Slab"].replace("%",""))/200,
            "SGST": base_amount*float(r["GST Slab"].replace("%",""))/200,
            "Total GST": base_amount*float(r["GST Slab"].replace("%",""))/100,
            "Total Amount": base_amount + base_amount*float(r["GST Slab"].replace("%",""))/100}
            for r in slab_rows]
        st.download_button("⬇  Download GST Table (CSV)", pd.DataFrame(export_rows).to_csv(index=False),
            file_name=f"GST_{int(base_amount)}base_{gst_rate}.csv", mime="text/csv")

    st.markdown('<div class="footer"><b>GST Calculator</b> &nbsp;·&nbsp; Results are indicative only. Consult your CA for exact tax figures.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    page_home()
elif st.session_state.page == "emi":
    page_emi()
elif st.session_state.page == "bond":
    page_bond()
elif st.session_state.page == "sip":
    page_sip()
elif st.session_state.page == "fd":
    page_fd()
elif st.session_state.page == "npv":
    page_npv()
elif st.session_state.page == "gst":
    page_gst()
