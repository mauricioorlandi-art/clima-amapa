import streamlit as st
import requests
import os
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime, timedelta, timezone

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
  --fundo:#0a1628; --superficie:#0f2040; --superficie2:#13284c;
  --linha:#1e3a64; --linha-suave:#16305a;
  --destaque:#00e5ff; --texto:#e8f4fd; --suave:#7ba3c8; --tenue:#4d6b94;
  --temp-maxima:#ff6b6b; --temp-minima:#38bdf8; --temp-media:#ffd166;
  --chuva:#00e5ff; --umidade:#a78bfa; --vento:#fb923c; --cultura:#2dd4a7;
}
html,body,[data-testid="stAppViewContainer"]{
  background:radial-gradient(1100px 460px at 18% -8%, rgba(0,229,255,.07), transparent 60%),
             radial-gradient(900px 500px at 100% 0%, rgba(167,139,250,.05), transparent 55%),
             var(--fundo)!important;
  color:var(--texto)!important; font-family:'DM Sans',sans-serif;
}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0a1f3d,#071530)!important;border-right:1px solid var(--linha);}
[data-testid="stSidebar"] *{color:var(--texto)!important;}
[data-testid="stSidebar"] hr{border-color:var(--linha-suave)!important;margin:14px 0!important;}
h1,h2,h3{font-family:'Space Mono',monospace!important;letter-spacing:-.01em;}
[data-testid="stSelectbox"]>div>div,[data-testid="stDateInput"]>div>div{
  background:var(--superficie2)!important;border:1px solid var(--linha)!important;color:var(--texto)!important;border-radius:8px!important;}

/* Sidebar: rótulos em versalete monoespaçado */
.lateral-rotulo{font-family:'Space Mono',monospace;font-size:.66rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--suave);margin:2px 0 6px;}
.lateral-marca{font-family:'Space Mono',monospace;font-weight:700;font-size:1.05rem;letter-spacing:.04em;color:var(--texto);}
.lateral-marca small{display:block;font-weight:400;font-size:.62rem;letter-spacing:.22em;color:var(--tenue);margin-top:3px;}

/* Hero */
.capa{padding:30px 36px 26px;border:1px solid var(--linha);border-radius:18px;margin-bottom:24px;
  background:linear-gradient(135deg,rgba(15,32,64,.9),rgba(19,40,76,.6));position:relative;overflow:hidden;}
.capa::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent 70%,rgba(0,229,255,.05));pointer-events:none;}
.capa-sobrancelha{font-family:'Space Mono',monospace;font-size:.68rem;letter-spacing:.32em;text-transform:uppercase;color:var(--destaque);}
.capa-titulo{font-family:'Space Mono',monospace;font-weight:700;font-size:2.5rem;line-height:1;color:var(--texto);margin:10px 0 14px;}
.capa-linha{height:1px;background:linear-gradient(90deg,var(--destaque),transparent 40%);margin-bottom:12px;}
.capa-info{font-family:'Space Mono',monospace;font-size:.82rem;color:var(--suave);letter-spacing:.02em;}
.capa-info b{color:var(--texto);font-weight:700;}

/* Eyebrow de seção */
.titulo-secao{font-family:'Space Mono',monospace;font-size:.72rem;text-transform:uppercase;letter-spacing:.2em;
  color:var(--suave);margin:6px 0 14px;border-left:2px solid var(--destaque);padding-left:11px;}

/* Abas */
.stTabs [data-baseweb="tabela-list"]{gap:4px;background:transparent;border-bottom:1px solid var(--linha);}
.stTabs [data-baseweb="tabela"]{background:transparent;border:none;color:var(--tenue);
  font-family:'Space Mono',monospace;font-size:.74rem;letter-spacing:.16em;padding:10px 18px;}
.stTabs [aria-selected="true"]{color:var(--destaque)!important;border-bottom:2px solid var(--destaque)!important;}

/* Cartão KPI */
.indicador{background:var(--superficie);border:1px solid var(--linha);border-top-width:3px;border-radius:13px;
  padding:15px 14px 13px;transition:border-color .18s,transform .18s;height:100%;}
.indicador:hover{border-color:#2e5fa0;transform:translateY(-2px);}
.indicador-rotulo{font-family:'Space Mono',monospace;font-size:.62rem;text-transform:uppercase;letter-spacing:.12em;color:var(--suave);}
.indicador-valor{font-family:'Space Mono',monospace;font-weight:700;font-size:1.5rem;line-height:1.15;color:var(--texto);margin-top:7px;}
.indicador-unidade{font-size:.66rem;color:var(--tenue);margin-top:1px;}

/* Cartão de previsão diária */
.previsao{background:var(--superficie);border:1px solid var(--linha);border-radius:13px;padding:13px 8px 11px;
  text-align:center;transition:border-color .18s,transform .18s;}
.previsao:hover{border-color:#2e5fa0;transform:translateY(-2px);}
.previsao-data{font-family:'Space Mono',monospace;font-size:.66rem;letter-spacing:.06em;color:var(--suave);}
.previsao-icone{height:34px;display:flex;align-items:center;justify-content:center;margin:8px 0 6px;}
.previsao-tmax{font-family:'Space Mono',monospace;font-weight:700;font-size:1.05rem;color:var(--temp-maxima);}
.previsao-tmin{font-family:'Space Mono',monospace;font-size:.84rem;color:var(--temp-minima);}
.previsao-info{font-size:.6rem;color:var(--tenue);margin-top:5px;line-height:1.5;}
.previsao-info b{color:var(--suave);font-weight:600;}

/* Alertas */
.alerta{background:var(--superficie);border:1px solid var(--linha);border-left-width:3px;border-radius:11px;
  padding:13px 16px;margin-bottom:9px;}
.alerta-topo{display:flex;align-items:center;gap:9px;}
.alerta-ponto{width:7px;height:7px;border-radius:50%;display:inline-block;}
.alerta-titulo{font-family:'Space Mono',monospace;font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;}
.alerta-texto{color:var(--texto);font-size:.86rem;margin-top:6px;line-height:1.55;}

/* Cartão de cultura */
.cartao-cultura{background:var(--superficie);border:1px solid var(--linha);border-radius:13px;padding:15px 17px;height:100%;}
.cultura-topo{display:flex;align-items:center;gap:9px;font-family:'Space Mono',monospace;font-weight:700;font-size:.92rem;color:var(--texto);}
.cultura-ponto{width:9px;height:9px;border-radius:2px;}
.cultura-corpo{color:var(--suave);font-size:.8rem;margin-top:9px;line-height:1.6;}

/* Painel de leitura */
.leitura{background:var(--superficie);border:1px solid var(--linha);border-radius:13px;padding:18px 22px;
  color:var(--texto);font-size:.9rem;line-height:1.75;}
.leitura b{color:var(--destaque);}

.nota{color:var(--tenue);font-size:.74rem;line-height:1.5;}
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
    "temp_maxima":"#ff6b6b","temp_minima":"#38bdf8","temp_media":"#ffd166",
    "chuva":"#00e5ff","umidade":"#a78bfa","vento":"#fb923c","crop":"#2dd4a7",
}
MESES_PT = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
            7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

# Códigos de tempo WMO → grupo de ícone
GRUPO_TEMPO = {
    0:"sol", 1:"sol", 2:"parcial", 3:"nuvem", 45:"nevoa", 48:"nevoa",
    51:"garoa", 53:"garoa", 55:"garoa", 56:"garoa", 57:"garoa",
    61:"chuva", 63:"chuva", 65:"forte", 66:"chuva", 67:"forte",
    71:"neve", 73:"neve", 75:"neve", 77:"neve",
    80:"garoa", 81:"chuva", 82:"forte", 85:"neve", 86:"neve",
    95:"tempestade", 96:"tempestade", 99:"tempestade",
}
DESCRICAO_TEMPO = {
    "sol":"Céu limpo","parcial":"Parcialmente nublado","nuvem":"Nublado","nevoa":"Névoa",
    "garoa":"Garoa","chuva":"Chuva","forte":"Chuva forte","neve":"Neve","tempestade":"Trovoada",
}

# Parâmetros agronômicos (valores de referência — ajuste à cultivar local)
CULTURAS = {
    "Soja":  {"temp_base": 10.0, "gdd_ciclo": 1400, "cor": "#2dd4a7"},
    "Milho": {"temp_base": 10.0, "gdd_ciclo": 1500, "cor": "#ffd166"},
}

# Sistema de sucessão. Cada fase é (rótulo, dia_inicial, dia_final) em DIAS A PARTIR
# do plantio da soja (dia 0 = início das chuvas, detectado por cidade). As durações
# de ciclo são típicas; o que se adapta à cidade é a data-âncora (inicio das chuvas).
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

# Delta T — faixas do Bureau of Meteorology (Austrália) / GRDC. Ideal 2–8 °C.
DELTA_T_IDEAL = (2.0, 8.0)
DELTA_T_MARGINAL = (0.0, 10.0)

# Lua — mês sinódico e nova de referência (época padrão, UTC)
MES_SINODICO = 29.530588853
LUA_NOVA_REFERENCIA = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
FASES_LUA = {
    "Nova":      {"cor": "#7ba3c8"},
    "Crescente": {"cor": "#2dd4a7"},
    "Cheia":     {"cor": "#ffd166"},
    "Minguante": {"cor": "#fb923c"},
}
# Recomendações da tradição agrícola brasileira (empírica — sem comprovação científica)
LUA_MANEJO = {
    "Nova":      "Preparo do solo, adubação e controle de pragas. Semeadura fraca; alguns "
                 "produtores aproveitam para raízes.",
    "Crescente": "Fase indicada para o que cresce acima do solo — grãos como soja e milho, "
                 "folhas e frutos. É a janela preferida da tradição para semear grãos.",
    "Cheia":     "Melhor período para a colheita (grãos e frutos mais 'cheios'). Evita-se "
                 "semear e podar.",
    "Minguante": "Raízes e tubérculos, podas e preparo. Menos indicada para plantio de grãos.",
}
LUA_GRAOS = {"Crescente": "favorável", "Nova": "aceitável", "Cheia": "colheita", "Minguante": "desfavorável"}

# ENOS (El Niño-Oscilação Sul) — efeito no Norte/Amapá (CPTEC-INPE, INMET, NOAA)
ENOS_INFO = {
    "Neutro": {"cor": "#7ba3c8", "titulo": "ENOS neutro",
        "texto": "Sem El Niño nem La Niña ativos: espere o padrão climatológico normal da "
                 "região. Siga a janela de plantio detectada pela chuva histórica."},
    "El Niño": {"cor": "#ff6b6b", "titulo": "El Niño ativo",
        "texto": "No Norte (Roraima, Amapá, norte do PA/AM) o El Niño tende a REDUZIR a chuva e "
                 "intensificar a estação seca, deslocando a ZCIT. Risco maior para sequeiro: "
                 "considere cultivares precoces, atenção à irrigação e não atrase o plantio da soja."},
    "La Niña": {"cor": "#2dd4a7", "titulo": "La Niña ativa",
        "texto": "No Norte a La Niña tende a AUMENTAR a chuva (acima da média). Bom para o "
                 "enchimento hídrico, mas atenção ao excesso: risco de encharcamento, doenças e "
                 "de colher em período úmido. Priorize drenagem e cultivares resistentes."},
}


def temperatura_bulbo_umido(T, RH):
    """Temperatura de bulbo úmido (°C) por Stull (2011), a partir de T (°C) e UR (%)."""
    RH = np.clip(np.asarray(RH, dtype=float), 1, 100)
    T = np.asarray(T, dtype=float)
    return (T * np.arctan(0.151977 * np.sqrt(RH + 8.313659))
            + np.arctan(T + RH) - np.arctan(RH - 1.676331)
            + 0.00391838 * (RH ** 1.5) * np.arctan(0.023101 * RH) - 4.686035)


def classificar_delta_t(valor):
    """Classifica o Delta T para pulverização."""
    if valor < DELTA_T_MARGINAL[0] or valor > DELTA_T_MARGINAL[1]:
        return ("Inadequado", "#ff6b6b")
    if valor < DELTA_T_IDEAL[0] or valor > DELTA_T_IDEAL[1]:
        return ("Marginal", "#fb923c")
    return ("Ideal", "#2dd4a7")


def janelas_pulverizacao(previsao_horaria):
    """Blocos horários bons para pulverizar: Delta T ideal, vento 3–15 km/h e sem chuva."""
    bom = (previsao_horaria["delta_t"].between(*DELTA_T_IDEAL) & previsao_horaria["vento"].between(3, 15) & (previsao_horaria["chuva"] < 0.1))
    janelas, ini, prev = [], None, None
    for t, ok in bom.items():
        if ok and ini is None:
            ini = t
        if (not ok) and ini is not None:
            janelas.append((ini, prev)); ini = None
        prev = t
    if ini is not None:
        janelas.append((ini, prev))
    return janelas


def idade_lunar(momento=None):
    """Idade da lua em dias (0 = lua nova)."""
    momento = momento or datetime.now(timezone.utc)
    return ((momento - LUA_NOVA_REFERENCIA).total_seconds() / 86400.0) % MES_SINODICO


def fase_lunar(idade):
    """Retorna (nome_da_fase, fração_iluminada 0-1, fração_do_ciclo 0-1)."""
    fracao = idade / MES_SINODICO
    iluminacao = (1 - math.cos(2 * math.pi * fracao)) / 2
    if fracao < 0.125 or fracao >= 0.875:
        nome = "Nova"
    elif fracao < 0.375:
        nome = "Crescente"
    elif fracao < 0.625:
        nome = "Cheia"
    else:
        nome = "Minguante"
    return nome, iluminacao, fracao


def proxima_fase_principal(alvo_frac, a_partir=None):
    """Próxima data (UTC) em que o ciclo lunar atinge a fração alvo (0=nova,0.25=q.crescente,
    0.5=cheia,0.75=q.minguante)."""
    a_partir = a_partir or datetime.now(timezone.utc)
    fracao = idade_lunar(a_partir) / MES_SINODICO
    d = (alvo_frac - fracao) % 1.0
    return a_partir + timedelta(days=d * MES_SINODICO)


def desenhar_lua_svg(iluminacao, fracao, tam=88):
    """Desenha a lua com a porção iluminada correta (crescente à direita, minguante à esquerda)."""
    r = tam / 2 - 4
    cx = cy = tam / 2
    disco = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#14284c" stroke="#1e3a64" stroke-width="1.5"/>'
    if iluminacao <= 0.02:
        luz = ""
    elif iluminacao >= 0.98:
        luz = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffd166"/>'
    else:
        crescendo = fracao < 0.5                 # antes da cheia ilumina pela direita
        rx = abs(r * (1 - 2 * iluminacao))          # raio horizontal do terminador
        sweep_out = 1 if crescendo else 0      # semicírculo externo no lado iluminado
        if crescendo:
            sweep_in = 0 if iluminacao < 0.5 else 1
        else:
            sweep_in = 1 if iluminacao < 0.5 else 0
        path = (f'M {cx} {cy - r} A {r} {r} 0 0 {sweep_out} {cx} {cy + r} '
                f'A {rx} {r} 0 0 {sweep_in} {cx} {cy - r} Z')
        luz = f'<path d="{path}" fill="#ffd166"/>'
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 {tam} {tam}" '
            f'xmlns="http://www.w3.org/2000/svg">{disco}{luz}</svg>')


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
def _clima_historico(lat, lon, inicio, fim):
    """Histórico diário do Open-Meteo Archive (ERA5). Tem atraso de ~5 dias."""
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
    dados = pd.DataFrame(r.json()["daily"])
    dados = dados.rename(columns={"time": "data"})
    dados["data"] = pd.to_datetime(dados["data"])
    dados.set_index("data", inplace=True)
    dados = dados.rename(columns={
        "temperature_2m_max":"temp_maxima", "temperature_2m_min":"temp_minima",
        "temperature_2m_mean":"temp_media", "precipitation_sum":"chuva",
        "windspeed_10m_max":"vento", "et0_fao_evapotranspiration":"et0",
    })
    dados["umidade"] = (dados["relative_humidity_2m_max"] + dados["relative_humidity_2m_min"]) / 2
    dados = dados.drop(columns=["relative_humidity_2m_max", "relative_humidity_2m_min"])
    return dados


def _clima_recente(lat, lon, past_days):
    """Dias recentes até hoje via Open-Meteo Forecast (past_days), no mesmo esquema."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "daily": ("temperature_2m_max,temperature_2m_min,precipitation_sum,"
                  "windspeed_10m_max,et0_fao_evapotranspiration"),
        "hourly": "relative_humidity_2m",
        "timezone": "America/Belem",
        "past_days": int(past_days), "forecast_days": 1,
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    j = r.json()
    dados = pd.DataFrame(j["daily"])
    dados = dados.rename(columns={"time": "data"})
    dados["data"] = pd.to_datetime(dados["data"])
    dados.set_index("data", inplace=True)
    dados = dados.rename(columns={
        "temperature_2m_max":"temp_maxima", "temperature_2m_min":"temp_minima",
        "precipitation_sum":"chuva", "windspeed_10m_max":"vento",
        "et0_fao_evapotranspiration":"et0",
    })
    dados["temp_media"] = (dados["temp_maxima"] + dados["temp_minima"]) / 2
    h = pd.DataFrame(j["hourly"])
    h = h.rename(columns={"time": "data"})
    h["data"] = pd.to_datetime(h["data"])
    h.set_index("data", inplace=True)
    dados["umidade"] = h["relative_humidity_2m"].resample("D").mean().reindex(dados.index)
    hoje = pd.Timestamp(date.today())
    return dados[dados.index <= hoje]


@st.cache_data(ttl=3600, show_spinner=False)
def buscar_clima(lat, lon, inicio, fim):
    """Histórico até hoje: Archive (ERA5) para o grosso + Forecast/past_days para os
    últimos dias, já que o Archive tem atraso de ~5 dias."""
    hoje = date.today()
    fim = min(fim, hoje)
    arch_fim = min(fim, hoje - timedelta(days=5))
    arch = rec = None
    if inicio <= arch_fim:
        try:
            arch = _clima_historico(lat, lon, inicio, arch_fim)
        except Exception:
            arch = None
    if fim > hoje - timedelta(days=6):
        past_days = max(7, min(92, (hoje - inicio).days + 1))
        try:
            rec = _clima_recente(lat, lon, past_days)
        except Exception:
            rec = None
    if arch is None and rec is None:
        # último recurso: tenta o Archive no intervalo inteiro
        return _clima_historico(lat, lon, inicio, fim)
    if arch is not None and rec is not None:
        dados = arch.combine_first(rec)       # Archive tem prioridade; recente preenche o rabo
    else:
        dados = arch if arch is not None else rec
    ini_ts, fim_ts = pd.Timestamp(inicio), pd.Timestamp(fim)
    return dados[(dados.index >= ini_ts) & (dados.index <= fim_ts)].sort_index()


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
    dados = pd.DataFrame(j["daily"])
    dados = dados.rename(columns={"time": "data"})
    dados["data"] = pd.to_datetime(dados["data"])
    dados.set_index("data", inplace=True)
    dados = dados.rename(columns={
        "temperature_2m_max":"temp_maxima", "temperature_2m_min":"temp_minima",
        "precipitation_sum":"chuva", "precipitation_probability_max":"prob_chuva",
        "windspeed_10m_max":"vento", "et0_fao_evapotranspiration":"et0", "weathercode":"cod_tempo",
    })
    dados["temp_media"] = (dados["temp_maxima"] + dados["temp_minima"]) / 2
    h = pd.DataFrame(j["hourly"])
    h = h.rename(columns={"time": "data"})
    h["data"] = pd.to_datetime(h["data"])
    h.set_index("data", inplace=True)
    dados["umidade"] = h["relative_humidity_2m"].resample("D").mean().reindex(dados.index)
    return dados


@st.cache_data(ttl=1800, show_spinner=False)
def buscar_previsao_horaria(lat, lon, dias=4):
    """Previsão horária (Open-Meteo). Base para o Delta T e a janela de pulverização."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,windspeed_10m,precipitation",
        "timezone": "America/Belem",
        "forecast_days": int(dias),
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    h = pd.DataFrame(r.json()["hourly"])
    h = h.rename(columns={"time": "data"})
    h["data"] = pd.to_datetime(h["data"])
    h.set_index("data", inplace=True)
    h = h.rename(columns={"temperature_2m": "temperatura", "relative_humidity_2m": "ur",
                          "windspeed_10m": "vento", "precipitation": "chuva"})
    h["bulbo_umido"] = temperatura_bulbo_umido(h["temperatura"].values, h["ur"].values)
    h["delta_t"] = h["temperatura"] - h["bulbo_umido"]
    return h


def carregar_planilha(arquivo):
    """Lê um CSV de clima diário (fonte sem API, atualização manual) para o mesmo
    esquema do histórico. Aceita nomes de coluna em PT ou EN."""
    bruto = pd.read_csv(arquivo)
    bruto.columns = [str(c).strip().lower() for c in bruto.columns]
    mapa = {
        # data
        "data": "data", "date": "data", "dia": "data",
        # temperatura máxima
        "temp_maxima": "temp_maxima", "temp_max": "temp_maxima", "tmax": "temp_maxima",
        "temperatura_maxima": "temp_maxima", "temperatura_max": "temp_maxima",
        "temp máxima": "temp_maxima", "maxima": "temp_maxima",
        # temperatura mínima
        "temp_minima": "temp_minima", "temp_min": "temp_minima", "tmin": "temp_minima",
        "temperatura_minima": "temp_minima", "temperatura_min": "temp_minima",
        "temp mínima": "temp_minima", "minima": "temp_minima",
        # temperatura média
        "temp_media": "temp_media", "temp_mean": "temp_media", "tmed": "temp_media",
        "temperatura_media": "temp_media", "media": "temp_media",
        # chuva
        "chuva": "chuva", "precipitacao": "chuva", "precipitação": "chuva",
        "precipitation": "chuva", "chuva": "chuva",
        # vento
        "vento": "vento", "wind": "vento", "windspeed": "vento",
        # umidade
        "umidade": "umidade", "humidity": "umidade", "ur": "umidade",
        # evapotranspiração
        "et0": "et0", "eto": "et0", "evapotranspiracao": "et0", "evapotranspiração": "et0",
    }
    bruto = bruto.rename(columns={c: mapa[c] for c in bruto.columns if c in mapa})
    if "data" not in bruto.columns:
        raise ValueError("O CSV precisa de uma coluna de data (data/date).")
    faltando = [c for c in ("temp_maxima", "temp_minima", "chuva") if c not in bruto.columns]
    if faltando:
        raise ValueError("Faltam colunas obrigatórias: " + ", ".join(faltando))
    # Data: tenta ISO (2026-07-01) primeiro; se não casar, tenta dd/mm/aaaa
    datas = pd.to_datetime(bruto["data"], format="ISO8601", errors="coerce")
    faltantes = datas.isna()
    if faltantes.any():
        datas[faltantes] = pd.to_datetime(bruto["data"][faltantes], dayfirst=True, errors="coerce")
    bruto["data"] = datas
    bruto = bruto.dropna(subset=["data"]).set_index("data").sort_index()
    if "temp_media" not in bruto.columns:
        bruto["temp_media"] = (bruto["temp_maxima"] + bruto["temp_minima"]) / 2
    for opc in ("vento", "umidade", "et0"):
        if opc not in bruto.columns:
            bruto[opc] = np.nan
    return bruto


def planilha_modelo():
    """CSV de exemplo para o usuário preencher manualmente."""
    indice = pd.date_range(date.today() - timedelta(days=4), periods=5)
    exemplo = pd.DataFrame({
        "data": indice.strftime("%d/%m/%Y"),
        "temp_maxima": [32.1, 31.5, 33.0, 30.8, 32.4],
        "temp_minima": [23.0, 22.6, 23.4, 22.1, 23.2],
        "chuva": [0.0, 12.4, 3.2, 0.0, 8.1],
        "vento": [9, 14, 7, 6, 11],
        "umidade": [78, 88, 74, 70, 83],
        "et0": [4.6, 3.1, 4.9, 5.2, 3.8],
    })
    return exemplo.to_csv(index=False).encode("utf-8")


def mostrar_modelo_planilha():
    """Guia visual de como o CSV precisa estar para o app aceitar."""
    st.markdown('<div class="titulo-secao">Modelo do arquivo CSV</div>', unsafe_allow_html=True)
    st.caption("Monte a planilha assim (uma linha por dia) e salve como CSV. "
               "A primeira linha deve conter os nomes das colunas.")

    exemplo = pd.DataFrame({
        "data": ["01/07/2026", "02/07/2026", "03/07/2026"],
        "temp_maxima": [32.1, 31.5, 33.0],
        "temp_minima": [23.0, 22.6, 23.4],
        "chuva": [0.0, 12.4, 3.2],
        "vento": [9, 14, 7],
        "umidade": [78, 88, 74],
        "et0": [4.6, 3.1, 4.9],
    })
    st.dataframe(exemplo, width="stretch", hide_index=True)

    st.markdown('<div class="titulo-secao" style="margin-top:14px;">Regras das colunas</div>',
                unsafe_allow_html=True)
    regras = pd.DataFrame({
        "Coluna": ["data", "temp_maxima", "temp_minima", "chuva", "vento", "umidade", "et0"],
        "O que é": ["Dia da medição", "Temperatura máxima", "Temperatura mínima",
                    "Chuva do dia", "Velocidade do vento", "Umidade relativa",
                    "Evapotranspiração"],
        "Unidade": ["dd/mm/aaaa", "°C", "°C", "mm", "km/h", "%", "mm"],
        "Obrigatória": ["Sim", "Sim", "Sim", "Sim", "Não", "Não", "Não"],
        "Também aceita": ["date, dia", "temp_max, tmax", "temp_min, tmin",
                          "precipitation, chuva, precipitacao",
                          "wind", "humidity, ur", "eto"],
    })
    st.dataframe(regras, width="stretch", hide_index=True)

    st.markdown("""
    <div class="alerta" style="border-left-color:#00e5ff;">
      <div class="alerta-topo"><span class="alerta-ponto" style="background:#00e5ff;"></span>
      <span class="alerta-titulo" style="color:#00e5ff;">Pontos de atenção</span></div>
      <div class="alerta-texto">
        Cada linha é um dia; a primeira linha da planilha deve ter os nomes das colunas.<br>
        Use <b>ponto</b> como separador decimal (32.1, não 32,1).<br>
        A data pode ser 01/07/2026 ou 2026-07-01 — as duas funcionam.<br>
        Dias sem chuva devem ter <b>0</b>, não célula vazia.<br>
        No Excel, salve com <b>Salvar como → CSV UTF-8 (delimitado por vírgula)</b>.
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nota" style="margin-bottom:8px;">Dica: baixe o modelo abaixo, abra no '
                'Excel, substitua pelos seus dados e salve. É o caminho mais seguro.</div>',
                unsafe_allow_html=True)
    st.download_button("Baixar este modelo em CSV", data=planilha_modelo(),
                       file_name="modelo_clima.csv", mime="text/csv")


COLUNAS_MANUAIS = ["Data", "Temp. máx (°C)", "Temp. mín (°C)", "Chuva (mm)",
                "Vento (km/h)", "Umidade (%)", "ET0 (mm)"]


def tabela_manual_inicial(linhas=7):
    """DataFrame vazio (datas recentes) para o usuário digitar na tabela do app."""
    datas = pd.date_range(date.today() - timedelta(days=linhas - 1), periods=linhas).date
    d = {"Data": list(datas)}
    for c in COLUNAS_MANUAIS[1:]:
        d[c] = [None] * linhas
    return pd.DataFrame(d)


# Arquivo de persistência: fica ao lado do app.py, independentemente da pasta de execução
ARQUIVO_MANUAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_manuais.csv")


def carregar_tabela_manual():
    """Lê a tabela manual salva em disco; se não existir, devolve a tabela inicial vazia."""
    if os.path.exists(ARQUIVO_MANUAL):
        try:
            t = pd.read_csv(ARQUIVO_MANUAL)
            for c in COLUNAS_MANUAIS:
                if c not in t.columns:
                    t[c] = None
            t = t[COLUNAS_MANUAIS]
            t["Data"] = pd.to_datetime(t["Data"], errors="coerce").dt.date
            return t
        except Exception:
            pass
    return tabela_manual_inicial()


def salvar_tabela_manual(tabela):
    """Grava a tabela manual em disco (chamado a cada edição)."""
    try:
        tabela.to_csv(ARQUIVO_MANUAL, index=False)
        return True
    except Exception:
        return False


# Persistência da planilha importada (CSV), no esquema interno já normalizado
ARQUIVO_PLANILHA_IMPORTADA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "dados_importados.csv")


def salvar_planilha_importada(dados):
    """Guarda em disco a planilha importada, já normalizada, para reabrir depois."""
    try:
        dados.to_csv(ARQUIVO_PLANILHA_IMPORTADA, index_label="data")
        return True
    except Exception:
        return False


def carregar_planilha_importada():
    """Recarrega a última planilha importada; devolve None se não houver."""
    if not os.path.exists(ARQUIVO_PLANILHA_IMPORTADA):
        return None
    try:
        d = pd.read_csv(ARQUIVO_PLANILHA_IMPORTADA)
        if "data" not in d.columns:
            return None
        d["data"] = pd.to_datetime(d["data"], errors="coerce")
        d = d.dropna(subset=["data"]).set_index("data").sort_index()
        return d if not d.empty else None
    except Exception:
        return None


def apagar_planilha_importada():
    try:
        if os.path.exists(ARQUIVO_PLANILHA_IMPORTADA):
            os.remove(ARQUIVO_PLANILHA_IMPORTADA)
    except Exception:
        pass


def tabela_para_dados(tabela):
    """Converte a tabela editada (COLUNAS_MANUAIS) para o esquema interno do app."""
    t = tabela.rename(columns={
        "Data": "data", "Temp. máx (°C)": "temp_maxima", "Temp. mín (°C)": "temp_minima",
        "Chuva (mm)": "chuva", "Vento (km/h)": "vento",
        "Umidade (%)": "umidade", "ET0 (mm)": "et0",
    })
    t["data"] = pd.to_datetime(t["data"], errors="coerce")
    for c in ("temp_maxima", "temp_minima", "chuva", "vento", "umidade", "et0"):
        if c in t.columns:
            t[c] = pd.to_numeric(t[c], errors="coerce")
    t = t.dropna(subset=["data", "temp_maxima", "temp_minima", "chuva"])
    if t.empty:
        return t
    t = t.set_index("data").sort_index()
    t["temp_media"] = (t["temp_maxima"] + t["temp_minima"]) / 2
    return t


def agregar(dados, agregacao_regra):
    regra = {"Semanal":"W", "Mensal":"ME"}.get(agregacao_regra)
    if regra:
        funcs = {"temp_maxima":"max","temp_minima":"min","temp_media":"mean",
                 "chuva":"sum","vento":"max","umidade":"mean"}
        if "et0" in dados.columns:
            funcs["et0"] = "sum"
        try:
            return dados.resample(regra).agg(funcs)
        except ValueError:
            return dados.resample("M").agg(funcs)
    return dados


# ── Indicadores agronômicos ──────────────────────────────────────────────────────
def calcular_gdd(dados, temp_base):
    """Graus-dia diários: max(0, Tmédia - Tbase)."""
    tmean = (dados["temp_maxima"] + dados["temp_minima"]) / 2
    return (tmean - temp_base).clip(lower=0)


def maior_veranico(chuva, limiar=1.0):
    """Maior sequência de dias consecutivos com chuva abaixo do limiar (mm)."""
    melhor = atual = 0
    for seco in (chuva < limiar):
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


def dia_do_ano_para_data(doy):
    """Dia do ano (cíclico) → Timestamp dentro do ANO_BASE."""
    doy = ((int(doy) - 1) % 365) + 1
    return pd.Timestamp(date(ANO_BASE, 1, 1)) + pd.Timedelta(days=doy - 1)


def fase_dias_para_segmentos(inicio_dia_do_ano, ini_off, fim_off):
    """Converte uma fase definida em dias a partir do plantio (inicio) em segmentos
    de data no calendário anual, dividindo na virada do ano quando necessário."""
    ini, fim = inicio_dia_do_ano + ini_off, inicio_dia_do_ano + fim_off
    if (ini - 1) // 365 == (fim - 1) // 365:
        return [(dia_do_ano_para_data(ini), dia_do_ano_para_data(fim) + pd.Timedelta(days=1))]
    return [
        (dia_do_ano_para_data(ini), pd.Timestamp(date(ANO_BASE, 12, 31)) + pd.Timedelta(days=1)),
        (pd.Timestamp(date(ANO_BASE, 1, 1)), dia_do_ano_para_data(fim) + pd.Timedelta(days=1)),
    ]


def maior_periodo_umido(umido):
    """Maior sequência cíclica de meses úmidos. Retorna (n_meses, ini_idx, fim_idx, regime)."""
    n = 12
    if all(umido):
        return (12, None, None, "umido")
    if not any(umido):
        return (0, None, None, "seco")
    melhor = (0, 0, 0)
    for inicio_idx in range(n):
        if umido[inicio_idx] and not umido[(inicio_idx - 1) % n]:
            duracao, m = 0, inicio_idx
            while umido[m % n] and duracao < n:
                duracao += 1; m += 1
            if duracao > melhor[0]:
                melhor = (duracao, inicio_idx, (inicio_idx + duracao - 1) % n)
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
    duracao, si, info_enos, regime = maior_periodo_umido(umido)
    if regime == "umido":
        inicio = trimestre_mais_chuvoso(precip_mes)
        return {"inicio": inicio, "fim": ((inicio + 10) % 12) + 1, "duracao": 12, "regime": "umido"}
    if regime == "seco":
        inicio = max(range(1, 13), key=lambda m: (precip_mes.get(m) or 0))
        return {"inicio": inicio, "fim": inicio, "duracao": 1, "regime": "seco"}
    return {"inicio": si + 1, "fim": info_enos + 1, "duracao": duracao, "regime": "sazonal"}


def cartao_indicador(coluna, label, valor, unidade, cor):
    coluna.markdown(f"""
    <div class="indicador" style="border-top-color:{cor};">
      <div class="indicador-rotulo">{label}</div>
      <div class="indicador-valor">{valor}</div>
      <div class="indicador-unidade">{unidade}</div>
    </div>""", unsafe_allow_html=True)


# ── Barra lateral ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="lateral-marca">CLIMA AMAPÁ<small>PAINEL CLIMÁTICO</small></div>',
                unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="lateral-rotulo">Cidade</div>', unsafe_allow_html=True)
    cidade = st.selectbox("Cidade", list(CIDADES.keys()), label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div class="lateral-rotulo">Período de análise</div>', unsafe_allow_html=True)
    DATA_MAX = date.today()
    c1, c2 = st.columns(2)
    with c1:
        data_inicio = st.date_input("Início", value=date(2023,1,1),
                                    min_value=date(1940,1,1), max_value=DATA_MAX)
    with c2:
        data_fim = st.date_input("Fim", value=DATA_MAX,
                                 min_value=date(1940,1,2), max_value=DATA_MAX)
    st.markdown("---")
    st.markdown('<div class="lateral-rotulo">Comparar com outro ano</div>', unsafe_allow_html=True)
    comparar = st.checkbox("Ativar comparação")
    ano_comparacao = None
    if comparar:
        ano_comparacao = st.number_input("Ano de referência", min_value=1940,
                                         max_value=date.today().year - 1,
                                         value=date.today().year - 2)
    st.markdown("---")
    st.markdown('<div class="lateral-rotulo">Agregação</div>', unsafe_allow_html=True)
    agregacao = st.selectbox("Agregação", ["Diário","Semanal","Mensal"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div class="lateral-rotulo">Painel agronômico</div>', unsafe_allow_html=True)
    cultura_ref = st.selectbox("Cultura de referência (GDD)", list(CULTURAS.keys()))
    st.markdown('<div class="lateral-rotulo" style="margin-top:10px;">Calendário agrícola</div>', unsafe_allow_html=True)
    limiar_chuva = st.slider("Mês chuvoso a partir de (mm)", 50, 200, 100, 10,
                             help="Limiar para o app considerar um mês dentro da estação chuvosa "
                                  "e ancorar o plantio. Detectado a partir da chuva da cidade selecionada.")
    st.markdown('<div class="lateral-rotulo" style="margin-top:10px;">Previsão</div>', unsafe_allow_html=True)
    dias_previsao = st.select_slider("Horizonte (dias)", options=[7,10,14,16], value=14)
    st.markdown("---")
    st.markdown('<div class="lateral-rotulo">Fonte dos dados</div>', unsafe_allow_html=True)
    fonte = st.radio("Fonte dos dados", ["Open-Meteo (API)", "Inserir manualmente"],
                     label_visibility="collapsed")
    metodo_manual = None
    arquivo_planilha = None
    if fonte == "Inserir manualmente":
        metodo_manual = st.radio("Como inserir", ["Digitar na tabela", "Enviar CSV"],
                                 help="Digite os dias direto na tabela do app, sem planilha, "
                                      "ou envie um CSV se preferir.")
        if metodo_manual == "Enviar CSV":
            arquivo_planilha = st.file_uploader("Enviar CSV diário", type=["csv"], label_visibility="collapsed")
            st.markdown('<div class="nota">O modelo de como formatar o arquivo aparece na página.</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div class="nota">A tabela para digitar aparece no topo da página.</div>',
                        unsafe_allow_html=True)
    st.markdown('<div class="lateral-rotulo" style="margin-top:12px;">Fase do ENOS</div>', unsafe_allow_html=True)
    enos_fase = st.selectbox("Fase do ENOS", ["Neutro", "El Niño", "La Niña"],
                             label_visibility="collapsed",
                             help="Leia a fase atual no boletim do CPTEC/INPE, INMET ou NOAA e "
                                  "selecione aqui — não há API aberta para isso.")
    enos_int = "—"
    if enos_fase != "Neutro":
        enos_int = st.selectbox("Intensidade", ["Fraco", "Moderado", "Forte"])
    st.markdown("---")
    st.markdown('<div class="nota">Dados até hoje: Open-Meteo Archive + Forecast (past_days).<br>Sem necessidade de chave de API.</div>',
                unsafe_allow_html=True)

# ── Validação ──────────────────────────────────────────────────────────────────
if data_inicio >= data_fim:
    st.error("A data de início deve ser anterior à data de fim. Ajuste o período na barra lateral.")
    st.stop()

lat = CIDADES[cidade]["lat"]
lon = CIDADES[cidade]["lon"]

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="capa">
  <div class="capa-sobrancelha">Painel climático · Amapá · Brasil</div>
  <div class="capa-titulo">CLIMA AMAPÁ</div>
  <div class="capa-linha"></div>
  <div class="capa-info">
    <b>{cidade}</b> &nbsp;·&nbsp; {lat:.4f}°, {lon:.4f}° &nbsp;·&nbsp;
    {data_inicio.strftime('%d/%m/%Y')} → {data_fim.strftime('%d/%m/%Y')}
  </div>
</div>
""", unsafe_allow_html=True)

# ── Carrega dados ──────────────────────────────────────────────────────────────
modo_manual = fonte == "Inserir manualmente"
if modo_manual:
    if metodo_manual == "Enviar CSV":
        if arquivo_planilha is not None:
            try:
                dados = carregar_planilha(arquivo_planilha)
            except Exception as e:
                st.error(f"Não foi possível ler o CSV: {e}")
                st.caption("Confira o modelo abaixo e ajuste o arquivo.")
                mostrar_modelo_planilha()
                st.stop()
            if dados.empty:
                st.error("O CSV não tem linhas válidas. Confira o modelo abaixo.")
                mostrar_modelo_planilha()
                st.stop()
            salvar_planilha_importada(dados)          # guarda para as próximas aberturas
            origem_planilha = "novo"
        else:
            dados = carregar_planilha_importada()     # nenhuma planilha enviada agora: usa a última
            if dados is None:
                st.info("Envie o arquivo CSV na barra lateral. Veja abaixo como ele precisa estar formatado.")
                mostrar_modelo_planilha()
                st.stop()
            origem_planilha = "salvo"

        periodo = (f"{dados.index.min().strftime('%d/%m/%Y')} a "
                   f"{dados.index.max().strftime('%d/%m/%Y')}")
        if origem_planilha == "novo":
            st.success(f"Planilha carregada e salva: {len(dados)} dias, de {periodo}. "
                       f"Ela será recarregada automaticamente da próxima vez que você abrir o app.")
        else:
            st.info(f"Usando a última planilha importada: {len(dados)} dias, de {periodo}. "
                    f"Envie um novo CSV na barra lateral para substituí-la.")

        coluna_info, coluna_apagar = st.columns([4, 1])
        with coluna_info:
            st.caption(f"Salvo em {os.path.basename(ARQUIVO_PLANILHA_IMPORTADA)}")
        with coluna_apagar:
            if st.button("Apagar planilha", width="stretch"):
                apagar_planilha_importada()
                st.rerun()

        with st.expander("Ver o modelo de formatação do CSV"):
            mostrar_modelo_planilha()
    else:
        st.markdown('<div class="titulo-secao">Inserir dados manualmente</div>', unsafe_allow_html=True)
        st.caption("Digite os dias direto na tabela (clique numa célula). Use o + para adicionar linhas. "
                   "Temp. máx, Temp. mín e Chuva são obrigatórias; vento, umidade e ET0 são opcionais. "
                   "Tudo é salvo automaticamente e reaparece quando você abrir o app de novo.")
        if "tabela_manual" not in st.session_state:
            st.session_state["tabela_manual"] = carregar_tabela_manual()

        editado = st.data_editor(
            st.session_state["tabela_manual"], num_rows="dynamic", width="stretch",
            key="editor_manual",
            column_config={
                "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                "Temp. máx (°C)": st.column_config.NumberColumn("Temp. máx (°C)", format="%.1f"),
                "Temp. mín (°C)": st.column_config.NumberColumn("Temp. mín (°C)", format="%.1f"),
                "Chuva (mm)": st.column_config.NumberColumn("Chuva (mm)", format="%.1f"),
                "Vento (km/h)": st.column_config.NumberColumn("Vento (km/h)", format="%.1f"),
                "Umidade (%)": st.column_config.NumberColumn("Umidade (%)", format="%.0f"),
                "ET0 (mm)": st.column_config.NumberColumn("ET0 (mm)", format="%.1f"),
            })

        # Persiste na sessão e em disco automaticamente, só quando algo muda
        texto_csv = editado.to_csv(index=False)
        if st.session_state.get("_hash_manual") != texto_csv:
            st.session_state["tabela_manual"] = editado
            salvar_tabela_manual(editado)
            st.session_state["_hash_manual"] = texto_csv

        coluna_status, coluna_limpar = st.columns([4, 1])
        with coluna_status:
            st.caption(f"Salvo automaticamente em {os.path.basename(ARQUIVO_MANUAL)}")
        with coluna_limpar:
            if st.button("Limpar tabela", width="stretch"):
                st.session_state["tabela_manual"] = tabela_manual_inicial()
                st.session_state.pop("_hash_manual", None)
                st.session_state.pop("editor_manual", None)
                if os.path.exists(ARQUIVO_MANUAL):
                    try:
                        os.remove(ARQUIVO_MANUAL)
                    except Exception:
                        pass
                st.rerun()

        dados = tabela_para_dados(editado)
        if len(dados) < 2:
            st.info("Preencha ao menos 2 dias (com temp. máx, temp. mín e chuva) para ver os gráficos.")
            st.stop()
    if dados.empty:
        st.error("Não há linhas válidas nos dados manuais.")
        st.stop()
else:
    with st.spinner("Carregando dados climáticos..."):
        try:
            dados = buscar_clima(lat, lon, data_inicio, data_fim)
        except Exception as e:
            st.error(f"Não foi possível buscar os dados: {e}")
            st.stop()

dados_agregados = agregar(dados, agregacao)

tab_hist, tab_prev, tab_cal, tab_lua, tab_agro = st.tabs([
    "HISTÓRICO", "PREVISÃO", "CALENDÁRIO AGRÍCOLA", "CALENDÁRIO LUNAR", "PAINEL AGRONÔMICO"
])

# ════════════════════════════════════════════════════════════════════ HISTÓRICO ═
with tab_hist:
    st.markdown('<div class="titulo-secao">Resumo do período</div>', unsafe_allow_html=True)
    indicadores = [
        ("Temp. média",   f"{dados['temp_media'].mean():.1f}", "°C",   CORES["temp_media"]),
        ("Máx. absoluta", f"{dados['temp_maxima'].max():.1f}",  "°C",   CORES["temp_maxima"]),
        ("Mín. absoluta", f"{dados['temp_minima'].min():.1f}",  "°C",   CORES["temp_minima"]),
        ("Precip. total", f"{dados['chuva'].sum():.0f}", "mm", CORES["chuva"]),
        ("Umidade média", f"{dados['umidade'].mean():.0f}", "%",    CORES["umidade"]),
        ("Vento máx.",    f"{dados['vento'].max():.0f}",      "km/h", CORES["vento"]),
    ]
    for coluna, (lb, vl, un, cor) in zip(st.columns(6), indicadores):
        cartao_indicador(coluna, lb, vl, un, cor)
    st.markdown("<br>", unsafe_allow_html=True)

    # Temperatura
    st.markdown('<div class="titulo-secao">Temperatura</div>', unsafe_allow_html=True)
    grafico_temperatura = go.Figure()
    grafico_temperatura.add_trace(go.Scatter(x=dados_agregados.index, y=dados_agregados["temp_maxima"], name="Máxima",
        line=dict(color=CORES["temp_maxima"], width=1.5), mode="lines"))
    grafico_temperatura.add_trace(go.Scatter(x=dados_agregados.index, y=dados_agregados["temp_minima"], name="Mínima",
        line=dict(color=CORES["temp_minima"], width=1.5),
        fill="tonexty", fillcolor="rgba(56,189,248,0.07)", mode="lines"))
    grafico_temperatura.add_trace(go.Scatter(x=dados_agregados.index, y=dados_agregados["temp_media"], name="Média",
        line=dict(color=CORES["temp_media"], width=2, dash="dot"), mode="lines"))
    if comparar and ano_comparacao:
        duracao = data_fim - data_inicio
        try:
            inicio_cmp = data_inicio.replace(year=int(ano_comparacao))
        except ValueError:
            inicio_cmp = data_inicio.replace(year=int(ano_comparacao), day=28)
        fim_cmp = min(inicio_cmp + duracao, date(int(ano_comparacao), 12, 31))
        try:
            dados_comparacao = buscar_clima(lat, lon, inicio_cmp, fim_cmp)
            dados_comparacao_agregados = agregar(dados_comparacao, agregacao)
            idx_deslocado = dados_comparacao_agregados.index + (dados_agregados.index[0] - dados_comparacao_agregados.index[0])
            grafico_temperatura.add_trace(go.Scatter(x=idx_deslocado, y=dados_comparacao_agregados["temp_media"],
                name=f"Média {int(ano_comparacao)}",
                line=dict(color="#a78bfa", width=1.5, dash="dash"), mode="lines", opacity=0.75))
        except Exception as ex:
            st.warning(f"Não foi possível carregar dados de {int(ano_comparacao)}: {ex}")
    grafico_temperatura.update_layout(**LAYOUT_BASE, height=320, yaxis={**_YAXIS,"title":"°C"},
        legend=_LEGEND, title=_TITLE("Temperatura (°C)"))
    st.plotly_chart(grafico_temperatura, width="stretch")

    # Precipitação + Umidade
    coluna_a, coluna_b = st.columns(2)
    with coluna_a:
        st.markdown('<div class="titulo-secao">Precipitação</div>', unsafe_allow_html=True)
        rotulo = "diária" if agregacao == "Diário" else "acumulada"
        grafico_chuva = go.Figure()
        grafico_chuva.add_trace(go.Bar(x=dados_agregados.index, y=dados_agregados["chuva"], name="Chuva",
            marker_color=CORES["chuva"], opacity=0.85, marker_line_width=0))
        grafico_chuva.update_layout(**LAYOUT_BASE, height=280, yaxis={**_YAXIS,"title":"mm"},
            legend=_LEGEND, title=_TITLE(f"Precipitação {rotulo} (mm)"))
        st.plotly_chart(grafico_chuva, width="stretch")
    with coluna_b:
        st.markdown('<div class="titulo-secao">Umidade relativa</div>', unsafe_allow_html=True)
        grafico_umidade = go.Figure()
        grafico_umidade.add_trace(go.Scatter(x=dados_agregados.index, y=dados_agregados["umidade"], name="Umidade",
            line=dict(color=CORES["umidade"], width=2),
            fill="tozeroy", fillcolor="rgba(167,139,250,0.1)", mode="lines"))
        grafico_umidade.update_layout(**LAYOUT_BASE, height=280,
            yaxis={**_YAXIS,"title":"%","range":[0,105]}, legend=_LEGEND,
            title=_TITLE("Umidade relativa média (%)"))
        st.plotly_chart(grafico_umidade, width="stretch")

    # Chuva × Umidade
    st.markdown('<div class="titulo-secao">Chuva × umidade</div>', unsafe_allow_html=True)
    grafico_chuva_umidade = go.Figure()
    grafico_chuva_umidade.add_trace(go.Bar(x=dados_agregados.index, y=dados_agregados["chuva"], name="Precipitação (mm)",
        yaxis="y2", marker_color="rgba(0,229,255,0.4)", marker_line_width=0, opacity=0.8))
    grafico_chuva_umidade.add_trace(go.Scatter(x=dados_agregados.index, y=dados_agregados["umidade"], name="Umidade (%)",
        line=dict(color=CORES["umidade"], width=2.5),
        fill="tozeroy", fillcolor="rgba(167,139,250,0.08)", mode="lines"))
    grafico_chuva_umidade.update_layout(**LAYOUT_BASE, height=340, title=_TITLE("Relação entre chuva e umidade do ar"),
        yaxis={**_YAXIS,"title":"Umidade (%)","range":[0,105]},
        yaxis2={**_YAXIS2,"title":"Precipitação (mm)"}, legend=_LEGEND)
    st.plotly_chart(grafico_chuva_umidade, width="stretch")

    # Vento
    st.markdown('<div class="titulo-secao">Velocidade do vento</div>', unsafe_allow_html=True)
    grafico_vento = go.Figure()
    grafico_vento.add_trace(go.Scatter(x=dados_agregados.index, y=dados_agregados["vento"], name="Vento máx.",
        line=dict(color=CORES["vento"], width=1.5),
        fill="tozeroy", fillcolor="rgba(251,146,60,0.08)", mode="lines"))
    grafico_vento.update_layout(**LAYOUT_BASE, height=240, yaxis={**_YAXIS,"title":"km/h"},
        legend=_LEGEND, title=_TITLE("Velocidade máxima do vento (km/h)"))
    st.plotly_chart(grafico_vento, width="stretch")

    # Climatologia mensal
    st.markdown('<div class="titulo-secao">Climatologia mensal — período completo</div>', unsafe_allow_html=True)
    dados_mensais = dados.copy(); dados_mensais["mes"] = dados_mensais.index.month
    climatologia = dados_mensais.groupby("mes").agg(
        temp_maxima=("temp_maxima","mean"), temp_minima=("temp_minima","mean"),
        temp_media=("temp_media","mean"), chuva=("chuva","sum"),
    ).reset_index()
    climatologia["nome_mes"] = climatologia["mes"].map(MESES_PT)
    grafico_climatologia = go.Figure()
    grafico_climatologia.add_trace(go.Bar(x=climatologia["nome_mes"], y=climatologia["chuva"], name="Precipitação (mm)",
        yaxis="y2", marker_color="rgba(0,229,255,0.32)", marker_line_width=0))
    for coluna, rotulo, cor in [("temp_maxima","Temp. máxima",CORES["temp_maxima"]),
                             ("temp_media","Temp. média",CORES["temp_media"]),
                             ("temp_minima","Temp. mínima",CORES["temp_minima"])]:
        grafico_climatologia.add_trace(go.Scatter(x=climatologia["nome_mes"], y=climatologia[coluna], name=rotulo,
            line=dict(color=cor, width=2), mode="lines+markers", marker=dict(size=6)))
    grafico_climatologia.update_layout(**LAYOUT_BASE, height=340, title=_TITLE("Temperatura média e precipitação por mês"),
        yaxis={**_YAXIS,"title":"°C"}, yaxis2={**_YAXIS2,"title":"mm"}, legend=_LEGEND)
    st.plotly_chart(grafico_climatologia, width="stretch")

    with st.expander("Ver dados brutos"):
        dados_exibir = dados.copy().round(2)
        dados_exibir.index = dados_exibir.index.strftime("%d/%m/%Y")
        dados_exibir.index.name = "Data"
        ordem = ["temp_maxima","temp_minima","temp_media","chuva","vento","umidade","et0"]
        dados_exibir = dados_exibir[[c for c in ordem if c in dados_exibir.columns]]
        dados_exibir.columns = ["Temp. máx. (°C)","Temp. mín. (°C)","Temp. média (°C)",
            "Precipitação (mm)","Vento máx. (km/h)","Umidade média (%)","ET0 (mm)"][:len(dados_exibir.columns)]
        fmt = {c:"{:.2f}" for c in dados_exibir.columns}
        st.dataframe(dados_exibir.style.format(fmt), width="stretch")

# ═════════════════════════════════════════════════════════════════════ PREVISÃO ═
with tab_prev:
    st.markdown(f'<div class="titulo-secao">Próximos {dias_previsao} dias · {cidade}</div>',
                unsafe_allow_html=True)
    if modo_manual:
        st.info("A previsão vem da API online do Open-Meteo. No modo de atualização manual (CSV) ela "
                "fica indisponível — troque a fonte para Open-Meteo na barra lateral para usá-la.")
        previsao = None
    else:
        try:
            previsao = buscar_previsao(lat, lon, dias_previsao)
        except Exception as e:
            st.error(f"Não foi possível obter a previsão: {e}")
            previsao = None

    if previsao is not None and not previsao.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        n = min(len(previsao), 8)
        for coluna, (indice, linha) in zip(st.columns(n), previsao.head(n).iterrows()):
            grupo = GRUPO_TEMPO.get(int(linha.get("cod_tempo", 0)), "nuvem")
            probabilidade = linha.get("prob_chuva")
            probabilidade_txt = f"{int(probabilidade)}%" if pd.notna(probabilidade) else "—"
            coluna.markdown(f"""
            <div class="previsao">
              <div class="previsao-data">{MESES_PT[indice.month]} {indice.day:02d}</div>
              <div class="previsao-icone">{icone_tempo(grupo)}</div>
              <div class="previsao-tmax">{linha['temp_maxima']:.0f}°</div>
              <div class="previsao-tmin">{linha['temp_minima']:.0f}°</div>
              <div class="previsao-info"><b>chuva</b> {probabilidade_txt}<br><b>vento</b> {linha['vento']:.0f} km/h</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="titulo-secao">Temperatura e chuva previstas</div>', unsafe_allow_html=True)
        grafico_previsao = go.Figure()
        grafico_previsao.add_trace(go.Bar(x=previsao.index, y=previsao["chuva"], name="Chuva (mm)", yaxis="y2",
            marker_color="rgba(0,229,255,0.45)", marker_line_width=0))
        grafico_previsao.add_trace(go.Scatter(x=previsao.index, y=previsao["temp_maxima"], name="Máxima",
            line=dict(color=CORES["temp_maxima"], width=2), mode="lines+markers"))
        grafico_previsao.add_trace(go.Scatter(x=previsao.index, y=previsao["temp_minima"], name="Mínima",
            line=dict(color=CORES["temp_minima"], width=2), mode="lines+markers",
            fill="tonexty", fillcolor="rgba(56,189,248,0.06)"))
        grafico_previsao.update_layout(**LAYOUT_BASE, height=340, legend=_LEGEND, title=_TITLE("Previsão diária"),
            yaxis={**_YAXIS,"title":"°C"}, yaxis2={**_YAXIS2,"title":"mm"})
        st.plotly_chart(grafico_previsao, width="stretch")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="titulo-secao">Vento previsto</div>', unsafe_allow_html=True)
            grafico_vento_previsto = go.Figure()
            grafico_vento_previsto.add_trace(go.Scatter(x=previsao.index, y=previsao["vento"], name="Vento máx.",
                line=dict(color=CORES["vento"], width=2), mode="lines+markers",
                fill="tozeroy", fillcolor="rgba(251,146,60,0.08)"))
            grafico_vento_previsto.add_hline(y=10, line_dash="dash", line_color="#ff6b6b",
                annotation_text="Limite p/ pulverização (~10 km/h)",
                annotation_font_color="#ff6b6b", annotation_font_size=10)
            grafico_vento_previsto.update_layout(**LAYOUT_BASE, height=260, legend=_LEGEND,
                yaxis={**_YAXIS,"title":"km/h"}, title=_TITLE("Velocidade máx. do vento"))
            st.plotly_chart(grafico_vento_previsto, width="stretch")
        with col2:
            st.markdown('<div class="titulo-secao">Probabilidade de chuva</div>', unsafe_allow_html=True)
            grafico_prob_chuva = go.Figure()
            grafico_prob_chuva.add_trace(go.Bar(x=previsao.index, y=previsao.get("prob_chuva"), name="Prob. (%)",
                marker_color="rgba(0,229,255,0.5)", marker_line_width=0))
            grafico_prob_chuva.update_layout(**LAYOUT_BASE, height=260, legend=_LEGEND,
                yaxis={**_YAXIS,"title":"%","range":[0,105]}, title=_TITLE("Chance de precipitação"))
            st.plotly_chart(grafico_prob_chuva, width="stretch")

        st.markdown('<div class="titulo-secao">Alertas operacionais</div>', unsafe_allow_html=True)
        chuva_prev = previsao["chuva"].sum()
        et0_prev = previsao["et0"].sum() if "et0" in previsao.columns else 0.0
        balanco = chuva_prev - et0_prev
        bons = previsao[(previsao["chuva"] < 1.0) & (previsao["vento"] < 12)]
        chuva_forte = previsao[previsao["chuva"] >= 20]
        estresse = previsao[previsao["temp_maxima"] >= 34]
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
            <div class="alerta" style="border-left-color:{cor};">
              <div class="alerta-topo"><span class="alerta-ponto" style="background:{cor};"></span>
              <span class="alerta-titulo" style="color:{cor};">{titulo}</span></div>
              <div class="alerta-texto">{texto}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="nota" style="margin-top:8px;">Previsão de até 16 dias — quanto mais '
                    'distante o dia, maior a incerteza. Use os primeiros dias para decisões operacionais.</div>',
                    unsafe_allow_html=True)

        # ── Delta T — janela de pulverização hora a hora ────────────────────────
        st.markdown('<div class="titulo-secao" style="margin-top:22px;">Delta T · janela de '
                    'pulverização (próximas 96 h)</div>', unsafe_allow_html=True)
        try:
            previsao_horaria = buscar_previsao_horaria(lat, lon, 4)
        except Exception as e:
            previsao_horaria = None
            st.warning(f"Não foi possível obter a previsão horária para o Delta T: {e}")

        if previsao_horaria is not None and not previsao_horaria.empty:
            agora = pd.Timestamp.now().normalize()
            previsao_horaria = previsao_horaria[previsao_horaria.index >= agora].head(96)
            pct_ideal = float(previsao_horaria["delta_t"].between(*DELTA_T_IDEAL).mean() * 100)
            delta_t_agora = float(previsao_horaria["delta_t"].iloc[0])
            classe_nome, classe_cor = classificar_delta_t(delta_t_agora)
            indicadores_delta_t = [
                ("Delta T inicial", f"{delta_t_agora:.1f}", "°C · agora", classe_cor),
                ("Condição", classe_nome, "faixa atual", classe_cor),
                ("Horas ideais", f"{pct_ideal:.0f}", "% das próximas 96 h", "#2dd4a7"),
                ("Faixa ideal", "2–8", "°C (padrão BOM/GRDC)", "#00e5ff"),
            ]
            for coluna, (lb, vl, un, cor) in zip(st.columns(4), indicadores_delta_t):
                cartao_indicador(coluna, lb, vl, un, cor)
            st.markdown("<br>", unsafe_allow_html=True)

            grafico_delta_t = go.Figure()
            # faixas de referência
            grafico_delta_t.add_hrect(y0=2, y1=8, fillcolor="rgba(45,212,167,0.10)", line_width=0,
                             annotation_text="ideal 2–8", annotation_font_color="#2dd4a7",
                             annotation_font_size=10, annotation_position="top left")
            grafico_delta_t.add_hrect(y0=0, y1=2, fillcolor="rgba(251,146,60,0.08)", line_width=0)
            grafico_delta_t.add_hrect(y0=8, y1=10, fillcolor="rgba(251,146,60,0.08)", line_width=0)
            grafico_delta_t.add_trace(go.Scatter(x=previsao_horaria.index, y=previsao_horaria["delta_t"], name="Delta T",
                line=dict(color="#00e5ff", width=2), mode="lines"))
            grafico_delta_t.add_trace(go.Scatter(x=previsao_horaria.index, y=previsao_horaria["vento"], name="Vento (km/h)", yaxis="y2",
                line=dict(color="#fb923c", width=1, dash="dot"), mode="lines", opacity=0.7))
            grafico_delta_t.update_layout(**LAYOUT_BASE, height=320, legend=_LEGEND,
                title=_TITLE("Delta T e vento hora a hora"),
                yaxis={**_YAXIS, "title": "Delta T (°C)"}, yaxis2={**_YAXIS2, "title": "Vento (km/h)"})
            st.plotly_chart(grafico_delta_t, width="stretch")

            janelas = janelas_pulverizacao(previsao_horaria)
            dias_semana = {0:"Seg",1:"Ter",2:"Qua",3:"Qui",4:"Sex",5:"Sáb",6:"Dom"}
            if janelas:
                itens = []
                for ini, fim in janelas[:8]:
                    dia = f"{dias_semana[ini.weekday()]} {ini.day:02d}/{ini.month:02d}"
                    itens.append(f"{dia}: {ini.hour:02d}h–{(fim.hour+1):02d}h")
                texto = " · ".join(itens)
                st.markdown(f"""
                <div class="alerta" style="border-left-color:#2dd4a7;">
                  <div class="alerta-topo"><span class="alerta-ponto" style="background:#2dd4a7;"></span>
                  <span class="alerta-titulo" style="color:#2dd4a7;">Melhores janelas para pulverizar</span></div>
                  <div class="alerta-texto">{texto}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alerta" style="border-left-color:#fb923c;">
                  <div class="alerta-topo"><span class="alerta-ponto" style="background:#fb923c;"></span>
                  <span class="alerta-titulo" style="color:#fb923c;">Sem janela ideal nas próximas 96 h</span></div>
                  <div class="alerta-texto">Delta T, vento ou chuva fora da faixa recomendada. Reavalie
                  nas primeiras horas da manhã ou fim de tarde, quando o Delta T costuma cair.</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="nota" style="margin-top:8px;">Delta T = temperatura do ar − '
                        'temperatura de bulbo úmido (fórmula de Stull, 2011). Janela boa = Delta T entre '
                        '2 e 8 °C, vento de 3 a 15 km/h e sem chuva. É um guia; confira sempre o rótulo do '
                        'produto e as condições no talhão.</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════ CALENDÁRIO AGRÍCOLA ═
with tab_cal:
    st.markdown(f'<div class="titulo-secao">Sucessão soja → milho safrinha · '
                f'ajustado à chuva de {cidade}</div>', unsafe_allow_html=True)

    # Climatologia mensal de chuva da cidade (média do total mensal entre os anos do período)
    mensal = dados["chuva"].resample("ME").sum()
    precip_mes = mensal.groupby(mensal.index.month).mean().reindex(range(1, 13))
    meses_com_dado = int(precip_mes.notna().sum())

    estacao = detectar_estacao(precip_mes, limiar_chuva)
    inicio_mes, fim_mes, regime = estacao["inicio"], estacao["fim"], estacao["regime"]
    inicio_dia_do_ano = date(ANO_BASE, inicio_mes, 1).timetuple().tm_yday

    def mes_do_offset(off):
        return MESES_PT[dia_do_ano_para_data(inicio_dia_do_ano + off).month]

    # Monta as fases do sistema ancoradas no início das chuvas detectado
    linhas = []
    for comp, info in SISTEMA.items():
        for nome_fase, ini_off, fim_off in info["fases"]:
            for ini, fim in fase_dias_para_segmentos(inicio_dia_do_ano, ini_off, fim_off):
                linhas.append({"Atividade": f"{comp} · {nome_fase}", "Componente": comp,
                               "Início": ini, "Fim": fim})
    dados_calendario = pd.DataFrame(linhas)

    cores_comp = {c: info["cor"] for c, info in SISTEMA.items()}
    grafico_calendario = px.timeline(dados_calendario, x_start="Início", x_end="Fim", y="Atividade", color="Componente",
        color_discrete_map=cores_comp, category_orders={"Atividade": ORDEM_ATIVIDADES})
    grafico_calendario.update_yaxes(autorange="reversed", title=None, gridcolor="#16305a")
    grafico_calendario.update_xaxes(gridcolor="#16305a",
        range=[pd.Timestamp(ANO_BASE, 1, 1), pd.Timestamp(ANO_BASE, 12, 31)],
        tickvals=[pd.Timestamp(ANO_BASE, m, 1) for m in range(1, 13)],
        ticktext=[MESES_PT[m] for m in range(1, 13)])

    # Faixa sombreada = estação chuvosa detectada
    for ini_s, fim_s in fase_para_segmentos(inicio_mes, 1, fim_mes, 28):
        grafico_calendario.add_vrect(x0=pd.Timestamp(ini_s), x1=pd.Timestamp(fim_s) + pd.Timedelta(days=1),
            fillcolor="rgba(0,229,255,0.06)", line_width=0, layer="below")

    hoje_base = pd.Timestamp(ANO_BASE, date.today().month, date.today().day)
    grafico_calendario.add_vline(x=hoje_base, line_color="#2dd4a7", line_width=2,
        annotation_text="hoje", annotation_font_color="#2dd4a7")
    grafico_calendario.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8f4fd", family="DM Sans", size=12), height=440,
        margin=dict(l=10, r=10, t=34, b=10), legend=_LEGEND,
        title=_TITLE("Faixa azul = estação chuvosa detectada · plantio ancorado no início das chuvas"))
    st.plotly_chart(grafico_calendario, width="stretch")

    # Parâmetros detectados (KPIs)
    dur_dias = estacao["duracao"] * 30
    indicadores_calendario = [
        ("Início das chuvas", MESES_PT[inicio_mes], "plantio da soja", "#00e5ff"),
        ("Fim das chuvas",    MESES_PT[fim_mes],   "fim do período úmido", "#a78bfa"),
        ("Estação chuvosa",   f"{estacao['duracao']}",  "meses úmidos", "#2dd4a7"),
        ("Colheita da soja",  mes_do_offset(120),  "≈ 118 dias após plantio", "#2dd4a7"),
        ("Colheita do milho", mes_do_offset(270),  "milho safrinha", "#ffd166"),
    ]
    for coluna, (lb, vl, un, cor) in zip(st.columns(5), indicadores_calendario):
        cartao_indicador(coluna, lb, vl, un, cor)
    st.markdown("<br>", unsafe_allow_html=True)

    # Cartões do sistema (datas derivadas)
    resumo = {
        "Soja": ("#2dd4a7", f"Plantio no início das chuvas ({MESES_PT[inicio_mes]}), ciclo de "
                            f"~118 dias, colheita por volta de {mes_do_offset(120)}. É a cultura que "
                            f"abre o sistema e paga a safra."),
        "Milho safrinha": ("#ffd166", f"Semeado logo após a colheita da soja (~{mes_do_offset(135)}); "
                            f"colheita do grão em torno de {mes_do_offset(270)}. Aproveita o fim das "
                            f"chuvas, então quanto mais cedo entrar, menor o risco hídrico."),
    }
    for coluna, (cult, (cor, texto)) in zip(st.columns(2), resumo.items()):
        coluna.markdown(f"""
        <div class="cartao-cultura">
          <div class="cultura-topo"><span class="cultura-ponto" style="background:{cor};"></span>{cult}</div>
          <div class="cultura-corpo">{texto}</div>
        </div>""", unsafe_allow_html=True)

    # Alertas adaptativos derivados do regime de chuva
    st.markdown('<div class="titulo-secao" style="margin-top:18px;">Leitura do regime</div>',
                unsafe_allow_html=True)
    avisos = []
    if meses_com_dado < 12:
        avisos.append(("#fb923c", "Período curto para climatologia",
            f"O período selecionado cobre {meses_com_dado} de 12 meses. Para um calendário "
            f"confiável, selecione pelo menos 1–2 anos completos na barra lateral."))
    if regime == "umido":
        avisos.append(("#00e5ff", "Chuva o ano todo",
            "Todos os meses superam o limiar — janela de plantio flexível. O cuidado migra para "
            "doenças e para a colheita em período úmido; priorize cultivares resistentes."))
    elif regime == "seco":
        avisos.append(("#ff6b6b", "Chuva insuficiente para sequeiro",
            f"Nenhum mês atinge {limiar_chuva} mm com o limiar atual. O sistema em sequeiro é "
            f"arriscado nesta cidade — considere irrigação ou reduza o limiar para inspecionar."))
    else:
        if dur_dias >= 240:
            avisos.append(("#2dd4a7", "Janela favorável ao sistema completo",
                f"A estação chuvosa dura ~{estacao['duracao']} meses, suficiente para soja + milho "
                f"safrinha com risco hídrico baixo."))
        elif dur_dias >= 150:
            avisos.append(("#fb923c", "Milho safrinha com risco no enchimento",
                f"A estação dura ~{estacao['duracao']} meses: o enchimento de grão do milho pode pegar o "
                f"fim das chuvas. Favoreça cultivares precoces e antecipe ao máximo o plantio da soja "
                f"para liberar a área mais cedo."))
        else:
            avisos.append(("#ff6b6b", "Estação chuvosa curta",
                f"Com ~{estacao['duracao']} meses úmidos, sobra pouca janela após a soja. O milho "
                f"safrinha fica arriscado — avalie ficar só com a soja ou irrigar a segunda safra."))
    for cor, titulo, texto in avisos:
        st.markdown(f"""
        <div class="alerta" style="border-left-color:{cor};">
          <div class="alerta-topo"><span class="alerta-ponto" style="background:{cor};"></span>
          <span class="alerta-titulo" style="color:{cor};">{titulo}</span></div>
          <div class="alerta-texto">{texto}</div>
        </div>""", unsafe_allow_html=True)

    # ── El Niño / La Niña (ENOS) ────────────────────────────────────────────────
    st.markdown('<div class="titulo-secao" style="margin-top:18px;">El Niño / La Niña (ENOS)</div>',
                unsafe_allow_html=True)
    info_enos = ENOS_INFO[enos_fase]
    rotulo_int = "" if enos_fase == "Neutro" else f" · intensidade {enos_int.lower()}"
    st.markdown(f"""
    <div class="alerta" style="border-left-color:{info_enos['cor']};">
      <div class="alerta-topo"><span class="alerta-ponto" style="background:{info_enos['cor']};"></span>
      <span class="alerta-titulo" style="color:{info_enos['cor']};">{info_enos['titulo']}{rotulo_int}</span></div>
      <div class="alerta-texto">{info_enos['texto']}</div>
    </div>""", unsafe_allow_html=True)
    if enos_fase != "Neutro":
        if enos_fase == "El Niño":
            extra = ("Com El Niño, a estação chuvosa detectada acima tende a chegar mais tarde e/ou "
                     "render menos que a média histórica — trate a janela como um teto otimista.")
        else:
            extra = ("Com La Niña, a chuva tende a superar a média histórica — a janela detectada é "
                     "conservadora, mas vigie o excesso na colheita.")
        st.markdown(f'<div class="nota" style="margin-top:2px;">{extra}</div>', unsafe_allow_html=True)

    st.markdown('<div class="nota" style="margin-top:12px;">O início das chuvas é detectado pela '
                'climatologia de precipitação da cidade selecionada (ajuste o limiar na barra '
                'lateral). A fase do ENOS é informada manualmente (barra lateral), lida do boletim do '
                'CPTEC/INPE, INMET ou NOAA. As durações de ciclo são típicas; confirme as datas no '
                'ZARC do município antes de plantar.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════ CALENDÁRIO LUNAR ═
with tab_lua:
    st.markdown('<div class="titulo-secao">Fase da lua e manejo (tradição agrícola brasileira)</div>',
                unsafe_allow_html=True)
    idade = idade_lunar()
    nome_lua, iluminacao, fracao_lua = fase_lunar(idade)
    cor_lua = FASES_LUA[nome_lua]["cor"]

    coluna_lua, coluna_texto = st.columns([1, 2.4])
    with coluna_lua:
        st.markdown(f"""
        <div style="text-align:center;padding:8px 0;">
          {desenhar_lua_svg(iluminacao, fracao_lua, 130)}
          <div style="font-family:'Space Mono',monospace;font-size:1.15rem;color:{cor_lua};margin-top:8px;">{nome_lua}</div>
          <div class="nota">{iluminacao*100:.0f}% iluminada · {idade:.0f} dias de idade</div>
        </div>""", unsafe_allow_html=True)
    with coluna_texto:
        st.markdown(f"""
        <div class="cartao-cultura" style="height:100%;">
          <div class="cultura-topo"><span class="cultura-ponto" style="background:{cor_lua};"></span>Manejo indicado agora</div>
          <div class="cultura-corpo">{LUA_MANEJO[nome_lua]}</div>
          <div class="cultura-corpo" style="margin-top:10px;color:#e8f4fd;">
            Para <b>grãos (soja e milho)</b>, esta fase é
            <b style="color:{cor_lua};">{LUA_GRAOS[nome_lua]}</b>.
            A tradição planta grãos na <b>crescente</b> e colhe na <b>cheia</b>.
          </div>
        </div>""", unsafe_allow_html=True)

    # Próximas fases principais
    st.markdown('<div class="titulo-secao" style="margin-top:18px;">Próximas fases</div>',
                unsafe_allow_html=True)
    principais = [("Nova", 0.0, "#7ba3c8"), ("Quarto crescente", 0.25, "#2dd4a7"),
                  ("Cheia", 0.5, "#ffd166"), ("Quarto minguante", 0.75, "#fb923c")]
    dias_pt = {0:"Seg",1:"Ter",2:"Qua",3:"Qui",4:"Sex",5:"Sáb",6:"Dom"}
    for coluna, (nome_p, fr_p, cor_p) in zip(st.columns(4), principais):
        d = proxima_fase_principal(fr_p)
        cartao_indicador(coluna, nome_p, d.strftime("%d/%m"), dias_pt[d.weekday()], cor_p)

    # Calendário do ciclo lunar atual (mini timeline)
    st.markdown('<div class="titulo-secao" style="margin-top:18px;">O que a tradição indica em cada fase</div>',
                unsafe_allow_html=True)
    for coluna, fase in zip(st.columns(4), ["Nova", "Crescente", "Cheia", "Minguante"]):
        cor_f = FASES_LUA[fase]["cor"]
        atual = " (agora)" if fase == nome_lua else ""
        coluna.markdown(f"""
        <div class="cartao-cultura" style="height:100%;">
          <div class="cultura-topo"><span class="cultura-ponto" style="background:{cor_f};"></span>{fase}{atual}</div>
          <div class="cultura-corpo">{LUA_MANEJO[fase]}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nota" style="margin-top:14px;">O calendário lunar de plantio é uma '
                'tradição do campo brasileiro, baseada na observação de gerações. Não há comprovação '
                'científica robusta de efeito das fases da lua na produtividade — fatores como solo, '
                'chuva, adubação e cultivar têm peso muito maior. Use como complemento cultural às '
                'outras abas, não como regra isolada. Fases calculadas astronomicamente (sem API).</div>',
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════ PAINEL AGRONÔMICO ═
with tab_agro:
    st.markdown(f'<div class="titulo-secao">Indicadores · período selecionado · '
                f'referência: {cultura_ref}</div>', unsafe_allow_html=True)
    temp_base = CULTURAS[cultura_ref]["temp_base"]
    gdd_ciclo = CULTURAS[cultura_ref]["gdd_ciclo"]
    cor_cultura = CULTURAS[cultura_ref]["cor"]

    gdd_acumulado = calcular_gdd(dados, temp_base).cumsum()
    gdd_total = float(gdd_acumulado.iloc[-1]) if len(gdd_acumulado) else 0.0
    balanco_acumulado = (dados["chuva"] - dados["et0"]).cumsum() if "et0" in dados.columns else dados["chuva"].cumsum()*0
    balanco_total = float(balanco_acumulado.iloc[-1]) if len(balanco_acumulado) else 0.0
    dias_estresse = int((dados["temp_maxima"] >= 34).sum())
    veranico = maior_veranico(dados["chuva"])
    pct_ciclo = min(gdd_total / gdd_ciclo * 100, 999) if gdd_ciclo else 0

    indicadores_agro = [
        ("GDD acumulado",  f"{gdd_total:.0f}",   f"°C·dia · {cultura_ref}", cor_cultura),
        ("Equiv. ciclo",   f"{pct_ciclo:.0f}",   f"% de {gdd_ciclo} °C·dia", "#ffd166"),
        ("Balanço hídrico",f"{balanco_total:+.0f}", "mm · chuva − ET0",      "#00e5ff"),
        ("Dias ≥ 34 °C",   f"{dias_estresse}",   "estresse térmico",         "#ff6b6b"),
        ("Maior veranico", f"{veranico}",        "dias secos seguidos",      "#fb923c"),
    ]
    for coluna, (lb, vl, un, cor) in zip(st.columns(5), indicadores_agro):
        cartao_indicador(coluna, lb, vl, un, cor)
    st.markdown("<br>", unsafe_allow_html=True)

    coluna_gdd, coluna_b = st.columns(2)
    with coluna_gdd:
        st.markdown('<div class="titulo-secao">Graus-dia acumulados (GDD)</div>', unsafe_allow_html=True)
        grafico_gdd = go.Figure()
        grafico_gdd.add_trace(go.Scatter(x=gdd_acumulado.index, y=gdd_acumulado.values, name="GDD acumulado",
            line=dict(color=cor_cultura, width=2.5), fill="tozeroy",
            fillcolor="rgba(45,212,167,0.08)", mode="lines"))
        grafico_gdd.add_hline(y=gdd_ciclo, line_dash="dash", line_color="#ffd166",
            annotation_text=f"Ciclo {cultura_ref} (~{gdd_ciclo})",
            annotation_font_color="#ffd166", annotation_font_size=10)
        grafico_gdd.update_layout(**LAYOUT_BASE, height=320, legend=_LEGEND, yaxis={**_YAXIS,"title":"°C·dia"},
            title=_TITLE(f"Acúmulo térmico · Tbase {temp_base:.0f} °C"))
        st.plotly_chart(grafico_gdd, width="stretch")
        st.markdown('<div class="nota">O GDD indica em que fase a cultura está e quando deve '
                    'florescer/maturar. O acúmulo soma todo o período selecionado — para um único '
                    'ciclo, escolha um período a partir da data de plantio.</div>', unsafe_allow_html=True)
    with coluna_b:
        st.markdown('<div class="titulo-secao">Balanço hídrico acumulado</div>', unsafe_allow_html=True)
        grafico_balanco = go.Figure()
        grafico_balanco.add_trace(go.Scatter(x=balanco_acumulado.index, y=balanco_acumulado.values, name="Balanço (mm)",
            line=dict(color="#00e5ff", width=2.5), fill="tozeroy",
            fillcolor="rgba(0,229,255,0.08)", mode="lines"))
        grafico_balanco.add_hline(y=0, line_color="#7ba3c8", line_width=1)
        grafico_balanco.update_layout(**LAYOUT_BASE, height=320, legend=_LEGEND, yaxis={**_YAXIS,"title":"mm"},
            title=_TITLE("Chuva − evapotranspiração (ET0)"))
        st.plotly_chart(grafico_balanco, width="stretch")
        st.markdown('<div class="nota">Acima de zero, sobra água no sistema; abaixo, há déficit e a '
                    'planta depende da reserva do solo ou de irrigação.</div>', unsafe_allow_html=True)

    st.markdown('<div class="titulo-secao">Leitura rápida</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="leitura">• ' + "<br>• ".join(leitura) + "</div>", unsafe_allow_html=True)

    st.markdown('<div class="nota" style="margin-top:12px;">Tbase e GDD de ciclo são valores de '
                'referência; ajuste à cultivar específica. ET0 é a evapotranspiração de referência '
                '(FAO Penman-Monteith) fornecida pela API.</div>', unsafe_allow_html=True)
