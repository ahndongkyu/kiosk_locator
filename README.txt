# 🗺️ 무인민원발급기 위치 조회 프로그램

> 현재 위치를 기준으로 가까운 무인민원발급기 5개를 찾아주는 Python GUI 프로그램입니다.  
> 공공데이터와 Kakao Maps API를 활용해 사용자에게 실시간 위치 기반 정보를 제공합니다.

---

## ✅ 주요 기능

- 📍 **현재 위치 기반 조회**  
  브라우저를 통해 내 위치를 확인하고, 가장 가까운 무인민원발급기 5곳을 자동으로 계산

- 🔎 **지도 보기**  
  Kakao Map을 통해 선택한 발급기의 위치를 지도에서 확인 가능

- ℹ️ **상세 정보 확인**  
  각 발급기의 운영 시간, 상세 위치 등 정보를 팝업으로 제공

- 📂 **공공데이터 기반 정제**  
  행정안전부 무인민원발급기 위치 데이터를 활용하여 정확한 위치 정보 제공

---

## 🛠 사용 기술

- Python 3.x
- Tkinter (GUI)
- Pandas (데이터 처리)
- Geopy (거리 계산)
- Kakao REST API (주소 → 위경도 변환)
- Webbrowser (지도 링크 실행)

---

## 🧑‍💻 실행 방법

1. 이 저장소를 클론하거나 압축 파일을 해제합니다.

```bash
git clone https://github.com/your-username/kiosk-locator.git

2. 필요한 라이브러리를 설치합니다.

pip install pandas geopy

3. 현재 위치를 받아오기 위해 get_location.html을 열어 위치를 확인한 후,
표시된 lat=...&lng=... 값을 복사하여 user_location.txt 파일로 저장합니다.

예시 (user_location.txt 내용): lat=37.5665&lng=126.9780

4. 메인 프로그램을 실행합니다.
python main.py

📁 파일 구성

📦 kiosk-locator/
├── main.py                     # 메인 실행 파일 (Tkinter GUI)
├── 무인민원발급기_최종.csv        # 위경도 포함된 정제된 공공데이터
├── get_location.html          # 현재 위치 확인용 HTML
├── user_location.txt          # 사용자 위치 정보 저장 파일
└── README.md

📌 데이터 출처
	•	행정안전부 공공데이터포털
👉 https://www.data.go.kr
