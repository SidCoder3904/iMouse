import time
import cv2 as cv
import mediapipe as mp
import pyautogui as pg

mesh = mp.solutions.face_mesh
W, H = pg.size()
live = cv.VideoCapture(0)
scaleX = 5
scaleY = 8
adjustX = 1/scaleX #or 1/scale?
adjustY = 2/scaleY #or 1/scale?
prevNoseX = None
prevNoseY = None
with mesh.FaceMesh(refine_landmarks=True) as face_mesh :
  while live.isOpened():
    success, frame = live.read()
    if success:
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        output = face_mesh.process(frame)
        points = output.multi_face_landmarks
        fH, fW, fZ = frame.shape
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if points :
            marks = points[0].landmark
            if prevNoseX==None or abs(prevNoseX-marks[1].x)>adjustX or abs(prevNoseY-marks[1].y)>adjustY :
                noseX = marks[1].x
                noseY = marks[1].y
            # print(noseX, noseY)
            cv.rectangle(frame, (int((noseX-adjustX)*fW), int((noseY-adjustY)*fW)), (int((noseX+adjustX)*fH), int((noseY+adjustY)*fH)), (0, 255, 0), 1)
            for i, landmark in enumerate(marks[474:478]) :
                x = int(landmark.x * fW)
                y = int(landmark.y * fH)
                # cv.circle(frame, (x, y), 3, (0, 255, 0), 1)
                if i==1 :
                    mouseX = scaleX * W * (landmark.x - (scaleX-1)/(2*scaleX) - noseX + 0.5) # see for face centering
                    mouseY = scaleY * H * (landmark.y - (scaleY-1)/(2*scaleY) - noseY + 0.5)
                    if mouseX > W - 5 :
                        mouseX = W - 5
                    if mouseX < 5 :
                        mouseX = 5
                    if mouseY > H - 5 :
                        mouseY = H - 5
                    if mouseY < 5 :
                        mouseY = 5
                    print(mouseX, mouseY)
                    pg.moveTo(mouseX, mouseY)
                lefteye = [marks[145], marks[159]]
                for landmark in lefteye :
                    x = int(landmark.x * fW)
                    y = int(landmark.y * fH)
                    cv.circle(frame, (x, y), 3, (0, 255, 0), -1)
                righteye = [marks[374], marks[386]]
                for landmark in righteye :
                    x = int(landmark.x * fW)
                    y = int(landmark.y * fH)
                    cv.circle(frame, (x, y), 3, (0, 255, 0), -1)
                if (righteye[0].y - righteye[1].y) <0.004 and (lefteye[0].y - lefteye[1].y) <0.004 :
                    print("both eyes blinked")
                    pg.click()
                    time.sleep(0.5)
                elif (lefteye[0].y - lefteye[1].y) <0.004 :
                    print("left eye blinked")
                    pg.leftClick()
                    time.sleep(0.5)
                elif (righteye[0].y - righteye[1].y) <0.004 :
                    print("right eye blinked")
                    pg.rightClick()
                    time.sleep(0.5)
            cv.imshow('Camera', frame)
            prevNoseX = noseX
            prevNoseY = noseY
        if cv.waitKey(20) & 0xFF == ord('d'):
            break
    else :
        continue
live.release()
cv.destroyAllWindows()