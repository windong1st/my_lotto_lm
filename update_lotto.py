import requests
import json
import time

def get_all_lotto_data():
    lotto_results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.dhlottery.co.kr/common.do?method=main'
    }
    
    with requests.Session() as session:
        session.headers.update(headers)
        # 초기 접속으로 쿠키 굽기
        session.get("https://www.dhlottery.co.kr/common.do?method=main")
        
        # 테스트를 위해 우선 1회부터 100회까지만 수집해보고, 성공하면 숫자를 늘리세요.
        for i in range(1, 100): 
            try:
                url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
                response = session.get(url, timeout=10)
                
                if response.status_code != 200: break
                
                data = response.json()
                if data.get("returnValue") == "success":
                    numbers = [data[f"drwtNo{j}"] for j in range(1, 7)]
                    lotto_results.append({"drwNo": data["drwNo"], "numbers": numbers, "drwNoDate": data["drwNoDate"]})
                else: break
                
                time.sleep(0.3) # 차단 방지 지연시간
            except:
                break
                
    return lotto_results

data = get_all_lotto_data()
if data:
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Successfully saved {len(data)} items.")
else:
    print("No data collected.")
