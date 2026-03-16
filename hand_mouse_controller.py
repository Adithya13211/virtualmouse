"""
hand_mouse_controller.py
IMPROVED VERSION:
- Thumb controls cursor movement
- Thumb + Index pinch = LEFT click
- Thumb + Pinky pinch = RIGHT click
- Faster movement
- Easier access to screen corners (ROI mapping)
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui
from math import hypot

# ---------- OPTIONAL WIN32 (SAFE) ----------
USE_WIN32 = False
try:
    import win32api
    USE_WIN32 = True
except:
    USE_WIN32 = False

# ---------- CONFIG ----------
CAM_WIDTH, CAM_HEIGHT = 640, 480
SMOOTHING = 0.2          # lower = faster cursor
LEFT_CLICK_THRESHOLD = 35
RIGHT_CLICK_THRESHOLD = 35
CLICK_DELAY = 0.5

# Active interaction box (ROI)
ROI_X1, ROI_Y1 = 80, 60
ROI_X2, ROI_Y2 = 560, 420
# -----------------------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

prev_x, prev_y = 0, 0
last_left_click = 0
last_right_click = 0

def map_to_screen(x, y):
    sx = np.interp(x, (ROI_X1, ROI_X2), (0, screen_w))
    sy = np.interp(y, (ROI_Y1, ROI_Y2), (0, screen_h))
    return int(sx), int(sy)

print("✅ Virtual Mouse Started | Press 'q' to exit")

while True:
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Draw ROI box
    cv2.rectangle(frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (255, 255, 0), 2)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark

        # Landmarks
        # Thumb tip
        tx, ty = int(lm[4].x * w), int(lm[4].y * h)
        # Index tip
        ix, iy = int(lm[8].x * w), int(lm[8].y * h)
        # Pinky tip
        px, py = int(lm[20].x * w), int(lm[20].y * h)

        # Draw points
        cv2.circle(frame, (tx, ty), 8, (255, 0, 255), cv2.FILLED)   # Thumb
        cv2.circle(frame, (ix, iy), 8, (0, 255, 0), cv2.FILLED)     # Index
        cv2.circle(frame, (px, py), 8, (0, 255, 255), cv2.FILLED)   # Pinky

        # Cursor movement (Thumb only)
        if ROI_X1 < tx < ROI_X2 and ROI_Y1 < ty < ROI_Y2:
            sx, sy = map_to_screen(tx, ty)

            smooth_x = prev_x + (sx - prev_x) * (1 - SMOOTHING)
            smooth_y = prev_y + (sy - prev_y) * (1 - SMOOTHING)
            prev_x, prev_y = smooth_x, smooth_y

            if USE_WIN32:
                win32api.SetCursorPos((int(smooth_x), int(smooth_y)))
            else:
                pyautogui.moveTo(int(smooth_x), int(smooth_y), duration=0)

        now = time.time()

        # LEFT CLICK (Thumb + Index)
        left_dist = hypot(ix - tx, iy - ty)
        if left_dist < LEFT_CLICK_THRESHOLD and (now - last_left_click) > CLICK_DELAY:
            pyautogui.click(button='left')
            last_left_click = now
            cv2.putText(frame, "LEFT CLICK", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # RIGHT CLICK (Thumb + Pinky)
        right_dist = hypot(px - tx, py - ty)
        if right_dist < RIGHT_CLICK_THRESHOLD and (now - last_right_click) > CLICK_DELAY:
            pyautogui.click(button='right')
            last_right_click = now
            cv2.putText(frame, "RIGHT CLICK", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.putText(
        frame,
        "Thumb=Move | Thumb+Index=Left Click | Thumb+Pinky=Right Click | q=Quit",
        (10, CAM_HEIGHT - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1
    )

    cv2.imshow("Hand Mouse Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
