import cv2
import numpy as np
import easyocr
import hashlib
import os
import json
from screen import screenshot
import config

# Ініціалізація EasyOCR (лише для цифр)
reader = easyocr.Reader(['en'], gpu=False)

# Файл, де бот зберігатиме зліпки плиток, щоб не розпізнавати їх знову після перезапуску
CACHE_FILE = "tile_cache.json"
tile_cache = {}

if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r") as f:
            tile_cache = json.load(f)
    except:
        tile_cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(tile_cache, f)

def get_board():
    img = screenshot()
    if img is None:
        return None
        
    cfg = config.load()
    b = cfg["board"]
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    return img[y:y+h, x:x+w]

def get_tile_value(tile_img):
    """
    Розпізнає плитку миттєво через кеш, або викликає EasyOCR, якщо плитка нова
    """
    # 1. Швидка перевірка на порожню клітинку за яскравістю
    mean_color = cv2.mean(tile_img)[:3]
    if sum(mean_color) < 160:
        return 0

    # 2. Переводимо в сірий колір та зменшуємо для створення стабільного хешу
    gray = cv2.cvtColor(tile_img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (32, 32), interpolation=cv2.INTER_AREA)
    
    # Створюємо унікальний текстовий "відбиток" картинки
    tile_hash = hashlib.md5(resized.tobytes()).hexdigest()

    # 3. Якщо ми вже бачили цю картинку раніше — миттєво повертаємо цифру з пам'яті
    if tile_hash in tile_cache:
        return tile_cache[tile_hash]

    # 4. Якщо картинка нова — один раз викликаємо EasyOCR
    padded = cv2.copyMakeBorder(gray, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=255)
    results = reader.readtext(padded, allowlist='0123456789')
    
    val = 0
    if results:
        text = results[0][1].strip()
        try:
            parsed_val = int(text)
            if parsed_val in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
                val = parsed_val
        except ValueError:
            pass

    # Запам'ятовуємо цю плитку в кеш, щоб більше ніколи її не розпізнавати через OCR
    tile_cache[tile_hash] = val
    save_cache()
    
    print(f"   [Пам'ять] Запам'ятав нову плитку як: {val}")
    return val

def get_board_matrix():
    board = get_board()
    if board is None:
        return None
        
    h, w = board.shape[:2]
    tile_h, tile_w = h // 4, w // 4
    matrix = []
    
    for row in range(4):
        matrix_row = []
        for col in range(4):
            tile = board[row*tile_h:(row+1)*tile_h, col*tile_w:(col+1)*tile_w]
            
            # Звужуємо межі, щоб не брати рамку поля
            th, tw = tile.shape[:2]
            border_h, border_w = int(th * 0.05), int(tw * 0.05)
            tile_cropped = tile[border_h:th-border_h, border_w:tw-border_w]
            
            val = get_tile_value(tile_cropped)
            matrix_row.append(val)
        matrix.append(matrix_row)
        
    return matrix

def test_matrix():
    print("[Кеш-Аналіз] Зчитую поле...")
    import time
    t0 = time.time()
    matrix = get_board_matrix()
    print(f"[Кеш-Аналіз] Поле оброблено за {time.time() - t0:.3f} сек.")
    if matrix is None:
        return
    for row in matrix:
        print(row)

if __name__ == "__main__":
    test_matrix()