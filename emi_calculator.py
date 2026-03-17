import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Know Your EMI",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Nunito:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Main padding */
.block-container {
    padding: 2.5rem 3rem 4rem 3rem;
    max-width: 1280px;
}

/* ── Hero banner ── */
.hero-wrap {
    background: linear-gradient(120deg, #1a1a4e 0%, #2d2d6e 50%, #1a3a5c 100%);
    border-radius: 24px;
    padding: 2.8rem 3rem 2.2rem 3rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(99,179,237,0.07);
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 320px; height: 200px;
    border-radius: 50%;
    background: rgba(159,122,234,0.06);
}
.hero-tag {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    color: #90cdf4;
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}
.hero-title span {
    background: linear-gradient(90deg, #63b3ed, #9f7aea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    color: rgba(255,255,255,0.5);
    font-size: 0.95rem;
    font-weight: 400;
    margin: 0;
}

/* ── Input section ── */
.input-section {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.8rem;
}
.input-section-title {
    font-size: 0.72rem;
    font-weight: 700;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1.2rem;
}

/* Streamlit input overrides */
label[data-testid="stWidgetLabel"] p {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.6) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-family: 'Nunito', sans-serif !important;
}
input[type="number"] {
    background: #ffffff !important;
    border: 1.5px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 0.6rem 1rem !important;
}
input[type="number"]:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.25) !important;
    background: #ffffff !important;
    color: #1a1a2e !important;
}
/* Also target the inner p tag and span inside number inputs */
[data-testid="stNumberInput"] input {
    color: #1a1a2e !important;
    background: #ffffff !important;
}
/* Streamlit wraps inputs in a div — ensure no inherited white-on-white */
div[data-baseweb="input"] {
    background: #ffffff !important;
    border-radius: 12px !important;
}
div[data-baseweb="input"] input {
    color: #1a1a2e !important;
    background: #ffffff !important;
    font-weight: 700 !important;
}

/* ── Metric cards ── */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1.8rem;
}
@media (max-width: 768px) {
    .cards-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 10px !important; }
    .block-container { padding: 1rem 0.8rem 3rem 0.8rem !important; }
    .hero-wrap { padding: 1.6rem 1.2rem 1.4rem 1.2rem !important; }
    .hero-title { font-size: 2rem !important; }
    .hero-sub { font-size: 0.82rem !important; }
    .input-section { padding: 1.2rem 1rem !important; }
    .chart-card { padding: 1rem 0.8rem 0.4rem 0.8rem !important; }
    .table-card { padding: 1rem 0.8rem !important; }
    .kpi-card { padding: 1rem 1rem !important; border-radius: 14px !important; }
    .kpi-icon { font-size: 1.1rem !important; margin-bottom: 0.3rem !important; }
    .kpi-label { font-size: 0.62rem !important; letter-spacing: 0.05em !important; white-space: normal !important; }
    .kpi-value { font-size: 1.05rem !important; }
}
.kpi-card {
    border-radius: 18px;
    padding: 1.4rem 1.5rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
    min-width: 0;
    word-break: break-word;
}
.kpi-card.blue   { background: linear-gradient(135deg, #1a3a6e 0%, #1e4d8c 100%); }
.kpi-card.green  { background: linear-gradient(135deg, #1a4a3a 0%, #1e6b52 100%); }
.kpi-card.red    { background: linear-gradient(135deg, #5a1a1a 0%, #7a2a2a 100%); }
.kpi-card.purple { background: linear-gradient(135deg, #2d1a5a 0%, #4a2d8c 100%); }
.kpi-card::after {
    content: '';
    position: absolute;
    top: -20px; right: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.kpi-icon  { font-size: 1.4rem; margin-bottom: 0.6rem; display: block; }
.kpi-label {
    font-size: 0.72rem; font-weight: 600; color: rgba(255,255,255,0.5);
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 5px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.kpi-value {
    font-size: 1.45rem; font-weight: 700; color: #ffffff;
    font-family: 'Nunito', sans-serif; line-height: 1.3;
    word-break: break-word; overflow-wrap: anywhere;
}
.kpi-card.blue   .kpi-value { color: #90cdf4; }
.kpi-card.green  .kpi-value { color: #68d391; }
.kpi-card.red    .kpi-value { color: #fc8181; }
.kpi-card.purple .kpi-value { color: #b794f4; }

/* ── Section titles ── */
.sec-title {
    font-size: 0.72rem;
    font-weight: 700;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 0 0 1rem 0;
}

/* ── Chart containers ── */
.chart-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.4rem 1.6rem 0.6rem 1.6rem;
}

/* ── Table card ── */
.table-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.4rem 1.6rem 1rem 1.6rem;
    margin-bottom: 1.5rem;
}
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* ── Download button ── */
.stDownloadButton button {
    background: linear-gradient(90deg, #3182ce, #553c9a) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 0.55rem 1.6rem !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em !important;
}
.stDownloadButton button:hover { opacity: 0.88 !important; }

/* ── Tip bar ── */
.tip-bar {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #63b3ed;
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1rem;
    margin-top: 1rem;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.6);
}
.tip-bar b { color: #90cdf4; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: rgba(255,255,255,0.2);
    font-size: 0.78rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
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


def calculate_emi(principal, annual_rate, years):
    n = years * 12
    r = annual_rate / 12 / 100
    emi = principal / n if r == 0 else principal * r * (1 + r)**n / ((1 + r)**n - 1)
    return emi, n, r


def build_schedule(principal, emi, r, n):
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


def fmt_cell(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return "—"
    return f"{val:,.2f}"


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-tag">🏦 Loan Planner</div>
  <div class="hero-title">Know Your <span>EMI</span></div>
  <p class="hero-sub">Enter your loan details · Instant breakdown · Full amortization schedule · Downloadable report</p>
</div>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<p class="input-section-title">⚙️  Loan Parameters</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    principal = st.number_input(
        "💰  Loan Amount (₹)",
        min_value=10_000, max_value=100_000_000,
        value=1_000_000, step=10_000, format="%d"
    )
with col2:
    annual_rate = st.number_input(
        "📈  Annual Interest Rate (%)",
        min_value=0.1, max_value=50.0,
        value=8.0, step=0.1, format="%.1f"
    )
with col3:
    years = st.number_input(
        "📅  Loan Tenure (Years)",
        min_value=1, max_value=30,
        value=5, step=1, format="%d"
    )
st.markdown('</div>', unsafe_allow_html=True)

# ── Compute ───────────────────────────────────────────────────────────────────
emi, n, r = calculate_emi(principal, annual_rate, years)
total_payable = emi * n
total_interest = total_payable - principal
interest_pct = total_interest / total_payable * 100
df = build_schedule(principal, emi, r, n)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cards-grid">
  <div class="kpi-card blue">
    <span class="kpi-icon">💸</span>
    <div class="kpi-label">Monthly EMI</div>
    <div class="kpi-value">{fmt_inr(emi)}</div>
  </div>
  <div class="kpi-card green">
    <span class="kpi-icon">🏦</span>
    <div class="kpi-label">Principal Amount</div>
    <div class="kpi-value">{fmt_inr(principal)}</div>
  </div>
  <div class="kpi-card red">
    <span class="kpi-icon">📊</span>
    <div class="kpi-label">Total Interest</div>
    <div class="kpi-value">{fmt_inr(total_interest)}</div>
  </div>
  <div class="kpi-card purple">
    <span class="kpi-icon">🧾</span>
    <div class="kpi-label">Total Payable</div>
    <div class="kpi-value">{fmt_inr(total_payable)}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Tip bar
st.markdown(f"""
<div class="tip-bar">
  💡 You pay <b>{interest_pct:.1f}%</b> as interest on your total outflow —
  that's <b>{fmt_inr(total_interest)}</b> over <b>{years} year{"s" if years > 1 else ""}</b>.
  Consider making prepayments to reduce your interest burden significantly.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin:1.6rem 0'></div>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
CHART_BG    = "rgba(0,0,0,0)"
GRID_COLOR  = "rgba(255,255,255,0.07)"
FONT_COLOR  = "rgba(255,255,255,0.5)"
FONT_FAMILY = "Nunito"

chart_col1, chart_col2 = st.columns([1, 1.7], gap="large")

with chart_col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">🥧  Principal vs Interest Breakup</p>', unsafe_allow_html=True)
    fig_pie = go.Figure(go.Pie(
        labels=["Principal", "Interest"],
        values=[round(principal, 2), round(total_interest, 2)],
        hole=0.65,
        marker=dict(colors=["#3182ce", "#e53e3e"],
                    line=dict(color="rgba(0,0,0,0.3)", width=3)),
        textinfo="label+percent",
        textfont=dict(family=FONT_FAMILY, size=12, color="white"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent}<extra></extra>",
    ))
    fig_pie.add_annotation(
        text=f"<b>{fmt_inr(total_payable)}</b><br>Total",
        x=0.5, y=0.5, xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=12, family=FONT_FAMILY, color="white"),
        align="center",
    )
    fig_pie.update_layout(
        showlegend=True,
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.05,
                    font=dict(family=FONT_FAMILY, size=12, color=FONT_COLOR)),
        margin=dict(t=5, b=10, l=10, r=10),
        height=295,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart_col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📉  Yearly Balance Reduction</p>', unsafe_allow_html=True)
    yearly = df[(df["Period"] % 12 == 0) & (df["Period"] > 0)].copy()
    yearly["Paid Off"] = principal - yearly["Remaining Amount"]
    yearly["Year"] = (yearly["Period"] / 12).astype(int)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Outstanding", x=yearly["Year"],
        y=yearly["Remaining Amount"].round(2),
        marker_color="#3182ce", marker_line_width=0,
        hovertemplate="<b>Year %{x}</b><br>Outstanding: ₹%{y:,.2f}<extra></extra>",
    ))
    fig_bar.add_trace(go.Bar(
        name="Paid Off", x=yearly["Year"],
        y=yearly["Paid Off"].round(2),
        marker_color="#68d391", marker_line_width=0,
        hovertemplate="<b>Year %{x}</b><br>Paid Off: ₹%{y:,.2f}<extra></extra>",
    ))
    fig_bar.update_layout(
        barmode="stack",
        xaxis=dict(title="Year", tickmode="linear", dtick=1, showgrid=False,
                   tickfont=dict(family=FONT_FAMILY, size=11, color=FONT_COLOR),
                   title_font=dict(family=FONT_FAMILY, color=FONT_COLOR)),
        yaxis=dict(title="Amount (₹)", tickformat=",.0f",
                   tickfont=dict(family=FONT_FAMILY, size=11, color=FONT_COLOR),
                   title_font=dict(family=FONT_FAMILY, color=FONT_COLOR),
                   gridcolor=GRID_COLOR, gridwidth=0.5),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=1.08,
                    font=dict(family=FONT_FAMILY, size=12, color=FONT_COLOR)),
        margin=dict(t=20, b=40, l=60, r=10),
        height=295,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        bargap=0.2,
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin:1.4rem 0'></div>", unsafe_allow_html=True)

# ── Amortization Table ────────────────────────────────────────────────────────
st.markdown('<div class="table-card">', unsafe_allow_html=True)
st.markdown('<p class="sec-title">📋  Amortization Schedule</p>', unsafe_allow_html=True)

display_df = df.copy()
for col in ["EMI", "Interest", "Principal Amount Paid", "Remaining Amount"]:
    display_df[col] = display_df[col].apply(fmt_cell)
display_df["Period"] = display_df["Period"].astype(int)
display_df = display_df.set_index("Period")

st.dataframe(display_df, use_container_width=True, height=420)
st.markdown('</div>', unsafe_allow_html=True)

# ── Download ──────────────────────────────────────────────────────────────────
export_df = df.copy()
for col in ["EMI", "Interest", "Principal Amount Paid"]:
    export_df[col] = export_df[col].apply(lambda x: round(x, 2) if x is not None else "")
export_df["Remaining Amount"] = export_df["Remaining Amount"].apply(lambda x: round(x, 2))
csv_data = export_df.to_csv(index=False)

dl_col, _ = st.columns([1, 3])
with dl_col:
    st.download_button(
        label="⬇  Download Schedule (CSV)",
        data=csv_data,
        file_name=f"KnowYourEMI_{int(principal)}_{annual_rate}pct_{years}yr.csv",
        mime="text/csv",
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <b>Know Your EMI</b> &nbsp;·&nbsp;
  EMI = P × r × (1+r)ⁿ / ((1+r)ⁿ − 1) &nbsp;·&nbsp;
  Results are indicative only. Consult your bank for exact figures.
</div>
""", unsafe_allow_html=True)
