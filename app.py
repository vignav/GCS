from QSwitchControl import SwitchControl
from PyQt5 import QtWidgets, QtCore, QtWidgets
import sys
import os
from random import randint
from plot import graph
from map_plot import mapWidget
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QLabel,QPushButton, QApplication, QWidget
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("GCS")

        # Menu
        self.logo = QLabel()
        logo_image = QPixmap('./image.jpeg')
        logo_image = logo_image.scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        self.logo.setPixmap(logo_image)

        self.MENU_label = QLabel('TEAM ID:1020')
        self.start_button = QPushButton()
        self.start_button.setText("START>>")
        self.start_button.clicked.connect(self.start)

        self.stop_button = QPushButton()
        self.stop_button.setText("<<STOP")
        self.stop_button.clicked.connect(self.stop)

        self.calibrate_button = QPushButton()
        self.calibrate_button.setText("CALIBRATION")
        self.calibrate_button.clicked.connect(self.calibrate)

        self.switch_control_1 = SwitchControl(bg_color="#777777", circle_color="#11111", active_color="#ff0000", animation_curve=QtCore.QEasingCurve.InOutCubic, animation_duration=100, checked=True, change_cursor=False)
        self.switch_control_2 = SwitchControl(bg_color="#777777", circle_color="#11111", active_color="#ff0000", animation_curve=QtCore.QEasingCurve.InOutCubic, animation_duration=100, checked=True, change_cursor=False)

        self.switch_control_1.toggled.connect(self.switch1_toggle)
        self.switch_control_2.toggled.connect(self.switch2_toggle)

        self.toggle1 = True
        self.toggle2 = True
        MISSION_STATUS_layout = QVBoxLayout()

        self.label_mission = QLabel('MISSION STATUS')
        self.label_mission.setStyleSheet("border: 0px solid black;")
        self.label_mission.setAlignment(QtCore.Qt.AlignCenter)

        MISSION_STATUS_layout.addWidget(self.label_mission)
        self.text_list = ['LAUNCH MISSION','CALIBRATE','ROCKET LAUNCH','ASCENT','RELEASE PAYLOAD','DESCENT','MISSION COMPLETE']
        self.labels = []
        for i, text in enumerate(self.text_list) :
            self.labels.append(QLabel(text))
            self.labels[i].setStyleSheet("background-color: grey")
            self.labels[i].setAlignment(QtCore.Qt.AlignCenter)
            MISSION_STATUS_layout.addWidget(self.labels[i])

        self.MISSION_STATUS_widget = QtWidgets.QWidget()
        self.MISSION_STATUS_widget.setLayout(MISSION_STATUS_layout)
        self.MISSION_STATUS_widget.setStyleSheet("border: 1px solid black;")

        self.Packet_count = QLabel('PACKET COUNT : 0')
        self.RTC = QLabel('')
        self.Date = QLabel('')

        MENU_layout = QVBoxLayout()
        MENU_layout.addWidget(self.logo, stretch=1)
        MENU_layout.addWidget(self.MENU_label)
        MENU_layout.addWidget(self.start_button)
        MENU_layout.addWidget(self.stop_button)
        MENU_layout.addWidget(self.calibrate_button)
        MENU_layout.addWidget(self.switch_control_1)
        MENU_layout.addWidget(self.switch_control_2)
        MENU_layout.addWidget(self.MISSION_STATUS_widget)
        MENU_layout.addWidget(self.Packet_count)
        MENU_layout.addWidget(self.RTC)
        MENU_layout.addWidget(self.Date)

        self.MENU_widget = QtWidgets.QWidget()
        self.MENU_widget.setLayout(MENU_layout)
        self.MENU_widget.setStyleSheet("background-color: #7315d1")
        # Container-----------------------------------------------------------------------------------
        self.CONTAINER_label = QLabel('CONTAINER')
        self.CONTAINER_label.setStyleSheet("color: white;")

        self.graphVoltage = graph([
            {
                "color":(0,0,255),
                "name":"Voltage"
            }],True,200,"time in s","V")

        self.graphAltitude = graph([
            {
                "color":(255,255,0),
                "name":"Altitude"
            }],False,20,"","Altitude in m")

        self.map = mapWidget()

        self.graphAxis = graph([
            {
                "color":(255,0,0),
                "name":"xaxis"
            },{
                "color":(0,0,255),
                "name":"yaxis"
            },{
                "color":(255,255,0),
                "name":"zaxis"
            }],True,150)

        CONTAINER_layout = QVBoxLayout()
        CONTAINER_layout.addWidget(self.CONTAINER_label)
        CONTAINER_layout.addWidget(self.graphVoltage.graphWidget)
        CONTAINER_layout.addWidget(self.graphAltitude.graphWidget)
        CONTAINER_layout.addWidget(self.map)
        CONTAINER_layout.addWidget(self.graphAxis.graphWidget)

        self.CONTAINER_widget = QtWidgets.QWidget()
        self.CONTAINER_widget.setLayout(CONTAINER_layout)
        self.CONTAINER_widget.setStyleSheet("""
        .QWidget {
            border: 2px solid white;
            }
        """)

        # Payload -----------------------------------------------------------------------------------
        self.PAYLOAD_label = QLabel('PAYLOAD', self)
        self.PAYLOAD_label.setStyleSheet("color: white;")
        self.graphPressure = graph([
            {
                "color":(0,0,255),
                "name":"Pressure"
            }],True,200,"","Pressure (Pa)")

        self.graphTemprature = graph([
            {
                "color":(255,0,0),
                "name":"Temprature"
            }],False,20,"","C")

        self.graphAxis_dps = graph([
            {
                "color":(255,0,0),
                "name":"xaxis"
            },{
                "color":(0,0,255),
                "name":"yaxis"
            },{
                "color":(255,255,0),
                "name":"zaxis"
            }],True,150)

        self.graphPressure_2 = graph([
            {
                "color":(0,0,255),
                "name":"Pressure"
            }],True,200,"","Pressure (Pa)")

        self.graphTemprature_2 = graph([
            {
                "color":(255,0,0),
                "name":"Temprature"
            }],False,20,"Time in s","C")


        PAYLOAD_layout = QVBoxLayout()
        PAYLOAD_layout.addWidget(self.PAYLOAD_label)
        PAYLOAD_layout.addWidget(self.graphPressure.graphWidget)
        PAYLOAD_layout.addWidget(self.graphTemprature.graphWidget)
        PAYLOAD_layout.addWidget(self.graphAxis_dps.graphWidget)
        PAYLOAD_layout.addWidget(self.graphPressure_2.graphWidget)
        PAYLOAD_layout.addWidget(self.graphTemprature_2.graphWidget)

        self.PAYLOAD_widget = QtWidgets.QWidget()
        self.PAYLOAD_widget.setLayout(PAYLOAD_layout)
        self.PAYLOAD_widget.setStyleSheet("""
        .QWidget {
            border: 2px solid white;
            }
        """)

        #Main layout ----------------------------------------------------------
        MAIN_layout = QHBoxLayout()

        #add widgets
        MAIN_layout.addWidget(self.MENU_widget)
        MAIN_layout.addWidget(self.CONTAINER_widget)
        MAIN_layout.addWidget(self.PAYLOAD_widget)

        self.MAIN_widget = QtWidgets.QWidget()
        self.MAIN_widget.setLayout(MAIN_layout)
        self.MAIN_widget.setStyleSheet("background-color: black")
        self.setCentralWidget(self.MAIN_widget)

        self.timer_n = 0 ;

        self.packet_count = 0
        self.number = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):
        print("wow")
        if self.timer_n%4 == 0 :
            self.map.update(self.number/10+16 , self.number/10 + 78)

            self.graphVoltage.update( self.number, [randint(0,100)])  # Add a new random value.
            self.graphAltitude.update( self.number, [randint(0,100)])  # Add a new random value.
            self.graphAxis.update( self.number, [randint(0,100),randint(0,100),randint(0,100)])  # Add a new random value.

            self.graphPressure.update( self.number, [randint(0,100)])  # Add a new random value.
            self.graphTemprature.update( self.number, [randint(0,100)])  # Add a new random value.
            self.graphAxis_dps.update( self.number, [randint(0,100),randint(0,100),randint(0,100)])  # Add a new random value.
            self.graphPressure_2.update( self.number, [randint(0,100)])  # Add a new random value.
            self.graphTemprature_2.update( self.number, [randint(0,100)])  # Add a new random value.

            self.Packet_count.setText("PACKET COUNT : "+str(self.packet_count))
            self.packet_count += 1
            for label in self.labels :
                label.setStyleSheet("background-color: grey")

            self.labels[self.number%len(self.labels)].setStyleSheet("background-color: red")
            self.number += 1
            self.timer_n = 0

        self.timer_n += 1

    def switch1_toggle(self):
        if self.toggle1 :
            self.toggle1 = False
            print("toggled 1 off")
        else :
            self.toggle1 = True
            print("toggled 1 on")

    def switch2_toggle(self):
        if self.toggle2 :
            self.toggle2 = False
            print("toggled 2 off")
        else :
            self.toggle2 = True
            print("toggled 2 on")

    def start(self):
        print("start")

    def stop(self):
        print("stop")

    def calibrate(self):
        print("calibrate")

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
