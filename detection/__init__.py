from detection.pipe_net.detect import PipeNet
from detection.yolov8.detect import Yolov8


def create_detector(cfg):
    """generate pipe network"""
    if cfg['detect_method'] == 'pipe_net':
        return PipeNet(cfg)
    else:
        return Yolov8(cfg)
