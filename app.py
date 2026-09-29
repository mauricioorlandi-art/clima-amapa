<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clima Amapá</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--fundo:#0a1628;--sup:#0f2040;--sup2:#13284c;--linha:#1e3a64;--dest:#00e5ff;--texto:#e8f4fd;--suave:#7ba3c8;--tenue:#4d6b94;--tmax:#ff6b6b;--tmin:#38bdf8;--tmed:#ffd166;--umid:#a78bfa;--vento:#fb923c;--ok:#2dd4a7}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(1100px 460px at 18% -8%,rgba(0,229,255,.07),transparent 60%),var(--fundo);color:var(--texto);font-family:'DM Sans',sans-serif;display:flex;min-height:100vh}
h1,h2,h3,.mono{font-family:'Space Mono',monospace}
aside{width:290px;flex:none;background:linear-gradient(180deg,#0a1f3d,#071530);border-right:1px solid var(--linha);padding:20px 18px;position:sticky;top:0;height:100vh;overflow:auto}
main{flex:1;min-width:0;padding:24px 30px}
.marca{font-family:'Space Mono',monospace;font-weight:700;font-size:1.05rem}
.marca small{display:block;font-weight:400;font-size:.62rem;color:var(--tenue);margin-top:3px}
aside label{display:block;font-family:'Space Mono',monospace;font-size:.66rem;color:var(--suave);margin:14px 0 5px}
aside hr{border:0;border-top:1px solid #16305a;margin:14px 0}
select,input,textarea,button{background:var(--sup2);border:1px solid var(--linha);color:var(--texto);border-radius:8px;padding:8px;font:inherit;width:100%}
input[type=checkbox],input[type=radio]{width:auto}
button{cursor:pointer;width:auto;padding:8px 14px}
button:hover{border-color:var(--dest)}
.par{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.capa{padding:26px 32px;border:1px solid var(--linha);border-radius:18px;margin-bottom:22px;background:linear-gradient(135deg,rgba(15,32,64,.9),rgba(19,40,76,.6))}
.capa h1{font-size:2.3rem;margin:8px 0 12px}
.capa .info{font-family:'Space Mono',monospace;font-size:.8rem;color:var(--suave)}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--linha);margin-bottom:20px;flex-wrap:wrap}
.tabs button{background:transparent;border:0;border-bottom:2px solid transparent;border-radius:0;color:var(--tenue);font-family:'Space Mono',monospace;font-size:.74rem;padding:10px 16px}
.tabs button.on{color:var(--dest);border-bottom-color:var(--dest)}
section{display:none}section.on{display:block}
.sec{font-family:'Space Mono',monospace;font-size:.72rem;color:var(--suave);margin:18px 0 12px;border-left:2px solid var(--dest);padding-left:11px}
.grade{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.kpi{background:var(--sup);border:1px solid var(--linha);border-top-width:3px;border-radius:13px;padding:14px}
.kpi .r{font-family:'Space Mono',monospace;font-size:.62rem;color:var(--suave)}
.kpi .v{font-family:'Space Mono',monospace;font-weight:700;font-size:1.5rem;margin-top:6px}
.kpi .u{font-size:.66rem;color:var(--tenue)}
.g{position:relative;height:300px;margin-bottom:8px}
.duas{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.prev{background:var(--sup);border:1px solid var(--linha);border-radius:13px;padding:12px 6px;text-align:center}
.prev .d{font-family:'Space Mono',monospace;font-size:.66rem;color:var(--suave)}
.prev .mx{font-family:'Space Mono',monospace;font-weight:700;color:var(--tmax)}
.prev .mn{font-family:'Space Mono',monospace;color:var(--tmin)}
.prev .i{font-size:.62rem;color:var(--tenue);margin-top:5px}
.alerta{background:var(--sup);border:1px solid var(--linha);border-left-width:3px;border-radius:11px;padding:12px 16px;margin-bottom:9px}
.alerta b.t{font-family:'Space Mono',monospace;font-size:.72rem}
.alerta p{margin:6px 0 0;font-size:.86rem;line-height:1.55}
.cartao{background:var(--sup);border:1px solid var(--linha);border-radius:13px;padding:15px 17px;font-size:.82rem;line-height:1.6;color:var(--suave)}
.cartao h3{margin:0 0 6px;font-size:.92rem;color:var(--texto)}
.nota{color:var(--tenue);font-size:.74rem;line-height:1.5;margin-top:8px}
.tl{display:grid;grid-template-columns:150px 1fr;gap:6px 10px;align-items:center;font-size:.72rem;color:var(--suave);margin-bottom:14px}
.trilho{position:relative;height:20px;background:rgba(255,255,255,.03);border-radius:4px}
.trilho i{position:absolute;top:0;bottom:0;border-radius:4px}
.meses{display:grid;grid-template-columns:repeat(12,1fr);font-size:.62rem;color:var(--tenue)}
#manual{display:none;margin-bottom:18px}
@media(max-width:820px){body{flex-direction:column}aside{width:100%;height:auto;position:static}.duas{grid-template-columns:1fr}}
</style>
</head>
<body>
<aside>
  <div class="marca">CLIMA AMAPÁ<small>PAINEL CLIMÁTICO</small></div>
  <label>Cidade</label><select id="cidade"></select>
  <label>Período de análise</label>
  <div class="par"><input type="date" id="ini"><input type="date" id="fim"></div>
  <label>Agregação</label>
  <select id="agr"><option>Diário</option><option>Semanal</option><option>Mensal</option></select>
  <hr>
  <label>Cultura de referência (GDD)</label><select id="cultura"><option>Soja</option><option>Milho</option></select>
  <label>Mês chuvoso a partir de (mm): <span id="limv">100</span></label>
  <input type="range" id="lim" min="50" max="200" step="10" value="100">
  <label>Horizonte da previsão (dias)</label>
  <select id="dias"><option>7</option><option>10</option><option selected>14</option><option>16</option></select>
  <hr>
  <label>Fonte dos dados</label>
  <select id="fonte"><option value="api">Open-Meteo (API)</option><option value="manual">Inserir manualmente</option></select>
  <label>Fase do ENOS</label>
  <select id="enos"><option>Neutro</option><option>El Niño</option><option>La Niña</option></select>
  <p class="nota" id="nuvem">Armazenamento: local (Firebase não configurado)</p>
</aside>
<main>
  <div class="capa">
    <div class="mono" style="font-size:.68rem;color:var(--dest)">Painel climático · Amapá · Brasil</div>
    <h1>CLIMA AMAPÁ</h1>
    <div class="info" id="info"></div>
  </div>
  <div id="manual">
    <div class="sec">Dados manuais (CSV colado)</div>
    <textarea id="txt" rows="7" placeholder="data;temp_maxima;temp_minima;chuva;vento;umidade;et0&#10;01/07/2026;32,1;23,0;0;9;78;4,6"></textarea>
    <p class="nota">Obrigatórias: data, temp_maxima, temp_minima, chuva. Aceita separador ; ou , e data dd/mm/aaaa ou aaaa-mm-dd.</p>
    <button id="aplicar">Aplicar e salvar</button>
  </div>
  <div id="erro" class="alerta" style="display:none;border-left-color:var(--tmax)"></div>
  <nav class="tabs" id="tabs"></nav>
  <section id="s-hist"><div class="sec">Resumo do período</div><div class="grade" id="k-hist"></div>
    <div class="sec">Temperatura</div><div class="g"><canvas id="c-temp"></canvas></div>
    <div class="duas"><div><div class="sec">Precipitação</div><div class="g"><canvas id="c-chuva"></canvas></div></div>
    <div><div class="sec">Umidade relativa</div><div class="g"><canvas id="c-umid"></canvas></div></div></div>
    <div class="sec">Velocidade do vento</div><div class="g"><canvas id="c-vento"></canvas></div>
    <div class="sec">Climatologia mensal</div><div class="g"><canvas id="c-clim"></canvas></div>
  </section>
  <section id="s-prev"><div class="sec" id="t-prev"></div>
    <div class="grade" id="cards-prev" style="grid-template-columns:repeat(auto-fit,minmax(90px,1fr))"></div>
    <div class="sec">Temperatura e chuva previstas</div><div class="g"><canvas id="c-prev"></canvas></div>
    <div id="al-prev"></div>
    <div class="sec">Delta T · janela de pulverização (96 h)</div><div class="grade" id="k-dt"></div>
    <div class="g" style="margin-top:12px"><canvas id="c-dt"></canvas></div><div id="al-dt"></div>
    <p class="nota">Delta T = temperatura do ar − bulbo úmido (Stull, 2011). Janela boa: Delta T 2–8 °C, vento 3–15 km/h, sem chuva.</p>
  </section>
  <section id="s-cal"><div class="sec" id="t-cal"></div><div id="tl"></div><div class="grade" id="k-cal"></div>
    <div class="sec">Leitura do regime</div><div id="al-cal"></div>
    <div class="sec">El Niño / La Niña (ENOS)</div><div id="al-enos"></div>
    <p class="nota">Início das chuvas detectado pela climatologia da cidade. Confirme as datas no ZARC do município antes de plantar.</p>
  </section>
  <section id="s-lua"><div class="sec">Fase da lua e manejo (tradição agrícola brasileira)</div>
    <div style="display:grid;grid-template-columns:160px 1fr;gap:20px;align-items:center"><div id="lua" style="text-align:center"></div><div class="cartao" id="lua-txt"></div></div>
    <div class="sec">Próximas fases</div><div class="grade" id="k-lua"></div>
    <p class="nota">Tradição do campo, sem comprovação científica robusta de efeito na produtividade. Use como complemento cultural.</p>
  </section>
  <section id="s-agro"><div class="sec" id="t-agro"></div><div class="grade" id="k-agro"></div>
    <div class="duas" style="margin-top:14px"><div><div class="sec">GDD acumulado</div><div class="g"><canvas id="c-gdd"></canvas></div></div>
    <div><div class="sec">Balanço hídrico acumulado</div><div class="g"><canvas id="c-bal"></canvas></div></div></div>
    <div class="sec">Leitura rápida</div><div class="cartao" id="leitura"></div>
  </section>
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script type="module">
/* ── Firebase (opcional): cole aqui o firebaseConfig do seu app web ── */
const FB_CONFIG = null; // ex.: { apiKey:"...", authDomain:"...", projectId:"...", appId:"..." }
let db = null, fs = null;
async function iniciarFirebase() {
  if (!FB_CONFIG) return;
  try {
    const { initializeApp } = await import("https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js");
    fs = await import("https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js");
    db = fs.getFirestore(initializeApp(FB_CONFIG));
    $("#nuvem").textContent = "Armazenamento: Firestore conectado";
  } catch (e) { console.warn("Firebase indisponível:", e); }
}
async function salvar(k, v) {
  localStorage.setItem(k, JSON.stringify(v));
  if (db) try { await fs.setDoc(fs.doc(db, "clima_amapa", k), { valor: JSON.stringify(v), atualizado: fs.serverTimestamp() }); } catch (e) { console.warn(e); }
}
async function carregar(k) {
  if (db) try { const s = await fs.getDoc(fs.doc(db, "clima_amapa", k)); if (s.exists()) return JSON.parse(s.data().valor); } catch (e) {}
  const l = localStorage.getItem(k); return l ? JSON.parse(l) : null;
}

/* ── Utilitários ── */
const $ = s => document.querySelector(s);
const fmt = (v, c = 1) => v == null || isNaN(v) ? "—" : (+v).toFixed(c);
const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, 0)}-${String(d.getDate()).padStart(2, 0)}`;
const addDias = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
const ok = a => a.filter(v => v != null && !isNaN(v));
const media = a => { a = ok(a); return a.length ? a.reduce((x, y) => x + y, 0) / a.length : null; };
const soma = a => ok(a).reduce((x, y) => x + y, 0);
const MES = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"];
const CIDADES = { "Macapá":[0.0349,-51.0694], "Santana":[-0.0589,-51.1783], "Laranjal do Jari":[-0.8022,-52.4619],
  "Oiapoque":[3.8411,-51.8339], "Amapá":[2.0522,-50.7961], "Tartarugalzinho":[1.5056,-50.9072] };
const CULT = { Soja:{base:10,gdd:1400,cor:"#2dd4a7"}, Milho:{base:10,gdd:1500,cor:"#ffd166"} };
const SISTEMA = { "Soja":{cor:"#2dd4a7",fases:[["Plantio",0,35],["Ciclo",0,118],["Colheita",108,135]]},
  "Milho safrinha":{cor:"#ffd166",fases:[["Plantio",128,158],["Ciclo",128,260],["Colheita",250,282]]} };
const ENOS = {
  "Neutro":{cor:"#7ba3c8",t:"ENOS neutro",x:"Sem El Niño nem La Niña ativos: espere o padrão climatológico normal. Siga a janela de plantio detectada pela chuva histórica."},
  "El Niño":{cor:"#ff6b6b",t:"El Niño ativo",x:"No Norte o El Niño tende a reduzir a chuva e intensificar a estação seca. Risco maior para sequeiro: cultivares precoces, atenção à irrigação e não atrase a soja."},
  "La Niña":{cor:"#2dd4a7",t:"La Niña ativa",x:"No Norte a La Niña tende a aumentar a chuva. Bom para o enchimento hídrico, mas atenção a encharcamento, doenças e colheita em período úmido."} };
const LUA = { Nova:["#7ba3c8","Preparo do solo, adubação e controle de pragas. Semeadura fraca.","aceitável"],
  Crescente:["#2dd4a7","Indicada para o que cresce acima do solo: grãos, folhas e frutos. Janela preferida para semear grãos.","favorável"],
  Cheia:["#ffd166","Melhor período para colheita. Evita-se semear e podar.","colheita"],
  Minguante:["#fb923c","Raízes, tubérculos, podas e preparo. Menos indicada para grãos.","desfavorável"] };

/* ── Gráficos ── */
Chart.defaults.color = "#7ba3c8"; Chart.defaults.font.family = "DM Sans";
const CH = {};
const L = (label, data, cor, x = {}) => ({ label, data, borderColor: cor, backgroundColor: cor + "22", borderWidth: 2, pointRadius: 0, tension: .2, ...x });
function graf(id, tipo, labels, ds, y2 = false) {
  CH[id]?.destroy();
  const eixo = { ticks: { color: "#7ba3c8", maxTicksLimit: 10 }, grid: { color: "#16305a" } };
  CH[id] = new Chart($("#" + id), { type: tipo, data: { labels, datasets: ds }, options: {
    responsive: true, maintainAspectRatio: false, interaction: { mode: "index", intersect: false },
    plugins: { legend: { labels: { color: "#e8f4fd" } } },
    scales: { x: eixo, y: eixo, ...(y2 ? { y2: { position: "right", grid: { display: false }, ticks: { color: "#7ba3c8" } } } : {}) } } });
}
const kpi = (r, v, u, cor) => `<div class="kpi" style="border-top-color:${cor}"><div class="r">${r}</div><div class="v">${v}</div><div class="u">${u}</div></div>`;
const alerta = (cor, t, x) => `<div class="alerta" style="border-left-color:${cor}"><b class="t" style="color:${cor}">${t}</b><p>${x}</p></div>`;

/* ── API ── */
const J = async u => { const r = await fetch(u); if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); };
const umidDia = h => { const m = {}; h.time.forEach((t, k) => (m[t.slice(0, 10)] ??= []).push(h.relative_humidity_2m[k])); return m; };
async function arquivo(c, i, f) {
  const d = (await J(`https://archive-api.open-meteo.com/v1/archive?latitude=${c[0]}&longitude=${c[1]}&start_date=${i}&end_date=${f}&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min,et0_fao_evapotranspiration&timezone=America/Belem`)).daily;
  return d.time.map((t, k) => ({ d: t, tmax: d.temperature_2m_max[k], tmin: d.temperature_2m_min[k], tmed: d.temperature_2m_mean[k], chuva: d.precipitation_sum[k], vento: d.windspeed_10m_max[k], umid: (d.relative_humidity_2m_max[k] + d.relative_humidity_2m_min[k]) / 2, et0: d.et0_fao_evapotranspiration[k] }));
}
async function recente(c) {
  const j = await J(`https://api.open-meteo.com/v1/forecast?latitude=${c[0]}&longitude=${c[1]}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,et0_fao_evapotranspiration&hourly=relative_humidity_2m&timezone=America/Belem&past_days=7&forecast_days=1`);
  const u = umidDia(j.hourly), d = j.daily;
  return d.time.map((t, k) => ({ d: t, tmax: d.temperature_2m_max[k], tmin: d.temperature_2m_min[k], tmed: (d.temperature_2m_max[k] + d.temperature_2m_min[k]) / 2, chuva: d.precipitation_sum[k], vento: d.windspeed_10m_max[k], umid: media(u[t] || []), et0: d.et0_fao_evapotranspiration[k] }));
}
async function buscarClima(c, ini, fim) {
  const h = new Date(), lim = iso(addDias(h, -5)), fimEf = fim > iso(h) ? iso(h) : fim, m = new Map();
  try { if (ini <= (fimEf < lim ? fimEf : lim)) (await arquivo(c, ini, fimEf < lim ? fimEf : lim)).forEach(r => m.set(r.d, r)); } catch (e) {}
  try { if (fimEf > lim) (await recente(c)).forEach(r => { if (!m.has(r.d) && r.tmax != null) m.set(r.d, r); }); } catch (e) {}
  if (!m.size) throw new Error("A API não retornou dados para o período.");
  return [...m.values()].filter(r => r.d >= ini && r.d <= fimEf).sort((a, b) => a.d.localeCompare(b.d));
}
function stull(T, RH) {
  RH = Math.min(100, Math.max(1, RH));
  return T * Math.atan(0.151977 * Math.sqrt(RH + 8.313659)) + Math.atan(T + RH) - Math.atan(RH - 1.676331) + 0.00391838 * RH ** 1.5 * Math.atan(0.023101 * RH) - 4.686035;
}
const classeDT = v => v < 0 || v > 10 ? ["Inadequado", "#ff6b6b"] : v < 2 || v > 8 ? ["Marginal", "#fb923c"] : ["Ideal", "#2dd4a7"];

/* ── Dados manuais ── */
function lerCSV(txt) {
  const linhas = txt.trim().split(/\r?\n/).filter(Boolean); if (linhas.length < 2) throw new Error("Cole o cabeçalho e ao menos 1 linha.");
  const sep = (linhas[0].match(/;/g) || []).length > (linhas[0].match(/,/g) || []).length ? ";" : ",";
  const cab = linhas[0].split(sep).map(s => s.trim().toLowerCase());
  const al = { data:"d", date:"d", dia:"d", temp_maxima:"tmax", temp_max:"tmax", tmax:"tmax", temp_minima:"tmin", temp_min:"tmin", tmin:"tmin", temp_media:"tmed", chuva:"chuva", precipitacao:"chuva", "precipitação":"chuva", precipitation:"chuva", vento:"vento", wind:"vento", umidade:"umid", humidity:"umid", ur:"umid", et0:"et0", eto:"et0" };
  const idx = cab.map(c => al[c]);
  for (const c of ["d", "tmax", "tmin", "chuva"]) if (!idx.includes(c)) throw new Error("Faltam colunas obrigatórias (data, temp_maxima, temp_minima, chuva).");
  const n = v => { const x = parseFloat(String(v ?? "").replace(",", ".")); return isNaN(x) ? null : x; };
  return linhas.slice(1).map(l => {
    const p = l.split(sep), r = {};
    idx.forEach((k, i) => { if (k) r[k] = k === "d" ? p[i]?.trim() : n(p[i]); });
    const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(r.d || ""); if (m) r.d = `${m[3]}-${m[2]}-${m[1]}`;
    r.tmed ??= (r.tmax + r.tmin) / 2; return r;
  }).filter(r => /^\d{4}-\d{2}-\d{2}$/.test(r.d) && r.tmax != null && r.tmin != null && r.chuva != null).sort((a, b) => a.d.localeCompare(b.d));
}

/* ── Agregação e agronomia ── */
function agregar(dados, modo) {
  if (modo === "Diário") return dados;
  const g = new Map();
  dados.forEach(r => {
    const dt = new Date(r.d + "T12:00:00");
    const k = modo === "Mensal" ? r.d.slice(0, 7) : iso(addDias(dt, -((dt.getDay() + 6) % 7)));
    (g.get(k) ?? g.set(k, []).get(k)).push(r);
  });
  return [...g].map(([d, a]) => ({ d, tmax: Math.max(...ok(a.map(r => r.tmax))), tmin: Math.min(...ok(a.map(r => r.tmin))), tmed: media(a.map(r => r.tmed)), chuva: soma(a.map(r => r.chuva)), vento: Math.max(...ok(a.map(r => r.vento))), umid: media(a.map(r => r.umid)), et0: soma(a.map(r => r.et0)) }));
}
function detectarEstacao(pm, lim) {
  const u = pm.map(v => (v || 0) >= lim);
  if (u.every(Boolean)) { let b = [-1, 0]; for (let m = 0; m < 12; m++) { const s = [0, 1, 2].reduce((x, k) => x + (pm[(m + k) % 12] || 0), 0); if (s > b[0]) b = [s, m]; } return { ini: b[1], fim: (b[1] + 11) % 12, dur: 12, reg: "umido" }; }
  if (!u.some(Boolean)) { const m = pm.indexOf(Math.max(...pm.map(v => v || 0))); return { ini: m, fim: m, dur: 1, reg: "seco" }; }
  let b = [0, 0, 0];
  for (let i = 0; i < 12; i++) if (u[i] && !u[(i + 11) % 12]) { let d = 0, m = i; while (u[m % 12] && d < 12) { d++; m++; } if (d > b[0]) b = [d, i, (i + d - 1) % 12]; }
  return { ini: b[1], fim: b[2], dur: b[0], reg: "sazonal" };
}
const doy = m => Math.round((new Date(2024, m, 1) - new Date(2024, 0, 1)) / 864e5) + 1;
const mesDoDia = d => MES[new Date(2024, 0, ((Math.round(d) - 1) % 365) + 1).getMonth()];

/* ── Lua ── */
const SIN = 29.530588853, NOVA = Date.UTC(2000, 0, 6, 18, 14);
const idadeLua = (t = Date.now()) => (((t - NOVA) / 864e5) % SIN + SIN) % SIN;
function faseLua(i) { const f = i / SIN, ilu = (1 - Math.cos(2 * Math.PI * f)) / 2; return [f < .125 || f >= .875 ? "Nova" : f < .375 ? "Crescente" : f < .625 ? "Cheia" : "Minguante", ilu, f]; }
function luaSVG(ilu, f, t = 130) {
  const r = t / 2 - 4, c = t / 2; let luz = "";
  if (ilu >= .98) luz = `<circle cx="${c}" cy="${c}" r="${r}" fill="#ffd166"/>`;
  else if (ilu > .02) {
    const cres = f < .5, rx = Math.abs(r * (1 - 2 * ilu)), so = cres ? 1 : 0, si = cres ? (ilu < .5 ? 0 : 1) : (ilu < .5 ? 1 : 0);
    luz = `<path d="M ${c} ${c - r} A ${r} ${r} 0 0 ${so} ${c} ${c + r} A ${rx} ${r} 0 0 ${si} ${c} ${c - r} Z" fill="#ffd166"/>`;
  }
  return `<svg width="${t}" height="${t}"><circle cx="${c}" cy="${c}" r="${r}" fill="#14284c" stroke="#1e3a64" stroke-width="1.5"/>${luz}</svg>`;
}

/* ── Estado e renderização ── */
let dados = [], prefs = {};
const S = { cid: $("#cidade"), ini: $("#ini"), fim: $("#fim"), agr: $("#agr"), cult: $("#cultura"), lim: $("#lim"), dias: $("#dias"), fonte: $("#fonte"), enos: $("#enos") };
Object.keys(CIDADES).forEach(c => S.cid.add(new Option(c)));
S.ini.value = "2023-01-01"; S.fim.value = iso(new Date()); S.fim.max = S.ini.max = iso(new Date());
const ABAS = [["hist", "HISTÓRICO"], ["prev", "PREVISÃO"], ["cal", "CALENDÁRIO AGRÍCOLA"], ["lua", "CALENDÁRIO LUNAR"], ["agro", "PAINEL AGRONÔMICO"]];
$("#tabs").innerHTML = ABAS.map(([k, n], i) => `<button data-k="${k}" class="${i ? "" : "on"}">${n}</button>`).join("");
$("#s-hist").classList.add("on");
$("#tabs").onclick = e => { const k = e.target.dataset.k; if (!k) return; document.querySelectorAll("#tabs button,section").forEach(x => x.classList.remove("on")); e.target.classList.add("on"); $("#s-" + k).classList.add("on"); Object.values(CH).forEach(c => c.resize()); };
const erro = m => { const e = $("#erro"); e.style.display = m ? "block" : "none"; e.innerHTML = m ? `<b class="t" style="color:#ff6b6b">Erro</b><p>${m}</p>` : ""; };

function histórico() {
  const ag = agregar(dados, S.agr.value), lb = ag.map(r => r.d);
  $("#k-hist").innerHTML = [["Temp. média", fmt(media(dados.map(r => r.tmed))), "°C", "#ffd166"], ["Máx. absoluta", fmt(Math.max(...dados.map(r => r.tmax))), "°C", "#ff6b6b"],
    ["Mín. absoluta", fmt(Math.min(...dados.map(r => r.tmin))), "°C", "#38bdf8"], ["Precip. total", fmt(soma(dados.map(r => r.chuva)), 0), "mm", "#00e5ff"],
    ["Umidade média", fmt(media(dados.map(r => r.umid)), 0), "%", "#a78bfa"], ["Vento máx.", fmt(Math.max(...ok(dados.map(r => r.vento))), 0), "km/h", "#fb923c"]].map(a => kpi(...a)).join("");
  graf("c-temp", "line", lb, [L("Máxima", ag.map(r => r.tmax), "#ff6b6b"), L("Mínima", ag.map(r => r.tmin), "#38bdf8", { fill: "-1" }), L("Média", ag.map(r => r.tmed), "#ffd166", { borderDash: [4, 4] })]);
  graf("c-chuva", "bar", lb, [{ label: "Chuva (mm)", data: ag.map(r => r.chuva), backgroundColor: "#00e5ffcc" }]);
  graf("c-umid", "line", lb, [L("Umidade (%)", ag.map(r => r.umid), "#a78bfa", { fill: true })]);
  graf("c-vento", "line", lb, [L("Vento máx. (km/h)", ag.map(r => r.vento), "#fb923c", { fill: true })]);
  const cl = MES.map((_, m) => dados.filter(r => +r.d.slice(5, 7) === m + 1));
  graf("c-clim", "bar", MES, [{ type: "bar", label: "Precip. (mm)", data: cl.map(a => a.length ? soma(a.map(r => r.chuva)) : null), backgroundColor: "#00e5ff55", yAxisID: "y2" },
    L("Máx.", cl.map(a => media(a.map(r => r.tmax))), "#ff6b6b", { type: "line" }), L("Média", cl.map(a => media(a.map(r => r.tmed))), "#ffd166", { type: "line" }), L("Mín.", cl.map(a => media(a.map(r => r.tmin))), "#38bdf8", { type: "line" })], true);
}

async function previsão() {
  const c = CIDADES[S.cid.value], n = +S.dias.value;
  $("#t-prev").textContent = `Próximos ${n} dias · ${S.cid.value}`;
  if (S.fonte.value === "manual") { $("#cards-prev").innerHTML = ""; $("#al-prev").innerHTML = alerta("#00e5ff", "Modo manual", "A previsão vem da API online e não está disponível com dados manuais."); return; }
  try {
    const j = await J(`https://api.open-meteo.com/v1/forecast?latitude=${c[0]}&longitude=${c[1]}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max,et0_fao_evapotranspiration&hourly=temperature_2m,relative_humidity_2m,windspeed_10m,precipitation&timezone=America/Belem&forecast_days=${Math.max(n, 4)}`);
    const d = j.daily, P = d.time.slice(0, n).map((t, k) => ({ d: t, tmax: d.temperature_2m_max[k], tmin: d.temperature_2m_min[k], chuva: d.precipitation_sum[k], prob: d.precipitation_probability_max[k], vento: d.windspeed_10m_max[k], et0: d.et0_fao_evapotranspiration[k] }));
    const fd = t => { const [, m, dd] = t.split("-"); return `${MES[+m - 1]} ${dd}`; };
    $("#cards-prev").innerHTML = P.slice(0, 8).map(r => `<div class="prev"><div class="d">${fd(r.d)}</div><div class="mx">${fmt(r.tmax, 0)}°</div><div class="mn">${fmt(r.tmin, 0)}°</div><div class="i">chuva ${r.prob ?? "—"}%<br>vento ${fmt(r.vento, 0)} km/h</div></div>`).join("");
    graf("c-prev", "line", P.map(r => r.d), [{ type: "bar", label: "Chuva (mm)", data: P.map(r => r.chuva), backgroundColor: "#00e5ff66", yAxisID: "y2" }, L("Máxima", P.map(r => r.tmax), "#ff6b6b"), L("Mínima", P.map(r => r.tmin), "#38bdf8")], true);
    const bons = P.filter(r => r.chuva < 1 && r.vento < 12), forte = P.filter(r => r.chuva >= 20), est = P.filter(r => r.tmax >= 34);
    const chu = soma(P.map(r => r.chuva)), et = soma(P.map(r => r.et0)), bal = chu - et, lst = a => a.map(r => fd(r.d)).join(", ");
    $("#al-prev").innerHTML = (bons.length ? alerta("#2dd4a7", "Janela de pulverização", "Dias com pouca chuva e vento moderado: " + lst(bons.slice(0, 6)) + ".") : alerta("#fb923c", "Pulverização limitada", "Poucos dias com chuva e vento ideais no horizonte."))
      + (forte.length ? alerta("#00e5ff", "Chuva forte prevista", "Volumes ≥ 20 mm em " + lst(forte) + ".") : "") + (est.length ? alerta("#ff6b6b", "Risco de estresse térmico", "Máxima ≥ 34 °C em " + lst(est) + ".") : "")
      + alerta(bal >= 0 ? "#2dd4a7" : "#ff6b6b", "Balanço hídrico previsto", `Chuva ${fmt(chu, 0)} mm − ET0 ${fmt(et, 0)} mm = <b>${bal >= 0 ? "+" : ""}${fmt(bal, 0)} mm</b> (${bal >= 0 ? "superávit" : "déficit"}).`);
    const h = j.hourly, agora = Date.now(); let H = h.time.map((t, k) => { const T = h.temperature_2m[k], U = h.relative_humidity_2m[k]; return { t: new Date(t), T, vento: h.windspeed_10m[k], chuva: h.precipitation[k], dt: T - stull(T, U) }; }).filter(r => r.t >= agora - 36e5).slice(0, 96);
    const bom = r => r.dt >= 2 && r.dt <= 8 && r.vento >= 3 && r.vento <= 15 && r.chuva < .1;
    const pct = H.filter(r => r.dt >= 2 && r.dt <= 8).length / H.length * 100, [cn, cc] = classeDT(H[0].dt);
    $("#k-dt").innerHTML = kpi("Delta T inicial", fmt(H[0].dt), "°C · agora", cc) + kpi("Condição", cn, "faixa atual", cc) + kpi("Horas ideais", fmt(pct, 0), "% das próximas 96 h", "#2dd4a7") + kpi("Faixa ideal", "2–8", "°C (BOM/GRDC)", "#00e5ff");
    graf("c-dt", "line", H.map(r => `${String(r.t.getDate()).padStart(2, 0)}/${String(r.t.getMonth() + 1).padStart(2, 0)} ${String(r.t.getHours()).padStart(2, 0)}h`), [L("Delta T (°C)", H.map(r => r.dt), "#00e5ff"), L("Vento (km/h)", H.map(r => r.vento), "#fb923c", { yAxisID: "y2", borderDash: [3, 3], borderWidth: 1 })], true);
    const jn = []; let a = null; H.forEach((r, i) => { if (bom(r) && !a) a = r; if ((!bom(r) || i === H.length - 1) && a) { jn.push([a.t, H[i - (bom(r) ? 0 : 1)].t]); a = null; } });
    const DS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
    $("#al-dt").innerHTML = jn.length ? alerta("#2dd4a7", "Melhores janelas para pulverizar", jn.slice(0, 8).map(([i, f]) => `${DS[i.getDay()]} ${String(i.getDate()).padStart(2, 0)}/${String(i.getMonth() + 1).padStart(2, 0)}: ${String(i.getHours()).padStart(2, 0)}h–${String((f.getHours() + 1) % 24).padStart(2, 0)}h`).join(" · "))
      : alerta("#fb923c", "Sem janela ideal nas próximas 96 h", "Delta T, vento ou chuva fora da faixa. Reavalie no início da manhã ou fim da tarde.");
  } catch (e) { $("#al-prev").innerHTML = alerta("#ff6b6b", "Previsão indisponível", e.message); }
}

function calendário() {
  const pm = MES.map((_, m) => { const a = {}; dados.forEach(r => { const k = r.d.slice(0, 7); a[k] = (a[k] || 0) + r.chuva; }); const v = Object.entries(a).filter(([k]) => +k.slice(5) === m + 1).map(x => x[1]); return media(v); });
  const est = detectarEstacao(pm, +S.lim.value), st = doy(est.ini), nMeses = pm.filter(v => v != null).length;
  $("#t-cal").textContent = `Sucessão soja → milho safrinha · ajustado à chuva de ${S.cid.value}`;
  const pos = d => ((d - 1) % 365 + 365) % 365 / 365 * 100;
  const bar = (a, b, cor) => { const x = pos(a), y = pos(b); return y >= x ? `<i style="left:${x}%;width:${Math.max(y - x, .6)}%;background:${cor}"></i>` : `<i style="left:${x}%;right:0;background:${cor}"></i><i style="left:0;width:${y}%;background:${cor}"></i>`; };
  const chuva = [0, 1, 2].length && est.reg !== "seco" ? bar(doy(est.ini), doy(est.fim) + 28, "rgba(0,229,255,.18)") : "";
  let h = `<div class="tl"><span></span><div class="meses">${MES.map(m => `<span>${m}</span>`).join("")}</div><span>Estação chuvosa</span><div class="trilho">${chuva}</div>`;
  Object.entries(SISTEMA).forEach(([c, s]) => s.fases.forEach(([f, i, e]) => { h += `<span>${c} · ${f}</span><div class="trilho">${bar(st + i, st + e, s.cor)}</div>`; }));
  $("#tl").innerHTML = h + "</div>";
  $("#k-cal").innerHTML = kpi("Início das chuvas", MES[est.ini], "plantio da soja", "#00e5ff") + kpi("Fim das chuvas", MES[est.fim], "fim do período úmido", "#a78bfa") + kpi("Estação chuvosa", est.dur, "meses úmidos", "#2dd4a7") + kpi("Colheita da soja", mesDoDia(st + 120), "≈ 118 dias após plantio", "#2dd4a7") + kpi("Colheita do milho", mesDoDia(st + 270), "milho safrinha", "#ffd166");
  const av = [];
  if (nMeses < 12) av.push(["#fb923c", "Período curto para climatologia", `O período cobre ${nMeses} de 12 meses. Selecione ao menos 1–2 anos completos.`]);
  if (est.reg === "umido") av.push(["#00e5ff", "Chuva o ano todo", "Janela de plantio flexível. O cuidado migra para doenças e colheita em período úmido."]);
  else if (est.reg === "seco") av.push(["#ff6b6b", "Chuva insuficiente para sequeiro", `Nenhum mês atinge ${S.lim.value} mm. Considere irrigação ou reduza o limiar.`]);
  else if (est.dur * 30 >= 240) av.push(["#2dd4a7", "Janela favorável ao sistema completo", `Estação de ~${est.dur} meses, suficiente para soja + milho safrinha.`]);
  else if (est.dur * 30 >= 150) av.push(["#fb923c", "Milho safrinha com risco no enchimento", `Estação de ~${est.dur} meses: favoreça cultivares precoces e antecipe a soja.`]);
  else av.push(["#ff6b6b", "Estação chuvosa curta", `Com ~${est.dur} meses úmidos, o milho safrinha fica arriscado.`]);
  $("#al-cal").innerHTML = av.map(a => alerta(...a)).join("");
  const e = ENOS[S.enos.value]; $("#al-enos").innerHTML = alerta(e.cor, e.t, e.x);
}

function lunar() {
  const i = idadeLua(), [nome, ilu, f] = faseLua(i), [cor, txt, gr] = LUA[nome];
  $("#lua").innerHTML = luaSVG(ilu, f) + `<div class="mono" style="color:${cor};margin-top:8px">${nome}</div><div class="nota">${fmt(ilu * 100, 0)}% iluminada · ${fmt(i, 0)} dias</div>`;
  $("#lua-txt").innerHTML = `<h3>Manejo indicado agora</h3>${txt}<br><br>Para <b>grãos (soja e milho)</b>, esta fase é <b style="color:${cor}">${gr}</b>. A tradição planta grãos na crescente e colhe na cheia.`;
  const DS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
  $("#k-lua").innerHTML = [["Nova", 0, "#7ba3c8"], ["Quarto crescente", .25, "#2dd4a7"], ["Cheia", .5, "#ffd166"], ["Quarto minguante", .75, "#fb923c"]].map(([n, fr, c]) => {
    const d = new Date(Date.now() + (((fr - i / SIN) % 1 + 1) % 1) * SIN * 864e5); return kpi(n, `${String(d.getDate()).padStart(2, 0)}/${String(d.getMonth() + 1).padStart(2, 0)}`, DS[d.getDay()], c);
  }).join("");
}

function agro() {
  const cf = CULT[S.cult.value], gdd = []; let ac = 0; dados.forEach(r => { ac += Math.max(0, (r.tmax + r.tmin) / 2 - cf.base); gdd.push(ac); });
  const bal = []; let b = 0; dados.forEach(r => { b += r.chuva - (r.et0 ?? 0); bal.push(b); });
  let vr = 0, atual = 0; dados.forEach(r => { atual = r.chuva < 1 ? atual + 1 : 0; vr = Math.max(vr, atual); });
  const est = dados.filter(r => r.tmax >= 34).length, pc = Math.min(ac / cf.gdd * 100, 999), bt = bal.at(-1) ?? 0;
  $("#t-agro").textContent = `Indicadores · período selecionado · referência: ${S.cult.value}`;
  $("#k-agro").innerHTML = kpi("GDD acumulado", fmt(ac, 0), "°C·dia · " + S.cult.value, cf.cor) + kpi("Equiv. ciclo", fmt(pc, 0), `% de ${cf.gdd} °C·dia`, "#ffd166") + kpi("Balanço hídrico", (bt >= 0 ? "+" : "") + fmt(bt, 0), "mm · chuva − ET0", "#00e5ff") + kpi("Dias ≥ 34 °C", est, "estresse térmico", "#ff6b6b") + kpi("Maior veranico", vr, "dias secos seguidos", "#fb923c");
  const lb = dados.map(r => r.d);
  graf("c-gdd", "line", lb, [L("GDD acumulado", gdd, cf.cor, { fill: true }), L("Ciclo de referência", lb.map(() => cf.gdd), "#ffd166", { borderDash: [6, 4], borderWidth: 1 })]);
  graf("c-bal", "line", lb, [L("Balanço (mm)", bal, "#00e5ff", { fill: true })]);
  const l = [`O período acumulou <b>${fmt(ac, 0)} °C·dia</b>, cerca de <b>${fmt(pc, 0)}%</b> do ciclo térmico da ${S.cult.value}.`,
    bt >= 0 ? `Balanço hídrico positivo (<b>+${fmt(bt, 0)} mm</b>): mais chuva do que demanda evaporativa.` : `Balanço hídrico negativo (<b>${fmt(bt, 0)} mm</b>): a demanda evaporativa superou a chuva.`];
  if (vr >= 10) l.push(`Veranico de <b>${vr} dias</b> sem chuva relevante: risco alto se coincidir com a floração.`);
  if (est) l.push(`<b>${est} dia(s)</b> com máxima ≥ 34 °C.`);
  $("#leitura").innerHTML = "• " + l.join("<br>• ");
}

async function atualizar() {
  erro("");
  const c = CIDADES[S.cid.value];
  $("#info").textContent = `${S.cid.value} · ${c[0].toFixed(4)}°, ${c[1].toFixed(4)}° · ${S.ini.value} → ${S.fim.value}`;
  if (S.ini.value >= S.fim.value) return erro("A data de início deve ser anterior à data de fim.");
  $("#manual").style.display = S.fonte.value === "manual" ? "block" : "none";
  try {
    dados = S.fonte.value === "manual" ? (await carregar("dados_manuais")) || [] : await buscarClima(c, S.ini.value, S.fim.value);
    if (dados.length < 2) return erro("Cole ao menos 2 dias de dados e clique em Aplicar e salvar.");
  } catch (e) { return erro("Não foi possível buscar os dados: " + e.message); }
  histórico(); calendário(); lunar(); agro(); previsão();
  salvar("prefs", { cid: S.cid.value, lim: S.lim.value, cult: S.cult.value, enos: S.enos.value, fonte: S.fonte.value });
}

Object.values(S).forEach(el => el.addEventListener("change", atualizar));
S.lim.addEventListener("input", () => $("#limv").textContent = S.lim.value);
$("#aplicar").onclick = async () => {
  try { const d = lerCSV($("#txt").value); await salvar("dados_manuais", d); atualizar(); } catch (e) { erro(e.message); }
};

await iniciarFirebase();
prefs = (await carregar("prefs")) || {};
if (prefs.cid) S.cid.value = prefs.cid; if (prefs.lim) { S.lim.value = prefs.lim; $("#limv").textContent = prefs.lim; }
if (prefs.cult) S.cult.value = prefs.cult; if (prefs.enos) S.enos.value = prefs.enos; if (prefs.fonte) S.fonte.value = prefs.fonte;
atualizar();
</script>
</body>
</html>
