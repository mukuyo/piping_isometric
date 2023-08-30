"""This is a generate isomeric program"""
from isometric.opencv.draw import Draw
from isometric.src.tool import Utils

class Iso(Utils):
    """Isometric class"""
    def __init__(self, cfg) -> None:
        super().__init__()
        self.cfg = cfg
        self.__draw = Draw(self.cfg)

    def generate_iso(self, pose_results: list) -> None:
        """generate_isometric"""
        pare_info, isometric_info = self.line_detect(pose_results)
        self.__draw.line_2d(pare_info)
        self.__draw.isometric(isometric_info)
        print("Complete making piping isometric drawing!!")
