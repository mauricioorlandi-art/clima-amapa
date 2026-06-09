import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Relatório Climático",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');
:root {
    --bg:#0a1628; --surface:#0f2040; --surface2:#162b52;
    --accent:#00e5ff; --accent2:#00ff9d; --accent3:#ff6b6b;
    --accent4:#ffd166; --text:#e8f4fd; --muted:#7ba3c8;
}
html,body,[data-testid="stAppViewContainer"]{background-color:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0a1f3d 0%,#071530 100%)!important;border-right:1px solid #1a3a6e;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
h1,h2,h3{font-family:'Space Mono',monospace!important;}
.stMetric{background:var(--surface)!important;border:1px solid #1a3a6e!important;border-radius:12px!important;padding:16px!important;}
.stMetric label{color:var(--muted)!important;font-size:0.75rem!important;text-transform:uppercase;letter-spacing:.1em;}
.stMetric [data-testid="metric-container"]>div{color:var(--accent)!important;font-family:'Space Mono',monospace!important;}
[data-testid="stSelectbox"]>div>div,[data-testid="stDateInput"]>div>div{background:var(--surface2)!important;border:1px solid #1e4a8a!important;color:var(--text)!important;border-radius:8px!important;}
.header-bar{background:linear-gradient(135deg,#0f2040 0%,#162b52 50%,#0a1f3d 100%);border:1px solid #1a3a6e;border-radius:16px;padding:24px 32px;margin-bottom:24px;}
.tag{display:inline-block;background:rgba(0,229,255,.12);border:1px solid rgba(0,229,255,.3);color:var(--accent);font-family:'Space Mono',monospace;font-size:.7rem;padding:3px 10px;border-radius:20px;margin-left:8px;}
.section-title{font-family:'Space Mono',monospace;font-size:.8rem;text-transform:uppercase;letter-spacing:.15em;color:var(--muted);margin-bottom:12px;border-left:3px solid var(--accent);padding-left:10px;}
</style>
""", unsafe_allow_html=True)

# ── Constantes ─────────────────────────────────────────────────────────────────
CIDADES = {
    "Macapá":           {"lat":  0.0349, "lon": -51.0694},
    "Santana":          {"lat": -0.0589, "lon": -51.1783},
    "Laranjal do Jari": {"lat": -0.8022, "lon": -52.4619},
    "Oiapoque":         {"lat":  3.8411, "lon": -51.8339},
    "Amapá":            {"lat":  2.0522, "lon": -50.7961},
    "Tartarugalzinho":  {"lat":  1.5056, "lon": -50.9072},
}
CORES = {
    "temp_max":"#ff6b6b","temp_min":"#00e5ff","temp_mean":"#ffd166",
    "precipitation":"#00ff9d","humidity":"#a78bfa","wind":"#fb923c",
}
MESES_PT = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
            7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e8f4fd", family="DM Sans"),
    xaxis=dict(gridcolor="#1a3a6e", linecolor="#1a3a6e", zerolinecolor="#1a3a6e"),
    margin=dict(l=10,r=10,t=40,b=10), hovermode="x unified",
)
_YAXIS  = dict(gridcolor="#1a3a6e", linecolor="#1a3a6e", zerolinecolor="#1a3a6e")
_LEGEND = dict(bgcolor="rgba(10,31,61,0.8)", bordercolor="#1a3a6e", borderwidth=1)
_YAXIS2 = dict(overlaying="y", side="right", showgrid=False,
               gridcolor="rgba(0,0,0,0)", color="#e8f4fd")

# ── API ────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def buscar_clima(lat, lon, inicio, fim):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": str(inicio), "end_date": str(fim),
        "daily": (
            "temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
            "precipitation_sum,windspeed_10m_max,"
            "relative_humidity_2m_max,relative_humidity_2m_min"
        ),
        "timezone": "America/Belem",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    d = r.json()["daily"]
    df = pd.DataFrame(d)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df.columns = ["temp_max","temp_min","temp_mean","precipitation","wind","hum_max","hum_min"]
    df["humidity"] = (df["hum_max"] + df["hum_min"]) / 2
    df.drop(columns=["hum_max","hum_min"], inplace=True)
    return df

def agregar(df, agg):
    regra = {"Semanal":"W","Mensal":"ME"}.get(agg)
    if regra:
        try:
            return df.resample(regra).agg({
                "temp_max":"max","temp_min":"min","temp_mean":"mean",
                "precipitation":"sum","wind":"max","humidity":"mean"
            })
        except ValueError:
            return df.resample("M").agg({
                "temp_max":"max","temp_min":"min","temp_mean":"mean",
                "precipitation":"sum","wind":"max","humidity":"mean"
            })
    return df

# ── Barra lateral ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 **RELATÓRIO CLIMA**")
    st.markdown("---")
    cidade = st.selectbox("🏙 Cidade", list(CIDADES.keys()))
    st.markdown("---")
    st.markdown("#### 📅 Período de análise")
    c1, c2 = st.columns(2)
    DATA_MAX = date.today() - timedelta(days=7)
    with c1:
        data_inicio = st.date_input("Início", value=date(2023,1,1),
                                    min_value=date(1940,1,1), max_value=DATA_MAX)
    with c2:
        data_fim = st.date_input("Fim", value=DATA_MAX,
                                 min_value=date(1940,1,2), max_value=DATA_MAX)
    st.markdown("---")
    st.markdown("#### 📊 Comparar com outro ano")
    comparar = st.checkbox("Ativar comparação")
    ano_comparacao = None
    if comparar:
        ano_comparacao = st.number_input(
            "Ano de referência", min_value=1940,
            max_value=date.today().year - 1, value=date.today().year - 2
        )
    st.markdown("---")
    agregacao = st.selectbox("🔍 Agregação", ["Diário","Semanal","Mensal"])
    st.markdown("---")
    st.markdown("<div style='font-size:.7rem;color:#7ba3c8;'>Fonte: Open-Meteo Archive API<br>Sem necessidade de chave de API</div>",
                unsafe_allow_html=True)

# ── Validação ──────────────────────────────────────────────────────────────────
if data_inicio >= data_fim:
    st.error("⚠️ A data de início deve ser anterior à data de fim.")
    st.stop()

lat = CIDADES[cidade]["lat"]
lon = CIDADES[cidade]["lon"]

# ── Cabeçalho ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header-bar">
  <div style="font-size:2rem;font-family:'Space Mono',monospace;font-weight:700;color:#e8f4fd;">
    CLIMA AMAPÁ <span class="tag">BRASIL</span>
  </div>
  <div style="color:#7ba3c8;font-size:.9rem;margin-top:4px;">
    📍 {cidade} &nbsp;·&nbsp; {lat:.4f}°, {lon:.4f}° &nbsp;·&nbsp;
    {data_inicio.strftime('%d/%m/%Y')} → {data_fim.strftime('%d/%m/%Y')}
  </div>
</div>
""", unsafe_allow_html=True)

# ── Carrega dados ──────────────────────────────────────────────────────────────
with st.spinner("Carregando dados climáticos..."):
    try:
        df = buscar_clima(lat, lon, data_inicio, data_fim)
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        st.stop()

df_agg = agregar(df, agregacao)

# ── Indicadores (KPIs) ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Resumo do período</div>', unsafe_allow_html=True)

kpi_data = [
    ("🌡", "Temp. Média",   f"{df['temp_mean'].mean():.2f}", "°C"),
    ("🔥", "Máx. Absoluta", f"{df['temp_max'].max():.2f}",  "°C"),
    ("❄️", "Mín. Absoluta", f"{df['temp_min'].min():.2f}",  "°C"),
    ("🌧", "Precip. Total", f"{df['precipitation'].sum():.2f}", "mm"),
    ("💧", "Umidade Média", f"{df['humidity'].mean():.2f}", "%"),
    ("💨", "Vento Máx.",    f"{df['wind'].max():.2f}",      "km/h"),
]
cols = st.columns(6)
for col, (icon, label, value, unit) in zip(cols, kpi_data):
    col.markdown(f"""
    <div style="background:#0f2040;border:1px solid #1a3a6e;border-radius:12px;padding:12px 10px;text-align:center;">
      <div style="font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;color:#7ba3c8;margin-bottom:4px;">{icon} {label}</div>
      <div style="font-family:'Space Mono',monospace;font-size:1.15rem;font-weight:700;color:#00e5ff;line-height:1.1;">{value}</div>
      <div style="font-size:.7rem;color:#7ba3c8;margin-top:2px;">{unit}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Temperatura ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Temperatura</div>', unsafe_allow_html=True)
fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=df_agg.index, y=df_agg["temp_max"], name="Máxima",
    line=dict(color=CORES["temp_max"], width=1.5), mode="lines"))
fig_temp.add_trace(go.Scatter(x=df_agg.index, y=df_agg["temp_min"], name="Mínima",
    line=dict(color=CORES["temp_min"], width=1.5),
    fill="tonexty", fillcolor="rgba(0,229,255,0.07)", mode="lines"))
fig_temp.add_trace(go.Scatter(x=df_agg.index, y=df_agg["temp_mean"], name="Média",
    line=dict(color=CORES["temp_mean"], width=2, dash="dot"), mode="lines"))

if comparar and ano_comparacao:
    duracao = data_fim - data_inicio
    try:
        inicio_cmp = data_inicio.replace(year=int(ano_comparacao))
    except ValueError:
        inicio_cmp = data_inicio.replace(year=int(ano_comparacao), day=28)
    fim_cmp = min(inicio_cmp + duracao, date(int(ano_comparacao), 12, 31))
    try:
        df_cmp = buscar_clima(lat, lon, inicio_cmp, fim_cmp)
        df_cmp_agg = agregar(df_cmp, agregacao)
        deslocamento = df_agg.index[0] - df_cmp_agg.index[0]
        idx_deslocado = df_cmp_agg.index + deslocamento
        fig_temp.add_trace(go.Scatter(
            x=idx_deslocado, y=df_cmp_agg["temp_mean"],
            name=f"Média {int(ano_comparacao)}",
            line=dict(color="#a78bfa", width=1.5, dash="dash"),
            mode="lines", opacity=0.75
        ))
    except Exception as ex:
        st.warning(f"Não foi possível carregar dados de {int(ano_comparacao)}: {ex}")

fig_temp.update_layout(**LAYOUT_BASE, height=320, yaxis={**_YAXIS, "title":"°C"}, legend=_LEGEND,
    title=dict(text="Temperatura (°C)", font=dict(color="#7ba3c8", size=13)))
st.plotly_chart(fig_temp, width="stretch")

# ── Precipitação + Umidade ─────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="section-title">Precipitação</div>', unsafe_allow_html=True)
    fig_chuva = go.Figure()
    fig_chuva.add_trace(go.Bar(x=df_agg.index, y=df_agg["precipitation"],
        name="Chuva", marker_color=CORES["precipitation"], opacity=0.85, marker_line_width=0))
    rotulo = "diária" if agregacao == "Diário" else "acumulada"
    fig_chuva.update_layout(**LAYOUT_BASE, height=280, yaxis={**_YAXIS, "title":"mm"}, legend=_LEGEND,
        title=dict(text=f"Precipitação {rotulo} (mm)", font=dict(color="#7ba3c8", size=13)))
    st.plotly_chart(fig_chuva, width="stretch")

with col_b:
    st.markdown('<div class="section-title">Umidade Relativa</div>', unsafe_allow_html=True)
    fig_umid = go.Figure()
    fig_umid.add_trace(go.Scatter(x=df_agg.index, y=df_agg["humidity"],
        name="Umidade", line=dict(color=CORES["humidity"], width=2),
        fill="tozeroy", fillcolor="rgba(167,139,250,0.1)", mode="lines"))
    fig_umid.update_layout(**LAYOUT_BASE, height=280, yaxis={**_YAXIS, "title":"%", "range":[0,105]}, legend=_LEGEND,
        title=dict(text="Umidade Relativa Média (%)", font=dict(color="#7ba3c8", size=13)))
    st.plotly_chart(fig_umid, width="stretch")

# ── Comparação: Chuva × Umidade ────────────────────────────────────────────────
st.markdown('<div class="section-title">Comparação: Chuva × Umidade</div>', unsafe_allow_html=True)
fig_comp = go.Figure()

# Barras de precipitação no eixo secundário
fig_comp.add_trace(go.Bar(
    x=df_agg.index, y=df_agg["precipitation"],
    name="Precipitação (mm)", yaxis="y2",
    marker_color="rgba(0,255,157,0.45)", marker_line_width=0,
    opacity=0.8
))
# Linha de umidade no eixo principal
fig_comp.add_trace(go.Scatter(
    x=df_agg.index, y=df_agg["humidity"],
    name="Umidade (%)",
    line=dict(color=CORES["humidity"], width=2.5),
    fill="tozeroy", fillcolor="rgba(167,139,250,0.08)", mode="lines"
))

fig_comp.update_layout(
    **LAYOUT_BASE, height=340,
    title=dict(text="Relação entre Chuva e Umidade do Ar", font=dict(color="#7ba3c8", size=13)),
    yaxis={**_YAXIS, "title":"Umidade (%)", "range":[0,105]},
    yaxis2={**_YAXIS2, "title":"Precipitação (mm)"},
    legend=_LEGEND
)
st.plotly_chart(fig_comp, width="stretch")

# ── Vento ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Velocidade do Vento</div>', unsafe_allow_html=True)
fig_vento = go.Figure()
fig_vento.add_trace(go.Scatter(x=df_agg.index, y=df_agg["wind"],
    name="Vento Máx.", line=dict(color=CORES["wind"], width=1.5),
    fill="tozeroy", fillcolor="rgba(251,146,60,0.08)", mode="lines"))
fig_vento.update_layout(**LAYOUT_BASE, height=240, yaxis={**_YAXIS, "title":"km/h"}, legend=_LEGEND,
    title=dict(text="Velocidade Máxima do Vento (km/h)", font=dict(color="#7ba3c8", size=13)))
st.plotly_chart(fig_vento, width="stretch")

# ── Climatologia mensal ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Climatologia Mensal (período completo)</div>', unsafe_allow_html=True)
df_m = df.copy()
df_m["mes"] = df_m.index.month
clim = df_m.groupby("mes").agg(
    temp_max=("temp_max","mean"), temp_min=("temp_min","mean"),
    temp_mean=("temp_mean","mean"), precipitation=("precipitation","sum"),
    humidity=("humidity","mean"), wind=("wind","mean")
).reset_index()
clim["nome_mes"] = clim["mes"].map(MESES_PT)

fig_clim = go.Figure()
fig_clim.add_trace(go.Bar(x=clim["nome_mes"], y=clim["precipitation"],
    name="Precipitação (mm)", yaxis="y2",
    marker_color="rgba(0,255,157,0.35)", marker_line_width=0))
for col, rotulo, cor in [
    ("temp_max","Temp. Máxima", CORES["temp_max"]),
    ("temp_mean","Temp. Média",  CORES["temp_mean"]),
    ("temp_min","Temp. Mínima", CORES["temp_min"]),
]:
    fig_clim.add_trace(go.Scatter(x=clim["nome_mes"], y=clim[col], name=rotulo,
        line=dict(color=cor, width=2), mode="lines+markers", marker=dict(size=6)))

fig_clim.update_layout(
    **LAYOUT_BASE, height=340,
    title=dict(text="Temperatura média e precipitação por mês", font=dict(color="#7ba3c8", size=13)),
    yaxis={**_YAXIS, "title":"°C"},
    yaxis2={**_YAXIS2, "title":"mm"},
    legend=_LEGEND
)
st.plotly_chart(fig_clim, width="stretch")

# ── Dados brutos ───────────────────────────────────────────────────────────────
with st.expander("📋 Ver dados brutos"):
    df_exibir = df.copy().round(2)
    df_exibir.index = df_exibir.index.strftime("%d/%m/%Y")
    df_exibir.index.name = "Data"
    df_exibir.columns = [
        "Temp. Máxima (°C)", "Temp. Mínima (°C)", "Temp. Média (°C)",
        "Precipitação (mm)", "Vento Máx. (km/h)", "Umidade Média (%)"
    ]
    fmt = {col: "{:.2f}" for col in df_exibir.columns}
    st.dataframe(
        df_exibir.style.format(fmt).background_gradient(cmap="Blues", subset=["Precipitação (mm)"]),
        width="stretch"
    )
    
