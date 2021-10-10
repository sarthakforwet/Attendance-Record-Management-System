import face_recognition
from sklearn.svm import SVC
import numpy as np, pandas as pd
import os, time, random, json
from sklearn.preprocessing import LabelEncoder
import pickle, cv2
 
model = pickle.loads(open("model_knn.pickle", "rb").read())
le = pickle.loads(open("le.pickle","rb").read())

def predict_video(filename: str):
    cap = cv2.VideoCapture(filename)
    while(cap):
        success, img = cap.read()
        if success:
            boxes = face_recognition.face_locations(img, model="hog")
            encodings = face_recognition.face_encodings(img, boxes)
            cv2.imshow("Prediction", img)
            names = []
            scores = []
            for encoding, (top, bottom, left, right) in zip(encodings, boxes):
                encoding = np.expand_dims(encoding, axis=0)
                preds = model.predict_proba(encoding)[0]
                j = np.argmax(preds)
                if preds[j] > 0.70:
                    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), cv2.FONT_HERSHEY_COMPLEX)
                    scores.append(preds[j])
                    names.append(le.classes_[j])
                else:
                    continue

            cv2.imwrite("prediction.png", img) # Save the result
            cv2.waitKey(27)
            print(names)
            print(scores)

#cap = cv2.VideoCapture("../test_video2.mp4")

def predict_pic(img_path: str):
    img = cv2.imread(img_path)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #cv2.imshow("Testing",img)
    boxes = face_recognition.face_locations(img)
    embeddings = face_recognition.face_encodings(img, boxes)
    names = []
    scores = []
    for embedding, (top, right, bottom, left) in zip(embeddings, boxes):
        embedding = np.expand_dims(embedding, axis=0)
        #print(model.predict_proba(embedding))
        cls = np.argmax(model.predict_proba(embedding))
        score = np.max(model.predict_proba(embedding))
        if score > 0.9:
            scores.append(score)
            names.append(le.classes_[cls])
            #cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), cv2.FONT_HERSHEY_COMPLEX)

    #print(f"Scores: {scores}")
    #print(f"Names: {names}")
    return scores, names
    #cv2.imshow('Prediction', img)
    #cv2.waitKey(0)

if __name__ == "__main__":
    predict_pic("../test5.jpeg")