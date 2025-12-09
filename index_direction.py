import math
import pyautogui

def finger_direction_left_right(lm, thresh=0.03):
    """
    根據 食指 TIP(8) 與 MCP(5) 的 x 差判斷左右方向。
    dx > 0 → 往右指， dx < 0 → 往左指
    thresh：越大越不敏感
    """
    base = lm[5]  # 食指 MCP (根部)
    tip  = lm[8]  # 食指 TIP (尖端)

    dx = tip.x - base.x  # 正:往右; 負:往左
    # print("dx 8-5:", dx)
    # print("thresh:", thresh)
    if dx > thresh:
        return "RIGHT"
    elif dx < -thresh:
        return "LEFT"
    else:
        return None

def handle_index_direction(lm, pose):
    if pose != "POINT":
        return  # 不是食指手勢就不偵測

    direction = finger_direction_left_right(lm)

    if direction == "RIGHT":
        pyautogui.press("right")
        print("➡▶ 快進 5 秒")

    elif direction == "LEFT":
        pyautogui.press("left")
        print("⬅◀ 後退 5 秒")
