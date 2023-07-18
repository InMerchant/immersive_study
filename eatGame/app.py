from datetime import datetime
from flask import Flask, render_template, Response, redirect, request, url_for
import os
import random
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone
from google.cloud import firestore

import firebase_admin
from firebase_admin import credentials, firestore

#이 부분의 키만 다운받으면 사용 가능
cred = credentials.Certificate('C:/Users/advan/Downloads/eatGame/serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = FaceMeshDetector(maxFaces=1)
idList = [0, 17, 78, 292]

folderEatable = 'Objects/eatable'
listEatable = os.listdir(folderEatable)
eatables = []
for object in listEatable:
    eatables.append(cv2.imread(f'{folderEatable}/{object}', cv2.IMREAD_UNCHANGED))

folderNonEatable = 'Objects/noneatable'
listNonEatable = os.listdir(folderNonEatable)
nonEatables = []
for object in listNonEatable:
    nonEatables.append(cv2.imread(f'{folderNonEatable}/{object}', cv2.IMREAD_UNCHANGED))

currentObject = eatables[0]
pos = [300, 0]
speed = 5
count = 0
isEatable = True
gameOver = False


def resetGame():
    global pos, count, gameOver
    pos = [300, 0]
    count = 0
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


def generate_frames():
    global cap, detector, currentObject, pos, speed, count, isEatable, gameOver

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
                    cv2.circle(img, face[id], 5, (255, 0, 255), 5)
                cv2.line(img, up, down, (0, 255, 0), 3)
                cv2.line(img, face[idList[2]], face[idList[3]], (0, 255, 0), 3)

                upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])
                leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])

                cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
                cv2.line(img, (cx, cy), (pos[0] + 50, pos[1] + 50), (0, 255, 0), 3)
                distMouthObject, _ = detector.findDistance((cx, cy), (pos[0] + 50, pos[1] + 50))
                print(distMouthObject)

                ratio = int((upDown / leftRight) * 100)
                if ratio > 60:
                    mouthStatus = "Open"
                else:
                    mouthStatus = "Closed"
                cv2.putText(img, mouthStatus, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

                if distMouthObject < 100 and ratio > 60:
                    if isEatable:
                        currentObject = resetObject()
                        count += 1
                    else:
                        gameOver = True
                cv2.putText(img, str(count), (1100, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 5)
            else:
                gameOver = True
                cv2.putText(img, "Game Over", (300, 400), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 255), 10)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            break

@app.route('/')
def index():
    resetGame()
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/gameOver')
def gameover():
    success = request.args.get('success')
    return render_template('gameover.html', score=count, success=success)


@app.route('/restartGame')
def restart_game():
    resetGame()
    return redirect(url_for('index'))

@app.route('/save_result', methods=['POST'])
def save_result_to_db():
    name = request.form.get('name')
    score = request.form.get('score')
    current_time = datetime.now()
    doc_ref = db.collection('results').document()
    doc_ref.set({
        'name': name,
        'score': score,
        'timestamp': current_time
    })
    return redirect(url_for('gameover', success=True))  # Add a return statement with a response message

@app.route('/leaderboard')
def leaderboard():
    leaderboard_ref = db.collection('results').order_by('score', direction=firestore.Query.DESCENDING).limit(10)
    leaderboard_data = leaderboard_ref.get()
    leaderboard_list = []
    rank = 1
    for doc in leaderboard_data:
        entry = doc.to_dict()
        entry['rank'] = rank
        leaderboard_list.append(entry)
        rank += 1

    return render_template('leaderboard.html', leaderboard=leaderboard_list)


if __name__ == '__main__':
    app.run(debug=True)
