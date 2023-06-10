import cv2
import mediapipe as mp
import time
from math import atan, degrees

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

indexLength = 0
middleLength = 0
thumbLength = 0

points = {}

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = {"x": cx, "y": cy}
                # print(id, cx, cy)
                cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            indexLength = max(indexLength, abs(points[8]["x"] - points[5]["x"]))
            middleLength = max(middleLength, abs(points[12]["x"] - points[9]["x"]))
            thumbLength = max(thumbLength, abs(points[4]["x"] - points[2]["x"]))

            indexAngle = degrees(atan((points[5]["y"] - points[8]["y"]) / indexLength))
            middleAngle = degrees(
                atan((points[9]["y"] - points[12]["y"]) / middleLength)
            )
            thumbAngle = degrees(atan((points[4]["y"] - points[2]["y"]) / thumbLength))
            print(thumbAngle, indexAngle, middleAngle)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    )

    cv2.imshow("Image", img)
    cv2.waitKey(1)
