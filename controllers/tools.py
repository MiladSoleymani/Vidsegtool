from typing import TYPE_CHECKING
import numpy as np
from PyQt6 import QtCore
import cv2

if TYPE_CHECKING:
    from models.model import Model
    from views.main_view import MainView

class Tool:
    name: str | None = None
    def __init__(self, model: "Model") -> None:
        self._model = model

    def mouse_press(self, event):
        pass

    def mouse_move(self, event):
        pass

class NoneTool(Tool):
    name = ""
    pass

class MoveTool(Tool):
    name = "move_tool"

    def mouse_press(self, event):
        y, x = event.pos().y(), event.pos().x()
        self._mouse_press_coordinates = (y, x)
        self._temp_coordinates = self._model.coordinates
        
    def mouse_move(self, event):
        y, x = event.pos().y(), event.pos().x()
        y0, x0 = self._mouse_press_coordinates
        y_temp, x_temp = self._temp_coordinates

        zoom_ratio = self._model.zoom_ratio if self._model.zoom_ratio > 0 else -1 / self._model.zoom_ratio
        new_move_y = (y - y0) / zoom_ratio
        new_move_x = (x - x0) / zoom_ratio
        self._model.coordinates = (y_temp + new_move_y, x_temp + new_move_x)


class PencilTool(Tool):
    name = "pencil_tool"

    def mouse_press(self, event):
        y, x = event.pos().y(), event.pos().x()
        self.temp_coordinates = (y, x)
        self.mouse_move(event)

    def mouse_move(self, event):
        y_temp, x_temp = self.temp_coordinates
        selected_label = self._model.selected_label

        y, x = event.pos().y(), event.pos().x()
        self.temp_coordinates = (y, x)

        frame_num = self._model.frame_num
        video_label = self._model.video_label

        y_t, x_t = self._model.top_left_image_coordinates
        zoom_ratio = self._model.zoom_ratio if self._model.zoom_ratio > 0 else -1 / self._model.zoom_ratio
        x = int((x - x_t) / zoom_ratio)
        y = int((y - y_t) / zoom_ratio)
        x_temp = int((x_temp - x_t) / zoom_ratio)
        y_temp = int((y_temp - y_t) / zoom_ratio)

        
        def fx(_x):
            m = (y_temp - y) / (x_temp - x)
            return round(m * (_x - x) + y) 
        def fy(_y):
            m = (x_temp - x) / (y_temp - y)
            return round(m * (_y - y) + x) 
        
        idx = []
        if x != x_temp or y != y_temp:
            if abs(x_temp - x) >= abs(y_temp - y):
                idx += [(frame_num, fx(xi), xi ) for xi in range(min(x_temp, x) + 1, max(x_temp, x))]
            else:
                idx += [(frame_num, yi, fy(yi) ) for yi in range(min(y_temp, y) + 1, max(y_temp, y))]

        tool_size = self._model.tool_size
        tool_size_r = (tool_size + 1) // 2
        tool_size_l = tool_size // 2
        idx.append((frame_num, y, x))
        idx.append((frame_num, y_temp, x_temp))

        idx = [(f, yi + j, xi + i) for f, yi, xi in idx for i in range(- tool_size_l, tool_size_r) for j in range(-tool_size_l, tool_size_r)]

        idx = list({(f, yi, xi) for f, yi, xi in set(idx) if 0 <= yi < video_label.shape[1] and 0 <= xi < video_label.shape[2]})
        if idx:
            video_label[tuple(np.transpose(idx))] = selected_label
            self._model.video_label = video_label

class PolygonTool(Tool):
    name = "polygon_tool"
    def mouse_press(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            y, x = event.pos().y(), event.pos().x()
            if not hasattr(self, "points"):
                self.points = []

            y_t, x_t = self._model.top_left_image_coordinates
            zoom_ratio = self._model.zoom_ratio if self._model.zoom_ratio > 0 else -1 / self._model.zoom_ratio
            x = int((x - x_t) / zoom_ratio)
            y = int((y - y_t) / zoom_ratio)
            self.points.append((y, x))

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if hasattr(self, "points"):
                points = [(int(x), int(y)) for y, x in self.points]
                selected_label = self._model.selected_label

                if points:
                    frame_num = self._model.frame_num
                    video_polygon_label = self._model.video_polygon_label
                    if frame_num not in video_polygon_label:
                        video_polygon_label[frame_num] = {}
                    if selected_label not in video_polygon_label[frame_num]:
                        video_polygon_label[frame_num][selected_label] = []
                    
                    video_polygon_label[frame_num][selected_label].append(points)
                    video_polygon_label[-1] = {}

                    self._model.video_polygon_label = video_polygon_label

                del self.points
    
    def mouse_move(self, event):
        if not hasattr(self, "points"):
            self.points = []
        y, x = event.pos().y(), event.pos().x()

        y_t, x_t = self._model.top_left_image_coordinates
        zoom_ratio = self._model.zoom_ratio if self._model.zoom_ratio > 0 else -1 / self._model.zoom_ratio
        x = int((x - x_t) / zoom_ratio)
        y = int((y - y_t) / zoom_ratio)

        points = self.points + [(y, x)]
        selected_label = self._model.selected_label

        points = [(int(x), int(y)) for y, x in points]
        video_polygon_label = self._model.video_polygon_label
        if -1 not in video_polygon_label:
            video_polygon_label[-1] = {}
        if 1 not in video_polygon_label[-1]:
            video_polygon_label[-1][selected_label] = []
        video_polygon_label[-1][selected_label] = [points]
        self._model.video_polygon_label = video_polygon_label

class Tools:
    NONE = NoneTool
    MOVE = MoveTool
    PENCIL = PencilTool
