import requests
import json
import os

def get_all_lotto_data():
    lotto_results = []
    # 최신 회차를 자동으로 파악하기 위해 넉넉히 범위를 잡거나 
    # 일단 1회부터 1200회까지 돌립니다. (GitHub 서버는 빠릅니다)
    for i in range(1, 1200):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("returnValue") == "success":
            numbers = [data[f"drwtNo{j}"] for j in range(1, 7)]
            lotto_results.append({
                "drwNo": data["drwNo"],
                "numbers": numbers,
                "drwNoDate": data["drwNoDate"]
            })
        else:
            break # 데이터가 없으면 중단
            
    return lotto_results

data = get_all_lotto_data()
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
