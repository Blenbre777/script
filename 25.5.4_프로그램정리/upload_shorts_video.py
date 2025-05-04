import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# ===== 설정 =====
BASE_PATH = r"C:\.."
OUTPUT_VIDEO = os.path.join(BASE_PATH, "", "")
CREDENTIALS_PATH = os.path.join(BASE_PATH, "", "")

def upload_shorts_video():
    scopes = [""]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "",
                "description": "",
                "tags": [],
                "categoryId": "10"  # 카테고리: 음악 , 범위는 좀 더 찾아봐야할듯 ..
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(OUTPUT_VIDEO)
    )

    response = request.execute()
    print("✅ 릴스 업로드 완료!")
    print("🔗 영상 링크: https://www.youtube.com/watch?v=" + response["id"])


if __name__ == "__main__":
    upload_shorts_video()
