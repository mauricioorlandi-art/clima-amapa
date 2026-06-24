import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
.stTabs [data-baseweb="tab-list"]{gap:6px;background:transparent;}
.stTabs [data-baseweb="tab"]{background:#0f2040;border:1px solid #1a3a6e;border-radius:10px 10px 0 0;color:#7ba3c8;font-family:'Space Mono',monospace;font-size:.8rem;padding:8px 16px;}
.stTabs [aria-selected="true"]{background:#162b52!important;color:#00e5ff!important;border-bottom:2px solid #00e5ff!important;}
.fc-card{background:#0f2040;border:1px solid #1a3a6e;border-radius:12px;padding:12px 8px;text-align:center;}
.alert-box{border-radius:10px;padding:12px 16px;margin-bottom:8px;font-size:.85rem;border-left:4px solid;}
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

# Tradução dos códigos de tempo WMO usados pela Forecast API → (descrição, ícone)
WEATHER_WMO = {
    0:("Céu limpo","☀️"), 1:("Predom. limpo","🌤️"), 2:("Parc. nublado","⛅"),
    3:("Nublado","☁️"), 45:("Névoa","🌫️"), 48:("Névoa gelada","🌫️"),
    51:("Garoa fraca","🌦️"), 53:("Garoa","🌦️"), 55:("Garoa forte","🌧️"),
    56:("Garoa congel.","🌧️"), 57:("Garoa congel.","🌧️"),
    61:("Chuva fraca","🌧️"), 63:("Chuva","🌧️"), 65:("Chuva forte","⛈️"),
    66:("Chuva congel.","🌨️"), 67:("Chuva congel.","🌨️"),
    71:("Neve fraca","🌨️"), 73:("Neve","🌨️"), 75:("Neve forte","❄️"),
    77:("Granizo fino","🌨️"),
    80:("Pancadas","🌦️"), 81:("Pancadas","🌧️"), 82:("Pancadas fortes","⛈️"),
    85:("Aguaneve","🌨️"), 86:("Aguaneve","🌨️"),
    95:("Trovoada","⛈️"), 96:("Trovoada/granizo","⛈️"), 99:("Trovoada/granizo","⛈️"),
}

# Parâmetros agronômicos por cultura (T base e GDD do ciclo são valores de
# referência amplamente usados; ajuste à cultivar/variedade local se precisar)
CULTURAS = {
    "Soja":  {"t_base": 10.0, "gdd_ciclo": 1400, "cor": "#00ff9d"},
    "Milho": {"t_base": 10.0, "gdd_ciclo": 1500, "cor": "#ffd166"},
}

# Janelas do calendário agrícola (mês, dia) → (mês, dia). APROXIMADAS para a
# região Norte/cerrado amapaense; o ideal é cruzar com o ZARC do município.
# Fases que cruzam a virada do ano são tratadas automaticamente.
ANO_BASE = 2024
CALENDARIO = {
    "Soja": {
        "cor": "#00ff9d",
        "fases": [
            ("Plantio",     (11, 15), (1, 15)),
            ("Ciclo",       (11, 15), (3, 31)),
            ("Colheita",    (3, 1),   (5, 15)),
        ],
    },
    "Milho 1ª safra": {
        "cor": "#ffd166",
        "fases": [
            ("Plantio",     (10, 1),  (12, 15)),
            ("Ciclo",       (10, 1),  (2, 28)),
            ("Colheita",    (2, 1),   (4, 15)),
        ],
    },
    "Milho safrinha": {
        "cor": "#fb923c",
        "fases": [
            ("Plantio",     (1, 15),  (3, 15)),
            ("Ciclo",       (1, 15),  (6, 15)),
            ("Colheita",    (5, 15),  (7, 31)),
        ],
    },
}

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
    """Dados históricos diários (Open-Meteo Archive). Inclui ET0 p/ balanço hídrico."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": str(inicio), "end_date": str(fim),
        "daily": (
            "temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
            "precipitation_sum,windspeed_10m_max,"
            "relative_humidity_2m_max,relative_humidity_2m_min,"
            "et0_fao_evapotranspiration"
        ),
        "timezone": "America/Belem",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["daily"])
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df = df.rename(columns={
        "temperature_2m_max": "temp_max", "temperature_2m_min": "temp_min",
        "temperature_2m_mean": "temp_mean", "precipitation_sum": "precipitation",
        "windspeed_10m_max": "wind", "et0_fao_evapotranspiration": "et0",
    })
    df["humidity"] = (df["relative_humidity_2m_max"] + df["relative_humidity_2m_min"]) / 2
    df = df.drop(columns=["relative_humidity_2m_max", "relative_humidity_2m_min"])
    return df


@st.cache_data(ttl=1800, show_spinner=False)
def buscar_previsao(lat, lon, dias=16):
    """Previsão diária (Open-Meteo Forecast). Mesma identidade de colunas + extras."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "daily": (
            "temperature_2m_max,temperature_2m_min,precipitation_sum,"
            "precipitation_probability_max,windspeed_10m_max,"
            "et0_fao_evapotranspiration,weathercode"
        ),
        "hourly": "relative_humidity_2m",
        "timezone": "America/Belem",
        "forecast_days": int(dias),
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    j = r.json()

    df = pd.DataFrame(j["daily"])
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df = df.rename(columns={
        "temperature_2m_max": "temp_max", "temperature_2m_min": "temp_min",
        "precipitation_sum": "precipitation", "precipitation_probability_max": "precip_prob",
        "windspeed_10m_max": "wind", "et0_fao_evapotranspiration": "et0",
        "weathercode": "wcode",
    })
    df["temp_mean"] = (df["temp_max"] + df["temp_min"]) / 2

    # umidade média diária a partir do horário
    h = pd.DataFrame(j["hourly"])
    h["time"] = pd.to_datetime(h["time"])
    h.set_index("time", inplace=True)
    df["humidity"] = h["relative_humidity_2m"].resample("D").mean().reindex(df.index)
    return df


def agregar(df, agg):
    regra = {"Semanal":"W","Mensal":"ME"}.get(agg)
    if regra:
        funcs = {"temp_max":"max","temp_min":"min","temp_mean":"mean",
                 "precipitation":"sum","wind":"max","humidity":"mean"}
        if "et0" in df.columns:
            funcs["et0"] = "sum"
        try:
            return df.resample(regra).agg(funcs)
        except ValueError:
            return df.resample("M").agg(funcs)
    return df


# ── Indicadores agronômicos ─────────────────────────────────────────────────────
def calcular_gdd(df, t_base):
    """Graus-dia diários: max(0, Tmédia - Tbase)."""
    tmean = (df["temp_max"] + df["temp_min"]) / 2
    return (tmean - t_base).clip(lower=0)


def maior_veranico(precip, limiar=1.0):
    """Maior sequência de dias consecutivos com chuva abaixo do limiar (mm)."""
    melhor = atual = 0
    for v in (precip < limiar):
        atual = atual + 1 if v else 0
        melhor = max(melhor, atual)
    return melhor


def fase_para_segmentos(mes_ini, dia_ini, mes_fim, dia_fim):
    """Converte uma janela (mês/dia)→(mês/dia) em segmentos de data no ANO_BASE,
    dividindo automaticamente quando a fase atravessa a virada do ano."""
    ini = date(ANO_BASE, mes_ini, dia_ini)
    fim = date(ANO_BASE, mes_fim, dia_fim)
    if fim >= ini:
        return [(ini, fim)]
    return [(ini, date(ANO_BASE, 12, 31)), (date(ANO_BASE, 1, 1), fim)]


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
    st.markdown("#### 🌾 Painel agronômico")
    cultura_ref = st.selectbox("Cultura de referência (GDD)", list(CULTURAS.keys()))
    st.markdown("#### 🔮 Previsão")
    dias_previsao = st.select_slider("Horizonte (dias)", options=[7, 10, 14, 16], value=14)
    st.markdown("---")
    st.markdown("<div style='font-size:.7rem;color:#7ba3c8;'>Fonte: Open-Meteo Archive + Forecast API<br>Sem necessidade de chave de API</div>",
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

# ── Abas ───────────────────────────────────────────────────────────────────────
tab_hist, tab_prev, tab_cal, tab_agro = st.tabs([
    "📊 HISTÓRICO", "🔮 PREVISÃO", "🌱 CALENDÁRIO AGRÍCOLA", "🌾 PAINEL AGRONÔMICO"
])

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ABA 1 — HISTÓRICO  (conteúdo original)                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab_hist:
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

    # Temperatura
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

    # Precipitação + Umidade
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

    # Comparação: Chuva × Umidade
    st.markdown('<div class="section-title">Comparação: Chuva × Umidade</div>', unsafe_allow_html=True)
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=df_agg.index, y=df_agg["precipitation"],
        name="Precipitação (mm)", yaxis="y2",
        marker_color="rgba(0,255,157,0.45)", marker_line_width=0, opacity=0.8))
    fig_comp.add_trace(go.Scatter(
        x=df_agg.index, y=df_agg["humidity"], name="Umidade (%)",
        line=dict(color=CORES["humidity"], width=2.5),
        fill="tozeroy", fillcolor="rgba(167,139,250,0.08)", mode="lines"))
    fig_comp.update_layout(
        **LAYOUT_BASE, height=340,
        title=dict(text="Relação entre Chuva e Umidade do Ar", font=dict(color="#7ba3c8", size=13)),
        yaxis={**_YAXIS, "title":"Umidade (%)", "range":[0,105]},
        yaxis2={**_YAXIS2, "title":"Precipitação (mm)"}, legend=_LEGEND)
    st.plotly_chart(fig_comp, width="stretch")

    # Vento
    st.markdown('<div class="section-title">Velocidade do Vento</div>', unsafe_allow_html=True)
    fig_vento = go.Figure()
    fig_vento.add_trace(go.Scatter(x=df_agg.index, y=df_agg["wind"],
        name="Vento Máx.", line=dict(color=CORES["wind"], width=1.5),
        fill="tozeroy", fillcolor="rgba(251,146,60,0.08)", mode="lines"))
    fig_vento.update_layout(**LAYOUT_BASE, height=240, yaxis={**_YAXIS, "title":"km/h"}, legend=_LEGEND,
        title=dict(text="Velocidade Máxima do Vento (km/h)", font=dict(color="#7ba3c8", size=13)))
    st.plotly_chart(fig_vento, width="stretch")

    # Climatologia mensal
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
        yaxis={**_YAXIS, "title":"°C"}, yaxis2={**_YAXIS2, "title":"mm"}, legend=_LEGEND)
    st.plotly_chart(fig_clim, width="stretch")

    # Dados brutos
    with st.expander("📋 Ver dados brutos"):
        df_exibir = df.copy().round(2)
        df_exibir.index = df_exibir.index.strftime("%d/%m/%Y")
        df_exibir.index.name = "Data"
        ordem = ["temp_max","temp_min","temp_mean","precipitation","wind","humidity","et0"]
        df_exibir = df_exibir[[c for c in ordem if c in df_exibir.columns]]
        df_exibir.columns = [
            "Temp. Máxima (°C)", "Temp. Mínima (°C)", "Temp. Média (°C)",
            "Precipitação (mm)", "Vento Máx. (km/h)", "Umidade Média (%)", "ET0 (mm)"
        ][:len(df_exibir.columns)]
        fmt = {col: "{:.2f}" for col in df_exibir.columns}
        st.dataframe(
            df_exibir.style.format(fmt).background_gradient(cmap="Blues", subset=["Precipitação (mm)"]),
            width="stretch")

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ABA 2 — PREVISÃO                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab_prev:
    st.markdown(f'<div class="section-title">Previsão para os próximos {dias_previsao} dias · {cidade}</div>',
                unsafe_allow_html=True)
    try:
        fc = buscar_previsao(lat, lon, dias_previsao)
    except Exception as e:
        st.error(f"Não foi possível obter a previsão: {e}")
        fc = None

    if fc is not None and not fc.empty:
        # Cartões diários com ícone do tempo
        st.markdown("<br>", unsafe_allow_html=True)
        max_cards = min(len(fc), 8)
        card_cols = st.columns(max_cards)
        for col, (idx, row) in zip(card_cols, fc.head(max_cards).iterrows()):
            desc, icon = WEATHER_WMO.get(int(row.get("wcode", 0)), ("—", "🌡"))
            prob = row.get("precip_prob")
            prob_txt = f"{int(prob)}%" if pd.notna(prob) else "—"
            col.markdown(f"""
            <div class="fc-card">
              <div style="font-size:.7rem;color:#7ba3c8;">{MESES_PT[idx.month]} {idx.day:02d}</div>
              <div style="font-size:1.6rem;line-height:1.3;">{icon}</div>
              <div style="font-family:'Space Mono',monospace;font-size:.95rem;color:#ff6b6b;">{row['temp_max']:.0f}°</div>
              <div style="font-family:'Space Mono',monospace;font-size:.8rem;color:#00e5ff;">{row['temp_min']:.0f}°</div>
              <div style="font-size:.65rem;color:#00ff9d;margin-top:3px;">💧 {prob_txt}</div>
              <div style="font-size:.6rem;color:#fb923c;">💨 {row['wind']:.0f} km/h</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfico: temperatura prevista (faixa máx/mín) + chuva
        st.markdown('<div class="section-title">Temperatura e chuva previstas</div>', unsafe_allow_html=True)
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Bar(x=fc.index, y=fc["precipitation"], name="Chuva (mm)", yaxis="y2",
            marker_color="rgba(0,255,157,0.5)", marker_line_width=0))
        fig_fc.add_trace(go.Scatter(x=fc.index, y=fc["temp_max"], name="Máxima",
            line=dict(color=CORES["temp_max"], width=2), mode="lines+markers"))
        fig_fc.add_trace(go.Scatter(x=fc.index, y=fc["temp_min"], name="Mínima",
            line=dict(color=CORES["temp_min"], width=2), mode="lines+markers",
            fill="tonexty", fillcolor="rgba(0,229,255,0.06)"))
        fig_fc.update_layout(**LAYOUT_BASE, height=340, legend=_LEGEND,
            title=dict(text="Previsão diária", font=dict(color="#7ba3c8", size=13)),
            yaxis={**_YAXIS, "title":"°C"}, yaxis2={**_YAXIS2, "title":"mm"})
        st.plotly_chart(fig_fc, width="stretch")

        # Vento + probabilidade de chuva
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">Vento previsto</div>', unsafe_allow_html=True)
            fig_w = go.Figure()
            fig_w.add_trace(go.Scatter(x=fc.index, y=fc["wind"], name="Vento Máx.",
                line=dict(color=CORES["wind"], width=2), mode="lines+markers",
                fill="tozeroy", fillcolor="rgba(251,146,60,0.08)"))
            fig_w.add_hline(y=10, line_dash="dash", line_color="#ff6b6b",
                annotation_text="Limite p/ pulverização (~10 km/h)",
                annotation_font_color="#ff6b6b", annotation_font_size=10)
            fig_w.update_layout(**LAYOUT_BASE, height=260, legend=_LEGEND,
                yaxis={**_YAXIS, "title":"km/h"},
                title=dict(text="Velocidade máx. do vento", font=dict(color="#7ba3c8", size=13)))
            st.plotly_chart(fig_w, width="stretch")
        with col2:
            st.markdown('<div class="section-title">Probabilidade de chuva</div>', unsafe_allow_html=True)
            fig_p = go.Figure()
            fig_p.add_trace(go.Bar(x=fc.index, y=fc.get("precip_prob"), name="Prob. (%)",
                marker_color="rgba(0,229,255,0.55)", marker_line_width=0))
            fig_p.update_layout(**LAYOUT_BASE, height=260, legend=_LEGEND,
                yaxis={**_YAXIS, "title":"%", "range":[0,105]},
                title=dict(text="Chance de precipitação", font=dict(color="#7ba3c8", size=13)))
            st.plotly_chart(fig_p, width="stretch")

        # ── Alertas operacionais ────────────────────────────────────────────────
        st.markdown('<div class="section-title">Alertas operacionais</div>', unsafe_allow_html=True)

        chuva_prevista = fc["precipitation"].sum()
        et0_prevista = fc["et0"].sum() if "et0" in fc.columns else 0
        balanco = chuva_prevista - et0_prevista

        # melhores dias para pulverizar: pouca chuva e vento moderado
        bons = fc[(fc["precipitation"] < 1.0) & (fc["wind"] < 12)]
        dias_bons = ", ".join(f"{MESES_PT[i.month]} {i.day:02d}" for i in bons.index[:6])
        # dias de chuva forte
        chuva_forte = fc[fc["precipitation"] >= 20]
        # estresse térmico
        estresse = fc[fc["temp_max"] >= 34]

        alertas = []
        if dias_bons:
            alertas.append(("#00ff9d", "🟢 Janela de pulverização",
                            f"Dias com pouca chuva e vento moderado: {dias_bons}."))
        else:
            alertas.append(("#fb923c", "🟡 Pulverização limitada",
                            "Poucos dias com condições ideais (chuva/vento) no horizonte previsto."))
        if not chuva_forte.empty:
            dias_cf = ", ".join(f"{MESES_PT[i.month]} {i.day:02d}" for i in chuva_forte.index)
            alertas.append(("#00e5ff", "🌧️ Chuva forte prevista",
                            f"≥20 mm em: {dias_cf}. Atenção a operações de campo e drenagem."))
        if not estresse.empty:
            dias_es = ", ".join(f"{MESES_PT[i.month]} {i.day:02d}" for i in estresse.index)
            alertas.append(("#ff6b6b", "🔥 Risco de estresse térmico",
                            f"Máx ≥34 °C em: {dias_es}. Crítico se coincidir com florescimento."))
        cor_bal = "#00ff9d" if balanco >= 0 else "#ff6b6b"
        sinal = "superávit" if balanco >= 0 else "déficit"
        alertas.append((cor_bal, "💧 Balanço hídrico previsto",
                        f"Chuva {chuva_prevista:.0f} mm − ET0 {et0_prevista:.0f} mm = "
                        f"<b>{balanco:+.0f} mm</b> ({sinal} no período)."))

        for cor, titulo, texto in alertas:
            st.markdown(f"""
            <div class="alert-box" style="background:{cor}1a;border-color:{cor};">
              <b style="color:{cor};">{titulo}</b><br>
              <span style="color:#e8f4fd;">{texto}</span>
            </div>""", unsafe_allow_html=True)

        st.caption("Previsão de até 16 dias. Quanto mais distante o dia, maior a incerteza — "
                   "use os primeiros dias para decisões operacionais.")

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ABA 3 — CALENDÁRIO AGRÍCOLA                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab_cal:
    st.markdown('<div class="section-title">Calendário de soja e milho — plantio, ciclo e colheita</div>',
                unsafe_allow_html=True)

    linhas = []
    for cultura, info in CALENDARIO.items():
        for nome_fase, (mi, di), (mf, df_) in info["fases"]:
            for ini, fim in fase_para_segmentos(mi, di, mf, df_):
                linhas.append({
                    "Atividade": f"{cultura} · {nome_fase}",
                    "Cultura": cultura,
                    "Fase": nome_fase,
                    "Início": pd.Timestamp(ini),
                    "Fim": pd.Timestamp(fim) + pd.Timedelta(days=1),
                })
    df_cal = pd.DataFrame(linhas)

    cor_fase = {"Plantio": "#00e5ff", "Ciclo": "#a78bfa", "Colheita": "#ffd166"}
    fig_cal = px.timeline(
        df_cal, x_start="Início", x_end="Fim", y="Atividade", color="Fase",
        color_discrete_map=cor_fase, category_orders={"Fase": ["Plantio", "Ciclo", "Colheita"]})
    fig_cal.update_yaxes(autorange="reversed", title=None, gridcolor="#1a3a6e")
    fig_cal.update_xaxes(
        tickformat="%b", dtick="M1", gridcolor="#1a3a6e",
        range=[pd.Timestamp(ANO_BASE,1,1), pd.Timestamp(ANO_BASE,12,31)])

    hoje_base = pd.Timestamp(ANO_BASE, date.today().month, date.today().day)
    fig_cal.add_vline(x=hoje_base, line_color="#00ff9d", line_width=2,
                      annotation_text="hoje", annotation_font_color="#00ff9d")

    fig_cal.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8f4fd", family="DM Sans"), height=420,
        margin=dict(l=10, r=10, t=30, b=10), legend=_LEGEND,
        title=dict(text="Janelas anuais (eixo = meses)", font=dict(color="#7ba3c8", size=13)))
    # rótulos de mês em PT
    fig_cal.update_xaxes(
        tickvals=[pd.Timestamp(ANO_BASE, m, 1) for m in range(1, 13)],
        ticktext=[MESES_PT[m] for m in range(1, 13)])
    st.plotly_chart(fig_cal, width="stretch")

    # Resumo textual por cultura
    cols_cal = st.columns(3)
    resumo = {
        "Soja": ("🟢", "Plantio nov–jan · ciclo ~120 dias · colheita mar–mai. "
                       "Plante no início das chuvas e busque colher antes do fim do período úmido."),
        "Milho 1ª safra": ("🟡", "Plantio out–dez · colheita fev–abr. "
                                  "Acompanha o início das águas; floração não pode pegar veranico."),
        "Milho safrinha": ("🟠", "Plantio jan–mar (após a soja) · colheita mai–jul. "
                                  "Maior risco hídrico no fim do ciclo — fique de olho no balanço hídrico."),
    }
    for col, (cult, (ic, txt)) in zip(cols_cal, resumo.items()):
        col.markdown(f"""
        <div class="fc-card" style="text-align:left;padding:14px 16px;">
          <b style="color:#00e5ff;">{ic} {cult}</b>
          <div style="color:#e8f4fd;font-size:.8rem;margin-top:6px;line-height:1.5;">{txt}</div>
        </div>""", unsafe_allow_html=True)

    st.caption("⚠️ Janelas aproximadas para a região Norte/cerrado amapaense. "
               "Antes de definir a data de plantio, confira o ZARC (Zoneamento Agrícola "
               "de Risco Climático) do município, que dá os períodos com menor risco por solo e cultivar.")

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ABA 4 — PAINEL AGRONÔMICO                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab_agro:
    st.markdown(f'<div class="section-title">Indicadores agronômicos · período selecionado · '
                f'referência: {cultura_ref}</div>', unsafe_allow_html=True)

    t_base = CULTURAS[cultura_ref]["t_base"]
    gdd_ciclo = CULTURAS[cultura_ref]["gdd_ciclo"]

    gdd_diario = calcular_gdd(df, t_base)
    gdd_acum = gdd_diario.cumsum()
    gdd_total = float(gdd_acum.iloc[-1]) if len(gdd_acum) else 0.0

    balanco_diario = df["precipitation"] - df["et0"] if "et0" in df.columns else df["precipitation"] * 0
    balanco_acum = balanco_diario.cumsum()
    balanco_total = float(balanco_acum.iloc[-1]) if len(balanco_acum) else 0.0

    dias_estresse = int((df["temp_max"] >= 34).sum())
    veranico = maior_veranico(df["precipitation"])
    pct_ciclo = min(gdd_total / gdd_ciclo * 100, 999) if gdd_ciclo else 0

    # KPIs agronômicos
    agro_kpis = [
        ("🌱", "GDD acumulado", f"{gdd_total:.0f}", f"°C·dia ({cultura_ref})"),
        ("📈", "Equiv. ciclo", f"{pct_ciclo:.0f}", f"% de {gdd_ciclo} °C·dia"),
        ("💧", "Balanço hídrico", f"{balanco_total:+.0f}", "mm (chuva − ET0)"),
        ("🔥", "Dias ≥34 °C", f"{dias_estresse}", "estresse térmico"),
        ("🏜️", "Maior veranico", f"{veranico}", "dias secos seguidos"),
    ]
    cols_a = st.columns(5)
    for col, (icon, label, value, unit) in zip(cols_a, agro_kpis):
        col.markdown(f"""
        <div style="background:#0f2040;border:1px solid #1a3a6e;border-radius:12px;padding:12px 10px;text-align:center;">
          <div style="font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;color:#7ba3c8;margin-bottom:4px;">{icon} {label}</div>
          <div style="font-family:'Space Mono',monospace;font-size:1.15rem;font-weight:700;color:#00ff9d;line-height:1.1;">{value}</div>
          <div style="font-size:.62rem;color:#7ba3c8;margin-top:2px;">{unit}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_g, col_b = st.columns(2)
    with col_g:
        st.markdown('<div class="section-title">Graus-dia acumulados (GDD)</div>', unsafe_allow_html=True)
        fig_g = go.Figure()
        fig_g.add_trace(go.Scatter(x=gdd_acum.index, y=gdd_acum.values, name="GDD acumulado",
            line=dict(color=CULTURAS[cultura_ref]["cor"], width=2.5),
            fill="tozeroy", fillcolor="rgba(0,255,157,0.08)", mode="lines"))
        fig_g.add_hline(y=gdd_ciclo, line_dash="dash", line_color="#ffd166",
            annotation_text=f"Ciclo {cultura_ref} (~{gdd_ciclo})", annotation_font_color="#ffd166",
            annotation_font_size=10)
        fig_g.update_layout(**LAYOUT_BASE, height=320, legend=_LEGEND,
            yaxis={**_YAXIS, "title":"°C·dia"},
            title=dict(text=f"Acúmulo térmico · Tbase {t_base:.0f} °C", font=dict(color="#7ba3c8", size=13)))
        st.plotly_chart(fig_g, width="stretch")
        st.caption("GDD prevê em que fase a cultura está e quando deve florescer/maturar. "
                   "Quando a linha cruza o tracejado, o ciclo térmico teórico se completou.")

    with col_b:
        st.markdown('<div class="section-title">Balanço hídrico acumulado</div>', unsafe_allow_html=True)
        cor_area = ["#00ff9d" if v >= 0 else "#ff6b6b" for v in balanco_acum.values]
        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(x=balanco_acum.index, y=balanco_acum.values,
            name="Balanço (mm)", line=dict(color="#00e5ff", width=2.5),
            fill="tozeroy", fillcolor="rgba(0,229,255,0.08)", mode="lines"))
        fig_b.add_hline(y=0, line_color="#7ba3c8", line_width=1)
        fig_b.update_layout(**LAYOUT_BASE, height=320, legend=_LEGEND,
            yaxis={**_YAXIS, "title":"mm"},
            title=dict(text="Chuva − evapotranspiração (ET0)", font=dict(color="#7ba3c8", size=13)))
        st.plotly_chart(fig_b, width="stretch")
        st.caption("Acima de zero, sobra água no sistema; abaixo, há déficit e a planta "
                   "depende de reserva no solo ou irrigação.")

    # Resumo interpretativo
    st.markdown('<div class="section-title">Leitura rápida</div>', unsafe_allow_html=True)
    leitura = []
    if pct_ciclo >= 100:
        leitura.append(f"O acúmulo térmico do período ({gdd_total:.0f} °C·dia) já cobre o "
                       f"ciclo de referência da {cultura_ref}.")
    else:
        leitura.append(f"O período acumulou {gdd_total:.0f} °C·dia — cerca de {pct_ciclo:.0f}% "
                       f"do ciclo térmico da {cultura_ref}.")
    if balanco_total >= 0:
        leitura.append(f"O balanço hídrico fechou positivo ({balanco_total:+.0f} mm): houve mais "
                       f"chuva do que demanda evaporativa.")
    else:
        leitura.append(f"O balanço hídrico fechou negativo ({balanco_total:+.0f} mm): a demanda "
                       f"evaporativa superou a chuva, sinal de estresse hídrico.")
    if veranico >= 10:
        leitura.append(f"Houve um veranico de {veranico} dias seguidos sem chuva relevante — "
                       f"risco se tivesse coincidido com floração.")
    if dias_estresse > 0:
        leitura.append(f"{dias_estresse} dia(s) com máxima ≥34 °C, faixa de estresse térmico para grãos.")
    st.markdown(
        "<div style='background:#0f2040;border:1px solid #1a3a6e;border-radius:12px;padding:16px 20px;"
        "color:#e8f4fd;font-size:.9rem;line-height:1.7;'>• " + "<br>• ".join(leitura) + "</div>",
        unsafe_allow_html=True)

    st.caption("Tbase e GDD de ciclo são valores de referência; ajuste à cultivar específica. "
               "ET0 é a evapotranspiração de referência (FAO Penman-Monteith) fornecida pela API.")
