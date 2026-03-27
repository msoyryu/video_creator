import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))
api_key = os.getenv("GOOGLE_API_KEY")

def list_voices():
    url = f"https://texttospeech.googleapis.com/v1/voices?key={api_key}&languageCode=ko-KR"
    response = requests.get(url)
    if response.status_code == 200:
        voices = response.json().get("voices", [])
        for voice in voices:
            print(f"Name: {voice['name']}, Gender: {voice['ssmlGender']}, Rate: {voice.get('naturalSampleRateHertz')}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    list_voices()
