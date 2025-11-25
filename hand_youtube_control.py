import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
prev_gesture = None
cooldown = 1.0
last_time = time.time()

def finger_up(lm, tip, pip):
    return lm[tip].y < lm[pip].y

def classify_gesture(lm):
    up = [
        finger_up(lm, 4, 3),   # thumb
        finger_up(lm, 8, 6),   # index
        finger_up(lm, 12,10),  # middle
        finger_up(lm, 16,14),  # ring
        finger_up(lm, 20,18)   # pinky
    ]
    up_count = sum(up)

    # gesture definitions
    if up_count == 0:
        return "PAUSE"       # ✊
    if up_count == 5:
        return "PLAY"        # 🖐
    if up[1] and not any(up[i] for i in [0,2,3,4]):
        return "FORWARD"     # 👉
    if up[0] and not any(up[i] for i in [1,2,3,4]):
        return "BACK"        # 👈
    if up[1] and up[2] and not up[0]:
        return "SPEEDUP"     # ✌
    if up[0] and up[1] and not up[2]:
        return "NORMAL"      # 🤟
    return None

def send_key(action):
    keymap = {
        "PLAY": "k",       # 播放/暫停
        "PAUSE": "k",
        "FORWARD": "l",    # 快轉 10 秒
        "BACK": "j",       # 倒退 10 秒
        "SPEEDUP": ">",    # 加速
        "NORMAL": "<"      # 降速
    }
    key = keymap.get(action)
    if key:
        print(f"👉 {action} → 按下 {key}")
        pyautogui.press(key)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark
            gesture = classify_gesture(lm)

            # gesture throttle
            if gesture and (time.time() - last_time > cooldown):
                if gesture != prev_gesture:
                    send_key(gesture)
                    prev_gesture = gesture
                    last_time = time.time()

    cv2.imshow('Gesture Control', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
