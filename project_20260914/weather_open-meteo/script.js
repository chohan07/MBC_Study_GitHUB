// Open-Meteo WMO weathercode 매핑 객체
const weatherCodeMap = {
  0: { text: "맑음", icon: "☀️" },
  1: { text: "대체로 맑음", icon: "🌤️" },
  2: { text: "구름 조금", icon: "⛅" },
  3: { text: "흐림", icon: "☁️" },
  45: { text: "안개", icon: "🌫️" },
  48: { text: "서리 안개", icon: "🌫️" },
  51: { text: "이슬비 (약함)", icon: "🌧️" },
  53: { text: "이슬비 (보통)", icon: "🌧️" },
  55: { text: "이슬비 (강함)", icon: "🌧️" },
  61: { text: "비 (약함)", icon: "☔" },
  63: { text: "비 (보통)", icon: "☔" },
  65: { text: "비 (강함)", icon: "🌧️" },
  71: { text: "눈 (약함)", icon: "🌨️" },
  73: { text: "눈 (보통)", icon: "❄️" },
  75: { text: "눈 (강함)", icon: "❄️" },
  77: { text: "진눈깨비", icon: "🌨️" },
  80: { text: "소나기 (약함)", icon: "🌦️" },
  81: { text: "소나기 (보통)", icon: "🌦️" },
  82: { text: "소나기 (강함)", icon: "⛈️" },
  95: { text: "뇌우", icon: "🌩️" },
  96: { text: "우박 동반 뇌우", icon: "⛈️" },
  99: { text: "강한 우박 동반 뇌우", icon: "⛈️" }
};

// 매핑 테이블에 없는 코드가 올 경우를 대비한 기본값 처리 함수
function getWeatherCondition(code) {
  return weatherCodeMap[code] || { text: "알 수 없음", icon: "❓" };
}

// HTML 엘리먼트 가져오기 (DOM 조작)
const weatherBtn = document.getElementById('get-weather-btn');
const weatherInfo = document.getElementById('weather-info');
const tempElement = document.getElementById('temperature');
const windElement = document.getElementById('windspeed');

// 서울 위도, 경도 좌표
const latitude = 37.5665;
const longitude = 126.9780;
const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true&timezone=Asia/Seoul`;

// 버튼 클릭 이벤트 리스너
weatherBtn.addEventListener('click', async () => {
  try {
    weatherBtn.innerText = '로딩 중...';
    
    // Open-Meteo API 호출 (비동기 처리)
    const response = await fetch(apiUrl);
    const data = await response.json();
    
    // 가져온 데이터 추출
    const current = data.current_weather;
    
    // 화면(DOM) 업데이트
    tempElement.innerText = current.temperature;
    windElement.innerText = current.windspeed;
    
    // 날씨 정보 영역 표시
    weatherInfo.classList.remove('hidden');
    weatherBtn.innerText = '날씨 새로고침';
  } catch (error) {
    alert('날씨 데이터를 가져오는 데 실패했습니다.');
    weatherBtn.innerText = '날씨 불러오기';
    console.error(error);
  }
});