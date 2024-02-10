from PyQt6 import QtCore
import numpy as np
from dataclasses import dataclass

class MouseMode:
        NONE = "none"
        MOVE = "move"
        PENCIL = "pencil"

@dataclass
class RenderData:
    initial_image: np.ndarray | None = None
    initial_label: np.ndarray | None = None

    zoomed_image: np.ndarray | None = None
    zoomed_label: np.ndarray | None = None

    moved_image: np.ndarray | None = None
    moved_label: np.ndarray | None = None

    initial_image_frame: np.ndarray | None = None
    initial_image_frame2: np.ndarray | None = None
    image_frame: np.ndarray | None = None

class Model(QtCore.QObject):
    render_data = RenderData()
    video_url = None
    video_data = None

    key_frames_changed = QtCore.pyqtSignal(set)
    image_frame_changed = QtCore.pyqtSignal(np.ndarray)
    frame_num_changed = QtCore.pyqtSignal(int)
    zoom_ratio_changed = QtCore.pyqtSignal(int)
    coordinates_changed = QtCore.pyqtSignal(tuple)
    video_label_changed = QtCore.pyqtSignal(np.ndarray)
    video_polygon_label_changed = QtCore.pyqtSignal(dict)
    tool_name_changed = QtCore.pyqtSignal(str)
    tool_size_changed = QtCore.pyqtSignal(int)
    alpha_changed = QtCore.pyqtSignal(int)
    selected_label_changed = QtCore.pyqtSignal(int)

    # RUN
    run__selected_frames_changed = QtCore.pyqtSignal(set)

    @property
    def run__selected_frames(self):
        return self._run__selected_frames
    
    @run__selected_frames.setter
    def run__selected_frames(self, value):
        self._run__selected_frames = value
        self.run__selected_frames_changed.emit(value)

    @property
    def key_frames(self):
        return self._key_frames
    
    @key_frames.setter
    def key_frames(self, value):
        self._key_frames = value
        self.key_frames_changed.emit(value)

    @property
    def video_label(self):
        return self._video_label
    
    @video_label.setter
    def video_label(self, value):
        self._video_label = value
        self.video_label_changed.emit(value)
    
    @property
    def video_polygon_label(self):
        # dict[<frame num>, dict[<label num>: list[<polygon>]]]
        return self._video_polygon_label

    @video_polygon_label.setter
    def video_polygon_label(self, value):
        self._video_polygon_label = value
        self.video_polygon_label_changed.emit(value)

    @property
    def image_frame(self):
        return self._image_frame
    
    @image_frame.setter
    def image_frame(self, value):
        self._image_frame = value
        self.image_frame_changed.emit(value)
    
    @property
    def frame_num(self):
        return self._frame_num
    
    @frame_num.setter
    def frame_num(self, value):
        self._frame_num = value
        self.frame_num_changed.emit(value)
    
    @property
    def zoom_ratio(self):
        return self._zoom_ratio
    
    @zoom_ratio.setter
    def zoom_ratio(self, value):
        self._zoom_ratio = value
        self.zoom_ratio_changed.emit(value)
    
    @property
    def coordinates(self):
        return self._coordinates
    
    @coordinates.setter
    def coordinates(self, value):
        self._coordinates = value
        self.coordinates_changed.emit(value)
    
    @property
    def tool_name(self):
        return self._tool_name
    
    @tool_name.setter
    def tool_name(self, value):
        self._tool_name = value
        self.tool_name_changed.emit(value)
    
    @property
    def tool_size(self):
        return self._tool_size
    
    @tool_size.setter
    def tool_size(self, value):
        self._tool_size = value
        self.tool_size_changed.emit(value)
    
    @property
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        self.alpha_changed.emit(value)
    
    @property
    def selected_label(self):
        return self._selected_label
    
    @selected_label.setter
    def selected_label(self, value):
        self._selected_label = value
        self.selected_label_changed.emit(value)

    def __init__(self):
        super().__init__()
        self._image_frame = np.zeros((1, 1, 3))
        self._key_frames = set()
        self._alpha = 50
        self._video_polygon_label = dict()
