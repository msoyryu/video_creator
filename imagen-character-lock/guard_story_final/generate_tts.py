import os
import re
from gtts import gTTS

# 설정
SCRIPT_PATH = r"d:\Vibe_Coding\chatsapiens\video_creator\imagen-character-lock\guard_story_final\script_v4.md"
AUDIO_OUTPUT_DIR = r"d:\Vibe_Coding\chatsapiens\video_creator\imagen-character-lock\guard_story_final\audio"

if not os.path.exists(AUDIO_OUTPUT_DIR):
    os.makedirs(AUDIO_OUTPUT_DIR)

def generate_tts():
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 나래이션 부분 추출 (Cut X.X ... 나래이션: ...)
    # 나래이션 혹은 나레이션 둘 다 대응, 대소문자 무시, 멀티라인 텍스트 추출
    pattern = re.compile(r"Cut\s+(\d+\.\d+)[\s\S]*?(?:나래이션|나레이션|나뢰이션)\*?: \s*([\s\S]*?)(?=\n+\*|\n+##|$)", re.IGNORECASE)
    matches = pattern.findall(content)

    print(f"Total scenes found: {len(matches)}")

    for i, (cut_id, text) in enumerate(matches):
        clean_text = text.strip().replace("\n", " ")
        filename = f"{cut_id.replace('.', '_')}.mp3"
        filepath = os.path.join(AUDIO_OUTPUT_DIR, filename)
        
        print(f"[{i+1}/{len(matches)}] Generating {filename}...")
        
        # gTTS 사용 (한국어)
        tts = gTTS(text=clean_text, lang='ko')
        tts.save(filepath)

    print("Success: All TTS files generated in", AUDIO_OUTPUT_DIR)

if __name__ == "__main__":
    generate_tts()
