# fist_speed_control.py
import time
import pyautogui

# === 內部狀態，用來記錄握拳持續時間與倍速模式 ===
_fist_start = None
_speed_mode = False

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


def handle_fist_speed(lm, hold_time=1.6):
    """
    長時間握拳 → 開啟倍速
    放開拳頭 → 恢復正常速度

    hold_time: 握拳多久後觸發倍速 (秒)
    """
    global _fist_start, _speed_mode

    now = time.time()

    # ===== 握拳狀態中 =====
    if is_fist(lm):
        if _fist_start is None:
            _fist_start = now  # 記錄開始握拳時間
        elif not _speed_mode and (now - _fist_start) > hold_time:
            pyautogui.press(">")
            print("⚡ 倍速 ON")
            _speed_mode = True
    else:
        # ===== 鬆開拳頭（離開握拳） =====
        if _speed_mode and _fist_start is not None:
            pyautogui.press("<")
            print("🐢 倍速 OFF")
            _speed_mode = False
        _fist_start = None
