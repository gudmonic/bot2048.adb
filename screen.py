import cv2
import numpy as np
import subprocess
import os

def screenshot():
    """
    Оптимізований знімок екрану через ADB pipe з виправленням ламаних байтів Windows (\r\n -> \n)
    """
    try:
        adb_path = "C:\\Users\\b0ber\\Downloads\\scrcpy-win64-v4.0\\scrcpy-win64-v4.0\\adb.exe"
        cmd = [adb_path, 'shell', 'screencap', '-p']
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, startupinfo=startupinfo)
        img_bytes, _ = proc.communicate()

        if not img_bytes:
            return None

        # МАГІЯ ДЛЯ WINDOWS: виправляємо заміну символів нового рядка, яку робить консоль
        if os.name == 'nt':
            img_bytes = img_bytes.replace(b'\r\n', b'\n')

        # Декодуємо виправлені байти картинки в масив OpenCV
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"[Помилка скріншоту]: {e}")
        return None

if __name__ == "__main__":
    import time
    print("Тест швидкості прямого ADB скріншотера...")
    t0 = time.time()
    img = screenshot()
    if img is not None:
        print(f"Успішно! Знімок отримано за {time.time() - t0:.3f} сек. Розмір: {img.shape}")
    else:
        print("Не вдалося отримати знімок через баг байтів.")