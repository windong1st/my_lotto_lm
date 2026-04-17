import requests
import json
import time

def get_all_lotto_data():
    lotto_results = []
    
    # 브라우저인 것처럼 보이게 하는 헤더 추가
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 세션 사용 (연결 유지)
    session = requests.Session()
    session.headers.update(headers)

    for i in range(1, 1200):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
        
        try:
            response = session.get(url, timeout=10)
            
            # 응답이 정상인지 확인
            if response.status_code != 200:
                print(f"{i}회차 요청 실패 (상태 코드: {response.status_code})")
                break
                
            data = response.json()
            
            if data.get("returnValue") == "success":
                numbers = [data[f"drwtNo{j}"] for j in range(1, 7)]
                lotto_results.append({
                    "drwNo": data["drwNo"],
                    "numbers": numbers,
                    "drwNoDate": data["drwNoDate"]
                })
                # 진행 상황 출력 (로그 확인용)
                if i % 100 == 0:
                    print(f"{i}회차 수집 중...")
            else:
                print(f"수집 완료: {i-1}회차가 마지막 데이터입니다.")
                break
                
        except Exception as e:
            print(f"{i}회차 수집 중 에러 발생: {e}")
            break
            
        # 서버 부하를 줄이기 위한 미세한 지연 (차단 예방)
        time.sleep(0.2)
            
    return lotto_results

# 실행 및 저장
try:
    data = get_all_lotto_data()
    if data:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"성공: 총 {len(data)}개의 데이터를 저장했습니다.")
    else:
        print("실패: 수집된 데이터가 없습니다.")
except Exception as e:
    print(f"최종 저장 중 에러: {e}")
