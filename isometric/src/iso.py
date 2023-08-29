"""This is a generate isomeric program"""
from isometric.opencv.draw import Draw
from isometric.src.tool import Utils

class Iso(Utils):
    """Isometric class"""
    def __init__(self, cfg) -> None:
        super().__init__()
        self.cfg = cfg
        self.__draw = Draw()

    def generate_iso(self, pose_results: list) -> None:
        """generate_isometric"""
        pare_info = self.line_detect(pose_results)
        self.__draw.line_2d(pare_info, pose_results)
        print("Complete making piping isometric drawing!!")
