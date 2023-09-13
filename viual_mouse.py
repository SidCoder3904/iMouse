# glitches to cater to...
# casual blinking 
# try using iris solutions of mp
# try classes
# retry adaptive face centering
# import time
import cv2 as cv
import mediapipe as mp
import pyautogui as pg

mesh = mp.solutions.face_mesh
W, H = pg.size()
live = cv.VideoCapture(0)
scaleX = 5
scaleY = 10
adjustX = 1/scaleX
adjustY = 2/scaleY
isFirst = True
with mesh.FaceMesh(refine_landmarks=True) as face_mesh :
  while live.isOpened():
    success, frame = live.read()
    if success:
        frame = cv.flip(frame, 1)
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        output = face_mesh.process(rgb)
        points = output.multi_face_landmarks
        fH, fW, fZ = frame.shape
        # frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if points :
            marks = points[0].landmark
            if isFirst :
                centerY = marks[6].y
                centerX = marks[6].x
                isFirst = False
            mid = marks[6]
            # cv.rectangle(frame, (int((centerX-adjustX)*fW), int((centerY-adjustY)*fW)), (int((centerX+adjustX)*fH), int((centerY+adjustY)*fH)), (0, 255, 0), 1)
            # print(mid)
            # x = int(mid.x * fW)
            # y = int(mid.y * fH)
            mouseX = scaleX * W * (mid.x - (scaleX-1)/(2*scaleX) - centerX + 0.5) # see for face centering
            mouseY = scaleY * H * (mid.y - (scaleY-1)/(2*scaleY) - centerY + 0.5)
            if mouseX > W - 5 :
                mouseX = W - 5
            if mouseX < 5 :
                mouseX = 5
            if mouseY > H - 5 :
                mouseY = H - 5
            if mouseY < 5 :
                mouseY = 5
            # print(mouseX, mouseY)
            pg.moveTo(mouseX, mouseY)
            lefteye = [marks[145], marks[159]]
            # for landmark in lefteye :
            #     x = int(landmark.x * fW)
            #     y = int(landmark.y * fH)
                # cv.circle(frame, (x, y), 1, (0, 255, 0), -1)
            righteye = [marks[374], marks[386]]
            # for landmark in righteye :
            #     x = int(landmark.x * fW)
            #     y = int(landmark.y * fH)
                # cv.circle(frame, (x, y), 1, (0, 255, 0), -1)
            Rblink = (righteye[0].y - righteye[1].y) <0.004
            Lblink = (lefteye[0].y - lefteye[1].y) <0.004
            if Rblink and Lblink :
                print("both eyes blinked")
                pg.click()
                # time.sleep(0.5)
            elif Lblink :
                print("left eye blinked")
                pg.leftClick()
                # time.sleep(0.5)
            elif Rblink :
                print("right eye blinked")
                pg.rightClick()
                # time.sleep(0.5)
            # cv.imshow('Camera', frame)
        # if cv.waitKey(20) & 0xFF == ord('d'):
        #     break
    else :
        continue
live.release()
cv.destroyAllWindows()