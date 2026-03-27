from PIL import Image
import os

IMAGE_PATH = r"C:\Users\ryu\.gemini\antigravity\brain\0fbf1fbe-88ba-4bf7-95dc-d73c0de2fa68\intro_hook_korean_kim_v2_1774553308179.png"
OUTPUT_DIR = r"d:\Vibe_Coding\chatsapiens\video_creator\imagen-character-lock\guard_story_final\FINAL_VREW_PACK"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "intro_16_9.png")

def crop_to_16_9():
    if not os.path.exists(IMAGE_PATH):
        print("Error: Image not found.")
        return

    img = Image.open(IMAGE_PATH)
    w, h = img.size
    
    # Target 16:9
    target_ratio = 16 / 9
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        # Too wide, crop sides
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, h))
    else:
        # Too tall, crop top/bottom
        new_h = int(w / target_ratio)
        offset = (h - new_h) // 2
        img = img.crop((0, offset, w, offset + new_h))
    
    img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
    img.save(OUTPUT_PATH)
    print(f"Success: Cropped image saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    crop_to_16_9()
