from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow


class Ui_MainWindow(object):
    def setup_layouts(self):
        self.central_hlayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.central_hlayout.setObjectName("central_hlayout")

        self.left_vlayout = QtWidgets.QVBoxLayout(
            self.central_widget,
        )
        self.left_vlayout.setObjectName("left_vlayout")
        self.center_vlayout = QtWidgets.QVBoxLayout(self.central_widget)
        self.center_vlayout.setObjectName("center_vlayout")
        self.right_vlayout = QtWidgets.QVBoxLayout(self.central_widget)
        self.right_vlayout.setObjectName("right_vlayout")
        self.left_vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.right_vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.central_hlayout.addLayout(self.left_vlayout)
        self.central_hlayout.addLayout(self.center_vlayout)
        self.central_hlayout.addLayout(self.right_vlayout)

    def setup_video_ctrl(self):
        self.video_ctrl_hlayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.video_ctrl_hlayout.setObjectName("video_ctrl_hlayout")
        self.video_ctrl_hlayout
        self.center_vlayout.addLayout(self.video_ctrl_hlayout)

        self.previous_frame = QtWidgets.QPushButton("⏮️", self.central_widget)
        self.previous_frame.setObjectName("previous_frame")
        self.previous_frame.setFixedSize(QtCore.QSize(32, 32))
        self.video_ctrl_hlayout.addWidget(self.previous_frame)

        self.play = QtWidgets.QPushButton("▶️", self.central_widget)
        self.play.setObjectName("play")
        self.play.setFixedSize(QtCore.QSize(32, 32))
        self.video_ctrl_hlayout.addWidget(self.play)

        self.next_frame = QtWidgets.QPushButton("⏭️", self.central_widget)
        self.next_frame.setObjectName("next_frame")
        self.next_frame.setFixedSize(QtCore.QSize(32, 32))
        self.video_ctrl_hlayout.addWidget(self.next_frame)

        self.clear = QtWidgets.QPushButton("Clear", self.central_widget)
        self.clear.setObjectName("clear")
        self.clear.setFixedSize(QtCore.QSize(64, 32))
        self.video_ctrl_hlayout.addWidget(self.clear)

        self.is_key_frame = QtWidgets.QPushButton("Key", self.central_widget)
        self.is_key_frame.setObjectName("is_key_frame")
        self.is_key_frame.setFixedSize(QtCore.QSize(64, 32))
        self.video_ctrl_hlayout.addWidget(self.is_key_frame)

        self.run = QtWidgets.QPushButton("Run", self.central_widget)
        self.run.setObjectName("run")
        self.run.setFixedSize(QtCore.QSize(64, 32))
        self.video_ctrl_hlayout.addWidget(self.run)

        self.video_ctrl_hlayout.addStretch()

        self.zoomin = QtWidgets.QPushButton("+", self.central_widget)
        self.zoomin.setObjectName("zoomin")
        self.zoomin.setFixedSize(QtCore.QSize(32, 32))
        self.video_ctrl_hlayout.addWidget(self.zoomin)

        self.zoomout = QtWidgets.QPushButton("-", self.central_widget)
        self.zoomout.setObjectName("zoomin")
        self.zoomout.setFixedSize(QtCore.QSize(32, 32))
        self.video_ctrl_hlayout.addWidget(self.zoomout)

    def setup_image_frame(self):
        self.image_frame = QtWidgets.QLabel("image", self.central_widget)
        self.image_frame.setObjectName("image_frame")
        self.center_vlayout.addWidget(self.image_frame)
        self.image_frame.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

    def setup_menu(self):
        self.menu = self.MainWindow.menuBar()
        self.file_menu = self.menu.addMenu("&File")
        self.file_toolbar = QtWidgets.QToolBar("File toolbar")
        self.file_toolbar.hide()
        self.MainWindow.addToolBar(self.file_toolbar)

        self.open_video_button = QtGui.QAction("Open Video", self.MainWindow)
        self.file_toolbar.addAction(self.open_video_button)
        self.file_menu.addAction(self.open_video_button)

        self.file_menu.addSeparator()

    def setup_toolbar(self):
        self.empty1 = QtWidgets.QLabel("", self.central_widget)
        self.empty1.setObjectName("empty1")
        self.empty1.setFixedSize(QtCore.QSize(32, 32))
        self.left_vlayout.addWidget(self.empty1)

        self.move_tool = QtWidgets.QPushButton("M", self.central_widget)
        self.move_tool.setObjectName("move_tool")
        self.move_tool.setFixedSize(QtCore.QSize(32, 32))
        self.left_vlayout.addWidget(self.move_tool)

        self.pencil_tool = QtWidgets.QPushButton("P", self.central_widget)
        self.pencil_tool.setObjectName("pencil_tool")
        self.pencil_tool.setFixedSize(QtCore.QSize(32, 32))
        self.left_vlayout.addWidget(self.pencil_tool)

        self.polygon_tool = QtWidgets.QPushButton("Po", self.central_widget)
        self.polygon_tool.setObjectName("polygon_tool")
        self.polygon_tool.setFixedSize(QtCore.QSize(32, 32))
        self.left_vlayout.addWidget(self.polygon_tool)

    def setup_toolbar2(self):
        self.l3 = QtWidgets.QLabel("", self.central_widget)
        self.l3.setObjectName("test")
        self.l3.setFixedSize(150, 32)
        self.right_vlayout.addWidget(self.l3)

        self.tool_size_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # tool size

        self.tool_size_dec = QtWidgets.QPushButton("-", self.central_widget)
        self.tool_size_dec.setObjectName("tool_size_dec")
        self.tool_size_dec.setFixedSize(QtCore.QSize(32, 32))
        self.tool_size_layout.addWidget(self.tool_size_dec)

        self.tool_size = QtWidgets.QLabel(f"Tool size: {1} px", self.central_widget)
        self.tool_size.setObjectName("tool_size_label")
        self.tool_size.setFixedWidth(100)
        self.tool_size_layout.addWidget(self.tool_size)

        self.tool_size_inc = QtWidgets.QPushButton("+", self.central_widget)
        self.tool_size_inc.setObjectName("tool_size_inc")
        self.tool_size_inc.setFixedSize(QtCore.QSize(32, 32))
        self.tool_size_layout.addWidget(self.tool_size_inc)

        self.alpha_layout = QtWidgets.QHBoxLayout(self.central_widget)

        self.alpha_dec = QtWidgets.QPushButton("-", self.central_widget)
        self.alpha_dec.setObjectName("alpha_dec")
        self.alpha_dec.setFixedSize(QtCore.QSize(32, 32))
        self.alpha_layout.addWidget(self.alpha_dec)

        self.alpha = QtWidgets.QLabel(f"Alpha: {50} %", self.central_widget)
        self.alpha.setObjectName("alpha")
        self.alpha.setFixedWidth(100)
        self.alpha_layout.addWidget(self.alpha)

        self.alpha_inc = QtWidgets.QPushButton("+", self.central_widget)
        self.alpha_inc.setObjectName("alpha_inc")
        self.alpha_inc.setFixedSize(QtCore.QSize(32, 32))
        self.alpha_layout.addWidget(self.alpha_inc)

        self.label0 = QtWidgets.QPushButton("Label 0", self.central_widget)
        self.label0.setStyleSheet("padding: 4px;")
        self.label1 = QtWidgets.QPushButton("Label 1", self.central_widget)
        self.label1.setStyleSheet("padding: 4px;")
        self.label2 = QtWidgets.QPushButton("Label 2", self.central_widget)
        self.label2.setStyleSheet("padding: 4px;")

        self.right_vlayout.addLayout(self.tool_size_layout)
        self.right_vlayout.addLayout(self.alpha_layout)
        self.right_vlayout.addWidget(self.label0)
        self.right_vlayout.addWidget(self.label1)
        self.right_vlayout.addWidget(self.label2)

        self.right_vlayout.addStretch()

        self.pbar = QtWidgets.QProgressBar(self.central_widget)
        self.pbar.setObjectName("pbar")
        self.pbar.setFixedSize(QtCore.QSize(140, 24))
        self.pbar.setValue(0)
        self.right_vlayout.addWidget(self.pbar)

    def setupUi(self, MainWindow: QMainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(900, 560)
        self.MainWindow.setMinimumSize(800, 400)
        self.central_widget = QtWidgets.QWidget(self.MainWindow)
        self.central_widget.setObjectName("central_widget")

        self.setup_layouts()
        self.setup_video_ctrl()
        self.setup_image_frame()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_toolbar2()

        MainWindow.setCentralWidget(self.central_widget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
