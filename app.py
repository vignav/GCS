from PyQt5 import QtWidgets, QtCore
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
from plot import graph

from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QLabel

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("GCS")

        CONTAINER_layout = QVBoxLayout()
        self.CONTAINER_label = QLabel('CONTAINER', self)
        CONTAINER_layout.addWidget(self.CONTAINER_label)
        self.graphVoltage = graph([
            {
                "color":(0,0,255),
                "name":"Voltage"
            }],True,200,"time in s","V")
        CONTAINER_layout.addWidget(self.graphVoltage.graphWidget)

        self.graphAltitude = graph([
            {
                "color":(255,255,0),
                "name":"Altitude"
            }],False,20,"","Altitude in m")
        CONTAINER_layout.addWidget(self.graphAltitude.graphWidget)

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
        CONTAINER_layout.addWidget(self.graphAxis.graphWidget)


        self.CONTAINER_widget = QtWidgets.QWidget()
        self.CONTAINER_widget.setLayout(CONTAINER_layout)

        PAYLOAD_layout = QVBoxLayout()
        self.PAYLOAD_label = QLabel('PAYLOAD', self)
        PAYLOAD_layout.addWidget(self.PAYLOAD_label)
        self.graphPressure = graph([
            {
                "color":(0,0,255),
                "name":"Pressure"
            }],True,200,"","Pressure (Pa)")
        PAYLOAD_layout.addWidget(self.graphPressure.graphWidget)

        self.graphTemprature = graph([
            {
                "color":(255,0,0),
                "name":"Temprature"
            }],False,20,"","C")
        PAYLOAD_layout.addWidget(self.graphTemprature.graphWidget)

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
        PAYLOAD_layout.addWidget(self.graphAxis_dps.graphWidget)

        self.graphPressure_2 = graph([
            {
                "color":(0,0,255),
                "name":"Pressure"
            }],True,200,"","Pressure (Pa)")
        PAYLOAD_layout.addWidget(self.graphPressure_2.graphWidget)

        self.graphTemprature_2 = graph([
            {
                "color":(255,0,0),
                "name":"Temprature"
            }],False,20,"Time in s","C")
        PAYLOAD_layout.addWidget(self.graphTemprature_2.graphWidget)


        self.PAYLOAD_widget = QtWidgets.QWidget()
        self.PAYLOAD_widget.setLayout(PAYLOAD_layout)

        MAIN_layout = QHBoxLayout()
        MAIN_layout.addWidget(self.CONTAINER_widget)
        MAIN_layout.addWidget(self.PAYLOAD_widget)
        self.MAIN_widget = QtWidgets.QWidget()
        self.MAIN_widget.setLayout(MAIN_layout)

        self.MAIN_widget.setBackground((0,0,0))
        self.setCentralWidget(self.MAIN_widget)

        self.number = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):
        self.graphVoltage.update( self.number, [randint(0,100)])  # Add a new random value.
        self.graphAltitude.update( self.number, [randint(0,100)])  # Add a new random value.
        self.graphAxis.update( self.number, [randint(0,100),randint(0,100),randint(0,100)])  # Add a new random value.

        self.graphPressure.update( self.number, [randint(0,100)])  # Add a new random value.
        self.graphTemprature.update( self.number, [randint(0,100)])  # Add a new random value.
        self.graphAxis_dps.update( self.number, [randint(0,100),randint(0,100),randint(0,100)])  # Add a new random value.
        self.graphPressure_2.update( self.number, [randint(0,100)])  # Add a new random value.
        self.graphTemprature_2.update( self.number, [randint(0,100)])  # Add a new random value.
        self.number += 1

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
