import requests
from datetime import datetime

# ===== 노션 설정 =====
NOTION_TOKEN = ""
NOTION_DATABASE_ID = ""

def send_to_notion(title, url):
    now = datetime.now().isoformat()

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "제목": {
                "title": [{
                    "text": { "content": title }
                }]
            },
            "링크": {
                "url": url
            },
            "업로드시간": {
                "date": {
                    "start": now
                }
            }
        }
    }

    print("📡 노션 전송 시도 중...")
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)

    print("📦 상태 코드:", response.status_code)
    print("🧾 응답 내용:\n", response.text)

    if response.status_code in [200, 201]:
        print("✅ 노션 전송 성공!")
    else:
        print("❌ 노션 전송 실패 — 위 응답을 참고해서 문제를 해결하세요.")

# 테스트 실행
if __name__ == "__main__":
    send_to_notion("🌙 테스트 영상 제목", "https://youtube.com/watch?v=dQw4w9WgXcQ")
