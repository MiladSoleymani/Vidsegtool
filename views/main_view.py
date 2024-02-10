from PyQt6 import QtWidgets, QtCore, QtGui
from views.main_view_ui import Ui_MainWindow
import numpy as np
from views.run_view import RunView
from controllers.render import RenderInput
import controllers.tools as tools 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.main_ctrl import MainController
    from models.model import Model

class MainView(QtWidgets.QMainWindow):
    def __init__(self, model: "Model", main_controller: "MainController"):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._main_controller.set_view(self)

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # connect widgets to controller
        self._ui.open_video_button.triggered.connect(self._main_controller.open_video)

        self._ui.run.clicked.connect(self.open_runview)

        self._ui.next_frame.clicked.connect(self._main_controller.next_frame)
        self._ui.previous_frame.clicked.connect(self._main_controller.previous_frame)
        self._ui.zoomin.clicked.connect(self._main_controller.zoomin)
        self._ui.zoomout.clicked.connect(self._main_controller.zoomout)

        self._ui.move_tool.clicked.connect(lambda: self._main_controller.change_tool(tools.MoveTool))
        self._ui.pencil_tool.clicked.connect(lambda: self._main_controller.change_tool(tools.PencilTool))
        self._ui.polygon_tool.clicked.connect(lambda: self._main_controller.change_tool(tools.PolygonTool))

        self._ui.tool_size_inc.clicked.connect(lambda: self._main_controller.change_tool_size(True))
        self._ui.tool_size_dec.clicked.connect(lambda: self._main_controller.change_tool_size(False))

        self._ui.alpha_inc.clicked.connect(lambda: self._main_controller.change_alpha(True))
        self._ui.alpha_dec.clicked.connect(lambda: self._main_controller.change_alpha(False))

        self._ui.is_key_frame.clicked.connect(self._main_controller.change_key_frame)
        self._ui.clear.clicked.connect(self._main_controller.clear_frame)

        self._ui.image_frame.mousePressEvent = self._main_controller.image_frame_mouse_press_event
        self._ui.image_frame.mouseMoveEvent = self._main_controller.image_frame_mouse_move_event

        self._ui.label0.clicked.connect(lambda: self._main_controller.change_label(0))
        self._ui.label1.clicked.connect(lambda: self._main_controller.change_label(1))
        self._ui.label2.clicked.connect(lambda: self._main_controller.change_label(2))

        # listen for model event signals
        self._model.image_frame_changed.connect(self.on_image_frame_changed)
        self._model.frame_num_changed.connect(self.on_frame_num_changed)
        self._model.zoom_ratio_changed.connect(self.on_zoom_ratio_changed)
        self._model.tool_name_changed.connect(self.on_tool_name_changed)
        self._model.tool_size_changed.connect(self.on_tool_size_changed)
        self._model.key_frames_changed.connect(self.on_key_frames_changed)
        self._model.alpha_changed.connect(self.on_alpha_changed)
        self._model.selected_label_changed.connect(self.on_selected_label_changed)

        # defaults TODO: make better
        video_data = np.array([[[[i, 255 - (i + j) // 2, j ] for i in range(0, 255)] for j in range(0, 255)]]) # FUN
        self._model.video_label = np.zeros((video_data.shape[0], video_data.shape[1], video_data.shape[2]))
        self._model.video_data = video_data
        self._model.frame_num = 0
        self._model.zoom_ratio = 1
        self._model.coordinates = (0, 0)
        self._model.tool_name = ""
        self._model.tool_size = 1
        self._model.key_frames = set()
        self._model.selected_label = 0

        # connect model to controller
        self._main_controller.render([RenderInput.ROOT])
        self._model.frame_num_changed.connect(lambda: self._main_controller.render([RenderInput.ROOT]))
        self._model.zoom_ratio_changed.connect(lambda: self._main_controller.render([RenderInput.IMAGE_ZOOM, RenderInput.LABEL_ZOOM]))
        self._model.coordinates_changed.connect(lambda: self._main_controller.render([RenderInput.IMAGE_MOVE_AND_APPLY, RenderInput.LABEL_MOVE_AND_APPLY]))
        self._model.video_label_changed.connect(lambda: self._main_controller.render([RenderInput.LABEL_INITIAL]))
        self._model.video_polygon_label_changed.connect(lambda: self._main_controller.render([RenderInput.LABEL_ZOOM]))

        # defaults TODO: make better
        self._model.alpha = 50

    @QtCore.pyqtSlot(set)
    def on_key_frames_changed(self, key_frames: set):
        if self._model.frame_num in key_frames:
            self._ui.is_key_frame.setStyleSheet("background: #27ae60; border-radius:5px; color: #ecf0f1")
        else:
            self._ui.is_key_frame.setStyleSheet("background: #e74c3c; border-radius:5px; color: #ecf0f1")

    @QtCore.pyqtSlot(np.ndarray)
    def on_image_frame_changed(self, value: np.ndarray):
        height = value.shape[0]
        total_bytes = value.nbytes
        bytes_per_line = int(total_bytes/height)
        qimage = QtGui.QImage(value.data, value.shape[1], value.shape[0], bytes_per_line, QtGui.QImage.Format.Format_RGB888).rgbSwapped()
        self._ui.image_frame.setPixmap(QtGui.QPixmap.fromImage(qimage))

    @QtCore.pyqtSlot(int)
    def on_frame_num_changed(self, frame_num: int):
        max_frame_num = self._model.video_data.shape[0] - 1
        self._ui.previous_frame.setEnabled(frame_num > 0)
        self._ui.next_frame.setEnabled(frame_num < max_frame_num)
        self.on_key_frames_changed(self._model.key_frames)

    @QtCore.pyqtSlot(int)
    def on_zoom_ratio_changed(self, zoom_ratio: int):
        self._ui.zoomin.setEnabled(zoom_ratio < 10)
        self._ui.zoomout.setEnabled(zoom_ratio > -10)

    @QtCore.pyqtSlot(str)
    def on_tool_name_changed(self, tool_name: str):
        ui_tools = [
            self._ui.move_tool,
            self._ui.pencil_tool,
            self._ui.polygon_tool,
        ]
        for ui_tool in ui_tools:
            if ui_tool.objectName() == tool_name:
                ui_tool.setStyleSheet("background: #03c2fc; border-radius:10px;")
            else:
                ui_tool.setStyleSheet("")
        
        if tool_name == self._ui.polygon_tool.objectName():
            self._ui.image_frame.setMouseTracking(True)
        else:
            self._ui.image_frame.setMouseTracking(False)

    
    @QtCore.pyqtSlot(int)
    def on_tool_size_changed(self, tool_size: int):
        self._ui.tool_size.setText(f"Tool size: {tool_size}")
    
    @QtCore.pyqtSlot(int)
    def on_alpha_changed(self, alpha: int):
        self._ui.alpha.setText(f"Alpha: {alpha} %")
        self._main_controller.render([RenderInput.LABEL_MOVE_AND_APPLY])
    
    @QtCore.pyqtSlot(int)
    def on_selected_label_changed(self, new_label: int):
        self._ui.label1.setStyleSheet("padding: 4px;")
        self._ui.label2.setStyleSheet("padding: 4px;")
        if new_label == 1:
            self._ui.label1.setStyleSheet("background: #f00; border-radius:10px; padding: 4px;")
        if new_label == 2:
            self._ui.label2.setStyleSheet("background: #0f0; border-radius:10px; padding: 4px;")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._main_controller.render([RenderInput.IMAGE_FRAME_INITIAL])
    
    def open_runview(self):
        _open_view = RunView(self._model, self._main_controller)
        _open_view.show()
