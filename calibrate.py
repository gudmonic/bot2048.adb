import cv2
import json
from screen import screenshot

print("1. Роблю скріншот...")
img = screenshot()

if img is None:
    print("Помилка: Скріншот порожній!")
    exit()

h_orig, w_orig = img.shape[:2]
print(f"2. Успішно зчитано оригінал: {w_orig}x{h_orig}")

# Розраховуємо коефіцієнт стиснення (робимо ширину 400 пікселів для монітора)
target_w = 400
scale = target_w / w_orig
target_h = int(h_orig * scale)

# Фізично зменшуємо копію зображення для виділення мишкою
img_small = cv2.resize(img, (target_w, target_h))

win_name = "ВИДІЛИ ПОЛЕ 4х4 МИШКОЮ ТА НАТИСНИ ENTER"
cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)

# Виділяємо область на МЕНШІЙ картинці (вона точно влазитиме в екран)
roi = cv2.selectROI(win_name, img_small, False, False)
cv2.destroyAllWindows()

x_small, y_small, w_small, h_small = roi

if w_small == 0 or h_small == 0:
    print("Калібрування скасовано: область не вибрано.")
    exit()

# Перераховуємо координати назад у великий (оригінальний) розмір
x_orig = int(x_small / scale)
y_orig = int(y_small / scale)
w_orig_roi = int(w_small / scale)
h_orig_roi = int(h_small / scale)

# Формуємо конфіг для бота
cfg = {
    "board": {
        "x": x_orig,
        "y": y_orig,
        "w": w_orig_roi,
        "h": h_orig_roi
    },
    "depth": 5,
    "move_delay": 0.15,
    "phone_width": w_orig,
    "phone_height": h_orig,
    "adb_serial": ""
}

# Зберігаємо
with open("config.json", "w") as f:
    json.dump(cfg, f, indent=4)

print("\n--- НАЛАШТУВАННЯ ЗБЕРЕЖЕНО! ---")
print(json.dumps(cfg, indent=4))