import os
import requests
import base64
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))
api_key = os.getenv("GOOGLE_API_KEY")

# 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_TEXT = "매일 밤 10시, 도시는 잠들지만 70세 김 씨의 하루는 이제 시작됩니다."
AUDIO_PATH = os.path.join(BASE_DIR, "01_01.mp3")

def generate_google_neural_slow():
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return

    # 유저가 선택한 2번 목소리 (Neural2-B)
    voice_name = "ko-KR-Neural2-B" 
    
    print(f"Generating Google Neural2-B (Slower 0.8x): {TEST_TEXT}")
    
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    
    payload = {
        "input": {"text": TEST_TEXT},
        "voice": {
            "languageCode": "ko-KR",
            "name": voice_name
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
        print(f"Success: Audio generated at {AUDIO_PATH}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    generate_google_neural_slow()
