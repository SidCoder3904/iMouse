import cv2 as cv
import pyautogui as pg

live = cv.VideoCapture(0)
eye_harr_cascade = cv.CascadeClassifier('eyetrack.xml')

while True :
    isTrue, frame = live.read()
    invert = cv.flip(frame, 1)
    gray = cv.cvtColor(invert, cv.COLOR_BGR2GRAY)
    eye_track = eye_harr_cascade.detectMultiScale(gray)
    for x, y, w, h in eye_track :
        cv.rectangle(invert, (x, y), (x+w, y+h), (0, 255, 0), 1)
    if isTrue :
        cv.imshow("Live Camera", invert)
        if cv.waitKey(20) & 0xFF == ord('d') :
            break
    else :
        break
live.release()
cv.destroyAllWindows()