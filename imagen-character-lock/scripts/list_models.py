import os
from google import genai
from dotenv import load_dotenv

# Find .env file
def find_env_file():
    current = os.getcwd()
    for _ in range(5):
        env_path = os.path.join(current, ".env")
        if os.path.exists(env_path):
            return env_path
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None

env_path = find_env_file()
if env_path:
    load_dotenv(env_path)

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("GOOGLE_API_KEY not found")
    exit(1)

client = genai.Client(api_key=api_key)

try:
    print("Available GenAI Models:")
    for model in client.models.list():
        print(f"  - {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
