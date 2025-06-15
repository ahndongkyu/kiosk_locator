import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import tkinter as tk
import webbrowser

# 현재 위치 불러오기
with open("user_location.txt", "r", encoding="utf-8") as f:
    content = f.read().strip()
    lat = float(content.split("lat=")[1].split("&")[0])
    lng = float(content.split("lng=")[1])
    user_coords = (lat, lng)

# 주소 변환
geolocator = Nominatim(user_agent="location_app")
location = geolocator.reverse((lat, lng), language="ko")
short_address = "주소 확인 실패"
if location and location.address:
    address_text = location.address
    short_address = " ".join(address_text.split()[1:4])

# CSV 데이터
df = pd.read_csv("무인민원발급기_최종.csv", encoding="utf-8")

# 거리 계산
def calculate_distances(center_lat, center_lng):
    center_coords = (center_lat, center_lng)
    df["거리(km)"] = df.apply(
        lambda row: geodesic(center_coords, (row["위도"], row["경도"])).km,
        axis=1
    )
    return df.sort_values("거리(km)").head(5)

# 지도 링크 열기

def open_map(lat, lng, name="무인발급기"):
    url = f"https://map.kakao.com/link/map/{name},{lat},{lng}"
    webbrowser.open(url)

# 상세정보 팝업
def show_details(row):
    win = tk.Toplevel()
    win.title(f"{row['발급기명']} - 상세정보")
    info = f"""발급기명: {row['발급기명']}

주소: {row['설치장소주소']}
상세위치: {row.get('설치장소상세위치', '-')}

평일 운영: {row.get('평일운영시작시각', '-') or '-'} ~ {row.get('평일운영종료시각', '-') or '-'}
공휴일 운영: {row.get('공휴일운영시작시각', '-') or '-'} ~ {row.get('공휴일운영종료시각', '-') or '-'}

"""
    tk.Label(win, text=info.strip(), font=("Noto Sans CJK KR", 10, "bold"), justify="left", anchor="w", wraplength=400, padx=20, pady=20).pack()

# GUI 실행
def show_gui():
    root = tk.Tk()
    root.title("무인민원발급기 위치 조회기")
    root.geometry("750x650")
    root.configure(bg="white")

    # 프로그램 제목
    tk.Label(root, text="무인민원발급기 위치 조회기", font=("Noto Sans CJK KR", 16, "bold"), bg="white").pack(pady=(20, 20))

    # 현재 위치
    tk.Label(root, text="현재 위치", font=("Noto Sans CJK KR", 13, "bold"), bg="white").pack()
    tk.Label(root, text=short_address, font=("Noto Sans CJK KR", 11), bg="white").pack()
    tk.Label(root, text=f"위도 {lat:.5f}, 경도 {lng:.5f}", font=("Noto Sans CJK KR", 9), fg="gray", bg="white").pack(pady=(0, 15))

    # 검색창
    search_frame = tk.Frame(root, bg="white")
    search_frame.pack(pady=(0, 15))

    tk.Label(search_frame, text="다른 위치로 검색:", font=("Noto Sans CJK KR", 10), bg="white").pack(side="left", padx=(0, 5))
    location_entry = tk.Entry(search_frame, width=30, font=("Noto Sans CJK KR", 10), relief="solid", bd=1)
    location_entry.pack(side="left", ipady=4, padx=(0, 5))

    def on_search():
        query = location_entry.get().strip()
        if not query:
            return
        try:
            location = geolocator.geocode(query)
            if location:
                update_results(location.latitude, location.longitude, f"(입력 위치: {query})")
        except Exception as e:
            tk.Label(result_frame, text=f"에러: {e}", fg="red", bg="white").grid(row=0, column=0)

    def back_to_current():
        update_results(lat, lng, "(현재 위치 기준)")

    btn_style = {"font": ("Noto Sans CJK KR", 9), "padx": 10, "pady": 5, "width": 6}
    tk.Button(search_frame, text="조회", command=on_search, bg="#4682B4", fg="white", **btn_style).pack(side="left")
    tk.Button(search_frame, text="현재 위치", command=back_to_current, bg="#D3D3D3", **btn_style).pack(side="left", padx=5)

    global result_frame
    result_frame = tk.Frame(root, bg="white")
    result_frame.pack(pady=(0, 20), fill="both")

    def update_results(center_lat, center_lng, query_label="(현재 위치 기준)"):
        for widget in result_frame.winfo_children():
            widget.destroy()

        nearest = calculate_distances(center_lat, center_lng)

        tk.Label(result_frame, text=f"조회 결과 {query_label}",
                 font=("Noto Sans CJK KR", 11, "bold"), bg="white").pack(anchor="w", padx=20, pady=(0, 15))

        for idx, (_, row_data) in enumerate(nearest.iterrows(), start=1):
            entry_frame = tk.Frame(result_frame, bg="white", bd=1, relief="solid")
            entry_frame.pack(fill="x", padx=20, pady=5)

            left = tk.Frame(entry_frame, bg="white")
            left.pack(side="left", fill="both", expand=True)

            right = tk.Frame(entry_frame, bg="white")
            right.pack(side="right", padx=10)

            # 주소 길이 제한
            short_address_text = row_data['설치장소주소']
            if len(short_address_text) > 40:
                short_address_text = short_address_text[:40] + "..."

            info_text = f"{idx}. {row_data['발급기명']} ({row_data['거리(km)']:.2f} km)\n\n주소: {short_address_text}"
            tk.Label(left, text=info_text, font=("Noto Sans CJK KR", 10), justify="left", anchor="w",
                     bg="white", wraplength=500).pack(anchor="w", padx=10, pady=8)

            btn_row = tk.Frame(right, bg="white")
            btn_row.pack()

            tk.Button(btn_row, text="지도", command=lambda lat=row_data['위도'], lng=row_data['경도'], name=row_data['발급기명']: open_map(lat, lng, name),
                      bg="#5F9EA0", fg="white", font=("Noto Sans CJK KR", 9), width=8, height=2).pack(side="left", padx=5)

            tk.Button(btn_row, text="상세정보", command=lambda r=row_data: show_details(r),
                      bg="#778899", fg="white", font=("Noto Sans CJK KR", 9), width=8, height=2).pack(side="left", padx=5)

    update_results(lat, lng)
    root.mainloop()

# 실행
show_gui()
