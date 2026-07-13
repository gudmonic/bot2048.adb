import time
import numpy as np
import subprocess

# Імпортуємо наш новий Expectimax ШІ замість старого Solver
from solver import get_best_move 
from vision import get_board_matrix
import config

def print_board(board):
    print("----------------")
    for row in board:
        print(row)
    print("----------------")

def execute_adb_swipe(direction, cfg):
    """
    Робить чіткий фізичний свайп по центру екрана 1440х3120
    """
    adb_path = "C:\\Users\\b0ber\\Downloads\\scrcpy-win64-v4.0\\scrcpy-win64-v4.0\\adb.exe"
    cx, cy = 720, 1560
    
    # Збільшено тривалість до 150мс для 100% розпізнавання пристроєм
    if direction == "UP":
        cmd = [adb_path, "shell", "input", "swipe", str(cx), str(cy + 400), str(cx), str(cy - 400), "150"]
    elif direction == "DOWN":
        cmd = [adb_path, "shell", "input", "swipe", str(cx), str(cy - 400), str(cx), str(cy + 400), "150"]
    elif direction == "LEFT":
        cmd = [adb_path, "shell", "input", "swipe", str(cx + 400), str(cy), str(cx - 400), str(cy), "150"]
    elif direction == "RIGHT":
        cmd = [adb_path, "shell", "input", "swipe", str(cx - 400), str(cy), str(cx + 400), str(cy), "150"]
        
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    cfg = config.load()
    depth = cfg.get("depth", 4)  # Оптимально для i3-7020U: depth 4

    print("==============================================")
    print("  2048 TURBO-BOT STARTED (Expectimax Edition) ")
    print("==============================================")
    print("Open monobank 2048 in scrcpy")
    print(f"Current proccessing depth: {depth}")
    print("Starting in 5 seconds...")
    time.sleep(5)

    while True:
        try:
            # 1. Зчитуємо матрицю через EasyOCR (із пам'яті через виправлений screen.py)
            raw_board = get_board_matrix()

            if raw_board is None:
                print("Failed to read screen")
                time.sleep(0.5)
                continue

            print_board(raw_board)

            # Перевіряємо, чи поле взагалі знайдене
            # Оскільки raw_board — це звичайний список списків, рахуємо нулі базовим python
            if sum(row.count(0) for row in raw_board) == 16:
                print("Board not detected")
                time.sleep(1)
                continue

            # 2. Вираховуємо найкращий хід за допомогою нового алгоритму
            # Очікує на вихід "UP", "RIGHT", "DOWN" або "LEFT"
            direction = get_best_move(raw_board, depth=depth)

            print("Move:", direction)

            # 3. Робимо фізичний свайп на пристрої
            execute_adb_swipe(direction, cfg)

            # Пауза між ходами (у конфігу ми поставили 0.02)
            time.sleep(cfg.get("move_delay", 0.02))

        except KeyboardInterrupt:
            print("Stopped by user")
            break

        except Exception as e:
            print("Error:", e)
            time.sleep(2)

if __name__ == "__main__":
    main()