import os
import random

# ===== 경로 설정 =====
BASE_PATH = r"C:\.."
MUSIC_FOLDER = os.path.join(BASE_PATH, "", "")
BG_FOLDER = os.path.join(BASE_PATH, "", "")
OUTPUT_FOLDER = os.path.join(BASE_PATH, "")
OUTPUT_VIDEO = os.path.join(OUTPUT_FOLDER, "")

# ===== 릴스용 영상 생성 (60초, 세로 9:16 비율) =====
def generate_shorts_video():
    music_file = random.choice(os.listdir(MUSIC_FOLDER))
    bg_file = random.choice(os.listdir(BG_FOLDER))

    music_path = os.path.join(MUSIC_FOLDER, music_file)
    bg_path = os.path.join(BG_FOLDER, bg_file)

    cmd = (
        f'ffmpeg -y -stream_loop -1 -i "{bg_path}" -i "{music_path}" '
        f'-t 60 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" '
        f'-shortest -c:v libx264 -c:a aac -preset ultrafast "{OUTPUT_VIDEO}"'
    )
    cmd = (
    f'ffmpeg -y -stream_loop -1 -i "{bg_path}" -i "{music_path}" '
    f'-t 60 -map 0:v:0 -map 1:a:0 '
    f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" '
    f'-c:v libx264 -c:a aac -shortest -preset ultrafast "{OUTPUT_VIDEO}"'
)


    print("🎬 릴스 영상 생성 중...")
    os.system(cmd)
    print("✅ 릴스 영상 생성 완료!")
    print("📂 파일 위치:", OUTPUT_VIDEO)

# ===== 실행 =====
if __name__ == "__main__":
    generate_shorts_video()
