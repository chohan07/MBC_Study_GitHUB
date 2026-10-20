const http = require("http");
const fs = require("fs");
const path = require("path");
const dotenv = require("dotenv");

dotenv.config();

const PORT = 3000;
const API_KEY = process.env.OPENWEATHER_API_KEY;

// 주요 도시 좌표 정보
const CITIES = {
  seoul: { name: "서울", lat: 37.5665, lon: 126.9780 },
  tokyo: { name: "도쿄", lat: 35.6762, lon: 139.6503 },
  newyork: { name: "뉴욕", lat: 40.7128, lon: -74.0060 },
  london: { name: "런던", lat: 51.5074, lon: -0.1278 },
  paris: { name: "파리", lat: 48.8566, lon: 2.3522 }
};

if (!API_KEY) {
  console.error("❌ .env 파일에 OPENWEATHER_API_KEY가 설정되지 않았습니다!");
  process.exit(1);
}

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg"
};

const server = http.createServer(async (req, res) => {
  try {
    const reqUrl = new URL(req.url, `http://localhost:${PORT}`);

    // 1. 단일 도시 날씨 API (/api/weather?city=seoul)
    if (reqUrl.pathname === "/api/weather") {
      const cityKey = reqUrl.searchParams.get("city") || "seoul";
      const targetCity = CITIES[cityKey] || CITIES.seoul;

      const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${targetCity.lat}&lon=${targetCity.lon}&appid=${encodeURIComponent(API_KEY)}&units=metric&lang=kr`;

      const response = await fetch(apiUrl);
      const data = await response.text();

      res.writeHead(response.ok ? 200 : response.status, { "Content-Type": "application/json; charset=utf-8" });
      res.end(data);
      return;
    }

    // 2. 전체 도시 병렬 날씨 API (/api/weather/compare)
    if (reqUrl.pathname === "/api/weather/compare") {
      const cityKeys = Object.keys(CITIES);
      const promises = cityKeys.map(async (key) => {
        const city = CITIES[key];
        const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${city.lat}&lon=${city.lon}&appid=${encodeURIComponent(API_KEY)}&units=metric&lang=kr`;
        const resp = await fetch(apiUrl);
        const json = await resp.json();
        return {
          key: key,
          name: city.name,
          temp: json.main ? Math.round(json.main.temp * 10) / 10 : 0,
          humidity: json.main ? json.main.humidity : 0
        };
      });

      const results = await Promise.all(promises);
      res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
      res.end(JSON.stringify(results));
      return;
    }

    // 3. 정적 파일 서빙
    let requestedPath = reqUrl.pathname === "/" ? "/index.html" : reqUrl.pathname;
    const filePath = path.join(__dirname, "public", requestedPath);
    const ext = path.extname(filePath);
    const contentType = mimeTypes[ext] || "application/octet-stream";

    fs.readFile(filePath, (error, data) => {
      if (error) {
        res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
        res.end("페이지를 찾을 수 없습니다.");
        return;
      }
      res.writeHead(200, { "Content-Type": contentType });
      res.end(data);
    });

  } catch (error) {
    console.error("서버 에러:", error);
    res.writeHead(500, { "Content-Type": "application/json; charset=utf-8" });
    res.end(JSON.stringify({ error: "서버 내부 오류 발생" }));
  }
});

server.listen(PORT, () => {
  console.log(`✅ 날씨 앱 서버 실행 성공: http://localhost:${PORT}`);
});