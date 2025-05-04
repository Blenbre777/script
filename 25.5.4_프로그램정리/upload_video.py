import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# 인증 정보 경로
CLIENT_SECRET_FILE = r""  

# 업로드할 영상 정보
VIDEO_FILE = r""
TITLE = ""
DESCRIPTION = ""
CATEGORY_ID = "10"  # Music
TAGS = [""]

# OAuth 인증 플로우 실행
scopes = ["https://www.googleapis.com/auth/youtube.upload"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes)
credentials = flow.run_local_server(port=0)

# 유튜브 API 클라이언트 생성
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# 영상 업로드 요청
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": CATEGORY_ID
        },
        "status": {
            "privacyStatus": "public"  # 또는 'unlisted'/'private'
        }
    },
    media_body=MediaFileUpload(VIDEO_FILE)
)

response = request.execute()
print("✅ 업로드 완료!")
print("영상 링크: https://www.youtube.com/watch?v=" + response["id"])
