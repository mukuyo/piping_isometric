"""This is a main script"""
from logging import getLogger, DEBUG, StreamHandler, Formatter
import sys
import yaml
from detection import create_detector
from pose.src.predict import Pose
from isometric.src.iso import Iso

class Main:
    """Main class"""
    def __init__(self, _cfg, _logger):
        self.cfg = _cfg
        self.logger = _logger
        self.detect = create_detector(self.cfg)
        self.pose = Pose(self.cfg)
        self.isometric = Iso(self.cfg, self.logger)

    def run(self):
        """run program"""
        detection_results = self.detect.run_detect()
        pose_results = self.pose.predict(results=detection_results)
        # self.isometric.generate_iso(pose_results)


if __name__ == "__main__":
    fmt = Formatter("[%(levelname)s] %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = getLogger(__name__)
    logger.setLevel(DEBUG)
    handler = StreamHandler(sys.stderr)
    handler.setFormatter(fmt)
    handler.setLevel(DEBUG)
    logger.addHandler(handler)

    with open('./config/main.yaml', 'r', encoding="utf8") as yml:
        cfg = yaml.safe_load(yml)

    logger.info('init model')
    main = Main(cfg, logger)

    logger.info('start predict')
    main.run()
    logger.info('end predict')
