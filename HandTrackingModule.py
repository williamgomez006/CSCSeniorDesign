import cv2
import mediapipe as mp
import time

class handDetector():

    def __init__(self, mode=False, maxHands=2, detectionCon=50, trackCon=50):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands# protocol to start using mediapipe
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)# call in function on mediapipe to read hands
        self.mpDraw = mp.solutions.drawing_utils# get the drawing utilities from mediapipe


    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#convert BGR image to RGB to be able to use mediapipe
        self.results = self.hands.process(imgRGB)#process image

        #print(results.multi_hand_landmarks) #testing for hand landmarks

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:# loop on all the landmarks
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)  # draw hand landmarks connections

        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                #print(id,lm)
                #find the landmarks location using pixel count
                h, w, c = img.shape
                cx, cy, = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                #write the landmark id
                    cv2.putText(img, str(int(id)), (cx,cy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255, 255, 255))
        return lmList






def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    # read webcam
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255, 3))

        cv2.imshow("Video", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
