import requests
import json
from bs4 import BeautifulSoup

# 🔹 네이버 뉴스 크롤링
main_url = "https://media.naver.com/press/055/ranking?type=popular"  # 크롤링할 페이지 URL
headers = {"User-Agent": "Mozilla/5.0"}  # 봇 차단 우회를 위한 헤더 설정
response = requests.get(main_url, headers=headers)
# cronetab으로 실행할때 디렉토리는 절대적으로 선언해야 한다.
path = "/apps/clawler/news/naver-news-kakao/"

news_list = []
list_size = 3

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.select('ul.press_ranking_list li.as_thumb')[:list_size]  # 상위 3개만 추출

    for item in news_items:
        link_tag = item.find('a')
        href = link_tag['href'] if link_tag else 'N/A'
        title_tag = item.find(class_='list_title')
        title = title_tag.text.strip() if title_tag else 'N/A'
        rank_tag = item.find(class_='list_ranking_num')
        rank = rank_tag.text.strip() if rank_tag else 'N/A'
        img_tag = item.find(class_='list_img').find('img') if item.find(class_='list_img') else None
        img_src = img_tag['src'] if img_tag else 'N/A'
        
        news_list.append({
            "title": "top " + rank,
            "image_url": img_src,
            "description": title,
            "link": {
                "web_url": href,
                "mobile_web_url": href
            }
        })
else:
    print("Failed to retrieve the page")

# 🔹 저장된 토큰 불러오기
with open(path + "kakao_code.json", "r") as fp:
    tokens = json.load(fp)

# 🔹 카카오톡 메시지 API URL
kakao_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 🔹 요청 헤더
kakao_headers = {
    "Authorization": "Bearer " + tokens["access_token"],
    "Content-Type": "application/x-www-form-urlencoded"
}

# print(news_list)

kakao_data = {
    "template_object": json.dumps({
        "object_type": "list",
        "header_title": f"네이버 뉴스 랭킹 Top {list_size}",
        "header_link": {
            "web_url": main_url,
            "mobile_web_url": main_url
        },
        "contents": news_list,
        "buttons": [
            {
                "title": "뉴스 전체 보기",
                "link": {
                    "web_url": main_url,
                    "mobile_web_url": main_url
                }
            }
        ]
    })
}

# 🔹 카카오톡 API 요청
kakao_response = requests.post(kakao_url, headers=kakao_headers, data=kakao_data)

# 🔹 응답 확인
print("응답 코드:", kakao_response.status_code)
print("응답 내용:", kakao_response.text)