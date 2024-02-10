import importlib
import math
from collections import defaultdict
from typing import TYPE_CHECKING

import cv2
import numpy as np
from PyQt6 import QtCore, QtWidgets

from controllers.render import Render
from controllers.tools import NoneTool, Tool

if TYPE_CHECKING:
    from models.model import Model
    from views.main_view import MainView


class MainController(QtCore.QObject):
    def __init__(self, model: "Model"):
        super().__init__()
        self._model = model
        self._tool: Tool = NoneTool(model)

    def set_view(self, view: "MainView"):
        self.view = view
        self._render = Render(self._model, self.view)

    def render(self, inputs):
        self._render(inputs)

    def open_video(self, fname):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.view._ui.central_widget, "Open Video", QtCore.QDir.homePath(), "Videos files (*.mp4)"
        )

        if fname:
            cap = cv2.VideoCapture(fname)
            if cap.isOpened() == False:
                print("Error opening video stream or file")
                return

            frames = []
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            frames = np.array(frames)
            label = np.zeros((frames.shape[0], frames.shape[1], frames.shape[2]))
            self._model.video_label = label
            self._model.video_polygon_label = dict()
            self._model.video_data = frames
            self._model.video_url = fname
            self._model.frame_num = 0
            self._model.key_frames = set()

    def next_frame(self):
        max_frame_num = self._model.video_data.shape[0]
        self._model.frame_num = min(self._model.frame_num + 1, max_frame_num)

    def previous_frame(self):
        self._model.frame_num = max(self._model.frame_num - 1, 0)

    def zoomin(self):
        if self._model.zoom_ratio in {0, -1}:
            self._model.zoom_ratio = min(2, 10)
        else:
            self._model.zoom_ratio = min(self._model.zoom_ratio + 1, 10)

    def zoomout(self):
        if self._model.zoom_ratio in {0, 1}:
            self._model.zoom_ratio = max(-2, -10)
        else:
            self._model.zoom_ratio = max(self._model.zoom_ratio - 1, -10)

    def image_frame_mouse_press_event(self, event):
        self._tool.mouse_press(event)

    def image_frame_mouse_move_event(self, event):
        self._tool.mouse_move(event)

    def change_tool(self, tool_class):
        if self._tool.__class__ == tool_class:
            tool_class = NoneTool
        self._tool: Tool = tool_class(self._model)
        self._model.tool_name = self._tool.name

        video_polygon_label = self._model.video_polygon_label
        video_polygon_label[-1] = {}
        self._model.video_polygon_label = video_polygon_label

    def change_tool_size(self, inc: bool):
        tool_size = self._model.tool_size
        tool_size = tool_size + 1 if inc else tool_size - 1
        self._model.tool_size = min(max(tool_size, 1), 50)

    def change_key_frame(self):
        frame_num = self._model.frame_num
        key_frames: set = self._model.key_frames
        if frame_num in key_frames:
            key_frames.remove(frame_num)
        else:
            key_frames.add(frame_num)

        self._model.key_frames = key_frames

    def clear_frame(self):
        frame_num = self._model.frame_num
        video_polygon_label = self._model.video_polygon_label
        video_label = self._model.video_label

        video_polygon_label.pop(frame_num, None)
        video_label[frame_num] = 0

        self._model.video_polygon_label = video_polygon_label
        self._model.video_label = video_label

    def change_alpha(self, inc: bool):
        alpha = self._model.alpha
        alpha = alpha + 10 if inc else alpha - 10
        self._model.alpha = min(max(alpha, 0), 100)

    def run(self, pbar):
        key_frames: set = self._model.key_frames
        video_data: np.ndarray = self._model.video_data
        video_label: np.ndarray = self._model.video_label
        video_polygon_label: dict = self._model.video_polygon_label
        flow: np.ndarray = self._model.flow

        len_video_data = len(video_data)

        pbar.setValue(0)
        assert 0 in key_frames
        for frame_num in range(1, len_video_data):
            if frame_num == 20:
                break
            if frame_num in key_frames:
                continue

            prev_label = video_label[frame_num - 1]
            prev_label_polys = video_polygon_label.get(frame_num - 1, {}).items()

            label_polygons = list(sorted(prev_label_polys, key=lambda x: x[0]))
            for label, polygons in label_polygons:
                for polygon in polygons:
                    cv2.fillPoly(prev_label, pts=[np.array(polygon, dtype=np.int32)], color=label)

            f = flow[frame_num - 1]

            current_label = np.zeros_like(prev_label)
            prev_xs = []
            prev_ys = []
            curr_xs = []
            curr_ys = []
            w, h = current_label.shape

            for i in range(w):
                for j in range(h):
                    fj, fi = f[i, j]
                    fj, fi = round(fj), round(fi)

                    prev_xs.append(min(w - 1, max(0, i + fi)))
                    prev_ys.append(min(h - 1, max(0, j + fj)))
                    curr_xs.append(i)
                    curr_ys.append(j)
            current_label[curr_xs, curr_ys] = prev_label[prev_xs, prev_ys]

            video_label[frame_num] = current_label
            video_polygon_label[frame_num] = {}

            pbar.setValue(math.ceil(frame_num / len_video_data * 100))

        self._model.video_label = video_label
        self._model.video_polygon_label = video_polygon_label

    def change_label(self, new_label):
        self._model.selected_label = new_label

    #### RUN

    def on_frame_clicked(self, i):
        selected_frames: set = self._model.run__selected_frames
        if i in selected_frames:
            selected_frames.remove(i)
        else:
            selected_frames.add(i)

        self._model.run__selected_frames = selected_frames

    def apply_poly(self, prev_label, prev_polygon_label):
        prev_label = prev_label.copy()
        prev_polygon_label = list(sorted(prev_polygon_label.items(), key=lambda x: x[0]))
        for label, polygons in prev_polygon_label:
            for polygon in polygons:
                cv2.fillPoly(prev_label, pts=[np.array(polygon, dtype=np.int32)], color=label)
        return prev_label

    def run_optical_flow(self, pbar):
        pbar.setValue(0)
        selected_frames = self._model.run__selected_frames

        video_data = self._model.video_data
        video_label = self._model.video_label
        video_polygon_label = self._model.video_polygon_label

        pbar_len = len(selected_frames)

        for pbar_i, curr_i in enumerate(sorted(selected_frames)):
            curr_img = video_data[curr_i]
            prev_img = video_data[curr_i - 1]
            prev_label = self.apply_poly(video_label[curr_i - 1], video_polygon_label.get(curr_i - 1, {}))

            flow = cv2.calcOpticalFlowFarneback(
                cv2.cvtColor(curr_img, cv2.COLOR_BGR2GRAY),
                cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY),
                None,
                0.5,
                3,
                15,
                3,
                5,
                1.2,
                0,
            )

            current_label = np.zeros_like(prev_label)
            prev_xs, prev_ys, curr_xs, curr_ys = [], [], [], []
            w, h = current_label.shape

            for i in range(w):
                for j in range(h):
                    fj, fi = flow[i, j]
                    fj, fi = round(fj), round(fi)

                    prev_xs.append(min(w - 1, max(0, i + fi)))
                    prev_ys.append(min(h - 1, max(0, j + fj)))
                    curr_xs.append(i)
                    curr_ys.append(j)
            current_label[curr_xs, curr_ys] = prev_label[prev_xs, prev_ys]

            video_label[curr_i] = current_label
            video_polygon_label[curr_i] = {}

            pbar.setValue(int((pbar_i + 1) / pbar_len * 100))

        self._model.video_label = video_label
        self._model.video_polygon_label = video_polygon_label

    def run_osvos(self, pbar):
        import osvos.main as osvos_model

        pbar.setValue(0)
        key_frames = self._model.key_frames
        selected_frames = self._model.run__selected_frames

        print(key_frames, selected_frames)

        video_data = self._model.video_data
        video_label = self._model.video_label
        video_polygon_label = self._model.video_polygon_label

        sorted_key_frames = list(sorted(key_frames))
        key_i = sorted_key_frames[-1]
        selected_frames_by_key_frame = defaultdict(list)
        for curr_i in sorted(selected_frames, reverse=True):
            if curr_i < sorted_key_frames[key_i]:
                key_i -= 1
            key_frame = sorted_key_frames[key_i]
            selected_frames_by_key_frame[key_frame].insert(0, curr_i)

        pbar_len = len(selected_frames_by_key_frame)

        for pbar_i, (key_frame, selected_frames) in enumerate(selected_frames_by_key_frame.items()):
            img = video_data[key_frame]
            label = self.apply_poly(video_label[curr_i - 1], video_polygon_label.get(curr_i - 1, {}))
            label = (label == 1).reshape((*label.shape, 1)) * np.ones((*label.shape, 3)) * 255
            test_image_list = [video_data[s] for s in selected_frames]

            test_labels = osvos_model.run(img, label, test_image_list)

            for t_label, t_frame in zip(test_labels, selected_frames, strict=True):
                video_label[t_frame] = (t_label > 0.9) * 1
                video_polygon_label[t_frame] = {}

            pbar.setValue(int((pbar_i + 1) / pbar_len * 100))

        self._model.video_label = video_label
        self._model.video_polygon_label = video_polygon_label
