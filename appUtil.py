import numpy as np, pandas as pd
import time, random, cv2, os
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyautogui
from PIL import Image
from predict import predict_pic
import argparse
import datetime
import smtplib
from email.message import EmailMessage
from automateTeamsUtil import send_attendance_alert
import face_recognition
import json
from train_model import train
import threading
from gCloudUtil import *

"""
parser = argparse.ArgumentParser()
parser.add_argument("-t", required=True, dest="t", help="Time for the meeting", type=int)
parser.add_argument("-s", dest="s", required=True, help="Number of snips to be taken", type=int)
parser.add_argument("-cls", dest="cls", required=True, help="Class name")
parser.add_argument("-clsName", dest='clsName', required=True, help='Name of the lecture')
args = parser.parse_args()
"""

class AttendanceManager:
    def __init__(self, mode, clsName, meetName,
    meetDuration, nSnips, moe):
        self.mode = mode
        self.clsName = clsName
        self.meetName = meetName
        self.meetDuration = meetDuration
        self.nSnips = nSnips
        self.moe = moe

        # Create DataFrame
        self.df = pd.DataFrame({"Enrollment Number":[], "Name":[],
            "Attendance":[], "Probability (%)":[],
            "Phone Number":[]})

        self.studentScores = {}
        self.studentAvailable = [os.path.split(e)[1] for e in os.listdir(f"Dataset\{self.clsName}")]
        for e in self.studentAvailable:
            self.studentScores[e] = []

    # Window Module
    def processImage(self):
        self.app = Application(backend='uia')
        titles = pyautogui.getAllTitles()
        for e in titles:
            if self.meetName in e:
                title = e
                break

        self.app = self.app.connect(title_re=title, timeout=20)
        self.app.window().maximize()
        time.sleep(2)
        pyautogui.screenshot("img.png")
        #time.sleep(2)
        scores, names = predict_pic("img.png")
        # = predict_pic("img.png")
        #t1.start()
        #scores, names = t1.join()
        #scores, names = [1,1,1], ["EN18CS301233", "EN18CS301234", "EN18CS301215"]
        send_keys("%{TAB}")
        for s, n in zip(scores, names):
            print(s, n)
            self.studentScores[n].append(s)

    def arrangeSlots(self):
        # Take Screenshots
        self.snipsTime = random.sample(range(5, self.meetDuration*60), self.nSnips) #Change time for a 40 minute class or use a standardized formula.
        #self.snipsTime = [10]
        print(self.snipsTime)
        self.alertTime = [e-3 for e in self.snipsTime]
        #self.alertTime = [6]

    def runApp(self):
        self.arrangeSlots()
        ptr = 0
        while(ptr < self.meetDuration*60):
            ptr +=1
            print(ptr, end="\r")
            time.sleep(1)
            if ptr in self.alertTime:
                send_attendance_alert(self.meetName, ptr)

            if ptr in self.snipsTime:
                self.snipsTime.remove(ptr)
                self.processImage()
        if self.moe=="Weighted Average":
            self.weightedAverage()
        else:
            self.TopN()

        self.ToCSVAndSend()

    def weightedAverage(self):
        #with open("studentData.json", "r") as f:
        #    data = json.load(f)
        data = getFileDataFromBucket("studentData.json")
        data = data["details"]
        # Calculate Weighted Average
        self.weights = [round(e, 3) for e in sorted(np.random.uniform(0.9, 1, size=(self.nSnips)))]
        scores = []
        for e in self.studentAvailable:
            if len(self.studentScores[e]) > 0:
                try:
                    score = np.mean(np.multiply(self.studentScores[e], self.weights[::-1][:len(self.studentScores[e])]))
                    if score > 0.6:
                        record = {}
                        record["Enrollment Number"] = e
                        record["Name"] = data[e]["Name"]
                        record["Attendance"] = "P"
                        record["Probability (%)"] = str(round(score, 4) * 100)
                        record["Phone Number"] = data[e]["Contact_number"]
                        self.df = self.df.append(record, ignore_index=True)
                        scores.append(score)
                    else:
                        # Process Image for that particular student
                        # Start this with an announcement saying the Enrollment number of the student.
                        print("Score not worthy!")
                        pass
                except:
                    continue

    def TopN(self):
        data = getFileDataFromBucket("studentData.json")
        data = data["details"]
        score={}
        temp=[]
        nSnipsToN={5:3,3:2,1:1}
        threshDict = {1: 0.9, 3:1.8, 5:2.7}
        for i in self.studentScores:
            temp=self.studentScores[i]
            temp.sort(reverse=True)
            if(sum(temp[:nSnipsToN[self.nSnips]])>=threshDict[self.nSnips]):
                #score[i]=sum(temp[:di[self.nSnips]])
                val=np.mean(temp[:nSnipsToN[self.nSnips]])
                record = {}
                record["Enrollment Number"] = i
                record["Name"] = data[i]["Name"]
                record["Attendance"] = "P"
                record["Probability (%)"] = str(round(val, 4) * 100)
                record["Phone Number"] = data[i]["Contact_number"]
                self.df = self.df.append(record, ignore_index=True)


    def ToCSVAndSend(self):
        # Convert to csv
        self.df.to_csv("Attendance report.csv", index=None)
        # Send dataframe via smtp api.
        FROM = "sarthakkhandelwal032000@gmail.com"
        TO = "en18cs301233@medicaps.ac.in"
        MESSAGE = f"Here's the attendance for {datetime.datetime.now().strftime('%d/%m/%Y')}"
        EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

        msg = EmailMessage()
        msg["Subject"] = f"Attendance report of {self.clsName} for {self.meetName} at {datetime.datetime.now().strftime('%d/%m/%Y')}"
        msg["From"] = FROM
        msg["To"] = TO
        msg.set_content(MESSAGE)

        with open("Attendance report.csv", 'r') as f:
            data = f.read()

        data = data.encode("utf-8")
        msg.add_attachment(data, maintype="application", subtype="csv", filename="Attendance Report.csv")

        with smtplib.SMTP_SSL("smtp.gmail.com", "465") as smtp:
            smtp.login(FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("mail sent!")

class StudentData():
    def calculateEncodings(self, path, n):
        try:
            imagePaths = os.listdir(path)
            EncodingList = []
            for imgPath in imagePaths:
                im = cv2.imread(os.path.join(path, imgPath))
                im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(im)
                encodings = face_recognition.face_encodings(im, boxes)
                for encoding in encodings:
                    print(imgPath)
                    EncodingList.append(list(encoding))
                time.sleep(2)

            #f  = open("StudentEncodings.json", "r+")
            #data = json.load(f)
            #f.close()
            data = getFileDataFromBucket("StudentEncodings.json")

            if n not in data["details"].keys():
                data["details"][n] = []

            data["details"][n].extend(EncodingList)

            #with open("StudentEncodings.json", "w") as f:
            #    json.dump(data, f)
            pushDataToBucket("StudentEncodings.json", data)
            # Rest for a while
            time.sleep(1)
            train()

            return True

        except Exception as e:
            print(e)
            return False