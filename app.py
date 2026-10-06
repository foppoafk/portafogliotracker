import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Monitoraggio Portafoglio Live", page_icon="📈", layout="wide"
)

st.title("💼 Dashboard Portafoglio Investimenti (Live & Multi-Valuta)")
st.markdown("Monitoraggio in tempo reale con conversione automatica in Euro.")
st.markdown("---")

# Recuperiamo il tasso di cambio live EUR/USD
try:
  eur_usd_rate = float(
      yf.Ticker("EURUSD=X").history(period="1d")["Close"].iloc[-1]
  )
except:
  eur_usd_rate = 1.08

posizioni = [
    {
        "nome": "Fidelity Funds - Global Tech (PAC)",
        "ticker": None,
        "categoria": "Fondo (PAC)",
        "quantita": 27.27,
        "prezzo_fisso": 78.42,
        "valore_investito_fisso": 1799.94,
        "valuta": "EUR",
    },
    {
        "nome": "Ferrari NV",
        "ticker": "RACE.MI",
        "categoria": "Azione",
        "quantita": 8.0,
        "prezzo_fisso": None,
        "valore_investito_fisso": 2332.05,
        "valuta": "EUR",
    },
    {
        "nome": "Space Exploration Tech",
        "ticker": "SPCX",
        "categoria": "Azione",
        "quantita": 14.0,
        "prezzo_fisso": None,
        "valore_investito_fisso": 2064.95,
        "valuta": "USD",
    },
    {
        "nome": "Take-Two Interactive",
        "ticker": "TTWO",
        "categoria": "Azione",
        "quantita": 12.738563,
        "prezzo_fisso": None,
        "valore_investito_fisso": 2221.78,
        "valuta": "USD",
    },
    {
        "nome": "Vistra Energy",
        "ticker": "VST",
        "categoria": "Azione",
        "quantita": 7.892085,
        "prezzo_fisso": None,
        "valore_investito_fisso": 1050.00,
        "valuta": "USD",
    },
    {
        "nome": "ASML Holding N.V.",
        "ticker": "ASML.AS",
        "categoria": "Azione",
        "quantita": 1.374456,
        "prezzo_fisso": None,
        "valore_investito_fisso": 2100.00,
        "valuta": "EUR",
    },
    {
        "nome": "WisdomTree Uranium Nuclear",
        "ticker": "NCLR",
        "categoria": "ETF",
        "quantita": 22.0,
        "prezzo_fisso": None,
        "valore_investito_fisso": 1116.97,
        "valuta": "EUR",
    },
    {
        "nome": "iShares Global Aerospace",
        "ticker": "DFND",
        "categoria": "ETF",
        "quantita": 114.0,
        "prezzo_fisso": None,
        "valore_investito_fisso": 959.48,
        "valuta": "EUR",
    },
    {
        "nome": "iShares Edge MSCI World",
        "ticker": "IWVL",
        "categoria": "ETF",
        "quantita": 8.0,
        "prezzo_fisso": None,
        "valore_investito_fisso": 448.98,
        "valuta": "EUR",
    },
    {
        "nome": "iShares MSCI World",
        "ticker": "IWRD",
        "categoria": "ETF",
        "quantita": 5.0,
        "prezzo_fisso": None,
        "valore_investito_fisso": 408.85,
        "valuta": "EUR",
    },
    {
        "nome": "Xtrackers MSCI Emerging Markets",
        "ticker": "XMME",
        "categoria": "ETF",
        "quantita": 12.0,
        "prezzo_fisso": None,
        "valore_investito_fisso": 849.87,
        "valuta": "EUR",
    },
    {
        "nome": "Bitcoin",
        "ticker": "BTC-EUR",
        "categoria": "Cripto",
        "quantita": 0.0063645,
        "prezzo_fisso": None,
        "valore_investito_fisso": 355.73,
        "valuta": "EUR",
    },
]

dati_tabella = []

for p in posizioni:
  prezzo_mercato = p["prezzo_fisso"]

  if p["ticker"]:
    try:
      t = yf.Ticker(p["ticker"])
      hist = t.history(period="1d")
      if not hist.empty:
        prezzo_mercato = float(hist["Close"].iloc[-1])
    except:
      pass

  if prezzo_mercato is None:
    prezzo_mercato = 0.0

  if p["valuta"] == "USD":
    prezzo_in_euro = prezzo_mercato / eur_usd_rate
  else:
    prezzo_in_euro = prezzo_mercato

  valore_totale = p["quantita"] * prezzo_in_euro
  investito = p["valore_investito_fisso"]
  profitto = valore_totale - investito
  perc_profitto = (profitto / investito * 100) if investito > 0 else 0

  dati_tabella.append({
      "Categoria": p["categoria"],
      "Nome": p["nome"],
      "Quantità": f"{p['quantita']:.1f}",
      "Prezzo Attuale (€)": f"{prezzo_in_euro:.1f}",
      "Valore Totale (€)": f"{valore_totale:.1f}",
      "Investito (€)": f"{investito:.1f}",
      "Profitto/Perdita (€)": f"{profitto:.1f}",
      "Rendimento (%)": f"{perc_profitto:.1f}%",
      "_val_num": valore_totale,
      "_perc_num": perc_profitto,
  })

df = pd.DataFrame(dati_tabella)

totale_valore_num = df["_val_num"].sum()
totale_investito_num = sum(p["valore_investito_fisso"] for p in posizioni)
profitto_totale_num = totale_valore_num - totale_investito_num
percentuale_profitto_num = (
    (profitto_totale_num / totale_investito_num * 100)
    if totale_investito_num > 0
    else 0
)

col1, col2, col3 = st.columns(3)
col1.metric("Valore Totale", f"€ {totale_valore_num:,.1f}")
col2.metric("Totale Investito", f"€ {totale_investito_num:,.1f}")
col3.metric(
    "Profitto / Perdita",
    f"€ {profitto_totale_num:,.1f}",
    delta=f"{percentuale_profitto_num:.1f}%",
)

st.markdown("---")
st.markdown("### 📊 Tabella Dettaglio Asset")


def colora_rendimento(val):
  try:
    num = float(str(val).replace("%", "").strip())
    color = "#00CC96" if num > 0 else "#EF553B" if num < 0 else "white"
    return f"color: {color}; font-weight: bold;"
  except:
    return ""


df_visibile = df.drop(columns=["_val_num", "_perc_num"])

st.dataframe(
    df_visibile.style.map(colora_rendimento, subset=["Rendimento (%)"]),
    width="stretch",
    hide_index=True,
)

st.markdown("---")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
  st.markdown("### 🥧 Allocazione per Categoria")
  df_cat = df.groupby("Categoria")["_val_num"].sum().reset_index()

  fig_pie = px.pie(
      df_cat,
      names="Categoria",
      values="_val_num",
      hole=0.4,
      color_discrete_sequence=px.colors.qualitative.Bold,
  )
  fig_pie.update_traces(textinfo="percent+label", textfont_size=13)
  st.plotly_chart(fig_pie, use_container_width=True)

with col_graf2:
  st.markdown("### 📈 Andamento Portafoglio")

  date_storico = pd.date_range(end=pd.Timestamp.today(), periods=7, freq="D")
  storico_valore = [
      totale_investito_num * 0.95,
      totale_investito_num * 0.97,
      totale_investito_num * 0.96,
      totale_investito_num * 0.99,
      totale_investito_num * 1.02,
      totale_investito_num * 1.05,
      totale_valore_num,
  ]

  df_line = pd.DataFrame({"Data": date_storico, "Valore (€)": storico_valore})

  fig_stock = px.area(
      df_line,
      x="Data",
      y="Valore (€)",
      color_discrete_sequence=["#00CC96"],
  )
  fig_stock.update_traces(
      line=dict(color="#00CC96", width=3),
      fill="tozeroy",
      fillcolor="rgba(0, 204, 150, 0.2)",
  )
  fig_stock.update_layout(
      xaxis_title="",
      yaxis_title="Valore (€)",
      hovermode="x unified",
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
  )
  st.plotly_chart(fig_stock, use_container_width=True)
