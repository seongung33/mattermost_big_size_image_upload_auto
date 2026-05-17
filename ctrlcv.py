import string
import pyperclip

# 입력
prefix = input("접두어 입력 (예: mari): ")
end_alpha = input("마지막 알파벳 입력 (예: o): ").lower()
end_num = int(input("마지막 숫자 입력 (예: 16): "))

result = []

# a ~ 입력한 알파벳까지
for alphabet in string.ascii_lowercase:
    if alphabet > end_alpha:
        break

    line = ""

    # 1 ~ 입력한 숫자까지
    for num in range(1, end_num + 1):
        line += f":{prefix}_{alphabet}{num}:"

    result.append(line)

# 최종 문자열
final_text = "\n".join(result)

# 클립보드 복사
pyperclip.copy(final_text)

print("복사 완료!")
print()
print(final_text)