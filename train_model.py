import face_recognition
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import numpy as np, pandas as pd
import os, time, random, json
from sklearn.preprocessing import LabelEncoder
import pickle

f = open("Encodings.json", "r")
data = json.load(f)

lbl = LabelEncoder()
labels = lbl.fit_transform(data["name"])
#svm = SVC(kernel = "rbf", gamma=0.8, C=1.0, probability=True)
knn = KNeighborsClassifier(n_neighbors=5, p=2, n_jobs=-1)
print(np.unique(labels))
knn.fit(data["encodings"], labels)


#svm.fit(data["encodings"], labels)
model_file = open("model_knn.pickle", "wb")
model_file.write(pickle.dumps(knn))

encoder_file = open("le.pickle", "wb")
encoder_file.write(pickle.dumps(lbl))

model_file.close(); encoder_file.close()