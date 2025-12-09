import math
import time
import pyautogui

_base_dist = None
_last_action = 0

def is_fist(lm, thresh=0.1):
    """
    判斷是否為握拳（不依靠 classify pose）
    方法：判斷 4 根手指的 TIP 與 MCP 距離很近 → 手指彎下去
    （不檢查拇指，避免受角度干擾）

    thresh 越小越嚴格，可調整（建議 0.05~0.09）
    """
    # 手指 Tip(8,12,16,20) 和 MCP(5,9,13,17) 的距離
    finger_pairs = [(8,5), (12,9), (16,13), (20,17)]

    for tip, mcp in finger_pairs:
        dx = abs(lm[tip].x - lm[mcp].x)
        dy = abs(lm[tip].y - lm[mcp].y)
        dist = (dx**2 + dy**2) ** 0.5
        if dist > thresh:
            return False  # 只要有一根手指距離太遠就不是握拳

    return True


def thumb_index_distance(lm):
    t = lm[4]  # thumb tip
    i = lm[8]  # index tip
    return math.hypot(t.x - i.x, t.y - i.y)

def handle_zoom(lm, pose, cooldown=0.8, up_ratio=1.35, down_ratio=0.75):
    """
    根據大拇指 + 食指距離判斷放大 / 縮小。

    ⚠ 若目前是 POINT 手勢（你用來控制快進/後退），
       這裡就完全不做事，避免跟 handle_index_direction 打架。
    """

    global _base_dist, _last_action

    # 保留 POINT 給左右快進/後退，不在 POINT 手勢時做 zoom
    if pose == "POINT" or is_fist(lm):
        return

    dist = thumb_index_distance(lm)
    if dist is None:
        return

    if _base_dist is None:
        _base_dist = dist
        return

    ratio = dist / _base_dist
    now = time.time()

    # print(f"[ZOOM] dist={dist:.4f}, ratio={ratio:.2f}")

    if ratio > up_ratio and (now - _last_action > cooldown):
        pyautogui.press("f")
        print("ZOOM IN")
        _last_action = now

    elif ratio < down_ratio and (now - _last_action > cooldown):
        pyautogui.press("f")
        print("ZOOM OUT")
        _last_action = now