import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# =============================
# Config
# =============================
st.set_page_config(page_title="FMD • Executive Marketing Dashboard", layout="wide")

PROJECT_ID = "campaign-analytics-487115"
TABLE_DAILY = "campaign-analytics-487115.campaign_analytics.mrt_campaign_daily"

# =============================
# Logo (SVG simples embutido)
# =============================
LOGO_SVG = """
<svg width="44" height="44" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6EE7F9"/>
      <stop offset="100%" stop-color="#A78BFA"/>
    </linearGradient>
  </defs>
  <rect x="6" y="6" width="44" height="44" rx="14" fill="url(#g)"/>
  <rect x="16" y="28" width="6" height="14" rx="3" fill="white" opacity="0.95"/>
  <rect x="25" y="22" width="6" height="20" rx="3" fill="white" opacity="0.95"/>
  <rect x="34" y="16" width="6" height="26" rx="3" fill="white" opacity="0.95"/>
</svg>
"""

# =============================
# CSS (corrige header cortado + cards)
# =============================
st.markdown(
    """
    <style>
      /* respiro no topo e evita "cortar" header */
      .block-container { padding-top: 1.6rem !important; padding-bottom: 2rem; }

      /* remove header padrão do Streamlit (aquele espaço azul/branco do topo) */
      header[data-testid="stHeader"] { height: 0rem; }

      /* container do nosso header */
      .brand-wrap {
        display:flex;
        align-items:center;
        gap: 14px;
        padding: 14px 16px;
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 18px;
        background: white;
        margin-bottom: 14px;
      }
      .brand-title {
        font-size: 1.55rem;
        font-weight: 750;
        line-height: 1.2;
        margin: 0;
      }
      .brand-subtitle {
        color: rgba(0,0,0,0.55);
        font-size: 0.95rem;
        margin-top: 4px;
      }

      /* cards KPI */
      div[data-testid="stMetric"] {
        border: 1px solid rgba(0,0,0,0.08);
        padding: 14px 14px;
        border-radius: 16px;
        background: white;
      }

      /* evita overflow horizontal */
      .stApp { overflow-x: hidden; }

      /* cards “soft” */
      .soft-card {
        border: 1px solid rgba(0,0,0,0.08);
        padding: 18px;
        border-radius: 18px;
        background: white;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# Helpers
# =============================
def brl(x):
    # evita crash quando x é None/NaN
    if x is None or (isinstance(x, float) and pd.isna(x)) or pd.isna(x):
        return "—"
    return f"R$ {float(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def intfmt(x):
    if x is None or pd.isna(x):
        return "—"
    return f"{int(x):,}".replace(",", ".")

def pct(x):
    if x is None or pd.isna(x):
        return "—"
    return f"{x*100:.1f}%".replace(".", ",")

def safe_delta(curr, prev):
    # retorna variação percentual, ou None se não der
    if prev is None or pd.isna(prev) or prev == 0:
        return None
    return (curr - prev) / prev

def normalize_period(period, min_dt, max_dt):
    # Aceita: date �nica, tupla/lista com 0-2 datas, None
    start_dt, end_dt = min_dt, max_dt

    if period is None:
        pass
    elif isinstance(period, (tuple, list)):
        values = [d for d in period if d is not None]
        if len(values) >= 2:
            start_dt, end_dt = values[0], values[1]
        elif len(values) == 1:
            start_dt = values[0]
            end_dt = values[0]
    else:
        start_dt, end_dt = period, period

    if start_dt is None:
        start_dt = min_dt
    if end_dt is None:
        end_dt = max_dt

    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    return start_dt, end_dt

# =============================
# BigQuery Loader
# =============================
@st.cache_data(ttl=600)
def load_daily() -> pd.DataFrame:
    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
    SELECT
      transaction_date,
      campaign_id,
      campaign_name,
      clientes_ativos,
      transacoes,
      receita_total,
      ticket_medio
    FROM `{TABLE_DAILY}`
    """

    df = client.query(query).to_dataframe()

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce").dt.date
    for c in ["clientes_ativos", "transacoes"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    for c in ["receita_total", "ticket_medio"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    return df

# =============================
# Header (FMD)
# =============================
st.markdown(
    f"""
    <div class="brand-wrap">
      <div style="flex:0 0 auto;">{LOGO_SVG}</div>
      <div style="min-width:0;">
        <div class="brand-title">FMD Insights • Executive Marketing Dashboard</div>
        <div class="brand-subtitle">
          Performance de campanhas (BigQuery → mart diário). Layout executivo para portfólio e entrevistas.
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

df = load_daily()

# =============================
# Sidebar (Filtros)
# =============================
st.sidebar.markdown("## Filtros")

min_dt = df["transaction_date"].min() if df["transaction_date"].notna().any() else date.today()
max_dt = df["transaction_date"].max() if df["transaction_date"].notna().any() else date.today()

default_start = max(min_dt, max_dt - timedelta(days=60))
period = st.sidebar.date_input(
    "Período",
    value=(default_start, max_dt),
    min_value=min_dt,
    max_value=max_dt
)

start_dt, end_dt = normalize_period(period, min_dt, max_dt)

campaigns = ["Todas"] + sorted(df["campaign_name"].dropna().unique().tolist())
campaign_sel = st.sidebar.selectbox("Campanha", campaigns)

ids = ["Todos"] + sorted(df["campaign_id"].dropna().unique().tolist())
id_sel = st.sidebar.selectbox("Campaign ID", ids)

compare_prev = st.sidebar.checkbox("Comparar com período anterior", value=True)

if st.sidebar.button("Limpar cache"):
    st.cache_data.clear()
    st.rerun()

# aplica filtros
fdf = df[(df["transaction_date"] >= start_dt) & (df["transaction_date"] <= end_dt)].copy()
if campaign_sel != "Todas":
    fdf = fdf[fdf["campaign_name"] == campaign_sel]
if id_sel != "Todos":
    fdf = fdf[fdf["campaign_id"] == id_sel]

if fdf.empty:
    st.warning("Sem dados para o per�odo e filtros selecionados.")
    st.stop()

# período anterior equivalente
days = (end_dt - start_dt).days + 1
prev_end = start_dt - timedelta(days=1)
prev_start = prev_end - timedelta(days=days - 1)

pdf = df[(df["transaction_date"] >= prev_start) & (df["transaction_date"] <= prev_end)].copy()
if campaign_sel != "Todas":
    pdf = pdf[pdf["campaign_name"] == campaign_sel]
if id_sel != "Todos":
    pdf = pdf[pdf["campaign_id"] == id_sel]

# =============================
# KPIs
# =============================
revenue = float(fdf["receita_total"].sum())
tx = int(fdf["transacoes"].sum())

# clientes_ativos aqui é diário; somar no período pode "repetir" clientes em dias diferentes
active_daily_sum = int(fdf["clientes_ativos"].sum())

ticket_weighted = (revenue / tx) if tx else 0.0

prev_revenue = float(pdf["receita_total"].sum()) if compare_prev else None
prev_tx = int(pdf["transacoes"].sum()) if compare_prev else None
prev_ticket = (prev_revenue / prev_tx) if (compare_prev and prev_tx) else None

d_rev = safe_delta(revenue, prev_revenue) if compare_prev else None
d_tx = safe_delta(tx, prev_tx) if compare_prev else None
d_tk = safe_delta(ticket_weighted, prev_ticket) if compare_prev else None

k1, k2, k3, k4 = st.columns(4)
k1.metric("Receita", brl(revenue), pct(d_rev) if d_rev is not None else None)
k2.metric("Transações", intfmt(tx), pct(d_tx) if d_tx is not None else None)
k3.metric("Clientes ativos (soma diária)", intfmt(active_daily_sum), help="Soma de clientes ativos por dia (pode contar o mesmo cliente em dias diferentes).")
k4.metric("Ticket médio (ponderado)", brl(ticket_weighted), pct(d_tk) if d_tk is not None else None)

st.divider()

# =============================
# Tabs
# =============================
tab1, tab2, tab3 = st.tabs(["📌 Executive Overview", "📈 Performance", "🧾 Dados & Export"])

# -----------------------------
# TAB 1 — Executive Overview
# -----------------------------
with tab1:
    left, right = st.columns([2, 1])

    ts = (
        fdf.groupby("transaction_date", as_index=False)
        .agg(
            receita_total=("receita_total", "sum"),
            transacoes=("transacoes", "sum"),
            clientes_ativos=("clientes_ativos", "sum"),
        )
        .sort_values("transaction_date")
    )

    with left:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("#### Receita ao longo do tempo")
        fig = px.line(ts, x="transaction_date", y="receita_total", markers=True)
        fig.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("#### Mix de receita (por campanha)")
        mix = (
            fdf.groupby("campaign_name", as_index=False)["receita_total"]
            .sum()
            .sort_values("receita_total", ascending=False)
        )

        if mix.empty:
            st.info("Sem dados no período selecionado.")
        else:
            # agrupa “Outras” se tiver muitas campanhas
            if len(mix) > 8:
                top = mix.head(7)
                other = pd.DataFrame([{"campaign_name": "Outras", "receita_total": mix["receita_total"].iloc[7:].sum()}])
                mix = pd.concat([top, other], ignore_index=True)

            fig2 = px.pie(mix, names="campaign_name", values="receita_total", hole=0.55)
            fig2.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("#### Top campanhas (Receita)")
        rank = (
            fdf.groupby(["campaign_id", "campaign_name"], as_index=False)
            .agg(receita_total=("receita_total", "sum"), transacoes=("transacoes", "sum"))
            .sort_values("receita_total", ascending=False)
            .head(10)
        )

        if rank.empty:
            st.info("Sem dados para ranking no período selecionado.")
        else:
            fig3 = px.bar(rank, x="receita_total", y="campaign_name", orientation="h")
            fig3.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), yaxis_title="")
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("#### Insights automáticos (simulado executivo)")

        if not ts.empty:
            best = ts.loc[ts["receita_total"].idxmax()]
            worst = ts.loc[ts["receita_total"].idxmin()]
            st.write(f"**Melhor dia:** {best['transaction_date']} • **{brl(best['receita_total'])}**")
            st.write(f"**Pior dia:** {worst['transaction_date']} • **{brl(worst['receita_total'])}**")
            st.write(f"**Período:** {start_dt} → {end_dt} (**{days} dias**)")

        if compare_prev:
            st.write("---")
            st.write("**Comparação vs período anterior**")
            st.write(f"- Receita: {brl(revenue)} (antes: {brl(prev_revenue)})")
            st.write(f"- Transações: {intfmt(tx)} (antes: {intfmt(prev_tx)})")
            st.write(f"- Ticket: {brl(ticket_weighted)} (antes: {brl(prev_ticket)})")

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# TAB 2 — Performance
# -----------------------------
with tab2:
    ts = (
        fdf.groupby("transaction_date", as_index=False)
        .agg(
            receita_total=("receita_total", "sum"),
            transacoes=("transacoes", "sum"),
            clientes_ativos=("clientes_ativos", "sum"),
        )
        .sort_values("transaction_date")
    )

    g1, g2 = st.columns([2, 1])
    with g1:
        st.markdown("#### Receita diária")
        fig = px.line(ts, x="transaction_date", y="receita_total", markers=True)
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with g2:
        st.markdown("#### Transações diárias")
        fig = px.bar(ts, x="transaction_date", y="transacoes")
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Eficiência (Ticket médio ponderado)")
    ts["ticket_ponderado"] = ts["receita_total"] / ts["transacoes"].replace(0, pd.NA)
    fig = px.line(ts, x="transaction_date", y="ticket_ponderado", markers=True)
    fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TAB 3 — Dados & Export
# -----------------------------
with tab3:
    st.markdown("#### Tabela (mrt_campaign_daily)")
    st.caption("Para dados realmente detalhados (clientes únicos, top customers, distribuição de tickets), use a mrt_campaign_detailed.")

    q = st.text_input("Buscar (nome da campanha ou ID)", value="")
    tdf = fdf.copy()

    if q.strip():
        ql = q.strip().lower()
        tdf = tdf[
            tdf["campaign_name"].str.lower().str.contains(ql, na=False)
            | tdf["campaign_id"].str.lower().str.contains(ql, na=False)
        ]

    st.dataframe(
        tdf.sort_values("transaction_date", ascending=False),
        use_container_width=True,
        height=420
    )

    st.download_button(
        "⬇️ Baixar CSV filtrado",
        data=tdf.to_csv(index=False).encode("utf-8"),
        file_name="fmd_campaign_daily_filtered.csv",
        mime="text/csv"
    )

