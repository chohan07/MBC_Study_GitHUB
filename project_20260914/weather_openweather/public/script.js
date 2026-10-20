const citySelect = document.getElementById("city-select");
const btnSingle = document.getElementById("btn-single");
const btnAll = document.getElementById("btn-all");
const btnClearLog = document.getElementById("btn-clear-log");
const consoleBox = document.getElementById("console-box");
const cardsContainer = document.getElementById("cards-container");
const resultStatus = document.getElementById("result-status");
const resultTime = document.getElementById("result-time");

// 로그 기록 함수
function log(msg, type = "info") {
  const timeStr = new Date().toLocaleTimeString("ko-KR", { hour12: true });
  const div = document.createElement("div");
  div.className = `log-line log-${type}`;
  div.textContent = `[${timeStr}] ${msg}`;
  consoleBox.appendChild(div);
  consoleBox.scrollTop = consoleBox.scrollHeight;
}

// 5개 도시 기본 데이터 세팅
const cityNames = {
  seoul: "서울",
  tokyo: "도쿄",
  newyork: "뉴욕",
  london: "런던",
  paris: "파리"
};

// 1. 단일 도시 조회 (async/await)
async function fetchSingleCity() {
  const cityKey = citySelect.value;
  const cityName = cityNames[cityKey];

  log(`[주문] fetch('/api/weather?city=${cityKey}') 호출`);

  const startTime = performance.now();
  try {
    const res = await fetch(`/api/weather?city=${cityKey}`);
    const data = await res.json();
    const endTime = performance.now();
    const duration = Math.round(endTime - startTime);

    log(`[응답 도착] HTTP 상태 코드: ${res.status}`);
    log(`[수령 완료] 기온: ${Math.round(data.main.temp * 10) / 10}°C | 습도: ${data.main.humidity}% | 출처: OpenWeatherMap`, "success");

    resultStatus.textContent = `✅ ${cityName} 날씨 조회 성공! (Fulfilled)`;
    resultTime.textContent = `총 소요 시간: 단 ${duration}ms`;

    renderCards([{
      name: cityName,
      temp: Math.round(data.main.temp * 10) / 10,
      humidity: data.main.humidity
    }]);

  } catch (err) {
    log(`[에러 발생] ${err.message}`, "error");
  }
}

// 2. 전체 도시 동시 조회 (Promise.all)
async function fetchAllCities() {
  log(`[동시 주문] fetch('/api/weather/compare') 병렬 API 호출 (Promise.all)`);
  
  const startTime = performance.now();
  try {
    const res = await fetch(`/api/weather/compare`);
    const data = await res.json();
    const endTime = performance.now();
    const duration = Math.round(endTime - startTime);

    log(`[전체 완료] 5개 도시 날씨를 병렬로 ${duration}ms 만에 일괄 수령했습니다.`, "success");

    resultStatus.textContent = `✅ 5개 도시 동시 수령 성공! (Fulfilled)`;
    resultTime.textContent = `총 소요 시간: 단 ${duration}ms (직렬 실행 대비 압도적 단축)`;

    renderCards(data);

  } catch (err) {
    log(`[에러 발생] ${err.message}`, "error");
  }
}

// 카드 UI 그리기
function renderCards(list) {
  cardsContainer.innerHTML = "";
  list.forEach(item => {
    const card = document.createElement("div");
    card.className = "weather-card";
    card.innerHTML = `
      <div class="city-title">${item.name}</div>
      <div class="city-temp">${item.temp}°C</div>
      <div class="city-hum">${item.humidity}%</div>
    `;
    cardsContainer.appendChild(card);
  });
}

// 이벤트 연결
btnSingle.addEventListener("click", fetchSingleCity);
btnAll.addEventListener("click", fetchAllCities);
btnClearLog.addEventListener("click", () => {
  consoleBox.innerHTML = "";
});

// 초기 실행 (전체 조회)
fetchAllCities();