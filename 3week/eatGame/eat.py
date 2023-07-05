import os
import random
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = FaceMeshDetector(maxFaces=1)
idList = [0, 17, 78, 292]

folderEatable = '/Objects/eatable'
listEatable = os.listdir(folderEatable)
eatables = []
for object in listEatable:
    eatables.append(cv2.imread(f'{folderEatable}/{object}', cv2.IMREAD_UNCHANGED))

folderNonEatable = 'C:\Users\advan\OneDrive\바탕 화면\하계방학git\eatGame\Objects\noneatable'
listNonEatable = os.listdir(folderNonEatable)
nonEatables = []
for object in listNonEatable:
    nonEatables.append(cv2.imread(f'{folderNonEatable}/{object}', cv2.IMREAD_UNCHANGED))

currentObject = eatables[0]
pos = [300, 0]
speed = 5
count = 0
global isEatable
isEatable = True
gameOver = False

def resetObject():
    global isEatable
    pos[0] = random.randint(100, 1180)
    pos[1] = 0
    randNo = random.randint(0, 2)
    if randNo == 0:
        currentObject = nonEatables[random.randint(0, 3)]
        isEatable = False
    else:
        currentObject = eatables[random.randint(0, 3)]
        isEatable = True

    return currentObject

while True:
    success, img = cap.read()

    if gameOver is False:
        img, faces = detector.findFaceMesh(img, draw=False)

        img = cvzone.overlayPNG(img, currentObject, pos)
        pos[1] += speed

        if pos[1] > 520:
            currentObject = resetObject()

        if faces:
            face = faces[0]

            up = face[idList[0]]
            down = face[idList[1]]

            for id in idList:
                # 얼굴 지점에 원 그리기
                cv2.circle(img, face[id], 5, (255, 0, 255), 5)
            #얼굴의 위쪽과 아래쪽 지점 사이에 선 그리기
            cv2.line(img, up, down, (0, 255, 0), 3)
            #얼굴의 두 가운데 지점 사이에 선 그리기
            cv2.line(img, face[idList[2]], face[idList[3]], (0, 255, 0), 3)
            #위쪽과 아래쪽 지점 사이의 거리 계산
            upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])
            #두 가운데 지점 사이의 거리 계산
            leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])

            cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
            cv2.line(img, (cx, cy), (pos[0] + 50, pos[1] + 50), (0, 255, 0), 3)
            distMouthObject, _ = detector.findDistance((cx, cy), (pos[0] + 50, pos[1] + 50))
            print(distMouthObject)

            ratio = int((upDown / leftRight) * 100)
            print(ratio) # 계산된 비율 출력
            if ratio > 60:
                mouthStatus = "Open"
            else:
                mouthStatus = "Closed"
            
            cv2.putText(img, mouthStatus, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

            if distMouthObject < 100 and ratio > 60:
                if isEatable:
                    currentObject = resetObject()
                else:
                    gameOver = True

        cv2.putText(img, str(count), (1100, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 5)

    else:
        cv2.putText(img, "Game Over", (300, 400), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 255), 10)

        cv2.imshow("image", img)
        key = cv2.waitKey(1)

        if key == ord('r'):
            resetObject()
            gameOver = False
            count = 0
            currentObject = eatables[0]
            pos = [300, 0]
        
        if key == ord('27'):
            break
    
    cap.release()
    cv2.destroyAllWindows()