import requests
import json
import time

def get_lotto_test():
    lotto_results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 1100회차부터 최근 5개만 테스트
    for i in range(1100, 1105):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
        try:
            print(f"Attempting to fetch draw {i}...")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            # 응답 내용의 앞부분 100자만 출력해보기 (HTML인지 JSON인지 확인용)
            print(f"Response snippet: {response.text[:100]}")
            
            data = response.json()
            if data.get("returnValue") == "success":
                lotto_results.append(data)
                print(f"Success for {i}")
            else:
                print(f"Fail: returnValue is {data.get('returnValue')}")
        except Exception as e:
            print(f"Error at draw {i}: {e}")
        
        time.sleep(1) # 테스트 시에는 여유 있게
        
    return lotto_results

results = get_lotto_test()

if results:
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Done! Saved {len(results)} items.")
else:
    print("CRITICAL: No data collected at all.")
