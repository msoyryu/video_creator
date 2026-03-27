import os
from moviepy import ImageClip, AudioFileClip, TextClip, ColorClip, CompositeVideoClip, CompositeAudioClip

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 사용자가 이름을 바꾼 BGM 파일 사용
BGM_PATH = r"d:\Vibe_Coding\chatsapiens\video_creator\imagen-character-lock\senior story BGM (1).wav"
IMAGE_PATH = os.path.join(BASE_DIR, "01_01.jpg")
AUDIO_PATH = os.path.join(BASE_DIR, "01_01.mp3")
OUTPUT_PATH = os.path.join(BASE_DIR, "test_output_bgm.mp4")
FONT_PATH = 'C:/Windows/Fonts/malgun.ttf'

def assemble_final_refined():
    if not os.path.exists(AUDIO_PATH):
        print(f"Error: {AUDIO_PATH} not found.")
        return

    print("Loading clips...")
    audio = AudioFileClip(AUDIO_PATH)
    duration = audio.duration

    # 1. 이미지 클립 (슬로우 줌 효과)
    img_clip = ImageClip(IMAGE_PATH).with_duration(duration)
    img_clip = img_clip.resized(lambda t: 1.0 + 0.05 * (t / duration))

    # 2. 자막 클립 (배경 높이와 투명도 60% 조정)
    sub_text = "매일 밤 10시, 도시는 잠들지만 70세 김 씨의 하루는 이제 시작됩니다."
    try:
        # 텍스트 클립 생성 (배경색 없음)
        txt_clip = TextClip(
            text=sub_text,
            font_size=32,
            color='white',
            font=FONT_PATH,
            method='caption',
            text_align='center',
            size=(int(img_clip.w * 0.8), None)
        ).with_duration(duration)

        # 투명도 60% 검은색 배경 클립 생성 (텍스트보다 약간 크게)
        bg_width = int(img_clip.w * 0.9)
        bg_height = int(txt_clip.h * 1.5) # 배경 높이를 상위로 넉넉하게 잡음
        bg_clip = ColorClip(
            size=(bg_width, bg_height),
            color=(0, 0, 0)
        ).with_opacity(0.6).with_duration(duration) # 진하기 60%

        # 자막 위치 조정 (0.85 지점으로 원위치)
        pos_y = int(img_clip.h * 0.85)
        
        # 배경과 텍스트를 중앙 정렬로 합성
        sub_group = CompositeVideoClip([
            bg_clip.with_position('center'),
            txt_clip.with_position('center')
        ]).with_position(('center', pos_y))
        
        # 이미지와 최종 자막 합산
        final_clip = CompositeVideoClip([img_clip, sub_group])
    except Exception as e:
        print(f"Subtitles failed: {e}")
        final_clip = img_clip

    # 3. 오디오 합성
    if os.path.exists(BGM_PATH):
        print(f"Adding BGM from: {BGM_PATH}")
        bgm = AudioFileClip(BGM_PATH).with_duration(duration).with_volume_scaled(0.15)
        final_audio = CompositeAudioClip([audio, bgm])
        final_clip = final_clip.with_audio(final_audio)
    else:
        print(f"Warning: BGM not found at {BGM_PATH}")
        final_clip = final_clip.with_audio(audio)
    
    print(f"Writing test video to {OUTPUT_PATH}...")
    final_clip.write_videofile(OUTPUT_PATH, fps=24, codec="libx264", audio_codec="aac")
    print("Success: Final refined test video generated!")

if __name__ == "__main__":
    assemble_final_refined()
