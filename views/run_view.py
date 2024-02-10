from PyQt6 import QtWidgets, QtCore, QtGui
from views.run_view_ui import Ui_RunWindow, AlgorithmsEnum
import cv2
import numpy as np
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from controllers.main_ctrl import MainController
    from models.model import Model

class RunView(QtWidgets.QMainWindow):
    def __init__(self, model: "Model", main_controller: "MainController"):
        super().__init__()
        self.is_open = True # handle a bug

        self._model = model
        self._main_controller = main_controller

        self._ui = Ui_RunWindow()
        self._ui.setupUi(self)

        self._model.run__selected_frames = set()

        key_frames = self._model.key_frames
        for i, frame in enumerate(self._ui.frames):
            self.apply_frame(frame, i)
            if i not in key_frames:
                frame.mousePressEvent = lambda e, i=i: self._main_controller.on_frame_clicked(i)
        
        self._model.run__selected_frames_changed.connect(self.on_run__selected_frames_changed)
        self._ui.generate_algo.currentTextChanged.connect(self.validate_run_button)
        self._ui.run_button.clicked.connect(self.on_run_button_clicked)

    def apply_frame(self, frame_obj, i):
        v = self._model.video_data[i]
        v = cv2.resize(v.astype(np.uint8), (128, 128))
        key_frames = self._model.key_frames
        selected_frames = self._model.run__selected_frames
        if i in key_frames:
            cv2.rectangle(v, (0, 0), (128,128), (0, 255, 0), 8)
        elif i in selected_frames:
            cv2.rectangle(v, (0, 0), (128,128), (0, 0, 255), 8)
        height = v.shape[0]
        total_bytes = v.nbytes
        bytes_per_line = int(total_bytes/height)
        qimage = QtGui.QImage(v, v.shape[1], v.shape[0], bytes_per_line, QtGui.QImage.Format.Format_RGB888).rgbSwapped()
        frame_obj.setPixmap(QtGui.QPixmap.fromImage(qimage))

    @QtCore.pyqtSlot(set)
    def on_run__selected_frames_changed(self):
        for i, frame in enumerate(self._ui.frames):
            self.apply_frame(frame, i)
        self.validate_run_button()

    def validate_run_button(self):
        algo = self._ui.generate_algo.currentText()
        key_frames = self._model.key_frames
        selected_frames = self._model.run__selected_frames

        valid = False
        if algo == AlgorithmsEnum.OPTICAL_FLOW:
            valid = bool(selected_frames)
            valid_frames = set()
            for f in sorted(selected_frames):
                if f-1 in key_frames or f-1 in valid_frames:
                    valid_frames.add(f)
                else:
                    valid = False
                    break
        elif algo == AlgorithmsEnum.OSVOS:
            valid = bool(selected_frames) and bool(key_frames)

        self._ui.run_button.setEnabled(valid)

    def on_run_button_clicked(self):
        algo = self._ui.generate_algo.currentText()
        pbar = self._ui.pbar

        if algo == AlgorithmsEnum.OPTICAL_FLOW:
            self._main_controller.run_optical_flow(pbar)
        elif algo == AlgorithmsEnum.OSVOS:
            self._main_controller.run_osvos(pbar)
        
        time.sleep(1)
        self.close()
