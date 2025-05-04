import os
import random
import json
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timezone, timedelta

# ===== 경로 설정 =====
BASE_PATH = r"C:\test"
MUSIC_FOLDER = os.path.join(BASE_PATH, "", "")
BG_FOLDER = os.path.join(BASE_PATH, "", "")
OUTPUT_FOLDER = os.path.join(BASE_PATH, "")
CREDENTIALS_PATH = os.path.join(BASE_PATH, "", "")
TOKEN_PATH = os.path.join(BASE_PATH, "", "")
SHORTS_VIDEO = os.path.join(OUTPUT_FOLDER, "")
LONG_VIDEO = os.path.join(OUTPUT_FOLDER, "")

# ===== 노션 설정 =====
NOTION_TOKEN = ""
NOTION_DATABASE_ID = ""

# ===== 노션에 전송 (디버깅 모드 포함) =====
def send_to_notion(title, url):
    now = datetime.now(timezone(timedelta(hours=9))).isoformat()  # KST (UTC+9)

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
    print("🧾 응답 내용:", response.text)

    if response.status_code in [200, 201]:
        print("✅ 노션 전송 성공!")
    else:
        print("❌ 노션 전송 실패 — 위 응답을 참고해서 문제를 해결하세요.")

# ===== 키워드 기반 정보 생성 =====
def create_metadata(keyword, is_shorts=True):
    if is_shorts:
        title = f""
        description = f""
        tags = [keyword, ]
    else:
        title = f""
        description = f""
        tags = [keyword, ]
    return title, description, tags

# ===== 릴스용 영상 생성 =====
def generate_shorts_video():
    music_file = random.choice(os.listdir(MUSIC_FOLDER))
    bg_file = random.choice(os.listdir(BG_FOLDER))

    music_path = os.path.join(MUSIC_FOLDER, music_file)
    bg_path = os.path.join(BG_FOLDER, bg_file)

    cmd = (
        f'ffmpeg -y -stream_loop -1 -i "{bg_path}" -i "{music_path}" '
        f'-t 60 -map 0:v:0 -map 1:a:0 '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" '
        f'-c:v libx264 -c:a aac -shortest -preset ultrafast "{SHORTS_VIDEO}"'
    )
    print("🎬 릴스 영상 생성 중...")
    os.system(cmd)
    print("✅ 릴스 영상 생성 완료!")

# ===== 일반 영상 생성 =====
def generate_long_video():
    music_file = random.choice(os.listdir(MUSIC_FOLDER))
    bg_file = random.choice(os.listdir(BG_FOLDER))

    music_path = os.path.join(MUSIC_FOLDER, music_file)
    bg_path = os.path.join(BG_FOLDER, bg_file)

    cmd = (
        f'ffmpeg -y -stream_loop -1 -i "{bg_path}" -i "{music_path}" '
        f'-map 0:v:0 -map 1:a:0 '
        f'-vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" '
        f'-c:v libx264 -c:a aac -shortest -preset ultrafast "{LONG_VIDEO}"'
    )
    print("🎬 일반 영상 생성 중...")
    os.system(cmd)
    print("✅ 일반 영상 생성 완료!")

# ===== 유튜브 업로드 함수 =====
def upload_video(video_path, title, description, tags):
    scopes = [""]
    print("🔍 인증 정보 확인 중...")

    credentials = None
    if os.path.exists(TOKEN_PATH):
        print("📄 token.json 발견됨 → 자동 로그인 시도")
        credentials = Credentials.from_authorized_user_file(TOKEN_PATH, scopes)
    else:
        print("🆕 token.json 없음 → 새 인증 진행 중...")
        try:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, scopes)
            print("🌐 브라우저 열기 전 준비 완료")
            credentials = flow.run_local_server(port=0)
            print("✅ 인증 완료 → token.json 저장 시도")
            os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
            with open(TOKEN_PATH, 'w') as token_file:
                token_file.write(credentials.to_json())
            print("✅ token.json 저장 완료")
        except Exception as e:
            print("❌ 인증 중 오류 발생:", e)
            return

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "10"  # Music
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_path)
    )

    response = request.execute()
    video_id = response["id"]
    video_url = "https://www.youtube.com/watch?v=" + video_id

    print("✅ 업로드 완료!")
    print("🔗 영상 링크:", video_url)

    # 노션에 업로드 결과 전송
    send_to_notion(title, video_url)


# ===== 실행 =====
if __name__ == "__main__":
    keyword = random.choice([
        
    ])

    print(f"\n🚀 키워드: {keyword}")

    # 릴스 생성 + 업로드
    shorts_title, shorts_desc, shorts_tags = create_metadata(keyword, is_shorts=True)
    generate_shorts_video()
    upload_video(SHORTS_VIDEO, shorts_title, shorts_desc, shorts_tags)

    # 일반 영상 생성 + 업로드
    long_title, long_desc, long_tags = create_metadata(keyword, is_shorts=False)
    generate_long_video()
    upload_video(LONG_VIDEO, long_title, long_desc, long_tags)
