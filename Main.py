import HandTracking as htm
import cv2 as cv
import numpy as np
import pyautogui

###########################
wCam, hCam = 640, 480
wScr, hScr = pyautogui.size()
frameR = 150
smoothing = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0
##########################
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector()


def Mouse(img):
    global frameR
    global smoothing
    global plocX
    global plocY
    global clocX
    global clocY
    global wScr
    global wCam
    global hScr
    global hCam
    # finding hands
    detector.findhands(img)
    lmlist, bbox = detector.findPosition(img)

    #cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 2. get the tip of index and middle finger
    if len(lmlist) != 0:
        Xindex, Yindex = lmlist[8][1], lmlist[8][2]
        Xmiddle, Ymiddle = lmlist[12][1], lmlist[12][2]
        # 3. check which one is up?
        fingers = detector.fingersUp()
        # 4. index: moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. coordinates the position (cam: 640*480) to (screen: 2560 × 1600)
            xMOUSE = np.interp(Xindex, (frameR, wCam - frameR), (0, wScr))
            yMOUSE = np.interp(Yindex, (frameR, hCam - frameR), (0, hScr))
            # 6. smoothen value
            clocX = plocX + (xMOUSE - plocX) / smoothing
            clocY = plocY + (yMOUSE - plocY) / smoothing
            # 7. move mouse
            pyautogui.moveTo(clocX, clocY)
            cv.circle(img, (Xindex, Yindex), 15, (20, 180, 90), cv.FILLED)
            plocY, plocX = clocY, clocX

        # 8. both are up: left-click mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. finding distance
            length, bbox = detector.findDistance(8, 12, img)
            print(length)
            # 10. click if distance was short
            if length < 40:
                pyautogui.click()

    return img


def main():
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)

        img = Mouse(img)

        # 11. display
        cv.imshow("demo", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()

