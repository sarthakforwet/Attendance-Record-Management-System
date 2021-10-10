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


parser = argparse.ArgumentParser()
parser.add_argument("-t", required=True, dest="t", help="Time for the meeting", type=int)
parser.add_argument("-s", dest="s", required=True, help="Number of snips to be taken", type=int)
parser.add_argument("-cls", dest="cls", required=True, help="Class name")
parser.add_argument("-clsName", dest='clsName', required=True, help='Class name for the lecture')
args = parser.parse_args()

# Create DataFrame
df = pd.DataFrame({"Enrollment Number":[], "Name":[], "Attendance":[], "Probability (%)":[], "Phone Number":[]})

studentScores = {}
studentAvailable = [os.path.split(e)[1] for e in os.listdir(f"..\Dataset\{args.cls}")]
for e in studentAvailable:
    studentScores[e] = []

# Window Module
def processImage():
    app = Application(backend='uia')
    titles = pyautogui.getAllTitles()
    for e in titles:
        if args.clsName in e:
            title = e
            break
    #try:
    app = app.connect(title_re=title, timeout=20)
    app.window().maximize()
    time.sleep(3)
    # Print - "Attendance To be captured"
    pyautogui.screenshot("snip.png")
    #im = Image.open('Ss1.png')
    scores, names = predict_pic("snip.png")
    #print(scores, names)
    send_keys("%{TAB}")
    #app.window().minimize()
    for s, n in zip(scores, names):
        print(s, n)
        studentScores[n].append(s)

# Take Screenshots
snipsTime = random.sample(range(10, args.t*60), args.s) #Change time for a 40 minute class or use a standardized formula.
print(snipsTime)
alertTime = [e-3 for e in snipsTime]
ptr = 0

while(ptr < args.t*60):
    ptr +=1
    print(ptr, end="\r")

    time.sleep(1)
    if ptr in alertTime:
        send_attendance_alert(args.clsName, ptr)

    if ptr in snipsTime:
        snipsTime.remove(ptr)
        processImage()

# Calculate Weighted Average
wghts = [round(e, 3) for e in sorted(np.random.uniform(0.9, 1, size=(args.s)))]


scores = []
for e in studentAvailable:
    if len(studentScores[e]) > 0:
        try:
            score = np.mean(np.multiply(studentScores[e], wghts))
            if score > 0.6:
                record = {}
                record["Enrollment Number"] = e
                record["Name"] = ""
                record["Attendance"] = "P"
                record["Probability (%)"] = str(round(score, 4) * 100)
                record["Phone Number"] = ""
                df = df.append(record, ignore_index=True)
                scores.append(score)
            else:
                # Process Image for that particular student
                # Start this with an announcement saying the Enrollment number of the student.
                print("here")
                pass

        except:
            continue
# Convert to csv
df.to_csv("Attendance report.csv", index=None)

# Send dataframe via smtp api.
FROM = "sarthakkhandelwal032000@gmail.com"
TO = "en18cs301233@medicaps.ac.in"
MESSAGE = f"Here's the attendance for {datetime.datetime.now().strftime('%d/%m/%Y')}"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

msg = EmailMessage()
msg["Subject"] = f"Attendance report of {args.cls} for {args.clsName} at {datetime.datetime.now().strftime('%d/%m/%Y')}"
msg["From"] = FROM
msg["To"] = TO
msg.set_content(MESSAGE)

with open("Attendance report.csv", 'r') as f:
    data = f.read()

data = data.encode("utf-8")
msg.add_attachment(data, maintype="application", subtype="csv", filename="Attendance Report.csv")
#print(studentScores)

with smtplib.SMTP_SSL("smtp.gmail.com", "465") as smtp:
    smtp.login(FROM, EMAIL_PASSWORD)
    smtp.send_message(msg)
    print("mail sent!")