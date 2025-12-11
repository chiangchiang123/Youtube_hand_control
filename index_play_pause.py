import math
import time
import pyautogui

def is_index_toward_camera(lm, xy_thresh=0.01):
    """
    食指是否「指向鏡頭」：
    1. TIP(8) 和 DIP(7) 在平面距離很近 → 手指不是橫著
    2. TIP 比 DIP 更靠近鏡頭 (z越小) → 表示往前指

    備註：threshold 需依鏡頭距離與手大小調整
    """

    tip = lm[8]  # 食指尖端
    dip = lm[7]  # 第二關節 (下個點位)

    # 計算投影平面的距離（x,y）
    dist_xy = math.hypot(tip.x - dip.x, tip.y - dip.y)

    # print("dist_xy 8-7:", dist_xy)
    return dist_xy < xy_thresh 

def handle_index_play_pause(lm):
    """
    只要食指指向鏡頭，就觸發 PLAY/PAUSE。（不依賴 classify_static_pose）
    """
    if is_index_toward_camera(lm):
        pyautogui.press("k")
        print("⏯ 播放/暫停")