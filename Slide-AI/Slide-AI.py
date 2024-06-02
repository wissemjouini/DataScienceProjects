q# -*- coding: utf-8 -*-
"""
Created on Sun May  5 20:01:56 2024

@author: Wissem
"""

from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "slides"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=int(0.8), maxHands=1)

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = 200, 300  # width and height of small image

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

while True:
    # Get image frame
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Resize imgCurrent to match the display size
    imgCurrent = cv2.resize(imgCurrent, (width, height))

    # Find the hand and its landmarks
    img = detectorHand.findHands(img)  # with draw
    lmList, _ = detectorHand.findPosition(img, draw=False)

    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if lmList and not buttonPressed:  # If hand is detected
        cx, cy = lmList[8][0], lmList[8][1]
        fingers = detectorHand.fingersUp()  # List of which fingers are up

        # Map the hand coordinates to slide coordinates
        xVal = int(np.interp(cx, [0, width], [0, imgCurrent.shape[1]]))*2
        yVal = int(np.interp(cy, [0, height], [0, imgCurrent.shape[0]]))*2
        indexFinger = (xVal, yVal)

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            elif fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
        elif fingers == [0, 1, 0, 0, 0]:
            if not annotationStart:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0] and annotations:
            annotations.pop(-1)
            annotationNumber -= 1
            buttonPressed = True

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for annotation in annotations:
        for j in range(1, len(annotation)):
            cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    imgSmall = cv2.resize(img, (ws, hs))
    imgCurrent[0:hs, -ws:] = imgSmall

    # Resize the image for display
    imgCurrentDisplay = cv2.resize(imgCurrent, (800, 600))  # Adjust the size as needed

    cv2.imshow("Slides", imgCurrentDisplay)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
