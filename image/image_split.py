from PIL import Image
import os
import math

# =========================
# 1. image_path 에 원하는 이미지 상대경로 복사 후 입력
# =========================
image_path = r"image/mari_sanabi.gif"  # 이미지 경로 복사 후 입력하기 역슬래시는 슬래시로 변경
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

gif_canvas = Image.new("RGBA", img.size, (0, 0, 0, 0))

for f in range(getattr(img, "n_frames", 1)):
    img.seek(f)

    duration = img.info.get("duration", 100)
    durations.append(duration)

    frame_rgba = img.convert("RGBA")

    # 현재 프레임 합성
    gif_canvas.paste(frame_rgba, (0, 0), frame_rgba)

    # 이 시점의 완성 프레임 복사
    full_frame = gif_canvas.copy()

    # 분할용 캔버스
    full_canvas = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    full_canvas.paste(full_frame, (0, 0))

    for r in range(rows):
        for c in range(cols):
            left = c * tile_size
            upper = r * tile_size
            cropped = full_canvas.crop((left, upper, left + tile_size, upper + tile_size))
            pieces_frames[(r, c)].append(cropped.copy())

    # disposal_method == 2면 다음 프레임 전에 현재 프레임 영역을 투명하게 비움
    disposal = getattr(img, "disposal_method", 0)

    if disposal == 2:
        bbox = img.getbbox()
        if bbox:
            clear_area = Image.new("RGBA", (bbox[2] - bbox[0], bbox[3] - bbox[1]), (0, 0, 0, 0))
            gif_canvas.paste(clear_area, bbox)

# =========================
# 3. 저장
# =========================
for r in range(rows):
    for c in range(cols):
        row_char = chr(97 + r)
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