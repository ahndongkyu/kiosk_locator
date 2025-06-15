import webbrowser

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>내 위치 확인</title>
  <style>
    #map { width: 100%; height: 400px; background-color: #eee; }
    #download {
      margin-top: 20px;
    }
    a {
      display: inline-block;
      padding: 10px 20px;
      background: #87CEFA;
      border-radius: 6px;
      color: black;
      text-decoration: none;
      font-weight: bold;
    }
  </style>
  <script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=7a7e89bb0498aad83866c42d6ea0f01f&libraries=services"></script>
</head>
<body>
  <h3>📍 충남 천안시 동남구 문암로 58</h3>
  <div id="map"></div>
  <p id="coord">위도: 36.835340, 경도: 127.179487</p>
  <div id="download"></div>

  <script>
    // 고정된 좌표
    const lat = 36.835340;
    const lng = 127.179487;

    // 지도 띄우기
    const mapContainer = document.getElementById("map");
    const mapOption = {
      center: new kakao.maps.LatLng(lat, lng),
      level: 3
    };
    const map = new kakao.maps.Map(mapContainer, mapOption);
    const marker = new kakao.maps.Marker({
      position: new kakao.maps.LatLng(lat, lng)
    });
    marker.setMap(map);

    // 텍스트 파일 생성
    const content = `lat=${lat}&lng=${lng}`;
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const downloadLink = document.createElement("a");
    downloadLink.href = url;
    downloadLink.download = "user_location.txt";
    downloadLink.innerText = "📥 위치 파일 저장";
    document.getElementById("download").appendChild(downloadLink);
  </script>
</body>
</html>
"""

# 저장 및 브라우저 열기
with open("get_location.html", "w", encoding="utf-8") as f:
    f.write(html_code)

webbrowser.open("get_location.html")
