

import cv2
import mediapipe as mp
import time
import math

import numpy as np

#set camera height and width

wCam, hCam = 640, 480


#add pycaw to the program

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(0.0, None)

minVol = volRange[0]
maxVol = volRange[1]


#capture video from webcam
cap = cv2.VideoCapture(0)
cap.set(3, wCam) # set camera width to wCam
cap.set(4, hCam) # set camera height to hCam



#initialize Mediapipe
mpHands = mp.solutions.hands# protocol to start using mediapipe
hands = mpHands.Hands()# call in function on mediapipe to read hands
mpDraw = mp.solutions.drawing_utils# get the drawing utilities from mediapipe

#variable for time and FPS calculations
pTime = 0
cTime = 0

#initializing coordinates for thumb and index

x1, x2, y1, y2 = 0, 0, 0, 0


#read webcam
while True:
    success, img = cap.read() #while I am able to read webcam continue to loop

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#convert BGR image to RGB to be able to use mediapipe
    results = hands.process(imgRGB)#process image



    #print(results.multi_hand_landmarks) #testing for hand landmarks

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:# loop on all the landmarks

            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                #find the landmarks location using pixel count
                h, w, c = img.shape
                cx, cy, = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                #write the landmark id 
                cv2.putText(img, str(int(id)), (cx,cy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255, 255, 255))

                #drawing a line between two landmarks

                if id == 4:
                    cv2.circle(img,  (cx,cy), 15, (255,0,0), cv2.FILLED)
                    x1, y1 = cx, cy

                if id == 8:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                    x2, y2 = cx, cy

                #middle point of the line

                mx, my = (x1+x2)//2, (y1+y2)//2


                #draw a line and a center circle between the index and the thumb
                cv2.line(img, (x1, y1), (x2, y2), (255,0,0),3)
                cv2.circle(img, (mx,my), 15, (255,0,0), cv2.FILLED)

                #obtain the lenght of the line between the thumb and the index
                length = math.hypot(x2-x1, y2-y1)
                #print(length)

                if length<50:
                    cv2.circle(img, (mx,my), 15, (0,255,255),cv2.FILLED)

                #fingers distance ranges from 20 to 300 and volume ranges from -65 to 0

                vol = np.interp(length, [50, 300],[minVol, maxVol])
                print(int(length), vol)
                volume.SetMasterVolumeLevel(vol, None)



            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)#draw hand landmarks




    #display FPS
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255,3))

    cv2.imshow("Video", img)
    cv2.waitKey(1)