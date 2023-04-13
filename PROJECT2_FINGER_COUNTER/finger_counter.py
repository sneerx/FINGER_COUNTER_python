import cv2
import HandTrackModule as htm
import time
import os

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


folderPath = "images"
myList = os.listdir(folderPath)
overlayList = list()

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)


pTime = 0
detector = htm.handDetector()

tipIds = [4, 8, 12, 16, 20]



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)
    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)

        else:

            fingers.append(0)
        # 4 Fingers
        for id in range(1,5):

            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)

            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1] # 6. jpg dosyasını göstermesinin sebebi totalFingers = 0 oldugunda [-1]'e dönüyor ve pythonda liste tersten okunuyor bize 6. jpg dosyasını gösteriyor.


    #img[0:200, 0:200] = overlayList[0] # resimleri 200x200 resize ettim.
    # SKELETON
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 0, 0), 3)
    img = cv2.imshow("Image", img)
    cv2.waitKey(1)
