import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Optimization
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0 
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Variables
prev_x, prev_y = 0, 0
frame_reduction = 80
smoothening = 3

# Gesture States
left_clicked = False
right_clicked = False
double_clicked = False

# Swipe Stability
prev_hand_center_x = 0
swipe_cooldown = 0
swipe_threshold = 0.15 # Sensitivity of the fast move

while True:
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1)
    h, w, c = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        handLms = result.multi_hand_landmarks[0]
        lm = handLms.landmark

        # 1. CURSOR (Thumb Tip - Landmark 4)
        tx, ty = lm[4].x * w, lm[4].y * h
        x_mapped = np.interp(tx, (frame_reduction, w - frame_reduction), (0, screen_w))
        y_mapped = np.interp(ty, (frame_reduction, h - frame_reduction), (0, screen_h))

        curr_x = prev_x + (x_mapped - prev_x) / smoothening
        curr_y = prev_y + (y_mapped - prev_y) / smoothening
        pyautogui.moveTo(np.clip(curr_x, 0, screen_w-1), np.clip(curr_y, 0, screen_h-1))
        prev_x, prev_y = curr_x, curr_y

        # 2. FINGER STATES (Tips: 8,12,16,20 | PIP Joints: 6,10,14,18)
        index_down = lm[8].y > lm[6].y
        middle_down = lm[12].y > lm[10].y
        ring_down = lm[16].y > lm[14].y
        pinky_down = lm[20].y > lm[18].y

        # 3. DOUBLE CLICK (All 4 fingers down)
        if index_down and middle_down and ring_down and pinky_down:
            if not double_clicked:
                pyautogui.doubleClick()
                print("💥 Double Click (4-Fingers)")
                double_clicked = True
        else:
            # Reset only when fingers are lifted
            if not (index_down or middle_down or ring_down or pinky_down):
                double_clicked = False

        # 4. SINGLE CLICKS (Only if not double-clicking)
        if not double_clicked:
            if index_down and not middle_down:
                if not left_clicked:
                    pyautogui.click()
                    left_clicked = True
            else: left_clicked = False

            if middle_down and not index_down:
                if not right_clicked:
                    pyautogui.rightClick()
                    right_clicked = True
            else: right_clicked = False

        # 5. FAST SWIPE (Media/Photo Control)
        # Using Wrist (0) and Middle Finger MCP (9) average for center stability
        current_hand_center_x = (lm[0].x + lm[9].x) / 2
        
        if prev_hand_center_x != 0:
            delta_x = current_hand_center_x - prev_hand_center_x
            
            if abs(delta_x) > swipe_threshold and (time.time() - swipe_cooldown > 0.8):
                if delta_x > 0: # Fast move Left to Right
                    pyautogui.press("nexttrack") # Audio/Video
                    pyautogui.press("right")     # Photos
                    print("▶▶ NEXT")
                    swipe_cooldown = time.time()
                elif delta_x < -swipe_threshold: # Fast move Right to Left
                    pyautogui.press("prevtrack") # Audio/Video
                    pyautogui.press("left")      # Photos
                    print("◀◀ PREVIOUS")
                    swipe_cooldown = time.time()
        
        prev_hand_center_x = current_hand_center_x

        mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Advanced Media Mouse", img)
    if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()