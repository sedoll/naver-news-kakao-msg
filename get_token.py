import requests
import json

# Kakao REST API 정보를 입력합니다.
rest_api_key = ''
redirect_uri = ''
token_url = 'https://kauth.kakao.com/oauth/token'
tokens = None
# cronetab으로 실행할때 디렉토리는 절대적으로 선언해야 한다.
path = "/apps/clawler/news/naver-news-kakao/"

# 카카오 토큰 갱신하기
def refresh_token():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
    "grant_type": "refresh_token",
    "client_id": rest_api_key,
    "refresh_token": tokens['refresh_token']
    }

    response = requests.post(url, data=data)

    # 갱신 된 토큰 내용 확인
    result = response.json()

    # 갱신 된 내용으로 파일 업데이트
    if 'access_token' in result:
        tokens['access_token'] = result['access_token']

    if 'refresh_token' in result:
        tokens['refresh_token'] = result['refresh_token']
    else:
        pass
    
    print("result ", result)
    print("tokens ", tokens)
    with open(path + "kakao_code.json", "w") as fp:
        json.dump(tokens, fp)

# 토큰을 갱신하기 위해 먼저 기존 토큰을 불러옵니다.
with open(path + "kakao_code.json", "r") as fp:
    tokens = json.load(fp)

refresh_token()