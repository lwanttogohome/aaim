
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Aim Lab | 에임 연습",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    .stApp {
        background: #0b1020;
        color: #f4f7ff;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3, p, label {
        color: #f4f7ff;
    }
    div[data-testid="stSelectbox"] label {
        color: #aebbd4 !important;
    }
    div[data-testid="stSelectbox"] > div > div {
        background: #151d32;
        color: white;
        border-color: #303b57;
    }
    .aim-subtitle {
        color: #9eacc9;
        font-size: 1rem;
        margin-top: -10px;
        margin-bottom: 18px;
    }
    .aim-note {
        text-align: center;
        color: #8c9bb9;
        font-size: 0.85rem;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🎯 AIM LAB")
st.markdown(
    '<p class="aim-subtitle">반응 속도와 정확도를 높이는 나만의 에임 트레이닝</p>',
    unsafe_allow_html=True,
)

left, right = st.columns([1, 2])

with left:
    difficulty = st.selectbox(
        "난이도",
        ["쉬움", "보통", "어려움"],
        index=1,
    )

    duration = st.selectbox(
        "연습 시간",
        [15, 30, 60],
        index=1,
        format_func=lambda x: f"{x}초",
    )

    target_size = {
        "쉬움": 52,
        "보통": 38,
        "어려움": 25,
    }[difficulty]

    target_speed = {
        "쉬움": 1800,
        "보통": 1250,
        "어려움": 850,
    }[difficulty]

    st.markdown("### 📋 연습 방법")
    st.markdown(
        """
        1. **연습 시작** 버튼을 누르세요.
        2. 화면에 나타나는 표적을 클릭하세요.
        3. 제한 시간 동안 최대한 많이 맞히세요.
        4. 결과에서 명중률과 반응 속도를 확인하세요.
        """
    )
    st.caption("팁: 마우스를 표적 가까이 이동한 뒤 정확하게 클릭해 보세요.")

with right:
    game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #0b1020;
    color: #f4f7ff;
    font-family: Arial, "Malgun Gothic", sans-serif;
}
.game { width: 100%; }
.stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 12px;
}
.stat {
    background: #151d32;
    border: 1px solid #26334f;
    border-radius: 12px;
    padding: 12px 8px;
    min-width: 0;
}
.stat-label {
    font-size: 11px;
    color: #9eacc9;
    margin-bottom: 7px;
}
.stat-value {
    font-size: clamp(17px, 3vw, 25px);
    font-weight: 800;
    overflow-wrap: anywhere;
}
.arena {
    height: 440px;
    position: relative;
    overflow: hidden;
    background-color: #0e172a;
    background-image:
      linear-gradient(#1c2940 1px, transparent 1px),
      linear-gradient(90deg, #1c2940 1px, transparent 1px);
    background-size: 32px 32px;
    border: 1px solid #2a3855;
    border-radius: 15px;
    cursor: crosshair;
    user-select: none;
}
.target {
    position: absolute;
    border-radius: 50%;
    border: 3px solid #ffffff;
    background: #ff496c;
    box-shadow: 0 0 0 5px rgba(255,73,108,.20),
                0 0 24px rgba(255,73,108,.75);
    cursor: crosshair;
    display: none;
    align-items: center;
    justify-content: center;
    transform: translate(-50%, -50%);
    padding: 0;
    outline: none;
}
.target::before {
    content: "";
    width: 55%;
    height: 55%;
    border-radius: 50%;
    background: #fff;
    box-shadow: 0 0 0 3px #ff496c;
}
.target::after {
    content: "";
    position: absolute;
    width: 22%;
    height: 22%;
    border-radius: 50%;
    background: #ff496c;
}
.target:active { filter: brightness(1.2); }
.overlay {
    position: absolute;
    inset: 0;
    background: rgba(8,13,27,.80);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 20px;
}
.panel { max-width: 360px; }
.panel h2 { font-size: 28px; margin: 0 0 12px; }
.panel p { color: #aebbd4; line-height: 1.6; font-size: 14px; }
.main-btn {
    border: 0;
    border-radius: 10px;
    padding: 13px 25px;
    color: #07101e;
    background: #63f5c8;
    font-weight: 800;
    font-size: 15px;
    cursor: pointer;
    margin-top: 8px;
}
.main-btn:hover { background: #8bffdc; }
.secondary-btn {
    border: 1px solid #435271;
    border-radius: 9px;
    padding: 10px 16px;
    color: #f4f7ff;
    background: #151d32;
    font-weight: 700;
    cursor: pointer;
}
.bottom {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    align-items: center;
    margin-top: 12px;
    flex-wrap: wrap;
}
.status { color: #9eacc9; font-size: 12px; }
.result-score { color: #63f5c8; font-size: 38px; font-weight: 800; }
.result-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 16px 0;
}
.result-cell {
    background: #151d32;
    border: 1px solid #293653;
    border-radius: 10px;
    padding: 12px;
}
.result-cell small { display: block; color: #9eacc9; margin-bottom: 6px; }
.result-cell strong { font-size: 21px; }
@media(max-width: 500px) {
    .arena { height: 390px; }
    .stat { padding: 10px 5px; }
    .stat-label { font-size: 10px; }
}
</style>
</head>
<body>
<div class="game">
  <div class="stats">
    <div class="stat"><div class="stat-label">남은 시간</div><div class="stat-value" id="time">30.0초</div></div>
    <div class="stat"><div class="stat-label">명중</div><div class="stat-value" id="hits">0</div></div>
    <div class="stat"><div class="stat-label">명중률</div><div class="stat-value" id="accuracy">0%</div></div>
    <div class="stat"><div class="stat-label">평균 반응</div><div class="stat-value" id="reaction">--</div></div>
  </div>

  <div class="arena" id="arena">
    <button class="target" id="target" aria-label="표적 맞히기"></button>
    <div class="overlay" id="overlay">
      <div class="panel" id="panel">
        <h2>준비되었나요?</h2>
        <p>표적을 빠르고 정확하게 클릭하세요.<br>시간이 끝나면 결과를 확인할 수 있습니다.</p>
        <button class="main-btn" id="start">연습 시작 →</button>
      </div>
    </div>
  </div>

  <div class="bottom">
    <span class="status" id="status">시작 버튼을 누르면 연습이 시작됩니다.</span>
    <button class="secondary-btn" id="restart">다시 시작</button>
  </div>
</div>

<script>
(function() {
    const arena = document.getElementById("arena");
    const target = document.getElementById("target");
    const overlay = document.getElementById("overlay");
    const panel = document.getElementById("panel");
    const startBtn = document.getElementById("start");
    const restartBtn = document.getElementById("restart");
    const timeEl = document.getElementById("time");
    const hitsEl = document.getElementById("hits");
    const accuracyEl = document.getElementById("accuracy");
    const reactionEl = document.getElementById("reaction");
    const statusEl = document.getElementById("status");

    const duration = __DURATION__;
    const targetSize = __SIZE__;
    const moveInterval = __SPEED__;

    let active = false;
    let hits = 0;
    let misses = 0;
    let reactionTimes = [];
    let startedAt = 0;
    let targetShownAt = 0;
    let timerId = null;
    let moveId = null;
    let endsAt = 0;

    function updateStats() {
        const attempts = hits + misses;
        const accuracy = attempts ? Math.round(hits / attempts * 100) : 0;
        const avg = reactionTimes.length
            ? Math.round(reactionTimes.reduce((a, b) => a + b, 0) / reactionTimes.length)
            : 0;
        hitsEl.textContent = hits;
        accuracyEl.textContent = accuracy + "%";
        reactionEl.textContent = avg ? avg + "ms" : "--";
    }

    function moveTarget() {
        const pad = targetSize / 2 + 8;
        const maxX = Math.max(pad, arena.clientWidth - pad);
        const maxY = Math.max(pad, arena.clientHeight - pad);
        const x = pad + Math.random() * (maxX - pad);
        const y = pad + Math.random() * (maxY - pad);
        target.style.width = targetSize + "px";
        target.style.height = targetSize + "px";
        target.style.left = x + "px";
        target.style.top = y + "px";
        target.style.display = "flex";
        targetShownAt = performance.now();
    }

    function startGame() {
        clearInterval(timerId);
        clearInterval(moveId);
        hits = 0;
        misses = 0;
        reactionTimes = [];
        active = true;
        startedAt = performance.now();
        endsAt = startedAt + duration * 1000;
        overlay.style.display = "none";
        statusEl.textContent = "표적을 클릭하세요!";
        updateStats();
        moveTarget();

        timerId = setInterval(function() {
            const remaining = Math.max(0, endsAt - performance.now());
            timeEl.textContent = (remaining / 1000).toFixed(1) + "초";
            if (remaining <= 0) endGame();
        }, 50);

        moveId = setInterval(function() {
            if (active) moveTarget();
        }, moveInterval);
    }

    function endGame() {
        if (!active) return;
        active = false;
        clearInterval(timerId);
        clearInterval(moveId);
        target.style.display = "none";
        overlay.style.display = "flex";
        const attempts = hits + misses;
        const accuracy = attempts ? Math.round(hits / attempts * 100) : 0;
        const avg = reactionTimes.length
            ? Math.round(reactionTimes.reduce((a, b) => a + b, 0) / reactionTimes.length)
            : 0;

        panel.innerHTML =
          '<h2>연습 완료! 🎯</h2>' +
          '<p>이번 연습 결과입니다.</p>' +
          '<div class="result-score">' + hits + '회 명중</div>' +
          '<div class="result-grid">' +
            '<div class="result-cell"><small>명중률</small><strong>' + accuracy + '%</strong></div>' +
            '<div class="result-cell"><small>평균 반응 시간</small><strong>' + (avg ? avg + 'ms' : '--') + '</strong></div>' +
            '<div class="result-cell"><small>빗나감</small><strong>' + misses + '회</strong></div>' +
            '<div class="result-cell"><small>총 시도</small><strong>' + attempts + '회</strong></div>' +
          '</div>' +
          '<button class="main-btn" id="playAgain">다시 도전하기 ↻</button>';

        document.getElementById("playAgain").addEventListener("click", startGame);
        timeEl.textContent = "0.0초";
        updateStats();
        statusEl.textContent = "연습이 끝났습니다. 다시 도전해 보세요!";
    }

    arena.addEventListener("click", function(event) {
        if (!active) return;
        if (event.target === target || target.contains(event.target)) {
            hits++;
            reactionTimes.push(Math.round(performance.now() - targetShownAt));
            moveTarget();
        } else {
            misses++;
        }
        updateStats();
    });

    startBtn.addEventListener("click", startGame);
    restartBtn.addEventListener("click", startGame);

    window.addEventListener("resize", function() {
        if (active) moveTarget();
    });
})();
</script>
</body>
</html>
"""
    game_html = (
        game_html
        .replace("__DURATION__", str(duration))
        .replace("__SIZE__", str(target_size))
        .replace("__SPEED__", str(target_speed))
    )

    components.html(game_html, height=570, scrolling=False)

st.markdown(
    '<p class="aim-note">AIM LAB · 꾸준한 연습으로 반응 속도와 정확도를 높여 보세요.</p>',
    unsafe_allow_html=True,
)
