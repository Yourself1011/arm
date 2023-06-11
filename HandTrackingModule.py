import cv2
import mediapipe as mp
import time
from math import asin, degrees, sqrt
from Arduino import write


class handDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.points = {}
        self.thumbLength = 0
        self.indexLength = 0
        self.middleLength = 0
        self.angleRange = 180

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS
                    )
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = {}
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList[id] = {"x": cx, "y": cy}
                if draw:
                    if id in [0, 2, 4, 5, 8, 9, 12]:
                        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    else:
                        cv2.circle(img, (cx, cy), 5, (128, 0, 128), cv2.FILLED)

        self.points = lmList
        return lmList

    def findAngles(self, img):
        if not (
            2 in self.points
            and 4 in self.points
            and 5 in self.points
            and 8 in self.points
            and 9 in self.points
            and 12 in self.points
        ):
            return
        self.thumbLength = max(
            self.thumbLength,
            sqrt(
                (self.points[4]["x"] - self.points[2]["x"]) ** 2
                + (self.points[4]["y"] - self.points[2]["y"]) ** 2
            ),
        )
        self.indexLength = max(
            self.indexLength,
            sqrt(
                (self.points[8]["x"] - self.points[5]["x"]) ** 2
                + (self.points[8]["y"] - self.points[5]["y"]) ** 2
            ),
        )
        self.middleLength = max(
            self.middleLength,
            sqrt(
                (self.points[12]["x"] - self.points[9]["x"]) ** 2
                + (self.points[12]["y"] - self.points[9]["y"]) ** 2
            ),
        )

        thumbAngle = degrees(
            asin((self.points[4]["y"] - self.points[2]["y"]) / self.thumbLength)
        )
        indexAngle = degrees(
            asin((self.points[5]["y"] - self.points[8]["y"]) / self.indexLength)
        )
        middleAngle = degrees(
            asin((self.points[9]["y"] - self.points[12]["y"]) / self.middleLength)
        )

        h, w, c = img.shape

        return (
            thumbAngle,
            indexAngle,
            middleAngle,
            self.points[0]["x"] / w * self.angleRange,
        )


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        angles = detector.findAngles(img)
        if angles:
            # thread = Thread(
            #     target=write,
            #     args=(",".join([str(angle) for angle in angles]),),
            # )
            # thread.start()
            write(",".join([str(round(angle, 1)) for angle in angles]))

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(
            img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
        )

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
