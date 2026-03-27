import os
import requests
import base64
from moviepy import ImageClip, AudioFileClip, TextClip, ColorClip, CompositeVideoClip, CompositeAudioClip
from dotenv import load_dotenv

# .env 로드 (GOOGLE_API_KEY 사용)
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))
api_key = os.getenv("GOOGLE_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# New image path from v2 generation (Korean Kim + Daughter, only 2 people)
IMAGE_PATH = r"C:\Users\ryu\.gemini\antigravity\brain\0fbf1fbe-88ba-4bf7-95dc-d73c0de2fa68\intro_hook_korean_kim_v2_1774553308179.png"
AUDIO_PATH = os.path.join(BASE_DIR, "intro_hook_audio.mp3")
OUTPUT_PATH = os.path.join(BASE_DIR, "intro_hook_video_final_16_9.mp4")
FONT_PATH = 'C:/Windows/Fonts/malgun.ttf'
BGM_PATH = r"d:\Vibe_Coding\chatsapiens\video_creator\imagen-character-lock\senior story BGM (1).wav"

# Standard 16:9 HD resolution
W, H = 1920, 1080

def generate_audio_via_rest(text):
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env")
    
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": "ko-KR",
            "name": "ko-KR-Neural2-B"
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 0.8
        }
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        audio_content = response.json().get("audioContent")
        with open(AUDIO_PATH, "wb") as f:
            f.write(base64.b64decode(audio_content))
        print(f"Audio generated: {AUDIO_PATH}")
    else:
        raise Exception(f"TTS API Error: {response.text}")

def assemble_video():
    text_to_speak = "20년 전 잃어버린 우리 딸이, 죽기 직전 제 병실 문을 열고 들어왔어요. 이게 꿈일까요, 아니면 하늘이 주신 마지막 기적일까요?"
    
    # 1. Audio Generation
    generate_audio_via_rest(text_to_speak)
    
    audio = AudioFileClip(AUDIO_PATH)
    duration = audio.duration
    
    # 2. Image Clip (Force 16:9 and Slow Zoom)
    img_clip = ImageClip(IMAGE_PATH).with_duration(duration)
    # Resize to cover 16:9 area then zoom
    img_clip = img_clip.resized(width=W) 
    if img_clip.h < H:
        img_clip = img_clip.resized(height=H)
    
    img_clip = img_clip.resized(lambda t: 1.0 + 0.05 * (t / duration)) # Slow zoom
    img_clip = img_clip.cropped(x1=(img_clip.w - W)//2, y1=(img_clip.h - H)//2, width=W, height=H) # Center crop to 16:9
    
    # 3. Subtitles (2 lines, SAME font size as requested)
    line1 = "20년 만에 돌아온 딸,"
    line2 = "죽기 직전 마주한 기적"
    
    shared_font_size = 70
    
    txt_clip1 = TextClip(
        text=line1,
        font_size=shared_font_size,
        color='yellow',
        font=FONT_PATH,
        method='caption',
        text_align='center',
        size=(int(W * 0.8), None)
    ).with_duration(duration)

    txt_clip2 = TextClip(
        text=line2,
        font_size=shared_font_size,
        color='yellow',
        font=FONT_PATH,
        method='caption',
        text_align='center',
        size=(int(W * 0.8), None)
    ).with_duration(duration)

    # Position lines vertically
    spacing = 20
    total_text_h = txt_clip1.h + txt_clip2.h + spacing
    
    bg_width = int(W * 0.9)
    bg_height = int(total_text_h * 1.5)
    bg_clip = ColorClip(size=(bg_width, bg_height), color=(0, 0, 0)).with_opacity(0.6).with_duration(duration)

    # Combine text and background
    sub_group = CompositeVideoClip([
        bg_clip.with_position('center'),
        txt_clip1.with_position(('center', (bg_height - total_text_h)//2)),
        txt_clip2.with_position(('center', (bg_height - total_text_h)//2 + txt_clip1.h + spacing))
    ]).with_position(('center', int(H * 0.8))) # Adjusted for 16:9

    final_video = CompositeVideoClip([img_clip, sub_group])
    
    # 4. Audio (Mix with BGM)
    if os.path.exists(BGM_PATH):
        bgm = AudioFileClip(BGM_PATH).with_duration(duration).with_volume_scaled(0.15)
        final_audio = CompositeAudioClip([audio, bgm])
        final_video = final_video.with_audio(final_audio)
    else:
        final_video = final_video.with_audio(audio)

    # Export
    final_video.write_videofile(OUTPUT_PATH, fps=24, codec="libx264", audio_codec="aac")
    print(f"Video generated: {OUTPUT_PATH}")

if __name__ == "__main__":
    assemble_video()
