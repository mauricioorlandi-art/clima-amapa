import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

# ── Configuração da página ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clima Amapá",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilo ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');
:root{
  --bg:#0a1628; --surface:#0f2040; --surface2:#13284c;
  --line:#1e3a64; --line-soft:#16305a;
  --accent:#00e5ff; --text:#e8f4fd; --muted:#7ba3c8; --faint:#4d6b94;
  --temp-max:#ff6b6b; --temp-min:#38bdf8; --temp-mean:#ffd166;
  --precip:#00e5ff; --humidity:#a78bfa; --wind:#fb923c; --crop:#2dd4a7;
}
html,body,[data-testid="stAppViewContainer"]{
  background:radial-gradient(1100px 460px at 18% -8%, rgba(0,229,255,.07), transparent 60%),
             radial-gradient(900px 500px at 100% 0%, rgba(167,139,250,.05), transparent 55%),
             var(--bg)!important;
  color:var(--text)!important; font-family:'DM Sans',sans-serif;
}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0a1f3d,#071530)!important;border-right:1px solid var(--line);}
[data-testid="stSidebar"] *{color:var(--text)!important;}
[data-testid="stSidebar"] hr{border-color:var(--line-soft)!important;margin:14px 0!important;}
h1,h2,h3{font-family:'Space Mono',monospace!important;letter-spacing:-.01em;}
[data-testid="stSelectbox"]>div>div,[data-testid="stDateInput"]>div>div{
  background:var(--surface2)!important;border:1px solid var(--line)!important;color:var(--text)!important;border-radius:8px!important;}

/* Sidebar: rótulos em versalete monoespaçado */
.side-label{font-family:'Space Mono',monospace;font-size:.66rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);margin:2px 0 6px;}
.side-brand{font-family:'Space Mono',monospace;font-weight:700;font-size:1.05rem;letter-spacing:.04em;color:var(--text);}
.side-brand small{display:block;font-weight:400;font-size:.62rem;letter-spacing:.22em;color:var(--faint);margin-top:3px;}

/* Hero */
.hero{padding:30px 36px 26px;border:1px solid var(--line);border-radius:18px;margin-bottom:24px;
  background:linear-gradient(135deg,rgba(15,32,64,.9),rgba(19,40,76,.6));position:relative;overflow:hidden;}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent 70%,rgba(0,229,255,.05));pointer-events:none;}
.hero-eyebrow{font-family:'Space Mono',monospace;font-size:.68rem;letter-spacing:.32em;text-transform:uppercase;color:var(--accent);}
.hero-title{font-family:'Space Mono',monospace;font-weight:700;font-size:2.5rem;line-height:1;color:var(--text);margin:10px 0 14px;}
.hero-rule{height:1px;background:linear-gradient(90deg,var(--accent),transparent 40%);margin-bottom:12px;}
.hero-meta{font-family:'Space Mono',monospace;font-size:.82rem;color:var(--muted);letter-spacing:.02em;}
.hero-meta b{color:var(--text);font-weight:700;}

/* Eyebrow de seção */
.section-title{font-family:'Space Mono',monospace;font-size:.72rem;text-transform:uppercase;letter-spacing:.2em;
  color:var(--muted);margin:6px 0 14px;border-left:2px solid var(--accent);padding-left:11px;}

/* Abas */
.stTabs [data-baseweb="tab-list"]{gap:4px;background:transparent;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{background:transparent;border:none;color:var(--faint);
  font-family:'Space Mono',monospace;font-size:.74rem;letter-spacing:.16em;padding:10px 18px;}
.stTabs [aria-selected="true"]{color:var(--accent)!important;border-bottom:2px solid var(--accent)!important;}

/* Cartão KPI */
.kpi{background:var(--surface);border:1px solid var(--line);border-top-width:3px;border-radius:13px;
  padding:15px 14px 13px;transition:border-color .18s,transform .18s;height:100%;}
.kpi:hover{border-color:#2e5fa0;transform:translateY(-2px);}
.kpi-label{font-family:'Space Mono',monospace;font-size:.62rem;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);}
.kpi-value{font-family:'Space Mono',monospace;font-weight:700;font-size:1.5rem;line-height:1.15;color:var(--text);margin-top:7px;}
.kpi-unit{font-size:.66rem;color:var(--faint);margin-top:1px;}

/* Cartão de previsão diária */
.fc{background:var(--surface);border:1px solid var(--line);border-radius:13px;padding:13px 8px 11px;
  text-align:center;transition:border-color .18s,transform .18s;}
.fc:hover{border-color:#2e5fa0;transform:translateY(-2px);}
.fc-date{font-family:'Space Mono',monospace;font-size:.66rem;letter-spacing:.06em;color:var(--muted);}
.fc-ico{height:34px;display:flex;align-items:center;justify-content:center;margin:8px 0 6px;}
.fc-tmax{font-family:'Space Mono',monospace;font-weight:700;font-size:1.05rem;color:var(--temp-max);}
.fc-tmin{font-family:'Space Mono',monospace;font-size:.84rem;color:var(--temp-min);}
.fc-meta{font-size:.6rem;color:var(--faint);margin-top:5px;line-height:1.5;}
.fc-meta b{color:var(--muted);font-weight:600;}

/* Alertas */
.alert{background:var(--surface);border:1px solid var(--line);border-left-width:3px;border-radius:11px;
  padding:13px 16px;margin-bottom:9px;}
.alert-head{display:flex;align-items:center;gap:9px;}
.alert-dot{width:7px;height:7px;border-radius:50%;display:inline-block;}
.alert-title{font-family:'Space Mono',monospace;font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;}
.alert-text{color:var(--text);font-size:.86rem;margin-top:6px;line-height:1.55;}

/* Cartão de cultura */
.crop-card{background:var(--surface);border:1px solid var(--line);border-radius:13px;padding:15px 17px;height:100%;}
.crop-head{display:flex;align-items:center;gap:9px;font-family:'Space Mono',monospace;font-weight:700;font-size:.92rem;color:var(--text);}
.crop-dot{width:9px;height:9px;border-radius:2px;}
.crop-body{color:var(--muted);font-size:.8rem;margin-top:9px;line-height:1.6;}

/* Painel de leitura */
.read{background:var(--surface);border:1px solid var(--line);border-radius:13px;padding:18px 22px;
  color:var(--text);font-size:.9rem;line-height:1.75;}
.read b{color:var(--accent);}

.note{color:var(--faint);font-size:.74rem;line-height:1.5;}
@media (prefers-reduced-motion:reduce){*{transition:none!important;}}
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
    "temp_max":"#ff6b6b","temp_min":"#38bdf8","temp_mean":"#ffd166",
    "precipitation":"#00e5ff","humidity":"#a78bfa","wind":"#fb923c","crop":"#2dd4a7",
}
MESES_PT = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
            7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

# Códigos de tempo WMO → grupo de ícone
WMO_GRUPO = {
    0:"sol", 1:"sol", 2:"parcial", 3:"nuvem", 45:"nevoa", 48:"nevoa",
    51:"garoa", 53:"garoa", 55:"garoa", 56:"garoa", 57:"garoa",
    61:"chuva", 63:"chuva", 65:"forte", 66:"chuva", 67:"forte",
    71:"neve", 73:"neve", 75:"neve", 77:"neve",
    80:"garoa", 81:"chuva", 82:"forte", 85:"neve", 86:"neve",
    95:"tempestade", 96:"tempestade", 99:"tempestade",
}
WMO_DESC = {
    "sol":"Céu limpo","parcial":"Parcialmente nublado","nuvem":"Nublado","nevoa":"Névoa",
    "garoa":"Garoa","chuva":"Chuva","forte":"Chuva forte","neve":"Neve","tempestade":"Trovoada",
}

# Parâmetros agronômicos (valores de referência — ajuste à cultivar local)
CULTURAS = {
    "Soja":  {"t_base": 10.0, "gdd_ciclo": 1400, "cor": "#2dd4a7"},
    "Milho": {"t_base": 10.0, "gdd_ciclo": 1500, "cor": "#ffd166"},
}

# Sistema de sucessão. Cada fase é (rótulo, dia_inicial, dia_final) em DIAS A PARTIR
# do plantio da soja (dia 0 = início das chuvas, detectado por cidade). As durações
# de ciclo são típicas; o que se adapta à cidade é a data-âncora (onset das chuvas).
ANO_BASE = 2024
SISTEMA = {
    "Soja": {
        "cor": "#2dd4a7",
        "fases": [("Plantio", 0, 35), ("Ciclo", 0, 118), ("Colheita", 108, 135)],
    },
    "Milho safrinha": {
        "cor": "#ffd166",
        "fases": [("Plantio", 128, 158), ("Ciclo", 128, 260), ("Colheita", 250, 282)],
    },
    "Brachiaria ruziziensis": {
        "cor": "#b5cc6a",
        "fases": [("Consórcio com o milho", 128, 282), ("Palhada / pasto", 282, 352)],
    },
}
ORDEM_ATIVIDADES = [f"{c} · {f[0]}" for c, info in SISTEMA.items() for f in info["fases"]]

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e8f4fd", family="DM Sans", size=12),
    xaxis=dict(gridcolor="#16305a", linecolor="#1e3a64", zerolinecolor="#16305a"),
    margin=dict(l=10,r=10,t=44,b=10), hovermode="x unified",
)
_YAXIS  = dict(gridcolor="#16305a", linecolor="#1e3a64", zerolinecolor="#16305a")
_LEGEND = dict(bgcolor="rgba(10,31,61,0.75)", bordercolor="#1e3a64", borderwidth=1,
               font=dict(size=11))
_YAXIS2 = dict(overlaying="y", side="right", showgrid=False,
               gridcolor="rgba(0,0,0,0)", color="#e8f4fd")
_TITLE  = lambda t: dict(text=t, font=dict(color="#7ba3c8", size=12.5))


# ── Ícones de tempo (SVG de traço) ──────────────────────────────────────────────
def icone_tempo(grupo):
    s = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    sol = '<g stroke="#ffd166"><circle cx="12" cy="12" r="3.6"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M18.4 5.6L17 7M7 17l-1.4 1.4"/></g>'
    nuvem = lambda c: f'<path stroke="{c}" d="M7 17.5h9.5a3.2 3.2 0 0 0 .3-6.4 4.7 4.7 0 0 0-9-1.3A3.4 3.4 0 0 0 7 17.5z"/>'
    if grupo == "sol":
        return s + sol + "</svg>"
    if grupo == "parcial":
        return (s + '<g stroke="#ffd166"><circle cx="8" cy="8" r="2.7"/>'
                '<path d="M8 2.6v1.4M2.6 8h1.4M4.4 4.4l1 1M11.6 4.4l-1 1"/></g>'
                + nuvem("#7ba3c8") + "</svg>")
    if grupo in ("nuvem", "nevoa"):
        extra = '<path stroke="#4d6b94" d="M6 20.5h7M9 23h6"/>' if grupo == "nevoa" else ""
        return s + nuvem("#7ba3c8") + extra + "</svg>"
    if grupo == "garoa":
        return s + nuvem("#7ba3c8") + '<g stroke="#00e5ff"><path d="M9 20v1.4M13 20v1.4M11 21.4v1.4"/></g>' + "</svg>"
    if grupo == "chuva":
        return s + nuvem("#7ba3c8") + '<g stroke="#00e5ff"><path d="M9 19.5l-.8 2.2M12.5 19.5l-.8 2.2M16 19.5l-.8 2.2"/></g>' + "</svg>"
    if grupo == "forte":
        return s + nuvem("#7ba3c8") + '<g stroke="#38bdf8"><path d="M8.5 19l-1.2 3M12 19l-1.2 3M15.5 19l-1.2 3"/></g>' + "</svg>"
    if grupo == "neve":
        return s + nuvem("#7ba3c8") + '<g stroke="#cfe8ff"><path d="M9 21h0M12 21.6h0M15 21h0"/></g>' + "</svg>"
    if grupo == "tempestade":
        return s + nuvem("#7ba3c8") + '<path stroke="#ffd166" d="M12.5 18.5l-2 3h2.4l-1.4 2.5"/>' + "</svg>"
    return s + nuvem("#7ba3c8") + "</svg>"


# ── API ────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def buscar_clima(lat, lon, inicio, fim):
    """Histórico diário (Open-Meteo Archive). Inclui ET0 para o balanço hídrico."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": str(inicio), "end_date": str(fim),
        "daily": ("temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
                  "precipitation_sum,windspeed_10m_max,"
                  "relative_humidity_2m_max,relative_humidity_2m_min,"
                  "et0_fao_evapotranspiration"),
        "timezone": "America/Belem",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["daily"])
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df = df.rename(columns={
        "temperature_2m_max":"temp_max", "temperature_2m_min":"temp_min",
        "temperature_2m_mean":"temp_mean", "precipitation_sum":"precipitation",
        "windspeed_10m_max":"wind", "et0_fao_evapotranspiration":"et0",
    })
    df["humidity"] = (df["relative_humidity_2m_max"] + df["relative_humidity_2m_min"]) / 2
    df = df.drop(columns=["relative_humidity_2m_max", "relative_humidity_2m_min"])
    return df


@st.cache_data(ttl=1800, show_spinner=False)
def buscar_previsao(lat, lon, dias=16):
    """Previsão diária (Open-Meteo Forecast). Mesmas colunas do histórico + extras."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "daily": ("temperature_2m_max,temperature_2m_min,precipitation_sum,"
                  "precipitation_probability_max,windspeed_10m_max,"
                  "et0_fao_evapotranspiration,weathercode"),
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
        "temperature_2m_max":"temp_max", "temperature_2m_min":"temp_min",
        "precipitation_sum":"precipitation", "precipitation_probability_max":"precip_prob",
        "windspeed_10m_max":"wind", "et0_fao_evapotranspiration":"et0", "weathercode":"wcode",
    })
    df["temp_mean"] = (df["temp_max"] + df["temp_min"]) / 2
    h = pd.DataFrame(j["hourly"])
    h["time"] = pd.to_datetime(h["time"])
    h.set_index("time", inplace=True)
    df["humidity"] = h["relative_humidity_2m"].resample("D").mean().reindex(df.index)
    return df


def agregar(df, agg):
    regra = {"Semanal":"W", "Mensal":"ME"}.get(agg)
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


# ── Indicadores agronômicos ──────────────────────────────────────────────────────
def calcular_gdd(df, t_base):
    """Graus-dia diários: max(0, Tmédia - Tbase)."""
    tmean = (df["temp_max"] + df["temp_min"]) / 2
    return (tmean - t_base).clip(lower=0)


def maior_veranico(precip, limiar=1.0):
    """Maior sequência de dias consecutivos com chuva abaixo do limiar (mm)."""
    melhor = atual = 0
    for seco in (precip < limiar):
        atual = atual + 1 if seco else 0
        melhor = max(melhor, atual)
    return melhor


def fase_para_segmentos(mes_ini, dia_ini, mes_fim, dia_fim):
    """Janela (mês/dia)→(mês/dia) em segmentos de data no ANO_BASE, dividindo
    automaticamente quando a fase cruza a virada do ano."""
    ini = date(ANO_BASE, mes_ini, dia_ini)
    fim = date(ANO_BASE, mes_fim, dia_fim)
    if fim >= ini:
        return [(ini, fim)]
    return [(ini, date(ANO_BASE, 12, 31)), (date(ANO_BASE, 1, 1), fim)]


def doy_para_data(doy):
    """Dia do ano (cíclico) → Timestamp dentro do ANO_BASE."""
    doy = ((int(doy) - 1) % 365) + 1
    return pd.Timestamp(date(ANO_BASE, 1, 1)) + pd.Timedelta(days=doy - 1)


def fase_doy_segmentos(onset_doy, ini_off, fim_off):
    """Converte uma fase definida em dias a partir do plantio (onset) em segmentos
    de data no calendário anual, dividindo na virada do ano quando necessário."""
    ini, fim = onset_doy + ini_off, onset_doy + fim_off
    if (ini - 1) // 365 == (fim - 1) // 365:
        return [(doy_para_data(ini), doy_para_data(fim) + pd.Timedelta(days=1))]
    return [
        (doy_para_data(ini), pd.Timestamp(date(ANO_BASE, 12, 31)) + pd.Timedelta(days=1)),
        (pd.Timestamp(date(ANO_BASE, 1, 1)), doy_para_data(fim) + pd.Timedelta(days=1)),
    ]


def maior_periodo_umido(umido):
    """Maior sequência cíclica de meses úmidos. Retorna (n_meses, ini_idx, fim_idx, regime)."""
    n = 12
    if all(umido):
        return (12, None, None, "umido")
    if not any(umido):
        return (0, None, None, "seco")
    melhor = (0, 0, 0)
    for start in range(n):
        if umido[start] and not umido[(start - 1) % n]:
            length, m = 0, start
            while umido[m % n] and length < n:
                length += 1; m += 1
            if length > melhor[0]:
                melhor = (length, start, (start + length - 1) % n)
    return (melhor[0], melhor[1], melhor[2], "sazonal")


def trimestre_mais_chuvoso(precip_mes):
    """Mês inicial do trimestre (janela móvel de 3 meses) com maior chuva."""
    melhor = (-1, 1)
    for m in range(1, 13):
        soma = sum((precip_mes.get(((m - 1 + k) % 12) + 1) or 0) for k in range(3))
        if soma > melhor[0]:
            melhor = (soma, m)
    return melhor[1]


def detectar_estacao(precip_mes, limiar):
    """Detecta início/fim da estação chuvosa a partir da climatologia mensal de chuva."""
    umido = [bool((precip_mes.get(m) or 0) >= limiar) for m in range(1, 13)]
    length, si, ei, regime = maior_periodo_umido(umido)
    if regime == "umido":
        onset = trimestre_mais_chuvoso(precip_mes)
        return {"onset": onset, "fim": ((onset + 10) % 12) + 1, "length": 12, "regime": "umido"}
    if regime == "seco":
        onset = max(range(1, 13), key=lambda m: (precip_mes.get(m) or 0))
        return {"onset": onset, "fim": onset, "length": 1, "regime": "seco"}
    return {"onset": si + 1, "fim": ei + 1, "length": length, "regime": "sazonal"}


def cartao_kpi(col, label, valor, unidade, cor):
    col.markdown(f"""
    <div class="kpi" style="border-top-color:{cor};">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{valor}</div>
      <div class="kpi-unit">{unidade}</div>
    </div>""", unsafe_allow_html=True)


# ── Barra lateral ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="side-brand">CLIMA AMAPÁ<small>PAINEL CLIMÁTICO</small></div>',
                unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="side-label">Cidade</div>', unsafe_allow_html=True)
    cidade = st.selectbox("Cidade", list(CIDADES.keys()), label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div class="side-label">Período de análise</div>', unsafe_allow_html=True)
    DATA_MAX = date.today() - timedelta(days=7)
    c1, c2 = st.columns(2)
    with c1:
        data_inicio = st.date_input("Início", value=date(2023,1,1),
                                    min_value=date(1940,1,1), max_value=DATA_MAX)
    with c2:
        data_fim = st.date_input("Fim", value=DATA_MAX,
                                 min_value=date(1940,1,2), max_value=DATA_MAX)
    st.markdown("---")
    st.markdown('<div class="side-label">Comparar com outro ano</div>', unsafe_allow_html=True)
    comparar = st.checkbox("Ativar comparação")
    ano_comparacao = None
    if comparar:
        ano_comparacao = st.number_input("Ano de referência", min_value=1940,
                                         max_value=date.today().year - 1,
                                         value=date.today().year - 2)
    st.markdown("---")
    st.markdown('<div class="side-label">Agregação</div>', unsafe_allow_html=True)
    agregacao = st.selectbox("Agregação", ["Diário","Semanal","Mensal"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div class="side-label">Painel agronômico</div>', unsafe_allow_html=True)
    cultura_ref = st.selectbox("Cultura de referência (GDD)", list(CULTURAS.keys()))
    st.markdown('<div class="side-label" style="margin-top:10px;">Calendário agrícola</div>', unsafe_allow_html=True)
    limiar_chuva = st.slider("Mês chuvoso a partir de (mm)", 50, 200, 100, 10,
                             help="Limiar para o app considerar um mês dentro da estação chuvosa "
                                  "e ancorar o plantio. Detectado a partir da chuva da cidade selecionada.")
    st.markdown('<div class="side-label" style="margin-top:10px;">Previsão</div>', unsafe_allow_html=True)
    dias_previsao = st.select_slider("Horizonte (dias)", options=[7,10,14,16], value=14)
    st.markdown("---")
    st.markdown('<div class="note">Fonte: Open-Meteo Archive + Forecast API.<br>Sem necessidade de chave de API.</div>',
                unsafe_allow_html=True)

# ── Validação ──────────────────────────────────────────────────────────────────
if data_inicio >= data_fim:
    st.error("A data de início deve ser anterior à data de fim. Ajuste o período na barra lateral.")
    st.stop()

lat = CIDADES[cidade]["lat"]
lon = CIDADES[cidade]["lon"]

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">Painel climático · Amapá · Brasil</div>
  <div class="hero-title">CLIMA AMAPÁ</div>
  <div class="hero-rule"></div>
  <div class="hero-meta">
    <b>{cidade}</b> &nbsp;·&nbsp; {lat:.4f}°, {lon:.4f}° &nbsp;·&nbsp;
    {data_inicio.strftime('%d/%m/%Y')} → {data_fim.strftime('%d/%m/%Y')}
  </div>
</div>
""", unsafe_allow_html=True)

# ── Carrega dados ──────────────────────────────────────────────────────────────
with st.spinner("Carregando dados climáticos..."):
    try:
        df = buscar_clima(lat, lon, data_inicio, data_fim)
    except Exception as e:
        st.error(f"Não foi possível buscar os dados: {e}")
        st.stop()

df_agg = agregar(df, agregacao)

tab_hist, tab_prev, tab_cal, tab_agro = st.tabs([
    "HISTÓRICO", "PREVISÃO", "CALENDÁRIO AGRÍCOLA", "PAINEL AGRONÔMICO"
])

# ════════════════════════════════════════════════════════════════════ HISTÓRICO ═
with tab_hist:
    st.markdown('<div class="section-title">Resumo do período</div>', unsafe_allow_html=True)
    kpis = [
        ("Temp. média",   f"{df['temp_mean'].mean():.1f}", "°C",   CORES["temp_mean"]),
        ("Máx. absoluta", f"{df['temp_max'].max():.1f}",  "°C",   CORES["temp_max"]),
        ("Mín. absoluta", f"{df['temp_min'].min():.1f}",  "°C",   CORES["temp_min"]),
        ("Precip. total", f"{df['precipitation'].sum():.0f}", "mm", CORES["precipitation"]),
        ("Umidade média", f"{df['humidity'].mean():.0f}", "%",    CORES["humidity"]),
        ("Vento máx.",    f"{df['wind'].max():.0f}",      "km/h", CORES["wind"]),
    ]
    for col, (lb, vl, un, cor) in zip(st.columns(6), kpis):
        cartao_kpi(col, lb, vl, un, cor)
    st.markdown("<br>", unsafe_allow_html=True)

    # Temperatura
    st.markdown('<div class="section-title">Temperatura</div>', unsafe_allow_html=True)
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=df_agg.index, y=df_agg["temp_max"], name="Máxima",
        line=dict(color=CORES["temp_max"], width=1.5), mode="lines"))
    fig_temp.add_trace(go.Scatter(x=df_agg.index, y=df_agg["temp_min"], name="Mínima",
        line=dict(color=CORES["temp_min"], width=1.5),
        fill="tonexty", fillcolor="rgba(56,189,248,0.07)", mode="lines"))
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
            idx_deslocado = df_cmp_agg.index + (df_agg.index[0] - df_cmp_agg.index[0])
            fig_temp.add_trace(go.Scatter(x=idx_deslocado, y=df_cmp_agg["temp_mean"],
                name=f"Média {int(ano_comparacao)}",
                line=dict(color="#a78bfa", width=1.5, dash="dash"), mode="lines", opacity=0.75))
        except Exception as ex:
            st.warning(f"Não foi possível carregar dados de {int(ano_comparacao)}: {ex}")
    fig_temp.update_layout(**LAYOUT_BASE, height=320, yaxis={**_YAXIS,"title":"°C"},
        legend=_LEGEND, title=_TITLE("Temperatura (°C)"))
    st.plotly_chart(fig_temp, width="stretch")

    # Precipitação + Umidade
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Precipitação</div>', unsafe_allow_html=True)
        rotulo = "diária" if agregacao == "Diário" else "acumulada"
        fig_chuva = go.Figure()
        fig_chuva.add_trace(go.Bar(x=df_agg.index, y=df_agg["precipitation"], name="Chuva",
            marker_color=CORES["precipitation"], opacity=0.85, marker_line_width=0))
        fig_chuva.update_layout(**LAYOUT_BASE, height=280, yaxis={**_YAXIS,"title":"mm"},
            legend=_LEGEND, title=_TITLE(f"Precipitação {rotulo} (mm)"))
        st.plotly_chart(fig_chuva, width="stretch")
    with col_b:
        st.markdown('<div class="section-title">Umidade relativa</div>', unsafe_allow_html=True)
        fig_umid = go.Figure()
        fig_umid.add_trace(go.Scatter(x=df_agg.index, y=df_agg["humidity"], name="Umidade",
            line=dict(color=CORES["humidity"], width=2),
            fill="tozeroy", fillcolor="rgba(167,139,250,0.1)", mode="lines"))
        fig_umid.update_layout(**LAYOUT_BASE, height=280,
            yaxis={**_YAXIS,"title":"%","range":[0,105]}, legend=_LEGEND,
            title=_TITLE("Umidade relativa média (%)"))
        st.plotly_chart(fig_umid, width="stretch")

    # Chuva × Umidade
    st.markdown('<div class="section-title">Chuva × umidade</div>', unsafe_allow_html=True)
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(x=df_agg.index, y=df_agg["precipitation"], name="Precipitação (mm)",
        yaxis="y2", marker_color="rgba(0,229,255,0.4)", marker_line_width=0, opacity=0.8))
    fig_comp.add_trace(go.Scatter(x=df_agg.index, y=df_agg["humidity"], name="Umidade (%)",
        line=dict(color=CORES["humidity"], width=2.5),
        fill="tozeroy", fillcolor="rgba(167,139,250,0.08)", mode="lines"))
    fig_comp.update_layout(**LAYOUT_BASE, height=340, title=_TITLE("Relação entre chuva e umidade do ar"),
        yaxis={**_YAXIS,"title":"Umidade (%)","range":[0,105]},
        yaxis2={**_YAXIS2,"title":"Precipitação (mm)"}, legend=_LEGEND)
    st.plotly_chart(fig_comp, width="stretch")

    # Vento
    st.markdown('<div class="section-title">Velocidade do vento</div>', unsafe_allow_html=True)
    fig_vento = go.Figure()
    fig_vento.add_trace(go.Scatter(x=df_agg.index, y=df_agg["wind"], name="Vento máx.",
        line=dict(color=CORES["wind"], width=1.5),
        fill="tozeroy", fillcolor="rgba(251,146,60,0.08)", mode="lines"))
    fig_vento.update_layout(**LAYOUT_BASE, height=240, yaxis={**_YAXIS,"title":"km/h"},
        legend=_LEGEND, title=_TITLE("Velocidade máxima do vento (km/h)"))
    st.plotly_chart(fig_vento, width="stretch")

    # Climatologia mensal
    st.markdown('<div class="section-title">Climatologia mensal — período completo</div>', unsafe_allow_html=True)
    df_m = df.copy(); df_m["mes"] = df_m.index.month
    clim = df_m.groupby("mes").agg(
        temp_max=("temp_max","mean"), temp_min=("temp_min","mean"),
        temp_mean=("temp_mean","mean"), precipitation=("precipitation","sum"),
    ).reset_index()
    clim["nome_mes"] = clim["mes"].map(MESES_PT)
    fig_clim = go.Figure()
    fig_clim.add_trace(go.Bar(x=clim["nome_mes"], y=clim["precipitation"], name="Precipitação (mm)",
        yaxis="y2", marker_color="rgba(0,229,255,0.32)", marker_line_width=0))
    for col, rotulo, cor in [("temp_max","Temp. máxima",CORES["temp_max"]),
                             ("temp_mean","Temp. média",CORES["temp_mean"]),
                             ("temp_min","Temp. mínima",CORES["temp_min"])]:
        fig_clim.add_trace(go.Scatter(x=clim["nome_mes"], y=clim[col], name=rotulo,
            line=dict(color=cor, width=2), mode="lines+markers", marker=dict(size=6)))
    fig_clim.update_layout(**LAYOUT_BASE, height=340, title=_TITLE("Temperatura média e precipitação por mês"),
        yaxis={**_YAXIS,"title":"°C"}, yaxis2={**_YAXIS2,"title":"mm"}, legend=_LEGEND)
    st.plotly_chart(fig_clim, width="stretch")

    with st.expander("Ver dados brutos"):
        df_exibir = df.copy().round(2)
        df_exibir.index = df_exibir.index.strftime("%d/%m/%Y")
        df_exibir.index.name = "Data"
        ordem = ["temp_max","temp_min","temp_mean","precipitation","wind","humidity","et0"]
        df_exibir = df_exibir[[c for c in ordem if c in df_exibir.columns]]
        df_exibir.columns = ["Temp. máx. (°C)","Temp. mín. (°C)","Temp. média (°C)",
            "Precipitação (mm)","Vento máx. (km/h)","Umidade média (%)","ET0 (mm)"][:len(df_exibir.columns)]
        fmt = {c:"{:.2f}" for c in df_exibir.columns}
        st.dataframe(df_exibir.style.format(fmt).background_gradient(cmap="Blues",
            subset=["Precipitação (mm)"]), width="stretch")

# ═════════════════════════════════════════════════════════════════════ PREVISÃO ═
with tab_prev:
    st.markdown(f'<div class="section-title">Próximos {dias_previsao} dias · {cidade}</div>',
                unsafe_allow_html=True)
    try:
        fc = buscar_previsao(lat, lon, dias_previsao)
    except Exception as e:
        st.error(f"Não foi possível obter a previsão: {e}")
        fc = None

    if fc is not None and not fc.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        n = min(len(fc), 8)
        for col, (idx, row) in zip(st.columns(n), fc.head(n).iterrows()):
            grupo = WMO_GRUPO.get(int(row.get("wcode", 0)), "nuvem")
            prob = row.get("precip_prob")
            prob_txt = f"{int(prob)}%" if pd.notna(prob) else "—"
            col.markdown(f"""
            <div class="fc">
              <div class="fc-date">{MESES_PT[idx.month]} {idx.day:02d}</div>
              <div class="fc-ico">{icone_tempo(grupo)}</div>
              <div class="fc-tmax">{row['temp_max']:.0f}°</div>
              <div class="fc-tmin">{row['temp_min']:.0f}°</div>
              <div class="fc-meta"><b>chuva</b> {prob_txt}<br><b>vento</b> {row['wind']:.0f} km/h</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-title">Temperatura e chuva previstas</div>', unsafe_allow_html=True)
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Bar(x=fc.index, y=fc["precipitation"], name="Chuva (mm)", yaxis="y2",
            marker_color="rgba(0,229,255,0.45)", marker_line_width=0))
        fig_fc.add_trace(go.Scatter(x=fc.index, y=fc["temp_max"], name="Máxima",
            line=dict(color=CORES["temp_max"], width=2), mode="lines+markers"))
        fig_fc.add_trace(go.Scatter(x=fc.index, y=fc["temp_min"], name="Mínima",
            line=dict(color=CORES["temp_min"], width=2), mode="lines+markers",
            fill="tonexty", fillcolor="rgba(56,189,248,0.06)"))
        fig_fc.update_layout(**LAYOUT_BASE, height=340, legend=_LEGEND, title=_TITLE("Previsão diária"),
            yaxis={**_YAXIS,"title":"°C"}, yaxis2={**_YAXIS2,"title":"mm"})
        st.plotly_chart(fig_fc, width="stretch")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">Vento previsto</div>', unsafe_allow_html=True)
            fig_w = go.Figure()
            fig_w.add_trace(go.Scatter(x=fc.index, y=fc["wind"], name="Vento máx.",
                line=dict(color=CORES["wind"], width=2), mode="lines+markers",
                fill="tozeroy", fillcolor="rgba(251,146,60,0.08)"))
            fig_w.add_hline(y=10, line_dash="dash", line_color="#ff6b6b",
                annotation_text="Limite p/ pulverização (~10 km/h)",
                annotation_font_color="#ff6b6b", annotation_font_size=10)
            fig_w.update_layout(**LAYOUT_BASE, height=260, legend=_LEGEND,
                yaxis={**_YAXIS,"title":"km/h"}, title=_TITLE("Velocidade máx. do vento"))
            st.plotly_chart(fig_w, width="stretch")
        with col2:
            st.markdown('<div class="section-title">Probabilidade de chuva</div>', unsafe_allow_html=True)
            fig_p = go.Figure()
            fig_p.add_trace(go.Bar(x=fc.index, y=fc.get("precip_prob"), name="Prob. (%)",
                marker_color="rgba(0,229,255,0.5)", marker_line_width=0))
            fig_p.update_layout(**LAYOUT_BASE, height=260, legend=_LEGEND,
                yaxis={**_YAXIS,"title":"%","range":[0,105]}, title=_TITLE("Chance de precipitação"))
            st.plotly_chart(fig_p, width="stretch")

        st.markdown('<div class="section-title">Alertas operacionais</div>', unsafe_allow_html=True)
        chuva_prev = fc["precipitation"].sum()
        et0_prev = fc["et0"].sum() if "et0" in fc.columns else 0.0
        balanco = chuva_prev - et0_prev
        bons = fc[(fc["precipitation"] < 1.0) & (fc["wind"] < 12)]
        chuva_forte = fc[fc["precipitation"] >= 20]
        estresse = fc[fc["temp_max"] >= 34]
        fmt_dias = lambda d: ", ".join(f"{MESES_PT[i.month]} {i.day:02d}" for i in d)

        alertas = []
        if not bons.empty:
            alertas.append(("#2dd4a7","Janela de pulverização",
                f"Dias com pouca chuva e vento moderado: {fmt_dias(bons.index[:6])}."))
        else:
            alertas.append(("#fb923c","Pulverização limitada",
                "Poucos dias com condições ideais de chuva e vento no horizonte previsto."))
        if not chuva_forte.empty:
            alertas.append(("#00e5ff","Chuva forte prevista",
                f"Volumes ≥ 20 mm em {fmt_dias(chuva_forte.index)}. Atenção a operações de campo e drenagem."))
        if not estresse.empty:
            alertas.append(("#ff6b6b","Risco de estresse térmico",
                f"Máxima ≥ 34 °C em {fmt_dias(estresse.index)}. Crítico se coincidir com o florescimento."))
        cor_bal = "#2dd4a7" if balanco >= 0 else "#ff6b6b"
        sinal = "superávit" if balanco >= 0 else "déficit"
        alertas.append((cor_bal,"Balanço hídrico previsto",
            f"Chuva {chuva_prev:.0f} mm − ET0 {et0_prev:.0f} mm = <b>{balanco:+.0f} mm</b> ({sinal} no período)."))

        for cor, titulo, texto in alertas:
            st.markdown(f"""
            <div class="alert" style="border-left-color:{cor};">
              <div class="alert-head"><span class="alert-dot" style="background:{cor};"></span>
              <span class="alert-title" style="color:{cor};">{titulo}</span></div>
              <div class="alert-text">{texto}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="note" style="margin-top:8px;">Previsão de até 16 dias — quanto mais '
                    'distante o dia, maior a incerteza. Use os primeiros dias para decisões operacionais.</div>',
                    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════ CALENDÁRIO AGRÍCOLA ═
with tab_cal:
    st.markdown(f'<div class="section-title">Sucessão soja → milho safrinha + braquiária · '
                f'ajustado à chuva de {cidade}</div>', unsafe_allow_html=True)

    # Climatologia mensal de chuva da cidade (média do total mensal entre os anos do período)
    mensal = df["precipitation"].resample("ME").sum()
    precip_mes = mensal.groupby(mensal.index.month).mean().reindex(range(1, 13))
    meses_com_dado = int(precip_mes.notna().sum())

    est = detectar_estacao(precip_mes, limiar_chuva)
    onset_mes, fim_mes, regime = est["onset"], est["fim"], est["regime"]
    onset_doy = date(ANO_BASE, onset_mes, 1).timetuple().tm_yday

    def mes_do_offset(off):
        return MESES_PT[doy_para_data(onset_doy + off).month]

    # Monta as fases do sistema ancoradas no início das chuvas detectado
    linhas = []
    for comp, info in SISTEMA.items():
        for nome_fase, ini_off, fim_off in info["fases"]:
            for ini, fim in fase_doy_segmentos(onset_doy, ini_off, fim_off):
                linhas.append({"Atividade": f"{comp} · {nome_fase}", "Componente": comp,
                               "Início": ini, "Fim": fim})
    df_cal = pd.DataFrame(linhas)

    cores_comp = {c: info["cor"] for c, info in SISTEMA.items()}
    fig_cal = px.timeline(df_cal, x_start="Início", x_end="Fim", y="Atividade", color="Componente",
        color_discrete_map=cores_comp, category_orders={"Atividade": ORDEM_ATIVIDADES})
    fig_cal.update_yaxes(autorange="reversed", title=None, gridcolor="#16305a")
    fig_cal.update_xaxes(gridcolor="#16305a",
        range=[pd.Timestamp(ANO_BASE, 1, 1), pd.Timestamp(ANO_BASE, 12, 31)],
        tickvals=[pd.Timestamp(ANO_BASE, m, 1) for m in range(1, 13)],
        ticktext=[MESES_PT[m] for m in range(1, 13)])

    # Faixa sombreada = estação chuvosa detectada
    for ini_s, fim_s in fase_para_segmentos(onset_mes, 1, fim_mes, 28):
        fig_cal.add_vrect(x0=pd.Timestamp(ini_s), x1=pd.Timestamp(fim_s) + pd.Timedelta(days=1),
            fillcolor="rgba(0,229,255,0.06)", line_width=0, layer="below")

    hoje_base = pd.Timestamp(ANO_BASE, date.today().month, date.today().day)
    fig_cal.add_vline(x=hoje_base, line_color="#2dd4a7", line_width=2,
        annotation_text="hoje", annotation_font_color="#2dd4a7")
    fig_cal.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8f4fd", family="DM Sans", size=12), height=440,
        margin=dict(l=10, r=10, t=34, b=10), legend=_LEGEND,
        title=_TITLE("Faixa azul = estação chuvosa detectada · plantio ancorado no início das chuvas"))
    st.plotly_chart(fig_cal, width="stretch")

    # Parâmetros detectados (KPIs)
    dur_dias = est["length"] * 30
    kpis_cal = [
        ("Início das chuvas", MESES_PT[onset_mes], "plantio da soja", "#00e5ff"),
        ("Fim das chuvas",    MESES_PT[fim_mes],   "fim do período úmido", "#a78bfa"),
        ("Estação chuvosa",   f"{est['length']}",  "meses úmidos", "#2dd4a7"),
        ("Colheita da soja",  mes_do_offset(120),  "≈ 118 dias após plantio", "#2dd4a7"),
        ("Colheita do milho", mes_do_offset(270),  "safrinha consorciada", "#ffd166"),
    ]
    for col, (lb, vl, un, cor) in zip(st.columns(5), kpis_cal):
        cartao_kpi(col, lb, vl, un, cor)
    st.markdown("<br>", unsafe_allow_html=True)

    # Cartões do sistema (datas derivadas)
    resumo = {
        "Soja": ("#2dd4a7", f"Plantio no início das chuvas ({MESES_PT[onset_mes]}), ciclo de "
                            f"~118 dias, colheita por volta de {mes_do_offset(120)}. É a cultura que "
                            f"abre o sistema e paga a safra."),
        "Milho safrinha": ("#ffd166", f"Semeado logo após a soja (~{mes_do_offset(135)}) em consórcio "
                            f"com a braquiária; colheita do grão em torno de {mes_do_offset(270)}. "
                            f"Aproveita o fim das chuvas."),
        "Brachiaria ruziziensis": ("#b5cc6a", "Semeada junto com o milho, cresce à sombra dele e "
                            "assume após a colheita, formando palhada para plantio direto e pasto na "
                            "seca (integração lavoura-pecuária)."),
    }
    for col, (cult, (cor, txt)) in zip(st.columns(3), resumo.items()):
        col.markdown(f"""
        <div class="crop-card">
          <div class="crop-head"><span class="crop-dot" style="background:{cor};"></span>{cult}</div>
          <div class="crop-body">{txt}</div>
        </div>""", unsafe_allow_html=True)

    # Alertas adaptativos derivados do regime de chuva
    st.markdown('<div class="section-title" style="margin-top:18px;">Leitura do regime</div>',
                unsafe_allow_html=True)
    av = []
    if meses_com_dado < 12:
        av.append(("#fb923c", "Período curto para climatologia",
            f"O período selecionado cobre {meses_com_dado} de 12 meses. Para um calendário "
            f"confiável, selecione pelo menos 1–2 anos completos na barra lateral."))
    if regime == "umido":
        av.append(("#00e5ff", "Chuva o ano todo",
            "Todos os meses superam o limiar — janela de plantio flexível. O cuidado migra para "
            "doenças e para a colheita em período úmido; priorize cultivares resistentes."))
    elif regime == "seco":
        av.append(("#ff6b6b", "Chuva insuficiente para sequeiro",
            f"Nenhum mês atinge {limiar_chuva} mm com o limiar atual. O sistema em sequeiro é "
            f"arriscado nesta cidade — considere irrigação ou reduza o limiar para inspecionar."))
    else:
        if dur_dias >= 240:
            av.append(("#2dd4a7", "Janela favorável ao sistema completo",
                f"A estação chuvosa dura ~{est['length']} meses, suficiente para soja + milho "
                f"safrinha consorciado com braquiária com risco hídrico baixo."))
        elif dur_dias >= 150:
            av.append(("#fb923c", "Milho safrinha com risco no enchimento",
                f"A estação dura ~{est['length']} meses: o enchimento de grão do milho pode pegar o "
                f"fim das chuvas. A braquiária ajuda a segurar umidade e cobertura — favoreça "
                f"cultivares precoces e antecipe o plantio da soja."))
        else:
            av.append(("#ff6b6b", "Estação chuvosa curta",
                f"Com ~{est['length']} meses úmidos, sobra pouca janela após a soja. O milho "
                f"safrinha fica arriscado; a braquiária solo ainda funciona como cobertura/pasto."))
    for cor, titulo, texto in av:
        st.markdown(f"""
        <div class="alert" style="border-left-color:{cor};">
          <div class="alert-head"><span class="alert-dot" style="background:{cor};"></span>
          <span class="alert-title" style="color:{cor};">{titulo}</span></div>
          <div class="alert-text">{texto}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="note" style="margin-top:12px;">O início das chuvas é detectado pela '
                'climatologia de precipitação da cidade selecionada (ajuste o limiar na barra '
                'lateral). As durações de ciclo são típicas; confirme as datas no ZARC do município '
                'antes de plantar.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════ PAINEL AGRONÔMICO ═
with tab_agro:
    st.markdown(f'<div class="section-title">Indicadores · período selecionado · '
                f'referência: {cultura_ref}</div>', unsafe_allow_html=True)
    t_base = CULTURAS[cultura_ref]["t_base"]
    gdd_ciclo = CULTURAS[cultura_ref]["gdd_ciclo"]
    cor_cult = CULTURAS[cultura_ref]["cor"]

    gdd_acum = calcular_gdd(df, t_base).cumsum()
    gdd_total = float(gdd_acum.iloc[-1]) if len(gdd_acum) else 0.0
    balanco_acum = (df["precipitation"] - df["et0"]).cumsum() if "et0" in df.columns else df["precipitation"].cumsum()*0
    balanco_total = float(balanco_acum.iloc[-1]) if len(balanco_acum) else 0.0
    dias_estresse = int((df["temp_max"] >= 34).sum())
    veranico = maior_veranico(df["precipitation"])
    pct_ciclo = min(gdd_total / gdd_ciclo * 100, 999) if gdd_ciclo else 0

    agro_kpis = [
        ("GDD acumulado",  f"{gdd_total:.0f}",   f"°C·dia · {cultura_ref}", cor_cult),
        ("Equiv. ciclo",   f"{pct_ciclo:.0f}",   f"% de {gdd_ciclo} °C·dia", "#ffd166"),
        ("Balanço hídrico",f"{balanco_total:+.0f}", "mm · chuva − ET0",      "#00e5ff"),
        ("Dias ≥ 34 °C",   f"{dias_estresse}",   "estresse térmico",         "#ff6b6b"),
        ("Maior veranico", f"{veranico}",        "dias secos seguidos",      "#fb923c"),
    ]
    for col, (lb, vl, un, cor) in zip(st.columns(5), agro_kpis):
        cartao_kpi(col, lb, vl, un, cor)
    st.markdown("<br>", unsafe_allow_html=True)

    col_g, col_b = st.columns(2)
    with col_g:
        st.markdown('<div class="section-title">Graus-dia acumulados (GDD)</div>', unsafe_allow_html=True)
        fig_g = go.Figure()
        fig_g.add_trace(go.Scatter(x=gdd_acum.index, y=gdd_acum.values, name="GDD acumulado",
            line=dict(color=cor_cult, width=2.5), fill="tozeroy",
            fillcolor="rgba(45,212,167,0.08)", mode="lines"))
        fig_g.add_hline(y=gdd_ciclo, line_dash="dash", line_color="#ffd166",
            annotation_text=f"Ciclo {cultura_ref} (~{gdd_ciclo})",
            annotation_font_color="#ffd166", annotation_font_size=10)
        fig_g.update_layout(**LAYOUT_BASE, height=320, legend=_LEGEND, yaxis={**_YAXIS,"title":"°C·dia"},
            title=_TITLE(f"Acúmulo térmico · Tbase {t_base:.0f} °C"))
        st.plotly_chart(fig_g, width="stretch")
        st.markdown('<div class="note">O GDD indica em que fase a cultura está e quando deve '
                    'florescer/maturar. O acúmulo soma todo o período selecionado — para um único '
                    'ciclo, escolha um período a partir da data de plantio.</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="section-title">Balanço hídrico acumulado</div>', unsafe_allow_html=True)
        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(x=balanco_acum.index, y=balanco_acum.values, name="Balanço (mm)",
            line=dict(color="#00e5ff", width=2.5), fill="tozeroy",
            fillcolor="rgba(0,229,255,0.08)", mode="lines"))
        fig_b.add_hline(y=0, line_color="#7ba3c8", line_width=1)
        fig_b.update_layout(**LAYOUT_BASE, height=320, legend=_LEGEND, yaxis={**_YAXIS,"title":"mm"},
            title=_TITLE("Chuva − evapotranspiração (ET0)"))
        st.plotly_chart(fig_b, width="stretch")
        st.markdown('<div class="note">Acima de zero, sobra água no sistema; abaixo, há déficit e a '
                    'planta depende da reserva do solo ou de irrigação.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Leitura rápida</div>', unsafe_allow_html=True)
    leitura = []
    if pct_ciclo >= 100:
        leitura.append(f"O acúmulo térmico do período (<b>{gdd_total:.0f} °C·dia</b>) já cobre o "
                       f"ciclo de referência da {cultura_ref}.")
    else:
        leitura.append(f"O período acumulou <b>{gdd_total:.0f} °C·dia</b>, cerca de "
                       f"<b>{pct_ciclo:.0f}%</b> do ciclo térmico da {cultura_ref}.")
    if balanco_total >= 0:
        leitura.append(f"O balanço hídrico fechou positivo (<b>{balanco_total:+.0f} mm</b>): "
                       f"mais chuva do que demanda evaporativa.")
    else:
        leitura.append(f"O balanço hídrico fechou negativo (<b>{balanco_total:+.0f} mm</b>): "
                       f"a demanda evaporativa superou a chuva — sinal de estresse hídrico.")
    if veranico >= 10:
        leitura.append(f"Houve um veranico de <b>{veranico} dias</b> seguidos sem chuva relevante — "
                       f"risco alto se coincidir com a floração.")
    if dias_estresse > 0:
        leitura.append(f"<b>{dias_estresse} dia(s)</b> com máxima ≥ 34 °C, faixa de estresse térmico para grãos.")
    st.markdown('<div class="read">• ' + "<br>• ".join(leitura) + "</div>", unsafe_allow_html=True)

    st.markdown('<div class="note" style="margin-top:12px;">Tbase e GDD de ciclo são valores de '
                'referência; ajuste à cultivar específica. ET0 é a evapotranspiração de referência '
                '(FAO Penman-Monteith) fornecida pela API.</div>', unsafe_allow_html=True)
