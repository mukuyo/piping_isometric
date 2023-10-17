from pathlib import Path

import torch
from .datasets.imagefolder import ImageFolder, ImageList
from .datasets.video import Video
from .utils import utils as utils
from .utils import vis_utils as vis_utils
from .utils.model import create_model, parse_yolo_weights
import cv2

class Detector:
    def __init__(self, conf):
        self.cfg = conf
        config_path = Path(self.cfg['detect']['pipe_net']['config_path'])
        weights_path = Path(self.cfg['detect']['pipe_net']['weights_path'])

        # 設定ファイルを読み込む。
        self.config = utils.load_config(config_path)
        self.class_names = utils.load_classes(
            config_path.parent / self.config["model"]["class_names"]
        )

        # Device を作成する。
        self.device = utils.get_device(gpu_id=0)

        # モデルを作成する。
        model = create_model(self.config)
        if weights_path.suffix == ".weights":
            parse_yolo_weights(model, weights_path)
            print(f"Darknet format weights file loaded. {weights_path}")
        else:
            state = torch.load(weights_path)
            model.load_state_dict(state["model"])
            print(f"Checkpoint file {weights_path} loaded.")

        self.model = model.to(self.device).eval()

    def detect_from_path(self):
        img_size = self.config["test"]["img_size"]
        conf_threshold = self.config["test"]["conf_threshold"]
        nms_threshold = self.config["test"]["nms_threshold"]
        batch_size = self.config["test"]["batch_size"]

        # Dataset を作成する。
        path = Path(self.cfg['detect']['rgb_path'] + self.cfg['input_name'])
        path2 = Path(self.cfg['detect']['rgb_path'] + self.cfg['input_name'])

        # path = Path("9090.png")
        dataset = ImageFolder(path, img_size)

        # path2 = Path("908.png")
        dataset_2 = ImageFolder(path2, img_size)

        # DataLoader を作成する。
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size)
        dataloader_2 = torch.utils.data.DataLoader(dataset_2, batch_size=batch_size)

        # 推論する。
        img_paths, detections = [], []
        train_iter = iter(dataloader)
        train_iter_2 = iter(dataloader_2)

        # for inputs, pad_infos, paths in dataloader:
        inputs, pad_infos, paths = next(train_iter)
        inputs2, pad_infos2, paths2 = next(train_iter_2)

        inputs = inputs.to(self.device)
        inputs2 = inputs2.to(self.device)

        pad_infos = [x.to(self.device) for x in pad_infos]

        with torch.no_grad():
            outputs = self.model(inputs, inputs2)
            outputs = utils.postprocess(
                outputs, conf_threshold, nms_threshold, pad_infos
            )
            detections += [self.output_to_dict(x, self.class_names) for x in outputs]
            img_paths += paths

        return detections, img_paths

    def detect_from_imgs(self, imgs):
        img_size = self.config["test"]["img_size"]
        conf_threshold = self.config["test"]["conf_threshold"]
        nms_threshold = self.config["test"]["nms_threshold"]
        batch_size = self.config["test"]["batch_size"]

        # Dataset を作成する。
        dataset = ImageList(imgs, img_size)

        # DataLoader を作成する。
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size)

        # 推論する。
        detections = []
        for inputs, pad_infos in dataloader:
            inputs = inputs.to(self.device)
            pad_infos = [x.to(self.device) for x in pad_infos]

            with torch.no_grad():
                outputs = self.model(inputs)
                print("d")
                outputs = utils.postprocess(
                    outputs, conf_threshold, nms_threshold, pad_infos
                )

                detections += [self.output_to_dict(x, self.class_names) for x in outputs]

        return detections

    def detect_from_video(self, path):
        img_size = self.config["test"]["img_size"]
        conf_threshold = self.config["test"]["conf_threshold"]
        nms_threshold = self.config["test"]["nms_threshold"]
        batch_size = self.config["test"]["batch_size"]

        # Dataset を作成する。
        dataset = Video(path, img_size)

        # DataLoader を作成する。
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size)

        # 推論する。
        detections = []
        for inputs, pad_infos in dataloader:
            inputs = inputs.to(self.device)
            pad_infos = [x.to(self.device) for x in pad_infos]

            with torch.no_grad():
                outputs = self.model(inputs)
                outputs = utils.postprocess(
                    outputs, conf_threshold, nms_threshold, pad_infos
                )

                detections += [self.output_to_dict(x, self.class_names) for x in outputs]

        return detections

    def draw_boxes(self, img, detection):
        vis_utils.draw_boxes(img, detection, n_classes=len(self.class_names))
    
    def output_to_dict(self, output, class_names):
        detection = []
        for x1, y1, x2, y2, obj_conf, class_conf, label in output:
            bbox = {
                "confidence": float(obj_conf * class_conf),
                "class_id": int(label),
                "class_name": class_names[int(label)],
                "x1": float(x1),
                "y1": float(y1),
                "x2": float(x2),
                "y2": float(y2),
            }
            detection.append(bbox)

        return detection
