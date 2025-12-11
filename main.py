# main.py
import cv2
import config
from hand_tracking import HandDetector
from gesture_action import GestureController

def main():
    # 初始化
    cap = cv2.VideoCapture(0)
    cap.set(3, config.CAM_WIDTH)
    cap.set(4, config.CAM_HEIGHT)
    
    detector = HandDetector()
    controller = GestureController()
    
    print("系統啟動... 按 'q' 結束")

    while True:
        success, img = cap.read()
        if not success: break
        
        # 翻轉影像 (鏡像)
        img = cv2.flip(img, 1)
        
        # 1. 偵測手部
        img, results = detector.find_hands(img)
        
        # 2. 處理每一隻手
        if results.multi_hand_landmarks:
            for i in range(len(results.multi_hand_landmarks)):
                # 獲取該手部的座標與標籤
                lm_list, label = detector.get_hand_info(img, i)
                
                # 3. 判斷手勢並執行
                feedback_text = controller.process_gesture(i, label, lm_list, img)
                
                # 4. 如果有觸發動作，顯示在畫面上
                if feedback_text:
                    cv2.putText(img, feedback_text, (50, 50 + i*50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
        cv2.imshow("Hand Gesture Controller", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()