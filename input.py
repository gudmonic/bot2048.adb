import subprocess
import time
import config


def adb_command(args):
    cfg = config.load()

    serial = cfg.get("adb_serial", "")

    cmd = ["C:\\Users\\b0ber\\Downloads\\scrcpy-win64-v4.0\\scrcpy-win64-v4.0\\adb.exe"]

    if serial:
        cmd += ["-s", serial]

    cmd += args

    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def swipe(direction):
    """
    Робить свайп на екрані телефона.
    Координати приблизно для вертикального телефона.
    Якщо треба — змінюються у config.py
    """

    cfg = config.load()

    w = cfg.get("phone_width", 1080)
    h = cfg.get("phone_height", 2400)

    cx = w // 2
    cy = h // 2

    distance = 300

    if direction == "LEFT":
        x1, y1 = cx + distance, cy
        x2, y2 = cx - distance, cy

    elif direction == "RIGHT":
        x1, y1 = cx - distance, cy
        x2, y2 = cx + distance, cy

    elif direction == "UP":
        x1, y1 = cx, cy + distance
        x2, y2 = cx, cy - distance

    elif direction == "DOWN":
        x1, y1 = cx, cy - distance
        x2, y2 = cx, cy + distance

    else:
        return


    adb_command([
        "shell",
        "input",
        "swipe",
        str(x1),
        str(y1),
        str(x2),
        str(y2),
        "100"
    ])

    time.sleep(
        cfg.get("move_delay", 0.05)
    )