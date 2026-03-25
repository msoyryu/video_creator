import os
import re
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip, AudioFileClip

# 경로 설정
BASE_DIR = r"d:\Vibe_Coding\chatsapiens\video_creator\imagen-character-lock\guard_story_final"
IMAGE_DIR = os.path.join(BASE_DIR, "images")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
BGM_PATH = os.path.join(BASE_DIR, "bgm.mp3")  # 사용자가 Suno로 만들어야 함
OUTPUT_PATH = os.path.join(BASE_DIR, "final_video.mp4")

# 정규식으로 컷 순서 정렬 (01_01, 01_02, ... 08_03)
def get_sort_key(filename):
    nums = re.findall(r"\d+", filename)
    return [int(n) for n in nums]

def assemble_video():
    image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")], key=get_sort_key)
    audio_files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")], key=get_sort_key)

    print(f"Images: {len(image_files)}, Audio: {len(audio_files)}")

    clips = []
    
    for img_file, aud_file in zip(image_files, audio_files):
        img_path = os.path.join(IMAGE_DIR, img_file)
        aud_path = os.path.join(AUDIO_DIR, aud_file)
        
        print(f"Processing {img_file} with {aud_file}...")
        
        # 오디오 로드 및 길이 측정
        audio = AudioFileClip(aud_path)
        duration = audio.duration
        
        # 이미지 클립 생성 (나래이션 길이에 맞춤)
        # MoviePy 2.x에서는 슬로우 줌 효과를 위해 resized() 직접 호출 가능
        img_clip = ImageClip(img_path).with_duration(duration)
        
        # 슬로우 줌 연출 (1.0에서 1.05로 줌)
        img_clip = img_clip.resized(lambda t: 1.0 + 0.05 * (t / duration))
        
        img_clip = img_clip.with_audio(audio)
        clips.append(img_clip)

    print("Concatenating clips...")
    final_clip = concatenate_videoclips(clips, method="compose")

    # BGM 추가 (파일이 있을 경우만)
    if os.path.exists(BGM_PATH):
        print("Adding BGM...")
        bgm = AudioFileClip(BGM_PATH).with_duration(final_clip.duration).with_volume_scaled(0.15)
        # 기존 나래이션과 병합
        final_audio = CompositeAudioClip([final_clip.audio, bgm])
        final_clip = final_clip.with_audio(final_audio)
    else:
        print("Warning: bgm.mp3 not found. Video will have narration only.")

    print(f"Writing final video to {OUTPUT_PATH}...")
    final_clip.write_videofile(OUTPUT_PATH, fps=24, codec="libx264", audio_codec="aac")
    print("Success: Video generated!")

if __name__ == "__main__":
    assemble_video()
