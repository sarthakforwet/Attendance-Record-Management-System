<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>347</height>
   </rect>
  </property>
  <property name="font">
   <font>
    <pointsize>12</pointsize>
   </font>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTextEdit" name="textEdit">
    <property name="geometry">
     <rect>
      <x>360</x>
      <y>20</y>
      <width>351</width>
      <height>51</height>
     </rect>
    </property>
   </widget>
   <widget class="QTextEdit" name="textEdit_2">
    <property name="geometry">
     <rect>
      <x>360</x>
      <y>100</y>
      <width>351</width>
      <height>51</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>260</x>
      <y>40</y>
      <width>55</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>EMAIL ID</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>260</x>
      <y>110</y>
      <width>55</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Password</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_clear">
    <property name="geometry">
     <rect>
      <x>390</x>
      <y>220</y>
      <width>93</width>
      <height>28</height>
     </rect>
    </property>
    <property name="text">
     <string>CANCEL</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_open">
    <property name="geometry">
     <rect>
      <x>530</x>
      <y>220</y>
      <width>93</width>
      <height>28</height>
     </rect>
    </property>
    <property name="text">
     <string>LOGIN</string>
    </property>
   </widget>
   <widget class="QRadioButton" name="radioButton">
    <property name="geometry">
     <rect>
      <x>360</x>
      <y>180</y>
      <width>151</width>
      <height>20</height>
     </rect>
    </property>
    <property name="text">
     <string>INSTRUCTOR</string>
    </property>
   </widget>
   <widget class="QRadioButton" name="radioButton_2">
    <property name="geometry">
     <rect>
      <x>530</x>
      <y>180</y>
      <width>111</width>
      <height>20</height>
     </rect>
    </property>
    <property name="text">
     <string>STUDENT</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>34</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuLOGIN">
    <property name="title">
     <string>LOGIN</string>
    </property>
   </widget>
   <addaction name="menuLOGIN"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
