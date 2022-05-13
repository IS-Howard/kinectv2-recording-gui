from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import time
import cv2
import os
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

### status init:1 recording:2 pause:3

class record(QtCore.QThread):
    def run(self):
        self.status = 1
        self.video_path = None
        self.depth_filename = None
        self.color_filename = None
        self.width = 1920
        self.height = 1080

        while(self.video_path == None):
            time.sleep(0.005)
        depth_fourcc = cv2.VideoWriter_fourcc('F','F','V','1')
        color_fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out_depth = cv2.VideoWriter(os.path.join(self.video_path,self.depth_filename + '.avi'), depth_fourcc, 30, (512, 424))
        self.out_color = cv2.VideoWriter(os.path.join(self.video_path,self.color_filename + '.avi'), color_fourcc, 30, (self.width, self.height))
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Color)
        #print("recording")
        while(self.status!=0):
            if self.status==2:  # 3:pause 
                # print("recording")
                self.recording()
                #time.sleep(2)
        print("end")

    def recording(self):
        if self.kinect.has_new_color_frame():
            frame = kinect.get_last_color_frame()
            gbra = frame.reshape([height, width, 4])
            color_frame = gbra[:, :, 0:3]
            # b = cv2.resize(color_frame,(960,540),interpolation=cv2.INTER_CUBIC)
            # cv2.imshow('KINECT Video Stream_RGB', b)
            
        if self.kinect.has_new_depth_frame():
            frame = kinect.get_last_depth_frame()
            frame = np.reshape(frame, (424, 512))

            B = (frame / 256).astype(np.uint8)
            R = (frame % 256).astype(np.uint8)
            G = np.zeros((424, 512)).astype(np.uint8)

            a = cv2.merge((B,G,R))
            cv2.imshow('KINECT Video Stream_Depth', a)
            
        self.out_color.write(color_frame)
        color_frame = None
        self.out_depth.write(a)
        frame = None
        a = None
        b = None
        


class Ui_MainWindow(object):
    def readfolder(self):
        self.folder = QFileDialog.getExistingDirectory()
        self.lineEdit.setText(self.folder)
    def start(self):
        if self._status == 1 and self._left_seconds > 0:
            self.recorder.start()
            time.sleep(0.005)
            # print(self.lineEdit.text())
            self.recorder.status = 2
            self.recorder.video_path = self.lineEdit.text()
            self.recorder.depth_filename = self.lineEdit_2.text()
            self.recorder.color_filename = self.lineEdit_3.text()
            self._left_seconds -= 1
            self._status = 2
            self.showTime()
            self.timer.start(1000)
            self.pushButton.setText('pause')
        elif self._status == 3 and self._left_seconds > 0:
            self.recorder.status = 2
            self._left_seconds -= 1
            self._status = 2
            self.showTime()
            self.timer.start(1000)
            self.pushButton.setText('pause')
        elif self._status == 2:
            self.timer.stop()
            self._status = 3
            self.pushButton.setText('start')
            self.recorder.status = 3
    def stop(self):
        self._status = 1
        self._left_seconds = self.spinBox.value() * 60
        self.pushButton.setText('start')
        self.timer.stop()
        self.showTime()
        self.recorder.status = 0
    
    ### timer functions
    def showTime(self):
        total_seconds = min(self._left_seconds, 359940)  # Max time: 99:59:00
        hours = total_seconds // 3600
        total_seconds = total_seconds - (hours * 3600)
        minutes = total_seconds // 60
        seconds = total_seconds - (minutes * 60)
        self.textEdit.setText("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)))
        self.textEdit.setAlignment(QtCore.Qt.AlignHCenter)
    def _edit_event(self):
        if self._status == 1:
            self._left_seconds = self.spinBox.value() * 60
            self.showTime()
    def _countdown_and_show(self):
        if self._left_seconds > 0:
            self._left_seconds -= 1
            self.showTime()
        else:
            self.stop()
            # self.timer.stop()
            # self.showTime()
            # self.pushButton.setText('start')
            # self._status = 1
            # self._left_seconds = self.spinBox.value() * 60
    #############

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(560, 130, 29, 24))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.readfolder)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(270, 130, 291, 26))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 130, 101, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 210, 111, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(270, 210, 291, 26))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setText("depth")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(270, 290, 291, 26))
        self.lineEdit_3.setText("color")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 290, 111, 20))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(510, 430, 61, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(590, 430, 61, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.stop)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(157, 370, 91, 20))
        self.label_4.setObjectName("label_4")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(270, 370, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setValue(10)
        self.spinBox.valueChanged.connect(self._edit_event)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(270, 430, 211, 35))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("border: none")
        self.textEdit.setFontFamily("Arial")
        self.textEdit.setFontPointSize(12)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        #self.textEdit.viewport().setCursor(QtCore.Qt.ArrowCursor)
        #self.textEdit.viewport().installEventFilter(self)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self._status = 1
        self._left_seconds = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._countdown_and_show)
        self.showTime()
        self.recorder = record()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "儲存資料夾"))
        self.label_2.setText(_translate("MainWindow", "深度影片名稱"))
        self.label_3.setText(_translate("MainWindow", "深度影片名稱"))
        self.pushButton.setText(_translate("MainWindow", "start"))
        self.pushButton_2.setText(_translate("MainWindow", "stop"))
        self.label_4.setText(_translate("MainWindow", "錄製時長(min)"))
        self._edit_event()


if __name__ == "__main__":
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
