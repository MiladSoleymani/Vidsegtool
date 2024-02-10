from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow
import os
import numpy as np
from typing import TYPE_CHECKING
import cv2
if TYPE_CHECKING:
    from views.run_view import RunView


class AlgorithmsEnum:
    OPTICAL_FLOW = "Optical Flow"
    OSVOS = "OSVOS"


class Ui_RunWindow(object):
    def setup_top_layout(self):
        self.top_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.layout.addLayout(self.top_layout)

        self.generate_algo = QtWidgets.QComboBox(self.central_widget)
        self.generate_algo.setObjectName("generate_algo")
        self.generate_algo.addItems(['-', AlgorithmsEnum.OPTICAL_FLOW, AlgorithmsEnum.OSVOS])
        self.top_layout.addWidget(self.generate_algo)

        self.run_button = QtWidgets.QPushButton("Run", self.central_widget)
        self.run_button.setFixedSize(QtCore.QSize(64, 24))
        self.run_button.setEnabled(False)
        self.top_layout.addWidget(self.run_button)

        self.pbar = QtWidgets.QProgressBar(self.central_widget)
        self.pbar.setObjectName("pbar")
        self.pbar.setValue(0)
        self.top_layout.addWidget(self.pbar)
    
    def setup_scroll(self):
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        self.content_widget = QtWidgets.QWidget(self.central_widget)
        self.content_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.content_widget.setLayout(self.content_layout)

        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.content_widget)
        self.layout.addWidget(self.scrollArea)


        video_data = self.MainWindow._model.video_data
        self.frames = []
        for i in range(len(video_data)):
            frame = QtWidgets.QLabel(f"frame_{i}", self.central_widget)
            frame.setObjectName("object")
            self.frames.append(frame)
            self.content_layout.addWidget(frame)


    def setupUi(self, MainWindow: "RunView"):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("abc")
        self.MainWindow.setFixedSize(850, 230)
        self.central_widget = QtWidgets.QWidget(self.MainWindow)
        self.central_widget.setObjectName("central_widget")

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.setup_top_layout()
        self.layout.addStretch()
        self.layout.addStretch()
        self.setup_scroll()

        MainWindow.setCentralWidget(self.central_widget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
