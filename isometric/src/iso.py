"""This is a generate isomeric program"""
from common.pipe import Pipe
from isometric.src.tool import are_facing_each_other
from isometric.opencv.draw import Draw

class Iso:
    """Isometric class"""
    def __init__(self, cfg) -> None:
        self.cfg = cfg
        # self.__draw = Draw()

    def generate_iso(self, pose_results: list) -> None:
        """generate_isometric"""
        pare_info = are_facing_each_other(pose_results)
        print(pare_info)
        print("Complete making piping isometric drawing!!") 
