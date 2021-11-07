from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPropertyAnimation, QThread, pyqtSignal, Qt, pyqtSlot
import os, sys, random, time, json
import threading, re, cv2
from appUtil import AttendanceManager, StudentData
from PyQt5.QtGui import QValidator, QImage, QPixmap
import face_recognition
import numpy as np
from train_model import train
from gCloudUtil import *

# Shift screens
def goToHome():
    stackWidget.setCurrentIndex(0)

def goToLoginWindow():
    stackWidget.setCurrentIndex(1)

def goToSignUpWindow():
    stackWidget.setCurrentIndex(2)

def goToConfigWindow():
        stackWidget.setCurrentIndex(3)

def goToForgotPasswordWindow(var, fileName):
    global resetVar, FileName
    resetVar = var
    FileName = fileName
    stackWidget.setCurrentIndex(4)

def goToDevInfoWindow():
    stackWidget.setCurrentIndex(5)

def goToStudentLoginWindow():
    stackWidget.setCurrentIndex(6)

def goToStudentSignUpWindow():
    stackWidget.setCurrentIndex(7)

def goToDataCollectionWindow():
    DataCollectionThreadActive_ = True
    dataCollectionWindow.worker1 = dataCollectionWindow.Worker1()
    dataCollectionWindow.worker1.start()
    dataCollectionWindow.worker1.ImageUpdate.connect(dataCollectionWindow.ImageUpdateSlot)
    stackWidget.setCurrentIndex(8)

def goToShowImagesWindow():
    stackWidget.setCurrentIndex(9)

# Util functions
def checkFacultyLoginStats(self):
    if not facultyloggedIn_:
        goToLoginWindow()
    else:
        goToConfigWindow()

def checkStudentLoginStats(self):
    if not studentloggedIn_:
        goToStudentLoginWindow()
    else:
        goToDataCollectionWindow()

def resetPassword(window):
        try:
            window.enrollNum
            fileName = "studentData.json"
            keyWord = "Enrollment Number"
        except:
            fileName = "data.json"
            keyWord = "Email Address"

        var, _ = QtWidgets.QInputDialog.getText(window, f"Enter your {keyWord}", f"Enter your {keyWord} to validate with the database.")

        # Check if variable exists
        with open(fileName, "r+") as f:
                obj = json.load(f)

        if var in obj["details"].keys():
                goToForgotPasswordWindow(var, fileName)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Id not exists!")
            msg.setText("Profile corresponding to the entered id does not exist")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 440)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(200, 214, 228))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(200, 214, 228))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(200, 214, 228))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(200, 214, 228))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks|QtWidgets.QMainWindow.VerticalTabs)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(20, 260, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.duration = QtWidgets.QSpinBox(self.centralwidget)
        self.duration.setGeometry(QtCore.QRect(250, 200, 111, 20))
        self.duration.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.duration.setMaximum(120)
        self.duration.setDisplayIntegerBase(10)
        self.duration.setObjectName("duration")
        self.submitAndRun = QtWidgets.QPushButton(self.centralwidget)
        self.submitAndRun.setGeometry(QtCore.QRect(250, 300, 124, 29))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.submitAndRun.setFont(font)
        self.submitAndRun.setStyleSheet("QPushButton{\n"
"    background-color:rgb(255,0,0);\n"
"    border-radius:10px;\n"
"    color:#FFFFFF\n"
"}")
        self.submitAndRun.setObjectName("submitAndRun")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.mode = QtWidgets.QComboBox(self.centralwidget)
        self.mode.setGeometry(QtCore.QRect(250, 110, 104, 21))
        self.mode.setObjectName("mode")
        self.mode.addItem("")
        self.mode.addItem("")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 200, 211, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.moe = QtWidgets.QComboBox(self.centralwidget)
        self.moe.setGeometry(QtCore.QRect(250, 260, 111, 20))
        self.moe.setObjectName("moe")
        self.moe.addItem("")
        self.moe.addItem("")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 230, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 170, 121, 20))
        self.label_5.setMaximumSize(QtCore.QSize(300, 300))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.clsName = QtWidgets.QLineEdit(self.centralwidget)
        self.clsName.setGeometry(QtCore.QRect(250, 140, 111, 20))
        self.clsName.setMaximumSize(QtCore.QSize(200, 16777215))
        self.clsName.setObjectName("clsName")
        self.nSnips = QtWidgets.QComboBox(self.centralwidget)
        self.nSnips.setGeometry(QtCore.QRect(250, 230, 111, 20))
        self.nSnips.setObjectName("nSnips")
        self.nSnips.addItem("")
        self.nSnips.addItem("")
        self.nSnips.addItem("")
        self.meetName = QtWidgets.QLineEdit(self.centralwidget)
        self.meetName.setGeometry(QtCore.QRect(250, 170, 111, 20))
        self.meetName.setMaximumSize(QtCore.QSize(200, 16777215))
        self.meetName.setObjectName("meetName")
        self.head = QtWidgets.QLabel(self.centralwidget)
        self.head.setGeometry(QtCore.QRect(9, 50, 319, 40))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(209, 31, 209))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(216, 27, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 134, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 80, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 13, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 18, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 14, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(216, 27, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 141, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(209, 31, 209))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(216, 27, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 134, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 80, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 13, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 18, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 14, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(216, 27, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 141, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 13, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(216, 27, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 134, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 80, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 13, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 18, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 13, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 13, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(216, 27, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(216, 27, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(216, 27, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.head.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(18)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.head.setFont(font)
        self.head.setScaledContents(True)
        self.head.setWordWrap(True)
        self.head.setObjectName("head")
        self.devInfo = QtWidgets.QPushButton(self.centralwidget)
        self.devInfo.setGeometry(QtCore.QRect(660, 380, 75, 23))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.devInfo.setPalette(palette)
        self.devInfo.setFlat(True)
        self.devInfo.setObjectName("devInfo")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(680, 50, 51, 31))
        self.pushButton.setObjectName("pushButton")
        self.home = QtWidgets.QPushButton(self.centralwidget)
        self.home.setGeometry(QtCore.QRect(190, 10, 131, 24))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.home.sizePolicy().hasHeightForWidth())
        self.home.setSizePolicy(sizePolicy)
        self.home.setMinimumSize(QtCore.QSize(120, 10))
        self.home.setMaximumSize(QtCore.QSize(300, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.home.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.home.setFont(font)
        self.home.setAutoFillBackground(False)
        self.home.setStyleSheet("QPushButton{\n"
"    background-color: rgb(255,0, 0);\n"
"    border-radius:10px;\n"
"    color:#FFFFFF\n"
"}\n"
"")
        self.home.setAutoDefault(False)
        self.home.setDefault(False)
        self.home.setFlat(True)
        self.home.setObjectName("home")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.copy = QtWidgets.QAction(MainWindow)
        self.copy.setObjectName("copy")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # Our Changes

        # Change Bg Color
        MainWindow.setStyleSheet("QMainWindow {background-color:#c8d6e4;}")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Backend stuff
        self.submitAndRun.clicked.connect(self.startApp)
        self.home.clicked.connect(goToHome)
        self.devInfo.clicked.connect(goToDevInfoWindow)
        self.threadPool = QtCore.QThreadPool()
        #self.logOut.clicked.connect(self.LogOut)
        #self.devInfo.clicked.connect(goToDevInfoWindow)
        #app.aboutToQuit.connect(self.closeEvent)

    def startApp(self):
        ui.submitAndRun.hide()
        #MainWindow.submitAndRun.hide()
        self.is_active = True
        self.worker = Worker(self)
        self.worker.start()

    def runApp(self):
            mode = self.mode.currentText()
            clsName = self.clsName.text()
            meetName = self.meetName.text()
            meetDuration = int(self.duration.value())
            nSnips = int(self.nSnips.currentText())
            moe = self.moe.currentText()

            self.atm = AttendanceManager(mode, clsName, meetName, meetDuration, nSnips, moe)

            # Run model on meeting
            if mode == "Microsoft Teams":
                #self.worker = Worker(self.atm.runApp)
                #self.threadPool.start(self.worker)
                self.atm.runApp()
            else:
                # Send critical message
                raise ValueError("Mode not found!")

            ui.submitAndRun.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Attendance Record Management System"))
        self.label_8.setText(_translate("MainWindow", "Method of Evaluation"))
        self.duration.setSpecialValueText(_translate("MainWindow", "40"))
        self.submitAndRun.setText(_translate("MainWindow", "Submit and Run"))
        self.label_3.setText(_translate("MainWindow", "Mode of Meeting"))
        self.mode.setItemText(0, _translate("MainWindow", "Microsoft Teams"))
        self.mode.setItemText(1, _translate("MainWindow", "Zoom"))
        self.label_6.setText(_translate("MainWindow", "Meeting Duration (in mins)"))
        self.moe.setItemText(0, _translate("MainWindow", "Weighted Average"))
        self.moe.setItemText(1, _translate("MainWindow", "Top N"))
        self.label_7.setText(_translate("MainWindow", "Number of Snips"))
        self.label_4.setText(_translate("MainWindow", "Class Name"))
        self.label_5.setText(_translate("MainWindow", "Meeting Name"))
        self.nSnips.setItemText(0, _translate("MainWindow", "1"))
        self.nSnips.setItemText(1, _translate("MainWindow", "3"))
        self.nSnips.setItemText(2, _translate("MainWindow", "5"))
        self.head.setText(_translate("MainWindow", "Enter the Configurations"))
        self.devInfo.setText(_translate("MainWindow", "Dev Info"))
        self.pushButton.setText(_translate("MainWindow", "Log out"))
        self.home.setText(_translate("MainWindow", "Home"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Ne w File can be created"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.copy.setText(_translate("MainWindow", "Cope"))
        self.copy.setStatusTip(_translate("MainWindow", "File can be copied"))
        self.copy.setShortcut(_translate("MainWindow", "Ctrl+C"))

    def closeEvent(self):
        self.worker.exit()
        print("Event Closed!!!")
        sys.exit(0)

class Worker(QThread):
    def __init__(self, parent):
        super(Worker, self).__init__()
        self.parent = parent

    def run(self):
        self.is_active = True
        self.parent.runApp()

class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow,self).__init__()
        loadUi("Windows/LoginWindow.ui", self)
        self.setWindowTitle("Attendance Record Management System")
        self.setStyleSheet("QDialog {background-color:#c8d6e4;}")

        self.SignUp.clicked.connect(goToSignUpWindow)
        self.loginBtn.clicked.connect(self.verifyAndLogin)
        self.home.clicked.connect(goToHome)
        #self.login_signUp.clicked.connect(goToLoginWindow)
        self.forgotPassBtn.clicked.connect(lambda: resetPassword(self))
        self.devInfo.clicked.connect(goToDevInfoWindow)

    def verifyAndLogin(self):
        email = self.email_id.toPlainText().lower()
        #password = QtWidgets.QLabel("password").text()
        password = self.password.text()
        error_ = 0

        data = getFileDataFromBucket("data.json")
        #with open('data.json','r+') as f:
        #    data=json.load(f)

        if(email in data['details'].keys()):
            if(password == data['details'][str(email)]['Password']):
                global facultyloggedIn_
                facultyloggedIn_ = True
                goToConfigWindow()
            else:
                error_ = 1
        else:
            error_ = 1

        if error_:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Login Credentials Invalid")
            msg.setText("You appeared to have entered wrong email/password")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()
        self.eraseLabels()

    def eraseLabels(self):
        self.email_id.clear()
        self.password.clear()

    def updateText(self):
        with open("textSnippets.txt", "r") as f:
            data = f.read().split("\n\n")
            self.loginText.setText(data[0])
            for i in range(10):
                print(i)
                val = random.randint(0, len(data)-1)
                self.anim = QPropertyAnimation(self.loginText, b"text")
                self.loginText.setText(data[val])
                time.sleep(5)
                self.anim.setDuration(200)

class SignUpWindow(QDialog):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        loadUi("Windows/SignUpWindow.ui", self)
        self.setWindowTitle("Attendance Record Management System")
        self.setStyleSheet("QDialog {background-color:#c8d6e4;}")

        self.signUp.clicked.connect(self.SignUp)
        self.home.clicked.connect(goToHome)
        #self.login.clicked.connect(goToLoginWindow)

        # Constrain Input
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[0-9]{10}'))
        self.contact.setValidator(validator)

        self.devInfo.clicked.connect(goToDevInfoWindow)

    def SignUp(self):
        name_ = self.name.toPlainText()
        email_id_ = self.email_id.toPlainText()

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email_id_):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Email invalid!")
            msg.setText("The entered email address is not a valid one!")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            _ = msg.exec_()
            self.eraseLabels()
            return
        number_ = self.contact.text()
        pwd1 = self.password.text()
        pwd2 = self.cPassword.text()

        if(pwd1==pwd2):
            #with open('data.json','r+') as fil:
            #    ob1=json.load(fil)
            ob1 = getFileDataFromBucket("data.json")

            if email_id_ in ob1["details"].keys():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Email already present")
                msg.setText("The entered is already taken up. Please enter a unique email id")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                _ = msg.exec_()

            ob1['details'][email_id_.lower()]={'Name':name_,'Contact_number':number_,'Password':pwd1}

            with open("data.json", "w") as f:
                json.dump(ob1,f)
            #pushDataToBucket("data.json", ob1)

            goToLoginWindow()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Passwords Don't Match")
            msg.setText("The entered passwords don't match. Try it again.")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            _ = msg.exec_()

    def eraseLabels(self):
        self.name.clear()
        self.email_id.clear()
        self.contact.clear()
        self.password.clear()
        self.cPassword.clear()

class HomeWindow(QMainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("Windows/HomeWindow.ui", self)
        self.home.clicked.connect(goToHome)
        self.student.clicked.connect(checkStudentLoginStats)
        self.faculty.clicked.connect(checkFacultyLoginStats)

class ForgotPasswordWindow(QMainWindow):
    def __init__(self):
        super(ForgotPasswordWindow, self).__init__()
        loadUi("Windows/ForgotPasswordWindow.ui", self)
        self.resetPassword.clicked.connect(self.updatePassword)
        self.home.clicked.connect(goToHome)

    def updatePassword(self):
        if self.nPassword.text() == self.cPassword.text():

            #with open(FileName, 'r+') as f:
            #    obj = json.load(f)
            obj = getFileDataFromBucket(FileName)
            obj["details"][str(resetVar)]["Password"] = self.nPassword.text()

            with open(FileName, "w") as f:
                json.dump(obj, f)
            #pushDataToBucket(FileName, obj)

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Password Reset')
            msg.setText(f"Your password for the id {resetVar} has been successfully reset")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()

            if FileName=="studentData.json":
                goToStudentLoginWindow()
            else:
                goToLoginWindow()

        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Passwords unmatch')
            msg.setText(f"You appeared to have written different passwords.")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_()
        self.eraseLabels()

    def eraseLabels(self):
        self.nPassword.clear()
        self.cPassword.clear()

class DevInfoWindow(QMainWindow):
    def __init__(self):
        super(DevInfoWindow, self).__init__()
        loadUi("Windows/DevInfo.ui", self)
        self.home.clicked.connect(goToHome)
        self.faculty.clicked.connect(checkFacultyLoginStats)
        self.student.clicked.connect(checkStudentLoginStats)

class StudentLoginWindow(QMainWindow):
    def __init__(self):
        super(StudentLoginWindow, self).__init__()
        loadUi("Windows/StudentLoginWindow.ui", self)
        self.home.clicked.connect(goToHome)
        self.loginBtn.clicked.connect(self.verifyAndLogin)
        self.SignUp.clicked.connect(goToStudentSignUpWindow)
        self.forgotPassBtn.clicked.connect(lambda: resetPassword(self))
        self.devInfo.clicked.connect(goToDevInfoWindow)

    def verifyAndLogin(self):
        enroll = self.enrollNum.toPlainText()
        password = self.password.text()
        error_ = 0
        #with open('studentData.json','r+') as f:
        #    data=json.load(f)
        data = getFileDataFromBucket("studentData.json")

        if(enroll in data['details'].keys()):
            if(password == data['details'][str(enroll)]['Password']):
                global studentloggedIn_, currentEnroll_, clsName_
                studentloggedIn_ = True
                currentEnroll_ = enroll
                clsName_ = data["details"][enroll]["Class"]
                goToDataCollectionWindow()
            else:
                error_ = 1
        else:
            error_ = 1

        if error_:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Login Credentials Invalid")
            msg.setText("You appeared to have entered wrong enroll/password")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()
        self.eraseLabels()

    def eraseLabels(self):
        self.enrollNum.clear()
        self.password.clear()

class StudentSignUpWindow(QMainWindow):
    def __init__(self):
        super(StudentSignUpWindow, self).__init__()
        loadUi("Windows/StudentSignUpWindow.ui", self)

        self.signUp.clicked.connect(self.SignUp)
        self.home.clicked.connect(goToHome)
        self.login.clicked.connect(goToStudentLoginWindow)

        # Constrain Input
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[0-9]{10}'))
        self.contact.setValidator(validator)

        self.devInfo.clicked.connect(goToDevInfoWindow)

    def SignUp(self):
        name_ = self.name.toPlainText()
        email_id_ = self.email_id.toPlainText()
        enrollNum = self.enrollNum.toPlainText()
        global clsName_
        clsName_ = self.clsName.toPlainText()

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email_id_):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Email invalid!")
            msg.setText("The entered email address is not a valid one!")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            _ = msg.exec_()
            self.eraseLabels()
            return

        number_ = self.contact.text()
        pwd1 = self.password.text()
        pwd2 = self.cPassword.text()

        if(pwd1==pwd2):
            #with open('studentData.json','r+') as fil:
            #    ob1=json.load(fil)
            ob1 = getFileDataFromBucket("studentData.json")

            if enrollNum in ob1["details"].keys():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Enrollment Number already present")
                msg.setText("The entered enrollment number is already taken up. Please enter a unique enrollment number")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                _ = msg.exec_()
                self.eraseLabels()
                return

            ob1['details'][enrollNum]={'Name':name_,'Contact_number':number_,'Password':pwd1, 'email_id':email_id_, 'Class':clsName_}
            with open("studentData.json", "w") as f:
                json.dump(ob1,f)
            #pushDataToBucket("studentData.json", ob1)

            # Make dataset directory for the particular student
            if not os.path.exists(f"Dataset/{clsName_}/{enrollNum}"):
                os.makedirs(f"Dataset/{clsName_}/{enrollNum}")

            goToStudentLoginWindow()

        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Passwords Don't Match")
            msg.setText("The entered passwords don't match. Try it again.")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            _ = msg.exec_()
        self.eraseLabels()

    def eraseLabels(self):
        self.name.clear()
        self.email_id.clear()
        self.contact.clear()
        self.password.clear()
        self.cPassword.clear()
        self.enrollNum.clear()
        self.clsName.clear()

class DataCollectionWindow(QMainWindow):
    def __init__(self, imgPtr: int=0, onlineTrain: bool=False):
        if not imgPtr:
            self.imgPtr = 1
        else:
            self.imgPtr = imgPtr

        self.onlineTrain = onlineTrain
        super(DataCollectionWindow, self).__init__()
        loadUi("Windows/DataCollectionWindow.ui", self)
        self.capture.clicked.connect(self.askAndSave)
        self.home.clicked.connect(goToHome)
        self.devInfo.clicked.connect(goToDevInfoWindow)
        self.showImages.clicked.connect(self.showCurrentImages)
        self.train.clicked.connect(self.trainModel)

    def trainModel(self):
        train()

    def showCurrentImages(self):
        if currentEnroll_!="":
            images = os.listdir(f"Dataset/{clsName_}/{currentEnroll_}")
            labels = [showImagesWindow.lbl1,showImagesWindow.lbl1, showImagesWindow.lbl2, showImagesWindow.lbl3, showImagesWindow.lbl4, showImagesWindow.lbl5,
                    showImagesWindow.lbl6, showImagesWindow.lbl7, showImagesWindow.lbl8, showImagesWindow.lbl9, showImagesWindow.lbl10]
            for i, lbl in zip(range(len(images)), labels):
                imgPtr = int(os.path.splitext(images[i])[0])
                im = QPixmap(f"Dataset/{clsName_}/{currentEnroll_}/{imgPtr-1}.png")
                lbl.setPixmap(im)
                lbl.setScaledContents(True)
                lbl.show()

        goToShowImagesWindow()

    def askAndSave(self):
        print(self.imgPtr)
        # len(os.listdir(f"./Dataset/{clsName_}/{currentEnroll_}"))<10
        if self.imgPtr <= 10 or self.onlineTrain:
            msg = QMessageBox()
            msg.setWindowTitle("Are you sure you wanna save this pic?")
            msg.setText("The taken picture would be stored for training.")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
            x = msg.exec_()
            if x==QMessageBox.Save:
                img = cv2.flip(self.worker1.frame, 1)
                cv2.imwrite(f"./Dataset/{clsName_}/{currentEnroll_}/{self.imgPtr}.png", img)
                self.CurrentImg.setText(f"Img {self.imgPtr}.png has been updated successfully")
                self.CurrentImg.adjustSize()
                self.imgPtr+=1

                if self.onlineTrain:
                    self.onlineTrain = False
                    boxes = face_recognition.face_locations(img)
                    encodings = face_recognition.face_encodings(img, boxes)[0] #Warning only one box expected!
                    print(encodings)
                    f = open("StudentEncodings.json", "r")
                    data = json.load(f); f.close()
                    data["details"][currentEnroll_][self.imgPtr-2] = list(encodings)

                    f = open("StudentEncodings.json", "w")
                    json.dump(data,f)
                    f.close()
            else:
                print("Cancelled!")
                pass
        else:
            dataCollectionWindow.capture.setText("Add Data")
            dataCollectionWindow.capture.clicked.connect(self.submitAndEncode)

    def submitAndEncode(self):
        path = f"Dataset/{clsName_}/{currentEnroll_}"
        std = StudentData()
        #t1 = threading.Thread(target=std.calculateEncodings, args=(path, currentEnroll_))

        success = std.calculateEncodings(path, currentEnroll_)
        msg = QMessageBox()
        if success:
            msg.setWindowTitle("Encodings added successfully!")
            msg.setText("The encodings corresponding to your provided photographs have been added and the model is trained for new data successfully.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        else:
            msg.setWindowTitle("Failed to add Encodings")
            msg.setText("There was a problem adding the encodings corresponding to your photographs!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def ImageUpdateSlot(self, Image):
        self.videoFrame.setPixmap(QPixmap.fromImage(Image))
        self.videoFrame.setScaledContents(True)

    class Worker1(QThread):
        ImageUpdate = pyqtSignal(QImage)
        def run(self):
            self.ThreadActive = True
            Capture = cv2.VideoCapture(0)
            while self.ThreadActive:
                ret, frame = Capture.read()
                if ret:
                    self.frame = frame
                    Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    flippedImage = cv2.flip(Image, 1)
                    boxes = face_recognition.face_locations(flippedImage)
                    for (top, right, bottom, left) in boxes:
                        cv2.rectangle(flippedImage, (left, top), (right, bottom), (19, 209, 60), cv2.FONT_HERSHEY_COMPLEX, 1)

                    # Show Image Bounding Boxes
                    qtFormatImage = QImage(flippedImage.data, flippedImage.shape[1], flippedImage.shape[0], QImage.Format_RGB888)
                    img = qtFormatImage.scaled(640, 480, Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(img)

        def stop(self):
            self.ThreadActive = False

class ShowImagesWindow(QMainWindow):
    def __init__(self):
        super(ShowImagesWindow, self).__init__()
        loadUi("Windows/ShowImagesWindow.ui", self)
        self.back.clicked.connect(goToDataCollectionWindow)
        self.updatePic.clicked.connect(self.changePic)

    def changePic(self):
        dataCollectionWindow.imgPtr = int(self.changePicBox.currentText())
        dataCollectionWindow.onlineTrain = True
        goToDataCollectionWindow()

if __name__ == "__main__":

    # Global Config
    facultyloggedIn_ = False
    studentloggedIn_ = False
    currentEnroll_ = ""
    currentEmail_ = ""
    clsName_ = ""
    ThreadActive_ = ""

    app = QtWidgets.QApplication(sys.argv)
    stackWidget = QtWidgets.QStackedWidget()
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowTitle("Title")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    loginWindow = LoginWindow()
    loginWindow.setWindowTitle("Attendance Record Management System")
    signUpWindow = SignUpWindow()
    signUpWindow.setWindowTitle("Attendance Record Management System")
    homeWindow = HomeWindow()
    homeWindow.setWindowTitle("Attendance Record Management System")
    forgotPasswordWindow = ForgotPasswordWindow()
    forgotPasswordWindow.setWindowTitle("Attendance Record Management System")
    devInfoWindow = DevInfoWindow()
    devInfoWindow.setWindowTitle("Attendance Record Management System")
    studentSignUpWindow = StudentSignUpWindow()
    studentLoginWindow = StudentLoginWindow()
    dataCollectionWindow = DataCollectionWindow()
    showImagesWindow = ShowImagesWindow()

    stackWidget.addWidget(homeWindow)
    stackWidget.addWidget(loginWindow)
    stackWidget.addWidget(signUpWindow)
    stackWidget.addWidget(MainWindow)
    stackWidget.addWidget(forgotPasswordWindow)
    stackWidget.addWidget(devInfoWindow)
    stackWidget.addWidget(studentLoginWindow)
    stackWidget.addWidget(studentSignUpWindow)
    stackWidget.addWidget(dataCollectionWindow)
    stackWidget.addWidget(showImagesWindow)

    stackWidget.setFixedHeight(440)
    stackWidget.setFixedWidth(740)

    stackWidget.show()
    app.exec_()
