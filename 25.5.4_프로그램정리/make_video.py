import os
import random

# 폴더 경로 설정
music_folder = ""
bg_folder = ""
output_folder = ""

# 랜덤으로 음악/배경 선택
music_file = random.choice(os.listdir(music_folder))
bg_file = random.choice(os.listdir(bg_folder))

# 파일 경로 지정
music_path = os.path.join(music_folder, music_file)
bg_path = os.path.join(bg_folder, bg_file)
output_path = os.path.join(output_folder, "output.mp4")

# FFmpeg 명령어 실행
#cmd = f'ffmpeg -y -i "{bg_path}" -i "{music_path}" -c:v libx264 -c:a aac -shortest -preset ultrafast "{output_path}"'

# 음악에 맞춰 영상 반복 
cmd = f'ffmpeg -y -stream_loop -1 -i "{bg_path}" -i "{music_path}" -shortest -c:v libx264 -c:a aac -preset ultrafast "{output_path}"'


print("📽️ 영상 생성 중...")
os.system(cmd)
print("✅ 완료! 저장 위치:", output_path)
