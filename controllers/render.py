from controllers.pipeline import Job, Pipeline
import numpy as np
from typing import TYPE_CHECKING
import cv2

if TYPE_CHECKING:
    from models.model import Model
    from views.main_view import MainView

class RenderInput:
    ROOT = "root"
    IMAGE_INITIAL = "_image_initial"
    LABEL_INITIAL = "_label_initial"
    IMAGE_FRAME_INITIAL = "_image_frame_initial"
    IMAGE_ZOOM = "_image_zoom"
    LABEL_ZOOM = "_label_zoom"
    IMAGE_MOVE_AND_APPLY = "_image_move_and_apply"
    LABEL_MOVE_AND_APPLY = "_label_move_and_apply"
    SHOW = "show"

class Render:
    def __init__(self, model: "Model", view: "MainView"):
        self._pipeline = Pipeline(
            [
                Job(name=RenderInput.ROOT, stage=0, func=lambda:None, next_job_names=[RenderInput.IMAGE_INITIAL, RenderInput.LABEL_INITIAL, RenderInput.IMAGE_FRAME_INITIAL]),
                Job(name=RenderInput.IMAGE_INITIAL, stage=0, func=self._image_initial, next_job_names=[RenderInput.IMAGE_ZOOM]),
                Job(name=RenderInput.LABEL_INITIAL, stage=0, func=self._label_initial, next_job_names=[RenderInput.LABEL_ZOOM]),
                Job(name=RenderInput.IMAGE_FRAME_INITIAL, stage=0, func=self._image_frame_initial, next_job_names=[RenderInput.IMAGE_MOVE_AND_APPLY]),
                Job(name=RenderInput.IMAGE_ZOOM, stage=1, func=self._image_zoom, next_job_names=[RenderInput.IMAGE_MOVE_AND_APPLY]),
                Job(name=RenderInput.LABEL_ZOOM, stage=1, func=self._label_zoom, next_job_names=[RenderInput.LABEL_MOVE_AND_APPLY]),
                Job(name=RenderInput.IMAGE_MOVE_AND_APPLY, stage=2, func=self._image_move_and_apply, next_job_names=[RenderInput.LABEL_MOVE_AND_APPLY]),
                Job(name=RenderInput.LABEL_MOVE_AND_APPLY, stage=3, func=self._label_move_and_apply, next_job_names=[RenderInput.SHOW]),
                Job(name=RenderInput.SHOW, stage=4, func=self._show, next_job_names=[]),
            ]
        )
        self._model = model
        self.view = view

    def _image_initial(self):
        frame_num = self._model.frame_num
        self._model.render_data.initial_image = self._model.video_data[frame_num]
    
    def _label_initial(self):
        frame_num = self._model.frame_num
        self._model.render_data.initial_label = self._model.video_label[frame_num]
    
    def _zoom(self, img, ratio: int):
        if ratio > 1:
            # zoomin
            img = np.repeat(img, ratio, axis=0)
            img = np.repeat(img, ratio, axis=1)
        elif ratio < -1:
            # zoomout
            step = int(-ratio)
            start = step // 2
            img = img[start::step, start::step]
        return np.float32(img)
    
    def _apply_polygons(self, initial_label):
        initial_label = initial_label.copy()
        frame_num = self._model.frame_num
        label_polygons = (
            list(self._model.video_polygon_label.get(frame_num, {}).items())
            + list(self._model.video_polygon_label.get(-1, {}).items())
        )

        label_polygons = list(sorted(label_polygons, key=lambda x: x[0]))
        for label, polygons in label_polygons:
            for polygon in polygons:
                cv2.fillPoly(initial_label, pts = [np.array(polygon, dtype=np.int32)], color = label)
        return initial_label
    
    def _apply_polygon_corners(self, zoomed_label):
        zoom_ratio = self._model.zoom_ratio
        ratio = 1
        if zoom_ratio > 1:
            ratio = zoom_ratio
        elif zoom_ratio < -1:
            ratio = -1 / zoom_ratio

        label_polygons = list(self._model.video_polygon_label.get(-1, {}).items())
        for label, polygons in label_polygons:
            for polygon in polygons:
                for point in polygon:
                    x, y = round(point[0] * ratio), round(point[1] * ratio)
                    cv2.circle(zoomed_label, (x, y), 4, -1, 1)
        return zoomed_label

    def _image_zoom(self):
        zoom_ratio = self._model.zoom_ratio
        self._model.render_data.zoomed_image = self._zoom(self._model.render_data.initial_image, zoom_ratio)

    def _label_zoom(self):
        zoom_ratio = self._model.zoom_ratio
        initial_label = self._model.render_data.initial_label
        initial_label = self._apply_polygons(initial_label)
        zoomed_label = self._zoom(initial_label, zoom_ratio)
        zoomed_label = self._apply_polygon_corners(zoomed_label)
        self._model.render_data.zoomed_label = zoomed_label

    def _image_frame_initial(self):
        image_frame_height=self.view._ui.image_frame.rect().bottom()
        image_frame_width=self.view._ui.image_frame.rect().right()
        self._model.render_data.initial_image_frame = np.zeros((image_frame_height, image_frame_width, 3), dtype="uint8") + 128

    def _move_and_apply(self, frm, to, alpha):
        image = frm
        image_frame = to.copy()
        image_h, image_w, _ = image.shape
        frame_h, frame_w, _ = image_frame.shape
        move_y, move_x = self._model.coordinates

        zoom_ratio = self._model.zoom_ratio if self._model.zoom_ratio > 0 else -1 / self._model.zoom_ratio
        move_x = move_x * zoom_ratio
        move_y = move_y * zoom_ratio

        image_left_edge = - image_w / 2 + move_x
        image_right_edge = image_w / 2 + move_x
        image_top_edge = - image_h / 2 + move_y
        image_bottom_edge = image_h / 2 + move_y

        frame_left_edge = - frame_w / 2
        frame_right_edge = frame_w / 2
        frame_top_edge = - frame_h / 2
        frame_bottom_edge = frame_h / 2

        inter_x0 = max(image_left_edge, frame_left_edge)
        inter_y0 = max(image_top_edge, frame_top_edge)
        inter_x1 = min(image_right_edge, frame_right_edge)
        inter_y1 = min(image_bottom_edge, frame_bottom_edge)

        image_x0 = min(int(inter_x0 + image_w / 2 - move_x + 0.01), image_w)
        image_y0 = min(int(inter_y0 + image_h / 2 - move_y + 0.01), image_h)
        image_x1 = max(int(inter_x1 + image_w / 2 - move_x + 0.01), 0)
        image_y1 = max(int(inter_y1 + image_h / 2 - move_y + 0.01), 0)
        
        frame_x0 = int(inter_x0 + frame_w / 2 + 0.01)
        frame_y0 = int(inter_y0 + frame_h / 2 + 0.01)
        frame_x1 = frame_x0 + image_x1 - image_x0
        frame_y1 = frame_y0 + image_y1 - image_y0

        image_frame[int(frame_y0):int(frame_y1), int(frame_x0): int(frame_x1)] = (
            image_frame[int(frame_y0):int(frame_y1), int(frame_x0): int(frame_x1)] * (1 - alpha) + 
            image[int(image_y0):int(image_y1), int(image_x0):int(image_x1)] * alpha
        ).astype("uint8")

        x_t = frame_x0 - image_x0
        y_t = frame_y0 - image_y0
        return image_frame, (y_t, x_t)

    def _image_move_and_apply(self):
        initial_image_frame2, top_left_image_coordinates = self._move_and_apply(
            self._model.render_data.zoomed_image,
            self._model.render_data.initial_image_frame,
            1,
        )
        self._model.top_left_image_coordinates = top_left_image_coordinates
        self._model.render_data.initial_image_frame2 = initial_image_frame2
    
    def _label_move_and_apply(self):
        zoomed_label = self._model.render_data.zoomed_label
        zoomed_label_image = np.zeros((*zoomed_label.shape, 3))

        zoomed_label_image[zoomed_label==-1] = [255, 255, 255]
        zoomed_label_image[zoomed_label==1] = [0, 0, 255]
        zoomed_label_image[zoomed_label==2] = [0, 255, 0]
        zoomed_label_image[zoomed_label==3] = [255, 0, 0]

        self._model.render_data.image_frame, _ = self._move_and_apply(
            zoomed_label_image, self._model.render_data.initial_image_frame2, self._model.alpha / 100
        )

    def _show(self):
        self._model.image_frame = self._model.render_data.image_frame

    def __call__(self, inputs:list[RenderInput]):
        self._pipeline.run(job_names=inputs)
