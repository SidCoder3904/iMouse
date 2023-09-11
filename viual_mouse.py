import cv2 as cv
import mediapipe as mp
import pyautogui as pg

mesh = mp.solutions.face_mesh
W, H = pg.size()
live = cv.VideoCapture(0)

with mesh.FaceMesh(refine_landmarks=True) as face_mesh :
  while live.isOpened():
    success, frame = live.read()
    if success:
        # cropped = frame[frame.shape[1]//4 : 3*frame.shape[1]//4, frame.shape[0]//4 : 3*frame.shape[0]//4]
        # frame = cv.flip(cropped, 1)
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        output = face_mesh.process(frame)
        points = output.multi_face_landmarks
        fH, fW, fZ = frame.shape
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if points :
            marks = points[0].landmark
            for i, landmark in enumerate(marks[474:478]) :
                x = int(landmark.x * fW)
                y = int(landmark.y * fH)
                cv.circle(frame, (x, y), 3, (0, 255, 0), 1)
                if i==1 :
                    mouseX = W * landmark.x
                    mouseY = H * landmark.y
                    print(mouseX, mouseY)
                    pg.moveTo(mouseX, mouseY)
                lefteye = [marks[145], marks[159]]
                for landmark in lefteye :
                    x = int(landmark.x * fW)
                    y = int(landmark.y * fH)
                    cv.circle(frame, (x, y), 3, (255, 0, 0), 1)
                if (lefteye[0].y - lefteye[1].y) <0.004 :
                    print("left eye blinked")
                    pg.click()
                    pg.sleep(1)
            cv.imshow('Camera', frame)
        if cv.waitKey(20) & 0xFF == ord('d'):
            break
    else :
        continue
live.release()
cv.destroyAllWindows()