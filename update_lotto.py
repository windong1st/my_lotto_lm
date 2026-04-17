import requests
import json
import time

def get_lotto_data():
    lotto_results = []
    # 브라우저와 거의 동일한 헤더 구성
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.dhlottery.co.kr/common.do?method=main',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # 1. 테스트용으로 최근 10개만 먼저 수집 시도
    for i in range(1100, 1110):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"[{i}회차] Status: {response.status_code}")
            
            # JSON 변환 시도
            data = response.json()
            if data.get("returnValue") == "success":
                lotto_results.append(data)
                print(f"[{i}회차] 수집 성공")
            else:
                print(f"[{i}회차] 데이터 없음")
        except Exception as e:
            print(f"[{i}회차] 에러: {e}")
            # 만약 HTML이 돌아온다면 여기서 에러가 남. 실제 내용 확인용:
            # print(response.text[:100]) 
            
        time.sleep(0.5) # 차단 방지용 딜레이
        
    return lotto_results

# 데이터가 하나라도 있으면 저장
data = get_lotto_data()
if data:
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"총 {len(data)}건 저장 완료")
else:
    print("수집된 데이터가 없어 파일을 생성하지 않았습니다.")
