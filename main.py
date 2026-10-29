
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="VALORANT Aim Training",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.stApp {
    background: #111317;
    color: #f4f4f4;
}
.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
}
h1, h2, h3, p, label {
    color: #f4f4f4;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    color: #d0d2d7;
}
div[data-testid="stSelectbox"] > div > div {
    background: #24272e;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='color:#ff4655;margin-bottom:0'>🎯 AIM TRAINING</h1>",
    unsafe_allow_html=True,
)
st.caption("VALORANT에서 영감을 받은 브라우저 에임 훈련장")

a, b, c = st.columns(3)

with a:
    mode = st.selectbox(
        "훈련 모드",
        ["정밀 사격", "플릭 에임", "반응 훈련"],
    )

with b:
    difficulty = st.selectbox(
        "난이도",
        ["쉬움", "보통", "어려움"],
        index=1,
    )

with c:
    duration = st.selectbox(
        "훈련 시간",
        [30, 60, 90],
        index=0,
        format_func=lambda x: f"{x}초",
    )

sizes = {"쉬움": 48, "보통": 34, "어려움": 23}
speeds = {"쉬움": 1800, "보통": 1100, "어려움": 650}
target_size = sizes[difficulty]
move_speed = speeds[difficulty]

mode_map = {
    "정밀 사격": "precision",
    "플릭 에임": "flick",
    "반응 훈련": "reaction",
}
game_mode = mode_map[mode]

st.markdown("---")

st.markdown("""
<div style="
background:#202329;
border-left:5px solid #ff4655;
padding:14px 18px;
border-radius:6px;
margin-bottom:12px;">
<b>훈련 지침</b><br>
<span style="color:#c8cbd2">
표적을 마우스로 클릭하세요. 빗나간 클릭도 기록됩니다.
훈련이 끝나면 정확도와 반응 속도를 확인할 수 있습니다.
</span>
</div>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin:0;
    background:#111317;
    color:#f5f5f5;
    font-family:Arial, "Malgun Gothic",sans-serif;
}
.stats {
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:9px;
    margin-bottom:12px;
}
.stat {
    background:#202329;
    border:1px solid #343740;
    border-radius:5px;
    padding:12px;
}
.label {
    color:#aeb2bc;
    font-size:12px;
    margin-bottom:7px;
}
.value {
    font-size:clamp(18px,3vw,27px);
    font-weight:800;
}
.red { color:#ff4655; }
.arena {
    height:460px;
    position:relative;
    overflow:hidden;
    background:
      radial-gradient(ellipse at center,#272a30 0%,#17191e 70%,#101216 100%);
    border:1px solid #41444c;
    cursor:crosshair;
    user-select:none;
}
.grid {
    position:absolute;
    inset:0;
    opacity:.18;
    background-image:
      linear-gradient(#555 1px,transparent 1px),
      linear-gradient(90deg,#555 1px,transparent 1px);
    background-size:40px 40px;
    pointer-events:none;
}
.crosshair {
    position:absolute;
    width:18px;
    height:18px;
    pointer-events:none;
    z-index:4;
    transform:translate(-50%,-50%);
    display:none;
}
.crosshair:before,.crosshair:after {
    content:"";
    position:absolute;
    background:#fff;
    box-shadow:0 0 2px #111;
}
.crosshair:before {
    width:2px;height:18px;left:8px;top:0;
}
.crosshair:after {
    height:2px;width:18px;left:0;top:8px;
}
.target {
    position:absolute;
    border:3px solid #f7f7f7;
    border-radius:50%;
    transform:translate(-50%,-50%);
    background:#ff4655;
    box-shadow:0 0 0 5px #ff465533,0 0 22px #ff465566;
    display:none;
    z-index:2;
    padding:0;
    cursor:crosshair;
}
.target:before {
    content:"";
    position:absolute;
    inset:20%;
    border-radius:50%;
    border:2px solid #fff;
}
.target:after {
    content:"";
    position:absolute;
    width:20%;height:20%;
    left:40%;top:40%;
    background:white;
    border-radius:50%;
}
.overlay {
    position:absolute;
    z-index:5;
    inset:0;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    padding:16px;
    background:#0e1015d9;
}
.panel { width:min(100%,380px); }
.panel h2 { font-size:28px;margin:0 0 10px; }
.panel p { color:#c2c5ce;line-height:1.65;font-size:14px; }
button.action {
    padding:13px 24px;
    border:0;
    border-radius:3px;
    color:white;
    background:#ff4655;
    font-weight:800;
    cursor:pointer;
    font-size:15px;
}
button.action:hover { background:#e93445; }
button.secondary {
    border:1px solid #4b4f59;
    background:#24272e;
    color:white;
    padding:10px 16px;
    cursor:pointer;
    border-radius:3px;
}
.bottom {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
    flex-wrap:wrap;
    margin-top:12px;
}
.note { color:#aeb2bc;font-size:12px; }
.results {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
    margin:14px 0;
}
.cell {
    padding:11px;
    border:1px solid #42454f;
    background:#202329;
}
.cell small { display:block;color:#aeb2bc;margin-bottom:6px; }
.cell strong { font-size:20px; }
@media(max-width:500px) {
    .arena { height:390px; }
    .stat { padding:9px 5px; }
    .label { font-size:10px; }
}
</style>
</head>
<body>
<div class="stats">
  <div class="stat"><div class="label">남은 시간</div><div class="value" id="time">30초</div></div>
  <div class="stat"><div class="label">명중</div><div class="value red" id="hits">0</div></div>
  <div class="stat"><div class="label">정확도</div><div class="value" id="accuracy">0%</div></div>
  <div class="stat"><div class="label">평균 반응</div><div class="value" id="reaction">--</div></div>
</div>

<div class="arena" id="arena">
    <div class="grid"></div>
    <div class="crosshair" id="crosshair"></div>
    <button class="target" id="target" aria-label="표적"></button>
    <div class="overlay" id="overlay">
        <div class="panel" id="panel">
            <h2>훈련 준비 완료</h2>
            <p>표적을 빠르고 정확하게 맞히세요.<br>
            헤드샷을 노리는 마음으로 조준해 보세요.</p>
            <button class="action" id="start">훈련 시작</button>
        </div>
    </div>
</div>

<div class="bottom">
    <span class="note" id="status">준비가 되면 훈련을 시작하세요.</span>
    <button class="secondary" id="restart">다시 시작 ↻</button>
</div>

<script>
(() => {
    const MODE = "__MODE__";
    const DURATION = __DURATION__;
    const SIZE = __SIZE__;
    const MOVE_INTERVAL = __SPEED__;

    const arena = document.getElementById("arena");
    const target = document.getElementById("target");
    const overlay = document.getElementById("overlay");
    const panel = document.getElementById("panel");
    const startBtn = document.getElementById("start");
    const restartBtn = document.getElementById("restart");
    const crosshair = document.getElementById("crosshair");

    let running = false;
    let hits = 0, misses = 0;
    let reactionTimes = [];
    let spawnTime = 0;
    let deadline = 0;
    let countdown = null;
    let movement = null;
    let targetTimeout = null;

    function stats() {
        const attempts = hits + misses;
        const accuracy = attempts ? Math.round(hits / attempts * 100) : 0;
        const average = reactionTimes.length
            ? Math.round(reactionTimes.reduce((a,b)=>a+b,0)/reactionTimes.length)
            : 0;
        document.getElementById("hits").textContent = hits;
        document.getElementById("accuracy").textContent = accuracy + "%";
        document.getElementById("reaction").textContent =
            average ? average + "ms" : "--";
    }

    function placeTarget() {
        if (!running) return;

        const pad = SIZE / 2 + 8;
        const maxX = Math.max(pad, arena.clientWidth - pad);
        const maxY = Math.max(pad, arena.clientHeight - pad);
        const x = pad + Math.random() * (maxX - pad);
        const y = pad + Math.random() * (maxY - pad);

        target.style.width = SIZE + "px";
        target.style.height = SIZE + "px";
        target.style.left = x + "px";
        target.style.top = y + "px";
        target.style.display = "block";
        spawnTime = performance.now();

        clearTimeout(targetTimeout);

        if (MODE === "reaction") {
            targetTimeout = setTimeout(() => {
                if (!running || target.style.display === "none") return;
                target.style.display = "none";
                misses++;
                stats();
                placeTarget();
            }, Math.max(900, MOVE_INTERVAL + 400));
        }
    }

    function startGame() {
        clearInterval(countdown);
        clearInterval(movement);
        clearTimeout(targetTimeout);

        hits = 0;
        misses = 0;
        reactionTimes = [];
        running = true;
        deadline = performance.now() + DURATION * 1000;

        overlay.style.display = "none";
        crosshair.style.display = "block";
        document.getElementById("status").textContent = "표적 조준 중...";
        stats();
        placeTarget();

        if (MODE === "flick") {
            movement = setInterval(placeTarget, MOVE_INTERVAL);
        } else if (MODE === "precision") {
            movement = setInterval(placeTarget, Math.max(2500, MOVE_INTERVAL * 2));
        }

        countdown = setInterval(() => {
            const remaining = Math.max(0, deadline - performance.now());
            document.getElementById("time").textContent =
                (remaining / 1000).toFixed(1) + "초";
            if (remaining <= 0) finishGame();
        }, 50);
    }

    function finishGame() {
        if (!running) return;
        running = false;
        clearInterval(countdown);
        clearInterval(movement);
        clearTimeout(targetTimeout);
        target.style.display = "none";
        overlay.style.display = "flex";
        crosshair.style.display = "none";

        const attempts = hits + misses;
        const accuracy = attempts ? Math.round(hits / attempts * 100) : 0;
        const average = reactionTimes.length
            ? Math.round(reactionTimes.reduce((a,b)=>a+b,0)/reactionTimes.length)
            : 0;

        panel.innerHTML = `
          <h2>훈련 종료</h2>
          <p>오늘의 에임 훈련 결과</p>
          <div style="font-size:38px;font-weight:800;color:#ff4655">
            ${hits}회 명중
          </div>
          <div class="results">
            <div class="cell"><small>정확도</small><strong>${accuracy}%</strong></div>
            <div class="cell"><small>평균 반응</small><strong>${average ? average+"ms" : "--"}</strong></div>
            <div class="cell"><small>빗나감</small><strong>${misses}회</strong></div>
            <div class="cell"><small>총 시도</small><strong>${attempts}회</strong></div>
          </div>
          <button class="action" id="again">다시 훈련하기</button>
        `;
        document.getElementById("again").addEventListener("click", startGame);
        document.getElementById("time").textContent = "0.0초";
        document.getElementById("status").textContent = "훈련이 끝났습니다.";
        stats();
    }

    arena.addEventListener("mousemove", e => {
        const rect = arena.getBoundingClientRect();
        crosshair.style.left = (e.clientX - rect.left) + "px";
        crosshair.style.top = (e.clientY - rect.top) + "px";
    });

    arena.addEventListener("click", e => {
        if (!running) return;

        if (e.target === target) {
            hits++;
            reactionTimes.push(Math.round(performance.now() - spawnTime));
            clearTimeout(targetTimeout);

            if (MODE === "precision") {
                target.style.display = "none";
                setTimeout(() => {
                    if (running) placeTarget();
                }, 160);
            } else {
                placeTarget();
            }
        } else {
            misses++;
        }
        stats();
    });

    startBtn.addEventListener("click", startGame);
    restartBtn.addEventListener("click", startGame);

    window.addEventListener("resize", () => {
        if (running) placeTarget();
    });
})();
</script>
</body>
</html>
"""

html = (
    html
    .replace("__MODE__", game_mode)
    .replace("__DURATION__", str(duration))
    .replace("__SIZE__", str(target_size))
    .replace("__SPEED__", str(move_speed))
)

components.html(html, height=590, scrolling=False)

st.markdown("---")
st.caption(
    "AIM TRAINING · 개인 연습용 미니게임입니다. "
    "실제 VALORANT 클라이언트나 Riot 계정과 연동되지 않습니다."
)
