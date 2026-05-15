from PIL import Image
import os
import math

# =========================
# 1. image_path 에 원하는 이미지 상대경로 복사 후 입력
# =========================
image_path = r"mattermost_big_size_image_upload_auto/image/image_name"  # 이미지 경로 복사 후 입력하기 역슬래시는 슬래시로 변경
base_name = input("파일 기본 이름 입력: ").strip()
tile_size = 32  # 메타모스트 최적화 사이즈 16 32 64 128 중 선택 크기가 클수록 메타모스트에선 작게 나타남
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

img = Image.open(image_path)
orig_w, orig_h = img.size

# 나누었을 때 남는 공간을 포함할 수 있도록 올림 처리하여 전체 크기 계산
cols = math.ceil(orig_w / tile_size)
rows = math.ceil(orig_h / tile_size)
new_w, new_h = cols * tile_size, rows * tile_size

# =========================
# 2. 프레임 처리
# =========================
pieces_frames = {(r, c): [] for r in range(rows) for c in range(cols)}
durations = []

for f in range(img.n_frames):
    img.seek(f)
    durations.append(img.info.get("duration", 100))
    
    frame_rgba = img.convert("RGBA")
    
    full_canvas = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    

    full_canvas.paste(frame_rgba, (0, 0))
    
    for r in range(rows):
        for c in range(cols):
            left, upper = c * tile_size, r * tile_size
            cropped = full_canvas.crop((left, upper, left + tile_size, upper + tile_size))
            
            pieces_frames[(r, c)].append(cropped.copy())

# =========================
# 3. 저장
# =========================
for r in range(rows):
    for c in range(cols):
        row_char = chr(65 + r)
        col_num = c + 1
        save_path = os.path.join(output_folder, f"{base_name}_{row_char}{col_num}.gif")
        
        frames = pieces_frames[(r, c)]
        
        frames[0].save(
            save_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,
            disposal=2,
            optimize=False # 최적화 제거
        )
        print(f"✅ 저장 완료: {save_path} ({tile_size}x{tile_size})")

print("\n✨ 메타모스트용 최적화 분할 완료!")